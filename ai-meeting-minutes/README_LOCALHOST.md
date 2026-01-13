# 🏠 Complete Localhost Setup & Deployment

## 📖 Table of Contents

1. [Quick Overview](#quick-overview)
2. [What You'll Get](#what-youll-get)
3. [System Requirements](#system-requirements)
4. [Installation Steps](#installation-steps)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [Daily Usage](#daily-usage)

---

## Quick Overview

This AI Meeting Minutes System runs entirely on your local computer (localhost). It will:
- ✅ Transcribe audio/video files or live recordings
- ✅ Generate professional meeting minutes using AI
- ✅ Export to PDF, Word (DOCX), or Text format
- ✅ Work with Zoom, Teams, or any meeting platform

**Time to setup**: ~10 minutes  
**Cost**: Only OpenAI API usage (~$0.40 per hour of meetings)

---

## What You'll Get

After setup, you'll have:

### Two Running Servers

1. **Backend Server** (http://localhost:8000)
   - Python FastAPI server
   - Handles AI processing
   - Manages database

2. **Frontend Server** (http://localhost:3000)
   - React web interface
   - Beautiful UI
   - Upload/record meetings

### Main Application

Access at: **http://localhost:3000**

**Features:**
- 🎤 Record audio directly in browser
- 📤 Upload audio/video files (MP3, WAV, MP4, etc.)
- 📝 Paste transcript text
- 🤖 AI generates meeting minutes
- 📄 Export to PDF/DOCX/TXT
- 🔄 Real-time processing status

---

## System Requirements

### Must Have

✅ **Python 3.11 or higher**
- Check: `python --version` or `python3 --version`
- Download: https://www.python.org/downloads/

✅ **Node.js 18 or higher**
- Check: `node --version`
- Download: https://nodejs.org/ (get LTS version)

✅ **OpenAI API Key**
- Sign up: https://platform.openai.com/signup
- Get key: https://platform.openai.com/api-keys
- Costs: ~$0.006/minute of audio + ~$0.01-0.03/meeting

✅ **Internet Connection**
- Required for OpenAI API calls

✅ **Modern Web Browser**
- Chrome, Firefox, Safari, or Edge
- Latest version recommended

### Recommended

- 8GB RAM or more
- 5GB free disk space
- Quiet environment for recording
- Good microphone (for recording feature)

---

## Installation Steps

### Quick Method (Automatic) 🚀

**Windows:**
```cmd
cd ai-meeting-minutes
quickstart.bat
```

**Mac/Linux:**
```bash
cd ai-meeting-minutes
chmod +x quickstart.sh
./quickstart.sh
```

Follow the prompts to add your OpenAI API key!

---

### Manual Method (Step-by-Step) 📝

#### Part A: Backend Setup

**Step 1: Open Terminal**
- Windows: Press `Win+R`, type `cmd`, press Enter
- Mac: Press `Cmd+Space`, type `terminal`, press Enter
- Linux: Press `Ctrl+Alt+T`

**Step 2: Navigate to Backend**
```bash
cd ai-meeting-minutes
cd backend
```

**Step 3: Create Virtual Environment**

*Windows:*
```cmd
python -m venv venv
```

*Mac/Linux:*
```bash
python3 -m venv venv
```

**Step 4: Activate Virtual Environment**

*Windows:*
```cmd
venv\Scripts\activate
```

*Mac/Linux:*
```bash
source venv/bin/activate
```

You should see `(venv)` in your prompt.

**Step 5: Install Python Packages**
```bash
pip install -r requirements.txt
```

Wait 2-3 minutes for installation.

**Step 6: Create Configuration File**

*Windows:*
```cmd
copy .env.example .env
```

*Mac/Linux:*
```bash
cp .env.example .env
```

**Step 7: Add OpenAI API Key**

Open `.env` file:
- Windows: `notepad .env`
- Mac: `open -e .env`
- Linux: `nano .env`

Find this line:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

Replace `sk-your-openai-api-key-here` with your actual OpenAI API key.

Save and close.

**Step 8: Verify Setup**
```bash
python test_setup.py
```

All checks should pass!

---

#### Part B: Frontend Setup

**Step 1: Open NEW Terminal** (keep backend terminal open!)

**Step 2: Navigate to Frontend**
```bash
cd ai-meeting-minutes
cd frontend
```

**Step 3: Install Node Packages**
```bash
npm install
```

Wait 2-3 minutes for installation.

---

## Running the Application

### Start Backend (Terminal 1)

```bash
cd ai-meeting-minutes/backend

# Activate venv if not already active
source venv/bin/activate         # Mac/Linux
venv\Scripts\activate            # Windows

# Start server
python run.py
```

**Success looks like:**
```
🚀 Starting AI Meeting Minutes System...
✅ Database initialized
✅ Directories created
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Leave this terminal running!**

### Start Frontend (Terminal 2)

Open NEW terminal:

```bash
cd ai-meeting-minutes/frontend

npm run dev
```

**Success looks like:**
```
VITE v5.0.11  ready in 500 ms

➜  Local:   http://localhost:3000/
➜  Network: http://192.168.1.x:3000/
```

**Leave this terminal running too!**

### Open Application

Go to: **http://localhost:3000**

You should see:
- 🎨 Purple gradient background
- 📋 "AI Meeting Summarizer" header
- 🎙️ Upload/Record interface
- ✨ Beautiful modern UI

**🎉 Success! Your system is running!**

---

## Testing

### Test 1: Sample Transcript (30 seconds) ⭐

1. Click **"Transcript Text"** tab
2. Click **"Load Sample Transcript"** button
3. Click **"Generate Meeting Minutes"** button
4. Wait ~10 seconds
5. See results with:
   - Summary
   - Participants
   - Key points
   - Decisions
   - Action items
   - Next steps
6. Try clicking **"PDF"**, **"DOCX"**, or **"TXT"** to export

### Test 2: Audio Recording (2 minutes)

1. Click **"Audio/Video Upload"** tab
2. Click **"Start Recording"** button
3. Allow microphone when prompted
4. Speak: *"This is [Your Name]. We need to schedule a meeting with the team to discuss Q4 budget. John will prepare the slides by Friday."*
5. Click **"Stop Recording"**
6. Click **"Generate Summary & Minutes"**
7. Wait ~30 seconds
8. View transcribed and analyzed meeting!

### Test 3: File Upload (if you have audio file)

1. Prepare MP3, WAV, or MP4 file
2. Drag and drop into upload area
3. Click **"Generate Summary & Minutes"**
4. Wait for processing
5. View results

---

## Troubleshooting

### Backend Won't Start

**Problem**: "ModuleNotFoundError"
```bash
# Make sure venv is activated (should see (venv) in prompt)
source venv/bin/activate
pip install -r requirements.txt
```

**Problem**: "OpenAI API key not found"
```bash
# Check .env file
cat .env              # Mac/Linux
type .env             # Windows

# Make sure line exists:
# OPENAI_API_KEY=sk-your-actual-key-here
```

**Problem**: "Port 8000 already in use"
```bash
# Kill process using port 8000
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID [number] /F
```

### Frontend Won't Start

**Problem**: "Cannot find module"
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Problem**: "Port 3000 already in use"
```bash
# Use different port
npm run dev -- --port 3001
```

### Application Issues

**Problem**: "Network Error" in browser
- ✅ Check backend is running (Terminal 1)
- ✅ Visit http://localhost:8000 (should see JSON)
- ✅ Check no firewall blocking

**Problem**: Recording not working
- ✅ Check browser permissions (click lock icon in address bar)
- ✅ Allow microphone access
- ✅ Try Chrome/Edge (best compatibility)

**Problem**: Processing stuck
- ✅ Check OpenAI API status: https://status.openai.com/
- ✅ Check API key is valid
- ✅ Check you have credits: https://platform.openai.com/usage
- ✅ Look at backend terminal for errors

### Still Not Working?

Read detailed troubleshooting in:
- `CHECK_SETUP.md` - Verify your setup
- `LOCALHOST_DEPLOYMENT.md` - Complete guide with solutions

---

## Daily Usage

### Starting the System

Every day when you want to use it:

**Terminal 1:**
```bash
cd ai-meeting-minutes/backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python run.py
```

**Terminal 2:**
```bash
cd ai-meeting-minutes/frontend
npm run dev
```

**Browser:**
```
http://localhost:3000
```

### Stopping the System

- Press `Ctrl+C` in each terminal
- Or just close the terminal windows

### Tips for Best Results

**Audio Quality:**
- Use good microphone
- Quiet environment
- Clear speech
- Moderate pace

**Transcript Format:**
```
John: Good morning. Let's discuss the Q4 roadmap.

Sarah: I've prepared the budget. It's $50,000.

John: Great. Sarah, finalize this by Friday.

Sarah: Will do.
```

Include speaker names for best results!

---

## File Locations

**Uploaded Audio:**
```
backend/uploads/
```

**Exported Documents:**
```
backend/exports/
```

**Database:**
```
backend/meeting_minutes.db
```

**To clean up:**
```bash
cd backend
rm -rf uploads/* exports/*     # Mac/Linux
del /q uploads\* exports\*     # Windows
```

---

## Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Main App** | http://localhost:3000 | Web interface |
| **Backend API** | http://localhost:8000 | API server |
| **API Docs** | http://localhost:8000/docs | Interactive API docs |
| **Health Check** | http://localhost:8000/health | Server status |

---

## Costs & Usage

### OpenAI API Pricing

- **Transcription**: $0.006 per minute of audio
- **Analysis**: $0.01-0.03 per meeting
- **Example**: 1-hour meeting ≈ $0.40

### Monthly Estimates

- 10 meetings (30 min each) ≈ $2.00/month
- 50 meetings (30 min each) ≈ $10.00/month
- 100 meetings (1 hour each) ≈ $40.00/month

Check usage: https://platform.openai.com/usage

---

## Security & Privacy

- ✅ All processing on your computer
- ✅ Files stored locally only
- ✅ OpenAI doesn't store your audio/transcripts
- ✅ API key kept in `.env` file (never commit to git)
- ✅ No data sent to third parties

**For Production:**
- Set `DEBUG=False` in `.env`
- Use HTTPS (required for recording)
- Add user authentication
- Use PostgreSQL instead of SQLite
- Set up proper backups

---

## Next Steps

### Learn More
- 📖 Read `FEATURES.md` for all features
- 📖 Read `SETUP_GUIDE.md` for advanced setup
- 🔌 Try Zoom/Teams integration

### Customize
- Change UI colors in `frontend/src/` CSS files
- Modify AI prompts in `backend/app/services/ai_processor.py`
- Add custom export templates

### Deploy to Production
- Use Docker: `docker-compose up`
- Deploy backend to Railway, Render, or AWS
- Deploy frontend to Vercel or Netlify
- See deployment section in `README.md`

---

## Support Resources

- **Setup Verification**: `CHECK_SETUP.md`
- **Complete Guide**: `LOCALHOST_DEPLOYMENT.md`
- **Quick Start**: `START_HERE.md`
- **API Documentation**: http://localhost:8000/docs
- **OpenAI Docs**: https://platform.openai.com/docs

---

## ✅ Success Checklist

Before you start using the system, verify:

- [ ] Python 3.11+ installed and working
- [ ] Node.js 18+ installed and working
- [ ] OpenAI API key obtained and added to `.env`
- [ ] Backend dependencies installed (`pip install`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend test script passes (`python test_setup.py`)
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Can access web interface at localhost:3000
- [ ] Sample transcript test works
- [ ] Can export to PDF/DOCX/TXT

---

## 🎉 You're All Set!

Your AI Meeting Minutes System is now running on localhost!

**What you can do:**
- 🎤 Record meetings in real-time
- 📤 Upload audio/video files
- 📝 Paste meeting transcripts
- 🤖 Get AI-generated professional minutes
- 📄 Export to PDF, Word, or Text
- 🔗 Integrate with Zoom/Teams
- 💼 Use for all your meetings!

**Quick Access:**
- **App**: http://localhost:3000
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

**Need Help?**
- Check troubleshooting section above
- Read `LOCALHOST_DEPLOYMENT.md`
- Review backend terminal for errors
- Check browser console (F12) for frontend issues

---

**Happy Meeting! 🎙️✨**

*Turn every meeting into actionable insights with AI!*
