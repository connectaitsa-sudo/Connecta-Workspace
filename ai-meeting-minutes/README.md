# 🎙️ AI Meeting Minutes System

An intelligent system that automatically transcribes, summarizes, and generates comprehensive meeting minutes from audio/video recordings or live meetings. Perfect for integration with Zoom, Microsoft Teams, Google Meet, and other meeting platforms.

## ✨ Features

### Core Capabilities
- 🎤 **Live Audio Recording** - Record meetings directly in the browser
- 📤 **File Upload** - Support for MP3, WAV, MP4, M4A, WebM, and more
- 📝 **Text Transcription** - Paste meeting transcripts directly
- 🤖 **AI-Powered Analysis** - Automatic extraction of:
  - Meeting summary
  - Key discussion points
  - Decisions made
  - Action items with owners and due dates
  - Next steps
  - Participant identification
- 📊 **Export Options** - Download minutes in PDF, DOCX, or TXT format
- 🔄 **Real-time Processing** - Background processing with live status updates

### Integration Ready
- 🔗 Zoom webhook support
- 🔗 Microsoft Teams integration
- 🔗 Generic webhook API for custom integrations

## 🏗️ Architecture

```
ai-meeting-minutes/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration & database
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   │       ├── transcription.py    # OpenAI Whisper integration
│   │       ├── ai_processor.py     # GPT-4 summarization
│   │       └── export_service.py   # PDF/DOCX export
│   ├── uploads/            # Uploaded audio files
│   ├── exports/            # Generated documents
│   └── requirements.txt
│
└── frontend/               # React + TypeScript frontend
    ├── src/
    │   ├── components/     # React components
    │   ├── api.ts         # API client
    │   ├── types.ts       # TypeScript types
    │   └── App.tsx
    └── package.json
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** - Backend runtime
- **Node.js 18+** - Frontend development
- **OpenAI API Key** - For Whisper (transcription) and GPT-4 (summarization)

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-meeting-minutes
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key
```

**Configure `.env` file:**

```env
# Required
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional
ASSEMBLYAI_API_KEY=your-assemblyai-key  # Alternative transcription service
DEBUG=True
PORT=8000
```

#### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Optional: Configure API URL
# Create .env file if backend is not on localhost:8000
echo "VITE_API_URL=http://localhost:8000" > .env
```

### Running the Application

#### Start Backend Server

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python run.py
```

Backend will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

#### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Frontend will be available at:
- **Web App**: http://localhost:3000

## 📖 Usage

### 1. Audio/Video Upload

1. Click on "Upload" button or drag & drop audio/video file
2. Supported formats: MP3, WAV, MP4, M4A, WebM, OGG, FLAC
3. Click "Generate Summary & Minutes"
4. Wait for processing (transcription + AI analysis)
5. View results and export as needed

### 2. Live Recording

1. Click "Record" button
2. Allow microphone access
3. Speak naturally during your meeting
4. Click "Stop Recording"
5. System processes automatically

### 3. Transcript Text

1. Switch to "Transcript Text" mode
2. Paste your meeting transcript
3. Include speaker names for best results (e.g., "John: Hello everyone...")
4. Click "Generate Meeting Minutes"
5. AI extracts structured information

### 4. Export Options

- **PDF** - Professional formatted document
- **DOCX** - Editable Microsoft Word format
- **TXT** - Plain text format

## 🔌 API Integration

### Platform Integrations

#### Zoom Integration

```python
# Configure in .env
ZOOM_CLIENT_ID=your-zoom-client-id
ZOOM_CLIENT_SECRET=your-zoom-client-secret
ZOOM_WEBHOOK_SECRET=your-webhook-secret
```

Set up Zoom webhook to send recordings to:
```
POST https://your-domain.com/api/meetings/zoom-webhook
```

#### Microsoft Teams Integration

```python
# Configure in .env
TEAMS_CLIENT_ID=your-teams-client-id
TEAMS_CLIENT_SECRET=your-teams-client-secret
```

### REST API Endpoints

#### Upload Audio File

```bash
curl -X POST http://localhost:8000/api/meetings/upload-audio \
  -F "file=@meeting.mp3" \
  -F "title=Product Review Meeting"
```

#### Upload Transcript

```bash
curl -X POST http://localhost:8000/api/meetings/upload-transcript \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "John: Hello everyone...",
    "title": "Team Standup"
  }'
```

#### Get Meeting Details

```bash
curl http://localhost:8000/api/meetings/1
```

#### Export Meeting Minutes

```bash
# Export as PDF
curl http://localhost:8000/api/meetings/1/export/pdf -o minutes.pdf

# Export as DOCX
curl http://localhost:8000/api/meetings/1/export/docx -o minutes.docx
```

## 🧪 Example Use Cases

### 1. Corporate Meetings
- Automatically capture action items and decisions
- Track participant engagement
- Generate executive summaries

### 2. Remote Team Standups
- Record daily standup meetings
- Extract blockers and tasks
- Share minutes with team

### 3. Client Calls
- Professional meeting documentation
- Track commitments and deliverables
- Easy sharing with stakeholders

### 4. Educational Settings
- Lecture transcription
- Key concept extraction
- Student reference material

### 5. Legal/Medical Consultations
- Accurate record keeping
- Compliance documentation
- Patient/client notes

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI Whisper API** - Audio transcription
- **GPT-4 Turbo** - Meeting analysis and summarization
- **SQLAlchemy** - Database ORM
- **Python-DOCX** - Word document generation
- **ReportLab** - PDF generation

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Axios** - HTTP client
- **Lucide React** - Icons
- **React Dropzone** - File upload

## 📊 Database Schema

```sql
meetings
├── id (Primary Key)
├── title
├── source_type (upload, recording, zoom, teams)
├── audio_file_path
├── transcript
├── duration_minutes
├── participants (JSON)
├── summary
├── key_points (JSON)
├── decisions (JSON)
├── action_items (JSON)
├── next_steps (JSON)
├── status (uploaded, transcribing, processing, completed, failed)
├── created_at
└── updated_at
```

## 🔐 Security Considerations

1. **API Keys** - Store in environment variables, never commit to git
2. **File Upload** - Validate file types and size limits
3. **CORS** - Configure allowed origins in production
4. **Rate Limiting** - Consider adding rate limiting for production
5. **Data Privacy** - Implement user authentication and meeting access control

## 📈 Performance

- **Transcription**: ~1 minute of audio = 10-15 seconds processing
- **AI Analysis**: ~5-10 seconds for typical meeting transcript
- **Max File Size**: 500MB (configurable)
- **Concurrent Processing**: Background tasks with async processing

## 🐛 Troubleshooting

### Backend Issues

**Issue**: Import errors
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: Database errors
```bash
# Solution: Delete and reinitialize database
rm meeting_minutes.db
python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"
```

### Frontend Issues

**Issue**: API connection errors
```bash
# Solution: Check backend is running and VITE_API_URL is correct
# Verify CORS settings in backend/app/core/config.py
```

**Issue**: Microphone access denied
```bash
# Solution: Check browser permissions
# Use HTTPS in production (required for getUserMedia API)
```

## 🚀 Deployment

### Backend (FastAPI)

**Docker:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

**Or use platforms:**
- Railway
- Render
- AWS Lambda + API Gateway
- Google Cloud Run

### Frontend (React)

```bash
npm run build
# Deploy 'dist' folder to:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
# - GitHub Pages
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenAI for Whisper and GPT-4 APIs
- FastAPI framework
- React community

## 📧 Support

For issues and questions:
- Create an issue on GitHub
- Check API documentation at `/docs` endpoint

---

Built with ❤️ for better meeting productivity
