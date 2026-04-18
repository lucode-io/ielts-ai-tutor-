# ============================================================
# modules/onboarding.py
# Phase 1: Conversational setup (5 questions, card-based)
# Phase 2: Diagnostic test (Speaking/Writing/Reading/Listening)
#
# BUG 2 FIX: _render_timer() — pure Python server-side elapsed
#   display. No JS countdown that resets on st.rerun(). Shows
#   elapsed time + static remaining. Accurate across all reruns.
# BUG 3 FIX (mobile listening): Audio + questions shown at same
#   time in listening section. Questions disabled until audio
#   played, enabled via a "Mark as listened" button below player.
# ============================================================

import streamlit as st
import re
import time
import base64
from utils.ai import chat
from utils.database import save_diagnostic, update_user_profile

# ── LISTENING SCRIPT ──────────────────────────────────────────
LISTENING_SCRIPT = """
Good morning students. I have some important announcements about next week's schedule.
On Monday, the library will open at 8am instead of the usual 9am, due to a special
study session for final year students. The science lab on the third floor will be closed
for maintenance on Tuesday and Wednesday. Students who need lab access should use the
alternative lab on the first floor. The cafeteria will introduce a new menu starting
Thursday, with vegetarian options now available every day. Finally, the sports hall
booking system has changed. You must now book at least 24 hours in advance using the
new online portal. Walk-in bookings will no longer be accepted. If you have any
questions, please contact the student office at extension 204.
"""

LISTENING_QUESTIONS = [
    "What time will the library open on Monday?",
    "Which floor is the science lab that will be closed?",
    "On which days will the science lab be closed?",
    "What is new about the cafeteria starting Thursday?",
    "How many hours in advance must students now book the sports hall?",
]

LISTENING_ANSWERS = ["8am", "third", "tuesday and wednesday", "vegetarian options", "24"]

# ── BAND SCORE DEFINITIONS ────────────────────────────────────
BAND_INFO = {
    5.0: ("Modest", "You have a basic command of English. Suitable for some low-skilled jobs."),
    5.5: ("Modest+", "Partial command — you handle overall meaning in most situations."),
    6.0: ("Competent", "Effective command despite inaccuracies. Most universities accept this."),
    6.5: ("Competent+", "Good working command. Many universities and visa routes accept 6.5."),
    7.0: ("Good", "Operational command with occasional errors. Most top universities require 7.0."),
    7.5: ("Good+", "Very good command. Strong for UK/Australian skilled migration visas."),
    8.0: ("Very Good", "Fully operational with minor unsystematic errors. Excellent for careers abroad."),
    8.5: ("Very Good+", "Near-native fluency. Required for some academic and professional roles."),
    9.0: ("Expert", "Full operational command. Native-level accuracy and fluency."),
}

# ── SCHEDULE OPTIONS ──────────────────────────────────────────
SCHEDULES = {
    "Every day": {"icon": "🔥", "desc": "7 days/week — maximum speed", "days": 7},
    "Weekdays only": {"icon": "📅", "desc": "Mon–Fri, rest on weekends", "days": 5},
    "3 days/week": {"icon": "⚡", "desc": "Mon, Wed, Fri — balanced", "days": 3},
    "Weekends only": {"icon": "🌅", "desc": "Sat + Sun — for busy students", "days": 2},
}

HOURS_OPTIONS = [
    {"label": "30 min", "value": 0.5, "desc": "Quick daily focus", "icon": "⚡"},
    {"label": "1 hour", "value": 1.0, "desc": "Solid daily session", "icon": "📚"},
    {"label": "2 hours", "value": 2.0, "desc": "Serious preparation", "icon": "💪"},
    {"label": "3+ hours", "value": 3.0, "desc": "Full immersion mode", "icon": "🚀"},
]


# ── MAIN ROUTER ───────────────────────────────────────────────
def render_onboarding():
    profile = st.session_state.get("profile", {})
    user_id = st.session_state.get("user_id", "demo")
    name = profile.get("full_name", "Student").split()[0]
    step = st.session_state.get("onboarding_step", 0)

    if step == 0:
        _render_setup_welcome(name)
    elif step == 1:
        _render_exam_type(name)
    elif step == 2:
        _render_target_band(name)
    elif step == 3:
        _render_schedule(name)
    elif step == 4:
        _render_hours(name)
    elif step == 5:
        _render_setup_summary(name, profile, user_id)
    elif step == 6:
        _render_diagnostic_welcome(name)
    elif step == 7:
        _render_diagnostic(profile, user_id)
    elif step == 8:
        _render_listening_section(profile, user_id)
    elif step == 9:
        _render_results(profile, user_id)


# ══════════════════════════════════════════════════════════════
#  SETUP PHASE
# ══════════════════════════════════════════════════════════════

