# ============================================================
# ielts_master.py
# Main entry point — Navigation router + top nav
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
        "onboarding_step": 1,
        "diagnostic_messages": [],
        "show_settings_panel": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── CHECK AUTH ──
# If already authenticated, skip auth screen
if st.session_state.current_view == "auth" and st.session_state.get("auth_user"):
    st.session_state.current_view = "dashboard"

# ── INJECT CSS ──
accent = st.session_state.get("profile", {}).get("accent_color", "#F0C040") \
         if st.session_state.get("profile") else "#F0C040"
inject_global_css(accent)

# ── AUTH GATE ──
if st.session_state.current_view == "auth" or not st.session_state.get("profile"):
    from modules.auth import render_auth
    render_auth()
    st.stop()

# ── TOP NAVIGATION BAR ──
profile = st.session_state.get("profile", {})
name = profile.get("full_name", "Student").split()[0]
streak = profile.get("streak_count", 0)
current_view = st.session_state.current_view

nav_left, nav_right = st.columns([8, 1])

with nav_left:
    st.markdown(f"""
    <div class="top-nav">
        <div class="top-nav-brand">
            <svg width="32" height="32" viewBox="0 0 56 56" fill="none">
                <rect width="56" height="56" rx="14" fill="rgba(255,255,255,0.06)"/>
                <polygon points="28,14 46,24 28,34 10,24" fill="rgba(255,255,255,0.08)"
                    stroke="{accent}" stroke-width="2" stroke-linejoin="round"/>
                <line x1="40" y1="27" x2="40" y2="38" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>
                <path d="M34,38 Q40,42 46,38" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>
                <circle cx="43" cy="13" r="1.5" fill="{accent}"/>
            </svg>
            <div>
                <div class="top-nav-brand-text">IELTS Master</div>
                <div class="top-nav-brand-sub">Powered by Claude</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:8px;font-size:13px;color:rgba(255,255,255,0.5)">
            <span>👋 {name}</span>
            <span style="color:{accent};font-weight:700">🔥 {streak}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with nav_right:
    if st.button("⚙️", key="top_gear", help="Settings", use_container_width=True):
        st.session_state.show_settings_panel = not st.session_state.get("show_settings_panel", False)

# ── INLINE SETTINGS PANEL ──
if st.session_state.get("show_settings_panel"):
    from modules.settings import LANGUAGES, ACCENT_OPTIONS
    with st.container():
        st.markdown('<div style="background:rgba(13,27,42,0.97);border:1px solid rgba(255,255,255,0.12);border-radius:20px;padding:20px;margin-bottom:16px;box-shadow:0 16px 48px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:13px;font-weight:700;color:{accent};letter-spacing:0.06em;text-transform:uppercase;margin-bottom:16px'>Quick Settings</div>", unsafe_allow_html=True)

        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            tutor_name = st.text_input("Tutor Name", value=profile.get("tutor_name", "Alex"),
                                       label_visibility="visible", key="qs_tutor")
        with sc2:
            lang = st.selectbox("Language", LANGUAGES,
                                index=LANGUAGES.index(profile.get("response_language", "English"))
                                      if profile.get("response_language") in LANGUAGES else 0,
                                label_visibility="visible", key="qs_lang")
        with sc3:
            acc_label = st.selectbox("Accent", list(ACCENT_OPTIONS.keys()),
                                     index=list(ACCENT_OPTIONS.values()).index(profile.get("accent_color", "#F0C040"))
                                           if profile.get("accent_color") in ACCENT_OPTIONS.values() else 0,
                                     label_visibility="visible", key="qs_accent")
        with sc4:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("Save & Close", key="qs_save", use_container_width=True):
                updates = {
                    "tutor_name": tutor_name,
                    "response_language": lang,
                    "accent_color": ACCENT_OPTIONS[acc_label],
                }
                st.session_state.profile.update(updates)
                if st.session_state.get("user_id") != "demo":
                    from utils.database import update_user_profile
                    update_user_profile(st.session_state.user_id, updates)
                st.session_state.show_settings_panel = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── TAB NAVIGATION ──
nav_tabs = {
    "dashboard": "🏠 Dashboard",
    "practice": "🎯 Practice",
    "reports": "📊 Reports",
    "challenge": "🚀 21-Day",
    "settings": "⚙️ HQ",
}

tab_html = '<div class="nav-tab-bar">'
for view_key, label in nav_tabs.items():
    active_class = "active" if current_view == view_key else ""
    tab_html += f'<span class="nav-tab {active_class}" onclick="">{label}</span>'
tab_html += '</div>'
st.markdown(tab_html, unsafe_allow_html=True)

# Streamlit buttons for navigation (invisible but functional)
t1, t2, t3, t4, t5 = st.columns(5)
with t1:
    if st.button("🏠 Dashboard", key="nav_dash", use_container_width=True):
        st.session_state.current_view = "dashboard"
        st.rerun()
with t2:
    if st.button("🎯 Practice", key="nav_prac", use_container_width=True):
        st.session_state.current_view = "practice"
        st.rerun()
with t3:
    if st.button("📊 Reports", key="nav_rep", use_container_width=True):
        st.session_state.current_view = "reports"
        st.rerun()
with t4:
    if st.button("🚀 21-Day", key="nav_chal", use_container_width=True):
        st.session_state.current_view = "challenge"
        st.rerun()
with t5:
    if st.button("⚙️ HQ", key="nav_hq", use_container_width=True):
        st.session_state.current_view = "settings"
        st.rerun()

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── ROUTER ──
view = st.session_state.current_view

if view == "onboarding":
    from modules.onboarding import render_onboarding
    render_onboarding()

elif view == "dashboard":
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
    st.session_state.current_view = "dashboard"
    st.rerun()