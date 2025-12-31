# 🏠 Complete Localhost Deployment Guide

This guide will help you run the AI Meeting Minutes System on your local computer from start to finish.

## 📋 Prerequisites Check

Before starting, verify you have everything installed:

### 1. Check Python Installation

Open terminal/command prompt and type:

```bash
python --version
```

Or try:

```bash
python3 --version
```

**You should see**: `Python 3.11.x` or higher

**If not installed**: Download from https://www.python.org/downloads/
- ✅ During installation, check "Add Python to PATH"

### 2. Check Node.js Installation

In terminal, type:

```bash
node --version
```

**You should see**: `v18.x.x` or higher

**If not installed**: Download from https://nodejs.org/
- Choose the "LTS" (Long Term Support) version

### 3. Get OpenAI API Key

1. Go to https://platform.openai.com/signup
2. Create account or sign in
3. Go to https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Name it "Meeting Minutes"
6. **Copy the key** (starts with `sk-`)
7. ⚠️ **Save it somewhere safe** - you can't see it again!

**Cost**: About $0.40 per 1-hour meeting

---

## 🚀 Step-by-Step Installation

### Part 1: Backend Setup (5 minutes)

#### Step 1.1: Open Terminal/Command Prompt

**Windows**: 
- Press `Win + R`
- Type `cmd` and press Enter

**Mac**: 
- Press `Cmd + Space`
- Type `terminal` and press Enter

**Linux**: 
- Press `Ctrl + Alt + T`

#### Step 1.2: Navigate to Project

```bash
cd ai-meeting-minutes
cd backend
```

#### Step 1.3: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
```

**On Mac/Linux:**
```bash
python3 -m venv venv
```

**What you'll see**: A new folder called `venv` will be created. This takes 30-60 seconds.

#### Step 1.4: Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
source venv/bin/activate
```

**Success indicator**: You should see `(venv)` at the start of your command line:
```
(venv) C:\...\backend>
```

#### Step 1.5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**What happens**: This installs all required Python packages. Takes 2-3 minutes.

**You'll see**: Many packages being downloaded and installed (FastAPI, OpenAI, SQLAlchemy, etc.)

#### Step 1.6: Create Configuration File

**On Windows:**
```bash
copy .env.example .env
```

**On Mac/Linux:**
```bash
cp .env.example .env
```

#### Step 1.7: Add Your OpenAI API Key

**Open the .env file:**

**Windows:**
```bash
notepad .env
```

**Mac:**
```bash
open -e .env
```

**Linux:**
```bash
nano .env
```

**Edit this line:**
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

Replace `sk-your-openai-api-key-here` with your actual OpenAI API key.

**Example:**
```env
OPENAI_API_KEY=sk-proj-abc123xyz789...
```

**Save and close the file**
- Windows (Notepad): File → Save, then close
- Mac: Cmd + S, then Cmd + Q
- Linux (nano): Ctrl + X, then Y, then Enter

#### Step 1.8: Start Backend Server

```bash
python run.py
```

**Success! You should see:**
```
╔══════════════════════════════════════════════════════════╗
║  🎙️  AI Meeting Minutes System - Backend Server        ║
╚══════════════════════════════════════════════════════════╝

Server starting on: http://0.0.0.0:8000
API Documentation: http://localhost:8000/docs

🚀 Starting AI Meeting Minutes System...
✅ Database initialized
✅ Directories created
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

**Test it**: Open browser and go to http://localhost:8000

You should see:
```json
{"message":"AI Meeting Minutes System API","version":"1.0.0","status":"operational"}
```

✅ **Backend is running!** Keep this terminal window open.

---

### Part 2: Frontend Setup (5 minutes)

#### Step 2.1: Open NEW Terminal Window

⚠️ **Important**: Don't close the first terminal! Open a NEW one.

**Windows**: 
- Press `Win + R`, type `cmd`, press Enter

**Mac**: 
- Press `Cmd + T` (new tab) or `Cmd + N` (new window)

**Linux**: 
- Press `Ctrl + Shift + T` (new tab)

#### Step 2.2: Navigate to Frontend

```bash
cd ai-meeting-minutes
cd frontend
```

#### Step 2.3: Install Node.js Dependencies

```bash
npm install
```

**What happens**: This installs all required JavaScript packages. Takes 2-3 minutes.

**You'll see**: Progress bar and many packages being installed (React, Vite, Axios, etc.)

**If you see warnings**: That's normal! Warnings are okay, errors are not.

#### Step 2.4: Start Frontend Server

```bash
npm run dev
```

**Success! You should see:**
```
VITE v5.0.11  ready in 500 ms

