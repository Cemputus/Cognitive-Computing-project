# PowerShell script to start the backend server
Write-Host "Starting Business Intelligence Analyst Backend..." -ForegroundColor Green
Write-Host ""

# Change to the backend directory
Set-Location -Path "backend"

# Start the Flask server
Write-Host "Backend will be available at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python backend_api.py

