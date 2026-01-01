# 🚀 AI Meeting Minutes - Kaise Run Karein (Asan Tareeqa)

## ✅ **Step 1: Code Already GitHub Par Hai**

Aap ka code already GitHub repository mein hai:
```
https://github.com/connectaitsa-sudo/Connecta-Workspace
Branch: cursor/ai-meeting-minutes-system-1e9d
```

**Aap ko download nahi karna!** Code already workspace mein hai!

---

## 📂 **Step 2: Terminal Kholo**

### Windows:
```
1. Windows key + R dabao
2. "cmd" type karo
3. Enter dabao
```

### Mac/Linux:
```
1. Terminal app kholo
2. Ya Ctrl+Alt+T dabao
```

---

## 🔥 **Step 3: Backend Start Karo**

### Terminal 1 (Backend):

```bash
# 1. Folder mein jao
cd /workspace/ai-meeting-minutes/backend

# 2. Virtual environment activate karo
source venv/bin/activate

# Windows users:
venv\Scripts\activate

# 3. Backend run karo
python run.py
```

**Yeh dikhega:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend chal raha hai!**

---

## 💻 **Step 4: Frontend Start Karo**

### Terminal 2 (Nayi terminal kholo):

```bash
# 1. Folder mein jao
cd /workspace/ai-meeting-minutes/frontend

# 2. Frontend run karo
npm run dev
```

**Yeh dikhega:**
```
VITE v5.0.0  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

✅ **Frontend chal raha hai!**

---

## 🌐 **Step 5: Browser Mein Kholo**

**Option 1:**
```
http://localhost:5173
```

**Option 2:**
```
http://localhost:3000
```

✅ **System khul gaya!**

---

## 🎯 **Quick Test - Sab Kuch Check Karo**

### Test 1: Dashboard Dekho
```
1. Browser mein URL kholo
2. Dashboard dikha? ✓
3. Sidebar dikha? ✓
4. Stats cards dikhe? ✓
```

### Test 2: Zoom Button
```
1. Sidebar mein "Integrations" par click
2. "Connect Zoom" button dikha? ✓
3. Click karo (popup aayega) ✓
```

### Test 3: Settings
```
1. Sidebar mein "Settings" par click
2. API Configuration dikha? ✓
3. Language options dikhe? ✓
4. "Save Settings" button dikha? ✓
```

### Test 4: New Meeting
```
1. Sidebar mein "New Meeting" par click
2. "Upload File" tab dikha? ✓
3. "Record Audio" tab dikha? ✓
4. "Paste Transcript" tab dikha? ✓
```

✅ **Sab kuch kaam kar raha hai!**

---

## 🔧 **Agar Masla Aaye:**

### Problem 1: "Command not found: python"
```bash
# Try:
python3 run.py

# Ya check Python installed hai:
python --version
python3 --version
```

### Problem 2: "venv/bin/activate: No such file"
```bash
# Virtual environment banao:
cd /workspace/ai-meeting-minutes/backend
python -m venv venv

# Phir activate karo:
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# Dependencies install karo:
pip install -r requirements.txt
```

### Problem 3: "Command not found: npm"
```bash
# Node.js install karo:
# Windows: https://nodejs.org/
# Mac: brew install node
# Linux: sudo apt install nodejs npm

# Check:
node --version
npm --version
```

### Problem 4: "Port 8000 already in use"
```bash
# Port change karo:
# backend/.env file mein:
PORT=8001

# Ya running process band karo:
# Windows: Ctrl+C terminal mein
# Mac/Linux: Ctrl+C terminal mein
```

### Problem 5: "Module not found"
```bash
# Backend dependencies install karo:
cd backend
pip install -r requirements.txt

# Frontend dependencies install karo:
cd frontend
npm install
```

---

## 📝 **Summary (Poora Process):**

```bash
# Terminal 1 - Backend
cd /workspace/ai-meeting-minutes/backend
source venv/bin/activate    # venv\Scripts\activate (Windows)
python run.py

# Terminal 2 - Frontend (nayi terminal)
cd /workspace/ai-meeting-minutes/frontend
npm run dev

# Browser
Open: http://localhost:5173
```

**Bus itna hi! Ab kaam karo!** 🎉

---

## 🎓 **Kya Kya Kar Sakte Ho:**

### 1. Meeting Record Karo
```
New Meeting → Record Audio → Start → Speak → Stop → Upload
```

### 2. Audio File Upload Karo
```
New Meeting → Upload File → Select file → Upload
```

### 3. Transcript Paste Karo
```
New Meeting → Paste Transcript → Paste text → Generate
```

### 4. Zoom Connect Karo
```
Integrations → Connect Zoom → Login → Authorize → Done!
```

### 5. Settings Change Karo
```
Settings → Report Language → Bilingual → Save Settings
```

### 6. Report Download Karo
```
Meeting Detail → Export PDF/DOCX/TXT → Download
```

---

## 💡 **Pro Tips:**

### Tip 1: Dono Terminals Ko Chalta Rakho
```
Backend terminal aur Frontend terminal
Dono ko close mat karo!
```

### Tip 2: Browser Console Check Karo (Agar Error Aaye)
```
F12 dabao → Console tab → Errors dekho
```

### Tip 3: Backend Logs Check Karo
```
Backend terminal mein errors/logs dikhengi
```

### Tip 4: Agar System Slow Ho
```
Ctrl+C dabao dono terminals mein
Phir restart karo
```

---

## 🔥 **Important URLs:**

- **Frontend:** http://localhost:5173 or http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## ✅ **Checklist (Sab Ready Hai?):**

- [ ] Python installed (python --version)
- [ ] Node.js installed (node --version)
- [ ] Code already workspace mein hai (/workspace/ai-meeting-minutes)
- [ ] OpenAI API key configured (backend/.env)
- [ ] Two terminals open
- [ ] Backend running (Terminal 1)
- [ ] Frontend running (Terminal 2)
- [ ] Browser open (http://localhost:5173)

**Agar sab ✓ hai, to system ready hai!** 🎉

---

## 🎯 **Ek Bar Samjho:**

```
1. Backend = Server (Python/FastAPI)
   ↓
   Ye transcription, AI processing, database handle karta hai
   
2. Frontend = User Interface (React)
   ↓
   Ye beautiful UI, buttons, forms dikhata hai
   
3. Dono miltey hain = Complete System!
   ↓
   Backend data process karta hai
   Frontend display karta hai
```

---

## 📞 **Quick Commands (Copy-Paste):**

### Windows:
```cmd
REM Terminal 1 - Backend
cd C:\workspace\ai-meeting-minutes\backend
venv\Scripts\activate
python run.py

REM Terminal 2 - Frontend
cd C:\workspace\ai-meeting-minutes\frontend
npm run dev
```

### Mac/Linux:
```bash
# Terminal 1 - Backend
cd /workspace/ai-meeting-minutes/backend
source venv/bin/activate
python run.py

# Terminal 2 - Frontend
cd /workspace/ai-meeting-minutes/frontend
npm run dev
```

---

## 🎉 **Ab Maza Karo!**

System ab chal raha hai! 🚀

- ✅ Backend running
- ✅ Frontend running
- ✅ Browser mein khula
- ✅ Sab kuch kaam kar raha hai!

**Happy Meeting! 🎙️✨**
