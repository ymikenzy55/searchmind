# SearchMind Backend API

FastAPI backend for SearchMind AI Assistant.

## Features

- 🤖 LangChain AI agent with Groq LLM
- 🔍 Real-time web search via Tavily
- 💾 Persistent conversation memory (SQLite)
- 🔐 JWT authentication
- 👥 User management
- 📊 Session tracking

## Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env with your API keys
```

## Environment Variables

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
CREATOR_NAME=YourName
JWT_SECRET_KEY=your_secret_key
```

## Run

```bash
python api.py
```

Server runs on **http://localhost:8000**

## API Documentation

Visit **http://localhost:8000/docs** for interactive Swagger UI documentation.

## Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Chat
- `POST /api/chat/query` - Send message to AI
- `GET /api/chat/history` - Get conversation history
- `DELETE /api/chat/history` - Clear conversation
- `GET /api/chat/sessions` - Get user sessions

### System
- `GET /` - API status
- `GET /api/health` - Health check

## Project Structure

```
backend/
├── api.py          # Main FastAPI application
├── agent.py        # LangChain agent logic
├── memory.py       # Conversation memory
├── database.py     # User database
├── requirements.txt
└── .env
```

## Database Schema

### Users Table
- id (INTEGER PRIMARY KEY)
- name (TEXT)
- email (TEXT UNIQUE)
- password (TEXT hashed)
- created_at (DATETIME)

### Conversations Table
- id (INTEGER PRIMARY KEY)
- session_id (TEXT)
- role (TEXT: 'user' or 'assistant')
- content (TEXT)
- timestamp (DATETIME)

## Deployment

See [DEPLOYMENT.md](../DEPLOYMENT.md) for production deployment.

## Dependencies

- fastapi - Web framework
- uvicorn - ASGI server
- langchain - AI orchestration
- langchain-groq - Groq integration
- tavily-python - Web search
- python-jose - JWT tokens
- passlib - Password hashing
- sqlite3 - Database

## Development

```bash
# Run with auto-reload
uvicorn api:app --reload

# View logs
# Backend shows verbose agent thinking in console
```

## Testing

```bash
# Test registration
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"test123"}'

# Test chat
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello","session_id":"default"}' \
  -G --data-urlencode "token=YOUR_TOKEN"
```

## License

MIT
