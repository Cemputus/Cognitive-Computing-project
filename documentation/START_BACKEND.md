# Starting the Backend Server

## Quick Start

The backend server is now running in the background!

**Server URL**: `http://localhost:5000`

## API Endpoints Available

### Authentication
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user (requires auth)
- `GET /api/auth/users` - Get all users (admin only)

### Business Intelligence
- `POST /api/sentiment/analyze` - Analyze sentiment (requires auth)
- `POST /api/sentiment/batch` - Batch analyze (requires auth)
- `GET /api/topics` - Get topics (requires auth)
- `GET /api/forecast` - Get forecast (requires auth)
- `GET /api/dashboard/stats` - Dashboard stats (requires auth)

## Sample Users

### Admin Account
- **Email**: `admin@business.com`
- **Password**: `admin123`

### Regular Users (7 users)
- **Email**: `user1@business.com` to `user7@business.com`
- **Password**: `user123` (for all)

## Testing

1. **Frontend**: Open `http://localhost:3000`
2. **Backend**: Running on `http://localhost:5000`
3. **Login**: Use any of the sample accounts above

## Notes

- All API endpoints (except `/api/auth/login` and `/api/health`) require authentication
- JWT tokens are valid for 24 hours
- Tokens are automatically included in requests via axios interceptor

---

**Status**: ✅ Backend running in background

