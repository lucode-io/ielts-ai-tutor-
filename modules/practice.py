# ============================================================
# modules/practice.py  —  FINAL VERSION (April 16 2026)
# CRITICAL_FIXES_REPORT items resolved:
#   ✅ #1  Recurring errors saved after every AI response (3 extraction methods)
#   ✅ #2  3-color annotation always rendered — dedup logic fully rewritten
#   ✅ #5  Error memory injected into system prompt at session start
#   ✅ #6  Writing: st.text_area + live word counter (key/value collision fixed)
#   ✅ #7  Listening: 2-column layout (audio+script left, questions right)
# BUG FIXES vs previous version:
#   🐛 render_practice — signature changed to zero-arg to match router call
#        (fixes TypeError at ielts_master.py:363)
#   🐛 render_annotation — dead `annotations` list + duplicate span renders removed
#   🐛 text_area key collision — value no longer mirrors key in session_state
#   🐛 Method 3 error extraction — false-positive guard added (scoring context only)
#   🐛 get_daily_session_count/increment_daily_session_count — graceful fallback
# ============================================================

import streamlit as st
import time
import json
import re
from datetime import datetime
from utils.ai import (
    chat, speaking_prompt, writing_task1_prompt, writing_task2_prompt,
    listening_prompt, reading_prompt, vocabulary_prompt, diagnostic_prompt,
)
from utils.database import (
    create_session, update_session, save_message, save_band_score,
    get_recurring_errors, upsert_recurring_error,
)

try:
    from streamlit_mic_recorder import speech_to_text
    HAS_MIC_RECORDER = True
except ImportError:
    HAS_MIC_RECORDER = False

# ── VIP WHITELIST ───────────────────────────────────────────
# Emails here bypass ALL session/call limits (unlimited free access)
VIP_EMAILS = {
    "ariukanyamraa@gmail.com",
    # add more lowercase emails here
}


def _is_vip(profile: dict) -> bool:
    """Return True if user email is whitelisted for unlimited access."""
    if not profile:
        return False
    email = (profile.get("email") or "").strip().lower()
    return email in VIP_EMAILS


# ── SCORING CONTEXT PHRASES ─────────────────────────────────
_SCORING_CONTEXT_RE = re.compile(
    r'\b(your (writing|essay|answer|response|speaking)|'
    r'you (wrote|used|said|made)|'
    r'student (uses|used|wrote|said)|'
    r'band killer|band score|penali[sz]e)\b',
    re.IGNORECASE
)

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
    "General Practice",
]

TOPICS = [
    "Technology", "Environment", "Education", "Health",
    "Work and Career", "Culture and Society", "Travel",
    "Food", "Family", "Crime and Law", "Economy", "Free choice",
]

MODE_TIMERS = {
    "Speaking - Part 2": 120,
    "Writing - Task 1":  1200,
    "Writing - Task 2":  2400,
    "Reading":           1200,
}

TIER_LIMITS = {
    "free":      {"sessions": 3,  "calls": 1,  "skills": ["Speaking", "Writing", "Vocabulary", "General"]},
    "starter":   {"sessions": 5,  "calls": 3,  "skills": ["Speaking", "Writing", "Reading", "Listening", "Vocabulary", "General"]},
    "pro":       {"sessions": 8,  "calls": 4,  "skills": ["Speaking", "Writing", "Reading", "Listening", "Vocabulary", "General"]},
    "intensive": {"sessions": 10, "calls": 2,  "skills": ["Speaking", "Writing", "Reading", "Listening", "Vocabulary", "General"]},
    "lifetime":  {"sessions": 6,  "calls": 2,  "skills": ["Speaking", "Writing", "Reading", "Listening", "Vocabulary", "General"]},
}


# ── DAILY SESSION COUNTER (DB-optional) ─────────────────────

def _get_daily_session_count(user_id: str) -> int:
    """Try DB function; fall back to session_state counter."""
    try:
        from utils.database import get_daily_session_count
        return get_daily_session_count(user_id)
    except Exception:
        key = f"daily_sessions_{datetime.utcnow().date().isoformat()}"
        return st.session_state.get(key, 0)


def _increment_daily_session_count(user_id: str):
    """Try DB function; fall back to session_state counter."""
    try:
        from utils.database import increment_daily_session_count
        increment_daily_session_count(user_id)
    except Exception:
        key = f"daily_sessions_{datetime.utcnow().date().isoformat()}"
        st.session_state[key] = st.session_state.get(key, 0) + 1


