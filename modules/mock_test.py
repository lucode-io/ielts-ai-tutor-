# ============================================================
# modules/mock_test.py - Final Mock Test with hash + save
# ============================================================

import streamlit as st
import re
from utils.ai import chat, build_base_prompt
from utils.database import save_band_score, update_session, create_session
from utils.certificate import generate_certificate_html, generate_cert_hash

MOCK_TEST_STAGES = ["intro", "speaking", "writing", "reading", "listening", "results"]

SPEAKING_QUESTIONS = [
    "Tell me about yourself, where you are from, and what you do.",
    "Describe a person who has had a great influence on your life. You should say: who this person is, how you know them, what qualities they have, and explain why they have influenced you so much.",
    "Some people believe technology is making people less social. To what extent do you agree or disagree? Give reasons and specific examples.",
]

WRITING_TASK1_PROMPT = """The graph below shows the percentage of households in owned and rented accommodation in England and Wales between 1918 and 2011.

Owned: 1918=23%, 1939=32%, 1953=38%, 1971=52%, 1981=57%, 1991=67%, 2001=69%, 2011=64%
Rented: 1918=77%, 1939=68%, 1953=62%, 1971=48%, 1981=43%, 1991=33%, 2001=31%, 2011=36%

Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words."""

WRITING_TASK2_PROMPT = """Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime.

Discuss both views and give your own opinion. Write at least 250 words."""

READING_PASSAGE = """The Psychology of Decision Making

Paragraph A
Every day, humans make thousands of decisions. Psychologists have revealed that human decision-making is far more complex and irrational than previously assumed.

Paragraph B
Daniel Kahneman, a Nobel Prize-winning psychologist, proposed that humans operate using two cognitive systems. System 1 is fast, automatic, and emotional, while System 2 is slow, deliberate, and logical. Most everyday decisions are driven by System 1, which relies on cognitive shortcuts known as heuristics. While efficient, these shortcuts can lead to systematic errors in judgment.

Paragraph C
One documented cognitive bias is confirmation bias, whereby individuals search for information that confirms existing beliefs. This bias affects decisions in fields from medicine to finance. A doctor who suspects a particular illness may unconsciously disregard contradictory symptoms.

Paragraph D
Another significant factor is loss aversion. Research indicates that people feel the pain of losing something approximately twice as strongly as the pleasure of gaining something of equal value. This causes investors to hold onto losing stocks far longer than is rational.

Paragraph E
Environmental factors also play a crucial role. A study conducted in 2011 found that judges were significantly more likely to grant parole in the morning and after breaks, with approval rates dropping to nearly zero by the end of each session. This phenomenon, known as decision fatigue, demonstrates that decision quality deteriorates as cognitive resources deplete.

Paragraph F
Despite these limitations, humans have developed strategies to improve decision-making. Breaking decisions into smaller components, seeking diverse perspectives, and introducing deliberate delays have all been shown to improve outcomes. The growing field of behavioural economics applies these insights to design better policies."""

READING_QUESTIONS = [
    ("TRUE/FALSE/NOT GIVEN", "Daniel Kahneman received a Nobel Prize.", "TRUE"),
    ("TRUE/FALSE/NOT GIVEN", "System 2 thinking is faster than System 1.", "FALSE"),
    ("TRUE/FALSE/NOT GIVEN", "Heuristics always lead to poor decision-making.", "FALSE"),
    ("TRUE/FALSE/NOT GIVEN", "Confirmation bias has been observed in medical professionals.", "TRUE"),
    ("TRUE/FALSE/NOT GIVEN", "Loss aversion means people value gains more than losses.", "FALSE"),
    ("TRUE/FALSE/NOT GIVEN", "The parole study was conducted in 2011.", "TRUE"),
    ("TRUE/FALSE/NOT GIVEN", "Decision fatigue only affects judges.", "NOT GIVEN"),
    ("SHORT ANSWER", "What term describes cognitive shortcuts humans use? (max 3 words)", "heuristics"),
    ("SHORT ANSWER", "Which paragraph discusses environmental influences?", "paragraph e"),
    ("SHORT ANSWER", "What field applies decision-making insights to policy design?", "behavioural economics"),
]

