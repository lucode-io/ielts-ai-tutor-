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
if st.session_state.current_view == "auth" and st.session_state.get("auth_user"):
    st.session_state.current_view = "dashboard"

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

# Build nav items HTML
nav_items_html = ""
for view_key, (icon, label) in nav_tabs.items():
    active_cls = "active" if current_view == view_key else ""
    nav_items_html += f'<button class="im-nav-tab {active_cls}" onclick="window.__imNav(\'{view_key}\')">{icon} {label}</button>'

# Render header + nav as a single HTML block — guaranteed to display
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
        <span class="im-streak-badge">🔥 {streak}</span>
    </div>
</div>
<div class="im-nav-bar">
    {nav_items_html}
</div>
""", unsafe_allow_html=True)

# Hidden Streamlit buttons to receive nav clicks from JS
nav_container = st.container()
with nav_container:
    nav_cols = st.columns(len(nav_tabs))
    for i, view_key in enumerate(nav_tabs.keys()):
        with nav_cols[i]:
            if st.button(f"nav_{view_key}", key=f"nav_{view_key}", use_container_width=True):
                st.session_state.current_view = view_key
                st.session_state.show_settings_panel = False
                st.rerun()

# Hide the hidden nav buttons with a unique wrapper
st.markdown("""
<style>
/* Hide ONLY the hidden relay nav buttons, not all horizontal blocks */
div[data-testid="stHorizontalBlock"]:has(button[key^="nav_"]) {
    position: absolute !important;
    opacity: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
}
</style>
<script>
window.__imNav = function(view) {
    // Find the hidden Streamlit button and click it
    const buttons = document.querySelectorAll('button[kind="secondary"]');
    for (const btn of buttons) {
        if (btn.textContent.trim() === 'nav_' + view) {
            btn.click();
            return;
        }
    }
};
</script>
""", unsafe_allow_html=True)

# ── INLINE SETTINGS PANEL ──
if st.session_state.get("show_settings_panel"):
    from modules.settings import LANGUAGES, ACCENT_OPTIONS
    with st.container():
        st.markdown(f"""
        <div style="background:rgba(13,27,42,0.97);border:1px solid rgba(74,158,255,0.15);
                    border-radius:20px;padding:20px;margin-bottom:16px;
                    box-shadow:0 16px 48px rgba(0,0,0,0.5);">
            <div style="font-size:13px;font-weight:700;color:{accent};
                        letter-spacing:0.06em;text-transform:uppercase;margin-bottom:16px">
                Quick Settings
            </div>
        """, unsafe_allow_html=True)

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
