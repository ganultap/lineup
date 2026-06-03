@echo off
REM RNB Auto Lineup Maker - Quick Setup Script for Windows

echo 🎵 Setting up Rhythm N Boost - Auto Lineup Maker 🎵
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3 is required but not installed. Please install Python 3.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo 🗄️  Running database migrations...
python manage.py migrate

REM Collect static files
echo 🎨 Collecting static files...
python manage.py collectstatic --noinput

REM Create superuser
echo.
set /p create_super="👤 Create superuser account? (y/n): "
if /i "%create_super%"=="y" (
    python manage.py createsuperuser
)

echo.
echo ✨ Setup complete! To start the server, run:
echo.
echo    venv\Scripts\activate.bat
echo    python manage.py runserver
echo.
echo Then visit:
echo    🎤 Participant: http://localhost:8000
echo    🎛️  Host Panel:  http://localhost:8000/host/
echo    👨‍💼 Admin:       http://localhost:8000/admin/
echo.
pause
