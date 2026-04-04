# ============================================================
# modules/auth.py
# Login, signup, forgot password — mobile optimized
# ============================================================

import streamlit as st
from utils.database import sign_in, sign_up, get_user_profile, get_supabase_client


def render_auth():
    _check_reset_token()

    st.markdown("""
    <style>
    /* ── MOBILE AUTH FIXES ── */
    [data-testid="stTextInput"] input,
    [data-baseweb="input"] input,
    input[type="text"],
    input[type="email"],
    input[type="password"] {
        color: #1a1a2e !important;
        background: #ffffff !important;
        caret-color: #1a1a2e !important;
        font-size: 16px !important;
    }
    /* Fix tab labels being cut off */
    [data-testid="stTabs"] button {
        font-size: 14px !important;
        padding: 8px 16px !important;
        white-space: nowrap !important;
    }
    /* Fix buttons wrapping on mobile */
    .stButton > button {
        white-space: nowrap !important;
        font-size: 14px !important;
        padding: 12px 20px !important;
        min-height: 48px !important;
    }
    /* Auth container full width on mobile */
    @media screen and (max-width: 640px) {
        .auth-container {
            padding: 0 8px !important;
        }
        [data-testid="stTabs"] button {
            font-size: 13px !important;
            padding: 8px 12px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:32px 16px 24px">
        <div style="font-size:48px;margin-bottom:10px">🎓</div>
        <div style="font-size:26px;font-weight:800;color:#F0C040;margin-bottom:6px">
            IELTS Master
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.4)">
            Your AI-powered path to Band 7.0+
        </div>
    </div>
    """, unsafe_allow_html=True)

    auth_view = st.session_state.get("auth_view", "login")

    # Use responsive columns — wider on mobile
    col = st.columns([0.1, 0.8, 0.1])[1]

    with col:
        if auth_view == "forgot_password":
            _render_forgot_password()
        elif auth_view == "set_new_password":
            _render_set_new_password()
        else:
            tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])
            with tab_login:
                _render_login()
            with tab_signup:
                _render_signup()

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Try Demo Mode (no account needed)",
                     key="demo_mode", use_container_width=True):
            _load_demo_profile()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def _check_reset_token():
    try:
        params = st.query_params
        token = params.get("access_token", "")
        token_type = params.get("type", "")
        if token and token_type == "recovery":
            st.session_state.reset_access_token = token
            st.session_state.auth_view = "set_new_password"
            st.query_params.clear()
    except Exception:
        pass


def _render_login():
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    email = st.text_input(
        "Email", placeholder="you@email.com",
        key="login_email", label_visibility="visible"
    )
    password = st.text_input(
        "Password", type="password",
        placeholder="Your password",
        key="login_pass", label_visibility="visible"
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
                    st.error("Wrong email or password.")
                elif "confirmed" in err.lower() or "verify" in err.lower():
                    st.error("Please verify your email first.")
                else:
                    st.error(f"Sign in failed: {err}")
        else:
            st.warning("Please enter your email and password.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("Forgot password?", key="go_forgot", use_container_width=True):
        st.session_state.auth_view = "forgot_password"
        st.rerun()


def _render_signup():
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    full_name = st.text_input(
        "Full Name", placeholder="Your full name",
        key="reg_name", label_visibility="visible"
    )
    email_r = st.text_input(
        "Email", placeholder="you@email.com",
        key="reg_email", label_visibility="visible"
    )
    pass_r = st.text_input(
        "Password", type="password",
        placeholder="Min 8 characters",
        key="reg_pass", label_visibility="visible"
    )
    target = st.selectbox(
        "Target Band Score",
        [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0],
        index=4, key="reg_band"
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
                    login_result = sign_in(email_r, pass_r)
                    if login_result["success"]:
                        st.session_state.auth_user = login_result["user"]
                        st.session_state.auth_session = login_result["session"]
                        _load_profile(login_result["user"].id)
                        st.rerun()
                    else:
                        st.success("Account created! Please sign in.")
                else:
                    err = result["error"]
                    if "already" in err:
                        st.error("Email already registered. Try signing in.")
                    else:
                        st.error(f"Sign up failed: {err}")
        else:
            st.warning("Please fill in all fields.")
    st.markdown('</div>', unsafe_allow_html=True)


def _render_forgot_password():
    st.markdown("""
    <div style="text-align:center;margin-bottom:20px">
        <div style="font-size:32px;margin-bottom:8px">🔑</div>
        <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:6px">
            Reset Your Password
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.4)">
            Enter your email and we'll send a reset link.
        </div>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "Email address", placeholder="you@email.com",
        key="forgot_email"
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("Send Reset Link", use_container_width=True, key="do_reset"):
        if email:
            with st.spinner("Sending reset email..."):
                result = _send_password_reset(email)
            if result["success"]:
                st.success("Reset link sent! Check your inbox.")
                st.info("Click the link in the email to set your new password.")
            else:
                st.error(f"Could not send: {result['error']}")
        else:
            st.warning("Please enter your email address.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    if st.button("Back to Sign In", key="back_login", use_container_width=True):
        st.session_state.auth_view = "login"
        st.rerun()


def _render_set_new_password():
    st.markdown("""
    <div style="text-align:center;margin-bottom:20px">
        <div style="font-size:32px;margin-bottom:8px">🔒</div>
        <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:6px">
            Set New Password
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.4)">
            Choose a strong new password.
        </div>
    </div>
    """, unsafe_allow_html=True)

    new_pass = st.text_input(
        "New Password", type="password",
        placeholder="Min 8 characters", key="new_pass"
    )
    confirm_pass = st.text_input(
        "Confirm Password", type="password",
        placeholder="Repeat your password", key="confirm_pass"
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("Save New Password", use_container_width=True, key="save_new_pass"):
        if new_pass and confirm_pass:
            if new_pass != confirm_pass:
                st.error("Passwords don't match.")
            elif len(new_pass) < 8:
                st.error("Password must be at least 8 characters.")
            else:
                access_token = st.session_state.get("reset_access_token", "")
                if access_token:
                    result = _update_password(access_token, new_pass)
                    if result["success"]:
                        st.success("Password updated! You can now sign in.")
                        st.session_state.reset_access_token = None
                        st.session_state.auth_view = "login"
                        st.rerun()
                    else:
                        st.error(f"Failed: {result['error']}")
                else:
                    st.error("Session expired. Request a new reset link.")
                    st.session_state.auth_view = "forgot_password"
                    st.rerun()
        else:
            st.warning("Please fill in both fields.")
    st.markdown('</div>', unsafe_allow_html=True)


def _send_password_reset(email: str) -> dict:
    try:
        supabase = get_supabase_client()
        supabase.auth.reset_password_email(
            email,
            options={"redirect_to": "https://ielts-ai-tutor.streamlit.app"}
        )
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _update_password(access_token: str, new_password: str) -> dict:
    try:
        supabase = get_supabase_client()
        supabase.auth.set_session(access_token, "")
        supabase.auth.update_user({"password": new_password})
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _load_profile(user_id: str):
    profile = get_user_profile(user_id)
    if profile:
        st.session_state.profile = profile
        st.session_state.user_id = user_id
        st.session_state.current_view = "onboarding" if not profile.get("baseline_band") else "dashboard"
    else:
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
