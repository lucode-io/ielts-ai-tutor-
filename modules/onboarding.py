# ============================================================
# modules/onboarding.py
# Diagnostic test - mini mock test with timer + audio
# ============================================================

import streamlit as st
import re
import time
import base64
from utils.ai import chat, diagnostic_prompt
from utils.database import save_diagnostic, update_user_profile


# ── LISTENING SCRIPT ──
LISTENING_SCRIPT = """
Good morning students. I have some important announcements about next week's schedule.
On Monday, the library will open at 8am instead of the usual 9am, due to a special
study session for final year students. The science lab on the third floor will be closed
for maintenance on Tuesday and Wednesday. Students who need lab access should use the
alternative lab on the first floor. The cafeteria will introduce a new menu starting
Thursday, with vegetarian options now available every day. Finally, the sports hall
booking system has changed. You must now book at least 24 hours in advance using the
new online portal. Walk-in bookings will no longer be accepted. If you have any
questions, please contact the student office at extension 204.
"""

LISTENING_QUESTIONS = [
    "What time will the library open on Monday?",
    "Which floor is the science lab that will be closed?",
    "On which days will the science lab be closed?",
    "What is new about the cafeteria starting Thursday?",
    "How many hours in advance must students now book the sports hall?",
]

LISTENING_ANSWERS = ["8am", "third", "tuesday and wednesday", "vegetarian options", "24"]


def render_onboarding():
    profile = st.session_state.get("profile", {})
    accent = profile.get("accent_color", "#F0C040")
    user_id = st.session_state.get("user_id", "demo")
    name = profile.get("full_name", "Student").split()[0]
    step = st.session_state.get("onboarding_step", 1)

    if step == 1:
        _render_welcome(name, accent)
    elif step == 2:
        _render_diagnostic(profile, user_id, accent)
    elif step == 3:
        _render_listening_section(profile, user_id, accent)
    elif step == 4:
        _render_results(profile, user_id, accent)


