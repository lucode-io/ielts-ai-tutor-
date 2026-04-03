# ============================================================
# modules/challenge.py - with Day 21 Final Mock Test trigger
# ============================================================

import streamlit as st
from datetime import datetime, date, timedelta
from utils.database import (
    get_challenge_days, complete_challenge_day,
    update_user_profile, get_user_profile
)
from utils.certificate import generate_certificate_html

CHALLENGE_TASKS = [
    (1,  "Speaking",   "Part 1 - Talk about yourself for 2 minutes",        "Speaking - Part 1 (Personal questions)"),
    (2,  "Writing",    "Write a Task 1 overview paragraph (50 words)",       "Writing - Task 1 (Graph/Chart description)"),
    (3,  "Listening",  "Section 1 - Complete a form-filling exercise",       "Listening - Section 1 (Conversation)"),
    (4,  "Reading",    "TFNG questions - 10 questions, 12 minutes",          "Reading - Academic passage"),
    (5,  "Vocabulary", "Learn 5 Band 7 words for Technology topic",          "Vocabulary Builder"),
    (6,  "Speaking",   "Part 2 - 2 minute talk from cue card",              "Speaking - Part 2 (Long turn / cue card)"),
    (7,  "Writing",    "Full Task 2 essay - 40 minutes, 250 words",         "Writing - Task 2 (Essay)"),
    (8,  "Listening",  "Section 2 - Monologue comprehension",                "Listening - Section 2 (Monologue)"),
    (9,  "Reading",    "Matching headings - academic passage",               "Reading - Academic passage"),
    (10, "Speaking",   "Part 3 - Abstract discussion questions",             "Speaking - Part 3 (Discussion)"),
    (11, "Writing",    "Task 1 full essay - graph description",              "Writing - Task 1 (Graph/Chart description)"),
    (12, "Vocabulary", "Learn 5 Band 7 words for Environment topic",         "Vocabulary Builder"),
    (13, "Listening",  "Section 3 - Academic discussion",                    "Listening - Section 3 (Academic discussion)"),
    (14, "Reading",    "Full 13-question reading test",                      "Reading - Academic passage"),
    (15, "Speaking",   "Mock Speaking Test - all 3 parts",                   "Speaking - Part 1 (Personal questions)"),
    (16, "Writing",    "Task 2 - Argument essay with counter-argument",      "Writing - Task 2 (Essay)"),
    (17, "Listening",  "Section 4 - Academic lecture",                       "Listening - Section 4 (Academic lecture)"),
    (18, "Vocabulary", "Vocabulary quiz - review all 30 words",              "Vocabulary Builder"),
    (19, "Reading",    "Speed reading - 20 minutes, 13 questions",           "Reading - Academic passage"),
    (20, "Speaking",   "Full Speaking Practice - recorded",                  "Speaking - Part 3 (Discussion)"),
    (21, "Final Test", "FINAL MOCK TEST - All 4 Skills for Certificate",     "mock_test"),
]


