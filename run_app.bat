@echo off
REM ====================================================
REM Wheat Disease Detection - Flask Application Launcher
REM ====================================================

echo.
echo ======================================================================
echo         WHEAT DISEASE DETECTION - FLASK SERVER LAUNCHER
echo ======================================================================
echo.

REM Check if virtual environment exists
if not exist ".venv1" (
    echo [ERROR] Virtual environment not found at .venv1
    echo.
    echo Please create it first:
    echo   python -m venv .venv1
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv1\Scripts\activate.bat

if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment activated
echo [OK] Using Python: %VIRTUAL_ENV%
echo.

REM Run the Flask application
echo ======================================================================
echo                         STARTING FLASK SERVER
echo ======================================================================
echo.
echo Server will be available at: http://localhost:5000
echo Press CTRL+C to stop the server
echo.

python app.py

pause