def _render_welcome(name, accent):
    st.markdown(f"""
    <div style="text-align:center;padding:32px 16px 24px">
        <div style="font-size:48px;margin-bottom:12px">🎓</div>
        <div style="font-size:24px;font-weight:800;color:#fff;margin-bottom:8px">
            Welcome, {name}!
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.5);line-height:1.7;
                    max-width:480px;margin:0 auto 24px">
            Let's find your current IELTS level with a
            <strong style="color:{accent}">Mini Diagnostic Test</strong>.
            It covers all 4 skills and takes about 20 minutes.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Skills overview
    skills = [
        ("🎤", "Speaking", "4 questions, Parts 1-3", "#A78BFA", "~5 min"),
        ("✍️", "Writing", "Task 2 intro + body", "#38BDF8", "~5 min"),
        ("📖", "Reading", "Academic passage, 5 TFNG", "#34D399", "~5 min"),
        ("🎧", "Listening", "Audio script, 5 questions", "#FCD34D", "~5 min"),
    ]

    cols = st.columns(2)
    for i, (icon, skill, desc, color, duration) in enumerate(skills):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:{color}11;border:1px solid {color}33;
                        border-radius:14px;padding:16px;text-align:center;margin-bottom:10px">
                <div style="font-size:28px;margin-bottom:6px">{icon}</div>
                <div style="font-size:14px;font-weight:700;color:{color};margin-bottom:4px">{skill}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-bottom:4px">{desc}</div>
                <div style="font-size:10px;color:{color};opacity:0.7;font-weight:600">{duration}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    _, col, _ = st.columns([0.05, 0.9, 0.05])
    with col:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("🚀 Start Diagnostic Test", use_container_width=True, key="start_diag"):
            st.session_state.onboarding_step = 2
            st.session_state.diagnostic_messages = []
            st.session_state.diag_start_time = time.time()
            st.session_state.diag_section_time = time.time()
            st.session_state.diag_scores = {}
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Skip — I know my level", use_container_width=True, key="skip_diag"):
            st.session_state.current_view = "dashboard"
            st.rerun()


def _render_timer(section_name: str, duration_seconds: int, accent: str):
    """Render a countdown timer for the current section."""
    start = st.session_state.get("diag_section_time", time.time())
    elapsed = int(time.time() - start)
    remaining = max(0, duration_seconds - elapsed)
    minutes = remaining // 60
    seconds = remaining % 60
    pct = max(0, int((remaining / duration_seconds) * 100))

    color = accent if remaining > 60 else "#E74C3C"

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.04);border-radius:14px;
                border:1px solid rgba(255,255,255,0.08);padding:12px 16px;
                margin-bottom:16px;display:flex;align-items:center;
                justify-content:space-between">
        <div>
            <div style="font-size:11px;color:rgba(255,255,255,0.4);
                        text-transform:uppercase;letter-spacing:0.06em;margin-bottom:2px">
                {section_name}
            </div>
            <div style="font-size:22px;font-weight:800;color:{color};font-variant-numeric:tabular-nums">
                {minutes:02d}:{seconds:02d}
            </div>
        </div>
        <div style="width:80px">
            <div style="background:rgba(255,255,255,0.08);border-radius:4px;height:6px">
                <div style="width:{pct}%;height:100%;border-radius:4px;
                            background:{color};transition:width 0.5s"></div>
            </div>
            <div style="font-size:10px;color:rgba(255,255,255,0.3);
                        text-align:right;margin-top:3px">{pct}% left</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    return remaining


def _render_diagnostic(profile, user_id, accent):
    """Speaking + Writing + Reading via AI chat."""

    remaining = _render_timer("Speaking · Writing · Reading", 900, accent)

    if "diagnostic_messages" not in st.session_state:
        st.session_state.diagnostic_messages = []

    # Auto-start
    if not st.session_state.diagnostic_messages:
        system = _get_hard_diagnostic_prompt()
        starter = [{"role": "user", "content": "Please start my baseline assessment."}]
        with st.spinner("Starting your diagnostic test..."):
            response = chat(starter, system, max_tokens=2000)
        if response.startswith("ERROR"):
            st.error(response)
            if st.button("Skip to Dashboard", key="skip_err"):
                st.session_state.current_view = "dashboard"
                st.rerun()
            return
        st.session_state.diagnostic_messages = [
            {"role": "user", "content": "Please start my baseline assessment."},
            {"role": "assistant", "content": response}
        ]

    # Section header
    st.markdown(f"""
    <div style="margin-bottom:16px">
        <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:4px">
            Diagnostic Test — Part 1 of 2
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.4)">
            Speaking, Writing and Reading assessed here.
            Listening test comes next with audio.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.diagnostic_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Check if parts 1-3 complete
    last_msg = st.session_state.diagnostic_messages[-1]["content"] \
        if st.session_state.diagnostic_messages else ""

    section_complete = (
        "READING COMPLETE" in last_msg.upper() or
        "PROCEED TO LISTENING" in last_msg.upper() or
        "PART 4: LISTENING" in last_msg.upper() or
        ("reading" in last_msg.lower() and "score" in last_msg.lower() and
         len(st.session_state.diagnostic_messages) > 12)
    )

    if section_complete or remaining == 0:
        # Extract partial scores
        _extract_partial_scores(last_msg)
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Continue to Listening Test →", key="go_listening",
                     use_container_width=True):
            st.session_state.onboarding_step = 3
            st.session_state.diag_section_time = time.time()
            st.session_state.mock_listened = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        user_input = st.chat_input("Type your answer here...")
        if user_input:
            st.session_state.diagnostic_messages.append(
                {"role": "user", "content": user_input}
            )
            with st.chat_message("user"):
                st.markdown(user_input)
            with st.chat_message("assistant"):
                with st.spinner("Evaluating..."):
                    system = _get_hard_diagnostic_prompt()
                    response = chat(st.session_state.diagnostic_messages,
                                    system, max_tokens=2000)
                st.markdown(response)
            st.session_state.diagnostic_messages.append(
                {"role": "assistant", "content": response}
            )
            st.rerun()


