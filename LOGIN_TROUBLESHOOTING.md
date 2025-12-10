# Login Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: Frontend Can't Reach Backend

**Symptoms:**
- Error in browser console about network/CORS
- "Failed to fetch" or "Network Error"

**Check:**
1. Open browser console (F12)
2. Go to **Network** tab
3. Try to login
4. Look for the `/auth/login` request
5. Check if it's going to the correct URL

**Fix:**
- Verify `REACT_APP_API_URL` is set correctly in Vercel/Netlify
- Should be: `https://crypto-dashboard-backend-6jum.onrender.com/api`
- Make sure it ends with `/api` (not `/api/`)

---

### Issue 2: CORS Error

**Symptoms:**
- Browser console shows: "CORS policy" error
- Request fails with CORS error

**Fix:**
1. Go to Render dashboard
2. Your backend service → **Environment** tab
3. Add/update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app
   ```
4. Save and redeploy backend
5. Wait 2-3 minutes

---

### Issue 3: User Doesn't Exist

**Symptoms:**
- "The username or password is incorrect" error
- User was registered but can't login

**Check:**
1. Did you register the user on the deployed site or locally?
2. If registered locally, the user only exists in your local MongoDB
3. If registered on deployed site, check Render logs for registration errors

**Fix:**
- Register a new user on the deployed frontend
- This will create the user in MongoDB Atlas (production database)

---

### Issue 4: Password Verification Fails

**Symptoms:**
- User exists but password doesn't match
- "The username or password is incorrect" error

**Possible Causes:**
- User registered with different password
- Password hash mismatch
- Special characters in password

**Fix:**
- Try registering a new user with a simple password (no special characters)
- Then try logging in with that user

---

### Issue 5: MongoDB Connection Issue

**Symptoms:**
- Backend logs show MongoDB errors
- 500 Internal Server Error

**Check:**
1. Go to Render → Your backend → **Logs** tab
2. Look for MongoDB connection errors
3. Check if `MONGO_URI` is set correctly

**Fix:**
- Verify `MONGO_URI` in Render environment variables
- Should be: `mongodb+srv://omergit2001_db_user:Omerc2001!@cluster0.7iwhuok.mongodb.net/crypto_dashboard?retryWrites=true&w=majority`
- Check MongoDB Atlas Network Access (should allow 0.0.0.0/0)

---

## Debugging Steps

### Step 1: Check Browser Console
1. Open your frontend URL
2. Press F12 to open Developer Tools
3. Go to **Console** tab
4. Try to login
5. Look for error messages
6. Check what API URL is being used

### Step 2: Check Network Tab
1. In Developer Tools, go to **Network** tab
2. Try to login
3. Find the `/auth/login` request
4. Click on it
5. Check:
   - **Request URL**: Should be `https://crypto-dashboard-backend-6jum.onrender.com/api/auth/login`
   - **Status**: What status code? (200 = success, 401 = wrong credentials, 500 = server error)
   - **Response**: What does the response say?

### Step 3: Check Backend Logs
1. Go to Render dashboard
2. Your backend service → **Logs** tab
3. Try to login
4. Watch the logs for:
   - Database connection errors
   - Password verification errors
   - Any exception messages

### Step 4: Test Backend Directly
1. Open a new browser tab
2. Visit: `https://crypto-dashboard-backend-6jum.onrender.com/api/auth/me`
3. Should see: `{"msg":"Missing Authorization Header"}` - this means backend is working
4. If you see an error, backend has issues

---

## Quick Tests

### Test 1: Is Backend Running?
Visit: `https://crypto-dashboard-backend-6jum.onrender.com/api/auth/me`
- ✅ Should see: `{"msg":"Missing Authorization Header"}`
- ❌ If error: Backend is not running

### Test 2: Is Frontend Connecting?
1. Open browser console (F12)
2. Try to login
3. Check Network tab for `/auth/login` request
4. ✅ If request appears: Frontend is connecting
5. ❌ If no request: Frontend API URL is wrong

### Test 3: Register New User
1. Try to register a NEW user on the deployed site
2. If registration works, then try logging in with that user
3. This tests if the issue is with existing users or all users

---

## Most Common Fix

**90% of login issues are:**
1. **User doesn't exist in production database**
   - Solution: Register a new user on the deployed site

2. **Frontend API URL is wrong**
   - Solution: Check `REACT_APP_API_URL` in Vercel/Netlify
   - Should be: `https://crypto-dashboard-backend-6jum.onrender.com/api`

3. **CORS not configured**
   - Solution: Add `CORS_ORIGINS` in Render with your frontend URL

---

## Need More Help?

Share these details:
1. What error message do you see? (exact text)
2. What does browser console show? (F12 → Console)
3. What does Network tab show for the login request?
4. What do Render backend logs show?

