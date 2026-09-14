@echo off
title SkillLoop - Teammate / Friend Browser Launcher
echo.
echo ==========================================================
echo        SkillLoop - Teammate / Friend Launcher
echo ==========================================================
echo.
echo Connecting to host at: http://192.168.1.7:3000
echo Enabling camera and mic permissions automatically...
echo.

set "TARGET_URL=http://192.168.1.7:3000"
set "SECURE_FLAG=--unsafely-treat-insecure-origin-as-secure=http://192.168.1.7:3000,http://192.168.1.7:5000"
set "USER_DIR=%LOCALAPPDATA%\SkillLoop\FriendWebRTCProfile"

:: Check for Brave Browser
if exist "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" (
    echo [OK] Found Brave Browser! Launching...
    start "" "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

:: Check for Google Chrome
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo [OK] Found Google Chrome! Launching...
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo [OK] Found Google Chrome (x86)! Launching...
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

:: Check for Microsoft Edge
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    echo [OK] Found Microsoft Edge! Launching...
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

echo [OK] Launching default browser...
start "" msedge %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"

:done
echo.
echo Done! Browser opened. Camera and mic are unblocked.
echo ==========================================================
timeout /t 3 >nul
