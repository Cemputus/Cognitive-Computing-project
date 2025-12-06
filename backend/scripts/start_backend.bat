@echo off
REM Batch script to start the backend server with virtual environment
echo Starting CENAnalytics Backend Server...
echo.

REM Get the script directory (backend/scripts/)
cd /d "%~dp0"
REM Get backend directory (parent of scripts)
cd ..
set "BACKEND_DIR=%CD%"

REM Check if venv exists
set "VENV_PATH=%BACKEND_DIR%\venv"
if not exist "%VENV_PATH%" (
    echo Warning: Virtual environment not found at: %VENV_PATH%
    echo Creating virtual environment...
    python -m venv venv
    
    echo Installing dependencies...
    call "%VENV_PATH%\Scripts\activate.bat"
    pip install -r requirements.txt
    
    echo Downloading NLTK data...
    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon'); nltk.download('wordnet')"
)

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"

echo.
echo Backend will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Start the backend server
python backend_api.py

pause

REM Check if venv exists
set "VENV_PATH=%BACKEND_DIR%\venv"
if not exist "%VENV_PATH%" (
    echo Warning: Virtual environment not found at: %VENV_PATH%
    echo Creating virtual environment...
    python -m venv venv
    
    echo Installing dependencies...
    call "%VENV_PATH%\Scripts\activate.bat"
    pip install -r requirements.txt
    
    echo Downloading NLTK data...
    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon'); nltk.download('wordnet')"
)

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"

echo.
echo Backend will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Start the backend server
python backend_api.py

pause
