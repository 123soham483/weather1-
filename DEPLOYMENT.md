# Deployment Guide for WeatherNow Application

This guide will help you deploy your full-stack weather application to the cloud.

## Architecture Overview

Your application has two parts:
- **Frontend**: React + Vite (located in `frontend/` folder)
- **Backend**: FastAPI + Python (located in `backend/` folder)

## Recommended Deployment Strategy

### Option 1: Frontend on Vercel + Backend on Render (Recommended)

This is the easiest and most reliable approach for full-stack applications.

---

## Step 1: Deploy Backend to Render

### 1.1 Sign Up for Render
1. Go to [https://render.com](https://render.com)
2. Sign up with your GitHub account

### 1.2 Create a New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `123soham483/Weather`
3. Configure the service:
   - **Name**: `weather-backend` (or any name you prefer)
   - **Region**: Choose closest to your location
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r ../requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### 1.3 Add Environment Variables
In the **Environment** section, add:
- **Key**: `MONGO_URL`
  - **Value**: Your MongoDB connection string (e.g., `mongodb+srv://username:password@cluster.mongodb.net/`)
- **Key**: `DB_NAME`
  - **Value**: Your database name (e.g., `weather_db`)

### 1.4 Deploy
1. Click **"Create Web Service"**
2. Wait for deployment to complete (5-10 minutes)
3. Copy your backend URL (e.g., `https://weather-backend-xxxx.onrender.com`)

---

## Step 2: Update Frontend to Use Backend URL

Before deploying the frontend, you need to update it to use your Render backend URL.

### 2.1 Update API Configuration

Open your frontend code and find where API calls are made. Update the base URL to your Render backend URL:

```javascript
// Example: In your frontend API configuration file
const API_BASE_URL = 'https://weather-backend-xxxx.onrender.com/api';
```

### 2.2 Commit the Changes
```bash
git add .
git commit -m "Update backend API URL for production"
git push origin main
```

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Go to Vercel Dashboard
1. Go to [https://vercel.com](https://vercel.com)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository: `123soham483/Weather`

### 3.2 Configure Project Settings
Vercel should automatically detect the configuration from `vercel.json`, but verify:
- **Framework Preset**: Vite
- **Root Directory**: Leave as `.` (root)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/dist`

### 3.3 Deploy
1. Click **"Deploy"**
2. Wait for deployment (2-3 minutes)
3. Your site will be live at `https://your-project.vercel.app`

---

## Step 4: Update CORS Settings

After deployment, you need to update your backend to allow requests from your Vercel frontend.

### 4.1 Update Backend CORS Configuration

In `backend/server.py`, update the CORS allowed origins to include your Vercel URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://your-project.vercel.app",  # Add your Vercel URL here
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4.2 Commit and Push
```bash
git add backend/server.py
git commit -m "Update CORS for production frontend"
git push origin main
```

Render will automatically redeploy your backend.

---

## Alternative: Deploy Everything to Render

If you prefer to host both frontend and backend on Render:

### Backend (Same as above)
Follow Step 1 above

### Frontend on Render
1. Create another **Web Service** on Render
2. Configure:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm run preview -- --port $PORT --host 0.0.0.0`
3. Add environment variable:
   - **Key**: `VITE_API_URL`
   - **Value**: Your backend URL

---

## Troubleshooting

### Issue: CORS Errors
- Make sure your Vercel URL is added to the backend's CORS allowed origins
- Redeploy the backend after updating CORS settings

### Issue: Backend Not Connecting to MongoDB
- Verify your MongoDB connection string is correct in Render environment variables
- Make sure your MongoDB Atlas allows connections from anywhere (IP: `0.0.0.0/0`)

### Issue: Frontend Shows "Network Error"
- Check that the backend URL in your frontend code is correct
- Verify the backend is running (visit the backend URL directly)

---

## Costs

Both services offer generous free tiers:
- **Vercel**: Free for personal projects
- **Render**: Free tier available (spins down after inactivity)

---

## Quick Reference

After successful deployment:
- **Frontend URL**: `https://your-project.vercel.app`
- **Backend URL**: `https://weather-backend-xxxx.onrender.com`
- **GitHub Repository**: `https://github.com/123soham483/Weather`

---

## Need Help?

If you encounter any issues during deployment, check:
1. Build logs on Vercel/Render dashboard
2. Browser console for frontend errors
3. Backend logs on Render dashboard

Good luck with your deployment! 🚀
