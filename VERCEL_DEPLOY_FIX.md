# Fix Vercel Frontend Deployment Error

## The Error
```
Environment Variable "REACT_APP_API_URL" references Secret "api_url", which does not exist.
```

This happens because `vercel.json` was trying to reference a secret that doesn't exist.

## The Fix

I've updated `vercel.json` to remove the secret reference. Now you need to set the environment variable directly in Vercel.

## Step-by-Step: Deploy Frontend to Vercel

### Step 1: Go to Vercel
1. Visit: https://vercel.com
2. Sign up/login (use GitHub)

### Step 2: Import Project
1. Click **"Add New..."** → **"Project"**
2. Click **"Import Git Repository"**
3. Select your repository: `MoveoEx` (or your repo name)
4. Click **"Import"**

### Step 3: Configure Project
1. **Framework Preset**: Leave as **"Other"** or select **"Create React App"**
2. **Root Directory**: Click **"Edit"** → Set to: `frontend`
3. **Build Command**: Should auto-fill as `npm run build` (keep it)
4. **Output Directory**: Should auto-fill as `build` (keep it)
5. **Install Command**: Should auto-fill as `npm install` (keep it)

### Step 4: Set Environment Variable (IMPORTANT!)
**Before clicking Deploy**, click **"Environment Variables"**:

1. Click **"Add"** button
2. **Key**: `REACT_APP_API_URL`
3. **Value**: `https://your-backend-url.onrender.com/api`
   - Replace `your-backend-url` with your actual Render backend URL
   - Example: `https://crypto-dashboard-backend.onrender.com/api`
4. Make sure it's set for **Production**, **Preview**, and **Development**
5. Click **"Add"**

### Step 5: Deploy
1. Click **"Deploy"** button
2. Wait 1-2 minutes for build
3. Vercel will give you a URL like: `https://your-app.vercel.app`

### Step 6: Test
1. Visit your Vercel URL
2. Try to register a user
3. If it works, you're done! 🎉

---

## Important Notes

- **Backend URL**: Make sure you have your backend URL from Render first
- **No trailing slash**: The URL should end with `/api` not `/api/`
- **HTTPS**: Make sure you use `https://` not `http://`

---

## If You Already Deployed

If you already created the project in Vercel:

1. Go to your project in Vercel dashboard
2. Click **"Settings"** tab
3. Click **"Environment Variables"** in the left menu
4. Click **"Add"**
5. Set:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://your-backend-url.onrender.com/api`
6. Click **"Save"**
7. Go to **"Deployments"** tab
8. Click the **"..."** menu on the latest deployment
9. Click **"Redeploy"**

---

## Example Environment Variable

If your backend URL is: `https://crypto-dashboard-backend.onrender.com`

Then set:
```
REACT_APP_API_URL=https://crypto-dashboard-backend.onrender.com/api
```

---

## Troubleshooting

### Frontend can't connect to backend:
- Verify `REACT_APP_API_URL` is set correctly
- Make sure it ends with `/api`
- Check browser console (F12) for errors
- Verify backend is running and accessible

### Build fails:
- Check that Root Directory is set to `frontend`
- Verify all dependencies are in `package.json`
- Check build logs in Vercel dashboard

