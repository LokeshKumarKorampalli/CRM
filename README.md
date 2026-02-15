# 🏠 AI Real Estate CRM

> An intelligent, AI-powered Customer Relationship Management system for real estate agents and buyers, featuring automated lead scoring, conversational AI, and comprehensive analytics.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-4.0+-brightgreen.svg)
![Ollama](https://img.shields.io/badge/Ollama-LLaMA3-orange.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [AI Components](#ai-components)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

AI Real Estate CRM is a modern, AI-first customer relationship management system designed specifically for the real estate industry. It leverages large language models (LLMs) to automate lead qualification, extract structured data from natural conversations, and provide intelligent recommendations to agents.

### Key Capabilities

- 🤖 **Conversational AI**: Natural language chat interface powered by LLaMA 3
- 📊 **Smart Lead Scoring**: Automatic lead classification (Hot/Warm/Cold)
- 🎯 **Intelligent Extraction**: Extracts budget, timeline, preferences from conversations
- 📧 **Automated Follow-ups**: Generates and sends summary emails
- 📈 **Executive Analytics**: Comprehensive dashboard with actionable insights
- ⚡ **Real-time Updates**: Live chat with streaming responses
- 🔒 **Session Management**: Secure buyer and agent authentication

---

## ✨ Features

### For Buyers

- **Easy Registration**: Simple 3-field registration (name, email, phone)
- **Conversational Search**: Chat naturally about property requirements
- **Smart Questions**: AI asks relevant questions to understand needs
- **Progress Tracking**: See conversation history and extracted details
- **Email Summaries**: Receive detailed summary of your requirements

### For Agents

- **Lead Dashboard**: View all leads with key information at a glance
- **Lead Scoring**: Automatic Hot/Warm/Cold classification
- **AI Recommendations**: Get suggested actions for each lead
- **Search & Filter**: Find leads by status, budget, timeline, etc.
- **Analytics Dashboard**: Visualize pipeline with interactive charts
- **Lead Details**: Comprehensive view of each lead's profile

### AI Capabilities

- **Natural Language Understanding**: Extracts structured data from conversations
- **Context Awareness**: Maintains conversation context across messages
- **Intelligent Questioning**: Asks one relevant question at a time
- **Completion Detection**: Knows when conversation is complete
- **Email Generation**: Creates professional summary emails automatically

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Home   │  │  Buyer   │  │Dashboard │  │Analytics │   │
│  │  Page    │  │  Portal  │  │          │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      Flask Backend                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Routes: /, /buyer, /chat, /dashboard, /analytics   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Session Management & Authentication                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      AI Layer (Ollama)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Conversation │  │  Extraction  │  │  Completion  │      │
│  │   Handler    │  │    Engine    │  │   Detector   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                   LLaMA 3 (8B model)                         │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      MongoDB Database                        │
│  ┌──────────────┐                  ┌──────────────┐         │
│  │    Leads     │                  │    Emails    │         │
│  │  Collection  │                  │  Collection  │         │
│  └──────────────┘                  └──────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **Flask 2.0+**: Python web framework
- **Python 3.8+**: Programming language
- **MongoDB**: NoSQL database for lead and email storage
- **PyMongo**: MongoDB driver for Python

### AI/ML
- **Ollama**: Local LLM inference server
- **LLaMA 3 (8B)**: Large language model for conversations
- **JSON Extraction**: Structured data extraction from LLM outputs

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with custom properties
- **JavaScript (Vanilla)**: Interactive functionality
- **Chart.js**: Data visualization for analytics

### Fonts & Icons
- **Inter**: Modern sans-serif font for UI
- **Playfair Display**: Elegant serif font for headings
- **Emoji Icons**: Native emoji for visual elements

---

## 📦 Installation

### Prerequisites

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **MongoDB 4.0+**
   ```bash
   # Install MongoDB Community Edition
   # macOS
   brew tap mongodb/brew
   brew install mongodb-community

   # Ubuntu
   sudo apt-get install mongodb

   # Start MongoDB
   mongod --dbpath /path/to/data/db
   ```

3. **Ollama with LLaMA 3**
   ```bash
   # Install Ollama from https://ollama.ai
   
   # Pull LLaMA 3 model (8B)
   ollama pull llama3:8b
   
   # Start Ollama server
   ollama serve
   ```

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ai-real-estate-crm.git
   cd ai-real-estate-crm
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install flask pymongo requests python-dotenv
   ```

4. **Create Configuration Files**

   Create `config.py`:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
   MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
   ```

   Create `models.py`:
   ```python
   from pymongo import MongoClient
   from config import MONGO_URI
   
   client = MongoClient(MONGO_URI)
   db = client['real_estate_crm']
   
   leads_collection = db['leads']
   emails_collection = db['emails']
   ```

   Create `.env`:
   ```env
   SECRET_KEY=your-super-secret-key-change-this
   MONGO_URI=mongodb://localhost:27017/
   ```

5. **Create Directory Structure**
   ```bash
   mkdir -p static templates
   
   # Move HTML files to templates/
   # Move CSS files to static/
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```

7. **Access the Application**
   ```
   Open browser: http://localhost:5000
   ```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=real_estate_crm

# Ollama Configuration
OLLAMA_API_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3:8b
OLLAMA_TIMEOUT=60

# Session Configuration
SESSION_LIFETIME_HOURS=24

# Email Configuration (if implementing email sending)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'real_estate_crm')
    
    # Ollama
    OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3:8b')
    OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', '60'))
    
    # Session
    PERMANENT_SESSION_LIFETIME = int(os.getenv('SESSION_LIFETIME_HOURS', '24')) * 3600
```

---

## 🚀 Usage

### For Buyers

1. **Start Chat**
   - Go to homepage
   - Click "I'm a Buyer"
   - Register with name, email, phone
   - Or login if returning

2. **Chat with AI**
   - Answer AI's questions naturally
   - Provide budget, timeline, preferences
   - AI extracts information automatically

3. **Review & Continue**
   - See conversation history
   - Receive email summary when complete
   - Agent will follow up

### For Agents

1. **Access Dashboard**
   - Go to homepage
   - Click "I'm an Agent"
   - View all leads

2. **Manage Leads**
   - See lead scores and status
   - Filter by Hot/Warm/Cold
   - Search by name, email, budget
   - View AI recommendations

3. **View Analytics**
   - Click "View Analytics"
   - See budget distribution
   - Analyze timeline patterns
   - Review recommended actions

4. **Lead Details**
   - Click on any lead card
   - View complete profile
   - See AI decision reasoning
   - Check buyer preferences

---

## 📁 Project Structure

```
ai-real-estate-crm/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .gitignore                 # Git ignore rules
├── README.md                   # This file
│
├── static/                     # Static files
│   ├── style.css              # Main stylesheet
│   └── images/                # Image assets
│
├── templates/                  # HTML templates
│   ├── home.html              # Landing page
│   ├── buyer_entry.html       # Buyer login/register
│   ├── buyer_register.html    # Registration form
│   ├── chat.html              # Chat interface
│   ├── dashboard.html         # Agent dashboard
│   ├── analytics.html         # Analytics dashboard
│   └── lead_view.html         # Individual lead view
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── llm.py                 # LLM integration
│   ├── extraction.py          # Data extraction
│   └── email_generator.py     # Email generation
│
└── tests/                      # Unit tests
    ├── __init__.py
    ├── test_routes.py
    ├── test_llm.py
    └── test_extraction.py
```

---

## 🤖 AI Components

### 1. Conversation Handler (`call_ollama`)

**Purpose**: Manages natural conversation flow with buyers

**How it works**:
```python
def call_ollama(lead):
    # Build context from lead data
    prompt = build_prompt(lead)
    
    # Call Ollama API
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:8b",
            "prompt": prompt,
            "temperature": 0.3  # Consistent responses
        }
    )
    
    return response.json()["response"]
