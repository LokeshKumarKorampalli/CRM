from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import leads_collection, emails_collection
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from config import SECRET_KEY
import requests
import json
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)

# ================= SESSION DECORATORS =================

def login_required_buyer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'buyer_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('buyer_entry'))
        return f(*args, **kwargs)
    return decorated_function


# def login_required_agent(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'agent_id' not in session:
#             flash('Please log in as an agent to continue.', 'warning')
#             return redirect(url_for('agent_login'))
#         return f(*args, **kwargs)
#     return decorated_function


# ================= LLM CORE =================

def call_ollama(lead):
    conversation = lead.get("conversation", [])

    prompt = """
You are an intelligent real estate AI agent inside a CRM.

Rules:
- Ask ONE important question at a time.
- Be concise.
- Keep replies under 4 sentences.
"""

    prompt += f"""
Lead Data:
Budget: {lead.get("budget")}
Timeline: {lead.get("timeline_months")}
Property Type: {lead.get("property_type")}
Location: {lead.get("location")}
Recommended Action: {lead.get("recommended_action")}

Conversation:
"""

    for msg in conversation:
        role = "Buyer" if msg["role"] == "buyer" else "Assistant"
        prompt += f"{role}: {msg['message']}\n"

    prompt += "\nAssistant:"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except:
        return "I'm experiencing a temporary issue. Please try again shortly."


# ================= EXTRACTION =================

def incremental_extract(lead):
    conversation = lead.get("conversation", [])

    prompt = f"""
Extract structured CRM data from conversation.
Only update fields explicitly mentioned.
Return ONLY valid JSON.

Schema:
{{
  "budget": number or null,
  "location": string or null,
  "property_type": string or null,
  "timeline_months": number or null
}}

Conversation:
"""

    for msg in conversation:
        prompt += f"{msg['role']}: {msg['message']}\n"

    prompt += "\nJSON:"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False,
                "temperature": 0
            },
            timeout=60
        )
        response.raise_for_status()

        raw = response.json().get("response", "").strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == -1:
            return {}

        return json.loads(raw[start:end])
    except:
        return {}


# ================= CHAT COMPLETION =================

def decide_chat_completion(lead):
    conversation = lead.get("conversation", [])

    prompt = f"""
Decide if buyer conversation is complete.

Complete only if:
- Budget known
- Timeline known
- Property type known
- Buyer clearly confirms no more questions

Return ONLY:
{{ "chat_completed": true or false }}

Structured:
Budget: {lead.get("budget")}
Timeline: {lead.get("timeline_months")}
Property Type: {lead.get("property_type")}

Conversation:
"""

    for msg in conversation:
        prompt += f"{msg['role']}: {msg['message']}\n"

    prompt += "\nJSON:"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False,
                "temperature": 0
            },
            timeout=60
        )

        response.raise_for_status()
        raw = response.json().get("response", "").strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == -1:
            return False

        result = json.loads(raw[start:end])
        return result.get("chat_completed", False)

    except:
        return False


# ================= EMAIL LOG =================

def generate_buyer_summary(lead):
    lines = []

    if lead.get("location"):
        lines.append(f"• Preferred Location: {lead['location']}")

    if lead.get("budget"):
        lines.append(f"• Budget: {lead['budget']}")

    if lead.get("property_type"):
        lines.append(f"• Property Type: {lead['property_type']}")

    if lead.get("timeline_months"):
        lines.append(f"• Expected Timeline: {lead['timeline_months']} month(s)")

    return "\n".join(lines)


def create_summary_email(lead):
    try:
        print(">>> create_summary_email triggered for lead:", lead.get("_id"))
        summary = generate_buyer_summary(lead)
        subject = "Your Property Inquiry Summary – AI Estate"
        body = f"""
Hi {lead.get("name")},

Thank you for discussing your property requirements with us.

Here’s a summary:

{summary}

An agent will contact you shortly.

AI Estate Team
"""
        email_doc = {
            "lead_id": lead["_id"],
            "lead_name": lead.get("name"),
            "to": lead.get("email"),
            "subject": subject,
            "body": body.strip(),
            "sent_at": datetime.utcnow()
        }

        # Try to insert and print outcome
        result = emails_collection.insert_one(email_doc)
        print(">>> emails_collection.inserted_id:", result.inserted_id)
    except Exception as e:
        print("!!! create_summary_email ERROR:", repr(e))


# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/buyer")
def buyer_entry():
    return render_template("buyer_entry.html")


@app.route("/buyer/register", methods=["GET", "POST"])
def buyer_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        existing = leads_collection.find_one({"email": email})
        if existing:
            flash("Email already registered.", "warning")
            return redirect(url_for("buyer_entry"))

        lead = {
            "name": name,
            "email": email,
            "phone": phone,
            "conversation": [],
            "budget": None,
            "location": None,
            "property_type": None,
            "timeline_months": None,

            # ADD THESE DEFAULTS
            "lead_score": 0,
            "recommended_action": None,
            "decision_reason": None,
            "decision_confidence": None,
            "extra_details": [],
            "meeting_time": None,

            "chat_completed": False,
            "status": "Cold",
            "created_at": datetime.utcnow()
        }


        result = leads_collection.insert_one(lead)

        session.permanent = True
        session["buyer_id"] = str(result.inserted_id)
        session["buyer_name"] = name

        return redirect(url_for("chat", lead_id=result.inserted_id))

    return render_template("buyer_register.html")


@app.route("/buyer/login", methods=["GET", "POST"])
def buyer_login():
    if request.method == "POST":
        email = request.form["identifier"]

        lead = leads_collection.find_one({"email": email})
        if not lead:
            flash("Account not found.", "error")
            return redirect(url_for("buyer_entry"))

        session.permanent = True
        session["buyer_id"] = str(lead["_id"])
        session["buyer_name"] = lead["name"]

        return redirect(url_for("chat", lead_id=lead["_id"]))

    return render_template("buyer_login.html")


