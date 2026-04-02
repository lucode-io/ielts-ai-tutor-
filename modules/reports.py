# ============================================================
# modules/reports.py
# Performance dashboard with Plotly charts
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from utils.database import get_score_history, get_user_sessions, get_recurring_errors


def render_reports():
    """Render the full performance & analytics dashboard."""
    profile = st.session_state.get("profile", {})
    accent = profile.get("accent_color", "#F0C040")
    user_id = st.session_state.get("user_id", "demo")

    st.markdown(f"""
    <div style="font-size:22px;font-weight:800;color:#fff;margin-bottom:4px">My Reports</div>
    <div style="font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:24px">
        Track your progress across all 4 IELTS skills
    </div>
    """, unsafe_allow_html=True)

    # ── TIME FILTER ──
    tf_col, _, _ = st.columns([1, 2, 1])
    with tf_col:
        days_filter = st.selectbox(
            "Period",
            ["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
            index=1,
            label_visibility="collapsed",
            key="report_period"
        )
    days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90, "All time": 365}
    days = days_map[days_filter]

    # ── FETCH DATA ──
    if user_id != "demo":
        scores = get_score_history(user_id, days=days)
        sessions = get_user_sessions(user_id, limit=50)
        errors = get_recurring_errors(user_id)
    else:
        scores = _demo_scores()
        sessions = _demo_sessions_data()
        errors = _demo_errors()

    # ── SUMMARY METRICS ──
    _render_summary_metrics(scores, accent)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── CHARTS ROW ──
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        _render_score_trend_chart(scores, accent)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        _render_radar_chart(scores, accent)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── SECOND ROW ──
    hist_col, err_col = st.columns(2)

    with hist_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        _render_session_history(sessions, accent)
        st.markdown('</div>', unsafe_allow_html=True)

    with err_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        _render_error_breakdown(errors, accent)
        st.markdown('</div>', unsafe_allow_html=True)


