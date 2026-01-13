# 🚀 Local Setup - Simple Guide

## Step 1: GitHub se Clone karein

```bash
# Terminal/CMD kholen aur ye command chalayein:
git clone <your-github-repo-url>
cd ai-meeting-minutes
```

## Step 2: Backend Setup (5 minutes)

```bash
# Backend folder mein jayein
cd backend

# Virtual environment banayein
python -m venv venv

# Activate karein
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Packages install karein
pip install -r requirements.txt

# .env file banayein
copy .env.example .env          # Windows
# ya
cp .env.example .env            # Mac/Linux

# Ab .env file kholen aur apni OpenAI API key add karein:
# OPENAI_API_KEY=sk-your-key-here

# Backend start karein
python run.py
```

✅ Backend chal raha hai: http://localhost:8000

## Step 3: Frontend Setup (5 minutes)

**Nayi terminal window kholen** (pehli ko chalta rehne dein!)

```bash
# Frontend folder mein jayein
cd ai-meeting-minutes/frontend

# Packages install karein
npm install

# Frontend start karein
npm run dev
```

✅ Frontend chal raha hai: http://localhost:3000

## Step 4: Browser mein kholen

http://localhost:3000

---

## Agar koi problem aaye:

### "Python not found"
```bash
python3 --version
# Agar install nahi hai: https://www.python.org/downloads/
```

### "npm not found"
```bash
node --version
# Agar install nahi hai: https://nodejs.org/
```

### "Port already in use"
```bash
# Pehle running process ko band karein
# Phir dobara try karein
```

### Backend errors
```bash
# Check karein .env file mein API key hai ya nahi
cat .env              # Mac/Linux
type .env             # Windows
```

---

## OpenAI API Key kahan se lein?

1. https://platform.openai.com/signup par jayein
2. Account banayein
3. https://platform.openai.com/api-keys par jayein
4. "Create new secret key" click karein
5. Key copy karein (sk- se shuru hogi)
6. backend/.env file mein paste karein

---

## Zaruri Requirements:

- Python 3.11+ 
- Node.js 18+
- OpenAI API key
- Internet connection

---

## Done! 🎉

Ab app chal raha hai: http://localhost:3000

Testing ke liye:
1. "Transcript Text" tab click karein
2. "Load Sample Transcript" button click karein  
3. "Generate Meeting Minutes" click karein
4. 10 seconds wait karein
5. Results dekhen!
