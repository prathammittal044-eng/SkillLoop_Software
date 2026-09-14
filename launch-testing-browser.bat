@echo off
title SkillLoop WebRTC Testing Browser Launcher
echo.
echo ==========================================================
echo       SkillLoop WebRTC Video Testing Launcher
echo ==========================================================
echo.
echo Opening browser with camera and mic enabled for local IP testing...
echo Target: http://192.168.1.7:3000
echo.

set "TARGET_URL=http://192.168.1.7:3000"
set "SECURE_FLAG=--unsafely-treat-insecure-origin-as-secure=http://192.168.1.7:3000,http://192.168.1.7:5000"
set "USER_DIR=%TEMP%\skillloop_webrtc_profile"

:: Check for Brave Browser
if exist "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" (
    echo [OK] Launching Brave Browser with camera and mic enabled...
    start "" "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

:: Check for Google Chrome
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo [OK] Launching Google Chrome with camera and mic enabled...
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo [OK] Launching Google Chrome with camera and mic enabled...
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

:: Check for Microsoft Edge
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    echo [OK] Launching Microsoft Edge with camera and mic enabled...
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

:: Fallback
echo [OK] Launching default browser...
start "" msedge %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"

:done
echo.
echo Browser opened! Camera, microphone and video calling are now 100%% unblocked.
echo ==========================================================
timeout /t 3 >nul
