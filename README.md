# 🎓 IELTS AI Tutor

A conversational AI tutor that helps students prepare for the IELTS exam.
Built with Claude API + Streamlit.

## What it does
- IELTS Speaking practice (Part 1, 2, 3)
- IELTS Writing evaluation (Task 1, Task 2)
- Scores on all 4 official IELTS criteria
- Band estimate after every response
- Vocabulary builder by topic

## How to run locally

### Step 1 — Install dependencies
pip install -r requirements.txt

### Step 2 — Run the app
streamlit run ielts_ai.py

### Step 3 — Add your API key
Get your Claude API key from console.anthropic.com
Paste it into the sidebar when the app opens.

## How to deploy free (get a public URL)

### Step 1 — Push to GitHub
- Create account at github.com
- Create new repository called "ielts-ai-tutor"
- Upload ielts_ai.py, requirements.txt, README.md

### Step 2 — Deploy on Streamlit Cloud
- Go to share.streamlit.io
- Sign in with GitHub
- Click "New app"
- Select your repository
- Main file: ielts_ai.py
- Click Deploy

### Step 3 — Add your API key as a secret
- In Streamlit Cloud dashboard → your app → Settings → Secrets
- Add this:
  ANTHROPIC_API_KEY = "your-key-here"
- Your public URL will be: yourname.streamlit.app

## Pricing
- Streamlit Cloud hosting: FREE
- Claude API: ~$0.01 per conversation
- $5 API credit = ~500 student sessions

## Built by
[LOGSHIR] — Gap year student, Mongolia
