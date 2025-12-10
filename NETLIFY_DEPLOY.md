# Netlify Frontend Deployment Guide

## Prerequisites

- ✅ Backend already deployed on Render: `https://crypto-dashboard-backend-6jum.onrender.com`
- ✅ GitHub repository with your code
- ✅ Netlify account (sign up at https://app.netlify.com)

---

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

Make sure your code is pushed to GitHub:
```bash
git add .
git commit -m "Prepare for Netlify deployment"
git push
```

### Step 2: Deploy to Netlify

1. **Go to Netlify Dashboard**
   - Visit: https://app.netlify.com
   - Sign in (GitHub login recommended)

2. **Import Your Project**
   - Click **"Add new site"** → **"Import an existing project"**
   - Click **"Deploy with GitHub"**
   - Authorize Netlify to access your GitHub repositories
   - Select your repository (`MoveoEx`)

3. **Configure Build Settings**
   
   **IMPORTANT**: Set these values:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`
   
   ⚠️ **Critical**: You MUST set the base directory to `frontend` because your React app is in a subdirectory!

4. **Set Environment Variables**
   
   Click **"Show advanced"** → **"New variable"**:
   
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://crypto-dashboard-backend-6jum.onrender.com/api`
   
   ⚠️ **Important**: 
   - Make sure it ends with `/api` (not `/api/`)
   - No trailing slash
   - Use `https://` (not `http://`)

5. **Deploy**
   - Click **"Deploy site"**
   - Wait 2-3 minutes for build to complete

---

## Step 3: Update CORS on Render Backend

After Netlify gives you your frontend URL (e.g., `https://your-app-name.netlify.app`):

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Select your backend service

2. **Update Environment Variables**
   - Go to **"Environment"** tab
   - Find or add: `CORS_ORIGINS`
   - Set value to: `https://your-app-name.netlify.app`
   
   Replace `your-app-name` with your actual Netlify site name.
   
   Example: `https://crypto-dashboard-123.netlify.app`

3. **Save and Redeploy**
   - Click **"Save Changes"**
   - Render will automatically redeploy (wait 2-3 minutes)

---

## Step 4: Verify Deployment

1. **Visit Your Netlify Site**
   - Go to your Netlify URL (e.g., `https://your-app-name.netlify.app`)

2. **Test the Application**
   - Open browser console (F12)
   - Try to register a new user
   - Try to login
   - Check Network tab for API calls

3. **Check for Errors**
   - **CORS Error**: Backend CORS not updated → Go back to Step 3
   - **404 on API calls**: Wrong `REACT_APP_API_URL` → Check Netlify environment variables
   - **Build failed**: Check Netlify build logs

---

## Troubleshooting

### Issue 1: Build Fails with "Cannot find module"

**Solution**: 
- Make sure **Base directory** is set to `frontend` in Netlify build settings
- The build command should run from the `frontend` directory

### Issue 2: CORS Error in Browser

**Symptoms**: 
```
Access to XMLHttpRequest at 'https://...' from origin 'https://...' has been blocked by CORS policy
```

**Solution**:
1. Get your Netlify URL (e.g., `https://your-app.netlify.app`)
2. Go to Render → Your backend → Environment
3. Add/update `CORS_ORIGINS` with your Netlify URL
4. Save and wait for redeploy

### Issue 3: API Calls Going to Wrong URL

**Symptoms**: 
- Network requests show `http://localhost:5000/api` or wrong URL
- Console shows: `API URL: http://localhost:5000/api`

**Solution**:
1. Go to Netlify → Site settings → Environment variables
2. Check `REACT_APP_API_URL` is set correctly
3. Make sure it's: `https://crypto-dashboard-backend-6jum.onrender.com/api`
4. **Redeploy** the site (environment variables require a new build)

### Issue 4: React Router Routes Not Working

**Symptoms**: 
- Direct URL access (e.g., `/dashboard`) shows 404
- Only `/` works

**Solution**: 
- The `netlify.toml` file already has redirects configured
- If it's not working, check that `netlify.toml` is in the `frontend` directory
- Netlify should automatically detect it

### Issue 5: Build Succeeds But Site Shows Blank Page

**Solution**:
1. Check browser console for errors
2. Verify `REACT_APP_API_URL` is set in Netlify environment variables
3. Check Netlify build logs for warnings
4. Try clearing browser cache

---

## Quick Reference

### Netlify Build Settings
```
Base directory: frontend
Build command: npm run build
Publish directory: frontend/build
```

### Environment Variables (Netlify)
```
REACT_APP_API_URL = https://crypto-dashboard-backend-6jum.onrender.com/api
```

### Environment Variables (Render - Backend)
```
CORS_ORIGINS = https://your-netlify-app.netlify.app
```

---

## After Deployment

Once everything is working:

1. **Custom Domain** (Optional)
   - Netlify → Site settings → Domain management
   - Add your custom domain

2. **SSL Certificate**
   - Netlify provides free SSL automatically
   - Your site will be `https://` by default

3. **Continuous Deployment**
   - Every push to GitHub will automatically trigger a new deployment
   - You can disable this in Netlify settings if needed

---

## Need Help?

If you encounter issues:
1. Check Netlify build logs (Deploys → Click on deploy → View logs)
2. Check browser console for errors
3. Verify all environment variables are set correctly
4. Make sure backend is running and accessible

