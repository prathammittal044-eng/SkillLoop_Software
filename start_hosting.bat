@echo off
color 0B
title SkillLoop - Temporary Hosting (Ngrok)
echo.
echo  ================================================
echo        SkillLoop  ^|  Ngrok Professional Tunnel    
echo  ================================================
echo.

:: ── Step 1: Kill any stale servers ──────────────────────────────────────────
echo [Cleanup] Freeing ports 5000 and 3000 if occupied...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
timeout /t 1 /nobreak >nul

:: ── Step 2: Flask Backend ───────────────────────────────────────────────────
echo [1/3] Starting Flask Backend on port 5000...
start "SkillLoop - Flask Backend" cmd /k "title SkillLoop Flask Backend && py app.py"
timeout /t 3 /nobreak >nul

:: ── Step 3: Nuxt Frontend ───────────────────────────────────────────────────
echo [2/3] Starting Nuxt Frontend on port 3000...
start "SkillLoop - Nuxt Frontend" cmd /k "title SkillLoop Nuxt Frontend && cd frontend && npm run dev"
echo        Waiting 12 seconds for Nuxt to compile...
timeout /t 12 /nobreak >nul

:: ── Step 4: Ngrok Tunnel ────────────────────────────────────────────────────
echo [3/3] Launching Ngrok Tunnel...
echo.

echo  ================================================
echo   Your PUBLIC link will appear in the Ngrok window!
echo   Look for the line that says "Forwarding".
echo   Share that link with anyone to access SkillLoop.      
echo  ================================================
echo.
start "SkillLoop - Ngrok Public URL" cmd /k "title SkillLoop - Public URL && npx ngrok http 3000"

echo.
echo  All 3 services are now running!
echo  Check the "SkillLoop - Ngrok Public URL" window for your live link.
echo.
pause
