# Signup Error Troubleshooting Guide

## Common Signup Errors & Solutions

### Error 1: "Network Error" or "Failed to fetch"

**Symptoms:**
- Console shows: `Network Error` or `Failed to fetch`
- No response from backend

**Possible Causes:**
1. Backend is sleeping (Render free tier)
2. Wrong API URL
3. CORS error
4. Backend not running

**Solutions:**

1. **Check Backend is Running:**
   - Visit: `https://crypto-dashboard-backend-6jum.onrender.com/api/health`
   - Should see: `{"status":"healthy",...}`
   - If error: Backend is sleeping, wait 30-60 seconds and try again

2. **Check API URL:**
   - Open browser console (F12)
   - Look for: `API URL: https://crypto-dashboard-backend-6jum.onrender.com/api`
   - If it shows `http://localhost:5000/api`: Environment variable not set correctly

3. **Check CORS:**
   - If you see CORS error in console
   - Make sure `CORS_ORIGINS` in Render includes your Netlify URL

---

### Error 2: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Symptoms:**
- Console shows CORS error
- Request blocked by browser

**Solution:**
1. Get your Netlify URL (e.g., `https://your-site.netlify.app`)
2. Go to Render → Your backend → Environment
3. Add/update `CORS_ORIGINS` with your Netlify URL
4. Save and wait for redeploy (2-3 minutes)
5. Try again

---

### Error 3: "User with this email already exists"

**Symptoms:**
- Error message: "User with this email already exists"
- Status: 400

**Solution:**
- This is normal - the email is already registered
- Try a different email or login instead

---

### Error 4: "Missing required fields"

**Symptoms:**
- Error message: "Missing required fields: email, password, name"
- Status: 400

**Solution:**
- Make sure all fields are filled
- Check that name, email, and password are provided

---

### Error 5: "Registration failed" or Generic Error

**Symptoms:**
- Generic error message
- Status: 500

**Possible Causes:**
- MongoDB connection issue
- Backend error

**Solution:**
1. Check Render backend logs
2. Look for MongoDB connection errors
3. Verify `MONGO_URI` is set correctly in Render

---

## How to Debug

### Step 1: Check Browser Console

1. Open browser console (F12)
2. Go to **Console** tab
3. Try to sign up
4. Look for error messages
5. **Copy the exact error message**

### Step 2: Check Network Tab

1. Open browser console (F12)
2. Go to **Network** tab
3. Try to sign up
4. Find the `/api/auth/register` request
5. Click on it
6. Check:
   - **Request URL**: Should be `https://crypto-dashboard-backend-6jum.onrender.com/api/auth/register`
   - **Status**: 
     - `200` or `201` = Success ✅
     - `400` = Bad request (validation error)
     - `500` = Server error
     - `CORS error` = CORS not configured
   - **Response**: What does the response say?

### Step 3: Check Backend Logs

1. Go to Render Dashboard
2. Your backend service → **Logs** tab
3. Try to sign up
4. Watch the logs for errors

### Step 4: Test Backend Directly

**Test registration endpoint:**
```bash
# Using curl (or use Postman)
curl -X POST https://crypto-dashboard-backend-6jum.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","name":"Test User"}'
```

**Expected response:**
- Success: `{"message":"User registered successfully","access_token":"...","user":{...}}`
- Error: `{"error":"..."}`

---

## Quick Checklist

- [ ] Backend is accessible (test `/api/health`)
- [ ] `REACT_APP_API_URL` is set in Netlify
- [ ] `CORS_ORIGINS` is set in Render with Netlify URL
- [ ] Browser console shows correct API URL
- [ ] Network tab shows request going to correct URL
- [ ] No CORS errors in console
- [ ] All form fields are filled

---

## Most Common Issues

**90% of signup issues are:**

1. **CORS not configured**
   - Fix: Add Netlify URL to `CORS_ORIGINS` in Render

2. **Backend sleeping (Render free tier)**
   - Fix: Wait 30-60 seconds for first request, then try again

3. **Wrong API URL**
   - Fix: Check `REACT_APP_API_URL` in Netlify environment variables

---

## Share These Details for Help

1. **Exact error message** from browser console
2. **Network tab status code** (200, 400, 500, CORS error?)
3. **Request URL** shown in Network tab
4. **Backend health check** result (`/api/health`)
5. **Your Netlify URL** (to verify CORS)

