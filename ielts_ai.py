# -*- coding: utf-8 -*-
# ============================================================
# IELTS AI Tutor — Production Version 4.0
# Premium Bento-Grid + Glassmorphism Design System
# Built with Claude API + Streamlit
# Author: Logshir (lucode-io)
# ============================================================

import streamlit as st
import anthropic
from streamlit_mic_recorder import speech_to_text

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IELTS AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# PREMIUM BENTO-GRID + GLASSMORPHISM CSS
# ============================================================

st.markdown("""
<style>

/* ── GLOBAL BACKGROUND: Dark Gradient ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 25%, #1b1b3a 50%, #0d1b2a 75%, #0a0a1a 100%) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: #e0e0e0;
}
[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── HIDE DEFAULT SIDEBAR ── */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
button[kind="headerNoPadding"],
[data-testid="stSidebarNav"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    overflow: hidden !important;
}

/* ── MAIN CONTAINER ── */
.main .block-container {
    background: transparent !important;
    padding-top: 0.5rem;
    max-width: 1280px;
}

/* ── GLASSMORPHISM CONTAINER (Bento Card) ── */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 20px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    margin-bottom: 16px;
}

/* ── TOP NAVIGATION BAR ── */
.top-nav {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 12px 24px;
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
}
.top-nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}
.top-nav-brand-text {
    font-size: 18px;
    font-weight: 700;
    color: #F0C040;
    letter-spacing: 0.03em;
}
.top-nav-brand-sub {
    font-size: 10px;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── PILLS / BADGES ── */
.ag-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    margin-right: 6px;
    letter-spacing: 0.04em;
    backdrop-filter: blur(8px);
}
.ag-pill-mode { background: rgba(240,192,64,0.15); color: #F0C040; border: 1px solid rgba(240,192,64,0.3); }
.ag-pill-topic { background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.1); }
.ag-pill-band { background: rgba(46,204,113,0.12); color: #2ECC71; border: 1px solid rgba(46,204,113,0.25); }

/* ── GENERIC BUTTONS ── */
.stButton > button {
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 18px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100% !important;
    background: rgba(255, 255, 255, 0.06) !important;
    color: #CBD5E8 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    backdrop-filter: blur(8px) !important;
}
.stButton > button:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    color: #ffffff !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
}

/* ── GLOWING ACTION BUTTON (Start Speaking) ── */
.glow-btn-wrap .stButton > button {
    background: linear-gradient(135deg, #F0C040 0%, #E8A020 100%) !important;
    color: #0a0a1a !important;
    border: none !important;
    border-radius: 20px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    padding: 16px 28px !important;
    box-shadow: 0 0 20px rgba(240,192,64,0.4), 0 0 60px rgba(240,192,64,0.15) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    letter-spacing: 0.02em;
}
.glow-btn-wrap .stButton > button:hover {
    background: linear-gradient(135deg, #FFD060 0%, #F0C040 100%) !important;
    color: #0a0a1a !important;
    box-shadow: 0 0 30px rgba(240,192,64,0.6), 0 0 80px rgba(240,192,64,0.25) !important;
    transform: translateY(-2px) scale(1.02);
}

/* Clear chat */
button[kind="secondary"] {
    background: transparent !important;
    color: #E74C3C !important;
    border: 1px solid rgba(231,76,60,0.3) !important;
    border-radius: 14px !important;
}
button[kind="secondary"]:hover {
    background: rgba(231,76,60,0.08) !important;
    border-color: rgba(231,76,60,0.6) !important;
}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 4px 0 !important;
}
[data-testid="stChatMessage"][data-author="user"] > div:last-child {
    background: rgba(0, 123, 255, 0.08) !important;
    border-radius: 20px 20px 4px 20px !important;
    border: 1px solid rgba(0,123,255,0.15) !important;
    padding: 14px 18px !important;
    color: #e0e8f8 !important;
    margin-left: auto !important;
    max-width: 85% !important;
    backdrop-filter: blur(12px) !important;
}
[data-testid="stChatMessage"][data-author="assistant"] > div:last-child {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 20px 20px 20px 4px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    padding: 20px 24px !important;
    max-width: 95% !important;
    backdrop-filter: blur(12px) !important;
}

/* ── ASSISTANT RESPONSE TYPOGRAPHY ── */
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span {
    font-size: 15px !important;
    line-height: 1.85 !important;
    color: #dde6f0 !important;
    letter-spacing: 0.012em !important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong {
    color: #F0C040 !important;
    font-weight: 600 !important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3 {
    color: #F0C040 !important;
    font-weight: 700 !important;
    font-size: 17px !important;
    margin: 1.2rem 0 0.4rem !important;
    letter-spacing: 0.02em !important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ul,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ol {
    padding-left: 1.4rem !important;
    margin: 0.5rem 0 0.8rem !important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {
    margin-bottom: 8px !important;
    color: #dde6f0 !important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] hr {
    border-color: rgba(240,192,64,0.25) !important;
    margin: 14px 0 !important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code {
    background: rgba(240,192,64,0.1) !important;
    color: #F0C040 !important;
    padding: 2px 7px !important;
    border-radius: 6px !important;
    font-size: 13px !important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] blockquote p {
    border-left: 3px solid rgba(240,192,64,0.4) !important;
    padding-left: 14px !important;
    color: rgba(255,255,255,0.6) !important;
    font-style: italic !important;
}
/* ── CHAT INPUT ── */
[data-testid="stChatInput"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    color: #e0e0e0 !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(240, 192, 64, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(240, 192, 64, 0.1) !important;
}

/* ── SELECTBOX (glass style) ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: #e0e0e0 !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] > div > div > div {
    background: #F0C040 !important;
}

/* ── ALERTS ── */
[data-testid="stAlert"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-left: 4px solid #F0C040 !important;
    border-radius: 14px !important;
    color: #e0e0e0 !important;
    backdrop-filter: blur(8px) !important;
}

/* ── METRICS (glass) ── */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border-radius: 16px !important;
    padding: 14px 18px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(8px) !important;
}
[data-testid="stMetricValue"] { color: #F0C040 !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.4) !important; }

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.06) !important; margin: 12px 0 !important; }

/* ── EXPANDER (glass) ── */
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(8px) !important;
}

/* ── STATUS WIDGET ── */
[data-testid="stStatus"],
[data-testid="stStatusWidget"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(240, 192, 64, 0.2) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(12px) !important;
    color: #e0e0e0 !important;
}

/* ── SCORE BADGES ── */
.score-high {
    display: inline-block;
    background: rgba(46,204,113,0.12);
    color: #2ECC71;
    border: 1px solid rgba(46,204,113,0.25);
    padding: 3px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 13px;
}
.score-mid {
    display: inline-block;
    background: rgba(240,192,64,0.12);
    color: #F0C040;
    border: 1px solid rgba(240,192,64,0.25);
    padding: 3px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 13px;
}
.score-low {
    display: inline-block;
    background: rgba(231,76,60,0.12);
    color: #E74C3C;
    border: 1px solid rgba(231,76,60,0.25);
    padding: 3px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 13px;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(240,192,64,0.3); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(240,192,64,0.5); }

/* ── WELCOME CARD ── */
.welcome-card {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 40px 36px;
    text-align: center;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}
.welcome-card h2 { font-size: 22px; font-weight: 700; color: #F0C040; margin-bottom: 8px; }
.welcome-card p { font-size: 14px; color: rgba(255,255,255,0.45); line-height: 1.7; }

/* ── REF CARD (glass) ── */
.ref-card {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 16px;
    margin-bottom: 12px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}
.ref-card-speaking { border-top: 2px solid #A78BFA; }
.ref-card-writing  { border-top: 2px solid #38BDF8; }
.ref-card-reading  { border-top: 2px solid #34D399; }
.ref-card-listening{ border-top: 2px solid #FCD34D; }
.ref-card-vocab    { border-top: 2px solid #F472B6; }

/* ── MODE CHIPS ── */
.mode-guide-wrap { margin-top: 8px; margin-bottom: 10px; }
.mode-guide-chip {
    display: inline-block;
    margin: 0 5px 5px 0;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.mode-speaking  { background: rgba(167,139,250,0.12); color: #A78BFA; border: 1px solid rgba(167,139,250,0.25); }
.mode-writing   { background: rgba(56,189,248,0.10); color: #38BDF8; border: 1px solid rgba(56,189,248,0.25); }
.mode-listening { background: rgba(252,211,77,0.10); color: #FCD34D; border: 1px solid rgba(252,211,77,0.25); }
.mode-reading   { background: rgba(52,211,153,0.10); color: #34D399; border: 1px solid rgba(52,211,153,0.25); }
.mode-vocab     { background: rgba(244,114,182,0.10); color: #F472B6; border: 1px solid rgba(244,114,182,0.25); }
.mode-general   { background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.4); border: 1px solid rgba(255,255,255,0.1); }

/* ── VOICE CARD ── */
.voice-card {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 20px;
    border: 1px solid rgba(240, 192, 64, 0.15);
    padding: 16px 20px;
    margin-bottom: 14px;
    backdrop-filter: blur(12px);
}

/* ── SPINNER ── */
[data-testid="stSpinner"] { color: #F0C040 !important; }

/* ── MOBILE RESPONSIVE ── */
@media screen and (max-width: 768px) {
    .main .block-container {
        max-width: 100% !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-top: 0.5rem !important;
    }
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }
    .glass-card { border-radius: 16px; padding: 14px; }
    .top-nav { padding: 10px 16px; border-radius: 14px; }
    [data-testid="stChatMessage"][data-author="user"] > div:last-child {
        max-width: 95% !important;
        font-size: 16px !important;
    }
    [data-testid="stChatMessage"][data-author="assistant"] > div:last-child {
        max-width: 100% !important;
        padding: 12px 14px !important;
        font-size: 16px !important;
    }
    .welcome-card { padding: 24px 18px !important; }
    .welcome-card h2 { font-size: 18px !important; }
    .welcome-card p { font-size: 13px !important; }
    .ref-card { margin-top: 10px !important; }
    .ag-pill { font-size: 10px !important; padding: 3px 8px !important; }
}

@media screen and (max-width: 480px) {
    .main .block-container {
        padding-left: 0.25rem !important;
        padding-right: 0.25rem !important;
    }
    .glass-card { border-radius: 12px; padding: 10px; }
    .top-nav { border-radius: 10px; }
    .welcome-card { padding: 18px 12px !important; }
    .welcome-card div[style*="font-size:48px"] {
        font-size: 36px !important;
    }
    .mode-guide-chip {
        font-size: 9px !important;
        padding: 2px 6px !important;
    }
}

/* ── SETTINGS PANEL ── */
.settings-label {
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 6px;
    margin-top: 14px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTS
# ============================================================

MODES = [
    "Speaking — Part 1 (Personal questions)",
    "Speaking — Part 2 (Long turn / cue card)",
    "Speaking — Part 3 (Discussion)",
    "Writing — Task 1 (Graph/Chart description)",
    "Writing — Task 2 (Essay)",
    "Listening — Section 1 (Conversation)",
    "Listening — Section 2 (Monologue)",
    "Listening — Section 3 (Academic discussion)",
    "Listening — Section 4 (Academic lecture)",
    "Reading — Academic passage",
    "Vocabulary Builder",
    "General Practice"
]

TOPICS = [
    "Technology", "Environment", "Education", "Health",
    "Work and Career", "Culture and Society", "Travel",
    "Food", "Family", "Crime and Law", "Economy", "Free choice"
]

# ============================================================
# SESSION STATE
# ============================================================

def init_session_state():
    defaults = {
        "messages": [],
        "mode": MODES[0],
        "task": "General Practice",
        "essay_count": 0,
        "target_band": 7.0
        "show_settings": False,
"tutor_name": "Alex",
"response_language": "English",
"accent_color": "#F0C040",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================
# SYSTEM PROMPTS
# ============================================================

def get_system_prompt(mode, task, target_band):
    base = f"""
You are an expert IELTS examiner with 15 years of experience.
You specialize in helping Mongolian and Central Asian students reach band 7.0+.
You are honest, specific, and encouraging.

Target band: {target_band}
Current task: {task}

RULES FOR ALL MODES:
- Never inflate scores. Honest feedback only.
- Never say "great job" without a specific reason.
- Always give ONE concrete thing to improve today.
- Use simple English — student may not be advanced.
- Never switch topics unless student asks.
"""

    if "Speaking" in mode:
        part = "Part 1" if "Part 1" in mode else "Part 2" if "Part 2" in mode else "Part 3"
        return base + f"""
YOU ARE NOW: IELTS Speaking Examiner — {part}

HOW TO HANDLE SPEAKING PRACTICE:
- Ask ONE question at a time
- Wait for student answer
- Score their answer using 4 criteria
- Ask the NEXT question naturally

IMPORTANT: The student may submit text OR a voice recording.
If voice recording is provided, first transcribe what they said,
then score it exactly like a text answer.

SPEAKING SCORING CRITERIA:
1. Fluency and Coherence (FC)
2. Lexical Resource (LR)
3. Grammatical Range and Accuracy (GRA)
4. Pronunciation (P) — evaluate from spoken delivery or written text

FORMAT YOUR SPEAKING FEEDBACK EXACTLY LIKE THIS:
---
TRANSCRIPTION (if voice):
[What the student said]

IELTS SPEAKING BAND SCORES
Fluency and Coherence: X.X — [specific comment]
Lexical Resource: X.X — [specific vocabulary tip]
Grammatical Range: X.X — [specific grammar note]
Pronunciation: X.X — [note from delivery or written clues]

Overall Speaking Band: X.X to X.X

Priority Fix This Week:
[One specific thing to practice — very concrete]

Better Phrases You Could Have Used:
[2 to 3 upgraded phrases based on what they said]
---
After feedback — ask the next question naturally.
"""

    elif "Task 1" in mode:
        return base + f"""
YOU ARE NOW: IELTS Writing Task 1 Examiner

TASK 1 CONTEXT:
- The student describes a graph, chart, map, or process.
- Time limit: 20 minutes.
- Minimum word count: 150 words.

SCORING:
1. Task Achievement (TA) — Key features described, overview present ("Overall..."), specific data/numbers used, no personal opinion.
2. Coherence and Cohesion (CC)
3. Lexical Resource (LR)
4. Grammatical Range and Accuracy (GRA)

EXAMINER CHECKLIST:
- Overview must start with "Overall..."
- Specific figures/dates must be present
- No personal opinion allowed

IF USER ASKS FOR A QUESTION: Generate ONE realistic IELTS Task 1 prompt with data.

FORMAT:
---
IELTS BAND SCORES — Writing Task 1
Task Achievement: X.X — [comment]
Coherence and Cohesion: X.X — [comment]
Lexical Resource: X.X — [comment]
Grammatical Range: X.X — [comment]

Overall Band Estimate: X.X to X.X

What Worked: [2 specific things with quotes]
What To Fix: [2 improvements with rewritten examples]
Improved Version of Your Introduction: [band 7+ rewrite]
Vocabulary Upgrades: [5 upgrades]
---
"""

    elif "Task 2" in mode:
        return base + f"""
YOU ARE NOW: IELTS Writing Task 2 Examiner

SCORING:
1. Task Response (TR)
2. Coherence and Cohesion (CC)
3. Lexical Resource (LR)
4. Grammatical Range and Accuracy (GRA)

BAND 7+ REQUIRES: Clear position, 2 developed body paragraphs, counter-argument, 250+ words.

IF USER ASKS FOR A QUESTION: Generate a realistic Task 2 question.

FORMAT:
---
IELTS BAND SCORES — Writing Task 2
Task Response: X.X — [comment]
Coherence and Cohesion: X.X — [comment]
Lexical Resource: X.X — [comment]
Grammatical Range: X.X — [comment]

Overall Band Estimate: X.X to X.X

What Worked: [2 specific things]
What To Fix: [2 improvements]
Improved Version of Your Introduction: [band 7+ rewrite]
Vocabulary Upgrades: [5 upgrades]
---
"""

    elif "Listening" in mode:
        section = mode.split("—")[1].strip() if "—" in mode else "Section 1"
        return base + f"""
YOU ARE NOW: IELTS Listening Practice Generator — {section}

1. Generate realistic listening script
2. Student reads once
3. Generate 10 questions from script only
4. Student answers from memory
5. Score and explain every error

FORMAT:
LISTENING SCRIPT — Read once carefully
[script]
QUESTIONS — Answer from memory
[10 questions]
After answers: scores + explanations
"""

    elif "Reading" in mode:
        return base + f"""
YOU ARE NOW: IELTS Reading Practice Generator

1. Generate 600-800 word academic passage
2. Generate 13 mixed-type questions
3. Student answers
4. Score every answer with paragraph reference

TFNG: TRUE = text confirms | FALSE = text contradicts | NOT GIVEN = not mentioned. If in doubt — NOT GIVEN.

PASSAGE: Academic topic, paragraphs labeled A B C D.
"""

    elif "Vocabulary" in mode:
        return base + """
YOU ARE NOW: IELTS Vocabulary Coach

Teach 5 words per session.
FORMAT FOR EACH WORD:
WORD: [word]
Definition: [simple]
IELTS example: [sentence]
Collocations: [2-3]
Band level: [B2/C1/C2]
Topic: [IELTS topic]

After teaching — quiz the student.
"""

    else:
        return base + """
YOU ARE NOW: Personal IELTS Tutor
Help the student with whatever they need.
"""

# ============================================================
# CLAUDE API
# ============================================================

def chat_with_claude(messages, mode, task, target_band, api_key):
    client = anthropic.Anthropic(api_key=api_key)

    clean_messages = []
    for msg in messages:
        clean_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        system=get_system_prompt(mode, task, target_band),
        messages=clean_messages
    )
    return response.content[0].text

# ============================================================
# HELPER
# ============================================================

def start_session(mode, starter_message):
    st.session_state.mode = mode
    st.session_state.messages = [{"role": "user", "content": starter_message}]
    st.rerun()

# ============================================================
# TOP NAVIGATION BAR (replaces sidebar)
# ============================================================

st.markdown("""
<div class="top-nav">
    <div class="top-nav-brand">
        <svg width="32" height="32" viewBox="0 0 56 56" fill="none">
            <rect width="56" height="56" rx="14" fill="rgba(255,255,255,0.06)"/>
            <polygon points="28,14 46,24 28,34 10,24" fill="rgba(255,255,255,0.08)" stroke="#F0C040" stroke-width="2" stroke-linejoin="round"/>
            <line x1="40" y1="27" x2="40" y2="38" stroke="#F0C040" stroke-width="2" stroke-linecap="round"/>
            <path d="M34,38 Q40,42 46,38" fill="none" stroke="#F0C040" stroke-width="2" stroke-linecap="round"/>
            <circle cx="43" cy="13" r="1.5" fill="#F0C040"/>
            <line x1="43" y1="13" x2="47" y2="9" stroke="#F0C040" stroke-width="1.2" stroke-linecap="round"/>
            <line x1="43" y1="13" x2="48" y2="14" stroke="#F0C040" stroke-width="1.2" stroke-linecap="round"/>
            <line x1="43" y1="13" x2="42" y2="8" stroke="#F0C040" stroke-width="1.2" stroke-linecap="round"/>
        </svg>
        <div>
            <div class="top-nav-brand-text">IELTS AI Tutor</div>
            <div class="top-nav-brand-sub">Powered by Claude</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Navigation Controls Row
nav_c1, nav_c2, nav_c3, nav_c4 = st.columns([3, 2, 1, 1])

with nav_c1:
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "") or st.text_input(
        "Claude API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Get your key at console.anthropic.com",
        label_visibility="collapsed"
    )

