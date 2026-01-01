# 🚀 Git Bash Se Kaise Run Karein - Complete Guide

## 📍 **Step-by-Step (Git Bash Users)**

---

## **STEP 1: Git Bash Kholo**

1. Windows Start Menu → Type "Git Bash"
2. Ya right-click karo folder mein → "Git Bash Here"

✅ **Git Bash terminal khul gaya!**

---

## **STEP 2: Repository Location Par Jao**

```bash
# Agar already cloned hai:
cd ~/Connecta-Workspace

# Agar nahi hai, to clone karo:
git clone https://github.com/connectaitsa-sudo/Connecta-Workspace.git
cd Connecta-Workspace
```

---

## **STEP 3: Branch Checkout Karo**

```bash
# Latest changes pull karo
git fetch origin

# Branch checkout karo
git checkout cursor/ai-meeting-minutes-system-1e9d

# Latest code pull karo
git pull origin cursor/ai-meeting-minutes-system-1e9d
```

✅ **Branch checkout ho gayi! Code latest hai!**

---

## **STEP 4: Backend Setup**

```bash
# AI Meeting Minutes folder mein jao
cd ai-meeting-minutes/backend

# Virtual environment activate karo (Git Bash mein)
source venv/bin/activate

# Agar venv nahi hai, to banao:
python -m venv venv
source venv/bin/activate

# Dependencies install karo
pip install -r requirements.txt

# Backend run karo
python run.py
```

**Ye dikhega:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend chal raha hai!** (Yeh terminal **khula rakho**)

---

## **STEP 5: Frontend Setup (Nayi Git Bash)**

**Nayi Git Bash terminal kholo** (pehli wali chalta rakho!)

```bash
# Same folder mein jao
cd ~/Connecta-Workspace/ai-meeting-minutes/frontend

# Dependencies install karo (agar nahi hai)
npm install

# Frontend run karo
npm run dev
```

**Ye dikhega:**
```
VITE v5.0.0  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

✅ **Frontend chal raha hai!** (Yeh terminal bhi **khula rakho**)

---

## **STEP 6: Browser Mein Kholo**

```
http://localhost:5173
```

✅ **System chal gaya! Maza karo!** 🎉

---

## 📝 **Complete Commands (Copy-Paste for Git Bash):**

### Terminal 1 (Backend):
```bash
cd ~/Connecta-Workspace
git checkout cursor/ai-meeting-minutes-system-1e9d
git pull origin cursor/ai-meeting-minutes-system-1e9d
cd ai-meeting-minutes/backend
source venv/bin/activate
python run.py
```

### Terminal 2 (Frontend):
```bash
cd ~/Connecta-Workspace/ai-meeting-minutes/frontend
npm run dev
```

### Browser:
```
http://localhost:5173
```

---

## 🔧 **Agar Masla Aaye:**

### Problem 1: "Repository not found"
```bash
# Clone karo pehle:
cd ~
git clone https://github.com/connectaitsa-sudo/Connecta-Workspace.git
cd Connecta-Workspace
```

### Problem 2: "Branch not found"
```bash
# Remote branches dekho:
git branch -r

# Fetch karo:
git fetch origin

# Phir checkout karo:
git checkout cursor/ai-meeting-minutes-system-1e9d
```

### Problem 3: "venv/bin/activate: No such file"
```bash
# Virtual environment banao:
cd ai-meeting-minutes/backend
python -m venv venv

# Activate karo:
source venv/bin/activate

# Dependencies install karo:
pip install -r requirements.txt
```

### Problem 4: "npm: command not found"
```bash
# Node.js install karo:
# Download from: https://nodejs.org/
# Restart Git Bash after installation

# Check:
node --version
npm --version
```

### Problem 5: "Port already in use"
```bash
# Backend band karo: Ctrl+C
# Ya port change karo backend/.env mein:
PORT=8001
```

---

## 🎯 **Visual Flow (Git Bash):**

```
Git Bash Terminal 1          Git Bash Terminal 2
        ↓                            ↓
cd Connecta-Workspace        cd Connecta-Workspace
        ↓                            ↓
git checkout branch          (same branch)
        ↓                            ↓
cd backend                   cd frontend
        ↓                            ↓
source venv/bin/activate     npm run dev
        ↓                            ↓
python run.py                Port 5173 running
        ↓                            ↓
Port 8000 running            ────────┘
        └────────────────────────┬──
                                ↓
                        Browser: localhost:5173
                                ↓
                        🎉 System Working!
```

---

## 💡 **Git Bash Specific Tips:**

### 1. Path Format:
```bash
# Git Bash mein Unix-style paths use karo:
cd ~/Connecta-Workspace              # ✓ Correct
cd C:\Users\Name\Connecta-Workspace  # ✗ Wrong