# ── TIMER ───────────────────────────────────────────────────

def _get_timer_seconds(mode: str):
    for key, secs in MODE_TIMERS.items():
        if key in mode:
            return secs
    return None


def _render_practice_timer(mode: str):
    timer_secs = _get_timer_seconds(mode)
    if timer_secs is None:
        return

    timer_key = f"practice_timer_{mode}"
    if timer_key not in st.session_state:
        st.session_state[timer_key] = time.time()

    elapsed  = time.time() - st.session_state[timer_key]
    remaining = max(0, timer_secs - int(elapsed))

    label_map = {"Task 1": "WRITING TASK 1", "Task 2": "WRITING TASK 2",
                 "Part 2": "SPEAKING PART 2", "Reading": "READING"}
    label = next((v for k, v in label_map.items() if k in mode),
                 mode.split("-")[0].strip().upper())

    tid = f"t_{mode.replace(' ','_').replace('-','_').replace('(','').replace(')','')}"
    st.markdown(f"""
<div style="background:rgba(74,158,255,0.04);border:1px solid rgba(74,158,255,0.1);
            border-radius:12px;padding:12px 16px;margin-bottom:16px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
    <div style="font-size:11px;color:rgba(180,210,255,0.45);text-transform:uppercase;
                letter-spacing:0.06em">{label}</div>
    <div id="{tid}_pct" style="font-size:11px;color:rgba(180,210,255,0.35)">...</div>
  </div>
  <div style="display:flex;align-items:center;gap:16px">
    <div id="{tid}_clock" style="font-size:28px;font-weight:800;color:#4A9EFF;
                font-family:monospace;min-width:80px">--:--</div>
    <div style="flex:1;height:6px;background:rgba(74,158,255,0.08);border-radius:3px;overflow:hidden">
      <div id="{tid}_bar" style="width:100%;height:100%;background:#4A9EFF;
                  border-radius:3px;transition:width 1s linear"></div>
    </div>
  </div>
  <div id="{tid}_warn" style="display:none;font-size:11px;color:#E74C3C;
              margin-top:6px;font-weight:600"></div>
</div>
<script>
(function(){{
  var total={timer_secs}, start=Date.now()-{int(elapsed*1000)};
  var clk=document.getElementById('{tid}_clock'),
      bar=document.getElementById('{tid}_bar'),
      warn=document.getElementById('{tid}_warn'),
      pct=document.getElementById('{tid}_pct');
  function tick(){{
    var el=Math.floor((Date.now()-start)/1000), rem=Math.max(0,total-el);
    var m=Math.floor(rem/60), s=rem%60;
    clk.textContent=(m<10?'0':'')+m+':'+(s<10?'0':'')+s;
    bar.style.width=(rem/total*100)+'%';
    pct.textContent=Math.round(rem/total*100)+'% left';
    if(rem<=120){{clk.style.color='#E74C3C';bar.style.background='#E74C3C';
                  warn.style.display='block';warn.textContent='Less than 2 minutes remaining!';}}
    else if(rem<=300){{clk.style.color='#F0C040';bar.style.background='#F0C040';}}
    else{{clk.style.color='#4A9EFF';bar.style.background='#4A9EFF';}}
    if(rem>0) setTimeout(tick,1000);
  }}
  setTimeout(tick,1000);
}})();
</script>
""", unsafe_allow_html=True)


# ── SYSTEM PROMPT ROUTER ────────────────────────────────────

def get_system_prompt(mode: str, profile: dict) -> str:
    if "Speaking" in mode:
        part = ("Part 1" if "Part 1" in mode else
                "Part 2" if "Part 2" in mode else "Part 3")
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


# ── RECURRING ERROR HELPERS ─────────────────────────────────

def _load_recurring_errors_into_profile(profile: dict, user_id: str) -> dict:
    if user_id == "demo":
        return profile
    try:
        errors = get_recurring_errors(user_id)
        if errors:
            profile = dict(profile)
            profile["_recurring_errors"] = errors[:5]
    except Exception:
        pass
    return profile