```

**Features**:
- Context-aware responses
- One question at a time
- Concise (under 4 sentences)
- Natural conversation flow

### 2. Data Extraction (`incremental_extract`)

**Purpose**: Extracts structured data from conversations

**Schema**:
```json
{
  "budget": number,
  "location": string,
  "property_type": string,
  "timeline_months": number
}
```

**How it works**:
- Analyzes full conversation history
- Only updates explicitly mentioned fields
- Returns valid JSON
- Incremental updates with each message

### 3. Completion Detector (`decide_chat_completion`)

**Purpose**: Determines when conversation is complete

**Completion Criteria**:
- ✅ Budget known
- ✅ Timeline known
- ✅ Property type known
- ✅ Buyer confirms no more questions

**Actions on Completion**:
1. Generate summary email
2. Update lead status to "Summary Sent"
3. Mark conversation as complete
4. Timestamp completion

---

## 🌐 API Endpoints

### Public Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/buyer` | Buyer portal entry |
| GET/POST | `/buyer/register` | New buyer registration |
| GET/POST | `/buyer/login` | Returning buyer login |

### Authenticated Routes (Buyer)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET/POST | `/chat/<lead_id>` | Chat interface | ✅ Buyer session |

### Dashboard Routes (Agent)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard` | Agent dashboard with all leads |
| GET | `/analytics` | Analytics dashboard |
| GET | `/lead/<lead_id>` | Individual lead detail view |

