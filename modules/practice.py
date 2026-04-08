# ============================================================
# modules/practice.py
# Core practice engine with HTML annotation renderer
# ============================================================

import streamlit as st
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


def get_system_prompt(mode: str, profile: dict) -> str:
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


def render_annotation(text: str):
    """Render AI response with 3-color inline annotation system.
    Matches the landing page style: colored background highlights on quoted text,
    with a legend bar below the annotated section.
    """
    import re

    # Extract annotation blocks and the rest of the response separately
    # Pattern: emoji + label + quoted text + arrow + correction/explanation
    annotation_pattern = r'(🔴|🔵|🟢)\s*(?:\[?(?:RED|BLUE|GREEN)[^\]]*\]?[:\s—–-]*|(?:Band Killer|Band 8 Upgrade|Strategic Success)[:\s—–-]*)(.+?)(?=(?:\n\s*(?:🔴|🔵|🟢))|$)'

    matches = list(re.finditer(annotation_pattern, text, flags=re.DOTALL))

    if not matches:
        st.markdown(text)
        return

    # Split text: everything before first annotation is "normal" text
    first_match_start = matches[0].start()
    pre_text = text[:first_match_start].strip()
    post_text_start = matches[-1].end()
    post_text = text[post_text_start:].strip()

    # Render the normal feedback text (band scores, comments, etc.)
    if pre_text:
        st.markdown(pre_text)

    # Color map matching landing page exactly
    color_map = {
        '🔴': {'bg': 'rgba(231,76,60,0.18)', 'border': '#E74C3C', 'label': 'Band Killer', 'dot': '#E74C3C'},
        '🔵': {'bg': 'rgba(56,189,248,0.18)', 'border': '#38BDF8', 'label': 'Band 8 Upgrade', 'dot': '#38BDF8'},
        '🟢': {'bg': 'rgba(46,204,113,0.18)', 'border': '#2ECC71', 'label': 'Strategic Success', 'dot': '#2ECC71'},
    }

    # Build annotation HTML — inline highlighted spans
    annotation_html = '<div style="background:rgba(255,255,255,0.03);border-radius:14px;padding:20px;margin:16px 0;border:1px solid rgba(74,158,255,0.08)">'

    # Group annotations by paragraph: red = errors, blue = upgrades, green = successes
    for match in matches:
        emoji = match.group(1)
        content = match.group(2).strip()
        colors = color_map.get(emoji, color_map['🔴'])

        # Try to extract quoted text vs explanation
        # Common formats: "quoted text" → correction → explanation
        #                 Quote: "text" | Correction: "text" | Why: text
        quote_match = re.search(r'["""](.+?)["""]', content)

        if quote_match:
            quoted = quote_match.group(1)
            rest = content[quote_match.end():].strip()
            rest = re.sub(r'^[→►\-—–:\s]+', '', rest).strip()

            annotation_html += f'''
            <div style="margin-bottom:12px">
                <span style="background:{colors['bg']};border-bottom:2px solid {colors['border']};
                             padding:3px 6px;border-radius:3px;font-size:14px;color:#f0f4ff;
                             line-height:2;display:inline">{quoted}</span>
                <div style="font-size:12px;color:rgba(180,210,255,0.6);margin-top:4px;padding-left:4px">{rest}</div>
            </div>'''
        else:
            # No clear quote — render as a highlighted block
            annotation_html += f'''
            <div style="margin-bottom:12px">
                <span style="background:{colors['bg']};border-bottom:2px solid {colors['border']};
                             padding:3px 6px;border-radius:3px;font-size:14px;color:#f0f4ff;
                             line-height:2;display:inline">{content[:120]}</span>
                {f'<div style="font-size:12px;color:rgba(180,210,255,0.6);margin-top:4px;padding-left:4px">{content[120:]}</div>' if len(content) > 120 else ''}
            </div>'''

    # Legend bar — matches landing page exactly
    annotation_html += '''
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:16px;padding-top:12px;border-top:1px solid rgba(74,158,255,0.08)">
        <span style="display:flex;align-items:center;gap:6px;font-size:11px;color:rgba(180,210,255,0.5)">
            <span style="width:8px;height:8px;border-radius:2px;background:#E74C3C;display:inline-block"></span>
            Band Killer — fix immediately
        </span>
        <span style="display:flex;align-items:center;gap:6px;font-size:11px;color:rgba(180,210,255,0.5)">
            <span style="width:8px;height:8px;border-radius:2px;background:#38BDF8;display:inline-block"></span>
            Band 8 Upgrade — use this
        </span>
        <span style="display:flex;align-items:center;gap:6px;font-size:11px;color:rgba(180,210,255,0.5)">
            <span style="width:8px;height:8px;border-radius:2px;background:#2ECC71;display:inline-block"></span>
            Strategic Success — P-R-E-A done right
        </span>
    </div>'''

    annotation_html += '</div>'

    st.markdown(annotation_html, unsafe_allow_html=True)

    # Render any text after annotations
    if post_text:
        st.markdown(post_text)


