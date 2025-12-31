# 🚀 Setup Guide - AI Meeting Minutes System

This guide will help you set up the AI Meeting Minutes System from scratch.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Getting Your API Keys](#getting-your-api-keys)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Testing the System](#testing-the-system)
6. [Platform Integrations](#platform-integrations)
7. [Production Deployment](#production-deployment)

---

## System Requirements

### Required Software
- **Python 3.11 or higher** 
  - Check: `python --version` or `python3 --version`
  - Download: https://www.python.org/downloads/
  
- **Node.js 18 or higher**
  - Check: `node --version`
  - Download: https://nodejs.org/

- **pip** (Python package manager)
  - Usually comes with Python
  - Check: `pip --version`

- **npm** (Node package manager)
  - Comes with Node.js
  - Check: `npm --version`

### Operating System
- ✅ Windows 10/11
- ✅ macOS 11+
- ✅ Linux (Ubuntu 20.04+, Debian, etc.)

---

## Getting Your API Keys

### OpenAI API Key (Required)

1. **Create OpenAI Account**
   - Go to https://platform.openai.com/signup
   - Sign up or log in

2. **Generate API Key**
   - Navigate to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Name it "AI Meeting Minutes"
   - Copy the key (starts with `sk-`)
   - ⚠️ **Save it securely** - you won't see it again!

3. **Add Billing Information**
   - Go to https://platform.openai.com/account/billing
   - Add payment method
   - Set usage limits if desired

4. **Pricing** (as of 2024)
   - Whisper API: ~$0.006 per minute of audio
   - GPT-4 Turbo: ~$0.01-0.03 per meeting analysis
   - Example: 1-hour meeting = ~$0.40 total

### AssemblyAI API Key (Optional)

For advanced features like speaker diarization:

1. Go to https://www.assemblyai.com/
2. Sign up for free account
3. Get your API key from dashboard
4. Add to `.env` file

---

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd ai-meeting-minutes/backend
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required Python packages:
- FastAPI
- Uvicorn
- OpenAI
- SQLAlchemy
- And more...

**Troubleshooting:**
- If you get SSL errors, try: `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt`
- If specific packages fail, install them individually: `pip install fastapi uvicorn openai`

### Step 4: Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Open .env in your text editor
# On Windows: notepad .env
# On macOS: open -e .env
# On Linux: nano .env or vim .env
```

**Edit `.env` file:**

```env
# REQUIRED - Add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-key-here

# OPTIONAL - Keep defaults or customize
DEBUG=True
PORT=8000
HOST=0.0.0.0
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# OPTIONAL - Advanced features
ASSEMBLYAI_API_KEY=
ZOOM_CLIENT_ID=
ZOOM_CLIENT_SECRET=
TEAMS_CLIENT_ID=
TEAMS_CLIENT_SECRET=
```

⚠️ **Important**: Replace `sk-your-actual-key-here` with your real OpenAI API key!

### Step 5: Create Required Directories

```bash
mkdir uploads exports
```

### Step 6: Test Backend

```bash
python run.py
```

You should see:
```
🚀 Starting AI Meeting Minutes System...
✅ Database initialized
✅ Directories created
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it:**
1. Open browser to http://localhost:8000
2. You should see: `{"message": "AI Meeting Minutes System API"}`
3. Visit http://localhost:8000/docs for API documentation

### Step 7: Keep Backend Running

Leave this terminal window open with the backend running.

---

## Frontend Setup

### Step 1: Open New Terminal

Keep backend running in first terminal, open a new one.

### Step 2: Navigate to Frontend Directory

```bash
cd ai-meeting-minutes/frontend
```

### Step 3: Install Dependencies

```bash
npm install
```

This will install all required packages:
- React
- TypeScript
- Vite
- Axios
- And more...

**Troubleshooting:**
- If you get permission errors on macOS/Linux, try: `sudo npm install`
- If it's slow, try: `npm install --registry=https://registry.npmjs.org/`

### Step 4: Configure Environment (Optional)

Only needed if backend is NOT on `localhost:8000`:

```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env
```

### Step 5: Start Development Server

```bash
npm run dev
```

You should see:
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.1.x:3000/
```

### Step 6: Open Application

1. Open browser to http://localhost:3000
2. You should see the AI Meeting Summarizer interface!

---

## Testing the System

### Test 1: Upload Text Transcript

1. Click "Transcript Text" tab
2. Click "Load Sample Transcript"
3. Click "Generate Meeting Minutes"
4. Wait 5-10 seconds
5. View generated minutes with:
   - Summary
   - Participants
   - Key points
   - Decisions
   - Action items
   - Next steps

### Test 2: Record Audio (Optional)

1. Click "Audio/Video Upload" tab
2. Click "Record" button
3. Allow microphone access
4. Say something like: "This is a test. John speaking. We need to fix bug 123."
5. Click "Stop Recording"
6. Click "Generate Summary & Minutes"
7. Wait for processing (15-30 seconds)
8. View results

### Test 3: Upload Audio File (Optional)

1. Prepare a short audio file (MP3, WAV, or MP4)
2. Drag and drop into upload area
3. Click "Generate Summary & Minutes"
4. Wait for processing
5. View results

### Test 4: Export Documents

1. After generating minutes, click export buttons:
   - PDF - Downloads formatted PDF
   - DOCX - Downloads Word document
   - TXT - Downloads plain text

---

## Platform Integrations

### Zoom Integration

#### Prerequisites
- Zoom account (Pro, Business, or Enterprise)
- Zoom App Marketplace access

#### Setup Steps

1. **Create Zoom App**
   - Go to https://marketplace.zoom.us/
   - Click "Develop" → "Build App"
   - Choose "Meeting SDK"
   - Fill in app details

2. **Configure Webhook**
   - In app settings, add webhook URL:
     ```
     https://your-domain.com/api/integrations/zoom-webhook
     ```
   - Subscribe to events:
     - `recording.completed`
     - `recording.transcript_completed`

3. **Get Credentials**
   - Copy Client ID and Client Secret
   - Copy Webhook Secret Token

4. **Update Backend `.env`**
   ```env
   ZOOM_CLIENT_ID=your-zoom-client-id
   ZOOM_CLIENT_SECRET=your-zoom-client-secret
   ZOOM_WEBHOOK_SECRET=your-webhook-secret
   ```

5. **Test**
   - Record a Zoom meeting
   - Check webhook receives notification
   - Meeting auto-imports to system

### Microsoft Teams Integration

#### Prerequisites
- Microsoft 365 account
- Teams admin access
- Azure AD application

#### Setup Steps

1. **Create Azure AD App**
   - Go to https://portal.azure.com/
   - Navigate to "Azure Active Directory" → "App registrations"
   - Click "New registration"

2. **Configure Permissions**
   - Add permissions:
     - `OnlineMeetings.Read.All`
     - `CallRecords.Read.All`

3. **Get Credentials**
   - Copy Application (client) ID
   - Create client secret

4. **Update Backend `.env`**
   ```env
   TEAMS_CLIENT_ID=your-teams-client-id
   TEAMS_CLIENT_SECRET=your-teams-client-secret
   ```

5. **Setup Graph API Webhook**
   - Configure notification endpoint
   - Subscribe to meeting recording events

---

## Production Deployment

### Backend Deployment Options

#### Option 1: Railway (Recommended for Beginners)

1. Sign up at https://railway.app/
2. Create new project from GitHub
3. Add environment variables (OpenAI key, etc.)
4. Deploy!

#### Option 2: Render

1. Sign up at https://render.com/
2. Create new Web Service
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python run.py`
6. Add environment variables

#### Option 3: AWS/GCP/Azure

Use Docker container:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "run.py"]
```

### Frontend Deployment Options

#### Option 1: Vercel (Recommended)

1. Sign up at https://vercel.com/
2. Import GitHub repository
3. Framework: Vite
4. Build command: `npm run build`
5. Output directory: `dist`
6. Add environment variable: `VITE_API_URL`

#### Option 2: Netlify

1. Sign up at https://netlify.com/
2. Connect GitHub repository
3. Build command: `npm run build`
4. Publish directory: `dist`

### Production Checklist

- [ ] Set `DEBUG=False` in backend `.env`
- [ ] Configure proper CORS origins
- [ ] Set up HTTPS (required for microphone access)
- [ ] Add rate limiting
- [ ] Set up user authentication
- [ ] Configure database backups
- [ ] Monitor API usage and costs
- [ ] Add error tracking (Sentry, etc.)

---

## Troubleshooting

### Common Issues

#### Backend won't start

**Issue**: `ModuleNotFoundError`
```bash
Solution: Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Issue**: `OpenAI API key not found`
```bash
Solution: Check .env file exists and has valid API key
cat .env  # Check file contents
```

#### Frontend won't start

**Issue**: `Cannot find module`
```bash
Solution: Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Issue**: `Network error` when uploading
```bash
Solution: 
1. Check backend is running (http://localhost:8000)
2. Check CORS settings in backend
3. Check browser console for errors
```

#### Microphone not working

**Issue**: Permission denied
```bash
Solution:
1. Check browser permissions
2. Use HTTPS in production (required)
3. Try different browser
```

#### Processing stuck

**Issue**: Meeting status stuck on "processing"
```bash
Solution:
1. Check backend logs for errors
2. Verify OpenAI API key is valid
3. Check API usage limits
4. Try regenerating minutes
```

---

## Getting Help

- **API Documentation**: http://localhost:8000/docs
- **GitHub Issues**: Create an issue for bugs
- **OpenAI Status**: https://status.openai.com/

## Next Steps

1. ✅ Complete setup and testing
2. 🎨 Customize UI colors and branding
3. 🔐 Add user authentication
4. 📊 Set up analytics
5. 🚀 Deploy to production
6. 🔗 Configure platform integrations

---

**Congratulations!** 🎉 Your AI Meeting Minutes System is ready to use!
