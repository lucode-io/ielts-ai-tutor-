# ============================================================
# modules/challenge.py
# 21-Day IELTS Speedrun Challenge with streak logic
# ============================================================

import streamlit as st
from datetime import datetime, date, timedelta
from utils.database import (
    get_challenge_days, complete_challenge_day,
    update_user_profile, get_user_profile
)

CHALLENGE_TASKS = [
    (1,  "Speaking",   "Part 1 - Talk about yourself for 2 minutes",          "Speaking - Part 1 (Personal questions)"),
    (2,  "Writing",    "Write a Task 1 overview paragraph (50 words)",         "Writing - Task 1 (Graph/Chart description)"),
    (3,  "Listening",  "Section 1 - Complete a form-filling exercise",         "Listening - Section 1 (Conversation)"),
    (4,  "Reading",    "TFNG questions - 10 questions, 12 minutes",            "Reading - Academic passage"),
    (5,  "Vocabulary", "Learn 5 Band 7 words for Technology topic",            "Vocabulary Builder"),
    (6,  "Speaking",   "Part 2 - 2 minute talk from cue card",                "Speaking - Part 2 (Long turn / cue card)"),
    (7,  "Writing",    "Full Task 2 essay - 40 minutes, 250 words",           "Writing - Task 2 (Essay)"),
    (8,  "Listening",  "Section 2 - Monologue comprehension",                  "Listening - Section 2 (Monologue)"),
    (9,  "Reading",    "Matching headings - academic passage",                 "Reading - Academic passage"),
    (10, "Speaking",   "Part 3 - Abstract discussion questions",               "Speaking - Part 3 (Discussion)"),
    (11, "Writing",    "Task 1 full essay - graph description",                "Writing - Task 1 (Graph/Chart description)"),
    (12, "Vocabulary", "Learn 5 Band 7 words for Environment topic",           "Vocabulary Builder"),
    (13, "Listening",  "Section 3 - Academic discussion",                      "Listening - Section 3 (Academic discussion)"),
    (14, "Reading",    "Full 13-question reading test",                        "Reading - Academic passage"),
    (15, "Speaking",   "Mock Speaking Test - all 3 parts",                     "Speaking - Part 1 (Personal questions)"),
    (16, "Writing",    "Task 2 - Argument essay with counter-argument",        "Writing - Task 2 (Essay)"),
    (17, "Listening",  "Section 4 - Academic lecture",                         "Listening - Section 4 (Academic lecture)"),
    (18, "Vocabulary", "Vocabulary quiz - review all 30 words",                "Vocabulary Builder"),
    (19, "Reading",    "Speed reading - 20 minutes, 13 questions",             "Reading - Academic passage"),
    (20, "Speaking",   "Full Speaking Practice - recorded",                    "Speaking - Part 3 (Discussion)"),
    (21, "Writing",    "Full Mock Writing Test - Task 1 + Task 2",             "Writing - Task 2 (Essay)"),
]