def _step_indicator(current_step: int):
    steps = ["Exam", "Band", "Schedule", "Hours", "Summary"]
    cols = st.columns(len(steps))
    for i, (col, label) in enumerate(zip(cols, steps)):
        step_num = i + 1
        done = step_num < current_step
        active = step_num == current_step
        color = "#4A9EFF" if active else ("#00e87a" if done else "rgba(180,210,255,0.2)")
        with col:
            st.markdown(
                f'<div style="text-align:center;font-size:11px;color:{color};'
                f'font-weight:{"700" if active else "400"}">'
                f'{"✓" if done else step_num}. {label}</div>',
                unsafe_allow_html=True,
            )
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)


def _render_setup_welcome(name):
    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.markdown(f"""
        <div style="text-align:center;padding:48px 0 32px">
            <div style="font-size:56px;margin-bottom:20px">👋</div>
            <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;
                        color:#f0f4ff;margin-bottom:12px;line-height:1.2">
                Hey {name}, let's set up<br>your personal study plan
            </div>
            <div style="font-size:15px;color:rgba(180,210,255,0.6);line-height:1.75;
                        max-width:400px;margin:0 auto 32px">
                I'll ask you 5 quick questions so your AI tutor knows
                exactly how to help you reach your target band — fast.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Let's go →", use_container_width=True, key="welcome_start"):
            st.session_state.onboarding_step = 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def _render_exam_type(name):
    _, col, _ = st.columns([1, 4, 1])
    with col:
        _step_indicator(1)
        st.markdown(f"""
        <div style="margin-bottom:24px">
            <div style="font-size:12px;color:rgba(74,158,255,0.7);font-weight:600;
                        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px">
                Question 1 of 5
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                        color:#f0f4ff;margin-bottom:8px;line-height:1.3">
                Which IELTS exam are you preparing for?
            </div>
        </div>
        """, unsafe_allow_html=True)

        currently_selected = st.session_state.get("setup_exam_type")
        col_a, col_g = st.columns(2)

        for col_el, exam_type, icon, desc in [
            (col_a, "Academic", "🎓", "University admission, professional registration"),
            (col_g, "General Training", "✈️", "Work experience, secondary education, migration to English-speaking countries"),
        ]:
            selected = currently_selected == exam_type
            border = "2px solid #4A9EFF" if selected else "1px solid rgba(74,158,255,0.12)"
            bg = "rgba(74,158,255,0.1)" if selected else "rgba(74,158,255,0.03)"
            with col_el:
                st.markdown(f"""
                <div style="background:{bg};border:{border};border-radius:14px;
                            padding:20px 16px;text-align:center;margin-bottom:10px">
                    <div style="font-size:32px;margin-bottom:8px">{icon}</div>
                    <div style="font-size:16px;font-weight:700;color:#f0f4ff;margin-bottom:6px">{exam_type}</div>
                    <div style="font-size:12px;color:rgba(180,210,255,0.45);line-height:1.5">{desc}</div>
                    {'<div style="margin-top:10px;font-size:11px;color:#4A9EFF;font-weight:600">✓ Selected</div>' if selected else ''}
                </div>
                """, unsafe_allow_html=True)
                btn_label = "Academic IELTS" if exam_type == "Academic" else "General Training"
                if st.button(f"Choose {btn_label.split()[0]}", use_container_width=True, key=f"pick_{exam_type.replace(' ','_')}"):
                    st.session_state.setup_exam_type = exam_type
                    st.session_state.onboarding_step = 2
                    st.rerun()

        st.markdown("""
        <div style="margin-top:16px;padding:12px 16px;background:rgba(74,158,255,0.04);
                    border-radius:10px;border:1px solid rgba(74,158,255,0.1)">
            <div style="font-size:11px;color:rgba(180,210,255,0.45);line-height:1.6">
                💡 <strong style="color:rgba(180,210,255,0.7)">Not sure?</strong>
                Choose Academic if you're applying to university. Choose General if you're
                applying for a UK, Australian or Canadian visa.
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_target_band(name):
    exam_type = st.session_state.get("setup_exam_type", "Academic")
    _, col, _ = st.columns([1, 4, 1])
    with col:
        _step_indicator(2)
        st.markdown(f"""
        <div style="margin-bottom:24px">
            <div style="font-size:12px;color:rgba(74,158,255,0.7);font-weight:600;
                        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px">
                Question 2 of 5
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                        color:#f0f4ff;margin-bottom:8px;line-height:1.3">
                What band score are you aiming for?
            </div>
            <div style="font-size:14px;color:rgba(180,210,255,0.5);line-height:1.6">
                Choose your target. Each card shows what that band means in real life.
            </div>
        </div>
        """, unsafe_allow_html=True)

        band_options = [6.0, 6.5, 7.0, 7.5, 8.0, 8.5]
        currently_selected = st.session_state.get("setup_target_band")

        cols_row1 = st.columns(3)
        cols_row2 = st.columns(3)
        all_cols = cols_row1 + cols_row2

        for i, band in enumerate(band_options):
            label, meaning = BAND_INFO[band]
            selected = currently_selected == band
            border = "2px solid #4A9EFF" if selected else "1px solid rgba(74,158,255,0.12)"
            bg = "rgba(74,158,255,0.1)" if selected else "rgba(74,158,255,0.03)"
            check = "✓ " if selected else ""
            with all_cols[i]:
                st.markdown(f"""<div style="background:{bg};border:{border};border-radius:14px;padding:16px 14px;margin-bottom:8px"><div style="font-size:28px;font-weight:800;color:#4A9EFF;line-height:1;margin-bottom:4px">{check}{band}</div><div style="font-size:12px;font-weight:700;color:#f0f4ff;margin-bottom:4px">{label}</div><div style="font-size:10px;color:rgba(180,210,255,0.45);line-height:1.5">{meaning}</div></div>""", unsafe_allow_html=True)
                if st.button(f"Band {band}", use_container_width=True, key=f"band_{band}"):
                    st.session_state.setup_target_band = band
                    st.session_state.onboarding_step = 3
                    st.rerun()

        st.markdown("""<div style="margin-top:8px;text-align:center;font-size:12px;color:rgba(180,210,255,0.35)">Other targets:</div>""", unsafe_allow_html=True)
        other_cols = st.columns(3)
        for i, band in enumerate([5.0, 5.5, 9.0]):
            with other_cols[i]:
                if st.button(f"Band {band}", use_container_width=True, key=f"band_{band}"):
                    st.session_state.setup_target_band = band
                    st.session_state.onboarding_step = 3
                    st.rerun()


def _render_schedule(name):
    target = st.session_state.get("setup_target_band", 7.0)
    _, col, _ = st.columns([1, 4, 1])
    with col:
        _step_indicator(3)
        st.markdown(f"""
        <div style="margin-bottom:24px">
            <div style="font-size:12px;color:rgba(74,158,255,0.7);font-weight:600;
                        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px">
                Question 3 of 5
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                        color:#f0f4ff;margin-bottom:8px;line-height:1.3">
                How often can you practice?
            </div>
            <div style="font-size:14px;color:rgba(180,210,255,0.5);line-height:1.6">
                More days = faster progress.
            </div>
        </div>
        """, unsafe_allow_html=True)

        currently_selected = st.session_state.get("setup_schedule")
        for sched_name, sched_info in SCHEDULES.items():
            selected = currently_selected == sched_name
            border = "2px solid #4A9EFF" if selected else "1px solid rgba(74,158,255,0.12)"
            bg = "rgba(74,158,255,0.1)" if selected else "rgba(74,158,255,0.03)"
            st.markdown(f"""<div style="background:{bg};border:{border};border-radius:12px;padding:14px 16px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between"><div style="display:flex;align-items:center;gap:12px"><div style="font-size:24px">{sched_info['icon']}</div><div><div style="font-size:14px;font-weight:700;color:#f0f4ff">{sched_name}</div><div style="font-size:11px;color:rgba(180,210,255,0.45)">{sched_info['desc']}</div></div></div>{'<div style="font-size:11px;color:#4A9EFF;font-weight:600">✓</div>' if selected else ''}</div>""", unsafe_allow_html=True)
            if st.button(sched_name, use_container_width=True, key=f"sched_{sched_name.replace(' ','_')}"):
                st.session_state.setup_schedule = sched_name
                st.session_state.onboarding_step = 4
                st.rerun()


def _render_hours(name):
    _, col, _ = st.columns([1, 4, 1])
    with col:
        _step_indicator(4)
        st.markdown(f"""
        <div style="margin-bottom:24px">
            <div style="font-size:12px;color:rgba(74,158,255,0.7);font-weight:600;
                        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px">
                Question 4 of 5
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                        color:#f0f4ff;margin-bottom:8px;line-height:1.3">
                How long is each study session?
            </div>
            <div style="font-size:14px;color:rgba(180,210,255,0.5);line-height:1.6">
                Even 30 minutes a day adds up.
            </div>
        </div>
        """, unsafe_allow_html=True)

        currently_selected = st.session_state.get("setup_hours")
        hr1, hr2 = st.columns(2)
        hr3, hr4 = st.columns(2)
        col_pairs = [hr1, hr2, hr3, hr4]

        for col_el, opt in zip(col_pairs, HOURS_OPTIONS):
            selected = currently_selected == opt["value"]
            border = "2px solid #4A9EFF" if selected else "1px solid rgba(74,158,255,0.12)"
            bg = "rgba(74,158,255,0.1)" if selected else "rgba(74,158,255,0.03)"
            check = '<div style="margin-top:8px;font-size:11px;color:#4A9EFF;font-weight:600">✓ Selected</div>' if selected else ''
            with col_el:
                st.markdown(f"""<div style="background:{bg};border:{border};border-radius:14px;padding:20px 16px;text-align:center;margin-bottom:10px"><div style="font-size:32px;margin-bottom:8px">{opt['icon']}</div><div style="font-size:20px;font-weight:800;color:#4A9EFF;margin-bottom:4px">{opt['label']}</div><div style="font-size:11px;color:rgba(180,210,255,0.45)">{opt['desc']}</div>{check}</div>""", unsafe_allow_html=True)
                if st.button(f"{opt['label']}/session", use_container_width=True, key=f"hours_{opt['value']}"):
                    st.session_state.setup_hours = opt["value"]
                    st.session_state.onboarding_step = 5
                    st.rerun()


def _render_setup_summary(name, profile, user_id):
    exam_type = st.session_state.get("setup_exam_type", "Academic")
    target_band = float(st.session_state.get("setup_target_band", 7.0))
    schedule = st.session_state.get("setup_schedule", "Every day")
    hours = float(st.session_state.get("setup_hours", 1.0))
    days_per_week = SCHEDULES.get(schedule, {}).get("days", 5)
    hours_per_week = hours * days_per_week
    weeks = _estimate_weeks(target_band, hours_per_week)
    band_label, band_meaning = BAND_INFO.get(target_band, ("", ""))

    _, col, _ = st.columns([1, 4, 1])
    with col:
        _step_indicator(5)
        st.markdown(f"""
        <div style="margin-bottom:20px">
            <div style="font-size:12px;color:rgba(74,158,255,0.7);font-weight:600;
                        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px">
                Question 5 of 5
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                        color:#f0f4ff;margin-bottom:8px;line-height:1.3">
                Your personalized study plan
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:rgba(74,158,255,0.04);border:1px solid rgba(74,158,255,0.12);
                    border-radius:14px;padding:20px;margin-bottom:16px">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
                <div><div style="font-size:10px;color:rgba(180,210,255,0.4);text-transform:uppercase;margin-bottom:4px">Exam Type</div><div style="font-size:14px;font-weight:700;color:#f0f4ff">{exam_type}</div></div>
                <div><div style="font-size:10px;color:rgba(180,210,255,0.4);text-transform:uppercase;margin-bottom:4px">Target Band</div><div style="font-size:14px;font-weight:700;color:#4A9EFF">{target_band} — {band_label}</div></div>
                <div><div style="font-size:10px;color:rgba(180,210,255,0.4);text-transform:uppercase;margin-bottom:4px">Schedule</div><div style="font-size:14px;font-weight:700;color:#f0f4ff">{schedule}</div></div>
                <div><div style="font-size:10px;color:rgba(180,210,255,0.4);text-transform:uppercase;margin-bottom:4px">Per Session</div><div style="font-size:14px;font-weight:700;color:#f0f4ff">{hours} hr{'s' if hours > 1 else ''}</div></div>
            </div>
        </div>
        <div style="background:rgba(0,232,122,0.05);border:1px solid rgba(0,232,122,0.2);
                    border-radius:12px;padding:14px 16px;margin-bottom:20px">
            <div style="font-size:13px;color:rgba(180,210,255,0.7);line-height:1.7">
                📈 Based on your schedule ({hours_per_week:.1f} hrs/week), you can reach
                <strong style="color:#4A9EFF">Band {target_band}</strong> in approximately
                <strong style="color:#00e87a">{weeks} weeks</strong>.
                Your AI tutor will track your progress and adjust your plan weekly.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("✅ Looks good — start my diagnostic test", use_container_width=True, key="confirm_setup"):
            updates = {
                "exam_type": exam_type,
                "target_band": target_band,
                "practice_schedule": schedule,
                "study_hours_per_day": hours,
            }
            if user_id != "demo":
                update_user_profile(user_id, updates)
            st.session_state.profile = {**st.session_state.get("profile", {}), **updates}
            st.session_state.onboarding_step = 6
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("← Edit my answers", use_container_width=True, key="edit_setup"):
            st.session_state.onboarding_step = 1
            st.rerun()


def _estimate_weeks(target_band: float, hours_per_week: float) -> str:
    base_weeks_per_half_band = max(3, 8 - (hours_per_week / 2))
    bands_to_improve = max(1, (target_band - 5.5))
    half_bands = bands_to_improve * 2
    weeks = int(half_bands * base_weeks_per_half_band)
    if weeks <= 8:
        return "6–8"
    elif weeks <= 14:
        return "8–14"
    elif weeks <= 20:
        return "12–20"
    else:
        return "16–24"


# ══════════════════════════════════════════════════════════════
#  DIAGNOSTIC PHASE
# ══════════════════════════════════════════════════════════════

def _render_diagnostic_welcome(name):
    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.markdown(f"""
        <div style="text-align:center;padding:32px 0 24px">
            <div style="font-size:48px;margin-bottom:16px">🎯</div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                        color:#f0f4ff;margin-bottom:8px">Baseline Diagnostic Test</div>
            <div style="font-size:14px;color:rgba(180,210,255,0.5);line-height:1.7;
                        max-width:380px;margin:0 auto 24px">
                A 15–20 minute test across all 4 IELTS skills.<br>
                This sets your starting band so your AI tutor knows exactly what to teach.
            </div>
        </div>
        <div style="background:rgba(74,158,255,0.04);border:1px solid rgba(74,158,255,0.12);
                    border-radius:14px;padding:16px;margin-bottom:20px">
            <div style="font-size:12px;color:rgba(180,210,255,0.6);line-height:1.8">
                ✅ Part 1: Speaking (4 questions)<br>
                ✅ Part 2: Writing (1 paragraph task)<br>
                ✅ Part 3: Reading (5 T/F/NG questions)<br>
                ✅ Part 4: Listening (short audio + 5 questions)
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("🚀 Start Diagnostic Test", use_container_width=True, key="start_diag"):
            st.session_state.onboarding_step = 7
            st.session_state.diagnostic_messages = []
            st.session_state.diag_start_time = time.time()
            st.session_state.diag_section_time = time.time()
            st.session_state.diag_scores = {}
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Skip — I know my level", use_container_width=True, key="skip_diag"):
            st.session_state.current_view = "dashboard"
            st.rerun()


# ── BUG 2 FIX: Pure Python timer — no JS, survives st.rerun() ──
def _render_timer(section_name: str, duration_seconds: int):
    """
    Server-side elapsed timer. Computes remaining from time.time() on each
    Python execution — survives st.rerun() without resetting to zero.
    JS-based countdowns reset every rerun; this does not.
    """
    start = st.session_state.get("diag_section_time", time.time())
    elapsed = int(time.time() - start)
    remaining = max(0, duration_seconds - elapsed)
    minutes = remaining // 60
    seconds = remaining % 60
    pct = max(0, int((remaining / duration_seconds) * 100))
    color = "#4A9EFF" if remaining > 120 else "#F0C040" if remaining > 60 else "#ff3a4a"

    st.markdown(f"""
    <div style="background:rgba(74,158,255,0.04);border-radius:12px;
                border:1px solid rgba(74,158,255,0.12);padding:12px 16px;
                margin-bottom:16px;display:flex;align-items:center;justify-content:space-between">
        <div>
            <div style="font-size:10px;color:rgba(180,210,255,0.4);text-transform:uppercase;
                        letter-spacing:0.06em;margin-bottom:2px">{section_name}</div>
            <div style="font-size:22px;font-weight:800;color:{color};font-variant-numeric:tabular-nums">
                {minutes:02d}:{seconds:02d}
            </div>
        </div>
        <div style="width:80px">
            <div style="background:rgba(255,255,255,0.06);border-radius:4px;height:5px">
                <div style="width:{pct}%;height:100%;border-radius:4px;background:{color}"></div>
            </div>
            <div style="font-size:10px;color:rgba(180,210,255,0.3);text-align:right;margin-top:3px">{pct}% left</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    return remaining


def _render_diagnostic(profile, user_id):
    """Speaking + Writing + Reading via AI chat."""
    remaining = _render_timer("Speaking · Writing · Reading", 900)

    if "diagnostic_messages" not in st.session_state:
        st.session_state.diagnostic_messages = []

    if not st.session_state.diagnostic_messages:
        system = _get_diagnostic_prompt(profile)
        starter = [{"role": "user", "content": "Please start my baseline assessment. Begin with Speaking Part 1."}]
        try:
            with st.spinner("Starting your diagnostic test..."):
                response = chat(starter, system, max_tokens=2000)
            if response.startswith("ERROR"):
                st.error(f"AI could not start the test: {response}")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Retry", key="retry_diag", use_container_width=True):
                        st.rerun()
                with c2:
                    if st.button("Skip to Dashboard", key="skip_diag_err", use_container_width=True):
                        st.session_state.current_view = "dashboard"
                        st.rerun()
                return
            st.session_state.diagnostic_messages = [
                {"role": "user", "content": "Please start my baseline assessment. Begin with Speaking Part 1."},
                {"role": "assistant", "content": response}
            ]
            st.rerun()
        except Exception as e:
            st.error(f"Could not connect to AI: {str(e)}")
            if st.button("Skip to Dashboard", key="skip_diag_exc", use_container_width=True):
                st.session_state.current_view = "dashboard"
                st.rerun()
            return

    st.markdown("""
    <div style="margin-bottom:16px">
        <div style="font-size:17px;font-weight:700;color:#f0f4ff;margin-bottom:4px">
            Diagnostic Test — Part 1 of 2
        </div>
        <div style="font-size:12px;color:rgba(180,210,255,0.4)">
            Speaking, Writing and Reading. Listening test follows.
        </div>
    </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.diagnostic_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    last_msg = st.session_state.diagnostic_messages[-1]["content"] \
        if st.session_state.diagnostic_messages else ""

    section_complete = (
        "READING COMPLETE" in last_msg.upper() or
        "PROCEED TO LISTENING" in last_msg.upper() or
        "PART 4: LISTENING" in last_msg.upper() or
        ("reading" in last_msg.lower() and "score" in last_msg.lower() and
         len(st.session_state.diagnostic_messages) > 12)
    )

    if section_complete or remaining == 0:
        _extract_partial_scores(last_msg)
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Continue to Listening Test →", key="go_listening", use_container_width=True):
            st.session_state.onboarding_step = 8
            st.session_state.diag_section_time = time.time()
            st.session_state.mock_listened = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        user_input = st.chat_input("Type your answer here...")
        if user_input:
            st.session_state.diagnostic_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            with st.chat_message("assistant"):
                with st.spinner("Evaluating..."):
                    system = _get_diagnostic_prompt(profile)
                    response = chat(st.session_state.diagnostic_messages, system, max_tokens=2000)
                st.markdown(response)
            st.session_state.diagnostic_messages.append({"role": "assistant", "content": response})
            st.rerun()


# ── BUG 3 FIX (mobile): Audio + questions shown simultaneously ──
def _render_listening_section(profile, user_id):
    """
    FIX: Audio player and questions are ALWAYS both visible.
    On mobile, the old 'audio phase → questions phase' gate meant
    users never saw questions while audio was playing.
    Now: audio plays at top, questions below it. A 'Mark as listened'
    button unlocks question inputs without hiding the player.
    """
    remaining = _render_timer("Listening Section", 300)
    listened = st.session_state.get("mock_listened", False)
    listening_submitted = st.session_state.get("listening_submitted", False)

    st.markdown("""
    <div style="margin-bottom:16px">
        <div style="font-size:17px;font-weight:700;color:#f0f4ff;margin-bottom:4px">
            Diagnostic Test — Part 2 of 2: Listening
        </div>
        <div style="font-size:12px;color:rgba(180,210,255,0.4)">
            Listen to the audio, then answer the 5 questions below.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── AUDIO ALWAYS VISIBLE ──
    audio_b64 = _generate_tts_audio(LISTENING_SCRIPT)
    if audio_b64:
        st.markdown(f"""
        <div style="background:rgba(252,211,77,0.06);border:1px solid rgba(252,211,77,0.2);
                    border-radius:14px;padding:16px;margin-bottom:12px">
            <div style="font-size:13px;font-weight:700;color:#FCD34D;margin-bottom:8px">
                🎧 Listen carefully
            </div>
            <audio controls style="width:100%;border-radius:10px;accent-color:#FCD34D">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
            <div style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:6px">
                Press play — you can replay as needed during the diagnostic
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback: show readable script if TTS fails
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border-radius:12px;padding:16px;
                    margin-bottom:12px;font-size:13px;color:#D8E8F8;line-height:1.8;font-style:italic">
            <strong style="color:#FCD34D;font-style:normal">📄 Read carefully once:</strong><br><br>
            {LISTENING_SCRIPT}
        </div>
        """, unsafe_allow_html=True)

    # ── MARK AS LISTENED BUTTON (unlocks questions) ──
    if not listened:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("✅ I have listened — unlock questions", key="done_listening", use_container_width=True):
            st.session_state.mock_listened = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:12px;color:rgba(180,210,255,0.35);text-align:center;margin-top:6px">
            Questions are shown below — you can read them while listening
        </div>
        """, unsafe_allow_html=True)

    # ── QUESTIONS ALWAYS VISIBLE (inputs disabled until listened) ──
    st.markdown("""
    <div style="margin-top:16px;margin-bottom:10px">
        <div style="font-size:14px;font-weight:700;color:#FCD34D">Questions</div>
        <div style="font-size:12px;color:rgba(180,210,255,0.4)">Answer from memory after listening</div>
    </div>
    """, unsafe_allow_html=True)

    if not listening_submitted:
        answers = {}
        all_answered = True

        for i, question in enumerate(LISTENING_QUESTIONS):
            st.markdown(f"""
            <div style="font-size:14px;color:#D8E8F8;margin-bottom:6px">
                <strong style="color:#FCD34D">Q{i+1}.</strong> {question}
            </div>
            """, unsafe_allow_html=True)

            if listened:
                ans = st.text_input(
                    "", key=f"diag_listen_{i}",
                    placeholder="Your answer...",
                    label_visibility="collapsed"
                )
            else:
                # Show locked placeholder until audio is acknowledged
                st.markdown(
                    '<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);'
                    'border-radius:8px;padding:10px 14px;font-size:13px;color:rgba(180,210,255,0.25);'
                    'margin-bottom:8px">🔒 Listen to audio first, then unlock above</div>',
                    unsafe_allow_html=True
                )
                ans = ""

            if not ans:
                all_answered = False
            answers[i] = ans
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        if listened and all_answered:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("Submit Listening & See Results →", key="submit_listening", use_container_width=True):
                correct = 0
                for i, correct_ans in enumerate(LISTENING_ANSWERS):
                    user_ans = answers.get(i, "").strip().lower()
                    if correct_ans.lower() in user_ans or user_ans in correct_ans.lower():
                        correct += 1
                score_map = {5: 9.0, 4: 7.5, 3: 6.5, 2: 5.5, 1: 4.5, 0: 4.0}
                st.session_state.diag_scores["listening"] = score_map.get(correct, 5.0)
                st.session_state.listening_correct = correct
                st.session_state.listening_submitted = True
                st.session_state.onboarding_step = 9
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        elif listened and not all_answered:
            st.info("Answer all 5 questions to submit.")


def _render_results(profile, user_id):
    scores = st.session_state.get("diag_scores", {})
    speaking = scores.get("speaking", 5.5)
    writing = scores.get("writing", 5.5)
    reading = scores.get("reading", 5.5)
    listening = scores.get("listening", 5.5)
    overall = round((speaking + writing + reading + listening) / 4 * 2) / 2

    exam_type = st.session_state.get("setup_exam_type", profile.get("exam_type", "Academic"))
    target = float(st.session_state.get("setup_target_band", profile.get("target_band", 7.0)))
    schedule = st.session_state.get("setup_schedule", profile.get("practice_schedule", "Every day"))
    gap = round(target - overall, 1)

    skill_data = [
        ("Speaking", speaking, "#A78BFA"),
        ("Writing", writing, "#38BDF8"),
        ("Reading", reading, "#34D399"),
        ("Listening", listening, "#FCD34D"),
    ]
    weakest = min(skill_data, key=lambda x: x[1])
    weeks = _estimate_weeks(target, SCHEDULES.get(schedule, {}).get("days", 5) * 1.0)

    _, col, _ = st.columns([0.5, 4, 0.5])
    with col:
        st.markdown(f"""
        <div style="text-align:center;padding:24px 0 16px">
            <div style="font-size:44px;margin-bottom:12px">📊</div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                        color:#f0f4ff;margin-bottom:6px">Your Baseline Results</div>
            <div style="font-size:13px;color:rgba(180,210,255,0.45)">
                This is your starting point. Everything goes up from here.
            </div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(4)
        for col_el, (skill, score, color) in zip(cols, skill_data):
            with col_el:
                st.markdown(f"""
                <div style="background:{color}0d;border:1px solid {color}33;border-radius:12px;
                            padding:12px;text-align:center">
                    <div style="font-size:10px;color:{color};text-transform:uppercase;
                                letter-spacing:0.06em;margin-bottom:4px">{skill}</div>
                    <div style="font-size:26px;font-weight:800;color:{color}">{score}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:16px;background:rgba(74,158,255,0.04);border:1px solid rgba(74,158,255,0.12);
                    border-radius:14px;padding:16px">
            <div style="font-size:28px;font-weight:800;color:#4A9EFF;text-align:center;margin-bottom:4px">
                {overall}
            </div>
            <div style="font-size:12px;color:rgba(180,210,255,0.4);text-align:center;margin-bottom:12px">
                Overall Baseline Band
            </div>
            <div style="font-size:13px;color:rgba(180,210,255,0.65);line-height:1.7">
                You need to improve <strong style="color:#4A9EFF">{gap} band points</strong> to reach your target.
                Your biggest opportunity is
                <strong style="color:{weakest[2]}">{weakest[0]}</strong>
                at Band {weakest[1]} — this is where we'll focus first.<br><br>
                Following your <strong style="color:#f0f4ff">{schedule}</strong> schedule,
                you're on track to reach
                <strong style="color:#4A9EFF">Band {target}</strong>
                in approximately <strong style="color:#00e87a">{weeks} weeks</strong>.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("✅ Start my IELTS journey →", key="save_diag", use_container_width=True):
            full_scores = {"speaking": speaking, "writing": writing,
                           "reading": reading, "listening": listening, "overall": overall}
            if user_id != "demo":
                save_diagnostic(user_id, full_scores)
                update_user_profile(user_id, {
                    "baseline_band": overall,
                    "exam_type": exam_type,
                    "target_band": target,
                    "practice_schedule": schedule,
                })
            updated = {**st.session_state.get("profile", {}),
                       "baseline_band": overall, "target_band": target,
                       "exam_type": exam_type}
            st.session_state.profile = updated
            st.session_state.current_view = "dashboard"
            for key in ["onboarding_step", "diagnostic_messages", "diag_scores",
                        "mock_listened", "listening_submitted", "setup_exam_type",
                        "setup_target_band", "setup_schedule", "setup_hours"]:
                st.session_state.pop(key, None)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────

def _extract_partial_scores(text: str):
    try:
        from utils.score_extractor import extract_all_scores_from_text, extract_all_scores_from_messages
        scores = st.session_state.get("diag_scores", {})
        found = extract_all_scores_from_text(text)
        for skill in ["speaking", "writing", "reading"]:
            if skill not in scores and skill in found:
                scores[skill] = found[skill]
        if any(skill not in scores for skill in ["speaking", "writing", "reading"]):
            messages = st.session_state.get("diagnostic_messages", [])
            if messages:
                from_all = extract_all_scores_from_messages(messages)
                for skill in ["speaking", "writing", "reading"]:
                    if skill not in scores and skill in from_all and from_all[skill] != 5.5:
                        scores[skill] = from_all[skill]
        for skill in ["speaking", "writing", "reading"]:
            if skill not in scores:
                scores[skill] = 5.5
        st.session_state.diag_scores = scores
    except ImportError:
        # Fallback regex extraction if score_extractor module missing
        scores = st.session_state.get("diag_scores", {})
        for skill, pattern in [
            ("speaking", r"SPEAKING BAND[:\s]+(\d+\.?\d*)"),
            ("writing",  r"WRITING BAND[:\s]+(\d+\.?\d*)"),
            ("reading",  r"READING BAND[:\s]+(\d+\.?\d*)"),
        ]:
            if skill not in scores:
                m = re.search(pattern, text, re.IGNORECASE)
                if m:
                    scores[skill] = float(m.group(1))
                else:
                    scores[skill] = 5.5
        st.session_state.diag_scores = scores


def _generate_tts_audio(text: str) -> str:
    """Generate TTS audio, cached in session to avoid re-generation on every rerun."""
    cache_key = "diag_listening_audio"
    cached = st.session_state.get(cache_key)
    if cached:
        return cached
    try:
        # Try ElevenLabs first via elevenlabs_audio util
        from utils.elevenlabs_audio import generate_audio
        result = generate_audio(text)
        if result:
            st.session_state[cache_key] = result
            return result
    except Exception:
        pass
    try:
        from gtts import gTTS
        import io
        tts = gTTS(text=text.strip(), lang='en', slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        result = base64.b64encode(buf.read()).decode()
        st.session_state[cache_key] = result
        return result
    except Exception:
        return ""


def _get_diagnostic_prompt(profile: dict) -> str:
    exam_type = profile.get("exam_type", "Academic")
    target = profile.get("target_band", 7.0)
    return f"""
You are a strict IELTS examiner conducting a baseline diagnostic test.
The student is taking {exam_type} IELTS. Their target band is {target}.
This is a MINI MOCK TEST — be thorough but efficient.

CONDUCT EXACTLY THIS SEQUENCE:

═══ PART 1: SPEAKING (4 questions) ═══
Ask these questions one at a time, wait for answers:
Q1: "Tell me about yourself — where are you from and what do you do?"
Q2: "Describe a teacher who had a big impact on you. What made them special?"
Q3 (Cue card): "Talk for 1-2 minutes about: A place you would like to visit.
You should say: where it is, why you want to go, what you would do there."
Q4: "Do you think people travel more now than in the past? Why?"
After all 4 answers, give Speaking band with brief reason. Format: SPEAKING BAND: X.X

═══ PART 2: WRITING ═══
Give this prompt:
"Some people believe that students should study only subjects that will be useful
for their future career. Others believe that students should study a wide range of subjects.
Discuss both views and give your own opinion."
Ask for: A full introduction paragraph AND one complete body paragraph (minimum 120 words total).
After they write, score it. Format: WRITING BAND: X.X

═══ PART 3: READING ═══
Give this passage and ask 5 TFNG questions. Score immediately.
Passage: "Urban green spaces play a significant role in improving residents' mental health.
Research conducted in 2019 found that people who spent at least 120 minutes per week
in nature reported substantially higher wellbeing. However, access to green spaces is often
unequally distributed, with wealthier neighbourhoods typically having more parks. Some city
planners argue that digital technology can compensate for lack of green space through virtual
nature experiences, though critics dispute this claim."
1. People who spend 120 minutes per week in nature reported higher wellbeing.
2. The 2019 research was conducted in urban areas only.
3. Poorer neighbourhoods typically have fewer parks than wealthy ones.
4. All city planners support virtual nature experiences as a solution.
5. Critics believe digital technology can fully replace green spaces.
Format: READING BAND: X.X

═══ TRANSITION ═══
After Reading, say EXACTLY:
"READING COMPLETE. You have finished Parts 1-3. Click the button below to continue to the Listening test."
Then STOP.

RULES:
- Be encouraging but honest
- Do not inflate scores
- Keep responses concise and clear
- If student gives very short answers, note this affects their band score
"""
