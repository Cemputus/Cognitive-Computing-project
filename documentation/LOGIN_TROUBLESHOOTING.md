# Login Troubleshooting Guide

## Issue: 401 Unauthorized Error

If you're getting a 401 error when trying to login, here are the steps to troubleshoot:

## ✅ Verified Working

The login endpoint has been tested and works correctly:
- **Endpoint**: `POST /api/auth/login`
- **Status**: ✅ Working (returns 200 when tested directly)

## 🔍 Debug Steps

### 1. Check Backend Logs

When you try to login, check the backend console for debug messages:
- `Login attempt: email=...` - Shows the request was received
- `Authentication successful for: ...` - Shows authentication passed
- `ERROR: ...` - Shows any errors

### 2. Test Login Directly

Test the endpoint using PowerShell:
```powershell
$body = @{email='admin@business.com'; password='admin123'} | ConvertTo-Json
Invoke-WebRequest -Uri 'http://localhost:5000/api/auth/login' -Method POST -Body $body -ContentType 'application/json'
```

### 3. Check CORS

The backend has CORS enabled for all origins. If you still see CORS errors:
- Make sure the backend is running on `http://localhost:5000`
- Check browser console for CORS errors
- Verify frontend is making requests to the correct URL

### 4. Verify Credentials

**Admin Account:**
- Email: `admin@business.com`
- Password: `admin123`

**User Accounts:**
- Email: `user1@business.com` through `user7@business.com`
- Password: `user123` (for all)

### 5. Check Frontend Request

Open browser DevTools → Network tab:
1. Try to login
2. Find the `/api/auth/login` request
3. Check:
   - Request Method: Should be `POST`
   - Request Headers: Should include `Content-Type: application/json`
   - Request Payload: Should have `email` and `password`
   - Response Status: Check if it's 401 or another error

### 6. Common Issues

#### Issue: "Request body is required"
- **Cause**: Frontend not sending JSON properly
- **Fix**: Check that `Content-Type: application/json` header is set

#### Issue: "Invalid email or password"
- **Cause**: Wrong credentials or authentication failure
- **Fix**: 
  - Verify email and password are correct
  - Check backend logs for authentication details
  - Make sure password is not being modified (trimmed, encoded, etc.)

#### Issue: CORS Error
- **Cause**: Backend not allowing frontend origin
- **Fix**: CORS is already configured for all origins, but check:
  - Backend is running
  - Frontend URL matches what backend expects
  - No firewall blocking requests

## 🔧 Backend Configuration

### CORS Settings
```python
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
```

### Login Endpoint
- **URL**: `/api/auth/login`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**: `{"email": "...", "password": "..."}`

## 📝 Debug Logging

The backend includes debug logging in the login endpoint:
- Login attempts are logged
- Authentication failures are logged
- Errors include full traceback

To see logs, check the console where `backend_api.py` is running.

## ✅ Solution Applied

The following improvements have been made:
1. ✅ Enhanced CORS configuration
2. ✅ Added OPTIONS method handling for CORS preflight
3. ✅ Improved error handling and logging
4. ✅ Better request validation
5. ✅ Debug logging for troubleshooting

## 🚀 Next Steps

If login still fails after checking the above:
1. Check backend console for error messages
2. Check browser console for frontend errors
3. Check Network tab for request/response details
4. Verify backend is running: `python backend_api.py`
5. Verify frontend is pointing to correct URL: `http://localhost:5000`

---

**Last Updated**: December 2025


