#!/bin/bash

# AI Meeting Minutes System - Quick Start Script
# This script helps you quickly set up and run the system

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  🎙️  AI Meeting Minutes System - Quick Start           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo "Please install Python 3.11+ from https://www.python.org/downloads/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed!${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}✅ Python and Node.js detected${NC}"
echo ""

# Backend Setup
echo -e "${BLUE}📦 Setting up backend...${NC}"
cd backend

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from template...${NC}"
    cp .env.example .env
    echo ""
    echo -e "${YELLOW}⚠️  IMPORTANT: You need to add your OpenAI API key to backend/.env${NC}"
    echo -e "   Open backend/.env and set: OPENAI_API_KEY=sk-your-key-here"
    echo ""
    read -p "Press Enter after you've added your API key..."
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Create directories
mkdir -p uploads exports

echo -e "${GREEN}✅ Backend setup complete${NC}"
echo ""

# Frontend Setup
echo -e "${BLUE}📦 Setting up frontend...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

echo -e "${GREEN}✅ Frontend setup complete${NC}"
echo ""

# Done
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Setup Complete!                                     ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "To start the system, run these commands in separate terminals:"
echo ""
echo -e "${YELLOW}Terminal 1 (Backend):${NC}"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo -e "${YELLOW}Terminal 2 (Frontend):${NC}"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
