@echo off
title SkillLoop - Browser for USER 1 (Emma / Your Account)
echo.
echo ==========================================================
echo     SkillLoop WebRTC Testing - USER 1 Browser
echo ==========================================================
echo.
echo  This browser = YOUR account (Emma / prathammitttal / etc)
echo  Target: http://192.168.1.7:3000
echo.
echo  NOTE: This browser has its OWN separate session.
echo  Use launch-browser-user2.bat for a second account
echo  on the SAME machine.
echo.

set "TARGET_URL=http://192.168.1.7:3000"
set "SECURE_FLAG=--unsafely-treat-insecure-origin-as-secure=http://192.168.1.7:3000,http://192.168.1.7:5000"
set "USER_DIR=%LOCALAPPDATA%\SkillLoop\WebRTCProfile_User1"

:: Check for Brave Browser
if exist "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" (
    echo [OK] Launching Brave Browser - User 1 Session...
    start "" "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

:: Check for Google Chrome
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo [OK] Launching Chrome - User 1 Session...
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo [OK] Launching Chrome - User 1 Session...
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

:: Check for Microsoft Edge
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    echo [OK] Launching Edge - User 1 Session...
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

echo [WARN] Could not find browser. Trying msedge...
start "" msedge %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"

:done
echo.
echo Browser opened! Log in as YOUR account here.
echo Camera and microphone are unblocked for this session.
echo ==========================================================
timeout /t 3 >nul
