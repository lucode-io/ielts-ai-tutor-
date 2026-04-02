# IELTS Master Platform

A full-stack AI-powered IELTS learning platform built with Streamlit, Claude API, and Supabase.

## Project Structure

```
ielts_master/
├── ielts_master.py          # Main entry point + router
├── requirements.txt
├── secrets.toml.template    # Copy to .streamlit/secrets.toml
├── schema.sql               # Run this in Supabase SQL Editor
├── modules/
│   ├── auth.py              # Login, signup, demo mode
│   ├── onboarding.py        # Diagnostic test for new users
│   ├── dashboard.py         # User HQ dashboard
│   ├── practice.py          # Core chat tutor (all 4 skills)
│   ├── reports.py           # Plotly analytics dashboard
│   ├── challenge.py         # 21-Day Speedrun Challenge
│   └── settings.py          # Profile & preferences
└── utils/
    ├── database.py          # All Supabase DB operations
    ├── ai.py                # Claude API + all system prompts
    └── styles.py            # Global CSS injection
```

## Setup Instructions

### 1. Supabase Setup
1. Go to https://supabase.com and create a new project
2. In the SQL Editor, run the contents of `schema.sql`
3. Copy your project URL and anon key from Project Settings > API

### 2. Anthropic API Key
1. Go to https://console.anthropic.com
2. Create an API key

### 3. Local Development
```bash
pip install -r requirements.txt
mkdir -p .streamlit
cp secrets.toml.template .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your actual keys
streamlit run ielts_master.py
```

### 4. Streamlit Cloud Deployment
1. Push this folder to a GitHub repository
2. Go to https://share.streamlit.io
3. Connect your repo, set main file to `ielts_master.py`
4. In app Settings > Secrets, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-..."
   SUPABASE_URL = "https://..."
   SUPABASE_ANON_KEY = "eyJ..."
   ```

## Features

| Feature | Status |
|---------|--------|
| Auth (login/signup/demo) | Ready |
| Diagnostic baseline test | Ready |
| Speaking practice (Part 1/2/3) | Ready |
| Writing Task 1 + Task 2 | Ready |
| Listening (Section 1-4) | Ready |
| Reading (Academic) | Ready |
| Vocabulary Builder | Ready |
| Score history charts | Ready |
| 21-Day Challenge + streak | Ready |
| Recurring error tracking | Ready |
| Settings (tutor/language/color) | Ready |
| Stripe subscription | Stub ready |
| Audio replay | Extend practice.py |

## Adding Stripe Subscriptions
In `modules/settings.py`, the upgrade button has a stub. To activate:
1. `pip install stripe`
2. Add `STRIPE_SECRET_KEY` and `STRIPE_PRICE_ID` to secrets
3. Implement checkout session creation in the button handler

## Language Support
Supported response languages: English, Mongolian, Kazakh, Uzbek, Kyrgyz, Tajik, Turkmen, Russian.
Mixed mode: explanations in native language, IELTS terms and examples in English.