### Debug Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/_debug/emails` | View email collection (JSON) |

---

## 🗄️ Database Schema

### Leads Collection

```javascript
{
  _id: ObjectId,
  name: String,              // Buyer name
  email: String,             // Buyer email (unique)
  phone: String,             // Buyer phone
  
  // Conversation
  conversation: [
    {
      role: String,          // "buyer" or "assistant"
      message: String,       // Message text
      timestamp: DateTime    // Message time
    }
  ],
  
  // Extracted Data
  budget: Number,            // Budget in dollars
  location: String,          // Preferred location
  property_type: String,     // e.g., "Single Family", "Condo"
  timeline_months: Number,   // Timeline in months
  
  // AI Scoring
  lead_score: Number,        // 0-100
  recommended_action: String, // AI-suggested action
  decision_reason: String,   // Why AI scored this way
  decision_confidence: Float, // 0.0-1.0
  extra_details: [String],   // Additional preferences
  
  // Meeting
  meeting_time: String,      // Scheduled meeting time
  available_slots: [String], // Proposed time slots
  
  // Status
  chat_completed: Boolean,   // Conversation complete?
  status: String,            // "Hot", "Warm", "Cold", "Summary Sent"
  
  // Timestamps
  created_at: DateTime,      // Lead created
  completed_at: DateTime     // Chat completed
}
```

### Emails Collection

```javascript
{
  _id: ObjectId,
  lead_id: ObjectId,         // Reference to lead
  lead_name: String,         // Buyer name
  to: String,                // Recipient email
  subject: String,           // Email subject
  body: String,              // Email body
  sent_at: DateTime          // When email was sent
}
```

---

## 📊 Analytics Features

### Dashboard Metrics

1. **Total Leads**: Count of all leads in system
2. **Hot Leads**: High-priority leads (score ≥ 75)
3. **Warm Leads**: Medium-priority leads (40 ≤ score < 75)
4. **Cold Leads**: Low-priority leads (score < 40)

### Visualizations

1. **Budget Distribution** (Bar Chart)
   - <$500k
   - $500k-$1M
   - >$1M

2. **Timeline Distribution** (Bar Chart)
   - ≤1 Month
   - 2-3 Months
   - 4-6 Months
   - >6 Months

3. **Recommended Actions** (Doughnut Chart)
   - Distribution of AI-suggested actions

4. **Status Overview** (Pie Chart)
   - Hot/Warm/Cold distribution

5. **Top Buyer Preferences**
   - Most common requirements and preferences

---

## 🖼️ Screenshots

### Home Page
Beautiful landing page with AI-powered features showcase, statistics, and clear CTAs.

### Buyer Portal
Split-screen design for new buyer registration and returning buyer login.

### Chat Interface
Real-time conversational AI with streaming responses and message history.

### Agent Dashboard
Comprehensive lead management with filtering, search, and lead scoring.

### Analytics Dashboard
Interactive charts showing budget distribution, timeline analysis, and AI recommendations.

### Lead Detail View
Complete lead profile with AI decision engine, buyer requirements, and action history.

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Ollama Connection Error

**Symptom**: "I'm experiencing a temporary issue"

**Solutions**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/generate

# Start Ollama
ollama serve

# Verify model is installed
ollama list | grep llama3

