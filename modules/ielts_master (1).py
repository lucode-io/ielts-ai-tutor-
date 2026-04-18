# ============================================================
# ielts_master.py
# Main entry point — Navigation router + top nav
# BUG FIX: Stale session cleared when ?new=1 param present
#           (landing page "Start Free" CTA must link with ?new=1)
# ============================================================

import streamlit as st
from utils.styles import inject_global_css

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="IELTS Master",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── SESSION STATE DEFAULTS ──
def init_state():
    defaults = {
        "current_view": "auth",
        "auth_user": None,
        "profile": None,
        "user_id": None,
        "is_demo": False,
        "practice_messages": [],
        "current_session_id": None,
        "practice_mode": "Speaking - Part 1 (Personal questions)",
        "onboarding_step": 0,
        "diagnostic_messages": [],
        "show_settings_panel": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── BUG 1 FIX: Clear stale session for new visitors from landing page ──
# Landing page CTAs must use: https://ielts-ai-tutor.streamlit.app/?new=1
# This prevents a returning user's cached Supabase session from
# auto-loading on a shared/family phone when a new user taps "Start Free".
_params = st.query_params
if _params.get("new") == "1":
    # Only run the forced sign-out once per page load
    if not st.session_state.get("_new_session_cleared"):
        try:
            from utils.database import get_supabase_client
            _supabase = get_supabase_client()
            _supabase.auth.sign_out()
        except Exception:
            pass
        # Wipe all auth-related session state
        for _k in ["auth_user", "profile", "user_id", "is_demo", "auth_session"]:
            st.session_state[_k] = None if _k != "is_demo" else False
        st.session_state.current_view = "auth"
        st.session_state._new_session_cleared = True
    # Remove the param so reloads don't re-trigger
    st.query_params.clear()

# ── CHECK AUTH ──
if st.session_state.current_view == "auth" and st.session_state.get("auth_user"):
    st.session_state.current_view = "dashboard"

# ── AUTO-RESTORE SESSION (prevents logout on browser back button) ──
# Only runs when NOT a forced new-session request
if not st.session_state.get("profile") and not st.session_state.get("auth_user"):
    try:
        from utils.database import get_supabase_client, get_user_profile
        supabase = get_supabase_client()
        session = supabase.auth.get_session()
        if session and session.user:
            user_id = session.user.id
            profile = get_user_profile(user_id)
            if profile:
                st.session_state.auth_user = session.user
                st.session_state.user_id = user_id
                st.session_state.profile = profile
                if st.session_state.current_view == "auth":
                    st.session_state.current_view = "dashboard"
    except Exception:
        pass

# ── INJECT CSS ──
accent = st.session_state.get("profile", {}).get("accent_color", "#4A9EFF") \
         if st.session_state.get("profile") else "#4A9EFF"
inject_global_css(accent)

# ── AUTH GATE ──
if st.session_state.current_view == "auth" or not st.session_state.get("profile"):
    from modules.auth import render_auth
    render_auth()
    st.stop()

# ── ONBOARDING GATE (skip nav for onboarding) ──
if st.session_state.current_view == "onboarding":
    from modules.onboarding import render_onboarding
    render_onboarding()
    st.stop()

# ── MOCK TEST GATE (full-screen, no nav) ──
if st.session_state.current_view == "mock_test":
    from modules.mock_test import render_mock_test
    render_mock_test()
    st.stop()

# ── TOP NAVIGATION BAR ──
profile = st.session_state.get("profile", {})
name = profile.get("full_name", "Student").split()[0]
streak = profile.get("streak_count", 0)
current_view = st.session_state.current_view

# ── NAV TABS CONFIG ──
nav_tabs = {
    "dashboard": ("🏠", "Dashboard"),
    "practice": ("🎯", "Practice"),
    "reports": ("📊", "Reports"),
    "challenge": ("🚀", "21-Day"),
    "settings": ("⚙️", "HQ"),
}

# Render header
st.markdown(f"""
<div class="im-top-nav">
    <div class="im-top-nav-left">
        <svg width="32" height="32" viewBox="0 0 56 56" fill="none">
            <rect width="56" height="56" rx="14" fill="rgba(255,255,255,0.06)"/>
            <polygon points="28,14 46,24 28,34 10,24" fill="rgba(255,255,255,0.08)"
                stroke="{accent}" stroke-width="2" stroke-linejoin="round"/>
            <line x1="40" y1="27" x2="40" y2="38" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>
            <path d="M34,38 Q40,42 46,38" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>
            <circle cx="43" cy="13" r="1.5" fill="{accent}"/>
        </svg>
        <div>
            <div class="im-brand-text">IELTS Master</div>
            <div class="im-brand-sub">POWERED BY CLAUDE</div>
        </div>
    </div>
    <div class="im-top-nav-right">
        <span class="im-user-badge">👋 {name}</span>
        {f'<span class="im-streak-badge">🔥 {streak}</span>' if streak > 0 else ''}
    </div>
</div>
""", unsafe_allow_html=True)

# ── NAV TABS ──
tab_cols = st.columns(len(nav_tabs))
for col, (view_key, (icon, label)) in zip(tab_cols, nav_tabs.items()):
    is_active = current_view == view_key
    with col:
        btn_style = "btn-primary" if is_active else ""
        st.markdown(f'<div class="im-nav-tab {"im-nav-tab-active" if is_active else ""}">', unsafe_allow_html=True)
        if st.button(f"{icon} {label}", key=f"nav_{view_key}", use_container_width=True):
            st.session_state.current_view = view_key
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── ROUTE TO VIEW ──
view = st.session_state.current_view

if view == "dashboard":
    from modules.dashboard import render_dashboard
    render_dashboard()
elif view == "practice":
    from modules.practice import render_practice
    render_practice()
elif view == "reports":
    from modules.reports import render_reports
    render_reports()
elif view == "challenge":
    from modules.challenge import render_challenge
    render_challenge()
elif view == "settings":
    from modules.settings import render_settings
    render_settings()
elif view == "mock_test":
    from modules.mock_test import render_mock_test
    render_mock_test()
else:
    st.error(f"Unknown view: {view}")
