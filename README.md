# 🔍 SearchMind - AI Research Assistant v2.0

A modern, full-stack AI research assistant with real-time web search, user authentication, and persistent memory. Built with Next.js, FastAPI, and LangChain.

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)

## ✨ Features

### 🎨 Frontend (Next.js)
- **Modern UI/UX** - Beautiful, responsive design with Tailwind CSS
- **🌓 Dark/Light Mode** - Automatic theme switching with system preference
- **🔐 User Authentication** - Secure registration and login
- **💬 Real-time Chat** - Smooth, interactive conversation interface
- **👤 Personalized Welcome** - Greets users by name
- **📱 Fully Responsive** - Works on desktop, tablet, and mobile

### ⚡ Backend (FastAPI)
- **🤖 AI Agent** - LangChain-powered intelligent assistant
- **🔍 Web Search** - Real-time information via Tavily API
- **💾 Persistent Memory** - SQLite-based conversation history
- **🔒 JWT Authentication** - Secure token-based auth
- **🚀 Fast API** - High-performance async endpoints
- **📊 Session Management** - Multiple chat sessions per user

## 🏗️ Architecture

```
searchmind/
├── frontend/              # Next.js + TypeScript
│   ├── app/              # App router pages
│   │   ├── page.tsx     # Main chat page
│   │   ├── layout.tsx   # Root layout
│   │   └── auth/        # Auth pages (login/register)
│   ├── components/       # React components
│   │   ├── Chat.tsx     # Main chat interface
│   │   ├── ThemeProvider.tsx
│   │   └── LoadingSpinner.tsx
│   ├── context/         # React context
│   │   └── AuthContext.tsx
│   └── package.json
│
└── backend/              # FastAPI + Python
    ├── api.py           # Main FastAPI application
    ├── agent.py         # LangChain agent logic
    ├── memory.py        # Conversation memory
    ├── database.py      # User database
    └── requirements.txt
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Groq API Key** ([Get it here](https://console.groq.com))
- **Tavily API Key** ([Get it here](https://tavily.com))

### 1️⃣ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux

# Edit .env and add your API keys
```

**backend/.env:**
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
CREATOR_NAME=YourName
JWT_SECRET_KEY=your-secret-jwt-key-change-in-production
```

**Run backend:**
```bash
python api.py
# Backend runs on http://localhost:8000
```

### 2️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
# Frontend runs on http://localhost:3000
```

### 3️⃣ Open Your Browser

Navigate to **http://localhost:3000** and create an account!

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Chat
- `POST /api/chat/query` - Send message to AI
- `GET /api/chat/history` - Get conversation history
- `DELETE /api/chat/history` - Clear conversation history
- `GET /api/chat/sessions` - Get user's chat sessions

### Health
- `GET /` - API status
- `GET /api/health` - Health check

## 🎯 Usage

### 1. **Register/Login**
- Create an account or sign in
- Your name is used for personalized greetings

### 2. **Start Chatting**
- Type your question or use quick questions
- AI searches the web when needed
- All conversations are saved

### 3. **Manage Chats**
- Clear current chat history
- Switch between light/dark mode
- Logout when done

## 🔧 Configuration

### Change AI Model

Edit `backend/agent.py`:
```python
llm = ChatGroq(
    model="openai/gpt-oss-20b",  # Change model here
    temperature=0.3,
    api_key=GROQ_API_KEY
)
```

**Available Models:**
- `openai/gpt-oss-20b` (default - fast)
- `openai/gpt-oss-120b` (more capable)
- `llama-3.3-70b-versatile`

### Adjust Memory Context

Edit `backend/agent.py`:
```python
context = memory.get_recent_context(session_id, num_messages=6)
```

### Customize Theme

Edit `frontend/tailwind.config.ts` for colors and styling.

## 🚢 Deployment

### Deploy Frontend (Vercel) - FREE

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your repository
5. Set root directory to `frontend`
6. Add environment variable:
   - `NEXT_PUBLIC_API_URL`: Your backend URL
7. Deploy!

### Deploy Backend (Railway) - FREE

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Set root directory to `backend`
5. Add environment variables:
   ```
   GROQ_API_KEY=your_key
   TAVILY_API_KEY=your_key
   CREATOR_NAME=YourName
   JWT_SECRET_KEY=your_secret
   ```
6. Deploy!

### Alternative Backend Hosts (Free Tiers)
- **Fly.io** - 3 shared VMs free
- **Render** - 750 hours/month free
- **Heroku** - Eco dynos available

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|-----------|---------|
| **Next.js 15** | React framework with App Router |
| **TypeScript** | Type-safe JavaScript |
| **Tailwind CSS** | Utility-first CSS |
| **next-themes** | Dark/light mode |
| **Axios** | HTTP client |
| **Lucide React** | Beautiful icons |

### Backend
| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Modern Python web framework |
| **LangChain** | AI agent orchestration |
| **Groq** | Fast LLM inference |
| **Tavily** | Real-time web search |
| **SQLite** | Embedded database |
| **PyJWT** | JWT authentication |
| **Passlib** | Password hashing |

## 🔒 Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Secure HTTP-only practices
- ✅ CORS protection
- ✅ SQL injection protection
- ✅ Input validation

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at DATETIME
);
```

### Conversations Table
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    role TEXT,
    content TEXT,
    timestamp DATETIME
);
```

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.11+)
- Verify .env file exists with all keys
- Install dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check `.env.local` has correct API URL

### CORS Errors
- Update `allow_origins` in `backend/api.py` with your frontend URL

### Chat not working
- Verify backend is running on port 8000
- Check browser console for errors
- Verify API_URL in frontend `.env.local`

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 👤 Author

**Mike** - AI Engineer

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) - AI orchestration
- [Groq](https://groq.com) - Lightning-fast LLM inference
- [Tavily](https://tavily.com) - Web search API
- [Next.js](https://nextjs.org) - React framework
- [FastAPI](https://fastapi.tiangolo.com) - Python web framework
- [Tailwind CSS](https://tailwindcss.com) - CSS framework

---

## 📸 Screenshots

### Light Mode
Beautiful, clean interface with smooth animations

### Dark Mode
Easy on the eyes with perfect contrast

### Mobile Responsive
Works flawlessly on all devices

---

⭐ **If you find this project helpful, please give it a star!**

🐛 **Found a bug?** [Open an issue](https://github.com/ymikenzy55/searchmind/issues)

💡 **Have an idea?** [Start a discussion](https://github.com/ymikenzy55/searchmind/discussions)