def render_practice():
    profile = st.session_state.get("profile", {})
    accent = profile.get("accent_color", "#4A9EFF")
    tutor_name = profile.get("tutor_name", "Alex")
    user_id = st.session_state.get("user_id", "demo")

    # ── CONTROLS ──
    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([3, 2, 1, 1])

    with ctrl_col1:
        mode = st.selectbox(
            "Mode", MODES,
            index=MODES.index(st.session_state.get("practice_mode", MODES[0]))
                  if st.session_state.get("practice_mode") in MODES else 0,
            label_visibility="collapsed", key="practice_mode_select"
        )
        st.session_state.practice_mode = mode

        # Redirect Listening modes to dedicated listening page
        if "Listening" in mode:
            st.session_state.practice_mode = MODES[0]  # Reset to prevent loop
            st.session_state.current_view = "listening"
            st.rerun()

    with ctrl_col2:
        topic = st.selectbox("Topic", TOPICS,
                             label_visibility="collapsed", key="practice_topic")

    with ctrl_col3:
        target_band = st.selectbox(
            "Band",
            options=[5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0],
            index=[5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0].index(
                float(profile.get("target_band", 7.0))
            ),
            label_visibility="collapsed", key="practice_band"
        )

    with ctrl_col4:
        if st.button("🗑️ Clear", use_container_width=True, key="clear_chat"):
            st.session_state.practice_messages = []
            st.session_state.current_session_id = None
            st.rerun()

    # ── FEEDBACK MODE TOGGLE ──
    fm_col1, fm_col2, _ = st.columns([1, 1, 3])
    with fm_col1:
        if st.button(
            "🎯 Detailed Feedback" if profile.get("feedback_mode", "detailed") == "detailed" else "📝 Simple Feedback",
            key="toggle_feedback_mode",
            use_container_width=True,
            help="Toggle between detailed 3-color annotation and simple feedback"
        ):
            current = profile.get("feedback_mode", "detailed")
            new_mode = "simple" if current == "detailed" else "detailed"
            st.session_state.profile["feedback_mode"] = new_mode
            st.rerun()

    mode_label = profile.get("feedback_mode", "detailed").title()
    st.markdown(f"""
    <div style="font-size:11px;color:rgba(255,255,255,0.35);margin-bottom:12px">
        Feedback mode: <span style="color:{accent}">{mode_label}</span>
        {"— 3-color annotation + fluency gap analysis active" if profile.get("feedback_mode","detailed") == "detailed" else "— clean scores and tips"}
    </div>
    """, unsafe_allow_html=True)

    # Mode pills
    mode_color = (
        "#A78BFA" if "Speaking" in mode else "#38BDF8" if "Writing" in mode else
        "#FCD34D" if "Listening" in mode else "#34D399" if "Reading" in mode else
        "#F472B6" if "Vocabulary" in mode else "rgba(255,255,255,0.4)"
    )
    st.markdown(f"""
    <div style="margin-bottom:12px">
        <span class="pill pill-gold">{mode.split("-")[0].strip()}</span>
        <span class="pill" style="background:rgba(255,255,255,0.06);color:rgba(255,255,255,0.5);border:1px solid rgba(255,255,255,0.1)">{topic}</span>
        <span class="pill pill-green">Band {target_band}</span>
        <span style="float:right;font-size:11px;font-weight:600;color:{mode_color};background:{mode_color}18;padding:4px 10px;border-radius:20px;border:1px solid {mode_color}44">{mode}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── GREETING ──
    mode_descs = {
        "Speaking": "I'll ask you IELTS Speaking questions and score each answer with band feedback.",
        "Writing": "Give you Task 1 or Task 2 questions and score your essays in detail.",
        "Listening": "Generate a realistic listening script and test your comprehension.",
        "Reading": "Give you an academic passage with 13 exam-style questions.",
        "Vocabulary": "Teach you 5 high-band words and quiz you at the end.",
        "General": "Ask me anything about IELTS."
    }
    mode_label_short = mode.split("-")[0].strip()
    mode_desc = next((v for k, v in mode_descs.items() if k in mode), "Ask me anything.")

    st.markdown(f"""
    <div style="background:rgba(240,192,64,0.06);border-radius:20px 20px 20px 4px;
                border:1px solid rgba(240,192,64,0.15);padding:16px 20px;margin-bottom:16px">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
            <div style="width:32px;height:32px;border-radius:50%;background:{accent}22;
                        border:1px solid {accent}44;display:flex;align-items:center;
                        justify-content:center;font-size:16px">🎓</div>
            <div style="font-size:13px;font-weight:700;color:{accent}">{tutor_name}</div>
        </div>
        <div style="font-size:14px;color:#dde6f0;line-height:1.7">
            Hello! I'm <strong style="color:{accent}">{tutor_name}</strong>, your IELTS AI tutor.
            You're in <strong style="color:{accent}">{mode_label_short}</strong> mode — {mode_desc}
            <br><br>What would you like to practice?
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── QUICK START CHIPS ──
    chip1, chip2, chip3, chip4 = st.columns(4)
    with chip1:
        if st.button("Give me a question", key="chip_q", use_container_width=True):
            _send_message(f"Give me an IELTS {mode_label_short} question about {topic}.",
                          mode, topic, target_band, profile, user_id)
    with chip2:
        if st.button("Score my essay", key="chip_e", use_container_width=True):
            _send_message("I want to submit my essay for scoring. Please wait for me to paste it.",
                          mode, topic, target_band, profile, user_id)
    with chip3:
        if st.button("Teach vocabulary", key="chip_v", use_container_width=True):
            _send_message(f"Teach me 5 high-band IELTS vocabulary words about {topic}.",
                          mode, topic, target_band, profile, user_id)
    with chip4:
        if st.button("Explain strategy", key="chip_s", use_container_width=True):
            _send_message(f"Explain the best strategy for IELTS {mode_label_short}.",
                          mode, topic, target_band, profile, user_id)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── CHAT HISTORY ──
    messages = st.session_state.get("practice_messages", [])
    for msg in messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                render_annotation(msg["content"])
            else:
                st.markdown(msg["content"])

    # ── VOICE INPUT ──
    if "Speaking" in mode and HAS_MIC_RECORDER:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.04);border-radius:16px;
                    border:1px solid rgba(240,192,64,0.15);padding:14px 18px;margin-bottom:10px">
            <div style="font-weight:700;font-size:13px;color:#4A9EFF;margin-bottom:4px">Voice Recording</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.35)">Click Start, speak your answer, click Stop.</div>
        </div>
        """, unsafe_allow_html=True)
        voice_text = speech_to_text(
            language='en', start_prompt="🎤 Start Speaking",
            stop_prompt="⏹️ Stop Recording", just_once=True,
            use_container_width=True, key='stt_main'
        )
        if voice_text:
            st.toast("Voice captured!", icon="🎙️")
            _send_message(f"[Voice answer]: {voice_text}",
                          mode, topic, target_band, profile, user_id)

    # ── TEXT INPUT ──
    user_input = st.chat_input("Type your answer, essay, or question here...")
    if user_input:
        _send_message(user_input, mode, topic, target_band, profile, user_id)


def _send_message(text: str, mode: str, topic: str,
                  target_band: float, profile: dict, user_id: str):
    if "practice_messages" not in st.session_state:
        st.session_state.practice_messages = []

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

    with st.chat_message("assistant"):
        with st.status("Thinking...", expanded=True) as status:
            system = get_system_prompt(mode, profile)
            response = chat(st.session_state.practice_messages, system)

            if response.startswith("ERROR"):
                status.update(label="Error", state="error", expanded=False)
                st.error(response)
                return

            render_annotation(response)
            status.update(label="Done!", state="complete", expanded=False)

    st.session_state.practice_messages.append({"role": "assistant", "content": response})
    if session_id and user_id != "demo":
        save_message(session_id, user_id, "assistant", response)
        update_session(session_id, {"message_count": len(st.session_state.practice_messages)})

    _try_extract_and_save_band(response, mode, user_id, session_id)
    st.toast("Response ready!", icon="✅")
    st.rerun()


def _try_extract_and_save_band(response: str, mode: str, user_id: str, session_id: str):
    """Extract band score from practice response and save to DB — robust version."""
    if not session_id or user_id == "demo":
        return

    from utils.score_extractor import extract_band_score_from_text

    skill = (
        "speaking" if "Speaking" in mode else
        "writing" if "Writing" in mode else
        "reading" if "Reading" in mode else
        "listening" if "Listening" in mode else
        "general"
    )

    # Try skill-specific extraction first, then overall
    band = extract_band_score_from_text(response, skill=skill, default=None)
    if band is None:
        band = extract_band_score_from_text(response, skill="overall", default=None)

    if band is not None:
        try:
            save_band_score(user_id, session_id, skill, band)
            update_session(session_id, {"overall_band": band})
        except Exception:
            pass
