@echo off
title Domain Intelligence Agent

echo =====================================================
echo   Domain Intelligence Agent - Startup
echo =====================================================
if exist "%~dp0screenshot-service" (
    echo [1/2] Starting Node.js Puppeteer Browser/Render Service on port 3000...
    start "Screenshot & Render Service" /min cmd /c "cd /d "%~dp0screenshot-service" && node server.js"
    timeout /t 2 /nobreak >nul
)

echo [2/2] Starting Streamlit Domain Intelligence Agent...
echo.

if exist "D:\Python313\python.exe" (
    "D:\Python313\python.exe" -m streamlit run app.py
) else (
    py -3.13 -m streamlit run app.py
)

pause

