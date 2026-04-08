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
        "onboarding_step": 0,
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
accent = st.session_state.get("profile", {}).get("accent_color", "#4A9EFF") \
         if st.session_state.get("profile") else "#4A9EFF"
inject_global_css(accent)

# ── AUTH GATE ──
if st.session_state.current_view == "auth" or st.session_state.get("profile") is None:
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

nav_left, nav_right = st.columns([8, 1])

with nav_left:
    st.markdown(f"""<div style="background:rgba(1,1,10,0.92);border-radius:14px;border:1px solid rgba(74,158,255,0.12);padding:12px 24px;display:flex;align-items:center;justify-content:space-between;margin-bottom:16px"><div style="display:flex;align-items:center;gap:10px"><div style="font-size:24px">🎓</div><div><div style="font-size:16px;font-weight:800;color:#f0f4ff;letter-spacing:0.05em">IELTS Master</div><div style="font-size:10px;color:rgba(180,210,255,0.38);letter-spacing:0.1em;text-transform:uppercase">Powered by Claude</div></div></div><div style="display:flex;align-items:center;gap:8px;font-size:13px;color:rgba(255,255,255,0.5)"><span>👋 {name}</span><span style="color:{accent};font-weight:700">🔥 {streak}</span></div></div>""", unsafe_allow_html=True)

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
                                     index=list(ACCENT_OPTIONS.values()).index(profile.get("accent_color", "#4A9EFF"))
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
    "dashboard": ("🏠", "Dashboard"),
    "practice": ("🎯", "Practice"),
    "reports": ("📊", "Reports"),
    "challenge": ("🚀", "21-Day"),
    "settings": ("⚙️", "HQ"),
}

# Style nav buttons to match tab bar design
st.markdown(f"""
<style>
[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {{display:none!important}}
.nav-btn-row {{
    display:flex;gap:4px;background:rgba(74,158,255,0.03);border-radius:12px;
    padding:4px;margin-bottom:16px;border:1px solid rgba(74,158,255,0.08);flex-wrap:wrap;
    justify-content:center
}}
.nav-btn-row .stButton>button {{
    background:transparent!important;border:1px solid transparent!important;
    border-radius:9px!important;font-size:12px!important;font-weight:600!important;
    padding:8px 16px!important;color:rgba(180,210,255,0.45)!important;
    letter-spacing:0.03em!important;min-height:unset!important;
    box-shadow:none!important;transform:none!important
}}
.nav-btn-row .stButton>button:hover {{
    background:rgba(74,158,255,0.06)!important;color:#4A9EFF!important;
    border-color:rgba(74,158,255,0.15)!important;
    box-shadow:none!important;transform:none!important
}}
.nav-btn-row .nav-active .stButton>button {{
    background:rgba(74,158,255,0.1)!important;color:#4A9EFF!important;
    border:1px solid rgba(74,158,255,0.25)!important
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="nav-btn-row">', unsafe_allow_html=True)
nav_cols = st.columns(len(nav_tabs))
for i, (view_key, (icon, label)) in enumerate(nav_tabs.items()):
    with nav_cols[i]:
        is_active = current_view == view_key
        if is_active:
            st.markdown('<div class="nav-active">', unsafe_allow_html=True)
        if st.button(f"{icon} {label}", key=f"nav_{view_key}", use_container_width=True):
            st.session_state.current_view = view_key
            st.rerun()
        if is_active:
            st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── ROUTER ──
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

elif view == "listening":
    from modules.practice_listening import render_listening_practice
    render_listening_practice()

else:
    st.error(f"Unknown view: {view}")
    st.session_state.current_view = "dashboard"
    st.rerun()