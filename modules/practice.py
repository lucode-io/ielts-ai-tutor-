# ============================================================
# modules/practice.py
# Core practice engine — timer, mic, 3-color annotations
# ============================================================

import streamlit as st
import time
from datetime import datetime
from utils.ai import (
    chat, speaking_prompt, writing_task1_prompt, writing_task2_prompt,
    listening_prompt, reading_prompt, vocabulary_prompt, diagnostic_prompt
)
from utils.database import (
    create_session, update_session, save_message, save_band_score
)
try:
    from streamlit_mic_recorder import speech_to_text
    HAS_MIC_RECORDER = True
except ImportError:
    HAS_MIC_RECORDER = False

MODES = [
    "Speaking - Part 1 (Personal questions)",
    "Speaking - Part 2 (Long turn / cue card)",
    "Speaking - Part 3 (Discussion)",
    "Writing - Task 1 (Graph/Chart description)",
    "Writing - Task 2 (Essay)",
    "Listening - Section 1 (Conversation)",
    "Listening - Section 2 (Monologue)",
    "Listening - Section 3 (Academic discussion)",
    "Listening - Section 4 (Academic lecture)",
    "Reading - Academic passage",
    "Vocabulary Builder",
    "General Practice"
]

TOPICS = [
    "Technology", "Environment", "Education", "Health",
    "Work and Career", "Culture and Society", "Travel",
    "Food", "Family", "Crime and Law", "Economy", "Free choice"
]

MODE_TIMERS = {
    "Speaking - Part 2": 120,
    "Writing - Task 1": 1200,
    "Writing - Task 2": 2400,
    "Reading": 1200,
}


def _get_timer_seconds(mode):
    for key, secs in MODE_TIMERS.items():
        if key in mode:
            return secs
    return None


def _render_practice_timer(mode):
    timer_secs = _get_timer_seconds(mode)
    if timer_secs is None:
        return

    timer_key = f"practice_timer_{mode}"
    if timer_key not in st.session_state:
        st.session_state[timer_key] = time.time()

    elapsed = time.time() - st.session_state[timer_key]
    remaining = max(0, timer_secs - int(elapsed))
    mins = remaining // 60
    secs = remaining % 60
    pct = (remaining / timer_secs) * 100

    if remaining <= 120:
        bar_color = "#E74C3C"
        text_color = "#E74C3C"
    elif remaining <= 300:
        bar_color = "#F0C040"
        text_color = "#F0C040"
    else:
        bar_color = "#4A9EFF"
        text_color = "#4A9EFF"

    if "Task 1" in mode:
        label = "WRITING TASK 1"
    elif "Task 2" in mode:
        label = "WRITING TASK 2"
    elif "Part 2" in mode:
        label = "SPEAKING PART 2"
    elif "Reading" in mode:
        label = "READING"
    else:
        label = mode.split("-")[0].strip().upper()

    st.markdown(f"""
    <div style="background:rgba(74,158,255,0.04);border:1px solid rgba(74,158,255,0.1);
                border-radius:12px;padding:12px 16px;margin-bottom:16px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
            <div style="font-size:11px;color:rgba(180,210,255,0.45);text-transform:uppercase;
                        letter-spacing:0.06em">{label}</div>
            <div style="font-size:11px;color:rgba(180,210,255,0.35)">{pct:.0f}% left</div>
        </div>
        <div style="display:flex;align-items:center;gap:12px">
            <div style="font-size:28px;font-weight:800;color:{text_color};font-family:monospace;
                        min-width:80px">{mins:02d}:{secs:02d}</div>
            <div style="flex:1;height:6px;background:rgba(74,158,255,0.08);border-radius:3px;overflow:hidden">
                <div style="width:{pct}%;height:100%;background:{bar_color};border-radius:3px;
                            transition:width 1s linear"></div>
            </div>
        </div>
        {'<div style="font-size:11px;color:#E74C3C;margin-top:6px;font-weight:600">Less than 2 minutes remaining!</div>' if remaining <= 120 and remaining > 0 else ''}
        {'<div style="font-size:13px;color:#E74C3C;margin-top:6px;font-weight:700">Time is up!</div>' if remaining == 0 else ''}
    </div>
    """, unsafe_allow_html=True)


