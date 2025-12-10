# MongoDB Connection Fix Guide

## Step 1: Get Your MongoDB Connection String

### Option A: If you already have MongoDB Atlas

1. **Go to MongoDB Atlas**
   - Visit: https://cloud.mongodb.com
   - Sign in to your account

2. **Get Connection String**
   - Click **"Connect"** on your cluster
   - Choose **"Connect your application"**
   - Copy the connection string
   - It should look like:
     ```
     mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
     ```

3. **Add Database Name**
   - Replace the `?` with `/crypto_dashboard?`
   - Final format:
     ```
     mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
     ```

### Option B: Create New MongoDB Atlas Cluster (Free)

1. **Sign Up/Login**
   - Visit: https://www.mongodb.com/cloud/atlas/register
   - Create free account

2. **Create Free Cluster**
   - Choose **"M0 Free"** tier
   - Select a region close to you
   - Click **"Create Cluster"**
   - Wait 3-5 minutes for cluster to be created

3. **Create Database User**
   - Go to **"Database Access"** (left sidebar)
   - Click **"Add New Database User"**
   - Choose **"Password"** authentication
   - Username: Choose a username (e.g., `crypto_user`)
   - Password: Click **"Autogenerate Secure Password"** or create your own
   - **SAVE THE PASSWORD!** You'll need it
   - Click **"Add User"**

4. **Configure Network Access**
   - Go to **"Network Access"** (left sidebar)
   - Click **"Add IP Address"**
   - Click **"Allow Access from Anywhere"** (for development)
   - This adds `0.0.0.0/0`
   - Click **"Confirm"**

5. **Get Connection String**
   - Go back to **"Clusters"** → Click **"Connect"** on your cluster
   - Choose **"Connect your application"**
   - Copy the connection string
   - Replace `<password>` with your database user password
   - Replace `?` with `/crypto_dashboard?`
   - Final format:
     ```
     mongodb+srv://crypto_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
     ```

---

## Step 2: Set MONGO_URI in Render

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Select your backend service

2. **Go to Environment Tab**
   - Click **"Environment"** tab

3. **Add/Update MONGO_URI**
   - Look for `MONGO_URI` variable
   - If it exists: Click to edit
   - If it doesn't exist: Click **"Add Environment Variable"**
   - **Key**: `MONGO_URI`
   - **Value**: Your full connection string from Step 1
   - Example:
     ```
     mongodb+srv://crypto_user:MyPassword123@cluster0.7iwhuok.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
     ```

4. **Important Notes:**
   - ⚠️ **URL Encode Special Characters**: If your password has special characters like `@`, `#`, `!`, etc., you need to URL-encode them:
     - `@` → `%40`
     - `#` → `%23`
     - `!` → `%21`
     - `&` → `%26`
     - `%` → `%25`
   - ⚠️ **Include Database Name**: Make sure `/crypto_dashboard` is in the connection string
   - ⚠️ **No Spaces**: Remove any spaces in the connection string

5. **Save Changes**
   - Click **"Save Changes"**
   - Render will automatically redeploy (wait 2-3 minutes)

---

## Step 3: Verify Connection String Format

**Correct Format:**
```
mongodb+srv://username:password@cluster.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
```

**Checklist:**
- ✅ Starts with `mongodb+srv://`
- ✅ Has username and password
- ✅ Has cluster address
- ✅ Has `/crypto_dashboard` (database name)
- ✅ Has query parameters `?retryWrites=true&w=majority`
- ✅ No spaces
- ✅ Special characters are URL-encoded

---

## Step 4: Test the Connection

### Test 1: Check Render Logs

1. **Go to Render Dashboard** → Your backend → **Logs** tab
2. **Look for MongoDB connection messages**
3. **Should see**: Connection successful or connection errors

### Test 2: Test Backend Health Endpoint

1. **Visit**: `https://crypto-dashboard-backend-6jum.onrender.com/api/health`
2. **Should see**: `{"status":"healthy",...}`

### Test 3: Try Registration Again

1. **Go to your Netlify site**
2. **Try to sign up**
3. **Check browser console** for errors
4. **Check Render logs** for MongoDB errors

---

## Common Issues & Solutions

### Issue 1: "ServerSelectionTimeoutError"

**Cause**: MongoDB Atlas network access not configured

**Fix**:
1. Go to MongoDB Atlas → Network Access
2. Add IP address: `0.0.0.0/0` (allow from anywhere)
3. Wait 2-3 minutes
4. Try again

### Issue 2: "Authentication failed"

**Cause**: Wrong username or password

**Fix**:
1. Check username and password in connection string
2. Make sure password doesn't have unencoded special characters
3. URL-encode special characters in password
4. Verify database user exists in MongoDB Atlas

### Issue 3: "Invalid URI scheme"

**Cause**: Wrong connection string format

**Fix**:
1. Make sure it starts with `mongodb+srv://` or `mongodb://`
2. Check for typos
3. Make sure database name is included: `/crypto_dashboard`

### Issue 4: Password Has Special Characters

**If your password has special characters**, you need to URL-encode them:

**Example:**
- Original password: `MyP@ss#123!`
- URL-encoded: `MyP%40ss%23123%21`

**Common encodings:**
- `@` → `%40`
- `#` → `%23`
- `!` → `%21`
- `$` → `%24`
- `&` → `%26`
- `%` → `%25`
- `+` → `%2B`
- `=` → `%3D`

**Or use an online URL encoder:**
- Visit: https://www.urlencoder.org/
- Paste your password
- Copy encoded version
- Use in connection string

---

## Quick Fix Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user created with username and password
- [ ] Network Access allows `0.0.0.0/0` (or specific IPs)
- [ ] Connection string copied from MongoDB Atlas
- [ ] Password replaced in connection string
- [ ] Database name `/crypto_dashboard` added to connection string
- [ ] Special characters in password are URL-encoded
- [ ] `MONGO_URI` set in Render environment variables
- [ ] Render backend redeployed after setting `MONGO_URI`
- [ ] Tested connection (check Render logs)

---

## Example Connection String

**If your MongoDB Atlas connection string is:**
```
mongodb+srv://crypto_user:<password>@cluster0.7iwhuok.mongodb.net/?retryWrites=true&w=majority
```

**And your password is:** `MyP@ss#123!`

**Your final MONGO_URI should be:**
```
mongodb+srv://crypto_user:MyP%40ss%23123%21@cluster0.7iwhuok.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
```

**Note**: Password is URL-encoded and database name is added.

---

## Still Having Issues?

**Share these details:**
1. Error message from Render logs
2. Your connection string format (hide password)
3. Whether network access is configured in MongoDB Atlas
4. Whether database user exists

I can help you fix the specific issue!