def _classify_error(text: str) -> tuple:
    t = text.lower()
    if any(w in t for w in ["verb", "tense", "agreement", "singular", "plural", "past", "present", "article"]):
        return "grammar", "grammar_error"
    if any(w in t for w in ["word choice", "vocabulary", "collocation", "phrase", "expression", "lexical"]):
        return "vocabulary", "vocabulary_error"
    if any(w in t for w in ["paragraph", "structure", "organisation", "organization", "coherence", "order"]):
        return "structure", "structure_error"
    if any(w in t for w in ["pronunciation", "filler", "fluency", "pause", "hesit"]):
        return "pronunciation", "pronunciation_error"
    return "grammar", "grammar_error"


def _extract_and_save_errors(response: str, user_id: str):
    if user_id == "demo":
        return

    # ── Method 1: Structured JSON block ──
    try:
        json_match = re.search(
            r'\{"errors"\s*:\s*\[[\s\S]*?\]\s*\}', response)
        if json_match:
            data = json.loads(json_match.group(0))
            for err in data.get("errors", []):
                upsert_recurring_error(
                    user_id=user_id,
                    error_type=err.get("error_type", "unknown"),
                    category=err.get("category", "grammar"),
                    description=err.get("description", ""),
                    example=err.get("example", ""),
                )
            return
    except Exception:
        pass

    # ── Method 2: RED annotation parsing ──
    try:
        red_re = re.compile(
            r'\U0001f534\s*\[RED[^\]]*\]:\s*'
            r'["\u201c\u2018]([^"\u201d\u2019\n]{3,120})["\u201d\u2019]\s*'
            r'\u2192\s*([^\u2192\n]{3,120})'
            r'(?:\u2192\s*([^\n]{3,200}))?',
            re.IGNORECASE,
        )
        for m in red_re.finditer(response):
            example    = m.group(1).strip()
            correction = m.group(2).strip()
            reason     = (m.group(3) or "").strip()
            cat, etype = _classify_error(f"{example} {correction} {reason}")
            upsert_recurring_error(
                user_id=user_id,
                error_type=etype,
                category=cat,
                description=correction[:200] if correction else f"Error: {example[:80]}",
                example=example[:200],
            )
    except Exception:
        pass

    # ── Method 3: Pattern matching — scoring context guard ──
    if not _SCORING_CONTEXT_RE.search(response):
        return

    try:
        grammar_patterns = [
            (r'\bsubject[- ]verb agreement\b',   "subject_verb_agreement", "grammar"),
            (r'\barticle (a|an|the)\b',          "article_usage",          "grammar"),
            (r'\btense error\b',                 "tense_error",            "grammar"),
            (r'\bplural (error|form)\b',         "plural_error",           "grammar"),
            (r'\bpreposition (error|mistake)\b', "preposition_error",      "grammar"),
            (r'\bword order (error|problem)\b',  "word_order",             "grammar"),
            (r'\bcollocation error\b',           "collocation_error",      "vocabulary"),
            (r'\bfiller words? detected\b',      "filler_overuse",         "pronunciation"),
            (r'\bno topic sentence\b',           "paragraph_structure",    "structure"),
        ]
        for pattern, etype, cat in grammar_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                upsert_recurring_error(
                    user_id=user_id,
                    error_type=etype,
                    category=cat,
                    description=etype.replace("_", " ").title(),
                    example=None,
                )
    except Exception:
        pass


# ── 3-COLOR ANNOTATION RENDERER ─────────────────────────────