def get_system_prompt(mode, profile):
    if "Speaking" in mode:
        part = "Part 1" if "Part 1" in mode else "Part 2" if "Part 2" in mode else "Part 3"
        return speaking_prompt(profile, part)
    elif "Task 1" in mode:
        return writing_task1_prompt(profile)
    elif "Task 2" in mode:
        return writing_task2_prompt(profile)
    elif "Listening" in mode:
        section = mode.split("-")[1].strip() if "-" in mode else "Section 1"
        return listening_prompt(profile, section)
    elif "Reading" in mode:
        return reading_prompt(profile)
    elif "Vocabulary" in mode:
        return vocabulary_prompt(profile)
    elif mode == "Diagnostic":
        return diagnostic_prompt()
    else:
        from utils.ai import build_base_prompt
        return build_base_prompt(profile) + "\nYOU ARE: Personal IELTS Tutor. Help with whatever the student needs."


def render_annotation(text):
    import re

    # Try multiple patterns — Claude outputs annotations inconsistently
    patterns = [
        # Pattern 1: emoji + [RED/BLUE/GREEN ...]: content
        r'(\U0001f534|\U0001f535|\U0001f7e2)\s*(?:\[?(?:RED|BLUE|GREEN)[^\]]*\]?[:\s\u2014\u2013-]*)(.*?)(?=(?:\n\s*(?:\U0001f534|\U0001f535|\U0001f7e2))|$)',
        # Pattern 2: emoji + Band Killer/Upgrade/Success: content
        r'(\U0001f534|\U0001f535|\U0001f7e2)\s*(?:Band Killer|Band 8 Upgrade|Strategic Success)[:\s\u2014\u2013-]*(.*?)(?=(?:\n\s*(?:\U0001f534|\U0001f535|\U0001f7e2))|$)',
        # Pattern 3: emoji + any content
        r'(\U0001f534|\U0001f535|\U0001f7e2)\s*(.*?)(?=(?:\n\s*(?:\U0001f534|\U0001f535|\U0001f7e2))|$)',
        # Pattern 4: **RED/BLUE/GREEN**: content (no emoji)
        r'\*\*(RED|BLUE|GREEN)[^*]*\*\*[:\s\u2014\u2013-]*(.*?)(?=(?:\n\s*\*\*(?:RED|BLUE|GREEN))|$)',
    ]

    matches = []
    for pattern in patterns:
        matches = list(re.finditer(pattern, text, flags=re.DOTALL))
        if matches and any(m.group(2).strip() for m in matches):
            break

    if not matches or not any(m.group(2).strip() for m in matches):
        st.markdown(text)
        return

    pre_text = text[:matches[0].start()].strip()
    post_text = text[matches[-1].end():].strip()

    if pre_text:
        st.markdown(pre_text)

    color_map = {
        '\U0001f534': {'bg': 'rgba(231,76,60,0.18)', 'border': '#E74C3C'},
        '\U0001f535': {'bg': 'rgba(56,189,248,0.18)', 'border': '#38BDF8'},
        '\U0001f7e2': {'bg': 'rgba(46,204,113,0.18)', 'border': '#2ECC71'},
        'RED': {'bg': 'rgba(231,76,60,0.18)', 'border': '#E74C3C'},
        'BLUE': {'bg': 'rgba(56,189,248,0.18)', 'border': '#38BDF8'},
        'GREEN': {'bg': 'rgba(46,204,113,0.18)', 'border': '#2ECC71'},
    }

    html = '<div style="background:rgba(255,255,255,0.03);border-radius:14px;padding:20px;margin:16px 0;border:1px solid rgba(74,158,255,0.08)">'
    html += '<div style="font-size:12px;font-weight:700;color:#4A9EFF;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:14px">3-COLOR ANNOTATION</div>'

    for match in matches:
        key = match.group(1)
        content = match.group(2).strip()
        if not content:
            continue
        c = color_map.get(key, color_map['\U0001f534'])

        # Try to extract quoted text (ASCII-safe regex)
        quote_match = re.search(r'"(.+?)"', content)
        if not quote_match:
            quote_match = re.search(r"'(.+?)'", content)
        if quote_match:
            quoted = quote_match.group(1)
            rest = content[quote_match.end():].strip()
            rest = re.sub(r'^[\u2192\u25ba\-\u2014\u2013:\s]+', '', rest)
            html += f'<div style="margin-bottom:14px"><span style="background:{c["bg"]};border-bottom:2px solid {c["border"]};padding:3px 6px;border-radius:3px;font-size:14px;color:#f0f4ff;line-height:2;display:inline">{quoted}</span>'
            if rest:
                html += f'<div style="font-size:12px;color:rgba(180,210,255,0.6);margin-top:4px;padding-left:4px">{rest}</div>'
            html += '</div>'
        else:
            # No quotes — show first sentence as highlight, rest as explanation
            parts = re.split(r'[\u2192\u25ba\u2014\u2013]', content, maxsplit=1)
            highlight = parts[0].strip()[:150]
            explanation = parts[1].strip() if len(parts) > 1 else ""
            html += f'<div style="margin-bottom:14px"><span style="background:{c["bg"]};border-bottom:2px solid {c["border"]};padding:3px 6px;border-radius:3px;font-size:14px;color:#f0f4ff;line-height:2;display:inline">{highlight}</span>'
            if explanation:
                html += f'<div style="font-size:12px;color:rgba(180,210,255,0.6);margin-top:4px;padding-left:4px">{explanation}</div>'
            html += '</div>'

    html += '''<div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:16px;padding-top:12px;border-top:1px solid rgba(74,158,255,0.08)">
        <span style="display:flex;align-items:center;gap:6px;font-size:11px;color:rgba(180,210,255,0.5)"><span style="width:8px;height:8px;border-radius:2px;background:#E74C3C;display:inline-block"></span>Band Killer</span>
        <span style="display:flex;align-items:center;gap:6px;font-size:11px;color:rgba(180,210,255,0.5)"><span style="width:8px;height:8px;border-radius:2px;background:#38BDF8;display:inline-block"></span>Band 8 Upgrade</span>
        <span style="display:flex;align-items:center;gap:6px;font-size:11px;color:rgba(180,210,255,0.5)"><span style="width:8px;height:8px;border-radius:2px;background:#2ECC71;display:inline-block"></span>Strategic Success</span>
    </div></div>'''
    st.markdown(html, unsafe_allow_html=True)

    if post_text:
        st.markdown(post_text)