➜  Local:   http://localhost:3000/
➜  Network: http://192.168.1.x:3000/
➜  press h to show help
```

✅ **Frontend is running!** Keep this terminal window open too.

---

## 🎉 Access Your Application

### Open Your Browser

Go to: **http://localhost:3000**

**You should see:**
- Purple gradient background
- "AI Meeting Summarizer" title with icon
- "Automatically transcribe, summarize, and generate meeting minutes"
- Two tabs: "Audio/Video Upload" and "Transcript Text"
- Upload area or transcript input box

✅ **Success! Your application is running!**

---

## 🧪 Test the System

### Test 1: Using Sample Transcript (30 seconds)

1. Click the **"Transcript Text"** tab
2. Click **"Load Sample Transcript"** button (top right)
3. You'll see a sample conversation appear
4. Click **"Generate Meeting Minutes"** button (big purple button at bottom)
5. Wait 5-10 seconds
6. **Results appear!** You should see:
   - ✅ Meeting Summary
   - ✅ Duration
   - ✅ Participants (4 people)
   - ✅ Key Discussion Points
   - ✅ Decisions Made
   - ✅ Action Items with owners
   - ✅ Next Steps

7. Try exporting:
   - Click **"PDF"** button - downloads a PDF file
   - Click **"DOCX"** button - downloads a Word document
   - Click **"TXT"** button - downloads a text file

### Test 2: Record Your Own Audio (2 minutes)

1. Click **"Audio/Video Upload"** tab
2. Click **"Start Recording"** button (purple microphone button)
3. Browser will ask for microphone permission - click **"Allow"**
4. Speak clearly: *"This is [Your Name]. We need to schedule a team meeting to discuss the Q4 budget. Sarah will prepare the presentation by Friday. Mike will review the numbers."*
5. Click **"Stop Recording"** (red button)
6. You'll see your recording file listed
7. Click **"Generate Summary & Minutes"** button
8. Wait 15-30 seconds (transcription + AI analysis)
9. View your results!

### Test 3: Upload Audio File (if you have one)

1. Prepare an audio/video file (MP3, WAV, MP4, etc.)
2. Click **"Audio/Video Upload"** tab
3. Drag and drop the file into the upload area
4. OR click the upload area to browse for file
5. Click **"Generate Summary & Minutes"**
6. Wait for processing
7. View results!

---

## 📍 Important URLs

Keep these bookmarked:

| Service | URL | What It Is |
|---------|-----|------------|
| **Main App** | http://localhost:3000 | Your web interface |
| **Backend API** | http://localhost:8000 | API server |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Health Check** | http://localhost:8000/health | Server status |

---

## 🔄 Daily Usage

### Starting the System

Every time you want to use the system:

**Terminal 1 - Backend:**
```bash
cd ai-meeting-minutes/backend
source venv/bin/activate         # Mac/Linux
# OR
venv\Scripts\activate            # Windows
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd ai-meeting-minutes/frontend
npm run dev
```

**Then open**: http://localhost:3000

### Stopping the System

**To stop servers:**
- Press `Ctrl + C` in each terminal window

**To close terminals:**
- Type `exit` or just close the window

---

## 🐛 Troubleshooting

### Problem: "Python not found"

**Solution:**
```bash
# Try python3 instead of python
python3 --version
python3 -m venv venv
python3 run.py
```

### Problem: "pip not found"

**Solution:**
```bash
# On Windows
python -m pip install -r requirements.txt

# On Mac/Linux
python3 -m pip install -r requirements.txt
```

### Problem: "npm not found"

**Solution:**
- Node.js not installed properly
- Reinstall Node.js from https://nodejs.org/
- Make sure to check "Add to PATH" during installation
- Close and reopen terminal after installation

### Problem: "Port 8000 already in use"

**Solution:**
```bash
# Find and kill the process using port 8000

# Windows:
netstat -ano | findstr :8000
taskkill /PID [number] /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### Problem: "Port 3000 already in use"

**Solution:**
```bash
# Option 1: Use different port
npm run dev -- --port 3001

# Option 2: Kill process on port 3000
# Mac/Linux:
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID [number] /F
```

### Problem: Backend starts but shows errors

**Check these:**

1. **Is .env file configured?**
   ```bash
   cd backend
   cat .env              # Mac/Linux
   type .env             # Windows
   # Verify OPENAI_API_KEY is set
   ```

2. **Is OpenAI API key valid?**
   - Go to https://platform.openai.com/api-keys
   - Check if key is active
   - Create new key if needed

3. **Check backend logs**
   - Look at Terminal 1 for error messages
   - Common: "Invalid API key" or "Authentication failed"

### Problem: Frontend shows "Network Error"

**Solutions:**

1. **Check backend is running**
   - Go to http://localhost:8000
   - Should see JSON response
   - If not, backend isn't running

2. **Check CORS settings**
   - Backend `.env` should have:
   ```env
   ALLOWED_ORIGINS=http://localhost:3000
   ```

3. **Clear browser cache**
   - Press `Ctrl + Shift + Delete` (or `Cmd + Shift + Delete` on Mac)
   - Clear cached images and files
   - Reload page

### Problem: Microphone not working

**Solutions:**

1. **Check browser permissions**
   - Click lock icon in address bar
   - Allow microphone access

2. **Try different browser**
   - Chrome/Edge work best
   - Safari on Mac works
   - Firefox works

