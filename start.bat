@echo off
chcp 65001 >nul
title ☀️ SunCloud Hosting Launcher
color 0D

echo.
echo ========================================
echo       ☀️  SunCloud Hosting Launcher ☀️
echo ========================================
echo.
echo Welcome to the futuristic hosting system startup!
echo Powered by Node.js, Python, and MongoDB
echo ----------------------------------------
echo.

REM ==================== CHECKS ====================

where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [❌] Node.js not found!
    echo Install from: https://nodejs.org/
    pause
    exit /b
)
echo [✅] Node.js detected

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [❌] Python not found!
    echo Install from: https://python.org/
    pause
    exit /b
)
echo [✅] Python detected

REM ==================== MONGODB ====================

tasklist /FI "IMAGENAME eq mongod.exe" 2>NUL | find /I /N "mongod.exe">NUL
if %ERRORLEVEL% NEQ 0 (
    echo [⚠️] MongoDB not running!
    echo Trying to start MongoDB...
    net start MongoDB >nul 2>nul
    timeout /t 2 >nul
)
tasklist /FI "IMAGENAME eq mongod.exe" 2>NUL | find /I /N "mongod.exe">NUL
if %ERRORLEVEL% NEQ 0 (
    echo [⚠️] Failed to start MongoDB automatically.
    echo Please start manually using:
    echo     net start MongoDB
) else (
    echo [✅] MongoDB is running!
)

echo.
echo [🚀] Launching backend...
start "Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn server:app --reload --host 0.0.0.0 --port 8001"

echo.
echo [🚀] Launching frontend...
start "Frontend" cmd /k "cd frontend && yarn start"

echo.
echo ========================================
echo  ☀️ SunCloud is now running!
echo  🌐 Frontend: http://localhost:3000
echo  ⚙️ Backend:  http://localhost:8001
echo ========================================
echo.
echo WebSite created by evgen4ik ☀️
echo.
pause