def render_practice():
    profile = st.session_state.get("profile", {})
    accent = profile.get("accent_color", "#4A9EFF")
    tutor_name = profile.get("tutor_name", "Alex")
    user_id = st.session_state.get("user_id", "demo")

    # ── TIER LIMITS ──
    TIER_LIMITS = {
        "free":      {"sessions": 3,  "calls": 1,  "skills": ["Speaking", "Writing", "Reading", "Listening", "Vocabulary"]},
        "starter":   {"sessions": 5,  "calls": 3,  "skills": ["Speaking", "Writing", "Vocabulary"]},
        "pro":       {"sessions": 8,  "calls": 4,  "skills": ["Speaking", "Writing", "Reading", "Listening", "Vocabulary"]},
        "intensive": {"sessions": 10, "calls": 2,  "skills": ["Speaking", "Writing", "Reading", "Listening", "Vocabulary"]},
        "lifetime":  {"sessions": 6,  "calls": 2,  "skills": ["Speaking", "Writing", "Reading", "Listening", "Vocabulary"]},
    }
    tier = profile.get("subscription_status", "free")
    limits = TIER_LIMITS.get(tier, TIER_LIMITS["free"])

    # Check daily session limit
    if user_id != "demo":
        from utils.database import get_daily_session_count
        daily_sessions = get_daily_session_count(user_id)
        if daily_sessions >= limits["sessions"]:
            st.markdown(f"""
            <div style="text-align:center;padding:40px 20px">
                <div style="font-size:40px;margin-bottom:12px">⏰</div>
                <div style="font-size:18px;font-weight:700;color:#f0f4ff;margin-bottom:8px">Daily session limit reached</div>
                <div style="font-size:14px;color:rgba(180,210,255,0.5)">
                    Your <strong style="color:#4A9EFF">{tier.title()}</strong> plan allows {limits["sessions"]} sessions/day.
                    You've used {daily_sessions} today. Come back tomorrow or upgrade for more.
                </div>
            </div>
            """, unsafe_allow_html=True)
            return

    # Track calls per session
    call_key = "session_call_count"
    if call_key not in st.session_state:
        st.session_state[call_key] = 0

    # ── CONTROLS ──
    # Filter modes based on tier
    allowed_skills = limits["skills"]
    available_modes = [m for m in MODES if any(s in m for s in allowed_skills)]
    if not available_modes:
        available_modes = MODES[:2]  # fallback to Speaking + Writing

    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([3, 2, 1, 1])
    with ctrl_col1:
        mode = st.selectbox("Mode", available_modes,
            index=available_modes.index(st.session_state.get("practice_mode", available_modes[0]))
                  if st.session_state.get("practice_mode") in available_modes else 0,
            label_visibility="collapsed", key="practice_mode_select")
        st.session_state.practice_mode = mode
        if "Listening" in mode:
            st.session_state.practice_mode = available_modes[0]
            st.session_state.current_view = "listening"
            st.rerun()
    with ctrl_col2:
        topic = st.selectbox("Topic", TOPICS, label_visibility="collapsed", key="practice_topic")
    with ctrl_col3:
        target_band = st.selectbox("Band", [5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0],
            index=[5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0].index(float(profile.get("target_band",7.0))),
            label_visibility="collapsed", key="practice_band")
    with ctrl_col4:
        if st.button("🗑️ Clear", use_container_width=True, key="clear_chat"):
            for key in list(st.session_state.keys()):
                if key.startswith("practice_timer_"):
                    del st.session_state[key]
            st.session_state.practice_messages = []
            st.session_state.current_session_id = None
            st.rerun()

    # ── TIMER ──
    _render_practice_timer(mode)

    # ── MODE PILLS ──
    mode_color = (
        "#A78BFA" if "Speaking" in mode else "#38BDF8" if "Writing" in mode else
        "#FCD34D" if "Listening" in mode else "#34D399" if "Reading" in mode else
        "#F472B6" if "Vocabulary" in mode else "rgba(255,255,255,0.4)")
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;flex-wrap:wrap">
        <span class="pill pill-gold">{mode.split("-")[0].strip()}</span>
        <span class="pill" style="background:rgba(255,255,255,0.06);color:rgba(255,255,255,0.5);border:1px solid rgba(255,255,255,0.1)">{topic}</span>
        <span class="pill pill-green">Band {target_band}</span>
        <span style="margin-left:auto;font-size:11px;font-weight:600;color:{mode_color};background:{mode_color}18;padding:4px 10px;border-radius:20px;border:1px solid {mode_color}44">{mode}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── FEEDBACK MODE TOGGLE ──
    if "feedback_mode" not in st.session_state:
        st.session_state.feedback_mode = profile.get("feedback_mode", "detailed")

    fb_col1, fb_col2 = st.columns([1, 3])
    with fb_col1:
        current_fb = st.session_state.feedback_mode
        btn_label = "\U0001f3af Detailed Feedback" if current_fb == "basic" else "\U0001f4dd Basic Feedback"
        if st.button(btn_label, key="toggle_feedback_mode", use_container_width=True):
            st.session_state.feedback_mode = "basic" if current_fb == "detailed" else "detailed"
            # Update profile so AI prompt picks it up
            if "profile" in st.session_state:
                st.session_state.profile["feedback_mode"] = st.session_state.feedback_mode
            st.rerun()
    with fb_col2:
        fb_mode = st.session_state.feedback_mode
        if fb_mode == "detailed":
            st.markdown("""<div style="font-size:12px;color:rgba(180,210,255,0.5);padding-top:8px">
                Feedback mode: <strong style="color:#4A9EFF">Detailed</strong> — 3-color annotation + fluency gap analysis active
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="font-size:12px;color:rgba(180,210,255,0.5);padding-top:8px">
                Feedback mode: <strong style="color:rgba(180,210,255,0.7)">Basic</strong> — band score + general feedback
            </div>""", unsafe_allow_html=True)

    # ── CHAT MESSAGES (ChatGPT-style separated bubbles) ──
    messages = st.session_state.get("practice_messages", [])

    # Inject chat styling — clear separation between user/AI
    st.markdown("""
    <style>
    [data-testid="stChatMessage"][data-author="user"] {
        background: rgba(74,158,255,0.06) !important;
        border: 1px solid rgba(74,158,255,0.12) !important;
        border-radius: 16px 16px 4px 16px !important;
        padding: 16px 20px !important;
        margin: 12px 0 12px 15% !important;
        max-width: 85% !important;
        margin-left: auto !important;
    }
    [data-testid="stChatMessage"][data-author="assistant"] {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(74,158,255,0.06) !important;
        border-radius: 16px 16px 16px 4px !important;
        padding: 20px 24px !important;
        margin: 12px 15% 12px 0 !important;
        max-width: 85% !important;
    }
    /* Separator line between messages */
    [data-testid="stChatMessage"] + [data-testid="stChatMessage"] {
        border-top: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if not messages:
        mode_descs = {
            "Speaking": "I'll ask you IELTS Speaking questions and score each answer with band feedback.",
            "Writing": "Give you Task 1 or Task 2 questions and score your essays in detail.",
            "Reading": "Give you an academic passage with 13 exam-style questions.",
            "Vocabulary": "Teach you 5 high-band words and quiz you at the end.",
            "General": "Ask me anything about IELTS."}
        mode_label_short = mode.split("-")[0].strip()
        mode_desc = next((v for k,v in mode_descs.items() if k in mode), "Ask me anything.")

        with st.chat_message("assistant"):
            st.markdown(f"Hello! I'm **{tutor_name}**, your IELTS AI tutor. You're in **{mode_label_short}** mode — {mode_desc}\n\nWhat would you like to practice?")

        chip1, chip2, chip3, chip4 = st.columns(4)
        with chip1:
            if st.button("Give me a question", key="chip_q", use_container_width=True):
                _send_message(f"Give me an IELTS {mode_label_short} question about {topic}.", mode, topic, target_band, profile, user_id)
        with chip2:
            if st.button("Score my essay", key="chip_e", use_container_width=True):
                _send_message("I want to submit my essay for scoring. Please wait for me to paste it.", mode, topic, target_band, profile, user_id)
        with chip3:
            if st.button("Teach vocabulary", key="chip_v", use_container_width=True):
                _send_message(f"Teach me 5 high-band IELTS vocabulary words about {topic}.", mode, topic, target_band, profile, user_id)
        with chip4:
            if st.button("Explain strategy", key="chip_s", use_container_width=True):
                _send_message(f"Explain the best strategy for IELTS {mode_label_short}.", mode, topic, target_band, profile, user_id)
    else:
        for msg in messages:
            with st.chat_message(msg["role"]):
                if msg["role"] == "assistant":
                    render_annotation(msg["content"])
                else:
                    st.markdown(msg["content"])

    # ── INPUT AREA: Mic + Text (side by side) ──
    if HAS_MIC_RECORDER and "Speaking" in mode:
        mic_col, input_col = st.columns([1, 5])
        with mic_col:
            voice_text = speech_to_text(
                language='en', start_prompt="🎤 Speak",
                stop_prompt="⏹️ Stop", just_once=True,
                use_container_width=True, key='stt_main')
            if voice_text:
                st.toast("Voice captured!", icon="🎙️")
                _send_message(f"{voice_text}", mode, topic, target_band, profile, user_id)
        with input_col:
            user_input = st.chat_input("Type your answer, essay, or question here...")
            if user_input:
                _send_message(user_input, mode, topic, target_band, profile, user_id)
    else:
        user_input = st.chat_input("Type your answer, essay, or question here...")
        if user_input:
            _send_message(user_input, mode, topic, target_band, profile, user_id)


def _send_message(text, mode, topic, target_band, profile, user_id):
    if "practice_messages" not in st.session_state:
        st.session_state.practice_messages = []

    # ── CALL LIMIT CHECK ──
    TIER_LIMITS = {
        "free":      {"sessions": 3,  "calls": 1},
        "starter":   {"sessions": 5,  "calls": 3},
        "pro":       {"sessions": 8,  "calls": 4},
        "intensive": {"sessions": 10, "calls": 2},
        "lifetime":  {"sessions": 6,  "calls": 2},
    }
    tier = profile.get("subscription_status", "free")
    limits = TIER_LIMITS.get(tier, TIER_LIMITS["free"])
    call_key = "session_call_count"

    if user_id != "demo":
        current_calls = st.session_state.get(call_key, 0)
        if current_calls >= limits["calls"]:
            st.warning(f"You've reached your {limits['calls']} AI call limit for this session. Start a new session or upgrade your plan.")
            return

    if not st.session_state.get("current_session_id") and user_id != "demo":
        session_id = create_session(user_id, mode, topic, target_band)
        st.session_state.current_session_id = session_id
    else:
        session_id = st.session_state.get("current_session_id")

    st.session_state.practice_messages.append({"role": "user", "content": text})
    if session_id and user_id != "demo":
        save_message(session_id, user_id, "user", text)

    with st.chat_message("user"):
        st.markdown(text)

    # Increment call count
    st.session_state[call_key] = st.session_state.get(call_key, 0) + 1

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            system = get_system_prompt(mode, profile)
            response = chat(st.session_state.practice_messages, system)
            if response.startswith("ERROR"):
                st.error(response)
                return
            render_annotation(response)

    st.session_state.practice_messages.append({"role": "assistant", "content": response})
    if session_id and user_id != "demo":
        save_message(session_id, user_id, "assistant", response)
        update_session(session_id, {"message_count": len(st.session_state.practice_messages)})

    _try_extract_and_save_band(response, mode, user_id, session_id)
    st.rerun()


def _try_extract_and_save_band(response, mode, user_id, session_id):
    if not session_id or user_id == "demo":
        return
    from utils.score_extractor import extract_band_score_from_text
    skill = ("speaking" if "Speaking" in mode else "writing" if "Writing" in mode else
             "reading" if "Reading" in mode else "listening" if "Listening" in mode else "general")
    band = extract_band_score_from_text(response, skill=skill, default=None)
    if band is None:
        band = extract_band_score_from_text(response, skill="overall", default=None)
    if band is not None:
        try:
            save_band_score(user_id, session_id, skill, band)
            update_session(session_id, {"overall_band": band})
        except Exception:
            pass
