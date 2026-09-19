@echo off
title Domain Intelligence Agent

echo =====================================================
echo   Domain Intelligence Agent - Startup
echo =====================================================
echo.
echo Starting Streamlit Domain Intelligence Agent...
echo.

if exist "D:\Python313\python.exe" (
    "D:\Python313\python.exe" -m streamlit run app.py
) else (
    py -3.13 -m streamlit run app.py
)

pause

