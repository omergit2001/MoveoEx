# Fix for Render Start Command Error

## The Problem
You're getting: `gunicorn.errors.AppImportError: Failed to find attribute 'app' in 'app'`

This happens because there's both:
- `backend/app.py` (a file)
- `backend/app/` (a directory/package)

Python gets confused about which `app` to import.

## The Solution

### Step 1: Update Start Command in Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click on your web service**
3. **Go to "Settings" tab**
4. **Find "Start Command" field**
5. **Change it to**:
   ```
   gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
   ```
   ⚠️ **Important**: Use `wsgi:app` NOT `app:app`

6. **Click "Save Changes"**
7. **Render will automatically redeploy**

### Step 2: Verify the Fix

After redeploy:
- Check the logs - should see "Starting service..."
- Visit: `https://your-backend-url.onrender.com/api/auth/me`
- Should see an error (401) - this means it's working! ✅

## Alternative: If wsgi:app doesn't work

If `wsgi:app` still doesn't work, try this start command instead:

```
python -m gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
```

Or this one:

```
gunicorn --chdir . -w 4 -b 0.0.0.0:$PORT wsgi:app
```

## What Changed

- **Before**: `gunicorn ... app:app` (confused between app.py and app/ package)
- **After**: `gunicorn ... wsgi:app` (uses dedicated wsgi.py file)

The `wsgi.py` file is now in your repository and will work correctly.

## Still Having Issues?

If you still get errors:
1. Check Render logs for the exact error
2. Make sure Root Directory is set to `backend` in Render settings
3. Verify all environment variables are set
4. Try the alternative start commands above

