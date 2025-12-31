# 🏃 Run Locally - Quick Guide

Simple steps to run the AI Meeting Minutes System on your local machine.

---

## Prerequisites

Before you start, make sure you have:

✅ **Python 3.11+** installed  
Check: `python --version` or `python3 --version`  
Download: https://www.python.org/downloads/

✅ **Node.js 18+** installed  
Check: `node --version`  
Download: https://nodejs.org/

✅ **Git** installed  
Check: `git --version`  
Download: https://git-scm.com/

✅ **OpenAI API Key**  
Get it from: https://platform.openai.com/api-keys

---

## Step-by-Step Instructions

### 1️⃣ Clone from GitHub

```bash
# Clone the repository
git clone <your-repository-url>

# Navigate to project folder
cd ai-meeting-minutes
```

### 2️⃣ Backend Setup

```bash
# Go to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# You should see (venv) in your terminal now

# Install dependencies
pip install -r requirements.txt

# Create .env file
# On Windows:
copy .env.example .env

# On Mac/Linux:
cp .env.example .env

# Edit .env file and add your OpenAI API key
# Open .env in any text editor and set:
# OPENAI_API_KEY=sk-your-actual-key-here

# Start backend server
python run.py
```

**Backend is now running!** 🎉  
Keep this terminal open.

You should see:
```
🚀 Starting AI Meeting Minutes System...
✅ Database initialized
✅ Directories created
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3️⃣ Frontend Setup

**Open a NEW terminal window** (keep backend running!)

```bash
# Navigate to frontend folder
cd ai-meeting-minutes/frontend

# Install dependencies
npm install

# Start frontend server
npm run dev
```

**Frontend is now running!** 🎉  
Keep this terminal open too.

You should see:
```
VITE v5.0.11  ready in 500 ms
➜  Local:   http://localhost:3000/
```

### 4️⃣ Open in Browser

Go to: **http://localhost:3000**

---

## Quick Test

1. Click **"Transcript Text"** tab
2. Click **"Load Sample Transcript"**
3. Click **"Generate Meeting Minutes"**
4. Wait 10 seconds
5. See the results! ✨

---

## Folder Structure After Clone

```
ai-meeting-minutes/
├── backend/              # Python FastAPI
│   ├── app/
│   ├── .env.example     # Copy this to .env
│   ├── requirements.txt
│   └── run.py
├── frontend/            # React app
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

---

## Common Issues & Solutions

### ❌ "python: command not found"

**Solution:** Try `python3` instead:
```bash
python3 -m venv venv
python3 run.py
```

### ❌ "npm: command not found"

**Solution:** Node.js not installed  
Download from: https://nodejs.org/

### ❌ "Port 8000 already in use"

**Solution:** Another app is using port 8000

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <number> /F
```

**Mac/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

### ❌ "Port 3000 already in use"

**Solution:** Use a different port
```bash
npm run dev -- --port 3001
```

### ❌ Backend starts but shows errors

**Solution:** Check .env file
```bash
# Make sure OPENAI_API_KEY is set correctly
cat .env              # Mac/Linux
type .env             # Windows
```

### ❌ "Network Error" in browser

**Solutions:**
1. Check backend is running (http://localhost:8000)
2. Check console for errors (F12 in browser)
3. Restart both backend and frontend

### ❌ "ModuleNotFoundError" in Python

**Solution:**
```bash
# Make sure venv is activated (should see (venv) in terminal)
# Then reinstall:
pip install -r requirements.txt
```

### ❌ npm install fails

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

---

## Getting OpenAI API Key

1. Go to https://platform.openai.com/signup
2. Create account or sign in
3. Go to https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Paste in `backend/.env` file:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

**Cost:** About $0.40 per 1-hour meeting

---

## Stopping the Application

1. In Backend terminal: Press `Ctrl + C`
2. In Frontend terminal: Press `Ctrl + C`
3. Close terminal windows

---

## Starting Again Later

**Backend:**
```bash
cd backend
source venv/bin/activate    # Mac/Linux
# or
venv\Scripts\activate       # Windows
python run.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

---

## Next Steps

- ✅ Test with your own audio files
- ✅ Try recording feature
- ✅ Export to PDF/DOCX
- ✅ Explore all features

---

## Need Help?

- Check `LOCALHOST_DEPLOYMENT.md` for detailed guide
- Check `CHECK_SETUP.md` to verify setup
- Run `python backend/test_setup.py` to check configuration

---

## URLs to Remember

- **Main App**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

**Enjoy your AI Meeting Minutes System! 🎉**
