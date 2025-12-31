# ✅ Setup Verification Guide

Use this guide to verify your setup is correct before running the application.

## Backend Check

### Automated Check

Run this script to verify everything:

```bash
cd backend
python test_setup.py
```

This will check:
- ✅ Python version (3.11+)
- ✅ .env file exists
- ✅ OpenAI API key is set
- ✅ All dependencies installed
- ✅ Required directories exist

### Manual Check

#### 1. Check Python Version

```bash
python --version
# or
python3 --version
```

**Expected**: `Python 3.11.0` or higher

#### 2. Check Virtual Environment

```bash
cd backend

# Check if venv exists
ls venv/          # Mac/Linux
dir venv\         # Windows
```

**Expected**: Should see `bin/` or `Scripts/` directory

#### 3. Check Dependencies

```bash
# Activate venv first!
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# Check if packages installed
pip list | grep fastapi
pip list | grep openai
```

**Expected**: Should see fastapi and openai packages

#### 4. Check .env File

```bash
cd backend
cat .env          # Mac/Linux
type .env         # Windows
```

**Expected**: Should see `OPENAI_API_KEY=sk-...`

#### 5. Check Directories

```bash
cd backend
ls -la            # Mac/Linux
dir               # Windows
```

**Expected**: Should see `uploads/` and `exports/` directories

## Frontend Check

### Check Node.js Version

```bash
node --version
```

**Expected**: `v18.0.0` or higher

### Check npm Version

```bash
npm --version
```

**Expected**: `9.0.0` or higher

### Check Dependencies

```bash
cd frontend

# Check if node_modules exists
ls node_modules/  # Mac/Linux
dir node_modules\ # Windows
```

**Expected**: Should see many package directories

### Check Package Installation

```bash
cd frontend
npm list react
npm list vite
```

**Expected**: Should show installed versions

## Quick Test Commands

### Test Backend

```bash
# In backend directory with venv activated
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"
python -c "import openai; print('OpenAI:', openai.__version__)"
python -c "from app.core.config import settings; print('Config loaded!')"
```

**Expected**: Should print versions without errors

### Test Frontend

```bash
# In frontend directory
npm run build -- --dry-run
```

**Expected**: Should complete without errors

## Port Check

### Check if Ports are Free

**Check port 8000 (backend):**

```bash
# Mac/Linux
lsof -i :8000

# Windows
netstat -ano | findstr :8000
```

**Expected**: No output (port is free)

**Check port 3000 (frontend):**

```bash
# Mac/Linux
lsof -i :3000

# Windows
netstat -ano | findstr :3000
```

**Expected**: No output (port is free)

## OpenAI API Check

### Test API Key

```bash
# In backend directory with venv activated
python -c "
from app.core.config import settings
from openai import OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)
print('API Key configured!')
print('Key starts with:', settings.OPENAI_API_KEY[:10])
"
```

**Expected**: Should print "API Key configured!" and show `sk-proj-...`

### Test API Connection (Optional)

```bash
python -c "
from openai import OpenAI
from app.core.config import settings
client = OpenAI(api_key=settings.OPENAI_API_KEY)
response = client.models.list()
print('✅ API connection successful!')
print('Available models:', [m.id for m in response.data[:3]])
"
```

**Expected**: Should list available models

## Browser Check

### Supported Browsers

Test your browser version:

**Chrome/Edge:**
1. Go to `chrome://settings/help` or `edge://settings/help`
2. Should be version 90+

**Firefox:**
1. Go to `about:support`
2. Should be version 88+

**Safari:**
1. Safari → About Safari
2. Should be version 14+

### Test Localhost Access

1. Open browser
2. Try accessing: http://localhost:8000
3. Should see "Cannot GET /" or connection refused (backend not running yet)
4. Try accessing: http://localhost:3000
5. Should see connection refused (frontend not running yet)

## Complete Setup Checklist

Print this and check off each item:

