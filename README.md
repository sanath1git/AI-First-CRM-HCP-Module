# AI-First-CRM-HCP-Module


An intelligent Customer Relationship Management (CRM) system designed specifically for pharmaceutical field representatives to log, manage, and get AI-powered guidance on their interactions with Healthcare Professionals (HCPs).

## 🎯 Key Features

### Two Parallel Input Modes
1. **Structured Form** - Traditional discrete field input for precision and speed
2. **Natural Language Chat** - Conversational AI interface that automatically fills the form

### 8 LangGraph AI Tools

1. **Log Interaction** (Mandatory) - Extracts structured data from natural language using Groq LLM (gemma2-9b-it)
2. **Edit Interaction** (Mandatory) - Allows modification of logged interactions with semantic validation
3. **Retrieve Interaction** - Search and retrieve past interactions by various criteria
4. **Sentiment Analyzer** - Scores HCP receptiveness on a 1-5 scale
5. **Schedule Follow-up** - Manages follow-up actions and reminders
6. **HCP Profile Lookup** - Queries HCP profiles by NPI or name
7. **Compliance Checker** - Scans for regulatory violations (critical for pharma)
8. **Next Best Action** - AI-powered recommendations using llama-3.3-70b-versatile

## 🏗️ Architecture

### Frontend
- **React** with **Redux** for state management
- Two synchronized UI components: InteractionForm and ChatInterface
- Google Inter font for professional appearance
- Responsive design

### Backend
- **Python** with **FastAPI** (async support)
- **LangGraph** for AI agent orchestration
- **Groq LLMs**:
  - `gemma2-9b-it` for entity extraction and parsing
  - `llama-3.3-70b-versatile` for complex reasoning (Next Best Action)

### Database
- **PostgreSQL** with SQLAlchemy ORM
- Four core tables:
  - `users` - Field rep credentials and territory
  - `hcp_profiles` - HCP information (NPI, specialty, tier)
  - `hcp_interactions` - Interaction records with LLM summaries
  - `audit_logs` - Change tracking with field-level diffs

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- PostgreSQL 13 or higher
- Groq API Key (get from https://console.groq.com/)

### Backend Setup

1. Navigate to the backend directory:
```powershell
cd backend
```

2. Create a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```powershell
Copy-Item .env.example .env
```

5. Edit `.env` and add your configuration:
```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://crm_user:crm_password@localhost:5432/crm_hcp_db
SECRET_KEY=your_secret_key_here
ENVIRONMENT=development
```

6. Start PostgreSQL and create the database:
```powershell
# Using PostgreSQL command line
psql -U postgres
CREATE DATABASE crm_hcp_db;
CREATE USER crm_user WITH PASSWORD 'crm_password';
GRANT ALL PRIVILEGES ON DATABASE crm_hcp_db TO crm_user;
\q
```

7. Run the backend:
```powershell
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```powershell
cd frontend
```

2. Install dependencies:
```powershell
npm install
```

3. Start the development server:
```powershell
npm start
```

The frontend will be available at `http://localhost:3000`

## 🚀 Usage

### Logging an Interaction

Simply chat with the AI assistant. For example:

```
"Today I met with Dr. Smith and discussed Product X efficiency. The sentiment was positive and I shared brochures."
```

The AI will automatically:
- Extract the HCP name (Dr. Smith)
- Set the date to today
- Identify sentiment as positive
- Note that brochures were shared
- Populate all form fields

### Editing an Interaction

If you need to correct something:

```
"Sorry, the name was actually Dr. John and the sentiment was negative"
```

The AI will update only the specified fields while keeping everything else unchanged.

### Additional Commands

- **Search**: "Find all interactions with Dr. Smith"
- **Analyze**: "Analyze the sentiment of the last interaction"
- **Schedule**: "Schedule a follow-up in 2 weeks"

<img width="1920" height="951" alt="Screenshot (176)" src="https://github.com/user-attachments/assets/000e0977-a2ef-4ab6-8d0a-934ac3eed233" />


## 📁 Project Structure

```
AI-CRM-HCP/
├── backend/
│   ├── tools/
│   │   ├── log_interaction.py
│   │   ├── edit_interaction.py
│   │   ├── retrieve_interaction.py
│   │   ├── analyze_sentiment.py
│   │   └── schedule_followup.py
│   ├── agent.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.js
│   │   │   ├── ChatInterface.css
│   │   │   ├── InteractionForm.js
│   │   │   └── InteractionForm.css
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── store/
│   │   │   ├── store.js
│   │   │   └── interactionSlice.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env
├── docker-compose.yml
├── README.md
└── todo.md
```


## 🔑 Environment Variables

### Backend (.env)
```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://user:pass@localhost:5432/db
SECRET_KEY=your_secret_key
ENVIRONMENT=development
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🧪 API Endpoints

- `POST /api/chat` - Send message to AI assistant
- `GET /api/interactions` - List all interactions
- `POST /api/interactions` - Create new interaction
- `GET /api/interactions/{id}` - Get specific interaction
- `PUT /api/interactions/{id}` - Update interaction
- `DELETE /api/interactions/{id}` - Delete interaction

## 🔧 Configuration

### Using llama-3.3-70b-versatile instead of gemma2-9b-it

The system uses Groq's `llama-3.3-70b-versatile` model (as gemma2-9b-it was discontinued). This model provides:
- Better instruction following
- Improved JSON output formatting
- Higher quality entity extraction
- More reliable sentiment analysis

## 📝 Database Schema

### hcp_interactions table
- `id`: Primary key
- `hcp_name`: Healthcare professional name
- `interaction_date`: Date of interaction
- `sentiment`: positive/negative/neutral
- `products_discussed`: Products mentioned
- `materials_shared`: JSON array of materials
- `interaction_type`: Meeting/Call/Email/Conference
- `location`: Where interaction occurred
- `duration_minutes`: Duration
- `notes`: Additional notes
- `follow_up_date`: Scheduled follow-up
- `follow_up_action`: Follow-up task
- `created_at`: Record creation timestamp
- `updated_at`: Last update timestamp

## 🤝 Contributing

For production use, consider:
- Adding authentication (JWT)
- Implementing rate limiting
- Adding data validation
- Setting up CI/CD
- Adding comprehensive tests
- Implementing error tracking

## 🐛 Troubleshooting

### Backend won't start
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Ensure GROQ_API_KEY is valid
- Check Python version (3.9+)

### Frontend won't connect to backend
- Verify backend is running on port 8000
- Check REACT_APP_API_URL in .env
- Ensure CORS is enabled (already configured)

### Database connection errors
- Verify PostgreSQL credentials
- Check database exists
- Ensure PostgreSQL service is running

## 📞 Support

For issues related to:
- **Groq API**: https://console.groq.com/docs
- **LangGraph**: https://python.langchain.com/docs/langgraph
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/

---

Built with ❤️ using LangGraph, Groq LLM, FastAPI, and React