def render_annotation(text: str):
    ANNO_RE = re.compile(
        r'(\U0001f534|\U0001f535|\U0001f7e2)'
        r'[^\S\n]*'
        r'(?:\[[^\]]{0,50}\][:\s\u2014\u2013\-]*)?'
        r'([^\n]+)',
        re.UNICODE,
    )

    COLOR_MAP = {
        '\U0001f534': ('#ff3a4a', '\U0001f534 Band Killer'),
        '\U0001f535': ('#4A9EFF', '\U0001f535 Band 8 Upgrade'),
        '\U0001f7e2': ('#00e87a', '\U0001f7e2 Strategic Win'),
    }

    seen_starts = set()
    spans = []

    for m in ANNO_RE.finditer(text):
        start = m.start()
        if start in seen_starts:
            continue
        seen_starts.add(start)
        emoji   = m.group(1)
        content = m.group(2).strip()
        if content and len(content) > 4:
            spans.append((start, m.end(), emoji, content))

    if not spans:
        st.markdown(text)
        return

    last_pos = 0
    for start, end, emoji, content in spans:
        prose = text[last_pos:start].strip()
        if prose:
            st.markdown(prose)

        color, label = COLOR_MAP.get(emoji, ('#4A9EFF', 'Note'))
        st.markdown(
            f'<div style="background:{color}12;border-left:3px solid {color};'
            f'border-radius:0 8px 8px 0;padding:10px 14px;margin:4px 0;'
            f'font-size:13px;line-height:1.6">'
            f'<span style="color:{color};font-weight:700;font-size:11px;'
            f'text-transform:uppercase;letter-spacing:0.05em">{label}</span><br>'
            f'<span style="color:rgba(240,244,255,0.9)">{content}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        last_pos = end

    remainder = text[last_pos:].strip()
    if remainder:
        st.markdown(remainder)


# ── WRITING INPUT ───────────────────────────────────────────

def _render_writing_input(mode: str, topic: str, target_band: float,
                           profile: dict, user_id: str):
    min_words  = 150 if "Task 1" in mode else 250
    task_label = "Task 1" if "Task 1" in mode else "Task 2"

    val_key    = f"essay_val_{mode}"
    widget_key = f"essay_widget_{mode}"

    st.markdown(
        f'<div style="font-size:11px;color:rgba(180,210,255,0.45);'
        f'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px">'
        f'Paste or type your {task_label} essay below (minimum {min_words} words)'
        f'</div>',
        unsafe_allow_html=True,
    )

    essay_text = st.text_area(
        label=f"{task_label} essay",
        height=220,
        placeholder=(
            f"Paste your essay here or ask for a question first...\n\n"
            f"Minimum {min_words} words for accurate scoring."
        ),
        key=widget_key,
        label_visibility="collapsed",
    )
    st.session_state[val_key] = essay_text

    word_count  = len(essay_text.split()) if essay_text.strip() else 0
    bar_pct     = min(100, int(word_count / min_words * 100))
    cnt_color   = ("#00e87a" if word_count >= min_words
                   else "#F0C040" if word_count >= int(min_words * 0.8)
                   else "#ff3a4a")
    status_txt  = ("✓ Ready to submit"
                   if word_count >= min_words
                   else f"{min_words - word_count} more words needed")

    st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">
  <div style="font-size:13px;color:{cnt_color};font-weight:700;min-width:100px">
    {word_count} / {min_words} words
  </div>
  <div style="flex:1;height:4px;background:rgba(74,158,255,0.1);border-radius:2px">
    <div style="width:{bar_pct}%;height:100%;background:{cnt_color};
                border-radius:2px;transition:width 0.3s"></div>
  </div>
  <div style="font-size:11px;color:rgba(180,210,255,0.4)">{status_txt}</div>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Submit for Scoring", use_container_width=True,
                     key=f"submit_{mode}", disabled=(word_count < 30)):
            if essay_text.strip():
                _send_message(essay_text, mode, topic, target_band, profile, user_id)
    with col2:
        if st.button("❓ Give me a question", use_container_width=True,
                     key=f"getq_{mode}"):
            _send_message(
                f"Give me an IELTS {task_label} question about {topic}.",
                mode, topic, target_band, profile, user_id,
            )
    with col3:
        if st.button("💡 Strategy tips", use_container_width=True,
                     key=f"strat_{mode}"):
            _send_message(
                f"Explain the best strategy for IELTS Writing {task_label}.",
                mode, topic, target_band, profile, user_id,
            )

    chat_in = st.chat_input("Ask anything about writing strategy, vocab, or grammar…")
    if chat_in:
        _send_message(chat_in, mode, topic, target_band, profile, user_id)


# ── LISTENING 2-COLUMN LAYOUT ───────────────────────────────

