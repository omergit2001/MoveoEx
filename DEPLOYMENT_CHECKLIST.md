# Deployment Checklist

## Pre-Deployment

- [ ] Code is committed and pushed to GitHub
- [ ] All tests pass locally
- [ ] MongoDB Atlas account created
- [ ] MongoDB cluster created and connection string ready

## Backend Deployment

### Render/Railway Setup
- [ ] Account created on Render or Railway
- [ ] GitHub repository connected
- [ ] New web service/project created
- [ ] Root directory set to `backend`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

### Environment Variables Set
- [ ] `SECRET_KEY` (random string)
- [ ] `JWT_SECRET_KEY` (random string)
- [ ] `MONGO_URI` (MongoDB Atlas connection string)
- [ ] `FLASK_ENV=production`
- [ ] `CORS_ORIGINS` (frontend URLs, comma-separated)

### Optional API Keys
- [ ] `OPENROUTER_API_KEY` (for AI insights)
- [ ] `CRYPTOPANIC_API_KEY` (for news)
- [ ] `COINGECKO_API_KEY` (optional)

### Backend Verification
- [ ] Backend URL obtained (e.g., `https://your-app.onrender.com`)
- [ ] Backend is accessible (test with browser/curl)
- [ ] No build errors in logs

## Frontend Deployment

### Vercel/Netlify Setup
- [ ] Account created on Vercel or Netlify
- [ ] GitHub repository connected
- [ ] New project/site created
- [ ] Root directory set to `frontend`
- [ ] Build command: `npm run build`
- [ ] Output directory: `build`

### Environment Variables Set
- [ ] `REACT_APP_API_URL` (backend URL + `/api`)

### Frontend Verification
- [ ] Frontend URL obtained (e.g., `https://your-app.vercel.app`)
- [ ] Frontend is accessible
- [ ] No build errors in logs

## Post-Deployment

### CORS Configuration
- [ ] Updated `backend/app/__init__.py` with frontend URL
- [ ] Added `CORS_ORIGINS` environment variable in backend
- [ ] Backend redeployed after CORS update

### Testing
- [ ] Frontend loads without errors
- [ ] User registration works
- [ ] User login works
- [ ] Onboarding quiz works
- [ ] Dashboard loads all 4 sections
- [ ] Market News displays
- [ ] Coin Prices display
- [ ] AI Insight displays
- [ ] Meme displays
- [ ] Feedback buttons work (thumbs up/down)
- [ ] Logout works

### Documentation
- [ ] Updated README with production URLs
- [ ] Documented any custom configurations
- [ ] Noted any limitations or known issues

## Troubleshooting

If something doesn't work:
1. Check service logs (Render/Railway/Vercel/Netlify dashboards)
2. Verify environment variables are set correctly
3. Check MongoDB Atlas connection
4. Review browser console for frontend errors
5. Review backend logs for API errors
6. Verify CORS configuration
7. Check that URLs are correct (no trailing slashes, correct protocol)

## URLs to Save

- Backend URL: `_________________________`
- Frontend URL: `_________________________`
- MongoDB Atlas Cluster: `_________________________`

