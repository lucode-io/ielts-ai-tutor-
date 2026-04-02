# ============================================================
# modules/auth.py
# Login, signup, and onboarding views
# ============================================================

import streamlit as st
from utils.database import sign_in, sign_up, get_user_profile


def render_auth():
    """Render the authentication gate (login/signup)."""

    st.markdown("""
    <div style="max-width:440px;margin:60px auto 0;text-align:center">
        <div style="font-size:48px;margin-bottom:12px">🎓</div>
        <div style="font-size:28px;font-weight:800;color:#F0C040;margin-bottom:6px">
            IELTS Master
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:32px">
            Your AI-powered path to Band 7.0+
        </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]

    with col:
        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="you@email.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("Sign In", use_container_width=True, key="do_login"):
                if email and password:
                    with st.spinner("Signing in..."):
                        result = sign_in(email, password)
                    if result["success"]:
                        st.session_state.auth_user = result["user"]
                        st.session_state.auth_session = result["session"]
                        _load_profile(result["user"].id)
                        st.rerun()
                    else:
                        err = result["error"]
                        if "Invalid" in err:
                            st.error("Wrong email or password.")
                        else:
                            st.error(f"Sign in failed: {err}")
                else:
                    st.warning("Please fill in all fields.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_signup:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            full_name = st.text_input("Full Name", placeholder="Your name", key="reg_name")
            email_r = st.text_input("Email", placeholder="you@email.com", key="reg_email")
            pass_r = st.text_input("Password", type="password",
                                   placeholder="Min 8 characters", key="reg_pass")
            target = st.selectbox("Target Band Score",
                                  [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0],
                                  index=4, key="reg_band")

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("Create Account", use_container_width=True, key="do_signup"):
                if full_name and email_r and pass_r:
                    if len(pass_r) < 8:
                        st.error("Password must be at least 8 characters.")
                    else:
                        with st.spinner("Creating your account..."):
                            result = sign_up(email_r, pass_r, full_name)
                        if result["success"]:
                            st.success("Account created! Please check your email to verify, then sign in.")
                        else:
                            err = result["error"]
                            if "already registered" in err:
                                st.error("This email is already registered.")
                            else:
                                st.error(f"Sign up failed: {err}")
                else:
                    st.warning("Please fill in all fields.")
            st.markdown('</div>', unsafe_allow_html=True)

    # Demo mode button
    st.markdown("<div style='text-align:center;margin-top:24px'>", unsafe_allow_html=True)
    if st.button("Try Demo Mode (no account needed)", key="demo_mode"):
        _load_demo_profile()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def _load_profile(user_id: str):
    """Load user profile into session state."""
    profile = get_user_profile(user_id)
    if profile:
        st.session_state.profile = profile
        st.session_state.user_id = user_id
        # Check if needs onboarding (no baseline yet)
        if not profile.get("baseline_band"):
            st.session_state.current_view = "onboarding"
        else:
            st.session_state.current_view = "dashboard"
    else:
        st.error("Could not load profile. Please try again.")


def _load_demo_profile():
    """Load a demo profile for users without an account."""
    st.session_state.profile = {
        "id": "demo",
        "full_name": "Demo Student",
        "email": "demo@ieltsmaster.ai",
        "target_band": 7.0,
        "baseline_band": 5.5,
        "streak_count": 3,
        "streak_last_date": None,
        "challenge_day": 3,
        "challenge_started_at": None,
        "challenge_completed": False,
        "tutor_name": "Alex",
        "response_language": "English",
        "accent_color": "#F0C040",
        "subscription_status": "free",
        "native_language": "English",
    }
    st.session_state.user_id = "demo"
    st.session_state.is_demo = True
    st.session_state.current_view = "dashboard"
