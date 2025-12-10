# Netlify Frontend Deployment Troubleshooting

## Common Error: Backend URL Issues

If you're seeing errors related to `https://crypto-dashboard-backend-6jum.onrender.com/api`, follow these steps:

---

## Step 1: Test Backend is Running

**Test the backend directly in your browser:**

1. Visit: `https://crypto-dashboard-backend-6jum.onrender.com/api/health`
   - ✅ **Should see**: `{"status":"healthy","service":"crypto-dashboard-backend","message":"API is running"}`
   - ❌ **If error**: Backend is not running or not accessible

2. Visit: `https://crypto-dashboard-backend-6jum.onrender.com/api/auth/me`
   - ✅ **Should see**: `{"msg":"Missing Authorization Header"}` (this is correct - means backend is working)
   - ❌ **If 404 or error**: Backend routes not configured correctly

---

## Step 2: Check Netlify Environment Variables

**In Netlify Dashboard:**

1. Go to: **Site settings** → **Environment variables**
2. Check if `REACT_APP_API_URL` exists
3. **Value should be**: `https://crypto-dashboard-backend-6jum.onrender.com/api`
   - ✅ Must start with `https://`
   - ✅ Must end with `/api` (not `/api/`)
   - ✅ No trailing slash

4. **If variable is missing or wrong:**
   - Click **"Add variable"**
   - Key: `REACT_APP_API_URL`
   - Value: `https://crypto-dashboard-backend-6jum.onrender.com/api`
   - **IMPORTANT**: After adding/changing, you MUST redeploy!

5. **Redeploy after changing environment variables:**
   - Go to **Deploys** tab
   - Click **"Trigger deploy"** → **"Deploy site"**
   - Wait for new build to complete

---

## Step 3: Check Browser Console

**On your deployed Netlify site:**

1. Open browser console (F12)
2. Go to **Console** tab
3. Look for errors like:
   - `Network Error`
   - `CORS policy`
   - `Failed to fetch`
   - `404 Not Found`

4. Go to **Network** tab
5. Try to login or register
6. Find the API request (e.g., `/api/auth/login`)
7. Click on it and check:
   - **Request URL**: Should be `https://crypto-dashboard-backend-6jum.onrender.com/api/auth/login`
   - **Status**: 
     - `200` = Success ✅
     - `401` = Wrong credentials (normal)
     - `404` = Wrong URL ❌
     - `CORS error` = CORS not configured ❌
     - `Network error` = Backend not accessible ❌

---

## Step 4: Check CORS Configuration

**If you see CORS errors in browser console:**

1. **Get your Netlify URL** (e.g., `https://your-app-name.netlify.app`)

2. **Go to Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Select your backend service
   - Go to **Environment** tab

3. **Add/Update CORS_ORIGINS:**
   - Key: `CORS_ORIGINS`
   - Value: `https://your-app-name.netlify.app`
   - Replace `your-app-name` with your actual Netlify site name
   - **No trailing slash!**

4. **Save and wait for redeploy** (2-3 minutes)

5. **Test again** on your Netlify site

---

## Step 5: Verify Backend is Accessible

**Test these URLs in your browser:**

1. **Health Check:**
   ```
   https://crypto-dashboard-backend-6jum.onrender.com/api/health
   ```
   - Should return: `{"status":"healthy",...}`

2. **Root API:**
   ```
   https://crypto-dashboard-backend-6jum.onrender.com/api/
   ```
   - Should return API information

3. **Auth Endpoint (without token):**
   ```
   https://crypto-dashboard-backend-6jum.onrender.com/api/auth/me
   ```
   - Should return: `{"msg":"Missing Authorization Header"}`

**If any of these fail:**
- Backend might be sleeping (Render free tier)
- Wait 30 seconds and try again
- Check Render logs for errors

---

## Step 6: Check Netlify Build Logs

**In Netlify Dashboard:**

1. Go to **Deploys** tab
2. Click on the latest deploy
3. Check **Build log** for:
   - Build errors
   - Environment variable warnings
   - Missing dependencies

**Common build issues:**
- `REACT_APP_API_URL is not defined` → Environment variable not set
- Build succeeds but site shows blank → Check browser console

---

## Step 7: Test Environment Variable in Build

**Add temporary logging to verify:**

The frontend already has console logging in `auth.js`. Check browser console when you try to login - it should show:
```
Attempting login with email: ...
API URL: https://crypto-dashboard-backend-6jum.onrender.com/api
```

**If it shows `http://localhost:5000/api`:**
- Environment variable not set correctly in Netlify
- Need to redeploy after setting variable

---

## Quick Fix Checklist

- [ ] Backend is running (test `/api/health` in browser)
- [ ] `REACT_APP_API_URL` is set in Netlify environment variables
- [ ] Environment variable value is: `https://crypto-dashboard-backend-6jum.onrender.com/api`
- [ ] Site was redeployed after setting environment variable
- [ ] `CORS_ORIGINS` is set in Render with your Netlify URL
- [ ] Browser console shows correct API URL when making requests
- [ ] No CORS errors in browser console

---

## Still Having Issues?

**Share these details:**

1. **What error message do you see?** (exact text from browser console)
2. **What does Network tab show?** (status code, request URL)
3. **What does `/api/health` return?** (test in browser)
4. **What is your Netlify URL?** (so we can check CORS)
5. **Screenshot of Netlify environment variables** (hide sensitive values)

---

## Common Error Messages & Solutions

### Error: "Network Error" or "Failed to fetch"
**Cause**: Backend not accessible or CORS issue
**Solution**: 
- Test backend URL directly in browser
- Check CORS_ORIGINS in Render
- Verify backend is running (not sleeping)

### Error: "404 Not Found" on API calls
**Cause**: Wrong API URL or backend route not found
**Solution**:
- Verify `REACT_APP_API_URL` ends with `/api`
- Test backend endpoints directly in browser
- Check backend routes are registered correctly

### Error: "CORS policy: No 'Access-Control-Allow-Origin' header"
**Cause**: CORS not configured for your Netlify domain
**Solution**:
- Add Netlify URL to `CORS_ORIGINS` in Render
- Wait for backend redeploy
- Clear browser cache and try again

### Error: Site loads but API calls go to localhost
**Cause**: Environment variable not set or not loaded
**Solution**:
- Set `REACT_APP_API_URL` in Netlify dashboard
- Redeploy site (environment variables require new build)
- Check browser console to verify URL

