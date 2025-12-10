# Fix MongoDB URI Error in Render

## The Error
```
pymongo.errors.InvalidURI: Invalid URI scheme: URI must begin with 'mongodb://' or 'mongodb+srv://'
```

This means the `MONGO_URI` environment variable in Render is either:
- Not set
- Has extra spaces
- Is missing the `mongodb+srv://` prefix
- Has special characters that need encoding

## The Correct MongoDB URI

Your MongoDB connection string should be:
```
mongodb+srv://omergit2001_db_user:Omerc2001!@cluster0.7iwhuok.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
```

## How to Fix in Render

### Step 1: Go to Render Dashboard
1. Visit: https://dashboard.render.com
2. Click on your web service

### Step 2: Check Environment Variables
1. Go to **"Environment"** tab (or **"Environment Variables"** section)
2. Find `MONGO_URI` in the list
3. Click on it to edit

### Step 3: Set the Correct Value
**Copy and paste this EXACT value** (no extra spaces before or after):
```
mongodb+srv://omergit2001_db_user:Omerc2001!@cluster0.7iwhuok.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
```

⚠️ **Important**:
- Make sure there are NO spaces before or after
- Make sure it starts with `mongodb+srv://`
- Make sure it includes `/crypto_dashboard` before the `?`
- The password `Omerc2001!` contains special characters - make sure they're preserved

### Step 4: Save and Redeploy
1. Click **"Save Changes"**
2. Render will automatically redeploy
3. Wait 2-3 minutes
4. Check logs to verify it connects

## If the Password Has Special Characters

If Render is having issues with the `!` in your password, you might need to URL-encode it:

The `!` character should be encoded as `%21`

So the URI would become:
```
mongodb+srv://omergit2001_db_user:Omerc2001%21@cluster0.7iwhuok.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
```

## Verify the URI is Correct

The URI should have this structure:
```
mongodb+srv://[username]:[password]@[cluster]/[database]?[options]
```

Your URI breakdown:
- **Scheme**: `mongodb+srv://`
- **Username**: `omergit2001_db_user`
- **Password**: `Omerc2001!` (or `Omerc2001%21` if URL-encoded)
- **Cluster**: `cluster0.7iwhuok.mongodb.net`
- **Database**: `crypto_dashboard`
- **Options**: `retryWrites=true&w=majority`

## Test After Fix

After updating and redeploying:
1. Check Render logs - should see "Starting service..." without MongoDB errors
2. Visit: `https://your-backend-url.onrender.com/api/auth/me`
3. Try registering a user - if it works, MongoDB is connected! ✅

## Troubleshooting

### Still getting the error?
1. **Double-check for spaces**: Copy the URI again, make sure no spaces
2. **Try URL-encoding the password**: Replace `!` with `%21`
3. **Check MongoDB Atlas**: Make sure your cluster is running and IP is whitelisted
4. **Verify database name**: Make sure `crypto_dashboard` is correct

### Common Mistakes:
- ❌ Missing `mongodb+srv://` at the start
- ❌ Extra spaces before/after the URI
- ❌ Missing `/crypto_dashboard` before the `?`
- ❌ Wrong password (special characters not encoded)
- ❌ Database name typo

## Quick Copy-Paste Value

Here's the exact value to paste (try this first):
```
mongodb+srv://omergit2001_db_user:Omerc2001!@cluster0.7iwhuok.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
```

If that doesn't work, try with URL-encoded password:
```
mongodb+srv://omergit2001_db_user:Omerc2001%21@cluster0.7iwhuok.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
```

