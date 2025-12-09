# Local Development Setup Guide

Quick guide to run the Crypto Dashboard locally for testing.

## Prerequisites

- Python 3.11+ installed
- Node.js 16+ and npm installed
- MongoDB (local or MongoDB Atlas free tier)

## Step 1: Set Up MongoDB

### Option A: MongoDB Atlas (Recommended - Free)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Create a free account and cluster
3. Create a database user (username/password)
4. Whitelist your IP (or use 0.0.0.0/0 for development)
5. Get your connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/...`)

### Option B: Local MongoDB

1. Install MongoDB locally
2. Start MongoDB service
3. Connection string: `mongodb://localhost:27017/crypto_dashboard`

## Step 2: Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create .env file:**
   ```bash
   copy .env.example .env
   ```
   (On Mac/Linux: `cp .env.example .env`)

6. **Edit .env file** with your values:
   ```env
   SECRET_KEY=your-random-secret-key-here
   JWT_SECRET_KEY=your-random-jwt-secret-key-here
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/crypto_dashboard?retryWrites=true&w=majority
   OPENROUTER_API_KEY=your-openrouter-key-optional
   ```

   **Quick secret keys** (for development only):
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

7. **Run the backend server:**
   ```bash
   python run.py
   ```

   You should see:
   ```
   * Running on http://0.0.0.0:5000
   ```

## Step 3: Frontend Setup

1. **Open a new terminal** and navigate to frontend:
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create .env file:**
   ```bash
   copy .env.example .env
   ```
   (On Mac/Linux: `cp .env.example .env`)

4. **Edit .env file:**
   ```env
   REACT_APP_API_URL=http://localhost:5000/api
   ```

5. **Start the React app:**
   ```bash
   npm start
   ```

   The app should open automatically at `http://localhost:3000`

## Step 4: Test the Application

1. **Sign Up**: Create a new account
2. **Onboarding**: Complete the 3-step onboarding quiz
3. **Dashboard**: View your personalized dashboard with:
   - Market News
   - Coin Prices
   - AI Insight
   - Fun Meme
4. **Feedback**: Click thumbs up/down on any content

## Troubleshooting

### Backend Issues

**Import errors:**
- Make sure you're in the `backend` directory when running `python run.py`
- Ensure virtual environment is activated
- Check that all packages are installed: `pip list`

**MongoDB connection errors:**
- Verify your MONGO_URI in `.env` is correct
- Check MongoDB Atlas IP whitelist
- Test connection string in MongoDB Compass

**Port already in use:**
- Change port in `run.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`
- Update frontend `.env`: `REACT_APP_API_URL=http://localhost:5001/api`

### Frontend Issues

**API connection errors:**
- Verify backend is running on port 5000
- Check `REACT_APP_API_URL` in frontend `.env`
- Look for CORS errors in browser console

**Module not found:**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

**Port 3000 already in use:**
- React will automatically use the next available port
- Or set PORT in `.env`: `PORT=3001`

## Quick Test Commands

**Test backend API:**
```bash
curl http://localhost:5000/api/auth/register -X POST -H "Content-Type: application/json" -d "{\"email\":\"test@test.com\",\"password\":\"test123\",\"name\":\"Test User\"}"
```

**Check MongoDB connection:**
```python
from pymongo import MongoClient
client = MongoClient("your-mongo-uri")
print(client.list_database_names())
```

## Next Steps

Once everything is running locally:
1. Test all features
2. Check browser console for errors
3. Verify data is being saved to MongoDB
4. Test feedback submission
5. Ready for deployment!

