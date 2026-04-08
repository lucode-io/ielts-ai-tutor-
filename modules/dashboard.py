# ============================================================
# modules/dashboard.py
# User HQ - personalized dashboard with stats and quick start
# ============================================================

import streamlit as st
from datetime import datetime, date
from utils.database import (
    get_score_history, get_user_sessions,
    get_recurring_errors, get_challenge_days
)


def render_dashboard():
    profile = st.session_state.get("profile", {})
    name = profile.get("full_name", "Student").split()[0]
    target = profile.get("target_band", 7.0)
    baseline = profile.get("baseline_band", None)
    streak = profile.get("streak_count", 0)
    tutor = profile.get("tutor_name", "Alex")
    accent = profile.get("accent_color", "#4A9EFF")

    hour = datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"

    band_display = f"{baseline}" if baseline else "N/A"
    # Scale: 4.0 = 0%, target = 100%
    if baseline and target:
        progress_pct = min(100, max(0, int(((float(baseline) - 4.0) / (float(target) - 4.0)) * 100)))
    else:
        progress_pct = 0

    st.markdown(f"""
    <div class="glass-card" style="background:linear-gradient(135deg,rgba(240,192,64,0.08),rgba(255,255,255,0.03));">
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px">
            <div>
                <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:4px">{greeting} 👋</div>
                <div style="font-size:26px;font-weight:800;color:#fff;margin-bottom:6px">Welcome back, {name}</div>
                <div style="font-size:14px;color:rgba(255,255,255,0.5)">
                    Your tutor <strong style="color:{accent}">{tutor}</strong> is ready.
                    Target: <strong style="color:{accent}">Band {target}</strong>
                </div>
                <div style="margin-top:12px">
                    <div style="font-size:11px;color:rgba(255,255,255,0.35);margin-bottom:4px">Progress to target</div>
                    <div class="progress-bar-wrap" style="width:280px;max-width:100%">
                        <div class="progress-bar-fill" style="width:{progress_pct}%"></div>
                    </div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:2px">{band_display} → Band {target}</div>
                </div>
            </div>
            <div style="display:flex;gap:16px;flex-wrap:wrap">
                <div style="text-align:center">
                    <div class="band-ring">{band_display}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.35);margin-top:6px">Current</div>
                </div>
                <div style="text-align:center">
                    <div style="width:72px;height:72px;border-radius:50%;border:3px solid rgba(255,255,255,0.15);
                                display:flex;align-items:center;justify-content:center;
                                font-size:22px;font-weight:800;color:rgba(255,255,255,0.5)">{target}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.35);margin-top:6px">Target</div>
                </div>
                <div style="text-align:center">
                    <div style="width:72px;height:72px;border-radius:50%;
                                background:rgba(231,76,60,0.12);border:3px solid rgba(231,76,60,0.4);
                                display:flex;align-items:center;justify-content:center;
                                font-size:22px;font-weight:800;color:#E74C3C">🔥{streak}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.35);margin-top:6px">Streak</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── QUICK START ──
    st.markdown(f"""
    <div style="font-size:13px;font-weight:700;color:{accent};
                letter-spacing:0.06em;text-transform:uppercase;margin:20px 0 12px">Quick Start</div>
    """, unsafe_allow_html=True)

    q1, q2, q3, q4 = st.columns(4)
    with q1:
        st.markdown(_quick_card("🎤", "Speaking", "Part 1 - 3", "#A78BFA"), unsafe_allow_html=True)
        if st.button("Start Speaking", key="qs_speaking", use_container_width=True):
            st.session_state.practice_mode = "Speaking - Part 1 (Personal questions)"
            st.session_state.current_view = "practice"
            st.rerun()
    with q2:
        st.markdown(_quick_card("✍️", "Writing", "Task 1 & 2", "#38BDF8"), unsafe_allow_html=True)
        if st.button("Start Writing", key="qs_writing", use_container_width=True):
            st.session_state.practice_mode = "Writing - Task 2 (Essay)"
            st.session_state.current_view = "practice"
            st.rerun()
    with q3:
        st.markdown(_quick_card("🎧", "Listening", "Sections 1-4", "#FCD34D"), unsafe_allow_html=True)
        if st.button("Start Listening", key="qs_listening", use_container_width=True):
            st.session_state.current_view = "listening"
            st.rerun()
    with q4:
        st.markdown(_quick_card("📖", "Reading", "Academic", "#34D399"), unsafe_allow_html=True)
        if st.button("Start Reading", key="qs_reading", use_container_width=True):
            st.session_state.practice_mode = "Reading - Academic passage"
            st.session_state.current_view = "practice"
            st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── STATS ──
    user_id = st.session_state.get("user_id", "demo")
    sessions = get_user_sessions(user_id, limit=30) if user_id != "demo" else []
    total_sessions = len(sessions)
    total_msgs = sum(s.get("message_count", 0) for s in sessions)

    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        st.metric("Total Sessions", total_sessions)
    with sc2:
        st.metric("Messages Sent", total_msgs)
    with sc3:
        st.metric("Day Streak", f"🔥 {streak}")
    with sc4:
        challenge_day = profile.get("challenge_day", 0)
        st.metric("Challenge Day", f"{challenge_day}/21")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── BOTTOM ROW ──
    err_col, sess_col = st.columns([1, 1])

    with err_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-weight:700;font-size:13px;color:{accent};
                    margin-bottom:12px;letter-spacing:0.04em;text-transform:uppercase">
            Top Recurring Errors
        </div>
        """, unsafe_allow_html=True)
        errors = get_recurring_errors(user_id) if user_id != "demo" else _demo_errors()
        if errors:
            for err in errors[:5]:
                cat_color = {
                    "grammar": "#E74C3C", "vocabulary": "#F0C040",
                    "structure": "#38BDF8", "pronunciation": "#A78BFA"
                }.get(err.get("error_category", "grammar"), "#888")
                st.markdown(f"""
                <div style="display:flex;align-items:center;justify-content:space-between;
                            padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
                    <div>
                        <div style="font-size:13px;color:#dde6f0">{err['description']}</div>
                        <div style="font-size:11px;color:rgba(255,255,255,0.35);margin-top:2px">
                            <span style="color:{cat_color}">{err['error_category'].title()}</span>
                            &nbsp;·&nbsp; seen {err['frequency']}x
                        </div>
                    </div>
                    <div style="font-size:11px;font-weight:700;color:{cat_color};
                                background:{cat_color}22;padding:3px 10px;border-radius:20px">
                        x{err['frequency']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""<div style="font-size:13px;color:rgba(255,255,255,0.3);
                text-align:center;padding:20px 0">No errors tracked yet. Start practicing!</div>""",
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with sess_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-weight:700;font-size:13px;color:{accent};
                    margin-bottom:12px;letter-spacing:0.04em;text-transform:uppercase">
            Recent Sessions
        </div>
        """, unsafe_allow_html=True)
        recent = sessions[:5] if sessions else _demo_sessions()
        if recent:
            for s in recent:
                skill = s.get("mode", "General").split("-")[0].strip()
                icon = {"Speaking": "🎤", "Writing": "✍️", "Listening": "🎧",
                        "Reading": "📖", "Vocabulary": "📚"}.get(skill, "🎓")
                band = s.get("overall_band")
                try:
                    band_color = "#2ECC71" if band and float(band) >= 7 else "#F0C040"
                except (ValueError, TypeError):
                    band_color = "#F0C040"
                created = str(s.get("created_at", ""))[:10] or "Today"
                band_display_val = str(band) if band else "-"
                st.markdown(f"""
                <div style="display:flex;align-items:center;justify-content:space-between;
                            padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
                    <div style="display:flex;align-items:center;gap:10px">
                        <div style="font-size:20px">{icon}</div>
                        <div>
                            <div style="font-size:13px;color:#dde6f0">{skill}</div>
                            <div style="font-size:11px;color:rgba(255,255,255,0.35)">{s.get('topic','')} · {created}</div>
                        </div>
                    </div>
                    <div style="font-size:16px;font-weight:800;color:{band_color}">{band_display_val}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""<div style="font-size:13px;color:rgba(255,255,255,0.3);
                text-align:center;padding:20px 0">No sessions yet. Start your first practice!</div>""",
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def _quick_card(icon, title, subtitle, color):
    # Convert hex color to rgba for background
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    return f"""<div style="background:rgba({r},{g},{b},0.07);border-radius:16px;border:1px solid rgba({r},{g},{b},0.2);padding:16px;margin-bottom:10px;text-align:center"><div style="font-size:28px;margin-bottom:6px">{icon}</div><div style="font-size:14px;font-weight:700;color:{color}">{title}</div><div style="font-size:11px;color:rgba(255,255,255,0.35);margin-top:2px">{subtitle}</div></div>"""


def _demo_errors():
    return [
        {"description": "Misuse of present perfect tense", "error_category": "grammar", "frequency": 8},
        {"description": "Overuse of 'however' as connector", "error_category": "vocabulary", "frequency": 6},
        {"description": "Missing overview in Task 1", "error_category": "structure", "frequency": 5},
        {"description": "Lack of specific examples in body", "error_category": "structure", "frequency": 4},
        {"description": "Informal vocabulary in writing", "error_category": "vocabulary", "frequency": 3},
    ]


def _demo_sessions():
    return [
        {"mode": "Speaking - Part 1", "topic": "Technology", "overall_band": 6.0, "created_at": "2026-04-01"},
        {"mode": "Writing - Task 2", "topic": "Education", "overall_band": 5.5, "created_at": "2026-03-31"},
        {"mode": "Reading - Academic", "topic": "Environment", "overall_band": 6.5, "created_at": "2026-03-30"},
        {"mode": "Listening - Section 1", "topic": "Health", "overall_band": 7.0, "created_at": "2026-03-29"},
        {"mode": "Vocabulary", "topic": "Technology", "overall_band": None, "created_at": "2026-03-28"},
    ]