# Pull model if missing
ollama pull llama3:8b
```

#### 2. MongoDB Connection Error

**Symptom**: Cannot connect to database

**Solutions**:
```bash
# Check if MongoDB is running
mongosh

# Start MongoDB
mongod --dbpath /path/to/data/db

# Check connection string in .env
MONGO_URI=mongodb://localhost:27017/
```

#### 3. Session Errors

**Symptom**: "Please log in to continue"

**Solutions**:
- Clear browser cookies
- Check SECRET_KEY in config
- Ensure session lifetime is set
- Restart Flask application

#### 4. Chat Not Responding

**Symptom**: Messages sent but no AI response

**Solutions**:
1. Check Ollama logs: `ollama logs`
2. Verify timeout settings
3. Check network connectivity
4. Test LLM directly: `ollama run llama3:8b`

#### 5. Extraction Not Working

**Symptom**: Lead data not being extracted

**Solutions**:
- Check LLM response format
- Verify JSON parsing
- Review extraction prompts
- Check conversation structure

---

## 🚀 Future Enhancements

### Planned Features

#### Short Term (1-2 months)
- [ ] Email sending integration (SMTP)
- [ ] SMS notifications via Twilio
- [ ] Property listings integration
- [ ] Calendar integration for meetings
- [ ] Export leads to CSV
- [ ] Dark mode toggle

#### Medium Term (3-6 months)
- [ ] Multi-agent support with roles
- [ ] Advanced lead scoring algorithm
- [ ] Property recommendation engine
- [ ] Automated email campaigns
- [ ] Video call scheduling
- [ ] Document uploads (ID, proof of funds)

#### Long Term (6-12 months)
- [ ] Mobile app (React Native)
- [ ] Voice chat integration
- [ ] Multi-language support
- [ ] Integration with MLS systems
- [ ] Predictive analytics
- [ ] Advanced reporting tools
- [ ] API for third-party integrations

### Potential Improvements

**AI Enhancements**:
- GPT-4 integration as alternative
- Fine-tuned model for real estate
- Sentiment analysis
- Intent classification
- Automated objection handling

**User Experience**:
- Progressive web app (PWA)
- Offline mode
- Real-time notifications
- Voice input
- Chatbot personality customization

**Analytics**:
- Conversion tracking
- A/B testing framework
- Lead source tracking
- Agent performance metrics
- Revenue forecasting

**Security**:
- Two-factor authentication (2FA)
- Role-based access control (RBAC)
- Audit logs
- Data encryption
- GDPR compliance tools

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 for Python code
- Write tests for new features
- Update documentation
- Use meaningful commit messages
- Keep PRs focused and small

### Code Style

```python
# Good
def extract_lead_data(conversation):
    """Extract structured data from conversation.
    
    Args:
        conversation: List of message dictionaries
        
    Returns:
        Dictionary with extracted fields
    """
    # Implementation
    pass

# Bad
def extract(c):
    # No docstring, unclear parameter
    pass
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 AI Real Estate CRM

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **Ollama Team** - For making local LLM inference accessible
- **Meta AI** - For the LLaMA 3 model
- **Flask Community** - For the excellent web framework
- **MongoDB** - For flexible NoSQL database
- **Chart.js** - For beautiful data visualizations

---

## 📞 Support

### Documentation
- Full API documentation: `/docs` (coming soon)
- Video tutorials: [YouTube Channel](https://youtube.com)
- Blog posts: [Blog](https://blog.example.com)

### Contact
- Email: support@aiestate.example.com
- Discord: [Join Server](https://discord.gg/example)
- GitHub Issues: [Report Bug](https://github.com/username/repo/issues)

### Community
- Discussion Forum: [Forum Link](https://forum.example.com)
- Reddit: r/AIRealEstateCRM
- Twitter: @AIEstateCRM

---

## 📈 Project Status

- **Version**: 1.0.0
- **Status**: Active Development
- **Last Updated**: February 2024
- **Stability**: Beta

### Version History

**v1.0.0** (February 2024)
- Initial release
- Core chat functionality
- Lead dashboard
- Analytics dashboard
- AI-powered lead scoring

**v0.9.0** (January 2024)
- Beta release
- UI improvements
- Bug fixes
- Performance optimization

---
[⬆ Back to Top](#-ai-real-estate-crm)

</div>
