# Run Both Servers - PowerShell Script
# This script starts the Flask API and React frontend in separate windows

Write-Host "🚀 Starting Theme Park Crowd Detection System..." -ForegroundColor Cyan

# Start API Server in new window
Write-Host "📡 Starting Flask API Server on port 5000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python api_server.py"

# Wait a moment for API to start
Start-Sleep -Seconds 3

# Start React Frontend in new window
Write-Host "🌐 Starting React Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "✅ Both servers are starting!" -ForegroundColor Green
Write-Host "📡 API: http://localhost:5000" -ForegroundColor Cyan
Write-Host "🌐 Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit (servers will keep running)..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