def render_challenge():
    profile = st.session_state.get("profile", {})
    accent = profile.get("accent_color", "#F0C040")
    user_id = st.session_state.get("user_id", "demo")

    completed_days_data = get_challenge_days(user_id) if user_id != "demo" else _demo_challenge_days()
    completed_days = {d["day_number"] for d in completed_days_data}
    current_day = min(max(completed_days) + 1 if completed_days else 1, 21)
    streak = profile.get("streak_count", 0)
    challenge_complete = len(completed_days) >= 21

    # ── HEADER ──
    st.markdown(f"""
    <div class="glass-card" style="background:linear-gradient(135deg,rgba(240,192,64,0.08),rgba(255,255,255,0.02));">
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
            <div>
                <div style="font-size:22px;font-weight:800;color:#fff;margin-bottom:4px">21-Day IELTS Speedrun</div>
                <div style="font-size:14px;color:rgba(255,255,255,0.45);margin-bottom:8px">
                    Complete one task every day. Day 21 is the <strong style="color:{accent}">Final Mock Test</strong>.
                    Achieve your target band to earn the <strong style="color:{accent}">Gold Certificate</strong>.
                </div>
                <div style="display:flex;gap:16px;flex-wrap:wrap">
                    <span style="font-size:13px;color:{accent}">Streak: <strong>{streak} days</strong></span>
                    <span style="font-size:13px;color:rgba(255,255,255,0.4)">Done: <strong style="color:#2ECC71">{len(completed_days)}/21</strong></span>
                    <span style="font-size:13px;color:rgba(255,255,255,0.4)">Today: <strong style="color:#fff">Day {current_day}</strong></span>
                </div>
            </div>
            <div style="text-align:center">
                <div style="font-size:36px;font-weight:900;color:{accent}">{len(completed_days)}<span style="font-size:18px;color:rgba(255,255,255,0.3)">/21</span></div>
                <div class="progress-bar-wrap" style="width:120px;margin-top:6px">
                    <div class="progress-bar-fill" style="width:{int(len(completed_days)/21*100)}%"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CERTIFICATE (if complete) ──
    if challenge_complete:
        final_score = profile.get("final_mock_band")
        target = float(profile.get("target_band", 7.0))
        achieved = final_score and float(final_score) >= target
        cert_type = "gold" if achieved else "silver"

        if achieved:
            st.markdown(f"""
            <div style="background:{accent}22;border:2px solid {accent};border-radius:20px;
                        padding:28px;text-align:center;margin-bottom:20px">
                <div style="font-size:44px;margin-bottom:10px">🏆</div>
                <div style="font-size:22px;font-weight:800;color:{accent};margin-bottom:6px">Gold Certificate Earned!</div>
                <div style="font-size:14px;color:rgba(255,255,255,0.6)">
                    You achieved Band {final_score} — target was Band {target}. Outstanding!
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.12);
                        border-radius:20px;padding:28px;text-align:center;margin-bottom:20px">
                <div style="font-size:44px;margin-bottom:10px">🥈</div>
                <div style="font-size:22px;font-weight:800;color:#fff;margin-bottom:6px">Silver Certificate Earned</div>
                <div style="font-size:14px;color:rgba(255,255,255,0.5)">
                    You completed 21 days. {'Score: Band ' + str(final_score) + ' — keep training for gold!' if final_score else 'Take the final test to earn your gold certificate.'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        cert_html = generate_certificate_html(
            full_name=profile.get("full_name", "Student"),
            target_band=target,
            achieved_band=final_score,
            cert_type=cert_type
        )
        label = "🏆 Download Gold Certificate" if achieved else "🥈 Download Silver Certificate"
        st.download_button(label=label, data=cert_html,
                           file_name=f"IELTS_Certificate_{profile.get('full_name','').replace(' ','_')}.html",
                           mime="text/html", key="dl_cert_challenge")
        st.caption("Open in any browser to view, print or share.")
        return

    # ── CALENDAR ──
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
            is_final = day_num == 21

            day_class = "done" if is_done else "today" if is_today else "locked" if is_locked else ""
            day_text = "✓" if is_done else ("🏆" if is_final and not is_locked else str(day_num))
            label_text = "TODAY" if is_today else ("FINAL" if is_final else f"Day {day_num}")
            label_class = "challenge-label today-label" if (is_today or is_final) else "challenge-label"

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
        is_final_day = current_day == 21
        skill_colors = {
            "Speaking": "#A78BFA", "Writing": "#38BDF8", "Listening": "#FCD34D",
            "Reading": "#34D399", "Vocabulary": "#F472B6", "Final Test": "#F0C040"
        }
        skill_color = skill_colors.get(today_task[1], "#888")

        st.markdown(f"""
        <div class="glass-card" style="border:1px solid {skill_color}44;
                    background:linear-gradient(135deg,{skill_color}08,rgba(255,255,255,0.02))">
            <div style="font-size:11px;color:{skill_color};font-weight:700;
                        letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px">
                Day {current_day} — {today_task[1]}
            </div>
            <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:8px">
                {today_task[2]}
            </div>
            <div style="font-size:13px;color:rgba(255,255,255,0.4)">
                {"This is your final assessment. Score your target band to earn the Gold Certificate." if is_final_day else f"Complete this task to maintain your streak and advance to Day {current_day + 1}."}
            </div>
        </div>
        """, unsafe_allow_html=True)

        btn1, btn2, _ = st.columns([1, 1, 2])
        with btn1:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            btn_label = "Start Final Test" if is_final_day else f"Start Day {current_day}"
            if st.button(btn_label, key="start_today", use_container_width=True):
                if is_final_day:
                    for k in list(st.session_state.keys()):
                        if k.startswith("mock_"):
                            del st.session_state[k]
                    st.session_state.mock_stage = "intro"
                    st.session_state.current_view = "mock_test"
                else:
                    st.session_state.practice_mode = today_task[3]
                    st.session_state.current_view = "practice"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with btn2:
            if not is_final_day:
                if st.button("Mark as Complete", key="mark_done", use_container_width=True):
                    _complete_today(user_id, current_day, today_task, profile)

    with st.expander("View All 21 Tasks", expanded=False):
        for day_num, skill, task_desc, _ in CHALLENGE_TASKS:
            is_done = day_num in completed_days
            is_locked = day_num > current_day
            skill_color = {"Speaking":"#A78BFA","Writing":"#38BDF8","Listening":"#FCD34D",
                           "Reading":"#34D399","Vocabulary":"#F472B6","Final Test":"#F0C040"}.get(skill,"#888")
            status_icon = "✅" if is_done else "🔒" if is_locked else ("🏆" if day_num == 21 else "▶️")
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:8px 0;
                        border-bottom:1px solid rgba(255,255,255,0.04);opacity:{'0.4' if is_locked else '1'}">
                <div style="font-size:16px;min-width:20px">{status_icon}</div>
                <div style="min-width:50px;font-size:11px;color:{skill_color};font-weight:700;text-transform:uppercase">Day {day_num}</div>
                <div style="flex:1">
                    <span style="font-size:13px;color:#dde6f0">{task_desc}</span>
                    <span style="font-size:11px;color:{skill_color};margin-left:8px;background:{skill_color}18;padding:2px 8px;border-radius:10px">{skill}</span>
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


def _demo_challenge_days():
    base = datetime.utcnow()
    return [{"day_number": i, "task_type": CHALLENGE_TASKS[i-1][1],
             "completed_at": (base - timedelta(days=3-i)).isoformat()} for i in range(1, 4)]
