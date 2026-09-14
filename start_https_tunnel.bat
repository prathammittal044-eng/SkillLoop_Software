@echo off
echo ==========================================
echo    SkillLoop HTTPS Tunnel Launcher
echo ==========================================
echo.
echo This script will download and run Cloudflare's cloudflared to create
echo a temporary HTTPS tunnel to your Nuxt dev server.
echo.
echo REQUIREMENTS:
echo - Your Nuxt app should be running on port 3000
echo - Your Flask backend should be running on port 5000
echo.

if not exist "cloudflared.exe" (
    echo Downloading cloudflared...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'cloudflared.exe'"
    if %ERRORLEVEL% neq 0 (
        echo Failed to download cloudflared.
        pause
        exit /b 1
    )
)

echo.
echo Launching tunnel to localhost:3000...
echo.
echo !!! IMPORTANT !!!
echo Wait for the link that looks like:
echo https://some-random-words.trycloudflare.com
echo.
echo Share that link with your friends to test WebRTC Video Calling!
echo.

cloudflared.exe tunnel --url http://localhost:3000
pause
