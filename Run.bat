@echo off
title SkillLoop Launcher
echo.
echo ==========================================
echo      SkillLoop Prototype Launcher
echo ==========================================
echo.

echo [1/2] Starting Flask Backend (Port 5000)...
cd /d "%~dp0"
:: Try python first, fallback to py if python is not in PATH
start "SkillLoop - Backend" cmd /k "python app.py || py app.py"

:: Wait 3 seconds to let backend start up
timeout /t 3 /nobreak >nul

echo [2/2] Starting Nuxt Frontend (Port 3000)...
cd /d "%~dp0frontend"
start "SkillLoop - Frontend" cmd /k "npm run dev"

echo.
echo Both servers are launching in separate windows!
echo.
echo Frontend : http://localhost:3000
echo Backend  : http://127.0.0.1:5000
echo Network   : http://%IP%:3000 (Check ipconfig for LAN teammate testing)
echo.
echo (You can safely close this launcher window now, the servers will keep running in their own windows)
echo ==========================================
pause >nul