def _render_listening_chat(messages: list, mode: str, topic: str,
                            target_band: float, profile: dict, user_id: str):
    script_text = ""
    for msg in reversed(messages):
        if msg["role"] == "assistant":
            m = re.search(
                r'\*\*LISTENING SCRIPT[^*]*\*\*\s*\n([\s\S]+?)(?=\n---|\n\*\*QUESTIONS)',
                msg["content"],
                re.IGNORECASE,
            )
            if m:
                script_text = m.group(1).strip()
                break

    left_col, right_col = st.columns([55, 45])

    with left_col:
        st.markdown(
            '<div style="font-size:11px;color:rgba(180,210,255,0.45);'
            'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px">'
            'Script / Transcript</div>',
            unsafe_allow_html=True,
        )
        if script_text:
            st.markdown(
                f'<div class="glass-card" style="padding:16px;font-size:13px;'
                f'line-height:1.8;color:rgba(240,244,255,0.85);max-height:420px;'
                f'overflow-y:auto;white-space:pre-wrap">{script_text}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="glass-card" style="padding:24px;text-align:center;'
                'color:rgba(180,210,255,0.35);font-size:13px">'
                '📄 Script will appear here after the AI generates the listening exercise.'
                '</div>',
                unsafe_allow_html=True,
            )

    with right_col:
        st.markdown(
            '<div style="font-size:11px;color:rgba(180,210,255,0.45);'
            'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px">'
            'Questions & Answers</div>',
            unsafe_allow_html=True,
        )
        for msg in messages:
            with st.chat_message(msg["role"]):
                if msg["role"] == "assistant":
                    display_content = re.sub(
                        r'\*\*LISTENING SCRIPT[^*]*\*\*\s*\n[\s\S]+?(?=\n---|\n\*\*QUESTIONS)',
                        '[Script shown on the left →]\n\n',
                        msg["content"],
                        flags=re.IGNORECASE,
                    )
                    render_annotation(display_content)
                else:
                    st.markdown(msg["content"])

        user_input = st.chat_input("Type your answers here…")
        if user_input:
            _send_message(user_input, mode, topic, target_band, profile, user_id)

        if not messages:
            section = mode.split("-")[1].strip() if "-" in mode else "Section 1"
            if st.button(f"▶ Generate {section} exercise", use_container_width=True,
                         key="gen_listening"):
                _send_message(
                    f"Generate an IELTS Listening {section} exercise about {topic}.",
                    mode, topic, target_band, profile, user_id,
                )


# ── MAIN RENDER ─────────────────────────────────────────────
# SIGNATURE FIX: zero-arg to match router call in ielts_master.py

