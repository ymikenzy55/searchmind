# ⚡ Quick Start Guide

Get SearchMind running in 5 minutes!

## 🎯 Prerequisites

Make sure you have:
- ✅ Python 3.11+ installed
- ✅ Node.js 18+ installed
- ✅ Groq API key ([Get here](https://console.groq.com))
- ✅ Tavily API key ([Get here](https://tavily.com))

Check versions:
```bash
python --version  # Should be 3.11+
node --version    # Should be 18+
npm --version
```

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/ymikenzy55/searchmind.git
cd searchmind
```

### 2. Backend Setup (5 steps)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux
```

**Edit backend/.env:**
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
TAVILY_API_KEY=tvly_your_actual_tavily_api_key_here
CREATOR_NAME=YourName
JWT_SECRET_KEY=change-this-to-something-random-and-secure
```

💡 **Tip:** Generate a secure JWT secret:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Frontend Setup (3 steps)

Open a NEW terminal window:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Copy environment file
copy .env.local.example .env.local  # Windows (if exists)
# Or create manually
```

**Create/Edit frontend/.env.local:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Running the Application

### Option A: Manual Start (Recommended for First Time)

**Terminal 1 - Backend:**
```bash
cd backend
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux
python api.py
```

Wait for: `Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Wait for: `Ready on http://localhost:3000`

### Option B: PowerShell Script (Windows Only)

```bash
.\start-dev.ps1
```

## 🎉 Open Your Browser

Navigate to **http://localhost:3000**

You should see the SearchMind login page!

## 🧪 First Test

1. Click "Sign up" to create an account
2. Enter:
   - Name: Your Name
   - Email: test@example.com
   - Password: password123
3. Click "Sign Up"
4. You should be redirected to the chat interface
5. Try asking: "What's the latest in AI?"

## ✅ Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can register a new account
- [ ] Can see personalized welcome message
- [ ] Can send a message and get a response
- [ ] Can toggle dark/light mode
- [ ] Can clear chat history

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

**Module not found errors:**
```bash
cd backend
.venv\Scripts\activate
pip install -r requirements.txt
```

**API keys not working:**
- Double-check `.env` file exists in `backend/` folder
- Verify no extra spaces in the `.env` file
- Make sure API keys are valid
- Try generating new keys

### Frontend Issues

**Port 3000 already in use:**
```bash
# Try port 3001
npm run dev -- -p 3001
# Update NEXT_PUBLIC_API_URL if needed
```

**Dependencies failed to install:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json  # Mac/Linux
# Remove-Item -Recurse -Force node_modules, package-lock.json  # Windows
npm install
```

**Cannot connect to backend:**
- Verify backend is running on port 8000
- Check `frontend/.env.local` has correct API URL
- Check browser console for CORS errors

### CORS Errors

If you see CORS errors in browser console:

Edit `backend/api.py`:
```python
allow_origins=["http://localhost:3000", "http://localhost:3001"],
```

## 🔍 Testing API Directly

Visit **http://localhost:8000/docs** to see interactive API documentation (Swagger UI).

Try these endpoints:
- `GET /` - API status
- `GET /api/health` - Health check
- `POST /api/auth/register` - Register user

## 📚 Next Steps

- ✅ Read the full [README.md](README.md)
- 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) to deploy to production
- 🎨 Customize the UI in `frontend/components/Chat.tsx`
- 🤖 Modify AI behavior in `backend/agent.py`

## 💡 Pro Tips

1. **Use 2 Terminal Windows** - One for backend, one for frontend
2. **Check Logs** - Backend shows verbose agent thinking
3. **Save API Keys** - Keep your `.env` file safe
4. **Dark Mode** - Toggle in top-right corner
5. **Quick Questions** - Click suggested questions to test

## 🆘 Still Having Issues?

1. Check that all prerequisites are installed
2. Verify both backend and frontend are running
3. Check browser console for errors (F12)
4. Review backend terminal for Python errors
5. Try restarting both servers
6. Create an issue on GitHub with error details

## 📞 Get Help

- 📖 [Full Documentation](README.md)
- 🐛 [Report Bug](https://github.com/ymikenzy55/searchmind/issues)
- 💬 [Discussions](https://github.com/ymikenzy55/searchmind/discussions)

---

🎉 **Enjoy SearchMind!** If it works, give the repo a ⭐!
