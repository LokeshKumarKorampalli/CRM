from models import leads_collection
from datetime import datetime
import random

leads_collection.delete_many({})  # clears old data (optional)

statuses = ["Hot", "Warm", "Cold"]
actions = ["propose_meeting", "ask_budget", "ask_timeline", "schedule_followup", "long_term_nurture"]
property_types = ["2BHK", "3BHK", "Villa", "Apartment"]
locations = ["Austin", "Dallas", "Houston", "San Antonio"]
preferences_pool = ["garage", "near good school", "balcony", "pet friendly", "pool", "garden", "downtown", "lake view"]

for i in range(40):
    budget = random.choice([400000, 550000, 650000, 750000, 900000, None])
    timeline = random.choice([1, 2, 3, 6, 12, None])
    intent_score = random.choice([None, 6, 7, 8, 9])

    extra_details = random.sample(preferences_pool, random.randint(1, 3))

    lead = {
        "name": f"Lead_{i}",
        "email": f"lead{i}@mail.com",
        "phone": str(1000000000 + i),
        "conversation": [],
        "execution_trace": [],
        "budget": budget,
        "location": random.choice(locations),
        "property_type": random.choice(property_types),
        "timeline_months": timeline,
        "intent_score": intent_score,
        "risk_flags": [],
        "extra_details": extra_details,
        "lead_score": random.randint(20, 95),
        "status": random.choice(statuses),
        "recommended_action": random.choice(actions),
        "decision_reason": "Auto-generated sample",
        "decision_confidence": round(random.uniform(0.6, 0.95), 2),
        "meeting_time": None,
        "available_slots": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    leads_collection.insert_one(lead)

print("Sample data inserted successfully.")
