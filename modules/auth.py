# ============================================================
# modules/auth.py
# Login, signup, forgot password, and onboarding views
# ============================================================

import streamlit as st
from utils.database import sign_in, sign_up, get_user_profile, get_supabase_client


def render_auth():
    """Render the authentication gate."""

    st.markdown("""
    <div style="max-width:440px;margin:40px auto 0;text-align:center">
        <div style="font-size:52px;margin-bottom:12px">🎓</div>
        <div style="font-size:28px;font-weight:800;color:#F0C040;margin-bottom:6px">
            IELTS Master
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:32px">
            Your AI-powered path to Band 7.0+
        </div>
    </div>
    <style>
    /* Fix input text visibility on auth screen */
    input[type="text"], input[type="email"], input[type="password"] {
        color: #1a1a2e !important;
        background: #ffffff !important;
    }
    [data-testid="stTextInput"] input {
        color: #1a1a2e !important;
        background: #ffffff !important;
    }
    [data-baseweb="input"] input {
        color: #1a1a2e !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]

    # Check which sub-view to show
    auth_view = st.session_state.get("auth_view", "login")

    with col:
        if auth_view == "forgot_password":
            _render_forgot_password()
        else:
            tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

            with tab_login:
                _render_login()

            with tab_signup:
                _render_signup()

    # Demo mode
    st.markdown("<div style='text-align:center;margin-top:20px'>", unsafe_allow_html=True)
    if st.button("Try Demo Mode (no account needed)", key="demo_mode"):
        _load_demo_profile()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def _render_login():
    """Login form."""
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    email = st.text_input(
        "Email",
        placeholder="you@email.com",
        key="login_email"
    )
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Your password",
        key="login_pass"
    )

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
                if "Invalid" in err or "invalid" in err:
                    st.error("Wrong email or password. Try again.")
                elif "confirmed" in err.lower() or "verify" in err.lower():
                    st.error("Please verify your email first. Check your inbox.")
                else:
                    st.error(f"Sign in failed: {err}")
        else:
            st.warning("Please enter your email and password.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Forgot password link
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("Forgot password?", key="go_forgot", use_container_width=False):
        st.session_state.auth_view = "forgot_password"
        st.rerun()


def _render_signup():
    """Signup form."""
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    full_name = st.text_input(
        "Full Name",
        placeholder="Your full name",
        key="reg_name"
    )
    email_r = st.text_input(
        "Email",
        placeholder="you@email.com",
        key="reg_email"
    )
    pass_r = st.text_input(
        "Password",
        type="password",
        placeholder="Min 8 characters",
        key="reg_pass"
    )
    target = st.selectbox(
        "Target Band Score",
        [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0],
        index=4,
        key="reg_band"
    )

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
                    st.success("Account created! You can now sign in.")
                    # Auto sign in
                    login_result = sign_in(email_r, pass_r)
                    if login_result["success"]:
                        st.session_state.auth_user = login_result["user"]
                        st.session_state.auth_session = login_result["session"]
                        _load_profile(login_result["user"].id)
                        st.rerun()
                else:
                    err = result["error"]
                    if "already registered" in err or "already been registered" in err:
                        st.error("This email is already registered. Try signing in.")
                    else:
                        st.error(f"Sign up failed: {err}")
        else:
            st.warning("Please fill in all fields.")
    st.markdown('</div>', unsafe_allow_html=True)


def _render_forgot_password():
    """Forgot password flow."""
    st.markdown("""
    <div style="text-align:center;margin-bottom:24px">
        <div style="font-size:32px;margin-bottom:8px">🔑</div>
        <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:6px">
            Reset Your Password
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.4)">
            Enter your email and we'll send you a reset link.
        </div>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "Email address",
        placeholder="you@email.com",
        key="forgot_email"
    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("Send Reset Link", use_container_width=True, key="do_reset"):
        if email:
            with st.spinner("Sending reset email..."):
                result = _send_password_reset(email)
            if result["success"]:
                st.success("Reset link sent! Check your email inbox.")
                st.info("Click the link in the email, set your new password, then come back here to sign in.")
            else:
                st.error(f"Could not send reset email: {result['error']}")
        else:
            st.warning("Please enter your email address.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    if st.button("Back to Sign In", key="back_login", use_container_width=False):
        st.session_state.auth_view = "login"
        st.rerun()


def _send_password_reset(email: str) -> dict:
    """Send password reset email via Supabase."""
    try:
        supabase = get_supabase_client()
        redirect_url = "https://ielts-ai-tutor.streamlit.app"
        supabase.auth.reset_password_email(
            email,
            options={"redirect_to": redirect_url}
        )
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _load_profile(user_id: str):
    """Load user profile into session state."""
    profile = get_user_profile(user_id)
    if profile:
        st.session_state.profile = profile
        st.session_state.user_id = user_id
        if not profile.get("baseline_band"):
            st.session_state.current_view = "onboarding"
        else:
            st.session_state.current_view = "dashboard"
    else:
        # Profile not in DB yet — create default and go to dashboard
        st.session_state.profile = {
            "id": user_id,
            "full_name": "Student",
            "email": "",
            "target_band": 7.0,
            "baseline_band": None,
            "streak_count": 0,
            "streak_last_date": None,
            "challenge_day": 0,
            "challenge_started_at": None,
            "challenge_completed": False,
            "tutor_name": "Alex",
            "response_language": "English",
            "accent_color": "#F0C040",
            "subscription_status": "free",
            "native_language": "English",
        }
        st.session_state.user_id = user_id
        st.session_state.current_view = "onboarding"


def _load_demo_profile():
    """Load a demo profile."""
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
