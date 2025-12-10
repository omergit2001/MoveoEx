# Deployment Guide

This guide will help you deploy the Crypto Dashboard to free hosting services.

## Prerequisites

1. **MongoDB Atlas Account** (Free tier)
   - Sign up at https://www.mongodb.com/cloud/atlas
   - Create a free cluster
   - Get your connection string

2. **GitHub Account** (for connecting to deployment services)

3. **API Keys** (Optional - services have fallbacks):
   - OpenRouter API key (for AI insights): https://openrouter.ai/
   - CryptoPanic API key (for news): https://cryptopanic.com/developers/api/
   - CoinGecko API key (optional, free tier available): https://www.coingecko.com/en/api

---

## Step 1: Deploy Backend (Render/Railway)

### Option A: Deploy to Render

1. **Sign up/Login** to Render: https://render.com

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure the Service**:
   - **Name**: `crypto-dashboard-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

4. **Set Environment Variables**:
   ```
   SECRET_KEY=<generate-a-random-secret-key>
   JWT_SECRET_KEY=<generate-a-random-secret-key>
   MONGO_URI=<your-mongodb-atlas-connection-string>
   COINGECKO_API_KEY=<optional>
   CRYPTOPANIC_API_KEY=<optional>
   OPENROUTER_API_KEY=<optional>
   AI_MODEL=meta-llama/llama-3.2-3b-instruct:free
   FLASK_ENV=production
   ```

5. **Deploy**: Click "Create Web Service"

6. **Note the URL**: After deployment, you'll get a URL like `https://crypto-dashboard-backend.onrender.com`

### Option B: Deploy to Railway

1. **Sign up/Login** to Railway: https://railway.app

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository

3. **Configure Service**:
   - Railway will auto-detect Python
   - Set **Root Directory** to `backend`
   - Add a **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

4. **Set Environment Variables** (same as Render above)

5. **Deploy**: Railway will automatically deploy

6. **Note the URL**: Railway will provide a URL like `https://your-app.up.railway.app`

---

## Step 2: Deploy Frontend (Vercel/Netlify)

### Option A: Deploy to Vercel

1. **Sign up/Login** to Vercel: https://vercel.com

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Import your GitHub repository

3. **Configure Project**:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Set Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-backend-url.onrender.com/api
   ```
   (Replace with your actual backend URL from Step 1)

5. **Deploy**: Click "Deploy"

6. **Note the URL**: Vercel will provide a URL like `https://your-app.vercel.app`

### Option B: Deploy to Netlify

1. **Sign up/Login** to Netlify: https://netlify.com

2. **Add New Site**:
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub and select your repository

3. **Configure Build Settings**:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`

4. **Set Environment Variables**:
   - Go to Site settings → Environment variables
   - Add:
     ```
     REACT_APP_API_URL=https://your-backend-url.onrender.com/api
     ```

5. **Deploy**: Click "Deploy site"

6. **Note the URL**: Netlify will provide a URL like `https://your-app.netlify.app`

---

## Step 3: Update CORS Configuration

After deploying the frontend, update the backend CORS to allow your frontend URL:

1. **Edit** `backend/app/__init__.py`
2. **Update** the CORS configuration:
   ```python
   CORS(app, resources={
       r"/api/*": {
           "origins": [
               "http://localhost:3000",  # Local development
               "https://your-frontend.vercel.app",  # Vercel
               "https://your-frontend.netlify.app"  # Netlify
           ]
       }
   })
   ```
3. **Redeploy** the backend

---

## Step 4: MongoDB Atlas Setup

1. **Create Cluster**:
   - Go to MongoDB Atlas dashboard
   - Click "Build a Database"
   - Choose "Free" tier (M0)
   - Select a cloud provider and region

2. **Create Database User**:
   - Go to "Database Access"
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Save the username and password

3. **Whitelist IP Addresses**:
   - Go to "Network Access"
   - Click "Add IP Address"
   - For Render/Railway: Click "Allow Access from Anywhere" (0.0.0.0/0)
   - For production, consider restricting to your service IPs

4. **Get Connection String**:
   - Go to "Database" → "Connect"
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user password
   - Replace `<dbname>` with `crypto_dashboard`

5. **Add to Backend Environment Variables**:
   ```
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
   ```

---

## Step 5: Test Deployment

1. **Test Backend**:
   - Visit: `https://your-backend-url.onrender.com/api/auth/me` (should return 401, which is expected)
   - This confirms the backend is running

2. **Test Frontend**:
   - Visit your frontend URL
   - Try registering a new user
   - Complete onboarding
   - Check if dashboard loads

---

## Troubleshooting

### Backend Issues

- **Build fails**: Check that `requirements.txt` is in the `backend` directory
- **Port error**: Ensure start command uses `$PORT` environment variable
- **MongoDB connection fails**: Verify `MONGO_URI` is correct and IP is whitelisted
- **CORS errors**: Update CORS origins in `backend/app/__init__.py`

### Frontend Issues

- **API calls fail**: Verify `REACT_APP_API_URL` is set correctly
- **Build fails**: Check Node.js version (should be 16+)
- **Blank page**: Check browser console for errors

### Common Issues

- **Environment variables not loading**: Restart the service after adding variables
- **Slow first request**: Free tiers may spin down after inactivity (Render/Railway)
- **API rate limits**: Some APIs have rate limits on free tiers

---

## Free Tier Limitations

### Render
- Services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- 750 hours/month free

### Railway
- $5 free credit per month
- Services may spin down after inactivity

### Vercel
- Unlimited deployments
- 100GB bandwidth/month
- No spin-down

### Netlify
- 100GB bandwidth/month
- 300 build minutes/month
- No spin-down

---

## Production Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] MongoDB Atlas cluster created and connected
- [ ] Environment variables set correctly
- [ ] CORS configured for frontend URL
- [ ] Test user registration
- [ ] Test login
- [ ] Test dashboard loading
- [ ] Test all 4 dashboard sections
- [ ] Test feedback buttons
- [ ] Update README with production URLs

---

## Support

If you encounter issues:
1. Check service logs (Render/Railway/Vercel/Netlify dashboards)
2. Verify environment variables are set correctly
3. Check MongoDB Atlas connection
4. Review browser console for frontend errors
5. Review backend logs for API errors

