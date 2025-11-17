@echo off
echo.
echo ========================================
echo Music Translator - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in your PATH!
    echo.
    echo Please download Python from: https://www.python.org/downloads/
    echo Make sure to CHECK "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo [✓] Python found
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed!
    echo.
    echo Please download Node.js from: https://nodejs.org/
    echo Install the LTS version.
    echo.
    pause
    exit /b 1
)

echo [✓] Node.js found
echo.

REM Check if .env file exists in backend
if not exist "backend\.env" (
    echo [WARNING] backend\.env file not found!
    echo.
    echo Please do this:
    echo 1. Go to the backend folder
    echo 2. Copy .env.example to .env
    echo 3. Edit .env and add your API keys (or leave empty for demo)
    echo.
    echo Without .env, the app will show the UI but searches won't work.
    echo.
    pause
    exit /b 1
)

echo [✓] .env file found
echo.
echo Starting setup...
echo.

cd backend
echo [1/4] Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)

echo [3/4] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    echo This might be a network issue. Try running again.
    pause
    exit /b 1
)

echo [4/4] Starting backend server...
echo.
echo ========================================
echo Backend starting on http://localhost:8000
echo ========================================
echo Keep this window open!
echo.
echo Opening frontend in a new window...
echo.

REM Open a new window for the frontend
start cmd /k "cd ..\frontend && npm install && npm start"

REM Start backend in this window
python main.py

pause