3. **Check microphone in system**
   - Windows: Settings → Privacy → Microphone
   - Mac: System Preferences → Security & Privacy → Microphone

### Problem: Processing stuck at "transcribing" or "processing"

**Solutions:**

1. **Check OpenAI API status**
   - Visit https://status.openai.com/
   - Check if services are operational

2. **Check API usage limits**
   - Go to https://platform.openai.com/usage
   - Verify you haven't hit limits
   - Add payment method if needed

3. **Check backend terminal**
   - Look for error messages
   - Common: "Rate limit exceeded" or "Insufficient quota"

4. **Restart processing**
   - Refresh the page
   - Upload/paste again

### Problem: Export buttons don't work

**Solutions:**

1. **Wait for processing to complete**
   - Status must be "completed"
   - Not "transcribing" or "processing"

2. **Check browser download settings**
   - Allow downloads from localhost
   - Check Downloads folder

3. **Try different format**
   - If PDF fails, try DOCX or TXT

---

## 📊 System Requirements

### Minimum Requirements
- **CPU**: Dual-core processor
- **RAM**: 4GB
- **Disk Space**: 2GB free
- **Internet**: Required (for OpenAI API calls)
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### Recommended Requirements
- **CPU**: Quad-core processor
- **RAM**: 8GB or more
- **Disk Space**: 5GB free
- **Internet**: Broadband connection
- **Browser**: Latest Chrome or Edge

---

## 💰 Cost Estimation

### OpenAI API Costs

| Item | Cost |
|------|------|
| Transcription (Whisper) | $0.006 per minute of audio |
| Analysis (GPT-4 Turbo) | $0.01-0.03 per meeting |

**Examples:**
- 5-minute meeting: ~$0.05
- 30-minute meeting: ~$0.20
- 1-hour meeting: ~$0.40
- 2-hour meeting: ~$0.75

**Monthly estimates:**
- 10 meetings/month (30 min each): ~$2.00
- 50 meetings/month (30 min each): ~$10.00
- 100 meetings/month (1 hour each): ~$40.00

---

## 🎯 Tips for Best Results

### For Audio Quality
- ✅ Use good microphone
- ✅ Quiet environment
- ✅ Speak clearly
- ✅ Moderate pace
- ✅ Minimize background noise

### For Transcript Input
- ✅ Include speaker names (e.g., "John: Hello...")
- ✅ Clear sentence structure
- ✅ Mention action items explicitly
- ✅ State decisions clearly

### Example Good Transcript
```
John: Good morning team. Let's review the Q4 roadmap.

Sarah: I've prepared three proposals. The budget is $50,000.

John: Great. Sarah, can you finalize the budget by Friday?

Sarah: Yes, I'll have it ready by end of week.

Mike: I'll review the technical requirements.

John: Perfect. Let's meet again next Tuesday.
```

---

## 📁 File Locations

### Where Files Are Stored

**Uploaded Audio Files:**
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

**To clean up old files:**
```bash
# Delete uploaded files
cd backend
rm -rf uploads/*        # Mac/Linux
del /q uploads\*        # Windows

# Delete exported files
rm -rf exports/*        # Mac/Linux
del /q exports\*        # Windows

# Reset database
rm meeting_minutes.db   # Mac/Linux
del meeting_minutes.db  # Windows
```

---

## 🔐 Security Notes

### Important
- ✅ Never share your `.env` file
- ✅ Never commit `.env` to git
- ✅ Keep OpenAI API key private
- ✅ Don't share meeting recordings without permission
- ✅ Use HTTPS in production (required for recording)

### For Production Use
- Change `DEBUG=False` in backend/.env
- Use PostgreSQL instead of SQLite
- Add user authentication
- Set up proper CORS
- Use environment variables
- Add rate limiting

---

## 🎓 Next Steps

### Learn More
1. 📖 Read `README.md` for overview
2. 📖 Read `FEATURES.md` for all features
3. 📖 Read `SETUP_GUIDE.md` for advanced setup
4. 🔌 Try Zoom/Teams integration
5. 🚀 Deploy to production

### Customize
1. Change color theme in frontend CSS
2. Modify AI prompts in `backend/app/services/ai_processor.py`
3. Add custom export templates
4. Integrate with your calendar
5. Add user authentication

---

## ✅ Success Checklist

Before you finish, verify:

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] OpenAI API key obtained
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] `.env` file created with API key
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Sample transcript test successful
- [ ] Export to PDF/DOCX/TXT working

---

## 🎉 Congratulations!

Your AI Meeting Minutes System is now running on localhost!

**Access it at**: http://localhost:3000

**What you can do:**
- 🎤 Record meetings directly
- 📤 Upload audio/video files
- 📝 Paste transcripts
- 🤖 Get AI-generated minutes
- 📄 Export to PDF/DOCX/TXT
- 🔗 Integrate with Zoom/Teams

**Need help?** Check the troubleshooting section above or review the documentation files.

**Happy meeting! 🎙️✨**
