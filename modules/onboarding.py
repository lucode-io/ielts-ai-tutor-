# ============================================================
# modules/onboarding.py
# First-time user onboarding and diagnostic test
# Mobile optimized
# ============================================================

import streamlit as st
import re
from utils.ai import chat, diagnostic_prompt
from utils.database import save_diagnostic, update_user_profile


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


def _render_welcome(name, accent):
    st.markdown(f"""
    <div style="text-align:center;padding:32px 16px 24px">
        <div style="font-size:48px;margin-bottom:12px">🎓</div>
        <div style="font-size:24px;font-weight:800;color:#fff;margin-bottom:8px">
            Welcome, {name}!
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.5);line-height:1.7;
                    max-width:480px;margin:0 auto 28px">
            Before we start, let's find out your current IELTS level.
            This 15-minute diagnostic covers all 4 skills and sets your
            <strong style="color:{accent}">Baseline Band Score</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Responsive columns — full width on mobile
    col = st.columns([0.1, 0.8, 0.1])[1]
    with col:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("🚀 Take Diagnostic Test (15 min)",
                     use_container_width=True, key="start_diag"):
            st.session_state.onboarding_step = 2
            st.session_state.diagnostic_messages = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Skip — I'll set my level manually",
                     use_container_width=True, key="skip_diag"):
            st.session_state.current_view = "dashboard"
            st.rerun()

    # Skills preview — responsive grid
    st.markdown(f"""
    <div style="max-width:560px;margin:28px auto 0">
        <div style="font-size:12px;font-weight:700;color:{accent};
                    letter-spacing:0.08em;text-transform:uppercase;
                    margin-bottom:12px;text-align:center">
            What the test covers
        </div>
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px">
    """, unsafe_allow_html=True)

    skills = [
        ("🎤", "Speaking", "3 Part 1 questions", "#A78BFA"),
        ("✍️", "Writing", "Short Task 2 intro", "#38BDF8"),
        ("📖", "Reading", "TFNG passage", "#34D399"),
        ("🎧", "Listening", "Script recall test", "#FCD34D"),
    ]
    for icon, skill, desc, color in skills:
        st.markdown(f"""
        <div style="background:{color}11;border:1px solid {color}33;
                    border-radius:12px;padding:14px;text-align:center">
            <div style="font-size:22px;margin-bottom:6px">{icon}</div>
            <div style="font-size:13px;font-weight:700;color:{color}">{skill}</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-top:3px">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


def _render_diagnostic(profile, user_id, accent):
    if "diagnostic_messages" not in st.session_state:
        st.session_state.diagnostic_messages = []

    # Auto-start with first message
    if not st.session_state.diagnostic_messages:
        system = diagnostic_prompt()
        starter = [{"role": "user", "content": "Please start my baseline assessment."}]
        with st.spinner("Starting your diagnostic test..."):
            response = chat(starter, system, max_tokens=1500)
        if response.startswith("ERROR"):
            st.error(response)
            if st.button("Go to Dashboard", key="skip_error"):
                st.session_state.current_view = "dashboard"
                st.rerun()
            return
        st.session_state.diagnostic_messages = [
            {"role": "user", "content": "Please start my baseline assessment."},
            {"role": "assistant", "content": response}
        ]

    st.markdown(f"""
    <div style="margin-bottom:16px">
        <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:4px">
            Diagnostic Test
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.4)">
            Complete all sections to get your baseline band score.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.diagnostic_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Check if complete
    last_msg = st.session_state.diagnostic_messages[-1]["content"] \
        if st.session_state.diagnostic_messages else ""

    is_complete = (
        "DIAGNOSTIC BASELINE ASSESSMENT" in last_msg or
        "Overall Baseline:" in last_msg or
        "overall_band" in last_msg.lower()
    )

    if is_complete:
        scores = {}
        for skill in ["Speaking", "Writing", "Reading", "Listening", "Overall"]:
            match = re.search(rf"{skill}[^:]*?Band[:\s]+(\d+\.?\d*)", last_msg, re.IGNORECASE)
            if not match:
                match = re.search(rf"{skill}[:\s]+(\d+\.?\d*)", last_msg, re.IGNORECASE)
            if match:
                scores[skill.lower()] = float(match.group(1))

        if scores:
            overall = scores.get("overall", scores.get("speaking", 5.5))
            st.markdown(f"""
            <div style="background:rgba(240,192,64,0.08);border:1px solid rgba(240,192,64,0.3);
                        border-radius:16px;padding:20px;text-align:center;margin:16px 0">
                <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:6px">
                    Your Baseline Band Score
                </div>
                <div style="font-size:44px;font-weight:900;color:{accent}">{overall}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("✅ Save Results & Go to Dashboard",
                         key="save_diag", use_container_width=True):
                if user_id != "demo":
                    save_diagnostic(user_id, scores)
                st.session_state.profile = {
                    **profile,
                    "baseline_band": overall
                }
                st.session_state.current_view = "dashboard"
                st.session_state.onboarding_step = 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # Text input
    user_input = st.chat_input("Type your answer here...")
    if user_input:
        st.session_state.diagnostic_messages.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Evaluating..."):
                system = diagnostic_prompt()
                response = chat(
                    st.session_state.diagnostic_messages,
                    system, max_tokens=1500
                )
            st.markdown(response)
        st.session_state.diagnostic_messages.append(
            {"role": "assistant", "content": response}
        )
        st.rerun()
