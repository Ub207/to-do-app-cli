# Deployment Guide

Quick guide to deploy your Todo API to various platforms.

## 🚀 Quick Start - Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn api.main:app --reload

# Access API
# - API: http://localhost:8000
# - Swagger Docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

## 📦 Deploy to Render (FREE)

### Step 1: Push to GitHub
Your code should already be on GitHub at: `https://github.com/Ub207/to-do-app-cli`

### Step 2: Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub

### Step 3: Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: `todo-db`
3. Select Free tier
4. Click "Create Database"
5. Copy the "Internal Database URL"

### Step 4: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repo: `Ub207/to-do-app-cli`
3. Configure:
   - **Name**: `todo-api` (or any name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. Add Environment Variable:
   - Key: `DATABASE_URL`
   - Value: (paste the Internal Database URL from Step 3)

5. Click "Create Web Service"

### Step 5: Done!
Your API will be live at: `https://todo-api-xxxx.onrender.com`

Access:
- API Docs: `https://todo-api-xxxx.onrender.com/docs`
- Health Check: `https://todo-api-xxxx.onrender.com/health`

**Note**: Free tier apps may spin down after 15 minutes of inactivity. First request after inactivity may take 30-60 seconds.

---

## 🚂 Deploy to Railway (FREE $5/month)

### Step 1: Create Railway Account
- Go to [railway.app](https://railway.app)
- Sign up with GitHub

### Step 2: New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `Ub207/to-do-app-cli`

### Step 3: Add PostgreSQL
1. Click "New" → "Database" → "Add PostgreSQL"
2. Railway automatically sets `DATABASE_URL`

### Step 4: Configure Service
1. Click on your service
2. Go to "Settings"
3. No additional config needed! Railway uses Procfile automatically

### Step 5: Done!
Your API will be live at the Railway-provided URL.

---

## ✈️ Deploy to Fly.io

### Step 1: Install flyctl
```bash
# Windows (PowerShell)
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login
```bash
flyctl auth login
```

### Step 3: Create fly.toml
Create `fly.toml` in project root:
```toml
app = "your-todo-api"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

### Step 4: Launch
```bash
flyctl launch
flyctl postgres create  # For database
flyctl postgres attach your-db-name
```

### Step 5: Deploy
```bash
flyctl deploy
```

---

## 🔧 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| PORT | Server port (auto-set by platforms) | `8000` |

---

## 🧪 Testing Deployed API

```bash
# Replace with your deployed URL
API_URL="https://your-api.onrender.com"

# Health check
curl $API_URL/health

# Create task
curl -X POST $API_URL/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Deploy successful!","description":"API is live"}'

# Get all tasks
curl $API_URL/api/v1/tasks

# View API docs
# Open: $API_URL/docs
```

---

## 📊 Monitoring

### Render
- View logs in Render dashboard
- Check metrics in "Metrics" tab

### Railway
- View logs in Railway dashboard
- Check usage in "Metrics"

### Fly.io
```bash
flyctl logs
flyctl status
```

---

## 🐛 Troubleshooting

### Build Fails
- Check `requirements.txt` has all dependencies
- Verify Python version in `runtime.txt`

### Database Connection Errors
- Verify `DATABASE_URL` is set correctly
- Check database is in same region (for Render)

### App Not Starting
- Check logs for errors
- Verify start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### 404 Errors
- Routes should be `/api/v1/tasks` not `/tasks`
- Check API docs at `/docs` for correct endpoints

---

## 💰 Cost Comparison

| Platform | Free Tier | Limits |
|----------|-----------|--------|
| **Render** | ✅ Yes | 750 hrs/month, spins down after 15 min |
| **Railway** | ✅ $5/month | $5 credit monthly |
| **Fly.io** | ✅ Yes | 3 small VMs, 3GB storage |

**Recommendation for Learning**: Start with **Render** - easiest setup, true free tier.

---

## 🔐 Production Checklist

Before going to production:

- [ ] Set proper CORS origins in `api/main.py`
- [ ] Use strong database password
- [ ] Enable HTTPS (automatic on platforms)
- [ ] Add rate limiting
- [ ] Set up monitoring/alerts
- [ ] Add authentication if needed
- [ ] Regular database backups
- [ ] Environment-specific configs

---

## 📚 Next Steps

1. **Add Authentication**: JWT tokens, OAuth
2. **Add Rate Limiting**: Prevent abuse
3. **Add Caching**: Redis for performance
4. **Add Websockets**: Real-time updates
5. **Add File Uploads**: Task attachments
6. **Add Email Notifications**: Due date reminders

---

Built with ❤️ using FastAPI
