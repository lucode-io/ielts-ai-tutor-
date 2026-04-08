# ============================================================
# modules/reports.py
# Score history and analytics dashboard
# ============================================================

import streamlit as st
from utils.database import get_score_history, get_user_sessions, get_recurring_errors


def render_reports():
    profile = st.session_state.get("profile", {})
    accent = "#4A9EFF"
    user_id = st.session_state.get("user_id", "demo")

    st.markdown(f"""
    <div style="margin-bottom:20px">
        <div style="font-size:22px;font-weight:800;color:#fff;margin-bottom:4px">
            📊 Score Reports & Analytics
        </div>
        <div style="font-size:14px;color:rgba(180,210,255,0.45)">
            Track your progress across all 4 IELTS skills over time.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if user_id == "demo":
        _render_demo_reports(accent)
        return

    # ── TIME RANGE ──
    days = st.selectbox("Time range", [7, 14, 30, 60, 90],
                        index=2, format_func=lambda d: f"Last {d} days",
                        label_visibility="collapsed", key="report_range")

    # ── SCORE HISTORY CHART ──
    scores = get_score_history(user_id, days=days)

    if scores:
        import pandas as pd
        import plotly.express as px

        df = pd.DataFrame(scores)
        df["recorded_at"] = pd.to_datetime(df["recorded_at"])

        fig = px.line(
            df, x="recorded_at", y="band_score", color="skill",
            markers=True,
            color_discrete_map={
                "speaking": "#A78BFA", "writing": "#38BDF8",
                "reading": "#34D399", "listening": "#FCD34D",
                "general": "#F472B6", "overall": "#4A9EFF"
            }
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(74,158,255,0.03)",
            font=dict(color="rgba(180,210,255,0.6)"),
            xaxis_title="", yaxis_title="Band Score",
            yaxis=dict(range=[3.5, 9.5], dtick=0.5),
            legend=dict(orientation="h", y=-0.15),
            margin=dict(l=40, r=20, t=20, b=40),
            height=360,
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── SKILL AVERAGES ──
        st.markdown(f"""
        <div style="font-size:13px;font-weight:700;color:{accent};
                    letter-spacing:0.06em;text-transform:uppercase;margin:20px 0 12px">
            Skill Averages (Last {days} days)
        </div>
        """, unsafe_allow_html=True)

        skill_cols = st.columns(4)
        for col, (skill, color) in zip(skill_cols, [
            ("speaking", "#A78BFA"), ("writing", "#38BDF8"),
            ("reading", "#34D399"), ("listening", "#FCD34D")
        ]):
            skill_scores = [s["band_score"] for s in scores if s.get("skill") == skill]
            avg = round(sum(skill_scores) / len(skill_scores), 1) if skill_scores else "—"
            count = len(skill_scores)
            with col:
                st.markdown(f"""
                <div style="background:{color}0d;border:1px solid {color}22;
                            border-radius:12px;padding:14px;text-align:center">
                    <div style="font-size:10px;color:{color};text-transform:uppercase;
                                letter-spacing:0.06em;margin-bottom:6px">{skill}</div>
                    <div style="font-size:28px;font-weight:800;color:{color}">{avg}</div>
                    <div style="font-size:10px;color:rgba(180,210,255,0.35);margin-top:4px">
                        {count} session{'s' if count != 1 else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:40px">
            <div style="font-size:36px;margin-bottom:12px">📈</div>
            <div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:6px">
                No scores yet
            </div>
            <div style="font-size:13px;color:rgba(180,210,255,0.45)">
                Complete a practice session to see your scores here.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── RECURRING ERRORS ──
    st.markdown(f"""
    <div style="font-size:13px;font-weight:700;color:{accent};
                letter-spacing:0.06em;text-transform:uppercase;margin:24px 0 12px">
        Top Recurring Errors
    </div>
    """, unsafe_allow_html=True)

    errors = get_recurring_errors(user_id)
    if errors:
        for err in errors[:8]:
            cat = err.get("error_category", "grammar")
            cat_color = {"grammar": "#ff3a4a", "vocabulary": "#F0C040",
                         "structure": "#38BDF8", "pronunciation": "#A78BFA"}.get(cat, "#888")
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                        padding:10px 0;border-bottom:1px solid rgba(74,158,255,0.06)">
                <div>
                    <div style="font-size:13px;color:#D8E8F8">{err['description']}</div>
                    <div style="font-size:11px;color:rgba(180,210,255,0.35);margin-top:2px">
                        <span style="color:{cat_color}">{cat.title()}</span>
                        &nbsp;·&nbsp; seen {err['frequency']}x
                    </div>
                </div>
                <div style="font-size:11px;font-weight:700;color:{cat_color};
                            background:{cat_color}18;padding:3px 10px;border-radius:20px">
                    x{err['frequency']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="font-size:13px;color:rgba(180,210,255,0.3);text-align:center;padding:16px 0">
            No errors tracked yet. Start practicing to build your error profile.
        </div>
        """, unsafe_allow_html=True)


def _render_demo_reports(accent):
    """Show demo data for non-authenticated users."""
    st.markdown("""
    <div class="glass-card" style="text-align:center;padding:32px">
        <div style="font-size:36px;margin-bottom:10px">📊</div>
        <div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:6px">
            Demo Mode
        </div>
        <div style="font-size:13px;color:rgba(180,210,255,0.45);line-height:1.6">
            Score tracking and analytics are available when you create an account.
            Your practice scores will be automatically saved and charted here.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Show demo skill cards
    demo_data = [
        ("🎤", "Speaking", 6.0, "#A78BFA"),
        ("✍️", "Writing", 5.5, "#38BDF8"),
        ("📖", "Reading", 6.5, "#34D399"),
        ("🎧", "Listening", 7.0, "#FCD34D"),
    ]
    cols = st.columns(4)
    for col, (icon, skill, score, color) in zip(cols, demo_data):
        with col:
            st.markdown(f"""
            <div style="background:{color}0d;border:1px solid {color}22;
                        border-radius:12px;padding:14px;text-align:center">
                <div style="font-size:20px;margin-bottom:4px">{icon}</div>
                <div style="font-size:10px;color:{color};text-transform:uppercase;
                            letter-spacing:0.06em;margin-bottom:6px">{skill}</div>
                <div style="font-size:28px;font-weight:800;color:{color}">{score}</div>
                <div style="font-size:10px;color:rgba(180,210,255,0.35);margin-top:4px">
                    Demo score
                </div>
            </div>
            """, unsafe_allow_html=True)