def render_practice():
    """
    Main practice module renderer.
    Reads profile and user_id from st.session_state (router pattern).
    """
    profile = st.session_state.get("profile", {}) or {}
    user_id = st.session_state.get("user_id", "demo")

    tier   = profile.get("subscription_status", "free")
    limits = TIER_LIMITS.get(tier, TIER_LIMITS["free"])

    # Daily session limit check (VIPs bypass)
    is_vip = _is_vip(profile)
    daily_sessions = _get_daily_session_count(user_id) if user_id != "demo" else 0
    if user_id != "demo" and not is_vip and daily_sessions >= limits["sessions"]:
        st.markdown(f"""
<div class="glass-card" style="text-align:center;padding:32px">
  <div style="font-size:32px;margin-bottom:12px">⏸️</div>
  <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:8px">
    Daily session limit reached
  </div>
  <div style="font-size:14px;color:rgba(180,210,255,0.5)">
    Used {daily_sessions} of {limits['sessions']} sessions today on the {tier} plan.
    Come back tomorrow or upgrade.
  </div>
</div>
""", unsafe_allow_html=True)
        return

    call_key = "session_call_count"
    if call_key not in st.session_state:
        st.session_state[call_key] = 0

    # Filter modes by tier
    allowed = limits["skills"]
    available_modes = [m for m in MODES if any(s in m for s in allowed)] or MODES[:2]

    # ── CONTROLS ──────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
    with c1:
        stored_mode = st.session_state.get("practice_mode", available_modes[0])
        mode_idx = available_modes.index(stored_mode) if stored_mode in available_modes else 0
        mode = st.selectbox("Mode", available_modes, index=mode_idx,
                            label_visibility="collapsed", key="practice_mode_select")
        st.session_state.practice_mode = mode
        # Listening redirects to dedicated module
        if "Listening" in mode:
            st.session_state.practice_mode = available_modes[0]
            st.session_state.current_view  = "listening"
            st.rerun()
    with c2:
        topic = st.selectbox("Topic", TOPICS, label_visibility="collapsed",
                             key="practice_topic")
    with c3:
        band_opts = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0]
        default_band = float(profile.get("target_band", 7.0))
        band_idx = band_opts.index(default_band) if default_band in band_opts else 4
        target_band = st.selectbox("Band", band_opts, index=band_idx,
                                   label_visibility="collapsed", key="practice_band")
    with c4:
        if st.button("🗑️ Clear", use_container_width=True, key="clear_chat"):
            for k in [k for k in st.session_state if k.startswith("practice_timer_")]:
                del st.session_state[k]
            st.session_state.practice_messages  = []
            st.session_state.current_session_id = None
            st.session_state[call_key]          = 0
            st.rerun()

    # Inject recurring errors into profile for prompt building
    profile_with_errors = _load_recurring_errors_into_profile(profile, user_id)

    # Timer
    _render_practice_timer(mode)

    # Messages init
    if "practice_messages" not in st.session_state:
        st.session_state.practice_messages = []
    messages    = st.session_state.practice_messages
    tutor_name  = profile.get("tutor_name", "Alex")

    # ── LISTENING — 2-column layout ──────────────────────────
    if "Listening" in mode:
        _render_listening_chat(messages, mode, topic, target_band,
                               profile_with_errors, user_id)
        return

    # ── CHAT HISTORY / WELCOME ────────────────────────────────
    if not messages:
        descs = {
            "Speaking":   "I'll ask IELTS Speaking questions and give instant band score feedback.",
            "Writing":    "Paste your essay to score, or ask me for a question first.",
            "Reading":    "I'll generate an academic passage and 13 exam-style questions.",
            "Vocabulary": "I'll teach 5 high-band words and quiz you.",
            "General":    "Ask me anything about IELTS.",
        }
        short = mode.split("-")[0].strip()
        desc  = next((v for k, v in descs.items() if k in mode), "Ask me anything.")
        with st.chat_message("assistant"):
            st.markdown(
                f"Hello! I'm **{tutor_name}**, your IELTS AI tutor. "
                f"You're in **{short}** mode — {desc}\n\nWhat would you like to practice?"
            )

        # Quick-start chips
        if "Reading" in mode:
            ch1, ch2, ch3 = st.columns(3)
            with ch1:
                if st.button("Generate passage + 13 Qs", key="cr1", use_container_width=True):
                    _send_message(
                        f"Generate an IELTS Academic reading passage about {topic} "
                        f"(600-800 words, paragraphs A-E). Give exactly 13 questions: "
                        f"4 TFNG, 4 matching headings, 3 sentence completion, 2 MCQ. "
                        f"I will answer them one by one.",
                        mode, topic, target_band, profile_with_errors, user_id)
            with ch2:
                if st.button("TFNG practice only", key="cr2", use_container_width=True):
                    _send_message(
                        f"Generate a 300-word academic passage about {topic} and give me 5 TFNG questions.",
                        mode, topic, target_band, profile_with_errors, user_id)
            with ch3:
                if st.button("TFNG strategy", key="cr3", use_container_width=True):
                    _send_message("Explain the best strategy for IELTS Academic Reading TFNG questions.",
                                  mode, topic, target_band, profile_with_errors, user_id)

        elif "Speaking" in mode:
            ch1, ch2, ch3 = st.columns(3)
            sp_part = ("Part 1" if "Part 1" in mode else
                       "Part 2" if "Part 2" in mode else "Part 3")
            with ch1:
                if st.button("Start with a question", key="cs1", use_container_width=True):
                    _send_message(f"Give me an IELTS {sp_part} question about {topic}.",
                                  mode, topic, target_band, profile_with_errors, user_id)
            with ch2:
                if st.button("Score my answer", key="cs2", use_container_width=True):
                    _send_message("Ask me a question and score my answer.",
                                  mode, topic, target_band, profile_with_errors, user_id)
            with ch3:
                if st.button("Explain strategy", key="cs3", use_container_width=True):
                    _send_message(f"Explain the best strategy for IELTS Speaking {sp_part}.",
                                  mode, topic, target_band, profile_with_errors, user_id)

        elif "Writing" not in mode:
            ch1, ch2, ch3, ch4 = st.columns(4)
            short_m = mode.split("-")[0].strip()
            with ch1:
                if st.button("Give me a question", key="cg1", use_container_width=True):
                    _send_message(f"Give me an IELTS {short_m} question about {topic}.",
                                  mode, topic, target_band, profile_with_errors, user_id)
            with ch2:
                if st.button("Score my answer", key="cg2", use_container_width=True):
                    _send_message("I want to submit my answer for scoring. Please wait.",
                                  mode, topic, target_band, profile_with_errors, user_id)
            with ch3:
                if st.button("Teach vocabulary", key="cg3", use_container_width=True):
                    _send_message(f"Teach me 5 high-band IELTS vocabulary words about {topic}.",
                                  mode, topic, target_band, profile_with_errors, user_id)
            with ch4:
                if st.button("Explain strategy", key="cg4", use_container_width=True):
                    _send_message(f"Explain the best strategy for IELTS {short_m}.",
                                  mode, topic, target_band, profile_with_errors, user_id)
    else:
        for msg in messages:
            with st.chat_message(msg["role"]):
                if msg["role"] == "assistant":
                    render_annotation(msg["content"])
                else:
                    st.markdown(msg["content"])

    # ── INPUT AREA ─────────────────────────────────────────────
    is_writing = "Writing" in mode and "Task" in mode

    if is_writing:
        _render_writing_input(mode, topic, target_band, profile_with_errors, user_id)
    elif HAS_MIC_RECORDER and "Speaking" in mode:
        mic_col, txt_col = st.columns([1, 5])
        with mic_col:
            voice = speech_to_text(language="en", start_prompt="🎤 Speak",
                                   stop_prompt="⏹️ Stop", just_once=True,
                                   use_container_width=True, key="stt_main")
            if voice:
                st.toast("Voice captured! ✓", icon="🎙️")
                _send_message(voice, mode, topic, target_band, profile_with_errors, user_id)
        with txt_col:
            ui = st.chat_input("Or type your answer here…")
            if ui:
                _send_message(ui, mode, topic, target_band, profile_with_errors, user_id)
    else:
        ui = st.chat_input("Type your answer or question here…")
        if ui:
            _send_message(ui, mode, topic, target_band, profile_with_errors, user_id)


