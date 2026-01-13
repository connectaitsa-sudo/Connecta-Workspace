# 🚀 Getting Started - AI Meeting Minutes System

Welcome! This guide will get you up and running in **5 minutes**.

## 📋 What You Need

Before starting, make sure you have:

1. ✅ **Python 3.11+** installed
   - Check: `python --version` or `python3 --version`
   - Download: https://www.python.org/downloads/

2. ✅ **Node.js 18+** installed
   - Check: `node --version`
   - Download: https://nodejs.org/

3. ✅ **OpenAI API Key**
   - Sign up: https://platform.openai.com/signup
   - Get key: https://platform.openai.com/api-keys
   - Cost: ~$0.40 per 1-hour meeting

## 🎯 Quick Start (5 Minutes)

### Option 1: Using Quick Start Script (Recommended)

**Windows:**
```bash
quickstart.bat
```

**macOS/Linux:**
```bash
chmod +x quickstart.sh
./quickstart.sh
```

Then follow the prompts to add your OpenAI API key!

### Option 2: Manual Setup

#### Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

**Edit `backend/.env` and add your OpenAI API key:**
```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

#### Step 2: Frontend Setup (2 minutes)

Open a **new terminal window** and run:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

#### Step 3: Start the Application (1 minute)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python run.py
```

You should see:
```
🚀 Starting AI Meeting Minutes System...
✅ Database initialized
✅ Directories created
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

You should see:
```
➜  Local:   http://localhost:3000/
```

#### Step 4: Open & Test

1. Open browser to: **http://localhost:3000**
2. You should see the AI Meeting Summarizer interface!

## 🎬 First Test

### Test 1: Using Sample Transcript (30 seconds)

1. Click the **"Transcript Text"** tab
2. Click **"Load Sample Transcript"**
3. Click **"Generate Meeting Minutes"**
4. Wait 5-10 seconds
5. See the magic! ✨

You should see:
- Meeting summary
- Participants identified
- Key discussion points
- Decisions made
- Action items with owners
- Next steps

### Test 2: Try Recording (1 minute)

1. Click **"Audio/Video Upload"** tab
2. Click **"Record"** button
3. Allow microphone access when prompted
4. Say: *"This is John. We need to schedule a meeting with Sarah to discuss the Q4 budget by Friday."*
5. Click **"Stop Recording"**
6. Click **"Generate Summary & Minutes"**
7. Wait for processing (~15-30 seconds)
8. View your transcribed and analyzed meeting!

### Test 3: Export Documents

After generating minutes:
1. Click **"Export"** button
2. Choose format: **PDF**, **DOCX**, or **TXT**
3. File downloads automatically!

## 🎨 Interface Overview

### Main Sections

1. **Header** - App title and description
2. **Input Mode Selector** - Switch between audio upload and transcript input
3. **Input Area** - Upload files, record, or paste transcript
4. **Results Area** - View generated meeting minutes
5. **Export Buttons** - Download in various formats

### Status Indicators

- **Uploading** - File being uploaded
- **Transcribing** - Audio being converted to text
- **Processing** - AI analyzing the transcript
- **Completed** - Ready to view and export
- **Failed** - Error occurred (check backend logs)

## 📁 Project Structure

```
ai-meeting-minutes/
├── backend/              # Python FastAPI server
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── services/    # Business logic
│   │   ├── models/      # Database models
│   │   └── main.py      # App entry point
│   └── run.py           # Start script
│
├── frontend/            # React web app
│   ├── src/
│   │   ├── components/  # UI components
│   │   └── api.ts       # API client
│   └── package.json
│
└── Documentation/
    ├── README.md        # Overview
    ├── SETUP_GUIDE.md   # Detailed setup
    ├── FEATURES.md      # Feature list
    └── GETTING_STARTED.md (this file)
```

## 🔧 Configuration

### Backend Configuration (`backend/.env`)

```env
# Required - Add your OpenAI API key here
OPENAI_API_KEY=sk-your-key-here

