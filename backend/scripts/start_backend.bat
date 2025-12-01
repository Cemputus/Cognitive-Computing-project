@echo off
echo Starting Business Intelligence Analyst Backend...
echo.
REM Change to backend directory (script is in backend/scripts/)
cd ..
echo Backend will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python backend_api.py
pause

