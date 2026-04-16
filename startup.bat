@echo off
REM SANKALP - Campus Management System - Windows Startup Script

echo.
echo ========================================
echo     SANKALP - Campus Management System
echo ========================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

REM Navigate to project
cd sankalp

REM Apply migrations
echo Applying migrations...
python manage.py migrate --noinput

REM Display options
echo.
echo ========================================
echo What would you like to do?
echo ========================================
echo 1. Run Development Server
echo 2. Create Superuser (Admin)
echo 3. Run Tests
echo 4. Collect Static Files
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting development server...
    echo Access the application at: http://127.0.0.1:8000/
    echo Press CTRL+C to stop the server
    echo.
    python manage.py runserver
)
if "%choice%"=="2" (
    echo.
    echo Create Superuser (Admin)
    python manage.py createsuperuser
    pause
)
if "%choice%"=="3" (
    echo.
    echo Running tests...
    python manage.py test
    pause
)
if "%choice%"=="4" (
    echo.
    echo Collecting static files...
    python manage.py collectstatic --noinput
    echo Done!
    pause
)
if "%choice%"=="5" (
    echo Goodbye!
    exit /b 0
)

pause
