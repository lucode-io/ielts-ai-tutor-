# ============================================================
# modules/onboarding.py
# First-time user onboarding and diagnostic test
# ============================================================

import streamlit as st
from utils.ai import chat, diagnostic_prompt
from utils.database import save_diagnostic, update_user_profile


def render_onboarding():
    """Render the onboarding flow for new users."""
    profile = st.session_state.get("profile", {})
    accent = profile.get("accent_color", "#F0C040")
    user_id = st.session_state.get("user_id", "demo")
    name = profile.get("full_name", "Student").split()[0]

    step = st.session_state.get("onboarding_step", 1)

    if step == 1:
        _render_welcome_step(name, accent)
    elif step == 2:
        _render_diagnostic_step(profile, user_id, accent)


def _render_welcome_step(name, accent):
    """Welcome screen with options."""
    st.markdown(f"""
    <div style="max-width:600px;margin:40px auto 0;text-align:center">
        <div style="font-size:52px;margin-bottom:16px">🎓</div>
        <div style="font-size:28px;font-weight:800;color:#fff;margin-bottom:8px">
            Welcome, {name}!
        </div>
        <div style="font-size:16px;color:rgba(255,255,255,0.5);margin-bottom:32px;line-height:1.7">
            Before we start, let's find out your current IELTS level.
            This 15-minute diagnostic test covers all 4 skills and sets your
            <strong style="color:{accent}">Baseline Band Score</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("🚀 Take Diagnostic Test (15 min)", use_container_width=True, key="start_diag"):
            st.session_state.onboarding_step = 2
            st.session_state.diagnostic_messages = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Skip — I know my level", use_container_width=True, key="skip_diag"):
            st.session_state.current_view = "dashboard"
            st.rerun()

    # What to expect
    st.markdown(f"""
    <div style="max-width:600px;margin:32px auto 0">
        <div style="font-size:13px;font-weight:700;color:{accent};
                    letter-spacing:0.06em;text-transform:uppercase;margin-bottom:12px">
            What the test covers
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
    """, unsafe_allow_html=True)

    skills = [
        ("🎤", "Speaking", "3 Part 1 questions", "#A78BFA"),
        ("✍️", "Writing", "Short Task 2 intro", "#38BDF8"),
        ("📖", "Reading", "TFNG passage", "#34D399"),
        ("🎧", "Listening", "Script recall test", "#FCD34D"),
    ]
    for icon, skill, desc, color in skills:
        st.markdown(f"""
        <div style="background:{color}11;border:1px solid {color}33;border-radius:14px;
                    padding:14px;text-align:center">
            <div style="font-size:24px;margin-bottom:6px">{icon}</div>
            <div style="font-size:13px;font-weight:700;color:{color}">{skill}</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-top:4px">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


def _render_diagnostic_step(profile, user_id, accent):
    """Render the diagnostic test chat."""
    if "diagnostic_messages" not in st.session_state:
        st.session_state.diagnostic_messages = []

    # Auto-start if no messages
    if not st.session_state.diagnostic_messages:
        system = diagnostic_prompt()
        starter = [{"role": "user", "content": "Please start my baseline assessment."}]
        with st.spinner("Starting your diagnostic test..."):
            response = chat(starter, system, max_tokens=1500)
        st.session_state.diagnostic_messages.append({"role": "user", "content": "Please start my baseline assessment."})
        st.session_state.diagnostic_messages.append({"role": "assistant", "content": response})

    st.markdown(f"""
    <div style="margin-bottom:16px">
        <div style="font-size:18px;font-weight:700;color:#fff">Diagnostic Test</div>
        <div style="font-size:13px;color:rgba(255,255,255,0.4)">
            Complete all sections to get your baseline band score.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.diagnostic_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Check if diagnostic is complete
    last_msg = st.session_state.diagnostic_messages[-1]["content"] if st.session_state.diagnostic_messages else ""
    if "DIAGNOSTIC BASELINE ASSESSMENT" in last_msg or "Overall Baseline:" in last_msg:
        import re
        scores = {}
        for skill in ["Speaking", "Writing", "Reading", "Listening", "Overall"]:
            match = re.search(rf"{skill} Band[:\s]+(\d+\.?\d*)", last_msg)
            if match:
                scores[skill.lower()] = float(match.group(1))

        if scores:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("✅ Save Results & Go to Dashboard", key="save_diag", use_container_width=False):
                if user_id != "demo":
                    save_diagnostic(user_id, scores)
                    updated_profile = {**profile, "baseline_band": scores.get("overall", 5.5)}
                    st.session_state.profile = updated_profile
                st.session_state.current_view = "dashboard"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # Input
    user_input = st.chat_input("Type your answer here...")
    if user_input:
        st.session_state.diagnostic_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Evaluating..."):
                system = diagnostic_prompt()
                response = chat(st.session_state.diagnostic_messages, system, max_tokens=1500)
            st.markdown(response)
        st.session_state.diagnostic_messages.append({"role": "assistant", "content": response})
        st.rerun()
