# ============================================================
# modules/practice_listening.py
# Dedicated IELTS Listening practice with ElevenLabs audio
#
# BUG 3 FIX (mobile): Audio player and questions are now shown
#   simultaneously. The old hard if/elif "audio"→"questions"
#   phase gate hid questions entirely during playback — on mobile
#   users had no idea questions existed below the player.
#   FIX: Both audio and questions render always. Question inputs
#   are locked (greyed) until user taps "I have listened".
#   Audio player stays visible in both states.
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
            Listen to the audio and answer the questions below.
            Questions are visible while audio plays.
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
    # States: "active" (audio+questions visible, questions locked)
    #         "unlocked" (questions interactive)
    #         "results" (score shown)
    if state_key not in st.session_state:
        st.session_state[state_key] = "active"

    state = st.session_state[state_key]

    # ── AUDIO — always visible in active and unlocked states ──
    if state in ("active", "unlocked"):
        cache_key = f"audio_{selected[:20]}"
        with st.spinner("🎙️ Generating audio..."):
            audio_b64 = get_cached_audio(cache_key, script)

        if audio_b64:
            st.markdown(f"""
            <div style="background:rgba(252,211,77,0.06);border:1px solid rgba(252,211,77,0.25);
                        border-radius:16px;padding:16px;margin-bottom:12px">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
                    <div style="font-size:22px">🎧</div>
                    <div>
                        <div style="font-size:13px;font-weight:700;color:{color}">
                            IELTS Listening — {selected}
                        </div>
                        <div style="font-size:11px;color:rgba(255,255,255,0.4)">
                            {"Tap play, then read the questions below while listening" if state == "active" else "Audio available for review"}
                        </div>
                    </div>
                </div>
                <audio controls style="width:100%;border-radius:10px;accent-color:{color}">
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                    Your browser does not support audio.
                </audio>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Audio generation failed. Please check your ElevenLabs API key.")
            return

        # ── UNLOCK BUTTON (shown only while locked) ──
        if state == "active":
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button(
                "✅ I have listened — unlock answers",
                key=f"done_{state_key}",
                use_container_width=True
            ):
                st.session_state[state_key] = "unlocked"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown(
                '<div style="font-size:12px;color:rgba(180,210,255,0.35);'
                'text-align:center;margin-top:4px">'
                'You can read the questions below while listening</div>',
                unsafe_allow_html=True
            )

        # ── QUESTIONS — always rendered, locked or unlocked ──
        st.markdown(f"""
        <div style="margin-top:20px;margin-bottom:10px">
            <div style="font-size:14px;font-weight:700;color:{color}">
                Questions — {selected}
            </div>
            <div style="font-size:12px;color:rgba(255,255,255,0.35);margin-top:2px">
                {"🔒 Listen to audio first, then tap unlock above" if state == "active" else "Answer from memory"}
            </div>
        </div>
        """, unsafe_allow_html=True)

        user_answers = {}
        all_answered = True

        for i, question in enumerate(questions):
            st.markdown(f"""
            <div style="font-size:14px;color:#dde6f0;margin-bottom:6px">
                <strong style="color:{color}">Q{i+1}.</strong> {question}
            </div>
            """, unsafe_allow_html=True)

            if state == "unlocked":
                ans = st.text_input(
                    "",
                    key=f"ans_{state_key}_{i}",
                    placeholder="Your answer...",
                    label_visibility="collapsed"
                )
                if not ans:
                    all_answered = False
                user_answers[i] = ans.strip().lower()
            else:
                # Locked visual placeholder
                st.markdown(
                    '<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);'
                    'border-radius:8px;padding:10px 14px;font-size:13px;'
                    'color:rgba(180,210,255,0.2);margin-bottom:8px">'
                    '🔒 Unlock after listening</div>',
                    unsafe_allow_html=True
                )
                user_answers[i] = ""

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if state == "unlocked" and all_answered:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("Submit Answers →", key=f"submit_{state_key}", use_container_width=True):
                st.session_state[f"answers_{state_key}"] = user_answers
                st.session_state[state_key] = "results"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        elif state == "unlocked" and not all_answered:
            st.info("Answer all questions to submit.")

    # ── RESULTS PHASE ──
    elif state == "results":
        user_answers = st.session_state.get(f"answers_{state_key}", {})

        correct_count = 0
        results = []
        for i, (question, correct_ans) in enumerate(zip(questions, answers)):
            user_ans = user_answers.get(i, "")
            is_correct = (
                correct_ans.lower().strip() in user_ans.lower() or
                user_ans.lower() in correct_ans.lower().strip()
            ) if user_ans else False
            if is_correct:
                correct_count += 1
            results.append({
                "question": question,
                "user": user_ans,
                "correct": correct_ans,
                "is_correct": is_correct,
            })

        score_map = {
            range(9, 11): 9.0, range(8, 9): 8.5, range(7, 8): 8.0,
            range(6, 7): 7.0, range(5, 6): 6.5, range(4, 5): 6.0,
            range(3, 4): 5.5, range(2, 3): 5.0, range(0, 2): 4.5,
        }
        band = 5.0
        for score_range, b in score_map.items():
            if correct_count in score_range:
                band = b
                break

        st.markdown(f"""
        <div style="background:rgba(74,158,255,0.04);border:1px solid rgba(74,158,255,0.12);
                    border-radius:16px;padding:20px;margin-bottom:20px;text-align:center">
            <div style="font-size:13px;color:rgba(180,210,255,0.5);margin-bottom:4px">Your Score</div>
            <div style="font-size:36px;font-weight:800;color:#4A9EFF;margin-bottom:4px">
                {correct_count}/{len(questions)}
            </div>
            <div style="font-size:18px;font-weight:700;color:#f0f4ff">
                Listening Band: {band}
            </div>
        </div>
        """, unsafe_allow_html=True)

        for r in results:
            bg = "rgba(0,232,122,0.05)" if r["is_correct"] else "rgba(255,58,74,0.05)"
            border = "rgba(0,232,122,0.2)" if r["is_correct"] else "rgba(255,58,74,0.2)"
            icon = "✅" if r["is_correct"] else "❌"
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {border};border-radius:10px;
                        padding:12px 14px;margin-bottom:8px">
                <div style="font-size:13px;color:#dde6f0;margin-bottom:4px">
                    {icon} {r['question']}
                </div>
                <div style="display:flex;gap:16px;flex-wrap:wrap">
                    <span style="font-size:13px;color:rgba(255,255,255,0.6)">
                        Your answer: <strong style="color:{'#2ECC71' if r['is_correct'] else '#E74C3C'}">{r['user'] or '(blank)'}</strong>
                    </span>
                    {f'<span style="font-size:13px;color:rgba(255,255,255,0.4)">Correct: <strong style="color:#2ECC71">{r["correct"]}</strong></span>' if not r["is_correct"] else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)

        if user_id != "demo":
            session_id = create_session(user_id, "Listening", selected, float(profile.get("target_band", 7.0)))
            if session_id:
                save_band_score(user_id, session_id, "listening", band)
                update_session(session_id, {"overall_band": band, "message_count": len(questions)})

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Try Again", key=f"retry_{state_key}", use_container_width=True):
                st.session_state[state_key] = "active"
                st.session_state.pop(f"answers_{state_key}", None)
                if "audio_cache" in st.session_state:
                    st.session_state.audio_cache.pop(f"audio_{selected[:20]}", None)
                st.rerun()
        with col2:
            if st.button("📊 Go to Reports", key=f"reports_{state_key}", use_container_width=True):
                st.session_state.current_view = "reports"
                st.rerun()