LISTENING_SCRIPT = """IELTS Listening — Section 2

Good morning everyone. Welcome to the Riverside Community Centre orientation. My name is Sandra.

The centre was established in 1998 and has been serving the community for over 25 years. We have three main areas: the sports complex, the learning hub, and the arts studio.

The sports complex opens at 6:30 in the morning on weekdays. On weekends, hours are 8am to 8pm. Annual membership is 240 pounds for adults and 120 pounds for students with valid ID.

The learning hub offers over 50 courses ranging from language classes to computer skills. The most popular is our digital photography class, which runs every Tuesday evening. Registration opens the first Monday of each month.

The arts studio on the third floor has recently been renovated and includes a professional recording studio. Community groups pay a subsidised rate of 15 pounds per hour. Private bookings cost 35 pounds per hour.

We currently need volunteers for three roles: reception support, sports coaching, and event organisation. The volunteer coordinator's office is room number 104, located next to the main entrance."""

LISTENING_QUESTIONS = [
    "In what year was the community centre established?",
    "What time does the sports complex open on weekdays?",
    "What is the annual adult membership fee in pounds?",
    "How many courses does the learning hub offer?",
    "On which day does the photography class run?",
    "When does registration for new courses open?",
    "On which floor is the arts studio?",
    "What is the subsidised hourly rate for community groups?",
    "How many volunteer roles are available?",
    "What is the coordinator's room number?",
]

LISTENING_ANSWERS = ["1998", "6:30", "240", "50", "tuesday", "first monday", "third", "15", "three", "104"]


