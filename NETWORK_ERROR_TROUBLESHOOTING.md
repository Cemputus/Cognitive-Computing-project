# Network Error Troubleshooting Guide

## Issue: Network Error when accessing the frontend

This error typically occurs when the backend API server is not running or not accessible.

## Solution Steps:

### 1. Start the Backend Server

**Option A: Using PowerShell (Recommended)**
```powershell
# Navigate to backend directory
cd D:\Cognitive Computing\backend

# Start the server
python backend_api.py
```

**Option B: Using the provided script**
```powershell
# From project root
cd D:\Cognitive Computing
.\backend\scripts\start_backend.ps1
```

**Option C: Using Batch file**
```cmd
# From project root
cd D:\Cognitive Computing
.\backend\scripts\start_backend.bat
```

### 2. Verify Backend is Running

You should see output like:
```
Starting Business Intelligence Analyst Backend...
Backend will be available at: http://localhost:5000
 * Running on http://127.0.0.1:5000
 * Running on http://[::1]:5000
Press CTRL+C to quit
```

### 3. Test Backend Connection

Open your browser and navigate to:
- `http://localhost:5000/api/auth/users` (should return user list if working)

Or test with curl:
```powershell
curl http://localhost:5000/api/auth/users
```

### 4. Check Frontend Configuration

The frontend is configured to connect to `http://localhost:5000/api` by default.

If you need to change this, update `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'
```

### 5. Common Issues

**Issue: Port 5000 already in use**
- Solution: Stop any other application using port 5000, or change the port in `backend_api.py`:
  ```python
  app.run(debug=True, port=5001)  # Change to different port
  ```
  Then update frontend API URL accordingly.

**Issue: ModuleNotFoundError when starting backend**
- Solution: Install dependencies:
  ```powershell
  cd D:\Cognitive Computing\backend
  pip install -r requirements.txt
  ```

**Issue: CORS errors**
- The backend already has CORS enabled. If you still see CORS errors, check that:
  - Backend is running on port 5000
  - Frontend is making requests to `http://localhost:5000/api/*`
  - CORS is properly configured in `backend_api.py` (line 42)

### 6. Verify Both Servers are Running

You need **both** servers running:
1. **Backend** (Flask): `http://localhost:5000`
2. **Frontend** (Vite/React): Usually `http://localhost:5173` or similar

### 7. Quick Test

1. Start backend: `cd backend && python backend_api.py`
2. In another terminal, start frontend: `cd frontend && npm run dev`
3. Open browser to frontend URL (usually shown in terminal)
4. Try logging in with: `admin@business.com` / `admin123`

## Still Having Issues?

1. Check browser console (F12) for specific error messages
2. Check backend terminal for error logs
3. Verify firewall isn't blocking port 5000
4. Ensure both servers are running simultaneously













## Issue: Network Error when accessing the frontend

This error typically occurs when the backend API server is not running or not accessible.

## Solution Steps:

### 1. Start the Backend Server

**Option A: Using PowerShell (Recommended)**
```powershell
# Navigate to backend directory
cd D:\Cognitive Computing\backend

# Start the server
python backend_api.py
```

**Option B: Using the provided script**
```powershell
# From project root
cd D:\Cognitive Computing
.\backend\scripts\start_backend.ps1
```

**Option C: Using Batch file**
```cmd
# From project root
cd D:\Cognitive Computing
.\backend\scripts\start_backend.bat
```

### 2. Verify Backend is Running

You should see output like:
```
Starting Business Intelligence Analyst Backend...
Backend will be available at: http://localhost:5000
 * Running on http://127.0.0.1:5000
 * Running on http://[::1]:5000
Press CTRL+C to quit
```

### 3. Test Backend Connection

Open your browser and navigate to:
- `http://localhost:5000/api/auth/users` (should return user list if working)

Or test with curl:
```powershell
curl http://localhost:5000/api/auth/users
```

### 4. Check Frontend Configuration

The frontend is configured to connect to `http://localhost:5000/api` by default.

If you need to change this, update `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'
```

### 5. Common Issues

**Issue: Port 5000 already in use**
- Solution: Stop any other application using port 5000, or change the port in `backend_api.py`:
  ```python
  app.run(debug=True, port=5001)  # Change to different port
  ```
  Then update frontend API URL accordingly.

**Issue: ModuleNotFoundError when starting backend**
- Solution: Install dependencies:
  ```powershell
  cd D:\Cognitive Computing\backend
  pip install -r requirements.txt
  ```

**Issue: CORS errors**
- The backend already has CORS enabled. If you still see CORS errors, check that:
  - Backend is running on port 5000
  - Frontend is making requests to `http://localhost:5000/api/*`
  - CORS is properly configured in `backend_api.py` (line 42)

### 6. Verify Both Servers are Running

You need **both** servers running:
1. **Backend** (Flask): `http://localhost:5000`
2. **Frontend** (Vite/React): Usually `http://localhost:5173` or similar

### 7. Quick Test

1. Start backend: `cd backend && python backend_api.py`
2. In another terminal, start frontend: `cd frontend && npm run dev`
3. Open browser to frontend URL (usually shown in terminal)
4. Try logging in with: `admin@business.com` / `admin123`

## Still Having Issues?

1. Check browser console (F12) for specific error messages
2. Check backend terminal for error logs
3. Verify firewall isn't blocking port 5000
4. Ensure both servers are running simultaneously
