with nav_c2:
    mode = st.selectbox("Mode", MODES,
        index=MODES.index(st.session_state.mode) if st.session_state.mode in MODES else 0,
        label_visibility="collapsed")
    st.session_state.mode = mode

with nav_c3:
    topic = st.selectbox("Topic", TOPICS, label_visibility="collapsed")

with nav_c4:
    target_band = st.selectbox(
        "Band",
        options=[5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0],
        index=[5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0].index(st.session_state.target_band),
        label_visibility="collapsed"
    )
    st.session_state.target_band = target_band
    st.session_state.task = f"Topic: {topic} | Target: Band {target_band}"

mode_color = (
    "mode-speaking" if "Speaking" in mode else
    "mode-writing" if "Writing" in mode else
    "mode-listening" if "Listening" in mode else
    "mode-reading" if "Reading" in mode else
    "mode-vocab" if "Vocabulary" in mode else
    "mode-general"
)

# ============================================================
# BENTO GRID: MAIN LAYOUT
# ============================================================

main_col, side_col = st.columns([3, 1])

# ── CHAT CONTAINER (Glass Card) ──
with main_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    # Pill bar
    st.markdown(f"""
    <div style="margin-bottom:14px">
        <span class="ag-pill ag-pill-mode">{mode.split("—")[0].strip()}</span>
        <span class="ag-pill ag-pill-topic">{topic}</span>
        <span class="ag-pill ag-pill-band">Band {target_band}</span>
        <span class="mode-guide-chip {mode_color}" style="float:right">{mode}</span>
    </div>
    """, unsafe_allow_html=True)

    # Welcome state
    if not st.session_state.messages:
        welcome_data = {
            "Speaking": ("🎤", "Speaking Practice", "Record your voice or type your answers. Claude scores each answer with detailed band feedback."),
            "Task 1": ("📊", "Writing Task 1", "20 minutes. Minimum 150 words. Ask for a question or paste your own essay for scoring."),
            "Task 2": ("✍️", "Writing Task 2", "40 minutes. Minimum 250 words. Ask for a question or paste your own essay for scoring."),
            "Listening": ("🎧", "Listening Practice", "Claude generates a realistic script. Read it once only. Then answer questions from memory."),
            "Reading": ("📖", "Reading Practice", "Claude generates an academic passage and 13 questions. 20 minutes. When in doubt — NOT GIVEN."),
            "Vocabulary": ("📚", "Vocabulary Builder", "5 new words per session. Quiz after each set. Target: 450 words retained by June exam.")
        }
        icon, title, desc = next(
            ((v[0], v[1], v[2]) for k, v in welcome_data.items() if k in mode),
            ("🎓", "Welcome", "Select your practice mode and click a Quick Start button to begin.")
        )
        st.markdown(f"""
        <div class="welcome-card">
            <div style="font-size:48px;margin-bottom:12px">{icon}</div>
            <h2>{title} Active</h2>
            <p>{desc}</p>
            <p style="margin-top:16px;font-size:13px;color:rgba(255,255,255,0.25)">
                Use the Quick Start panel on the right to begin instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Message history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.markdown('</div>', unsafe_allow_html=True)

# ── SCORECARD / QUICK START PANEL (Glass Card) ──
with side_col:

    # Session Stats Bento Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-weight:700;font-size:13px;color:#F0C040;margin-bottom:12px;letter-spacing:0.04em;text-transform:uppercase">
        Session Stats
    </div>
    """, unsafe_allow_html=True)
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Msgs", user_msgs)
    with s2:
        st.metric("Target", f"{target_band}")
    with s3:
        st.metric("Essays", st.session_state.essay_count)
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick Start Bento Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-weight:700;font-size:13px;color:#F0C040;margin-bottom:12px;letter-spacing:0.04em;text-transform:uppercase">
        Quick Start
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🎤 Speaking", expanded=False):
        if st.button("Part 1 — Personal", key="task_spk_p1", use_container_width=True):
            start_session(
                "Speaking — Part 1 (Personal questions)",
                f"Please start my IELTS Speaking Part 1 practice. Ask me the first question about {topic}."
            )
        if st.button("Part 2 — Cue Card", key="task_spk_p2", use_container_width=True):
            start_session(
                "Speaking — Part 2 (Long turn / cue card)",
                f"Please start my IELTS Speaking Part 2 practice. Ask me a cue card question about {topic}."
            )
        if st.button("Part 3 — Discussion", key="task_spk_p3", use_container_width=True):
            start_session(
                "Speaking — Part 3 (Discussion)",
                f"Please start my IELTS Speaking Part 3 practice. Ask me a discussion question about {topic}."
            )

    with st.expander("✍️ Writing", expanded=False):
        if st.button("Task 1 Question", key="task_w_t1_q", use_container_width=True):
            start_session(
                "Writing — Task 1 (Graph/Chart description)",
                f"Give me an IELTS Writing Task 1 question about {topic}. Make it realistic like Cambridge books."
            )
        if st.button("Submit Task 1", key="task_w_t1_s", use_container_width=True):
            start_session(
                "Writing — Task 1 (Graph/Chart description)",
                "I want to submit my IELTS Writing Task 1 essay for scoring. Please wait for me to paste it."
            )
        if st.button("Task 2 Question", key="task_w_t2_q", use_container_width=True):
            start_session(
                "Writing — Task 2 (Essay)",
                f"Give me a realistic IELTS Writing Task 2 question about {topic}."
            )
        if st.button("Submit Task 2", key="task_w_t2_s", use_container_width=True):
            start_session(
                "Writing — Task 2 (Essay)",
                "I want to submit my IELTS Writing Task 2 essay for scoring. Please wait for me to paste it."
            )

    with st.expander("🎧 Listening", expanded=False):
        for i, (sec, sec_mode) in enumerate([
            ("Section 1", "Listening — Section 1 (Conversation)"),
            ("Section 2", "Listening — Section 2 (Monologue)"),
            ("Section 3", "Listening — Section 3 (Academic discussion)"),
            ("Section 4", "Listening — Section 4 (Academic lecture)")
        ]):
            if st.button(f"Start {sec}", key=f"task_ls_s{i+1}", use_container_width=True):
                start_session(sec_mode, f"Give me an IELTS {sec} practice about {topic}. Generate the script and 10 questions.")

    with st.expander("📖 Reading", expanded=False):
        if st.button("Academic Reading", key="task_rd_ac", use_container_width=True):
            start_session(
                "Reading — Academic passage",
                f"Give me an IELTS Academic Reading passage about {topic} with 13 mixed questions."
            )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.essay_count = 0
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Reference Tips Bento Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    ref_data = {
        "Speaking": ("speaking", "🎤 Speaking Tips", [
            "Extend every answer — aim for 3-4 sentences",
            "Use linking words: furthermore, however",
            "Avoid fillers: maybe, actually, you know",
            "Part 2: speak for 2 full minutes",
            "Part 3: give opinions with reasons"
        ], "Band 7 needs: wide vocabulary, complex sentences, fluent delivery"),

        "Task 1": ("writing", "📊 Task 1 Formula", [
            "Para 1: Paraphrase the question",
            "Para 2: Overview — start with Overall",
            "Para 3: Key detail with numbers",
            "Para 4: Comparison or contrast"
        ], "Must have: specific numbers, no opinion, 150+ words"),

        "Task 2": ("writing", "✍️ Task 2 Formula", [
            "Para 1: Introduction + clear position",
            "Para 2: Main argument + example",
            "Para 3: Second argument + example",
            "Para 4: Counter + refute",
            "Para 5: Conclusion"
        ], "Must have: clear position, real examples, 250+ words"),

        "Listening": ("listening", "🎧 Listening Strategy", [
            "Read ALL questions before audio",
            "Predict the answer type",
            "Listen for keywords not sentences",
            "Check spelling carefully",
            "One play only — never pause"
        ], "Common errors: missing plurals, wrong spelling, extra words"),

        "Reading": ("reading", "📖 TFNG Rules", [
            "TRUE = text clearly confirms it",
            "FALSE = text clearly contradicts it",
            "NOT GIVEN = not mentioned at all",
            "If unsure — always NOT GIVEN",
            "2 minutes maximum per question"
        ], "Strategy: read questions first, scan keywords, never get stuck"),

        "Vocabulary": ("vocab", "📚 Vocab System", [
            "5 new words every session",
            "Review previous 5 first",
            "Use each in one sentence aloud",
            "Learn collocations not just words",
            "Target: 450 new words by June"
        ], "B2 to C1: use rare words, collocations, avoid repetition")
    }

    matched = None
    for k, v in ref_data.items():
        if k in mode:
            matched = v
            break

    if matched:
        card_class, title, tips, footer = matched
        tips_html = "".join([f"<li style='margin-bottom:6px;color:rgba(255,255,255,0.65);font-size:13px'>{t}</li>" for t in tips])
        st.markdown(f"""
        <div class="ref-card ref-card-{card_class}">
            <div style="font-weight:700;font-size:13px;color:#F0C040;margin-bottom:10px">{title}</div>
            <ul style="margin:0;padding-left:16px">{tips_html}</ul>
            <div style="margin-top:10px;font-size:11px;color:rgba(255,255,255,0.3);border-top:1px solid rgba(255,255,255,0.06);padding-top:8px">{footer}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ref-card" style="border-top:2px solid #F0C040">
            <div style="font-weight:700;font-size:13px;color:#F0C040;margin-bottom:10px">IELTS Band Scale</div>
            <ul style="margin:0;padding-left:16px">
                <li style="margin-bottom:6px;color:rgba(255,255,255,0.65);font-size:13px">Band 9 — Expert user</li>
                <li style="margin-bottom:6px;color:rgba(255,255,255,0.65);font-size:13px">Band 8 — Very good user</li>
                <li style="margin-bottom:6px;color:rgba(255,255,255,0.65);font-size:13px">Band 7 — Good user</li>
                <li style="margin-bottom:6px;color:rgba(255,255,255,0.65);font-size:13px">Band 6 — Competent user</li>
                <li style="margin-bottom:6px;color:rgba(255,255,255,0.65);font-size:13px">Band 5 — Modest user</li>
            </ul>
            <div style="margin-top:10px;font-size:11px;color:rgba(255,255,255,0.3);border-top:1px solid rgba(255,255,255,0.06);padding-top:8px">Target: 7.0+ — all 4 skills matter equally</div>
        </div>
        """, unsafe_allow_html=True)

    # Band Progression mini-card
    st.markdown("""
    <div style="background:rgba(255,255,255,0.03);border-radius:16px;border:1px solid rgba(255,255,255,0.06);
                padding:14px;margin-top:10px;backdrop-filter:blur(8px)">
        <div style="font-weight:700;font-size:12px;color:#F0C040;margin-bottom:8px;letter-spacing:0.04em;text-transform:uppercase">
            Band Progression
        </div>
        <div style="font-size:12px;color:rgba(255,255,255,0.35);line-height:1.9">
            Baseline: <strong style="color:#E74C3C">A2</strong><br>
            March target: <strong style="color:#F0C040">5.5+</strong><br>
            May target: <strong style="color:#F0C040">6.5+</strong><br>
            June exam: <strong style="color:#2ECC71">6.0-6.5</strong><br>
            August target: <strong style="color:#2ECC71">7.0+</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# VOICE INPUT + CHAT INPUT
# ============================================================

needs_response = (
    st.session_state.messages and
    st.session_state.messages[-1]["role"] == "user"
)

if "Speaking" in st.session_state.mode:
    with main_col:
        st.markdown("""
        <div class="voice-card">
            <div style="font-weight:700;font-size:13px;color:#F0C040;margin-bottom:4px">
                Voice Recording
            </div>
            <div style="font-size:12px;color:rgba(255,255,255,0.35);margin-bottom:8px">
                Click Start — speak your answer — click Stop.
                Speech is converted to text and graded instantly.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Glowing action button wrapper
        st.markdown('<div class="glow-btn-wrap">', unsafe_allow_html=True)
        voice_text = speech_to_text(
            language='en',
            start_prompt="🎤 Start Speaking",
            stop_prompt="⏹️ Stop Recording",
            just_once=True,
            use_container_width=True,
            key='stt_speaking'
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if voice_text:
            st.toast("Recording started...", icon="🎙️")
            st.session_state.messages.append({
                "role": "user",
                "content": f"[Voice answer]: {voice_text}"
            })
            needs_response = True
            st.rerun()

        st.markdown("""
        <div style="text-align:center;font-size:11px;color:rgba(255,255,255,0.25);margin:8px 0;letter-spacing:0.04em">
            — or type your answer below —
        </div>
        """, unsafe_allow_html=True)

user_input = st.chat_input("Type your answer, essay, or question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    needs_response = True

if needs_response:
    if not api_key:
        st.error("Please enter your Claude API key in the top navigation bar.\n\nGet your free key at: console.anthropic.com")
        st.stop()

    with main_col:
        with st.chat_message("user"):
            st.markdown(st.session_state.messages[-1]["content"])

        with st.chat_message("assistant"):
            with st.status("Evaluating your English...", expanded=True) as status:
                try:
                    response = chat_with_claude(
                        messages=st.session_state.messages,
                        mode=st.session_state.mode,
                        task=st.session_state.task,
                        target_band=st.session_state.target_band,
                        api_key=api_key
                    )
                    st.markdown(response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                    status.update(label="Analysis complete!", state="complete", expanded=False)
                    st.toast("Analysis complete!", icon="✅")
                    if "Task" in st.session_state.mode and len(st.session_state.messages[-2]["content"]) > 100:
                        st.session_state.essay_count += 1

                except anthropic.AuthenticationError:
                    status.update(label="Authentication failed", state="error", expanded=False)
                    st.error("Invalid API key. Check your key at console.anthropic.com")
                except anthropic.RateLimitError:
                    status.update(label="Rate limited", state="error", expanded=False)
                    st.error("Rate limit hit. Wait 30 seconds and try again.")
                except Exception as e:
                    status.update(label="Error occurred", state="error", expanded=False)
                    st.error(f"Something went wrong: {str(e)}")