@app.route("/chat/<lead_id>", methods=["GET", "POST"])
@login_required_buyer
def chat(lead_id):
    if session.get("buyer_id") != lead_id:
        return redirect(url_for("buyer_entry"))

    lead = leads_collection.find_one({"_id": ObjectId(lead_id)})
    if not lead:
        return "Not found", 404

    if lead.get("chat_completed"):
        return render_template("chat.html", lead=lead)

    if request.method == "POST":
        message = request.form["message"]

        leads_collection.update_one(
            {"_id": ObjectId(lead_id)},
            {"$push": {"conversation": {
                "role": "buyer",
                "message": message,
                "timestamp": datetime.utcnow()
            }}}
        )

        lead = leads_collection.find_one({"_id": ObjectId(lead_id)})

        updates = incremental_extract(lead)
        if updates:
            leads_collection.update_one({"_id": ObjectId(lead_id)}, {"$set": updates})

        lead = leads_collection.find_one({"_id": ObjectId(lead_id)})

        ai_reply = call_ollama(lead)

        leads_collection.update_one(
            {"_id": ObjectId(lead_id)},
            {"$push": {"conversation": {
                "role": "assistant",
                "message": ai_reply,
                "timestamp": datetime.utcnow()
            }}}
        )

        lead = leads_collection.find_one({"_id": ObjectId(lead_id)})

        if decide_chat_completion(lead):
            create_summary_email(lead)

            leads_collection.update_one(
                {"_id": ObjectId(lead_id)},
                {"$set": {
                    "chat_completed": True,
                    "status": "Summary Sent",
                    "completed_at": datetime.utcnow()
                }}
            )

            leads_collection.update_one(
                {"_id": ObjectId(lead_id)},
                {"$push": {"conversation": {
                    "role": "assistant",
                    "message": "Thank you. We've emailed you a summary. An agent will contact you shortly.",
                    "timestamp": datetime.utcnow()
                }}}
            )

        return redirect(url_for("chat", lead_id=lead_id))

    return render_template("chat.html", lead=lead)


# @app.route("/agent/login", methods=["GET", "POST"])
# def agent_login():
#     if request.method == "POST":
#         email = request.form["email"]

#         if not (email.endswith("@agent.com") or email.endswith("@aiestate.com")):
#             flash("Invalid agent email.", "error")
#             return redirect(url_for("agent_login"))

#         session.permanent = True
#         session["agent_id"] = email
#         session["agent_name"] = email.split("@")[0].title()

#         return redirect(url_for("dashboard"))

#     return render_template("agent_login.html")

@app.route("/_debug/emails")
def debug_emails():
    docs = list(emails_collection.find().sort("sent_at", -1).limit(50))
    # Convert ObjectId / datetime to strings for safe rendering
    for d in docs:
        d["lead_id"] = str(d.get("lead_id"))
        d["_id"] = str(d.get("_id"))
        if "sent_at" in d:
            d["sent_at"] = d["sent_at"].isoformat()
    return {"count": len(docs), "emails": docs}

@app.route("/dashboard")
# @login_required_agent
def dashboard():
    leads = list(leads_collection.find().sort("created_at", -1))
    return render_template("dashboard.html", leads=leads)

@app.route("/analytics")
def analytics():
    leads = list(leads_collection.find())

    total = len(leads)

    hot = 0
    warm = 0
    cold = 0

    # Buckets
    budget_buckets = {
        "<500k": 0,
        "500k-1M": 0,
        ">1M": 0
    }

    timeline_buckets = {
        "≤1 Month": 0,
        "2-3 Months": 0,
        "4-6 Months": 0,
        ">6 Months": 0
    }

    action_counts = {}
    preference_counts = {}

    for lead in leads:

        # ---- STATUS COUNT ----
        status = lead.get("status", "Cold")
        if status == "Hot":
            hot += 1
        elif status == "Warm":
            warm += 1
        else:
            cold += 1

        # ---- BUDGET BUCKETS ----
        budget = lead.get("budget")
        if budget:
            if budget < 500000:
                budget_buckets["<500k"] += 1
            elif budget <= 1000000:
                budget_buckets["500k-1M"] += 1
            else:
                budget_buckets[">1M"] += 1

        # ---- TIMELINE BUCKETS ----
        timeline = lead.get("timeline_months")
        if timeline:
            if timeline <= 1:
                timeline_buckets["≤1 Month"] += 1
            elif timeline <= 3:
                timeline_buckets["2-3 Months"] += 1
            elif timeline <= 6:
                timeline_buckets["4-6 Months"] += 1
            else:
                timeline_buckets[">6 Months"] += 1

        # ---- ACTION COUNTS ----
        action = lead.get("recommended_action")
        if action:
            action_counts[action] = action_counts.get(action, 0) + 1

        # ---- PREFERENCE COUNTS ----
        for pref in lead.get("extra_details", []):
            preference_counts[pref] = preference_counts.get(pref, 0) + 1

    return render_template(
        "analytics.html",
        total=total,
        hot=hot,
        warm=warm,
        cold=cold,
        budget_buckets=budget_buckets,
        timeline_buckets=timeline_buckets,
        action_counts=action_counts,
        preference_counts=preference_counts
    )

@app.route("/lead/<lead_id>")
def lead_view(lead_id):
    lead = leads_collection.find_one({"_id": ObjectId(lead_id)})
    if not lead:
        return "Lead not found", 404
    return render_template("lead_view.html", lead=lead)


if __name__ == "__main__":
    app.run(debug=True)