# Server settings (usually keep defaults)
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS (frontend URL)
ALLOWED_ORIGINS=http://localhost:3000

# Database (SQLite by default)
DATABASE_URL=sqlite+aiosqlite:///./meeting_minutes.db

# File upload limits
MAX_UPLOAD_SIZE=500000000  # 500MB
```

### Frontend Configuration (optional)

Create `frontend/.env` only if backend is not on localhost:8000:
```env
VITE_API_URL=http://your-backend-url:8000
```

## 🔍 Testing the API

Visit http://localhost:8000/docs for interactive API documentation!

Try these endpoints:
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/meetings/upload-audio` - Upload audio file
- `GET /api/meetings/` - List all meetings

## 🐛 Troubleshooting

### Backend Won't Start

**Problem**: Import errors or module not found
```bash
# Solution: Activate virtual environment
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Problem**: "OpenAI API key not found"
```bash
# Solution: Check .env file
cd backend
cat .env  # Verify OPENAI_API_KEY is set
```

### Frontend Won't Start

**Problem**: Cannot find module
```bash
# Solution: Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Network error / Cannot connect to backend
```bash
# Solution:
# 1. Verify backend is running (Terminal 1)
# 2. Check http://localhost:8000 in browser
# 3. Check browser console for errors
```

### Recording Not Working

**Problem**: Microphone access denied
```bash
# Solution:
# 1. Check browser permissions (usually top-right of address bar)
# 2. For production, must use HTTPS
# 3. Try a different browser
```

### Processing Stuck

**Problem**: Meeting status stuck on "processing"
```bash
# Solution:
# 1. Check backend terminal for errors
# 2. Verify OpenAI API key is valid
# 3. Check OpenAI usage limits: https://platform.openai.com/usage
# 4. Try clicking "Regenerate" button
```

## 💡 Tips for Best Results

### For Transcription
- ✅ Use high-quality audio (minimal background noise)
- ✅ Clear speech at moderate pace
- ✅ Supported formats: MP3, WAV, MP4, M4A, WebM

### For AI Analysis
- ✅ Include speaker names (e.g., "John: Hello everyone...")
- ✅ Clear dialogue structure
- ✅ Mention action items explicitly
- ✅ State decisions clearly

### Sample Transcript Format
```
John: Good morning team. Let's discuss the Q4 roadmap.

Sarah: I've prepared three proposals. Should we start with the budget?

John: Yes. Sarah, can you present the budget by Friday?

Sarah: Absolutely. I'll have it ready.
```

## 📚 Next Steps

### For Daily Use
1. ✅ Bookmark http://localhost:3000
2. ✅ Keep backend running in background
3. ✅ Upload meetings after calls
4. ✅ Export and share with team

### For Integrations
1. 📖 Read `SETUP_GUIDE.md` for Zoom integration
2. 📖 Read `SETUP_GUIDE.md` for Teams integration
3. 📖 Check webhook endpoints in API docs

### For Production
1. 📖 Read deployment section in `README.md`
2. 🔐 Set `DEBUG=False` in production
3. 🔒 Use HTTPS (required for recording)
4. 💾 Consider PostgreSQL for database
5. 📊 Monitor API usage and costs

## 🎓 Learn More

- **Full Documentation**: See `README.md`
- **Detailed Setup**: See `SETUP_GUIDE.md`
- **All Features**: See `FEATURES.md`
- **API Docs**: http://localhost:8000/docs
- **OpenAI Docs**: https://platform.openai.com/docs

## 💬 Need Help?

- Check the troubleshooting section above
- Review backend logs in Terminal 1
- Check browser console for frontend errors
- Visit OpenAI status: https://status.openai.com/

## 🎉 You're Ready!

Congratulations! Your AI Meeting Minutes System is ready to use.

Start by uploading a recording or pasting a transcript, and watch the AI generate professional meeting minutes in seconds!

---

**Quick Links:**
- 🌐 App: http://localhost:3000
- 🔌 API: http://localhost:8000
- 📖 API Docs: http://localhost:8000/docs

**Happy Meeting! 🎙️**