def render_challenge():
    profile = st.session_state.get("profile", {})
    accent = profile.get("accent_color", "#F0C040")
    user_id = st.session_state.get("user_id", "demo")

    if user_id != "demo":
        completed_days_data = get_challenge_days(user_id)
    else:
        completed_days_data = _demo_challenge_days()

    completed_days = {d["day_number"] for d in completed_days_data}
    current_day = max(completed_days) + 1 if completed_days else 1
    current_day = min(current_day, 21)
    streak = profile.get("streak_count", 0)
    challenge_complete = len(completed_days) >= 21

    # ── HEADER ──
    st.markdown(f"""
    <div class="glass-card" style="background:linear-gradient(135deg,rgba(240,192,64,0.08),rgba(255,255,255,0.02));">
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
            <div>
                <div style="font-size:22px;font-weight:800;color:#fff;margin-bottom:4px">
                    21-Day IELTS Speedrun
                </div>
                <div style="font-size:14px;color:rgba(255,255,255,0.45);margin-bottom:8px">
                    Complete one task every day. Miss a day and the streak resets.
                    Finish all 21 days to unlock your <strong style="color:{accent}">Certificate</strong>.
                </div>
                <div style="display:flex;gap:16px;flex-wrap:wrap">
                    <div style="font-size:13px;color:{accent}">Streak: <strong>{streak} days</strong></div>
                    <div style="font-size:13px;color:rgba(255,255,255,0.4)">Completed: <strong style="color:#2ECC71">{len(completed_days)}/21</strong></div>
                    <div style="font-size:13px;color:rgba(255,255,255,0.4)">Today: <strong style="color:#fff">Day {current_day}</strong></div>
                </div>
            </div>
            <div style="text-align:center">
                <div style="font-size:36px;font-weight:900;color:{accent}">
                    {len(completed_days)}<span style="font-size:18px;color:rgba(255,255,255,0.3)">/21</span>
                </div>
                <div class="progress-bar-wrap" style="width:120px;margin-top:6px">
                    <div class="progress-bar-fill" style="width:{int(len(completed_days)/21*100)}%"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CERTIFICATE ──
    if challenge_complete:
        st.markdown(f"""
        <div style="background:{accent}22;border:2px solid {accent}66;border-radius:20px;
                    padding:24px;text-align:center;margin-bottom:20px">
            <div style="font-size:48px;margin-bottom:8px">🏆</div>
            <div style="font-size:22px;font-weight:800;color:{accent};margin-bottom:6px">Challenge Complete!</div>
            <div style="font-size:14px;color:rgba(255,255,255,0.6)">
                You completed the 21-Day IELTS Speedrun. Your certificate is ready.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Download Certificate", key="dl_cert"):
            _generate_certificate(profile)
        return

    # ── CALENDAR GRID ──
    st.markdown(f"""
    <div style="font-size:13px;font-weight:700;color:{accent};
                letter-spacing:0.06em;text-transform:uppercase;margin:20px 0 14px">
        Challenge Calendar
    </div>
    """, unsafe_allow_html=True)

    for row in range(3):
        cols = st.columns(7)
        for col_idx in range(7):
            day_num = row * 7 + col_idx + 1
            task = CHALLENGE_TASKS[day_num - 1]
            is_done = day_num in completed_days
            is_today = day_num == current_day
            is_locked = day_num > current_day

            day_class = "done" if is_done else "today" if is_today else "locked" if is_locked else ""
            day_text = "✓" if is_done else str(day_num)
            label_text = "TODAY" if is_today else f"Day {day_num}"
            label_class = "challenge-label today-label" if is_today else "challenge-label"

            with cols[col_idx]:
                st.markdown(f"""
                <div style="text-align:center;padding:2px 0">
                    <div class="challenge-day {day_class}">{day_text}</div>
                    <div class="{label_class}">{label_text}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── TODAY'S TASK ──
    if current_day <= 21:
        today_task = CHALLENGE_TASKS[current_day - 1]
        skill_colors = {
            "Speaking": "#A78BFA", "Writing": "#38BDF8",
            "Listening": "#FCD34D", "Reading": "#34D399", "Vocabulary": "#F472B6"
        }
        skill_color = skill_colors.get(today_task[1], "#888")

        st.markdown(f"""
        <div class="glass-card" style="border:1px solid {skill_color}44;
                    background:linear-gradient(135deg,{skill_color}08,rgba(255,255,255,0.02))">
            <div style="font-size:11px;color:{skill_color};font-weight:700;
                        letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px">
                Day {current_day} - {today_task[1]}
            </div>
            <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:8px">
                {today_task[2]}
            </div>
            <div style="font-size:13px;color:rgba(255,255,255,0.4)">
                Complete this task to maintain your streak and advance to Day {current_day + 1}.
            </div>
        </div>
        """, unsafe_allow_html=True)

        btn1, btn2, _ = st.columns([1, 1, 2])
        with btn1:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button(f"Start Day {current_day}", key="start_today", use_container_width=True):
                st.session_state.practice_mode = today_task[3]
                st.session_state.current_view = "practice"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with btn2:
            if st.button("Mark as Complete", key="mark_done", use_container_width=True):
                _complete_today(user_id, current_day, today_task, profile)

    # ── ALL TASKS LIST ──
    with st.expander("View All 21 Tasks", expanded=False):
        for day_num, skill, task_desc, mode_key in CHALLENGE_TASKS:
            is_done = day_num in completed_days
            is_locked = day_num > current_day
            skill_color = {
                "Speaking": "#A78BFA", "Writing": "#38BDF8",
                "Listening": "#FCD34D", "Reading": "#34D399", "Vocabulary": "#F472B6"
            }.get(skill, "#888")
            status_icon = "✅" if is_done else "🔒" if is_locked else "▶️"
            opacity = "0.4" if is_locked else "1"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:8px 0;
                        border-bottom:1px solid rgba(255,255,255,0.04);opacity:{opacity}">
                <div style="font-size:16px;min-width:20px">{status_icon}</div>
                <div style="min-width:50px;font-size:11px;color:{skill_color};
                            font-weight:700;text-transform:uppercase">Day {day_num}</div>
                <div style="flex:1">
                    <span style="font-size:13px;color:#dde6f0">{task_desc}</span>
                    <span style="font-size:11px;color:{skill_color};margin-left:8px;
                                 background:{skill_color}18;padding:2px 8px;border-radius:10px">{skill}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


def _complete_today(user_id, day_num, task, profile):
    if user_id != "demo":
        success = complete_challenge_day(user_id, day_num, task[1])
        if success:
            updated = get_user_profile(user_id)
            if updated:
                st.session_state.profile = updated
            st.toast(f"Day {day_num} complete! Streak updated!", icon="✅")
            st.rerun()
    else:
        st.toast(f"Day {day_num} complete! (Demo mode)", icon="✅")


def _generate_certificate(profile):
    name = profile.get("full_name", "Student")
    target = profile.get("target_band", 7.0)
    today = date.today().strftime("%B %d, %Y")
    cert = f"""
IELTS MASTER - 21 DAY CERTIFICATE
===================================

This certifies that

{name.upper()}

has successfully completed the
21-Day IELTS Speedrun Challenge

Target Band: {target}
Completed:   {today}

Powered by IELTS Master AI
ielts-ai-tutor.streamlit.app
"""
    st.download_button(
        "Download Certificate (.txt)",
        cert,
        file_name=f"IELTS_Certificate_{name.replace(' ','_')}.txt",
        mime="text/plain"
    )


def _demo_challenge_days():
    base = datetime.utcnow()
    return [
        {"day_number": i, "task_type": CHALLENGE_TASKS[i-1][1],
         "completed_at": (base - timedelta(days=3-i)).isoformat()}
        for i in range(1, 4)
    ]
