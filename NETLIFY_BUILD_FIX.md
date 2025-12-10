# Netlify Build Error Fix

## Error: "Build script returned non-zero exit code: 2"

This error means the build command failed. Here's how to fix it:

---

## Solution 1: Configure Build Settings in Netlify Dashboard

**The most important step - you MUST set the base directory:**

1. **Go to Netlify Dashboard**
   - Visit: https://app.netlify.com
   - Select your site

2. **Go to Site Settings**
   - Click **"Site settings"** → **"Build & deploy"** → **"Build settings"**

3. **Edit Build Settings**
   - Click **"Edit settings"**
   
4. **Set these values:**
   - **Base directory**: `frontend`
   - **Build command**: `npm install && npm run build`
   - **Publish directory**: `frontend/build`
   
   ⚠️ **CRITICAL**: The base directory MUST be `frontend` because your React app is in a subdirectory!

5. **Set Node Version** (optional but recommended)
   - Scroll down to **"Environment variables"**
   - Add: `NODE_VERSION` = `18`
   - Or go to **"Build & deploy"** → **"Environment"** → Add variable

6. **Save and Redeploy**
   - Click **"Save"**
   - Go to **"Deploys"** tab
   - Click **"Trigger deploy"** → **"Deploy site"**

---

## Solution 2: Check Build Logs

1. **Go to Deploys tab**
   - Click on the failed deploy
   - Click **"View build log"**

2. **Look for specific errors:**
   - `npm ERR!` → Dependency installation failed
   - `Cannot find module` → Missing dependency
   - `Command not found` → Wrong build command
   - `ENOENT` → File/directory not found

3. **Common issues:**
   - **"Cannot find package.json"** → Base directory not set to `frontend`
   - **"npm ERR! code ELIFECYCLE"** → Build script failed
   - **"Out of memory"** → Need to increase Node memory

---

## Solution 3: Verify netlify.toml Location

The `netlify.toml` file should be in the **root** of your repository (not in the frontend folder).

**If it's in the wrong place:**
1. Move it to the root directory
2. Update it with the correct base directory

**Current structure should be:**
```
MoveoEx/
├── frontend/
│   ├── package.json
│   ├── src/
│   └── ...
├── backend/
└── netlify.toml  ← Should be here (root)
```

**If netlify.toml is in frontend/, move it to root:**
```bash
# From project root
mv frontend/netlify.toml netlify.toml
```

---

## Solution 4: Manual Build Test

**Test the build locally to see the error:**

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run build:**
   ```bash
   npm run build
   ```

4. **If it fails locally:**
   - Fix the error
   - Commit and push
   - Redeploy on Netlify

---

## Solution 5: Alternative Build Configuration

**If base directory doesn't work, try this in Netlify dashboard:**

1. **Base directory**: Leave empty or set to `.`
2. **Build command**: `cd frontend && npm install && npm run build`
3. **Publish directory**: `frontend/build`

---

## Quick Fix Checklist

- [ ] Base directory set to `frontend` in Netlify dashboard
- [ ] Build command: `npm install && npm run build`
- [ ] Publish directory: `frontend/build`
- [ ] `netlify.toml` is in root directory (not in frontend/)
- [ ] Node version set to 18 (in environment variables)
- [ ] Checked build logs for specific error
- [ ] Tested build locally (`cd frontend && npm run build`)

---

## Most Common Fix

**90% of build failures are because:**
- Base directory is NOT set to `frontend`
- Netlify tries to build from root and can't find `package.json`

**Fix:**
1. Go to Netlify → Site settings → Build & deploy → Build settings
2. Set **Base directory** = `frontend`
3. Set **Build command** = `npm install && npm run build`
4. Set **Publish directory** = `frontend/build`
5. Save and redeploy

---

## Still Not Working?

**Share these details:**
1. Screenshot of Netlify build settings (Base directory, Build command, Publish directory)
2. Build log output (last 50 lines)
3. Result of local build test (`cd frontend && npm run build`)

