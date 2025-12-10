# Quick Deployment Guide

## 🚀 Fast Track Deployment

### Backend Deployment (Choose One)

#### Option 1: Render (Recommended - Easiest)

1. Go to https://render.com and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Name**: `crypto-dashboard-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
5. Add Environment Variables:
   ```
   SECRET_KEY=<random-string>
   JWT_SECRET_KEY=<random-string>
   MONGO_URI=<your-mongodb-atlas-uri>
   FLASK_ENV=production
   ```
6. Deploy and copy the URL (e.g., `https://your-app.onrender.com`)

#### Option 2: Railway

1. Go to https://railway.app and sign up/login
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repo
4. Set **Root Directory** to `backend`
5. Add environment variables (same as Render)
6. Deploy and copy the URL

---

### Frontend Deployment (Choose One)

#### Option 1: Vercel (Recommended - Fastest)

1. Go to https://vercel.com and sign up/login
2. Click "Add New..." → "Project"
3. Import your GitHub repo
4. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. Add Environment Variable:
   ```
   REACT_APP_API_URL=https://your-backend-url.onrender.com/api
   ```
6. Deploy and copy the URL

#### Option 2: Netlify

1. Go to https://netlify.com and sign up/login
2. Click "Add new site" → "Import an existing project"
3. Connect GitHub and select repo
4. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`
5. Add Environment Variable:
   ```
   REACT_APP_API_URL=https://your-backend-url.onrender.com/api
   ```
6. Deploy and copy the URL

---

### MongoDB Atlas Setup (Required)

1. Sign up at https://www.mongodb.com/cloud/atlas
2. Create a free cluster (M0)
3. Create database user (Database Access)
4. Whitelist IP: `0.0.0.0/0` (Network Access)
5. Get connection string (Database → Connect → Connect your application)
6. Replace `<password>` and `<dbname>` in the connection string
7. Use this as `MONGO_URI` in backend environment variables

---

### Final Steps

1. **Update CORS**: Edit `backend/app/__init__.py` and add your frontend URL to allowed origins
2. **Redeploy backend** after CORS update
3. **Test**: Visit your frontend URL and try registering a user

---

## Environment Variables Reference

### Backend (Render/Railway)
```
SECRET_KEY=your-random-secret-key-here
JWT_SECRET_KEY=your-random-jwt-secret-here
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app
```

### Frontend (Vercel/Netlify)
```
REACT_APP_API_URL=https://your-backend.onrender.com/api
```

---

## Need Help?

See `DEPLOYMENT.md` for detailed instructions and troubleshooting.

