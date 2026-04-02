# -*- coding: utf-8 -*-
# ============================================================
# IELTS AI Tutor - Production Version 3.0
# Light Antigravity Design System
# Built with Claude API + Streamlit
# Author: Logshir (lucode-io)
# ============================================================

import streamlit as st
import anthropic
import base64
from st_audiorecorder import st_audiorecorder

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IELTS AI Tutor",
 -page_icon="🎓",
 -layout="wide",
 -initial_sidebar_state="expanded"
)

# ============================================================
# LIGHT ANTIGRAVITY CSS
# ============================================================

st.markdown("""
<style>

/* ── BASE ── */
html, body, [data-testid="stAppViewContainer"] {
 -background: #F4F4F8 !important;
 -font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Subtle dot grid background */
[data-testid="stAppViewContainer"]::before {
 -content: '';
 -position: fixed;
 -inset: 0;
 -background-image: radial-gradient(rgba(99,102,241,0.07) 1px, transparent 1px);
 -background-size: 24px 24px;
 -pointer-events: none;
 -z-index: 0;
}

/* Center glow */
[data-testid="stAppViewContainer"]::after {
 -content: '';
 -position: fixed;
 -top: 30%;
 -left: 50%;
 -transform: translate(-50%, -50%);
 -width: 600px;
 -height: 400px;
 -background: radial-gradient(ellipse, rgba(99,102,241,0.04) 0%, transparent 70%);
 -pointer-events: none;
 -z-index: 0;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
 -background: #FAFAFA !important;
 -border-right: 1px solid #F3F4F6 !important;
 -box-shadow: 2px 0 20px rgba(99,102,241,0.06) !important;
}

[data-testid="stSidebar"] > div {
 -padding-top: 1.5rem;
}

/* ── MAIN CONTENT ── */
.main .block-container {
 -background: transparent;
 -padding-top: 1rem;
 -max-width: 900px;
}

/* ── CARDS ── */
.ag-card {
 -background: #FFFFFF;
 -border-radius: 16px;
 -border: 1px solid #F3F4F6;
 -padding: 20px 24px;
 -margin-bottom: 16px;
 -box-shadow:
 --- 0 1px 3px rgba(0,0,0,0.06),
 --- 0 4px 16px rgba(99,102,241,0.08),
 --- 0 12px 40px rgba(99,102,241,0.05);
 -transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.ag-card:hover {
 -box-shadow:
 --- 0 2px 8px rgba(0,0,0,0.08),
 --- 0 8px 32px rgba(99,102,241,0.15),
 --- 0 20px 60px rgba(99,102,241,0.08);
 -transform: translateY(-2px);
}

/* ── APP TITLE ── */
.ag-title {
 -font-size: 26px;
 -font-weight: 700;
 -color: #0F0F1A;
 -letter-spacing: -0.5px;
 -margin-bottom: 2px;
}

.ag-caption {
 -font-size: 13px;
 -color: #9CA3AF;
 -margin-bottom: 20px;
}

/* ── PILLS ── */
.ag-pill {
 -display: inline-block;
 -padding: 3px 10px;
 -border-radius: 20px;
 -font-size: 12px;
 -font-weight: 600;
 -margin-right: 6px;
}

.ag-pill-mode {
 -background: linear-gradient(135deg, #6366F1, #8B5CF6);
 -color: #FFFFFF;
}

.ag-pill-topic {
 -background: #F3F4F6;
 -color: #374151;
}

.ag-pill-band {
 -background: linear-gradient(135deg, #10B981, #06B6D4);
 -color: #FFFFFF;
}

/* ── SIDEBAR BUTTONS - QUICK START ── */
.stButton > button {
 -border-radius: 10px !important;
 -font-weight: 600 !important;
 -font-size: 14px !important;
 -padding: 10px 16px !important;
 -transition: all 0.2s ease !important;
 -border: none !important;
 -width: 100% !important;
}

/* Speaking button */
div[data-testid="column"]:nth-of-type(1) .stButton:nth-of-type(1) > button {
 -background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
 -color: #FFFFFF !important;
 -box-shadow: 0 2px 8px rgba(99,102,241,0.30), 0 4px 16px rgba(99,102,241,0.15) !important;
}

div[data-testid="column"]:nth-of-type(1) .stButton:nth-of-type(1) > button:hover {
 -box-shadow: 0 4px 16px rgba(99,102,241,0.50), 0 8px 32px rgba(99,102,241,0.25) !important;
 -transform: translateY(-2px) !important;
}

/* Reading button */
div[data-testid="column"]:nth-of-type(1) .stButton:nth-of-type(2) > button {
 -background: linear-gradient(135deg, #10B981, #06B6D4) !important;
 -color: #FFFFFF !important;
 -box-shadow: 0 2px 8px rgba(16,185,129,0.30), 0 4px 16px rgba(16,185,129,0.15) !important;
}

div[data-testid="column"]:nth-of-type(1) .stButton:nth-of-type(2) > button:hover {
 -box-shadow: 0 4px 16px rgba(16,185,129,0.50), 0 8px 32px rgba(16,185,129,0.25) !important;
 -transform: translateY(-2px) !important;
}

/* Writing button */
div[data-testid="column"]:nth-of-type(2) .stButton:nth-of-type(1) > button {
 -background: linear-gradient(135deg, #0EA5E9, #6366F1) !important;
 -color: #FFFFFF !important;
 -box-shadow: 0 2px 8px rgba(14,165,233,0.30), 0 4px 16px rgba(14,165,233,0.15) !important;
}

div[data-testid="column"]:nth-of-type(2) .stButton:nth-of-type(1) > button:hover {
 -box-shadow: 0 4px 16px rgba(14,165,233,0.50), 0 8px 32px rgba(14,165,233,0.25) !important;
 -transform: translateY(-2px) !important;
}

/* Listening button */
div[data-testid="column"]:nth-of-type(2) .stButton:nth-of-type(2) > button {
 -background: linear-gradient(135deg, #F59E0B, #EF4444) !important;
 -color: #FFFFFF !important;
 -box-shadow: 0 2px 8px rgba(245,158,11,0.30), 0 4px 16px rgba(245,158,11,0.15) !important;
}

div[data-testid="column"]:nth-of-type(2) .stButton:nth-of-type(2) > button:hover {
 -box-shadow: 0 4px 16px rgba(245,158,11,0.50), 0 8px 32px rgba(245,158,11,0.25) !important;
 -transform: translateY(-2px) !important;
}

/* Clear Chat button */
button[kind="secondary"] {
 -background: #FFFFFF !important;
 -color: #EF4444 !important;
 -border: 1px solid #FCA5A5 !important;
 -box-shadow: 0 1px 4px rgba(239,68,68,0.10) !important;
}

button[kind="secondary"]:hover {
 -box-shadow: 0 2px 12px rgba(239,68,68,0.20) !important;
 -transform: translateY(-1px) !important;
}

/* Mode specific action buttons */
.stButton > button[data-testid*="start"],
.stButton > button[data-testid*="give"],
.stButton > button[data-testid*="submit"] {
 -background: #FFFFFF !important;
 -color: #0F0F1A !important;
 -border: 1px solid #E5E7EB !important;
 -box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 2px 8px rgba(99,102,241,0.06) !important;
}

.stButton > button[data-testid*="start"]:hover,
.stButton > button[data-testid*="give"]:hover,
.stButton > button[data-testid*="submit"]:hover {
 -box-shadow: 0 2px 12px rgba(99,102,241,0.15) !important;
 -transform: translateY(-1px) !important;
 -border-color: #C7D2FE !important;
}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {
 -background: transparent !important;
 -border: none !important;
 -padding: 4px 0 !important;
}

/* User messages */
[data-testid="stChatMessage"][data-author="user"] > div:last-child {
 -background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
 -border-radius: 18px 18px 4px 18px !important;
 -padding: 12px 16px !important;
 -color: #FFFFFF !important;
 -box-shadow: 0 4px 16px rgba(99,102,241,0.25) !important;
 -margin-left: auto !important;
 -max-width: 85% !important;
}

/* Assistant messages */
[data-testid="stChatMessage"][data-author="assistant"] > div:last-child {
 -background: #FFFFFF !important;
 -border-radius: 18px 18px 18px 4px !important;
 -padding: 14px 18px !important;
 -border: 1px solid #F3F4F6 !important;
 -border-left: 3px solid #6366F1 !important;
 -box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
 -max-width: 95% !important;
}

/* ── CHAT INPUT ── */
[data-testid="stChatInput"] {
 -background: #FFFFFF !important;
 -border: 1px solid #E5E7EB !important;
 -border-radius: 14px !important;
 -box-shadow:
 --- 0 2px 8px rgba(0,0,0,0.06),
 --- 0 4px 16px rgba(99,102,241,0.08) !important;
 -padding: 4px 8px !important;
}

[data-testid="stChatInput"]:focus-within {
 -border-color: #6366F1 !important;
 -box-shadow:
 --- 0 0 0 3px rgba(99,102,241,0.12),
 --- 0 4px 16px rgba(99,102,241,0.15) !important;
}

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
 -background: #FFFFFF !important;
 -border: 1px solid #E5E7EB !important;
 -border-radius: 8px !important;
 -box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] > div > div > div {
 -background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
}

/* ── INFO BOXES ── */
[data-testid="stAlert"] {
 -background: #FFFFFF !important;
 -border: 1px solid #E0E7FF !important;
 -border-left: 4px solid #6366F1 !important;
 -border-radius: 10px !important;
 -box-shadow: 0 2px 12px rgba(99,102,241,0.08) !important;
 -color: #1E1B4B !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
 -background: #FFFFFF !important;
 -border-radius: 10px !important;
 -padding: 12px 16px !important;
 -border: 1px solid #F3F4F6 !important;
 -border-top: 3px solid #6366F1 !important;
 -box-shadow: 0 2px 8px rgba(99,102,241,0.08) !important;
}

[data-testid="stMetricValue"] {
 -color: #0F0F1A !important;
 -font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
 -color: #6B7280 !important;
}

/* ── DIVIDER ── */
hr {
 -border-color: #F3F4F6 !important;
 -margin: 12px 0 !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
 -background: #FFFFFF !important;
 -border: 1px solid #F3F4F6 !important;
 -border-radius: 10px !important;
 -box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}

/* ── SIDEBAR TITLES ── */
[data-testid="stSidebar"] h1 {
 -font-size: 20px !important;
 -font-weight: 700 !important;
 -color: #0F0F1A !important;
 -letter-spacing: -0.3px !important;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
 -font-size: 13px !important;
 -font-weight: 600 !important;
 -color: #6B7280 !important;
 -text-transform: uppercase !important;
 -letter-spacing: 0.06em !important;
}

/* ── SCORE BADGES ── */
.score-high {
 -display: inline-block;
 -background: linear-gradient(135deg, #10B981, #06B6D4);
 -color: #FFFFFF;
 -padding: 2px 10px;
 -border-radius: 20px;
 -font-weight: 700;
 -font-size: 13px;
 -box-shadow: 0 2px 8px rgba(16,185,129,0.30);
}

.score-mid {
 -display: inline-block;
 -background: linear-gradient(135deg, #F59E0B, #EF4444);
 -color: #FFFFFF;
 -padding: 2px 10px;
 -border-radius: 20px;
 -font-weight: 700;
 -font-size: 13px;
 -box-shadow: 0 2px 8px rgba(245,158,11,0.30);
}

.score-low {
 -display: inline-block;
 -background: linear-gradient(135deg, #EF4444, #DC2626);
 -color: #FFFFFF;
 -padding: 2px 10px;
 -border-radius: 20px;
 -font-weight: 700;
 -font-size: 13px;
 -box-shadow: 0 2px 8px rgba(239,68,68,0.30);
}

/* ── SPINNER ── */
[data-testid="stSpinner"] {
 -color: #6366F1 !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F4F4F8; }
::-webkit-scrollbar-thumb {
 -background: linear-gradient(#6366F1, #8B5CF6);
 -border-radius: 3px;
}

/* ── WELCOME CARD ── */
.welcome-card {
 -background: #FFFFFF;
 -border-radius: 20px;
 -border: 1px solid #F3F4F6;
 -padding: 32px;
 -text-align: center;
 -box-shadow:
 --- 0 1px 3px rgba(0,0,0,0.06),
 --- 0 8px 32px rgba(99,102,241,0.10),
 --- 0 20px 60px rgba(99,102,241,0.06);
}

.welcome-card h2 {
 -font-size: 22px;
 -font-weight: 700;
 -color: #0F0F1A;
 -margin-bottom: 8px;
}

.welcome-card p {
 -font-size: 15px;
 -color: #6B7280;
 -line-height: 1.6;
}

/* ── REFERENCE CARD ── */
.ref-card {
 -background: #FFFFFF;
 -border-radius: 12px;
 -border: 1px solid #F3F4F6;
 -border-top: 3px solid;
 -padding: 16px;
 -margin-bottom: 12px;
 -box-shadow: 0 2px 12px rgba(99,102,241,0.08);
}

.ref-card-speaking { border-top-color: #8B5CF6; }
.ref-card-writing - { border-top-color: #0EA5E9; }
.ref-card-reading - { border-top-color: #10B981; }
.ref-card-listening{ border-top-color: #F59E0B; }
.ref-card-vocab -{ border-top-color: #EC4899; }

/* Practice mode color guide */
.mode-guide-wrap {
 -margin-top: 8px;
 -margin-bottom: 10px;
}
.mode-guide-chip {
 -display: inline-block;
 -margin: 0 6px 6px 0;
 -padding: 4px 10px;
 -border-radius: 999px;
 -font-size: 11px;
 -font-weight: 700;
 -color: #111827;
}
.mode-speaking - { background: #EDE9FE; border: 1px solid #C4B5FD; }
.mode-writing - - { background: #E0F2FE; border: 1px solid #93C5FD; }
.mode-listening { background: #FEF3C7; border: 1px solid #FCD34D; }
.mode-reading - - { background: #DCFCE7; border: 1px solid #86EFAC; }
.mode-vocab -- { background: #FCE7F3; border: 1px solid #F9A8D4; }
.mode-general - - { background: #E5E7EB; border: 1px solid #CBD5E1; }

</style>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTS
# ============================================================

MODES = [
 -"Speaking - Part 1 (Personal questions)",
 -"Speaking - Part 2 (Long turn / cue card)",
 -"Speaking - Part 3 (Discussion)",
 -"Writing - Task 1 (Graph/Chart description)",
 -"Writing - Task 2 (Essay)",
 -"Listening - Section 1 (Conversation)",
 -"Listening - Section 2 (Monologue)",
 -"Listening - Section 3 (Academic discussion)",
 -"Listening - Section 4 (Academic lecture)",
 -"Reading - Academic passage",
 -"Vocabulary Builder",
 -"General Practice"
]

TOPICS = [
 -"Technology", "Environment", "Education", "Health",
 -"Work and Career", "Culture and Society", "Travel",
 -"Food", "Family", "Crime and Law", "Economy", "Free choice"
]

# ============================================================
# SESSION STATE
# ============================================================

def init_session_state():
 -defaults = {
 --- "messages": [],
 --- "mode": MODES[0],
 --- "task": "General Practice",
 --- "essay_count": 0,
 --- "target_band": 7.0
 -}
 -for key, value in defaults.items():
 --- if key not in st.session_state:
 ---- - st.session_state[key] = value

init_session_state()

# ============================================================
# SYSTEM PROMPTS
# ============================================================

def get_system_prompt(mode, task, target_band):
 -base = f"""
You are an expert IELTS examiner with 15 years of experience.
You specialize in helping Mongolian and Central Asian students reach band 7.0+.
You are honest, specific, and encouraging.

Target band: {target_band}
Current task: {task}

RULES FOR ALL MODES:
- Never inflate scores. Honest feedback only.
- Never say "great job" without a specific reason.
- Always give ONE concrete thing to improve today.
- Use simple English - student may not be advanced.
- Never switch topics unless student asks.
"""

 -if "Speaking" in mode:
 --- part = "Part 1" if "Part 1" in mode else "Part 2" if "Part 2" in mode else "Part 3"
 --- return base + f"""
YOU ARE NOW: IELTS Speaking Examiner - {part}

HOW TO HANDLE SPEAKING PRACTICE:
- Ask ONE question at a time
- Wait for student answer
- Score their answer using 4 criteria
- Ask the NEXT question naturally

SPEAKING SCORING CRITERIA:
1. Fluency and Coherence (FC)
2. Lexical Resource (LR)
3. Grammatical Range and Accuracy (GRA)
4. Pronunciation (P) - evaluate from written text

FORMAT YOUR SPEAKING FEEDBACK EXACTLY LIKE THIS:
---
IELTS SPEAKING BAND SCORES
Fluency and Coherence: X.X - [specific comment]
Lexical Resource: X.X - [specific vocabulary tip]
Grammatical Range: X.X - [specific grammar note]
Pronunciation: X.X - [note from written clues]

Overall Speaking Band: X.X to X.X

Priority Fix This Week:
[One specific thing to practice - very concrete]

Better Phrases You Could Have Used:
[2 to 3 upgraded phrases based on what they said]
---
After feedback - ask the next question naturally.
"""

 -elif "Task 1" in mode:
 --- return base + f"""
YOU ARE NOW: IELTS Writing Task 1 Examiner

TASK 1 CONTEXT:
- The student describes a graph, chart, map, or process.
- Time limit: 20 minutes.
- Minimum word count: 150 words.

SCORING (ONLY TASK ACHIEVEMENT - NOT TASK RESPONSE):
1. Task Achievement (TA) - Key features described, overview present ("Overall..."), specific data/numbers used, and no personal opinion.
2. Coherence and Cohesion (CC) - Logical paragraphing and progression.
3. Lexical Resource (LR) - Vocabulary for describing data and stages.
4. Grammatical Range and Accuracy (GRA) - Variety and accuracy.

EXAMINER CHECKLIST (USE THIS WHEN SCORING):
- Overview: Does the essay include a separate overview paragraph that starts with "Overall..." (case-insensitive)? If missing or not starting with "Overall...", lower TA.
- Specific data/numbers: Are there specific figures/dates (not just general statements)? If numbers are missing or too vague, lower TA.
- No personal opinion: Detect and penalize personal viewpoints or recommendations (for example: "I think", "in my opinion", "we should", "it is better"). Task 1 should describe facts only; use objective language.

IF USER ASKS FOR A QUESTION:
Generate ONE realistic IELTS Writing Task 1 prompt (graph/chart/table/pie chart/map/process) with realistic numbers/data. If it is a chart/process, ensure the key trends are describable.

FORMAT YOUR TASK 1 FEEDBACK EXACTLY LIKE THIS:
---
IELTS BAND SCORES - Writing Task 1
Task Achievement: X.X - [does the overview exist starting with "Overall..."? are key features covered with specific data/numbers? is there any personal opinion?]
Coherence and Cohesion: X.X - [paragraph structure and flow]
Lexical Resource: X.X - [data-description vocabulary accuracy/range]
Grammatical Range: X.X - [grammar accuracy and variety]

Overall Band Estimate: X.X to X.X

What Worked:
[2 specific things with quotes from their essay]

What To Fix:
[2 specific improvements with rewritten examples]

Improved Version of Your Introduction:
[Rewrite their introduction at band 7+ level]

Vocabulary Upgrades:
[5 word or phrase upgrades from their essay]
---
"""

 -elif "Task 2" in mode:
 --- return base + f"""
YOU ARE NOW: IELTS Writing Task 2 Examiner

TASK 2 SCORING CRITERIA:
1. Task Response (TR) - All parts answered? Position clear?
2. Coherence and Cohesion (CC) - Essay structure and flow?
3. Lexical Resource (LR) - Vocabulary range and accuracy?
4. Grammatical Range and Accuracy (GRA)

BAND 7+ TASK 2 REQUIRES:
- Clear position in introduction
- 2 fully developed body paragraphs with examples
- Counter-argument addressed and refuted properly
- Consistent position throughout
- Minimum 250 words

IF USER ASKS FOR A QUESTION:
Generate a realistic Task 2 question - opinion, discussion, problem-solution, or two-part style.

FORMAT YOUR TASK 2 FEEDBACK EXACTLY LIKE THIS:
---
IELTS BAND SCORES - Writing Task 2
Task Response: X.X - [all parts answered fully?]
Coherence and Cohesion: X.X - [structure comment]
Lexical Resource: X.X - [vocabulary range comment]
Grammatical Range: X.X - [grammar accuracy comment]

Overall Band Estimate: X.X to X.X

What Worked:
[2 specific things with quotes from their essay]

What To Fix:
[2 specific improvements with rewritten examples]

Improved Version of Your Introduction:
[Rewrite their introduction at band 7+ level]

Vocabulary Upgrades:
[5 word or phrase upgrades from their essay]
---
"""

 -elif "Listening" in mode:
 --- section = mode.split("")[1].strip() if "" in mode else "Section 1"
 --- return base + f"""
YOU ARE NOW: IELTS Listening Practice Generator - {section}

HOW LISTENING PRACTICE WORKS:
1. Generate a realistic listening script for {section}
2. Student reads it carefully once (simulates listening once)
3. Generate 10 questions based only on the script
4. Student answers from memory
5. Score and explain every error

QUESTION TYPES TO USE:
- Form or note completion (write exact words - 1 to 3 words)
- Multiple choice (A, B, or C)
- Matching
- Short answer (maximum 3 words)

IMPORTANT RULES:
- Answers must come ONLY from the script
- Note completion answers should be 1 to 3 words only
- Multiple choice must have 3 clear options

FORMAT:
1. Show script labeled LISTENING SCRIPT - Read once carefully
2. Tell student to answer questions without looking back
3. Show questions labeled QUESTIONS - Answer from memory
4. After answers - show scores and explain each error
"""

 -elif "Reading" in mode:
 --- return base + f"""
YOU ARE NOW: IELTS Reading Practice Generator

HOW READING PRACTICE WORKS:
1. Generate a realistic academic passage - 600 to 800 words
2. Generate 13 questions of mixed types
3. Student answers all questions
4. Score every answer and explain each error

QUESTION TYPES TO INCLUDE:
- True False Not Given (most important)
- Yes No Not Given
- Matching headings to paragraphs
- Multiple choice
- Short answer (3 words maximum)
- Sentence completion

TFNG STRICT RULES:
TRUE = passage clearly and directly confirms it
FALSE = passage clearly and directly contradicts it
NOT GIVEN = passage does not mention it at all
If in doubt - NOT GIVEN. Never guess TRUE or FALSE.

PASSAGE REQUIREMENTS:
- Academic topic - science, history, society, technology
- Realistic Cambridge IELTS style
- Include specific facts, numbers, and names
- Paragraphs labeled A, B, C, D

FORMAT:
1. Show passage with labeled paragraphs
2. Show all 13 questions
3. After student answers - score each one
4. Explain every wrong answer with paragraph reference
5. Identify which question type they struggle with most
"""

 -elif "Vocabulary" in mode:
 --- return base + f"""
YOU ARE NOW: IELTS Vocabulary Coach

HOW VOCABULARY SESSIONS WORK:
1. Teach 5 words per session connected to IELTS topics
2. Test student on previous words first
3. Give definition plus example plus collocations
4. Quiz the student at the end

FORMAT FOR EACH WORD:
WORD: [word]
Definition: [simple clear definition]
IELTS example: [natural sentence using this word]
Collocations: [2 to 3 common word combinations]
Band level: [B2 or C1 or C2]
Topic: [which IELTS topic this helps]

After teaching - quiz the student:
Use [word] in your own sentence about [topic].
Give specific feedback on their sentence.
"""

 -else:
 --- return base + """
YOU ARE NOW: Personal IELTS Tutor

Help the student with whatever they need.
Answer questions about IELTS format, scoring, strategies.
Give vocabulary tips. Explain grammar rules.
Encourage them. Point them toward the right practice mode.
"""

# ============================================================
# CLAUDE API
# ============================================================

def chat_with_claude(messages, mode, task, target_band, api_key):
 -client = anthropic.Anthropic(api_key=api_key)

 -anthropic_messages = []
 -for msg in messages:
 --- content_blocks = []
 --- if "audio" in msg and msg["audio"] is not None:
 ---- - audio_data_base64 = base64.b64encode(msg["audio"]).decode("utf-8")
 ---- - content_blocks.append({
 -----"type": "audio",
 -----"source": {
 ------- "type": "base64",
 ------- "media_type": "audio/wav",
 ------- "data": audio_data_base64
 -----}
 ---- - })
 ---- - # Also include a text part to prompt the model about the audio
 ---- - content_blocks.append({"type": "text", "text": "The user has provided an audio response. Please transcribe it and then grade it based on IELTS Speaking criteria (Fluency and Coherence, Lexical Resource, Grammatical Range and Accuracy, Pronunciation). Then ask the next question naturally."})
 --- 
 --- if "content" in msg and msg["content"] is not None and msg["content"] != "(Audio response)":
 ---- - content_blocks.append({"type": "text", "text": msg["content"]})

 --- # If content_blocks is empty, it means only audio was present and handled, or it was an empty message.
 --- # For cases where only text was provided, or if it's the initial message without audio.
 --- if not content_blocks and "content" in msg and msg["content"] is not None:
 ---- - anthropic_messages.append({"role": msg["role"], "content": msg["content"]})
 --- elif content_blocks:
 ---- - anthropic_messages.append({"role": msg["role"], "content": content_blocks})

 -response = client.messages.create(
 --- model="claude-sonnet-4-5",
 --- max_tokens=2048,
 --- system=get_system_prompt(mode, task, target_band),
 --- messages=anthropic_messages
 -)
 -return response.content[0].text

# ============================================================
# HELPER
# ============================================================

def start_session(mode, starter_message):
 -st.session_state.mode = mode
 -st.session_state.messages = [{"role": "user", "content": starter_message}]
 -st.rerun()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
 -st.title("🎓 IELTS AI Tutor")
 -st.caption("Powered by Claude AI")

 -api_key = st.secrets.get("ANTHROPIC_API_KEY", "") or st.text_input(
 --- "Claude API Key",
 --- type="password",
 --- placeholder="sk-ant-...",
 --- help="Get your key at console.anthropic.com"
 -)

 -st.divider()

 -st.subheader("⚙️ User Custom Settings")
 -mode = st.selectbox("Practice mode:", MODES,
 --- index=MODES.index(st.session_state.mode) if st.session_state.mode in MODES else 0)
 -st.session_state.mode = mode
 -mode_color = (
 --- "mode-speaking" if "Speaking" in mode else
 --- "mode-writing" if "Writing" in mode else
 --- "mode-listening" if "Listening" in mode else
 --- "mode-reading" if "Reading" in mode else
 --- "mode-vocab" if "Vocabulary" in mode else
 --- "mode-general"
 -)
 -st.markdown(
 --- """
 --- <div class="mode-guide-wrap">
 ---- - <span class="mode-guide-chip mode-speaking">Speaking</span>
 ---- - <span class="mode-guide-chip mode-writing">Writing</span>
 ---- - <span class="mode-guide-chip mode-listening">Listening</span>
 ---- - <span class="mode-guide-chip mode-reading">Reading</span>
 ---- - <span class="mode-guide-chip mode-vocab">Vocabulary Builder</span>
 ---- - <span class="mode-guide-chip mode-general">General Practice</span>
 --- </div>
 --- """,
 --- unsafe_allow_html=True
 -)
 -st.markdown(
 --- f'<span class="mode-guide-chip {mode_color}">Current: {mode}</span>',
 --- unsafe_allow_html=True
 -)

 -topic = st.selectbox("Topic:", TOPICS)

 -target_band = st.slider(
 --- "Target band score:",
 --- min_value=5.0, max_value=9.0, value=st.session_state.target_band, step=0.5
 -)
 -st.session_state.target_band = target_band
 -st.session_state.task = f"Topic: {topic} | Target: Band {target_band}"

 -if st.button("🗑️ Clear Chat", use_container_width=True):
 --- st.session_state.messages = []
 --- st.session_state.essay_count = 0
 --- st.rerun()

 -st.divider()

 -st.subheader("🎯 Skills Tasks")

 -with st.expander("🎤 Speaking Tasks", expanded=True):
 --- if st.button("Start Speaking Part 1", use_container_width=True):
 ---- - start_session(
 -----"Speaking - Part 1 (Personal questions)",
 -----f"Please start my IELTS Speaking Part 1 practice. Ask me the first question about {topic}."
 ---- - )
 --- if st.button("Start Speaking Part 2", use_container_width=True):
 ---- - start_session(
 -----"Speaking - Part 2 (Long turn / cue card)",
 -----f"Please start my IELTS Speaking Part 2 practice. Ask me a cue card question about {topic}."
 ---- - )
 --- if st.button("Start Speaking Part 3", use_container_width=True):
 ---- - start_session(
 -----"Speaking - Part 3 (Discussion)",
 -----f"Please start my IELTS Speaking Part 3 practice. Ask me a discussion question about {topic}."
 ---- - )

 -with st.expander("✍️ Writing Tasks", expanded=True):
 --- if st.button("Get Task 1 question", use_container_width=True):
 ---- - start_session(
 -----"Writing - Task 1 (Graph/Chart description)",
 -----f"Give me an IELTS Writing Task 1 question about {topic}. Make it realistic like Cambridge books."
 ---- - )
 --- if st.button("Submit Task 1 essay", use_container_width=True):
 ---- - start_session(
 -----"Writing - Task 1 (Graph/Chart description)",
 -----"I want to submit my IELTS Writing Task 1 essay for scoring. Please wait for me to paste it."
 ---- - )
 --- if st.button("Get Task 2 question", use_container_width=True):
 ---- - start_session(
 -----"Writing - Task 2 (Essay)",
 -----f"Give me a realistic IELTS Writing Task 2 question about {topic}."
 ---- - )
 --- if st.button("Submit Task 2 essay", use_container_width=True):
 ---- - start_session(
 -----"Writing - Task 2 (Essay)",
 -----"I want to submit my IELTS Writing Task 2 essay for scoring. Please wait for me to paste it."
 ---- - )

 -with st.expander("🎧 Listening Tasks", expanded=True):
 --- if st.button("Start Listening Section 1", use_container_width=True):
 ---- - start_session(
 -----"Listening - Section 1 (Conversation)",
 -----f"Give me an IELTS Listening Section 1 practice about {topic}. Generate the script and 10 questions."
 ---- - )
 --- if st.button("Start Listening Section 2", use_container_width=True):
 ---- - start_session(
 -----"Listening - Section 2 (Monologue)",
 -----f"Give me an IELTS Listening Section 2 practice about {topic}. Generate the script and 10 questions."
 ---- - )
 --- if st.button("Start Listening Section 3", use_container_width=True):
 ---- - start_session(
 -----"Listening - Section 3 (Academic discussion)",
 -----f"Give me an IELTS Listening Section 3 practice about {topic}. Generate the script and 10 questions."
 ---- - )
 --- if st.button("Start Listening Section 4", use_container_width=True):
 ---- - start_session(
 -----"Listening - Section 4 (Academic lecture)",
 -----f"Give me an IELTS Listening Section 4 practice about {topic}. Generate the script and 10 questions."
 ---- - )

 -with st.expander("📖 Reading Tasks", expanded=True):
 --- if st.button("Start Academic Reading", use_container_width=True):
 ---- - start_session(
 -----"Reading - Academic passage",
 -----f"Give me an IELTS Academic Reading passage about {topic} with 13 mixed questions."
 ---- - )

 -st.divider()

 -# Session stats
 -st.subheader("Session Stats")
 -user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
 -c1, c2, c3 = st.columns(3)
 -with c1:
 --- st.metric("Messages", user_msgs)
 -with c2:
 --- st.metric("Target", f"{target_band}")
 -with c3:
 --- st.metric("Essays", st.session_state.essay_count)

# ============================================================
# MAIN LAYOUT
# ============================================================

main_col, ref_col = st.columns([3, 1])

with main_col:

 -# Header
 -st.markdown(f"""
 -<div class="ag-title">🎓 IELTS AI Tutor</div>
 -<div class="ag-caption">
 --- <span class="ag-pill ag-pill-mode">{mode.split("")[0].strip()}</span>
 --- <span class="ag-pill ag-pill-topic">{topic}</span>
 --- <span class="ag-pill ag-pill-band">Band {target_band}</span>
 -</div>
 -""", unsafe_allow_html=True)

 -# Welcome screen
 -if not st.session_state.messages:
 --- welcome_data = {
 ---- - "Speaking": ("🎤", "Speaking Practice", "Type your answers as if speaking. Claude asks questions one at a time and scores each answer with detailed feedback."),
 ---- - "Task 1": ("📊", "Writing Task 1", "20 minutes. Minimum 150 words. Ask for a question or paste your own essay for scoring."),
 ---- - "Task 2": ("✍️", "Writing Task 2", "40 minutes. Minimum 250 words. Ask for a question or paste your own essay for scoring."),
 ---- - "Listening": ("🎧", "Listening Practice", "Claude generates a realistic script. Read it once only. Then answer questions from memory."),
 ---- - "Reading": ("📖", "Reading Practice", "Claude generates an academic passage and 13 questions. 20 minutes. When in doubt - NOT GIVEN."),
 ---- - "Vocabulary": ("📚", "Vocabulary Builder", "5 new words per session. Quiz after each set. Target: 450 words retained by June exam.")
 --- }
 --- icon, title, desc = next(
 ---- - ((v[0], v[1], v[2]) for k, v in welcome_data.items() if k in mode),
 ---- - ("🎓", "Welcome", "Select your practice mode and click a Quick Start button to begin.")
 --- )
 --- st.markdown(f"""
 --- <div class="welcome-card">
 ---- - <div style="font-size:48px;margin-bottom:12px">{icon}</div>
 ---- - <h2>{title} Active</h2>
 ---- - <p>{desc}</p>
 ---- - <p style="margin-top:16px;font-size:13px;color:#9CA3AF">
 -----Click a Quick Start button in the sidebar to begin instantly.
 ---- - </p>
 --- </div>
 --- """, unsafe_allow_html=True)

 -# Chat history
 -for message in st.session_state.messages:
 --- with st.chat_message(message["role"]):
 ---- - if "audio" in message and message["audio"] is not None:
 -----st.audio(message["audio"], format="audio/wav")
 -----st.markdown(message["content"])
 ---- - else:
 -----st.markdown(message["content"])

# ============================================================
# REFERENCE PANEL
# ============================================================

with ref_col:

 -ref_data = {
 --- "Speaking": ("speaking", "🎤 Speaking Tips", [
 ---- - "Extend every answer - aim for 3-4 sentences",
 ---- - "Use linking words: furthermore, however",
 ---- - "Avoid fillers: maybe, actually, you know",
 ---- - "Part 2: speak for 2 full minutes",
 ---- - "Part 3: give opinions with reasons"
 --- ], "Band 7 needs: wide vocabulary, complex sentences, fluent delivery"),

 --- "Task 1": ("writing", "📊 Task 1 Formula", [
 ---- - "Para 1: Paraphrase the question",
 ---- - "Para 2: Overview - start with Overall",
 ---- - "Para 3: Key detail with numbers",
 ---- - "Para 4: Comparison or contrast"
 --- ], "Must have: specific numbers, no opinion, 150+ words"),

 --- "Task 2": ("writing", "✍️ Task 2 Formula", [
 ---- - "Para 1: Introduction + clear position",
 ---- - "Para 2: Main argument + example",
 ---- - "Para 3: Second argument + example",
 ---- - "Para 4: Counter + refute",
 ---- - "Para 5: Conclusion"
 --- ], "Must have: clear position, real examples, 250+ words"),

 --- "Listening": ("listening", "🎧 Listening Strategy", [
 ---- - "Read ALL questions before audio",
 ---- - "Predict the answer type",
 ---- - "Listen for keywords not sentences",
 ---- - "Check spelling carefully",
 ---- - "One play only - never pause"
 --- ], "Common errors: missing plurals, wrong spelling, extra words"),

 --- "Reading": ("reading", "📖 TFNG Rules", [
 ---- - "TRUE = text clearly confirms it",
 ---- - "FALSE = text clearly contradicts it",
 ---- - "NOT GIVEN = not mentioned at all",
 ---- - "If unsure - always NOT GIVEN",
 ---- - "2 minutes maximum per question"
 --- ], "Strategy: read questions first, scan keywords, never get stuck"),

 --- "Vocabulary": ("vocab", "📚 Vocab System", [
 ---- - "5 new words every session",
 ---- - "Review previous 5 first",
 ---- - "Use each in one sentence aloud",
 ---- - "Learn collocations not just words",
 ---- - "Target: 450 new words by June"
 --- ], "B2 to C1: use rare words, collocations, avoid repetition")
 -}

 -matched = None
 -for k, v in ref_data.items():
 --- if k in mode:
 ---- - matched = v
 ---- - break

 -if matched:
 --- card_class, title, tips, footer = matched
 --- tips_html = "".join([f"<li style='margin-bottom:6px;color:#374151;font-size:13px'>{t}</li>" for t in tips])
 --- st.markdown(f"""
 --- <div class="ref-card ref-card-{card_class}">
 ---- - <div style="font-weight:700;font-size:14px;color:#0F0F1A;margin-bottom:10px">{title}</div>
 ---- - <ul style="margin:0;padding-left:16px">{tips_html}</ul>
 ---- - <div style="margin-top:10px;font-size:12px;color:#6B7280;border-top:1px solid #F3F4F6;padding-top:8px">{footer}</div>
 --- </div>
 --- """, unsafe_allow_html=True)
 -else:
 --- st.markdown("""
 --- <div class="ref-card" style="border-top-color:#6366F1">
 ---- - <div style="font-weight:700;font-size:14px;color:#0F0F1A;margin-bottom:10px">📋 IELTS Band Scale</div>
 ---- - <ul style="margin:0;padding-left:16px">
 -----<li style="margin-bottom:6px;color:#374151;font-size:13px">Band 9: Expert user</li>
 -----<li style="margin-bottom:6px;color:#374151;font-size:13px">Band 8: Very good user</li>
 -----<li style="margin-bottom:6px;color:#374151;font-size:13px">Band 7: Good user</li>
 -----<li style="margin-bottom:6px;color:#374151;font-size:13px">Band 6: Competent user</li>
 -----<li style="margin-bottom:6px;color:#374151;font-size:13px">Band 5: Modest user</li>
 ---- - </ul>
 ---- - <div style="margin-top:10px;font-size:12px;color:#6B7280;border-top:1px solid #F3F4F6;padding-top:8px">Your target: 7.0+ - all 4 skills matter equally</div>
 --- </div>
 --- """, unsafe_allow_html=True)

 -# Minimal progress tracker
 -st.markdown("""
 -<div style="background:#FFFFFF;border-radius:10px;border:1px solid #F3F4F6;
 -----border-top:3px solid #6366F1;padding:14px;
 -----box-shadow:0 2px 8px rgba(99,102,241,0.08);margin-top:12px">
 --- <div style="font-weight:700;font-size:13px;color:#0F0F1A;margin-bottom:8px">
 ---- - 📈 Band Progression
 --- </div>
 --- <div style="font-size:12px;color:#6B7280;line-height:1.8">
 ---- - Baseline: <strong style="color:#EF4444">A2</strong><br>
 ---- - March target: <strong style="color:#F59E0B">5.5+</strong><br>
 ---- - May target: <strong style="color:#F59E0B">6.5+</strong><br>
 ---- - June exam: <strong style="color:#10B981">6.0-6.5</strong><br>
 ---- - August target: <strong style="color:#10B981">7.0+</strong>
 --- </div>
 -</div>
 -""", unsafe_allow_html=True)

# ============================================================
# CHAT INPUT AND RESPONSE
# ============================================================

needs_response = (
 -st.session_state.messages and
 -st.session_state.messages[-1]["role"] == "user"
)

audio_bytes = None
user_input = None

if "Speaking" in st.session_state.mode:
 -st.markdown("### Record your response")
 -audio_bytes = st_audiorecorder()
 -if audio_bytes:
 --- st.session_state.messages.append({"role": "user", "content": "(Audio response)", "audio": audio_bytes})
 --- needs_response = True
else:
 -user_input = st.chat_input("Type your answer, essay, or question here...")
 -if user_input:
 --- st.session_state.messages.append({"role": "user", "content": user_input})
 --- needs_response = True

if needs_response:
 -if not api_key:
 --- st.error("Please enter your Claude API key in Settings.\n\nGet your free key at: console.anthropic.com")
 --- st.stop()

 -with main_col:
 --- with st.chat_message("user"):
 ---- - st.markdown(st.session_state.messages[-1]["content"])

 --- with st.chat_message("assistant"):
 ---- - with st.spinner("Evaluating your English..."):
 -----try:
 ------- response = chat_with_claude(
 -------- - messages=st.session_state.messages,
 -------- - mode=st.session_state.mode,
 -------- - task=st.session_state.task,
 -------- - target_bnd=st.session_state.target_band,
 -------- - api_key=api_key
 ------- )
 ------- st.markdown(response)
 ------- st.session_state.messages.append({
 -------- - "role": "assistant",
 -------- - "content": response
 ------- })
 ------- if "Task" in st.session_state.mode and len(st.session_state.messages[-2]["content"]) > 100:
 -------- - st.session_state.essay_count += 1

 -----except anthropic.AuthenticationError:
 ------- st.error("Invalid API key. Check your key at console.anthropic.com")
 -----except anthropic.RateLimitError:
 ------- st.error("Rate limit hit. Wait 30 seconds and try again.")
 -----except Exception as e:
 ------- st.error(f"Something went wrong: {str(e)}")
