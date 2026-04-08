# ============================================================
# modules/practice_listening.py
# Dedicated IELTS Listening practice with ElevenLabs audio
# ============================================================

import streamlit as st
from utils.elevenlabs_audio import get_cached_audio, render_audio_player
from utils.listening_content import LISTENING_SECTIONS
from utils.database import create_session, save_band_score, update_session


def render_listening_practice():
    """Full listening practice module with ElevenLabs audio."""
    profile = st.session_state.get("profile", {})
    accent = profile.get("accent_color", "#4A9EFF")
    user_id = st.session_state.get("user_id", "demo")

    # ── HEADER ──
    st.markdown(f"""
    <div style="margin-bottom:20px">
        <div style="font-size:22px;font-weight:800;color:#fff;margin-bottom:4px">
            🎧 IELTS Listening Practice
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.4)">
            Listen to the audio carefully. You will hear it once only.
            Then answer all questions from memory.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SECTION SELECTOR ──
    sections = list(LISTENING_SECTIONS.keys())
    selected = st.selectbox(
        "Choose a section:",
        sections,
        key="listening_section_select",
        label_visibility="collapsed"
    )

    section_data = LISTENING_SECTIONS[selected]
    script = section_data["script"]
    questions = section_data["questions"]
    answers = section_data["answers"]

    # Difficulty info
    section_colors = {
        "Section 1 — Conversation": "#34D399",
        "Section 2 — Monologue": "#38BDF8",
        "Section 3 — Academic discussion": "#A78BFA",
        "Section 4 — Academic lecture": "#F87171",
    }
    color = section_colors.get(selected, accent)
    difficulty = {
        "Section 1 — Conversation": "Easier — everyday conversation",
        "Section 2 — Monologue": "Medium — talk or announcement",
        "Section 3 — Academic discussion": "Hard — academic discussion",
        "Section 4 — Academic lecture": "Hardest — academic monologue",
    }.get(selected, "")

    st.markdown(f"""
    <div style="background:{color}11;border:1px solid {color}33;border-radius:12px;
                padding:12px 16px;margin-bottom:20px;display:flex;
                align-items:center;justify-content:space-between">
        <div style="font-size:13px;font-weight:700;color:{color}">{selected}</div>
        <div style="font-size:12px;color:rgba(255,255,255,0.4)">{difficulty}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── STATE ──
    state_key = f"listening_state_{selected.replace(' ','_')}"
    if state_key not in st.session_state:
        st.session_state[state_key] = "audio"

    state = st.session_state[state_key]

    # ── AUDIO PHASE ──
    if state == "audio":
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border-radius:14px;
                    border:1px solid rgba(255,255,255,0.08);padding:16px;
                    margin-bottom:16px">
            <div style="font-size:13px;font-weight:700;color:{accent};margin-bottom:8px">
                Instructions
            </div>
            <div style="font-size:13px;color:rgba(255,255,255,0.6);line-height:1.7">
                1. Press play and listen carefully to the entire recording<br>
                2. You will hear the audio <strong style="color:{accent}">once only</strong><br>
                3. Take notes if needed<br>
                4. When finished, click the button below to answer the questions
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Generate audio with caching
        cache_key = f"audio_{selected[:20]}"
        with st.spinner("🎙️ Generating audio with ElevenLabs..."):
            audio_b64 = get_cached_audio(cache_key, script)

        if audio_b64:
            render_audio_player(
                audio_b64,
                title=f"IELTS Listening — {selected}",
                subtitle="Listen once carefully before answering",
                color=color
            )
        else:
            st.error("Audio generation failed. Please check your ElevenLabs API key.")
            return

        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("I have listened — Show Questions →",
                     key=f"done_{state_key}", use_container_width=True):
            st.session_state[state_key] = "questions"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── QUESTIONS PHASE ──
    elif state == "questions":
        st.info("📝 Answer from memory only — do not scroll up to replay audio.")

        all_answered = True
        user_answers = {}

        st.markdown(f"""
        <div style="font-size:14px;font-weight:700;color:{color};margin-bottom:16px">
            Questions — {selected}
        </div>
        """, unsafe_allow_html=True)

        for i, question in enumerate(questions):
            st.markdown(f"""
            <div style="font-size:14px;color:#dde6f0;margin-bottom:6px">
                <strong style="color:{color}">Q{i+1}.</strong> {question}
            </div>
            """, unsafe_allow_html=True)
            ans = st.text_input(
                "", key=f"ans_{state_key}_{i}",
                placeholder="Your answer...",
                label_visibility="collapsed"
            )
            if not ans:
                all_answered = False
            user_answers[i] = ans.strip().lower()
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        if all_answered:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("Submit Answers →",
                         key=f"submit_{state_key}", use_container_width=True):
                st.session_state[f"answers_{state_key}"] = user_answers
                st.session_state[state_key] = "results"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── RESULTS PHASE ──
    elif state == "results":
        user_answers = st.session_state.get(f"answers_{state_key}", {})
        correct = 0
        results = []

        for i, correct_ans in enumerate(answers):
            user_ans = user_answers.get(i, "")
            is_correct = (
                correct_ans.lower() in user_ans or
                user_ans in correct_ans.lower() or
                user_ans == correct_ans.lower()
            )
            if is_correct:
                correct += 1
            results.append({
                "question": questions[i],
                "user": user_answers.get(i, ""),
                "correct": correct_ans,
                "is_correct": is_correct
            })

        score_map = {
            10: 9.0, 9: 8.5, 8: 8.0, 7: 7.5, 6: 7.0,
            5: 6.5, 4: 6.0, 3: 5.5, 2: 5.0, 1: 4.5, 0: 4.0
        }
        band = score_map.get(correct, 5.0)
        pct = int((correct / len(questions)) * 100)

        # Score card
        band_color = "#2ECC71" if band >= 7 else "#F0C040" if band >= 6 else "#E74C3C"
        st.markdown(f"""
        <div style="background:{band_color}11;border:2px solid {band_color}44;
                    border-radius:20px;padding:24px;text-align:center;margin-bottom:20px">
            <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:6px;
                        text-transform:uppercase;letter-spacing:0.06em">
                Your Score
            </div>
            <div style="font-size:52px;font-weight:900;color:{band_color};line-height:1">
                {band}
            </div>
            <div style="font-size:14px;color:rgba(255,255,255,0.5);margin-top:6px">
                {correct}/{len(questions)} correct ({pct}%)
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Answer review
        st.markdown(f"""
        <div style="font-size:13px;font-weight:700;color:{accent};
                    margin-bottom:12px;text-transform:uppercase;letter-spacing:0.06em">
            Answer Review
        </div>
        """, unsafe_allow_html=True)

        for i, r in enumerate(results):
            icon = "✅" if r["is_correct"] else "❌"
            bg = "rgba(46,204,113,0.06)" if r["is_correct"] else "rgba(231,76,60,0.06)"
            border = "rgba(46,204,113,0.2)" if r["is_correct"] else "rgba(231,76,60,0.2)"
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {border};border-radius:10px;
                        padding:10px 14px;margin-bottom:8px">
                <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-bottom:4px">
                    Q{i+1}. {r['question']}
                </div>
                <div style="display:flex;gap:16px;flex-wrap:wrap">
                    <span style="font-size:13px;color:rgba(255,255,255,0.6)">
                        Your answer: <strong style="color:{'#2ECC71' if r['is_correct'] else '#E74C3C'}">{r['user'] or '(blank)'}</strong>
                    </span>
                    {f'<span style="font-size:13px;color:rgba(255,255,255,0.4)">Correct: <strong style="color:#2ECC71">{r["correct"]}</strong></span>' if not r["is_correct"] else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Save score
        if user_id != "demo":
            session_id = create_session(user_id, "Listening", selected, float(profile.get("target_band", 7.0)))
            if session_id:
                save_band_score(user_id, session_id, "listening", band)
                update_session(session_id, {"overall_band": band, "message_count": len(questions)})

        # Try again button
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Try Again", key=f"retry_{state_key}", use_container_width=True):
                st.session_state[state_key] = "audio"
                st.session_state.pop(f"answers_{state_key}", None)
                st.session_state.pop(f"audio_{selected[:20]}", None)
                if "audio_cache" in st.session_state:
                    st.session_state.audio_cache.pop(f"audio_{selected[:20]}", None)
                st.rerun()
        with col2:
            if st.button("📊 Go to Reports", key=f"reports_{state_key}", use_container_width=True):
                st.session_state.current_view = "reports"
                st.rerun()
