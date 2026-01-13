#!/bin/bash
# Quick setup script after cloning from GitHub

echo "================================================"
echo "  AI Meeting Minutes - Local Setup"
echo "================================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install from https://www.python.org/"
    exit 1
fi
echo "✅ Python found"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Install from https://nodejs.org/"
    exit 1
fi
echo "✅ Node.js found"

echo ""
echo "Setting up backend..."
cd backend

# Create venv
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -q -r requirements.txt

# Create .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your OpenAI API key!"
fi

echo "✅ Backend setup complete!"

echo ""
echo "Setting up frontend..."
cd ../frontend

# Install packages
npm install

echo "✅ Frontend setup complete!"

echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
