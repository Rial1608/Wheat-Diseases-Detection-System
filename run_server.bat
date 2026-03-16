@echo off
REM This batch file starts the Wheat Disease Detection Flask application

echo.
echo ======================================================================
echo           WHEAT DISEASE DETECTION - FLASK SERVER LAUNCHER
echo ======================================================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo [ERROR] Virtual environment not found at .venv
    echo.
    echo Please create a virtual environment first:
    echo   python -m venv .venv
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment activated
echo.

REM Check for TensorFlow issues
echo Running environment check...
python fix_tensorflow.py

echo.
echo ======================================================================
echo                         STARTING FLASK SERVER
echo ======================================================================
echo.
echo Server will be available at: http://localhost:5000
echo Press CTRL+C to stop the server
echo.

REM Start Flask app
python app.py

pause