def _render_summary_metrics(scores, accent):
    """Render the 4 skill summary metric cards."""
    skills = ["speaking", "writing", "reading", "listening"]
    skill_labels = {"speaking": "Speaking 🎤", "writing": "Writing ✍️",
                    "reading": "Reading 📖", "listening": "Listening 🎧"}
    skill_icons = {"speaking": "🎤", "writing": "✍️", "reading": "📖", "listening": "🎧"}

    cols = st.columns(4)
    for i, skill in enumerate(skills):
        skill_scores = [s["band_score"] for s in scores if s["skill"] == skill]
        if skill_scores:
            latest = skill_scores[-1]
            prev = skill_scores[-2] if len(skill_scores) > 1 else latest
            delta = round(latest - prev, 1)
        else:
            latest = None
            delta = None

        with cols[i]:
            if latest:
                delta_str = f"+{delta}" if delta and delta > 0 else str(delta) if delta else "0"
                color = "#2ECC71" if (delta and delta > 0) else "#E74C3C" if (delta and delta < 0) else accent
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;padding:16px">
                    <div style="font-size:22px;margin-bottom:6px">{skill_icons[skill]}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.4);text-transform:uppercase;
                                letter-spacing:0.06em;margin-bottom:8px">{skill.title()}</div>
                    <div style="font-size:32px;font-weight:800;color:{accent}">{latest}</div>
                    <div style="font-size:12px;color:{color};margin-top:4px">{delta_str} vs last</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;padding:16px;opacity:0.5">
                    <div style="font-size:22px;margin-bottom:6px">{skill_icons[skill]}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.4);text-transform:uppercase;
                                letter-spacing:0.06em;margin-bottom:8px">{skill.title()}</div>
                    <div style="font-size:20px;color:rgba(255,255,255,0.3)">No data</div>
                </div>
                """, unsafe_allow_html=True)


def _render_score_trend_chart(scores, accent):
    """Line chart showing score trends over time."""
    st.markdown(f"""
    <div style="font-weight:700;font-size:13px;color:{accent};
                margin-bottom:12px;letter-spacing:0.04em;text-transform:uppercase">
        Score Trend
    </div>
    """, unsafe_allow_html=True)

    if not scores:
        st.markdown("<div style='text-align:center;color:rgba(255,255,255,0.3);padding:40px 0'>No data yet</div>",
                    unsafe_allow_html=True)
        return

    df = pd.DataFrame(scores)
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])

    colors = {
        "speaking": "#A78BFA",
        "writing": "#38BDF8",
        "reading": "#34D399",
        "listening": "#FCD34D"
    }

    fig = go.Figure()
    for skill, color in colors.items():
        skill_data = df[df["skill"] == skill].sort_values("recorded_at")
        if not skill_data.empty:
            fig.add_trace(go.Scatter(
                x=skill_data["recorded_at"],
                y=skill_data["band_score"],
                name=skill.title(),
                line=dict(color=color, width=2.5),
                mode="lines+markers",
                marker=dict(size=6, color=color),
                hovertemplate=f"<b>{skill.title()}</b><br>Band: %{{y}}<br>%{{x|%b %d}}<extra></extra>"
            ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9CA3AF", size=11),
        legend=dict(
            orientation="h", y=-0.2,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9CA3AF")
        ),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.06)",
            zeroline=False, tickfont=dict(color="#6B7280")
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.06)",
            zeroline=False, range=[0, 9.5],
            tickfont=dict(color="#6B7280")
        ),
        margin=dict(l=0, r=0, t=10, b=40),
        height=220
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_radar_chart(scores, accent):
    """Radar chart showing skill balance."""
    st.markdown(f"""
    <div style="font-weight:700;font-size:13px;color:{accent};
                margin-bottom:12px;letter-spacing:0.04em;text-transform:uppercase">
        Skill Balance
    </div>
    """, unsafe_allow_html=True)

    skills = ["speaking", "writing", "reading", "listening"]
    values = []
    for skill in skills:
        skill_scores = [s["band_score"] for s in scores if s["skill"] == skill]
        values.append(round(sum(skill_scores) / len(skill_scores), 1) if skill_scores else 0)

    if all(v == 0 for v in values):
        st.markdown("<div style='text-align:center;color:rgba(255,255,255,0.3);padding:40px 0'>No data yet</div>",
                    unsafe_allow_html=True)
        return

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=["Speaking", "Writing", "Reading", "Listening", "Speaking"],
        fill='toself',
        fillcolor=f"rgba(240,192,64,0.12)",
        line=dict(color=accent, width=2),
        name="Your Scores"
    ))
    fig.add_trace(go.Scatterpolar(
        r=[7, 7, 7, 7, 7],
        theta=["Speaking", "Writing", "Reading", "Listening", "Speaking"],
        line=dict(color="rgba(255,255,255,0.1)", width=1, dash="dot"),
        name="Band 7 Target",
        showlegend=True
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 9],
                gridcolor="rgba(255,255,255,0.08)",
                tickfont=dict(color="#6B7280", size=9)
            ),
            angularaxis=dict(
                tickfont=dict(color="#9CA3AF", size=11),
                gridcolor="rgba(255,255,255,0.08)"
            )
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9CA3AF"),
        legend=dict(
            orientation="h", y=-0.15,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9CA3AF", size=10)
        ),
        margin=dict(l=20, r=20, t=20, b=40),
        height=220
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_session_history(sessions, accent):
    """Table of recent sessions."""
    st.markdown(f"""
    <div style="font-weight:700;font-size:13px;color:{accent};
                margin-bottom:12px;letter-spacing:0.04em;text-transform:uppercase">
        Session History
    </div>
    """, unsafe_allow_html=True)

    if not sessions:
        st.markdown("<div style='text-align:center;color:rgba(255,255,255,0.3);padding:20px 0'>No sessions yet</div>",
                    unsafe_allow_html=True)
        return

    for s in sessions[:8]:
        skill = s.get("mode", "").split("-")[0].strip()
        icon = {"Speaking": "🎤", "Writing": "✍️", "Listening": "🎧",
                "Reading": "📖", "Vocabulary": "📚"}.get(skill, "🎓")
        band = s.get("overall_band")
        band_color = "#2ECC71" if band and float(band) >= 7 else "#F0C040" if band else "rgba(255,255,255,0.3)"
        created = s.get("created_at", "")[:10]

        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;
                    padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
            <div style="display:flex;align-items:center;gap:10px">
                <span style="font-size:18px">{icon}</span>
                <div>
                    <div style="font-size:13px;color:#dde6f0">{s.get('mode','').split('-')[0].strip()}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.3)">{s.get('topic','')} · {created}</div>
                </div>
            </div>
            <div style="font-size:16px;font-weight:800;color:{band_color}">
                {band if band else '-'}
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_error_breakdown(errors, accent):
    """Bar chart of error categories."""
    st.markdown(f"""
    <div style="font-weight:700;font-size:13px;color:{accent};
                margin-bottom:12px;letter-spacing:0.04em;text-transform:uppercase">
        Error Breakdown
    </div>
    """, unsafe_allow_html=True)

    if not errors:
        st.markdown("<div style='text-align:center;color:rgba(255,255,255,0.3);padding:20px 0'>No errors tracked</div>",
                    unsafe_allow_html=True)
        return

    # Group by category
    cat_totals = {}
    for e in errors:
        cat = e.get("error_category", "other")
        cat_totals[cat] = cat_totals.get(cat, 0) + e.get("frequency", 1)

    cat_colors = {
        "grammar": "#E74C3C",
        "vocabulary": "#F0C040",
        "structure": "#38BDF8",
        "pronunciation": "#A78BFA",
        "other": "#888"
    }

    fig = go.Figure(go.Bar(
        x=list(cat_totals.values()),
        y=[c.title() for c in cat_totals.keys()],
        orientation='h',
        marker=dict(
            color=[cat_colors.get(c, "#888") for c in cat_totals.keys()],
            opacity=0.8
        ),
        text=list(cat_totals.values()),
        textposition='outside',
        textfont=dict(color="#9CA3AF", size=11)
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(tickfont=dict(color="#9CA3AF", size=11), gridcolor="rgba(255,255,255,0.04)"),
        margin=dict(l=0, r=40, t=0, b=0),
        height=180,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Top errors list
    for e in errors[:4]:
        cat_color = cat_colors.get(e.get("error_category", "other"), "#888")
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;padding:5px 0;
                    border-bottom:1px solid rgba(255,255,255,0.04)">
            <div style="width:6px;height:6px;border-radius:50%;background:{cat_color};flex-shrink:0"></div>
            <div style="font-size:12px;color:rgba(255,255,255,0.55);flex:1">{e['description']}</div>
            <div style="font-size:11px;color:{cat_color};font-weight:700">x{e['frequency']}</div>
        </div>
        """, unsafe_allow_html=True)