def render_mock_test():
    profile = st.session_state.get("profile", {})
    accent = profile.get("accent_color", "#F0C040")
    target_band = float(profile.get("target_band", 7.0))

    for key, default in [("mock_stage","intro"),("mock_scores",{}),
                          ("mock_messages",[]),("mock_q_index",0),
                          ("mock_answers",{}),("mock_listened",False)]:
        if key not in st.session_state:
            st.session_state[key] = default

    stage = st.session_state.mock_stage
    stage_idx = MOCK_TEST_STAGES.index(stage) if stage in MOCK_TEST_STAGES else 0
    progress = int((stage_idx / (len(MOCK_TEST_STAGES) - 1)) * 100)

    if stage != "intro":
        labels = ["Speaking","Writing","Reading","Listening","Results"]
        st.markdown(f"""
        <div style="margin-bottom:20px">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                <span style="font-size:12px;color:rgba(255,255,255,0.4)">Final Mock Test</span>
                <span style="font-size:12px;color:{accent}">{stage.title()}</span>
            </div>
            <div style="background:rgba(255,255,255,0.08);border-radius:8px;height:6px">
                <div style="width:{progress}%;height:100%;border-radius:8px;background:{accent}"></div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:6px">
                {"".join([f'<span style="font-size:10px;color:{"' + accent + '" if s.lower() == stage else "rgba(255,255,255,0.25)"}">{s}</span>' for s in labels])}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if stage == "intro": _render_intro(profile, accent, target_band)
    elif stage == "speaking": _render_speaking(profile, accent)
    elif stage == "writing": _render_writing(profile, accent)
    elif stage == "reading": _render_reading(profile, accent)
    elif stage == "listening": _render_listening(profile, accent)
    elif stage == "results": _render_results(profile, accent, target_band)


def _render_intro(profile, accent, target_band):
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;padding:48px 32px">
        <div style="font-size:56px;margin-bottom:16px">🏆</div>
        <div style="font-size:26px;font-weight:800;color:#fff;margin-bottom:8px">Final Mock Test</div>
        <div style="font-size:15px;color:rgba(255,255,255,0.5);line-height:1.7;max-width:520px;margin:0 auto 28px">
            You have completed 21 days of training. This test covers all 4 IELTS skills.
            Score <strong style="color:{accent}">Band {target_band}+</strong> to earn your
            <strong style="color:{accent}">Gold Achievement Certificate</strong> with a unique verified hash.
        </div>
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;max-width:380px;margin:0 auto 28px">
            <div style="background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.3);border-radius:12px;padding:14px">
                <div style="font-size:24px;margin-bottom:6px">🎤</div>
                <div style="font-size:13px;font-weight:700;color:#A78BFA">Speaking</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.35)">3 questions + fluency analysis</div>
            </div>
            <div style="background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.3);border-radius:12px;padding:14px">
                <div style="font-size:24px;margin-bottom:6px">✍️</div>
                <div style="font-size:13px;font-weight:700;color:#38BDF8">Writing</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.35)">Task 1 + Task 2 + annotation</div>
            </div>
            <div style="background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.3);border-radius:12px;padding:14px">
                <div style="font-size:24px;margin-bottom:6px">📖</div>
                <div style="font-size:13px;font-weight:700;color:#34D399">Reading</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.35)">10 questions with distractors</div>
            </div>
            <div style="background:rgba(252,211,77,0.1);border:1px solid rgba(252,211,77,0.3);border-radius:12px;padding:14px">
                <div style="font-size:24px;margin-bottom:6px">🎧</div>
                <div style="font-size:13px;font-weight:700;color:#FCD34D">Listening</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.35)">10 questions from memory</div>
            </div>
        </div>
        <div style="background:rgba(240,192,64,0.08);border:1px solid rgba(240,192,64,0.2);border-radius:12px;padding:14px;max-width:380px;margin:0 auto 24px;font-size:13px;color:rgba(255,255,255,0.6)">
            🏆 Gold Certificate: Score Band {target_band}+ — includes verified hash<br>
            🥈 Silver Certificate: Complete the test (any score)
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("Start Final Mock Test", key="start_mock", use_container_width=False):
        for k in list(st.session_state.keys()):
            if k.startswith("mock_") and k != "mock_stage":
                del st.session_state[k]
        st.session_state.mock_stage = "speaking"
        st.session_state.mock_q_index = 0
        st.session_state.mock_scores = {}
        st.session_state.mock_answers = {}
        st.session_state.mock_listened = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Back to Challenge", key="back_challenge"):
        st.session_state.current_view = "challenge"
        st.rerun()


def _render_speaking(profile, accent):
    st.markdown(f"""
    <div style="font-size:20px;font-weight:700;color:#A78BFA;margin-bottom:4px">Speaking Test</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:20px">
        Answer all 3 questions fully. Part 2 requires at least 4 sentences or Fluency is capped at 5.5.
    </div>
    """, unsafe_allow_html=True)

    q_idx = st.session_state.mock_q_index

    for i, q in enumerate(SPEAKING_QUESTIONS):
        answered = f"speaking_q{i}" in st.session_state.mock_answers
        color = "#2ECC71" if answered else "#A78BFA"
        status = "Answered ✓" if answered else ("Current" if i == q_idx else "Pending")

        st.markdown(f"""
        <div style="background:rgba(167,139,250,0.06);border:1px solid rgba(167,139,250,{'0.3' if i == q_idx else '0.1'});
                    border-radius:14px;padding:14px;margin-bottom:10px">
            <div style="font-size:11px;font-weight:700;color:{color};text-transform:uppercase;
                        letter-spacing:0.06em;margin-bottom:6px">Question {i+1} — {status}</div>
            <div style="font-size:14px;color:#dde6f0">{q}</div>
        </div>
        """, unsafe_allow_html=True)

        if i == q_idx and not answered:
            answer = st.text_area(f"Your answer:", height=100, key=f"spk_input_{i}",
                                  placeholder="Write at least 3-4 sentences...")
            if st.button(f"Submit Answer {i+1}", key=f"spk_submit_{i}"):
                if answer and len(answer.split()) > 15:
                    st.session_state.mock_answers[f"speaking_q{i}"] = answer
                    st.session_state.mock_q_index = i + 1
                    st.rerun()
                else:
                    st.warning("Please write a more complete answer.")

    if all(f"speaking_q{i}" in st.session_state.mock_answers for i in range(3)):
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Score Speaking and Continue", key="score_speaking"):
            with st.spinner("AI is scoring your Speaking with Fluency Gap Analysis..."):
                score = _score_speaking(profile)
            st.session_state.mock_scores["speaking"] = score
            st.session_state.mock_stage = "writing"
            st.session_state.mock_q_index = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def _render_writing(profile, accent):
    st.markdown(f"""
    <div style="font-size:20px;font-weight:700;color:#38BDF8;margin-bottom:4px">Writing Test</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:20px">
        Task 1: min 150 words. Task 2: min 250 words. 3-color annotation will be applied.
    </div>
    """, unsafe_allow_html=True)

    t1_done = "writing_t1" in st.session_state.mock_answers
    t2_done = "writing_t2" in st.session_state.mock_answers

    with st.expander("Task 1 — Graph Description" + (" ✅" if t1_done else ""), expanded=not t1_done):
        st.markdown(f"""
        <div style="background:rgba(56,189,248,0.06);border:1px solid rgba(56,189,248,0.2);
                    border-radius:12px;padding:14px;margin-bottom:12px;font-size:13px;color:#dde6f0;line-height:1.7">
            {WRITING_TASK1_PROMPT}
        </div>
        """, unsafe_allow_html=True)
        if not t1_done:
            t1 = st.text_area("Your Task 1 response:", height=200, key="wrt_t1",
                              placeholder="Write at least 150 words...")
            wc1 = len(t1.split()) if t1 else 0
            color1 = "#2ECC71" if wc1 >= 150 else "#F0C040" if wc1 >= 100 else "#E74C3C"
            st.markdown(f"<div style='font-size:12px;color:{color1}'>Word count: {wc1} / 150 minimum</div>",
                        unsafe_allow_html=True)
            if st.button("Submit Task 1", key="submit_t1"):
                if wc1 >= 100:
                    st.session_state.mock_answers["writing_t1"] = t1
                    st.rerun()
                else:
                    st.warning("Please write at least 100 words.")

    with st.expander("Task 2 — Essay" + (" ✅" if t2_done else ""), expanded=t1_done and not t2_done):
        st.markdown(f"""
        <div style="background:rgba(56,189,248,0.06);border:1px solid rgba(56,189,248,0.2);
                    border-radius:12px;padding:14px;margin-bottom:12px;font-size:13px;color:#dde6f0;line-height:1.7">
            {WRITING_TASK2_PROMPT}
        </div>
        """, unsafe_allow_html=True)
        if not t2_done:
            t2 = st.text_area("Your Task 2 response:", height=250, key="wrt_t2",
                              placeholder="Write at least 250 words...")
            wc2 = len(t2.split()) if t2 else 0
            color2 = "#2ECC71" if wc2 >= 250 else "#F0C040" if wc2 >= 200 else "#E74C3C"
            st.markdown(f"<div style='font-size:12px;color:{color2}'>Word count: {wc2} / 250 minimum</div>",
                        unsafe_allow_html=True)
            if st.button("Submit Task 2", key="submit_t2"):
                if wc2 >= 200:
                    st.session_state.mock_answers["writing_t2"] = t2
                    st.rerun()
                else:
                    st.warning("Please write at least 200 words.")

    if t1_done and t2_done:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Score Writing and Continue", key="score_writing"):
            with st.spinner("AI is scoring with 3-color annotation + P-R-E-A analysis..."):
                score = _score_writing(profile)
            st.session_state.mock_scores["writing"] = score
            st.session_state.mock_stage = "reading"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def _render_reading(profile, accent):
    st.markdown(f"""
    <div style="font-size:20px;font-weight:700;color:#34D399;margin-bottom:4px">Reading Test</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:16px">
        Read the passage carefully, then answer all 10 questions.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Reading Passage — The Psychology of Decision Making", expanded=True):
        for para in READING_PASSAGE.strip().split("\n\n"):
            if para.strip():
                lines = para.strip().split("\n")
                if lines[0].startswith("Paragraph"):
                    st.markdown(f"**{lines[0]}**")
                    st.markdown(" ".join(lines[1:]))
                else:
                    st.markdown(para)

    st.markdown(f"""
    <div style="font-size:14px;font-weight:700;color:#34D399;margin:16px 0 12px">Questions</div>
    """, unsafe_allow_html=True)

    all_answered = True
    for i, (qtype, question, _) in enumerate(READING_QUESTIONS):
        key = f"reading_q{i}"
        st.markdown(f"""
        <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-bottom:4px">Q{i+1} — {qtype}</div>
        <div style="font-size:14px;color:#dde6f0;margin-bottom:6px">{question}</div>
        """, unsafe_allow_html=True)
        if qtype == "TRUE/FALSE/NOT GIVEN":
            ans = st.selectbox("", ["","TRUE","FALSE","NOT GIVEN"],
                               key=key, label_visibility="collapsed")
        else:
            ans = st.text_input("", key=key, placeholder="Your answer...",
                                label_visibility="collapsed")
        if not ans:
            all_answered = False
        else:
            st.session_state.mock_answers[key] = ans
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if all_answered:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Submit Reading and Continue", key="submit_reading"):
            score = _score_reading()
            st.session_state.mock_scores["reading"] = score
            st.session_state.mock_stage = "listening"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def _render_listening(profile, accent):
    listened = st.session_state.get("mock_listened", False)

    st.markdown(f"""
    <div style="font-size:20px;font-weight:700;color:#FCD34D;margin-bottom:4px">Listening Test</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:16px">
        Read the script ONCE only. Then answer all 10 questions from memory.
    </div>
    """, unsafe_allow_html=True)

    if not listened:
        st.markdown(f"""
        <div style="background:rgba(252,211,77,0.06);border:1px solid rgba(252,211,77,0.2);
                    border-radius:14px;padding:20px;margin-bottom:16px">
            <div style="font-size:13px;font-weight:700;color:#FCD34D;margin-bottom:12px">
                LISTENING SCRIPT — Read once carefully
            </div>
            <div style="font-size:13px;color:#dde6f0;line-height:1.8;white-space:pre-line">{LISTENING_SCRIPT}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("I Have Read It — Show Questions", key="done_reading_script"):
            st.session_state.mock_listened = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.info("Answer from memory only — do not scroll up to check the script.")

    all_answered = True
    for i, question in enumerate(LISTENING_QUESTIONS):
        key = f"listening_q{i}"
        st.markdown(f"""
        <div style="font-size:14px;color:#dde6f0;margin-bottom:6px">
            <strong style="color:#FCD34D">Q{i+1}.</strong> {question}
        </div>
        """, unsafe_allow_html=True)
        ans = st.text_input("", key=key, placeholder="Your answer...",
                            label_visibility="collapsed")
        if not ans:
            all_answered = False
        else:
            st.session_state.mock_answers[key] = ans
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    if all_answered:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Submit Listening and See Results", key="submit_listening"):
            score = _score_listening()
            st.session_state.mock_scores["listening"] = score
            st.session_state.mock_stage = "results"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def _render_results(profile, accent, target_band):
    scores = st.session_state.mock_scores
    speaking = scores.get("speaking", 0)
    writing = scores.get("writing", 0)
    reading = scores.get("reading", 0)
    listening = scores.get("listening", 0)

    if all([speaking, writing, reading, listening]):
        overall = round((speaking + writing + reading + listening) / 4 * 2) / 2
    else:
        overall = 0

    achieved = overall >= target_band
    cert_type = "gold" if achieved else "silver"

    # Generate and save certificate hash
    user_id = st.session_state.get("user_id", "demo")
    full_name = profile.get("full_name", "Student")

    if not st.session_state.get("mock_cert_hash"):
        cert_hash = generate_cert_hash(user_id, full_name, overall, cert_type)
        st.session_state.mock_cert_hash = cert_hash

        # Save to DB
        if user_id != "demo" and not st.session_state.get("mock_scores_saved"):
            from utils.database import save_certificate
            save_certificate(
                user_id=user_id,
                cert_hash=cert_hash,
                full_name=full_name,
                target_band=target_band,
                achieved_band=overall,
                cert_type=cert_type,
                scores={"speaking": speaking, "writing": writing,
                        "reading": reading, "listening": listening}
            )
            session_id = create_session(user_id, "Final Mock Test", "All Skills", target_band)
            if session_id:
                for skill, score in [("speaking", speaking), ("writing", writing),
                                      ("reading", reading), ("listening", listening)]:
                    save_band_score(user_id, session_id, skill, score)
                save_band_score(user_id, session_id, "overall", overall)
            st.session_state.mock_scores_saved = True
    else:
        cert_hash = st.session_state.mock_cert_hash

    # Result banner
    if achieved:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(240,192,64,0.15),rgba(240,192,64,0.05));
                    border:2px solid {accent};border-radius:20px;padding:32px;text-align:center;margin-bottom:24px">
            <div style="font-size:52px;margin-bottom:12px">🏆</div>
            <div style="font-size:26px;font-weight:800;color:{accent};margin-bottom:8px">Congratulations! Target Achieved!</div>
            <div style="font-size:15px;color:rgba(255,255,255,0.6);margin-bottom:8px">
                You scored <strong style="color:{accent}">Band {overall}</strong> — target was Band {target_band}.
            </div>
            <div style="font-size:13px;color:rgba(255,255,255,0.4)">
                Your Gold Certificate is ready. Certificate code: <strong style="color:{accent}">{cert_hash}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                    border-radius:20px;padding:32px;text-align:center;margin-bottom:24px">
            <div style="font-size:52px;margin-bottom:12px">🥈</div>
            <div style="font-size:26px;font-weight:800;color:#fff;margin-bottom:8px">21 Days Completed</div>
            <div style="font-size:15px;color:rgba(255,255,255,0.5);margin-bottom:8px">
                You scored <strong style="color:#fff">Band {overall}</strong> — target was Band {target_band}.
            </div>
            <div style="font-size:13px;color:rgba(255,255,255,0.4)">Keep training and retry to earn your Gold Certificate.</div>
        </div>
        """, unsafe_allow_html=True)

    # Score breakdown
    c1, c2, c3, c4 = st.columns(4)
    for col, skill, score, color in zip(
        [c1, c2, c3, c4],
        ["Speaking","Writing","Reading","Listening"],
        [speaking, writing, reading, listening],
        ["#A78BFA","#38BDF8","#34D399","#FCD34D"]
    ):
        with col:
            st.markdown(f"""
            <div style="background:{color}11;border:1px solid {color}33;border-radius:14px;
                        padding:14px;text-align:center">
                <div style="font-size:11px;color:{color};text-transform:uppercase;
                            letter-spacing:0.06em;margin-bottom:6px">{skill}</div>
                <div style="font-size:28px;font-weight:800;color:{color}">{score}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;margin:20px 0">
        <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:6px">Overall Band Score</div>
        <div style="font-size:52px;font-weight:900;color:{'#F0C040' if achieved else '#fff'}">{overall}</div>
        <div style="font-size:13px;color:rgba(255,255,255,0.35)">Target: Band {target_band}</div>
    </div>
    """, unsafe_allow_html=True)

    # Certificate download
    cert_html = generate_certificate_html(
        full_name=full_name,
        target_band=target_band,
        achieved_band=overall,
        cert_type=cert_type,
        cert_hash=cert_hash,
        scores={"speaking": speaking, "writing": writing,
                "reading": reading, "listening": listening}
    )
    label = "🏆 Download Gold Certificate" if achieved else "🥈 Download Silver Certificate"
    st.download_button(
        label=label, data=cert_html,
        file_name=f"IELTS_Master_Certificate_{full_name.replace(' ','_')}.html",
        mime="text/html", key="dl_final_cert"
    )
    st.caption(f"Certificate code: **{cert_hash}** — Verify at: ielts-ai-tutor.streamlit.app/?verify={cert_hash}")

    if not achieved:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("Retry Challenge", key="retry_challenge"):
            for key in list(st.session_state.keys()):
                if key.startswith("mock_"):
                    del st.session_state[key]
            st.session_state.current_view = "challenge"
            st.rerun()


def _score_speaking(profile) -> float:
    answers = st.session_state.mock_answers
    combined = "\n\n".join([
        f"Q{i+1}: {SPEAKING_QUESTIONS[i]}\nAnswer: {answers.get(f'speaking_q{i}','')}"
        for i in range(3)
    ])
    system = build_base_prompt(profile) + """
You are a STRICT IELTS Speaking examiner [FINAL MOCK TEST].
Score these 3 answers holistically using 2026 IELTS Band Descriptors.
If Part 2 answer has fewer than 4 sentences, cap Fluency at 5.5.
Return ONLY a number between 3.0 and 9.0 in 0.5 increments. Example: "6.5"
"""
    response = chat([{"role": "user", "content": combined}], system, max_tokens=10)
    return _extract_score(response, 5.5)


def _score_writing(profile) -> float:
    t1 = st.session_state.mock_answers.get("writing_t1", "")
    t2 = st.session_state.mock_answers.get("writing_t2", "")
    system = build_base_prompt(profile) + """
You are a STRICT IELTS Writing examiner [FINAL MOCK TEST].
Score Task 1 (graph about owned vs rented accommodation) and Task 2 (crime/prison sentences) holistically.
Apply 2026 Band Descriptors strictly. Apply P-R-E-A check to Task 2.
Return ONLY a number between 3.0 and 9.0 in 0.5 increments. Example: "5.5"
"""
    content = f"TASK 1:\n{t1}\n\nTASK 2:\n{t2}"
    response = chat([{"role": "user", "content": content}], system, max_tokens=10)
    return _extract_score(response, 5.5)


def _score_reading() -> float:
    correct = sum(
        1 for i, (_, _, ans) in enumerate(READING_QUESTIONS)
        if st.session_state.mock_answers.get(f"reading_q{i}", "").strip().lower() == ans.lower()
    )
    return {10:9.0,9:8.5,8:8.0,7:7.5,6:7.0,5:6.5,4:6.0,3:5.5,2:5.0,1:4.5,0:4.0}.get(correct, 5.0)


def _score_listening() -> float:
    correct = sum(
        1 for i, ans in enumerate(LISTENING_ANSWERS)
        if ans.lower() in st.session_state.mock_answers.get(f"listening_q{i}", "").strip().lower()
        or st.session_state.mock_answers.get(f"listening_q{i}", "").strip().lower() in ans.lower()
    )
    return {10:9.0,9:8.5,8:8.0,7:7.5,6:7.0,5:6.5,4:6.0,3:5.5,2:5.0,1:4.5,0:4.0}.get(correct, 5.0)


def _extract_score(text: str, default: float = 5.5) -> float:
    matches = re.findall(r'\b([3-9]\.?[05]?)\b', text)
    for m in matches:
        try:
            v = float(m)
            if 3.0 <= v <= 9.0:
                return round(v * 2) / 2
        except Exception:
            pass
    return default
