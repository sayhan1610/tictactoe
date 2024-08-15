@echo off
echo Checking for Python...
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python 3.11.6 or later.
    exit /b
)

echo Checking for pip...
pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo pip is not installed. Please install pip.
    exit /b
)

echo Installing dependencies...
pip install -r requirements.txt

echo Starting 2048 Game...
python main.py
pause