# ── DEMO DATA ──

def _demo_scores():
    base = datetime.utcnow()
    data = []
    skills = {
        "speaking": [5.5, 5.5, 6.0, 6.0, 6.0, 6.5],
        "writing": [5.0, 5.5, 5.5, 6.0, 6.0, 6.0],
        "reading": [6.0, 6.5, 6.5, 7.0, 6.5, 7.0],
        "listening": [5.5, 6.0, 6.0, 6.5, 7.0, 7.0]
    }
    for i in range(6):
        dt = (base - timedelta(days=25 - i * 5)).isoformat()
        for skill, values in skills.items():
            data.append({"skill": skill, "band_score": values[i], "recorded_at": dt})
    return data


def _demo_sessions_data():
    base = datetime.utcnow()
    return [
        {"mode": "Speaking - Part 1", "topic": "Technology", "overall_band": 6.0,
         "created_at": (base - timedelta(days=1)).isoformat()},
        {"mode": "Writing - Task 2", "topic": "Education", "overall_band": 5.5,
         "created_at": (base - timedelta(days=2)).isoformat()},
        {"mode": "Reading - Academic", "topic": "Environment", "overall_band": 7.0,
         "created_at": (base - timedelta(days=3)).isoformat()},
        {"mode": "Listening - Section 2", "topic": "Health", "overall_band": 6.5,
         "created_at": (base - timedelta(days=4)).isoformat()},
        {"mode": "Speaking - Part 3", "topic": "Society", "overall_band": 6.0,
         "created_at": (base - timedelta(days=5)).isoformat()},
    ]


def _demo_errors():
    return [
        {"description": "Misuse of present perfect tense", "error_category": "grammar", "frequency": 8},
        {"description": "Overuse of 'however'", "error_category": "vocabulary", "frequency": 6},
        {"description": "Missing overview paragraph", "error_category": "structure", "frequency": 5},
        {"description": "Lack of specific examples", "error_category": "structure", "frequency": 4},
        {"description": "Informal vocabulary in writing", "error_category": "vocabulary", "frequency": 3},
    ]
