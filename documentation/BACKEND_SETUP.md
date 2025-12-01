# Backend Setup & Start Guide

## ✅ Dependencies Installed

The following packages have been installed:
- `flask-cors` - For CORS support
- `PyJWT` - For JWT authentication

## 🚀 Starting the Backend

### Option 1: Using the Batch File (Easiest)
```bash
start_backend.bat
```

### Option 2: Using PowerShell Script
```powershell
.\start_backend.ps1
```

### Option 3: Manual Start
```powershell
cd src\api
python backend_api.py
```

## 📋 Expected Output

When the backend starts successfully, you should see:

```
Starting Business Intelligence Analyst API...
API will be available at http://localhost:5000

============================================================
Sample Users Created:
============================================================
Admin Account:
  Email: admin@business.com
  Password: admin123

User Accounts (7 users):
  User 1: user1@business.com / user123
  User 2: user2@business.com / user123
  ...
============================================================

 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## 🔍 Troubleshooting

### If you see "ModuleNotFoundError"
1. Make sure you're in the correct Python environment
2. Install missing packages: `pip install flask-cors PyJWT`
3. Or install all requirements: `pip install -r requirements.txt`

### If the server doesn't start
1. Check if port 5000 is already in use
2. Make sure all data files exist (the backend will work even if some are missing)
3. Check the console for error messages

## 🌐 Testing the Backend

Once running, test the health endpoint:
```powershell
curl http://localhost:5000/api/health
```

Or open in browser: `http://localhost:5000/api/health`

You should see: `{"status":"healthy","message":"API is running"}`

## 👤 Login Credentials

### Admin Account
- **Email**: `admin@business.com`
- **Password**: `admin123`

### Regular Users (7 users)
- **Email**: `user1@business.com` through `user7@business.com`
- **Password**: `user123` (for all)

## 🔗 Next Steps

1. ✅ Backend is running on `http://localhost:5000`
2. Start the frontend: `cd frontend && npm run dev`
3. Open browser: `http://localhost:3000`
4. Click "Login" in the top right
5. Use any of the credentials above to log in

---

**Status**: ✅ Dependencies installed and ready to start!

