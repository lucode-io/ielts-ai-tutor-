# ============================================================
# modules/settings.py
# User HQ - profile, preferences, subscription
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
    "Gold": "#F0C040",
    "Blue": "#38BDF8",
    "Green": "#34D399",
    "Purple": "#A78BFA",
    "Coral": "#F87171",
    "Pink": "#F472B6",
}


def render_settings():
    profile = st.session_state.get("profile", {})
    accent = profile.get("accent_color", "#F0C040")
    user_id = st.session_state.get("user_id", "demo")
    is_demo = st.session_state.get("is_demo", False)

    st.markdown(f"""
    <div style="font-size:22px;font-weight:800;color:#fff;margin-bottom:4px">User HQ ⚙️</div>
    <div style="font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:24px">
        Manage your profile, preferences, and subscription
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Profile", "Tutor Preferences", "Subscription"])

    # ── PROFILE TAB ──
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-weight:700;font-size:13px;color:{accent};
                    margin-bottom:16px;letter-spacing:0.04em;text-transform:uppercase">
            Profile Settings
        </div>
        """, unsafe_allow_html=True)

        p1, p2 = st.columns(2)
        with p1:
            full_name = st.text_input("Full Name",
                value=profile.get("full_name", ""), key="set_name")
            email = st.text_input("Email",
                value=profile.get("email", ""), disabled=True, key="set_email")
        with p2:
            target_band = st.selectbox("Target Band Score",
                [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0],
                index=[5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0].index(
                    float(profile.get("target_band", 7.0))), key="set_target")
            native_language = st.selectbox("Native Language", LANGUAGES,
                index=LANGUAGES.index(profile.get("native_language","English"))
                      if profile.get("native_language") in LANGUAGES else 0,
                key="set_native")

        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Save Profile", key="save_profile", use_container_width=False):
            updates = {
                "full_name": full_name,
                "target_band": target_band,
                "native_language": native_language,
            }
            if not is_demo:
                if update_user_profile(user_id, updates):
                    st.session_state.profile.update(updates)
                    st.success("Profile saved!")
                else:
                    st.error("Failed to save. Please try again.")
            else:
                st.session_state.profile.update(updates)
                st.success("Profile saved! (Demo mode)")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── BASELINE BAND ──
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        baseline = profile.get("baseline_band")

        if baseline:
            st.markdown(f"""
            <div style="padding:14px;background:rgba(255,255,255,0.04);
                        border-radius:12px;border:1px solid rgba(255,255,255,0.08);
                        margin-bottom:12px">
                <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-bottom:4px">
                    Baseline Band (from diagnostic test)
                </div>
                <div style="font-size:28px;font-weight:700;color:{accent}">{baseline}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔄 Retake Diagnostic Test", key="retake_diag",
                         use_container_width=False):
                st.session_state.profile["baseline_band"] = None
                st.session_state.onboarding_step = 1
                st.session_state.diagnostic_messages = []
                st.session_state.current_view = "onboarding"
                st.rerun()
        else:
            st.markdown(f"""
            <div style="padding:14px;background:rgba(240,192,64,0.06);
                        border-radius:12px;border:1px solid rgba(240,192,64,0.2);
                        margin-bottom:12px">
                <div style="font-size:13px;color:rgba(255,255,255,0.5);margin-bottom:8px">
                    No baseline band yet. Take the diagnostic test to set your starting level.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("🚀 Take Diagnostic Test", key="take_diag",
                         use_container_width=False):
                st.session_state.onboarding_step = 1
                st.session_state.diagnostic_messages = []
                st.session_state.current_view = "onboarding"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── SIGN OUT ──
        if not is_demo:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            if st.button("Sign Out", key="sign_out", use_container_width=False):
                sign_out()
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    # ── TUTOR PREFERENCES TAB ──
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-weight:700;font-size:13px;color:{accent};
                    margin-bottom:16px;letter-spacing:0.04em;text-transform:uppercase">
            Tutor Preferences
        </div>
        """, unsafe_allow_html=True)

        t1, t2 = st.columns(2)
        with t1:
            tutor_name = st.text_input("Tutor Name",
                value=profile.get("tutor_name", "Alex"),
                placeholder="e.g. Alex, Sara, James...", key="set_tutor_name")
            response_language = st.selectbox("Response Language", LANGUAGES,
                index=LANGUAGES.index(profile.get("response_language","English"))
                      if profile.get("response_language") in LANGUAGES else 0,
                key="set_lang")
        with t2:
            accent_label = st.selectbox("Accent Color",
                list(ACCENT_OPTIONS.keys()),
                index=list(ACCENT_OPTIONS.values()).index(profile.get("accent_color","#F0C040"))
                      if profile.get("accent_color") in ACCENT_OPTIONS.values() else 0,
                key="set_accent")
            new_accent = ACCENT_OPTIONS[accent_label]
            st.markdown(f"""
            <div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">
                {"".join(f'<div style="width:28px;height:28px;border-radius:50%;background:{c};border:2px solid {"rgba(255,255,255,0.6)" if c == new_accent else "transparent"}"></div>' for c in ACCENT_OPTIONS.values())}
            </div>
            """, unsafe_allow_html=True)

        if response_language != "English":
            st.info(f"Mixed mode: explanations in {response_language}, IELTS terms in English.")

        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Save Preferences", key="save_prefs", use_container_width=False):
            updates = {
                "tutor_name": tutor_name,
                "response_language": response_language,
                "accent_color": new_accent,
            }
            if not is_demo:
                if update_user_profile(user_id, updates):
                    st.session_state.profile.update(updates)
                    st.success("Preferences saved!")
                else:
                    st.error("Failed to save.")
            else:
                st.session_state.profile.update(updates)
                st.success("Preferences saved!")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── SUBSCRIPTION TAB ──
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        status = profile.get("subscription_status", "free")

        st.markdown(f"""
        <div style="font-weight:700;font-size:13px;color:{accent};
                    margin-bottom:16px;letter-spacing:0.04em;text-transform:uppercase">
            Subscription
        </div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px">
            <div style="font-size:28px">{"⭐" if status == "pro" else "🎓"}</div>
            <div>
                <div style="font-size:16px;font-weight:700;color:#fff">
                    {"Pro Plan" if status == "pro" else "Free Plan"}
                </div>
                <div style="font-size:13px;color:rgba(255,255,255,0.4)">
                    {"Full access to all features" if status == "pro" else "Limited to 10 sessions/month"}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if status != "pro":
            features = [
                ("Unlimited practice sessions", True, False),
                ("Full mock tests with timer", True, False),
                ("Score history & analytics", True, False),
                ("3-color writing annotation", True, False),
                ("Fluency gap analysis", True, False),
                ("21-Day challenge certificate", True, False),
                ("Verified certificate hash", True, False),
                ("Basic practice sessions", True, True),
                ("5 sessions per month", True, True),
            ]
            st.markdown("""
            <div style="display:flex;justify-content:flex-end;gap:24px;
                        font-size:11px;color:rgba(255,255,255,0.35);
                        text-transform:uppercase;letter-spacing:0.06em;
                        margin-bottom:6px;padding-right:4px">
                <span>Pro</span><span>Free</span>
            </div>
            """, unsafe_allow_html=True)
            for feat, pro_has, free_has in features:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04)">
                    <div style="font-size:13px;color:rgba(255,255,255,0.6)">{feat}</div>
                    <div style="display:flex;gap:24px;min-width:60px;justify-content:flex-end">
                        <span>{"✅" if pro_has else "❌"}</span>
                        <span>{"✅" if free_has else "❌"}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("Upgrade to Pro — $19/month", key="upgrade",
                         use_container_width=False):
                st.info("Stripe coming soon. Contact us at mlogshir@gmail.com to upgrade manually.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("You are on the Pro plan. Thank you for supporting IELTS Master!")
            if st.button("Manage Subscription", key="manage_sub"):
                st.info("Contact mlogshir@gmail.com to manage your subscription.")

        st.markdown('</div>', unsafe_allow_html=True)
