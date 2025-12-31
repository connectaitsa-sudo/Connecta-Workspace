# 🚀 START HERE - Quick Setup

Welcome to the AI Meeting Minutes System! Follow these steps to get started.

## ⚡ Quick Start (Choose One)

### Option 1: Automatic Setup (Easiest) ⭐

**Windows:**
```bash
quickstart.bat
```

**Mac/Linux:**
```bash
chmod +x quickstart.sh
./quickstart.sh
```

Then follow the prompts!

---

### Option 2: Manual Setup (Step-by-Step)

## Step 1: Get OpenAI API Key 🔑

1. Go to https://platform.openai.com/signup
2. Create account
3. Visit https://platform.openai.com/api-keys
4. Create new key
5. Copy it (starts with `sk-`)

## Step 2: Setup Backend 🔧

Open Terminal/Command Prompt:

```bash
# Navigate to backend
cd ai-meeting-minutes/backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Create config
cp .env.example .env

# Edit .env file and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here

# Start backend
python run.py
```

**Keep this terminal open!**

## Step 3: Setup Frontend 🎨

Open **NEW** Terminal:

```bash
# Navigate to frontend
cd ai-meeting-minutes/frontend

# Install packages
npm install

# Start frontend
npm run dev
```

**Keep this terminal open too!**

## Step 4: Open Application 🌐

Go to: **http://localhost:3000**

## Step 5: Test It! 🧪

1. Click "Transcript Text" tab
2. Click "Load Sample Transcript"
3. Click "Generate Meeting Minutes"
4. Wait 10 seconds
5. See the magic! ✨

---

## 📚 Need More Help?

- **Complete Guide**: Read `LOCALHOST_DEPLOYMENT.md`
- **Troubleshooting**: Check troubleshooting section in `LOCALHOST_DEPLOYMENT.md`
- **Features**: Read `FEATURES.md`
- **API Docs**: http://localhost:8000/docs

---

## 🎯 What You'll See

### Backend Terminal (Terminal 1)
```
🚀 Starting AI Meeting Minutes System...
✅ Database initialized
✅ Directories created
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Frontend Terminal (Terminal 2)
```
VITE v5.0.11  ready in 500 ms
➜  Local:   http://localhost:3000/
```

### Browser (http://localhost:3000)
- Purple gradient background
- "AI Meeting Summarizer" title
- Upload area or transcript input
- Generate button

---

## ⚠️ Common Issues

### "Python not found"
```bash
Try: python3 --version
```

### "npm not found"
Install Node.js from https://nodejs.org/

### "Port already in use"
Another app is using the port. Stop it or use different port.

### Backend errors
Check if OPENAI_API_KEY is set in `backend/.env`

### "Network Error" in browser
Check if backend is running (http://localhost:8000)

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] Python 3.11+ (`python --version`)
- [ ] Node.js 18+ (`node --version`)
- [ ] OpenAI API key (from https://platform.openai.com/api-keys)
- [ ] Internet connection
- [ ] About 10 minutes

---

## 💰 Costs

OpenAI API charges:
- ~$0.006 per minute of audio transcription
- ~$0.01-0.03 per meeting analysis
- **Example**: 1-hour meeting ≈ $0.40

---

## 🎉 You're Ready!

Follow the steps above and you'll have your AI Meeting Minutes System running in 10 minutes!

For detailed instructions, see: **LOCALHOST_DEPLOYMENT.md**

**Happy Meeting! 🎙️**
