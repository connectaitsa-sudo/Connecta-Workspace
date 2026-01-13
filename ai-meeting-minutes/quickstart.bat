@echo off
REM AI Meeting Minutes System - Quick Start Script (Windows)
REM This script helps you quickly set up and run the system

echo ========================================================
echo   AI Meeting Minutes System - Quick Start
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is not installed!
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Python and Node.js detected
echo.

REM Backend Setup
echo [INFO] Setting up backend...
cd backend

REM Check if .env exists
if not exist .env (
    echo [WARNING] No .env file found. Creating from template...
    copy .env.example .env
    echo.
    echo [IMPORTANT] You need to add your OpenAI API key to backend\.env
    echo             Open backend\.env and set: OPENAI_API_KEY=sk-your-key-here
    echo.
    pause
)

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -q -r requirements.txt

REM Create directories
if not exist uploads mkdir uploads
if not exist exports mkdir exports

echo [OK] Backend setup complete
echo.

REM Frontend Setup
echo [INFO] Setting up frontend...
cd ..\frontend

if not exist node_modules (
    echo Installing Node.js dependencies...
    call npm install
)

echo [OK] Frontend setup complete
echo.

REM Done
echo ========================================================
echo   Setup Complete!
echo ========================================================
echo.
echo To start the system, run these commands in separate terminals:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   python run.py
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:3000
echo.
pause
