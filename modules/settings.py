# ============================================================
# modules/settings.py
# Profile & preferences — Settings HQ
# ============================================================

import streamlit as st
from utils.database import update_user_profile, sign_out

LANGUAGES = [
    "English",
    "Mongolian (Монгол)",
    "Kazakh (Қазақша)",
    "Uzbek (O'zbek)",
    "Kyrgyz (Кыргызча)",
    "Tajik (Тоҷикӣ)",
    "Turkmen (Turkmen)",
    "Russian (Русский)",
]

ACCENT_OPTIONS = {
    "Blue": "#4A9EFF",
    "Gold": "#F0C040",
    "Green": "#34D399",
    "Purple": "#A78BFA",
    "Coral": "#F87171",
}


def render_settings():
    profile = st.session_state.get("profile", {})
    accent = profile.get("accent_color", "#4A9EFF")
    user_id = st.session_state.get("user_id", "demo")

    st.markdown(f"""
    <div style="margin-bottom:20px">
        <div style="font-size:22px;font-weight:800;color:#fff;margin-bottom:4px">
            ⚙️ Settings HQ
        </div>
        <div style="font-size:14px;color:rgba(180,210,255,0.45)">
            Customise your tutor, language, and preferences.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PROFILE SECTION ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:13px;font-weight:700;color:{accent};
                letter-spacing:0.06em;text-transform:uppercase;margin-bottom:16px">
        Profile
    </div>
    """, unsafe_allow_html=True)

    pc1, pc2 = st.columns(2)
    with pc1:
        full_name = st.text_input("Full Name", value=profile.get("full_name", "Student"), key="set_name")
    with pc2:
        email = st.text_input("Email", value=profile.get("email", ""), disabled=True, key="set_email")

    target_options = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0]
    current_target = float(profile.get("target_band", 7.0))
    target_idx = target_options.index(current_target) if current_target in target_options else 4
    target_band = st.selectbox("Target Band", target_options, index=target_idx, key="set_target")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── TUTOR SECTION ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:13px;font-weight:700;color:{accent};
                letter-spacing:0.06em;text-transform:uppercase;margin-bottom:16px">
        Tutor Preferences
    </div>
    """, unsafe_allow_html=True)

    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        tutor_name = st.text_input("Tutor Name", value=profile.get("tutor_name", "Alex"), key="set_tutor")
    with tc2:
        current_lang = profile.get("response_language", "English")
        lang_idx = LANGUAGES.index(current_lang) if current_lang in LANGUAGES else 0
        response_lang = st.selectbox("Response Language", LANGUAGES, index=lang_idx, key="set_lang")
    with tc3:
        current_accent = profile.get("accent_color", "#4A9EFF")
        accent_keys = list(ACCENT_OPTIONS.keys())
        accent_vals = list(ACCENT_OPTIONS.values())
        accent_idx = accent_vals.index(current_accent) if current_accent in accent_vals else 0
        accent_label = st.selectbox("Accent Color", accent_keys, index=accent_idx, key="set_accent")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── SAVE ──
    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("Save Settings", key="save_settings", use_container_width=True):
        updates = {
            "full_name": full_name,
            "target_band": target_band,
            "tutor_name": tutor_name,
            "response_language": response_lang,
            "accent_color": ACCENT_OPTIONS[accent_label],
        }
        st.session_state.profile.update(updates)
        if user_id != "demo":
            update_user_profile(user_id, updates)
        st.toast("Settings saved!", icon="✅")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── SUBSCRIPTION STATUS ──
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    sub_status = profile.get("subscription_status", "free")
    st.markdown(f"""
    <div style="font-size:13px;font-weight:700;color:{accent};
                letter-spacing:0.06em;text-transform:uppercase;margin-bottom:12px">
        Subscription
    </div>
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
        <div style="background:{'rgba(0,232,122,0.1)' if sub_status == 'pro' else 'rgba(255,255,255,0.06)'};
                    border:1px solid {'rgba(0,232,122,0.3)' if sub_status == 'pro' else 'rgba(255,255,255,0.1)'};
                    border-radius:100px;padding:4px 14px;font-size:12px;font-weight:700;
                    color:{'#00e87a' if sub_status == 'pro' else 'rgba(180,210,255,0.5)'}">
            {sub_status.upper()}
        </div>
        <div style="font-size:13px;color:rgba(180,210,255,0.45)">
            {'Unlimited access to all features' if sub_status == 'pro' else '7 free sessions per month'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if sub_status == "free":
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("🏆 Lifetime — $199 one-time", key="upgrade_lifetime", use_container_width=True):
                st.markdown('<meta http-equiv="refresh" content="0;url=https://www.paypal.com/ncp/payment/ZVNEYQCPY5TQN">', unsafe_allow_html=True)
        with sc2:
            if st.button("🎯 Pro — $29/month", key="upgrade_pro", use_container_width=True):
                st.markdown('<meta http-equiv="refresh" content="0;url=https://www.paypal.com/webapps/billing/plans/subscribe?plan_id=P-26J94392NK133254HNHNAOQY">', unsafe_allow_html=True)
        sc3, sc4 = st.columns(2)
        with sc3:
            if st.button("⚡ Intensive — $79 (30 days)", key="upgrade_intensive", use_container_width=True):
                st.markdown('<meta http-equiv="refresh" content="0;url=https://www.paypal.com/ncp/payment/W52FTAGH9JQLL">', unsafe_allow_html=True)
        with sc4:
            if st.button("📚 Starter — $19/month", key="upgrade_starter", use_container_width=True):
                st.markdown('<meta http-equiv="refresh" content="0;url=https://www.paypal.com/webapps/billing/plans/subscribe?plan_id=P-8CU37273YY437041HNHNAQIA">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── SIGN OUT ──
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button("Sign Out", key="sign_out", type="secondary"):
        if user_id != "demo":
            sign_out()
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