### Prerequisites
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] OpenAI API key obtained
- [ ] Git installed (if cloning repo)

### Backend Setup
- [ ] Virtual environment created (`venv/` exists)
- [ ] Virtual environment activated (see `(venv)` in prompt)
- [ ] Dependencies installed (`pip install -r requirements.txt` completed)
- [ ] `.env` file created
- [ ] OpenAI API key added to `.env`
- [ ] `uploads/` directory exists
- [ ] `exports/` directory exists
- [ ] Test script passes (`python test_setup.py`)

### Frontend Setup
- [ ] Dependencies installed (`npm install` completed)
- [ ] `node_modules/` directory exists
- [ ] No errors in npm install output
- [ ] `.env` file created (if needed)

### Network
- [ ] Port 8000 is free (for backend)
- [ ] Port 3000 is free (for frontend)
- [ ] Internet connection active
- [ ] No firewall blocking localhost

### Testing
- [ ] Backend test script passes
- [ ] Can import Python packages
- [ ] OpenAI API key is valid
- [ ] Browser supports required features

## Troubleshooting Failed Checks

### Python Version Too Old

**Problem**: Python 3.10 or older

**Solution**:
1. Download Python 3.11+ from https://www.python.org/downloads/
2. Install it
3. Use `python3.11` command instead of `python`
4. Recreate virtual environment: `python3.11 -m venv venv`

### Dependencies Not Installing

**Problem**: `pip install` fails

**Solution**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Try installing packages individually
pip install fastapi
pip install uvicorn
pip install openai

# If SSL errors
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### .env File Issues

**Problem**: `.env` not recognized

**Solution**:
1. Make sure file is named exactly `.env` (with the dot)
2. Make sure it's in `backend/` directory
3. On Windows, save as "All Files" type, not ".env.txt"

### OpenAI API Key Invalid

**Problem**: API calls fail with authentication error

**Solution**:
1. Go to https://platform.openai.com/api-keys
2. Create a new key
3. Copy the entire key (starts with `sk-`)
4. Replace in `.env` file
5. Make sure no spaces around the `=` sign
6. Make sure no quotes around the key

### Port Already in Use

**Problem**: Backend or frontend port is occupied

**Solution**:

**Find and kill process (Mac/Linux):**
```bash
# Find process
lsof -ti :8000

# Kill it
kill -9 [PID]
```

**Find and kill process (Windows):**
```bash
# Find process
netstat -ano | findstr :8000

# Kill it (replace PID)
taskkill /PID [number] /F
```

### npm Install Fails

**Problem**: Frontend dependencies won't install

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete existing files
rm -rf node_modules package-lock.json

# Try again
npm install

# If still fails, try older node version
nvm install 18
nvm use 18
npm install
```

## Final Verification

Before starting the servers, verify:

```bash
# Backend
cd backend
source venv/bin/activate
python test_setup.py
# Should pass all checks

# Frontend  
cd frontend
npm list
# Should show dependency tree without errors
```

If all checks pass, you're ready to start!

**Next step**: Read `START_HERE.md` or `LOCALHOST_DEPLOYMENT.md`

## Success Indicators

### When Backend Starts Successfully

```
🚀 Starting AI Meeting Minutes System...
✅ Database initialized
✅ Directories created
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### When Frontend Starts Successfully

```
VITE v5.0.11  ready in 500 ms

➜  Local:   http://localhost:3000/
➜  Network: http://192.168.1.x:3000/
```

### When You Access http://localhost:3000

You should see:
- Purple gradient background
- "AI Meeting Summarizer" header
- Upload/Record buttons OR transcript input
- No error messages in browser console (F12)

## Still Having Issues?

1. Read `LOCALHOST_DEPLOYMENT.md` for detailed troubleshooting
2. Check backend terminal for error messages
3. Check browser console (F12) for frontend errors
4. Verify OpenAI API status: https://status.openai.com/
5. Make sure you have internet connection

---

**Once all checks pass, proceed to**: `START_HERE.md`