# ── SEND MESSAGE ────────────────────────────────────────────

def _send_message(text: str, mode: str, topic: str, target_band: float,
                  profile: dict, user_id: str):
    if "practice_messages" not in st.session_state:
        st.session_state.practice_messages = []

    # Call limit check
    tier   = profile.get("subscription_status", "free")
    limits = TIER_LIMITS.get(tier, TIER_LIMITS["free"])
    call_key = "session_call_count"

    if user_id != "demo" and not _is_vip(profile):
        if st.session_state.get(call_key, 0) >= limits["calls"]:
            st.warning(
                f"You've reached your {limits['calls']} AI call limit for this session. "
                "Start a new session or upgrade your plan."
            )
            return

    # Create session on first message
    session_id = st.session_state.get("current_session_id")
    if not session_id and user_id != "demo":
        session_id = create_session(user_id, mode, topic, target_band)
        st.session_state.current_session_id = session_id
        _increment_daily_session_count(user_id)

    # Save user message
    st.session_state.practice_messages.append({"role": "user", "content": text})
    if session_id and user_id != "demo":
        save_message(session_id, user_id, "user", text)

    with st.chat_message("user"):
        st.markdown(text)

    st.session_state[call_key] = st.session_state.get(call_key, 0) + 1

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            system   = get_system_prompt(mode, profile)
            response = chat(st.session_state.practice_messages, system)
            if response.startswith("ERROR"):
                st.error(response)
                st.session_state[call_key] -= 1
                return
            render_annotation(response)

    st.session_state.practice_messages.append({"role": "assistant", "content": response})

    if session_id and user_id != "demo":
        save_message(session_id, user_id, "assistant", response)
        update_session(session_id, {"message_count": len(st.session_state.practice_messages)})

    # Save band score
    _try_extract_and_save_band(response, mode, user_id, session_id)

    # Save recurring errors
    if user_id != "demo":
        _extract_and_save_errors(response, user_id)

    st.rerun()


def _try_extract_and_save_band(response: str, mode: str, user_id: str, session_id):
    if not session_id or user_id == "demo":
        return
    try:
        from utils.score_extractor import extract_band_score_from_text
        skill = ("speaking"  if "Speaking"  in mode else
                 "writing"   if "Writing"   in mode else
                 "reading"   if "Reading"   in mode else
                 "listening" if "Listening" in mode else "general")
        band = extract_band_score_from_text(response, skill=skill, default=None)
        if band is None:
            band = extract_band_score_from_text(response, skill="overall", default=None)
        if band is not None:
            save_band_score(user_id, session_id, skill, band)
            update_session(session_id, {"overall_band": band})
    except Exception:
        pass
