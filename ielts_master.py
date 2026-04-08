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
        <span class="im-streak-badge">🔥 {streak}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── REAL STREAMLIT NAV BUTTONS (styled as tab bar) ──
nav_cols = st.columns(len(nav_tabs))
for i, (view_key, (icon, label)) in enumerate(nav_tabs.items()):
    with nav_cols[i]:
        is_active = current_view == view_key
        # Style active tab differently
        btn_type = "primary" if is_active else "secondary"
        if st.button(f"{icon} {label}", key=f"nav_{view_key}", use_container_width=True, type=btn_type):
            st.session_state.current_view = view_key
            st.session_state.show_settings_panel = False
            st.rerun()

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

# ── PAYWALL GATE ──────────────────────────────────────────────
# Free users get 7 sessions. After that, block practice + listening + challenge.
FREE_SESSION_LIMIT = 7
CHECKOUT_URL = "https://ieltsmaster-org.lemonsqueezy.com/checkout/buy/138f5144-e21e-4692-8631-feeee456bbbf"

def _check_paywall(user_id, profile):
    """Returns True if user is blocked by paywall. Shows upgrade wall."""
    if user_id == "demo":
        return False
    if profile.get("subscription_status") in ("lifetime", "pro", "paid"):
        return False

    from utils.database import get_session_count
    count = get_session_count(user_id)

    # Cache count in session_state so dashboard can show remaining
    st.session_state["_session_count"] = count

    if count < FREE_SESSION_LIMIT:
        # Show soft reminder at sessions 5 and 6
        remaining = FREE_SESSION_LIMIT - count
        if remaining <= 2:
            st.markdown(f"""
            <div style="background:rgba(240,192,64,0.08);border:1px solid rgba(240,192,64,0.2);
                        border-radius:12px;padding:12px 16px;margin-bottom:16px;
                        display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
                <div style="font-size:13px;color:#FCD34D">
                    ⚡ <strong>{remaining} free session{'s' if remaining != 1 else ''} remaining</strong>
                </div>
                <div style="font-size:12px;color:rgba(180,210,255,0.45)">
                    Upgrade to Lifetime for unlimited access
                </div>
            </div>
            """, unsafe_allow_html=True)
        return False

    # ── BLOCKED — show upgrade wall ──
    st.markdown(f"""
    <div style="text-align:center;padding:48px 20px;max-width:480px;margin:0 auto">
        <div style="font-size:56px;margin-bottom:16px">🔒</div>
        <div style="font-family:'Syne',sans-serif;font-size:24px;font-weight:800;
                    color:#f0f4ff;margin-bottom:10px">
            Free sessions used up
        </div>
        <div style="font-size:14px;color:rgba(180,210,255,0.5);line-height:1.7;margin-bottom:24px">
            You've completed <strong style="color:#4A9EFF">{count} sessions</strong> — great progress!
            Upgrade to Lifetime to continue practicing all 4 skills with your AI tutor, forever.
        </div>
        <div style="background:rgba(74,158,255,0.06);border:1px solid rgba(74,158,255,0.15);
                    border-radius:16px;padding:24px;margin-bottom:24px">
            <div style="font-size:36px;font-weight:900;color:#4A9EFF;margin-bottom:4px">$149</div>
            <div style="font-size:13px;color:rgba(180,210,255,0.5)">One-time payment · Lifetime access · All 4 skills</div>
            <div style="font-size:12px;color:rgba(180,210,255,0.35);margin-top:8px">
                8 languages · 21-Day Challenge · Certificates · Score tracking
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="btn-primary" style="max-width:480px;margin:0 auto">', unsafe_allow_html=True)
    if st.button("🚀 Upgrade to Lifetime — $149", key="paywall_upgrade", use_container_width=True):
        st.markdown(f'<meta http-equiv="refresh" content="0;url={CHECKOUT_URL}">', unsafe_allow_html=True)
        st.info("Redirecting to checkout...")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    col1, col2, _ = st.columns([1, 1, 2])
    with col1:
        if st.button("📊 View my reports", key="paywall_reports"):
            st.session_state.current_view = "reports"
            st.rerun()
    with col2:
        if st.button("⚙️ Settings", key="paywall_settings"):
            st.session_state.current_view = "settings"
            st.rerun()

    return True  # Blocked

if view == "dashboard":
    from modules.dashboard import render_dashboard
    render_dashboard()

elif view == "practice":
    if not _check_paywall(st.session_state.get("user_id", "demo"), profile):
        from modules.practice import render_practice
        render_practice()

elif view == "reports":
    from modules.reports import render_reports
    render_reports()

elif view == "challenge":
    if not _check_paywall(st.session_state.get("user_id", "demo"), profile):
        from modules.challenge import render_challenge
        render_challenge()

elif view == "settings":
    from modules.settings import render_settings
    render_settings()

elif view == "listening":
    if not _check_paywall(st.session_state.get("user_id", "demo"), profile):
        from modules.practice_listening import render_listening_practice
        render_listening_practice()

else:
    st.error(f"Unknown view: {view}")
    st.session_state.current_view = "dashboard"
    st.rerun()