# Windows path ko Git Bash format mein:
cd /c/Users/Name/Connecta-Workspace  # ✓ Correct
```

### 2. Virtual Environment:
```bash
# Git Bash mein:
source venv/bin/activate  # ✓ Correct

# CMD/PowerShell mein:
venv\Scripts\activate     # ✗ Wrong for Git Bash
```

### 3. Multiple Terminals:
```bash
# Right-click karo folder mein → "Git Bash Here"
# Ya new tab kholo: Ctrl+Shift+N
```

---

## 🚀 **Quick Start Script (Git Bash):**

Copy-paste karo **ek saath**:

### Script 1: Backend Start
```bash
#!/bin/bash
cd ~/Connecta-Workspace
git checkout cursor/ai-meeting-minutes-system-1e9d
git pull origin cursor/ai-meeting-minutes-system-1e9d
cd ai-meeting-minutes/backend
source venv/bin/activate || python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Script 2: Frontend Start (Nayi terminal)
```bash
#!/bin/bash
cd ~/Connecta-Workspace/ai-meeting-minutes/frontend
npm install
npm run dev
```

---

## ✅ **Checklist (Git Bash):**

- [ ] Git Bash installed? (`git --version`)
- [ ] Python installed? (`python --version`)
- [ ] Node.js installed? (`node --version`)
- [ ] Repository cloned? (`ls ~/Connecta-Workspace`)
- [ ] Branch checkout? (`git branch`)
- [ ] Backend running? (Terminal 1: Port 8000)
- [ ] Frontend running? (Terminal 2: Port 5173)
- [ ] Browser open? (http://localhost:5173)

---

## 🎓 **Common Git Bash Commands:**

```bash
# Current location dekho
pwd

# Branch dekho
git branch

# Status dekho
git status

# Latest changes pull karo
git pull

# Branches list karo
git branch -a

# Switch branch
git checkout branch-name

# Logs dekho
git log --oneline -5
```

---

## 🔥 **Super Quick Start (Git Bash - 2 Minutes):**

### Terminal 1:
```bash
cd ~/Connecta-Workspace && \
git checkout cursor/ai-meeting-minutes-system-1e9d && \
git pull && \
cd ai-meeting-minutes/backend && \
source venv/bin/activate && \
python run.py
```

### Terminal 2 (Nayi Git Bash):
```bash
cd ~/Connecta-Workspace/ai-meeting-minutes/frontend && \
npm run dev
```

### Browser:
```
http://localhost:5173
```

---

## 📞 **Git Bash Specific Errors:**

### Error 1: "bash: cd: no such file or directory"
```bash
# Repository path check karo:
ls ~
ls ~/Connecta-Workspace

# Agar nahi hai:
cd ~
git clone https://github.com/connectaitsa-sudo/Connecta-Workspace.git
```

### Error 2: "fatal: not a git repository"
```bash
# Repository mein jao:
cd ~/Connecta-Workspace
git status
```

### Error 3: "error: pathspec did not match"
```bash
# Branches fetch karo:
git fetch origin
git branch -r
git checkout cursor/ai-meeting-minutes-system-1e9d
```

### Error 4: "python: command not found"
```bash
# Try python3:
python3 --version
python3 run.py

# Ya Python path add karo
```

---

## 🎯 **Final Commands Summary:**

```bash
# ============================================
# GIT BASH - AI MEETING MINUTES
# ============================================

# TERMINAL 1 (Backend):
cd ~/Connecta-Workspace
git checkout cursor/ai-meeting-minutes-system-1e9d
git pull origin cursor/ai-meeting-minutes-system-1e9d
cd ai-meeting-minutes/backend
source venv/bin/activate
python run.py

# TERMINAL 2 (Frontend):
cd ~/Connecta-Workspace/ai-meeting-minutes/frontend
npm run dev

# BROWSER:
http://localhost:5173

# ============================================
# DONE! SYSTEM RUNNING! 🚀
# ============================================
```

---

## 🎉 **Ab System Chal Raha Hai!**

Aap kar sakte ho:

✅ Meetings record karo  
✅ Files upload karo  
✅ Transcripts paste karo  
✅ AI minutes generate karo  
✅ Reports download karo (PDF/DOCX/TXT)  
✅ Zoom connect karo  
✅ Teams connect karo  
✅ Settings change karo  
✅ Multilingual use karo  

**Happy Meeting! 🎙️✨**

---

## 📚 **More Help:**

- **Quick Commands**: `COMMANDS.txt`
- **Urdu Guide**: `URDU_GUIDE.md`
- **English Guide**: `FINAL_GUIDE.md`
- **What's Fixed**: `WHATS_FIXED.md`

**Enjoy your enterprise-level system!** 🚀
