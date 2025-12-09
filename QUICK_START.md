# Quick Start Guide - Run Locally

## ✅ What's Already Done

- ✅ Backend `.env` file created with secret keys
- ✅ Frontend `.env` file created with API URL
- ✅ All configuration files are ready

## 🚀 Next Steps

### 1. Set Up MongoDB

You need a MongoDB database. Choose one:

**Option A: MongoDB Atlas (Free, Recommended)**
1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create free account → Create free cluster
3. Create database user (username/password)
4. Network Access → Add IP Address (0.0.0.0/0 for development)
5. Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/crypto_dashboard?retryWrites=true&w=majority`
6. Update `backend/.env` file: Replace `MONGO_URI` with your connection string

**Option B: Local MongoDB**
- Install MongoDB locally
- Start MongoDB service
- Connection string: `mongodb://localhost:27017/crypto_dashboard`
- Update `backend/.env` file: Set `MONGO_URI=mongodb://localhost:27017/crypto_dashboard`

### 2. Start Backend Server

Open a terminal in the `backend` folder:

```bash
# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start server
python run.py
```

**OR use the quick start script:**
- Windows: Double-click `start_local.bat`
- Mac/Linux: Run `bash start_local.sh`

You should see: `* Running on http://0.0.0.0:5000`

### 3. Start Frontend (New Terminal)

Open a NEW terminal in the `frontend` folder:

```bash
# Install dependencies (first time only)
npm install

# Start React app
npm start
```

**OR use the quick start script:**
- Windows: Double-click `start_local.bat`
- Mac/Linux: Run `bash start_local.sh`

The app will open at `http://localhost:3000`

### 4. Test the App

1. **Sign Up**: Create a new account
2. **Onboarding**: Complete the quiz (3 steps)
3. **Dashboard**: See your personalized content!

## 🔧 Troubleshooting

**Backend won't start:**
- Check MongoDB connection string in `backend/.env`
- Make sure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`

**Frontend can't connect:**
- Make sure backend is running on port 5000
- Check `frontend/.env` has: `REACT_APP_API_URL=http://localhost:5000/api`

**MongoDB connection error:**
- Verify your connection string
- Check MongoDB Atlas IP whitelist (should include your IP or 0.0.0.0/0)
- Test connection in MongoDB Compass

## 📝 Important Files

- `backend/.env` - Backend configuration (MongoDB URI, secret keys)
- `frontend/.env` - Frontend configuration (API URL)
- `LOCAL_SETUP.md` - Detailed setup instructions

## 🎉 You're Ready!

Once both servers are running:
- Backend: http://localhost:5000
- Frontend: http://localhost:3000

Open your browser to http://localhost:3000 and start testing!

