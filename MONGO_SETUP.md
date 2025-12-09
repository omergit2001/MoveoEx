# MongoDB Local Setup Guide

## ✅ Good News!

MongoDB is already installed and running on your system!

## Current Configuration

Your MongoDB service is running. The connection string has been set to:
```
mongodb://localhost:27017/crypto_dashboard
```

## Verify MongoDB is Working

### Option 1: Using MongoDB Compass (GUI - Recommended)

1. Download MongoDB Compass: https://www.mongodb.com/try/download/compass
2. Install and open MongoDB Compass
3. Connect using: `mongodb://localhost:27017`
4. You should see your databases

### Option 2: Using Command Line

Once you have the backend virtual environment set up:

```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017/'); print('Connected!'); print('Databases:', client.list_database_names())"
```

## MongoDB Service Management

### Check if MongoDB is running:
```powershell
Get-Service -Name MongoDB
```

### Start MongoDB (if stopped):
```powershell
Start-Service -Name MongoDB
```

### Stop MongoDB:
```powershell
Stop-Service -Name MongoDB
```

### Restart MongoDB:
```powershell
Restart-Service -Name MongoDB
```

## Database Creation

The database `crypto_dashboard` will be created automatically when you first run the backend application. You don't need to create it manually!

## Collections

The app will automatically create these collections:
- `users` - User accounts and preferences
- `feedback` - User feedback/votes

## Default Connection

Your `backend/.env` file is configured with:
```
MONGO_URI=mongodb://localhost:27017/crypto_dashboard
```

## Troubleshooting

### MongoDB service not running:
```powershell
# Check status
Get-Service -Name MongoDB

# Start it
Start-Service -Name MongoDB
```

### Connection refused:
- Make sure MongoDB service is running
- Check if MongoDB is listening on port 27017:
  ```powershell
  netstat -an | findstr 27017
  ```

### Permission issues:
- Make sure you're running as Administrator if needed
- Check MongoDB logs (usually in `C:\Program Files\MongoDB\Server\<version>\log\`)

## Next Steps

1. ✅ MongoDB is running
2. ✅ Connection string configured
3. Now start your backend server:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python run.py
   ```

The database will be created automatically when you first register a user!

