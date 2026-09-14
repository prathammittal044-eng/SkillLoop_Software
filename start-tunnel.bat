@echo off
title SkillLoop Public HTTPS Tunnel
echo.
echo ==========================================================
echo        SkillLoop - Cloudflare Public HTTPS Tunnel
echo ==========================================================
echo.
echo Starting secure tunnel for port 3000...
echo.
.\cloudflared.exe tunnel --url http://localhost:3000
