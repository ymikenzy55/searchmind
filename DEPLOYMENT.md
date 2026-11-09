# 🚀 Deployment Guide

Complete guide to deploy SearchMind to production.

## 📋 Pre-Deployment Checklist

- [ ] Get Groq API Key
- [ ] Get Tavily API Key
- [ ] Generate strong JWT secret key
- [ ] Create GitHub repository
- [ ] Test locally (both frontend and backend)

## 🎨 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. Ensure your frontend code is in the `frontend/` directory
2. Test locally: `cd frontend && npm run dev`
3. Build test: `npm run build`

### Step 2: Deploy to Vercel

**Via Vercel Dashboard:**

1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click "Add New..." → "Project"
4. Import your GitHub repository
5. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
6. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL`: (Your backend URL - add after backend deployment)
7. Click "Deploy"

**Via Vercel CLI:**

```bash
cd frontend
npm install -g vercel
vercel login
vercel
```

### Step 3: Update API URL

After backend deployment, go to:
- Vercel Dashboard → Your Project → Settings → Environment Variables
- Update `NEXT_PUBLIC_API_URL` with your backend URL
- Redeploy: Deployments → ... → Redeploy

## ⚡ Backend Deployment (Railway)

### Option 1: Railway (Recommended - Easy)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Click "Add variables" and add:
   ```
   GROQ_API_KEY=your_groq_key
   TAVILY_API_KEY=your_tavily_key
   CREATOR_NAME=YourName
   JWT_SECRET_KEY=your_super_secret_key
   ```
6. In Settings:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
7. Click "Deploy"
8. Copy the generated URL (e.g., `https://your-app.railway.app`)

### Option 2: Fly.io (Free 3 VMs)

**Prerequisites:**
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh
```

**Deploy:**
```bash
cd backend

# Login
flyctl auth login

# Launch app
flyctl launch

# Set secrets
flyctl secrets set GROQ_API_KEY=your_key
flyctl secrets set TAVILY_API_KEY=your_key
flyctl secrets set JWT_SECRET_KEY=your_secret
flyctl secrets set CREATOR_NAME=YourName

# Deploy
flyctl deploy
```

**Create fly.toml:**
```toml
app = "searchmind-api"
primary_region = "sjc"

[build]
  builder = "paketobuildpacks/builder:base"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

### Option 3: Render (Free Tier)

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Name**: searchmind-api
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   ```
   GROQ_API_KEY
   TAVILY_API_KEY
   JWT_SECRET_KEY
   CREATOR_NAME
   ```
6. Click "Create Web Service"

### Option 4: Heroku

```bash
cd backend

# Login
heroku login

# Create app
heroku create searchmind-api

# Set environment variables
heroku config:set GROQ_API_KEY=your_key
heroku config:set TAVILY_API_KEY=your_key
heroku config:set JWT_SECRET_KEY=your_secret
heroku config:set CREATOR_NAME=YourName

# Create Procfile
echo "web: uvicorn api:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## 🔗 Connecting Frontend & Backend

### Update CORS in Backend

Edit `backend/api.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.vercel.app",  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Update API URL in Frontend

On Vercel Dashboard:
1. Go to your project → Settings → Environment Variables
2. Update `NEXT_PUBLIC_API_URL`:
   - Value: `https://your-backend.railway.app` (or your backend URL)
3. Redeploy from Deployments tab

## 🔒 Security Checklist

Before going live:

- [ ] Change JWT_SECRET_KEY to a strong random string
- [ ] Use HTTPS for both frontend and backend
- [ ] Set proper CORS origins (no wildcards in production)
- [ ] Enable rate limiting on API endpoints
- [ ] Review and test authentication flow
- [ ] Backup database regularly
- [ ] Monitor API usage and costs

## 📊 Post-Deployment

### Test Your Deployment

1. Visit your frontend URL
2. Register a new account
3. Test chat functionality
4. Verify web search works
5. Test dark/light mode
6. Test on mobile device

### Monitor Your App

**Railway:**
- View logs in Railway dashboard
- Check metrics tab for usage

**Vercel:**
- Analytics tab for frontend performance
- Function logs for debugging

### Database Backup

SQLite databases are ephemeral on some platforms. Consider:
- Using Railway's persistent volume
- Migrating to PostgreSQL for production
- Regular backups to cloud storage

## 💰 Cost Estimates

| Service | Free Tier | Cost After |
|---------|-----------|------------|
| **Vercel** | Unlimited hobby projects | $20/month Pro |
| **Railway** | $5 trial credit | Pay-as-you-go |
| **Fly.io** | 3 shared VMs, 160GB | ~$2/month after |
| **Groq API** | Free tier available | Pay-as-you-go |
| **Tavily API** | 1,000 requests/month | $0.001/request |

## 🐛 Common Issues

### "Module not found" errors
- Check `requirements.txt` is complete
- Rebuild on hosting platform

### CORS errors
- Verify CORS settings in `api.py`
- Check frontend API URL is correct

### Database not persisting
- Use persistent storage (Railway volumes)
- Consider PostgreSQL for production

### Slow cold starts
- Keep-alive services (UptimeRobot)
- Upgrade to paid tier for always-on

## 📞 Support

Need help? Check:
- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [Fly.io Docs](https://fly.io/docs)
- [GitHub Issues](https://github.com/ymikenzy55/searchmind/issues)

---

✅ **Deployment complete!** Share your app with the world! 🎉
