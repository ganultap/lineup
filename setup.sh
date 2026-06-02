#!/bin/bash

# RNB Auto Lineup Maker - Quick Setup Script

echo "🎵 Setting up Rhythm N Boost - Auto Lineup Maker 🎵"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser
echo ""
echo "👤 Create a superuser account for the admin panel (optional)"
read -p "Create superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

echo ""
echo "✨ Setup complete! To start the server, run:"
echo ""
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "Then visit:"
echo "   🎤 Participant: http://localhost:8000"
echo "   🎛️  Host Panel:  http://localhost:8000/host/"
echo "   👨‍💼 Admin:       http://localhost:8000/admin/"
echo ""
