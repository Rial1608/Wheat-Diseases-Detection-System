@echo off
REM Wheat Disease Detection Web Application - Windows Startup Script

echo.
echo ======================================================
echo   WHEAT DISEASE DETECTION SYSTEM
echo   Starting Flask Server...
echo ======================================================
echo.

REM Check if venv is activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import flask, tensorflow, numpy, cv2" 2>nul
if errorlevel 1 (
    echo Installing missing packages...
    pip install -r requirements.txt
)

echo.
echo Starting Flask application...
echo.
echo Server running at: http://localhost:5000
echo Press CTRL+C to stop the server.
echo.

python app.py