def _render_listening_section(profile, user_id, accent):
    """Listening section with audio + questions."""

    remaining = _render_timer("Listening Section", 300, accent)

    listened = st.session_state.get("mock_listened", False)
    listening_submitted = st.session_state.get("listening_submitted", False)

    st.markdown(f"""
    <div style="margin-bottom:16px">
        <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:4px">
            Diagnostic Test — Part 2 of 2: Listening
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.4)">
            Listen to the announcement carefully. You will hear it once.
            Then answer 5 questions from memory.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not listened:
        # Generate and play TTS audio
        st.markdown(f"""
        <div style="background:rgba(252,211,77,0.08);border:1px solid rgba(252,211,77,0.25);
                    border-radius:14px;padding:20px;margin-bottom:16px">
            <div style="font-size:13px;font-weight:700;color:#FCD34D;margin-bottom:12px">
                🎧 Listen carefully — you will hear this only once
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Generate TTS audio
        audio_b64 = _generate_tts_audio(LISTENING_SCRIPT)

        if audio_b64:
            st.markdown(f"""
            <audio controls style="width:100%;border-radius:10px;margin-bottom:16px">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)
            st.caption("Press play — listen once only, then click the button below")
        else:
            # Fallback — show script
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04);border-radius:12px;
                        padding:16px;margin-bottom:16px;font-size:13px;
                        color:#dde6f0;line-height:1.8;font-style:italic">
                {LISTENING_SCRIPT}
            </div>
            """, unsafe_allow_html=True)
            st.caption("Read the script carefully once, then proceed to questions")

        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("I have listened — Show Questions →",
                     key="done_listening", use_container_width=True):
            st.session_state.mock_listened = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif not listening_submitted:
        st.info("Answer from memory only — do not scroll up.")

        answers = {}
        all_answered = True

        for i, question in enumerate(LISTENING_QUESTIONS):
            st.markdown(f"""
            <div style="font-size:14px;color:#dde6f0;margin-bottom:6px">
                <strong style="color:#FCD34D">Q{i+1}.</strong> {question}
            </div>
            """, unsafe_allow_html=True)
            ans = st.text_input("", key=f"diag_listen_{i}",
                                placeholder="Your answer...",
                                label_visibility="collapsed")
            if not ans:
                all_answered = False
            answers[i] = ans
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        if all_answered:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("Submit Listening & See Results →",
                         key="submit_listening", use_container_width=True):
                # Score listening
                correct = 0
                for i, correct_ans in enumerate(LISTENING_ANSWERS):
                    user_ans = answers.get(i, "").strip().lower()
                    if correct_ans.lower() in user_ans or user_ans in correct_ans.lower():
                        correct += 1
                score_map = {5: 9.0, 4: 7.5, 3: 6.5, 2: 5.5, 1: 4.5, 0: 4.0}
                listening_band = score_map.get(correct, 5.0)
                st.session_state.diag_scores["listening"] = listening_band
                st.session_state.listening_correct = correct
                st.session_state.listening_submitted = True
                st.session_state.onboarding_step = 4
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


def _render_results(profile, user_id, accent):
    """Show final diagnostic results and save."""
    scores = st.session_state.get("diag_scores", {})

    speaking = scores.get("speaking", 5.5)
    writing = scores.get("writing", 5.5)
    reading = scores.get("reading", 5.5)
    listening = scores.get("listening", 5.5)
    overall = round((speaking + writing + reading + listening) / 4 * 2) / 2

    st.markdown(f"""
    <div style="text-align:center;padding:24px 0 16px">
        <div style="font-size:44px;margin-bottom:12px">📊</div>
        <div style="font-size:22px;font-weight:800;color:#fff;margin-bottom:6px">
            Your Baseline Results
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.4)">
            This is your starting point. Let's improve from here.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Overall score
    st.markdown(f"""
    <div style="background:rgba(240,192,64,0.08);border:2px solid rgba(240,192,64,0.3);
                border-radius:20px;padding:24px;text-align:center;margin:16px 0">
        <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:6px;
                    text-transform:uppercase;letter-spacing:0.06em">
            Overall Baseline Band
        </div>
        <div style="font-size:60px;font-weight:900;color:{accent};line-height:1">{overall}</div>
        <div style="font-size:13px;color:rgba(255,255,255,0.35);margin-top:6px">
            Target: Band {profile.get('target_band', 7.0)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Skill breakdown
    skill_data = [
        ("🎤", "Speaking", speaking, "#A78BFA"),
        ("✍️", "Writing", writing, "#38BDF8"),
        ("📖", "Reading", reading, "#34D399"),
        ("🎧", "Listening", listening, "#FCD34D"),
    ]

    cols = st.columns(4)
    for col, (icon, skill, score, color) in zip(cols, skill_data):
        with col:
            st.markdown(f"""
            <div style="background:{color}11;border:1px solid {color}33;
                        border-radius:14px;padding:14px;text-align:center">
                <div style="font-size:20px;margin-bottom:4px">{icon}</div>
                <div style="font-size:11px;color:{color};text-transform:uppercase;
                            letter-spacing:0.06em;margin-bottom:6px">{skill}</div>
                <div style="font-size:26px;font-weight:800;color:{color}">{score}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Weakest skill recommendation
    weakest = min(skill_data, key=lambda x: x[2])
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.04);border-radius:14px;
                padding:16px;margin-bottom:16px;border:1px solid rgba(255,255,255,0.08)">
        <div style="font-size:13px;font-weight:700;color:{accent};margin-bottom:6px">
            Priority Focus
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.6);line-height:1.6">
            Your weakest area is <strong style="color:{weakest[3]}">{weakest[1]}</strong>
            at Band {weakest[2]}. Start your 21-Day Challenge with daily {weakest[1]} practice
            to close this gap fastest.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("✅ Save & Go to Dashboard →",
                 key="save_diag", use_container_width=True):
        full_scores = {
            "speaking": speaking, "writing": writing,
            "reading": reading, "listening": listening, "overall": overall
        }
        if user_id != "demo":
            save_diagnostic(user_id, full_scores)
        st.session_state.profile = {**profile, "baseline_band": overall}
        st.session_state.current_view = "dashboard"
        st.session_state.onboarding_step = 1
        st.session_state.diagnostic_messages = []
        st.session_state.diag_scores = {}
        st.session_state.mock_listened = False
        st.session_state.listening_submitted = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def _extract_partial_scores(text: str):
    """Extract Speaking/Writing/Reading scores from diagnostic chat."""
    scores = st.session_state.get("diag_scores", {})
    for skill in ["Speaking", "Writing", "Reading"]:
        if skill.lower() not in scores:
            patterns = [
                rf"{skill}[^:]*?Band[:\s]+(\d+\.?\d*)",
                rf"{skill}[:\s]+(\d+\.?\d*)",
                rf"{skill.lower()}[:\s]+(\d+\.?\d*)",
            ]
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        val = float(match.group(1))
                        if 3.0 <= val <= 9.0:
                            scores[skill.lower()] = val
                            break
                    except Exception:
                        pass
    # Defaults if not found
    for skill in ["speaking", "writing", "reading"]:
        if skill not in scores:
            scores[skill] = 5.5
    st.session_state.diag_scores = scores


def _generate_tts_audio(text: str) -> str:
    """Generate TTS audio using gTTS and return base64."""
    try:
        from gtts import gTTS
        import io
        tts = gTTS(text=text.strip(), lang='en', slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode()
    except Exception:
        return ""


def _get_hard_diagnostic_prompt() -> str:
    """Harder diagnostic prompt — mini mock test style."""
    return """
You are a strict IELTS examiner conducting a baseline diagnostic test.
This is a MINI MOCK TEST — be thorough but efficient.

CONDUCT EXACTLY THIS SEQUENCE:

═══ PART 1: SPEAKING (4 questions) ═══
Ask these questions one at a time, wait for answers:
Q1: "Tell me about yourself — where are you from and what do you do?"
Q2: "Describe a teacher who had a big impact on you. What made them special?"
Q3 (Cue card): "Talk for 1-2 minutes about: A place you would like to visit.
You should say: where it is, why you want to go, what you would do there."
Q4: "Do you think people travel more now than in the past? Why?"
After all 4 answers, give Speaking band with brief reason. Format: SPEAKING BAND: X.X

═══ PART 2: WRITING ═══
Give this prompt:
"Some people believe that students should study only subjects that will be useful for their future career. Others believe that students should study a wide range of subjects.
Discuss both views and give your own opinion."
Ask for: A full introduction paragraph AND one complete body paragraph (minimum 120 words total).
After they write, score it. Format: WRITING BAND: X.X

═══ PART 3: READING ═══
Give this passage:
"Urban green spaces, such as parks and community gardens, play a significant role in
improving residents' mental health. Research conducted in 2019 found that people who
spent at least 120 minutes per week in nature reported substantially higher wellbeing.
However, access to green spaces is often unequally distributed, with wealthier
neighbourhoods typically having more parks. Some city planners argue that digital
technology can compensate for lack of green space through virtual nature experiences,
though critics dispute this claim."

Ask these 5 TFNG questions:
1. People who spend 120 minutes per week in nature reported higher wellbeing.
2. The 2019 research was conducted in urban areas only.
3. Poorer neighbourhoods typically have fewer parks than wealthy ones.
4. All city planners support virtual nature experiences as a solution.
5. Critics believe digital technology can fully replace green spaces.

Score immediately after answers. Format: READING BAND: X.X

═══ TRANSITION ═══
After Reading, say EXACTLY:
"READING COMPLETE. You have finished Parts 1-3. Click the button below to continue to the Listening test."
Then STOP. Do not continue further.

RULES:
- Be encouraging but honest
- Do not inflate scores
- Keep responses concise and clear
- Use simple formatting — no excessive markdown
- If student gives very short answers, note this affects their band score
"""
