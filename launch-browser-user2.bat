@echo off
title SkillLoop - Browser for USER 2 (Krishna / Second Account)
echo.
echo ==========================================================
echo     SkillLoop WebRTC Testing - USER 2 Browser
echo ==========================================================
echo.
echo  This browser = SECOND account (Krishna / mittalserenity)
echo  Target: http://192.168.1.7:3000
echo.
echo  NOTE: This has a SEPARATE session from User 1 browser.
echo  Both can be open at the same time on the same machine.
echo.

set "TARGET_URL=http://192.168.1.7:3000"
set "SECURE_FLAG=--unsafely-treat-insecure-origin-as-secure=http://192.168.1.7:3000,http://192.168.1.7:5000"
set "USER_DIR=%LOCALAPPDATA%\SkillLoop\WebRTCProfile_User2"

:: Check for Brave Browser
if exist "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" (
    echo [OK] Launching Brave Browser - User 2 Session...
    start "" "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

:: Check for Google Chrome
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo [OK] Launching Chrome - User 2 Session...
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo [OK] Launching Chrome - User 2 Session...
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

:: Check for Microsoft Edge
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    echo [OK] Launching Edge - User 2 Session...
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"
    goto done
)

echo [WARN] Could not find browser. Trying msedge...
start "" msedge %SECURE_FLAG% --user-data-dir="%USER_DIR%" "%TARGET_URL%"

:done
echo.
echo Browser opened! Log in as SECOND account here (e.g. @mittalserenity).
echo Camera and microphone are unblocked for this session.
echo ==========================================================
timeout /t 3 >nul
