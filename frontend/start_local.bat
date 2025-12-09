@echo off
echo Starting Crypto Dashboard Frontend...
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

REM Check if .env exists
if not exist ".env" (
    echo.
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo Please edit .env and set REACT_APP_API_URL if needed
    echo.
)

REM Start the React app
echo.
echo Starting React app on http://localhost:3000
echo Press Ctrl+C to stop
echo.
call npm start

