# ============================================================
# utils/styles.py
# Global CSS — Blue + White calm theme
# Primary: #4A9EFF (electric blue)
# Background: #0B1120 → #0F1A2E (deep navy, calm)
# Cards: rgba white on navy — cozy, not crypto
# ============================================================

import streamlit as st


def inject_global_css(accent: str = "#4A9EFF"):
    st.markdown(f"""
    <style>

    /* ── BASE ── */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
        background: linear-gradient(160deg, #0B1120 0%, #0F1A2E 40%, #111D35 70%, #0B1120 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: #E8EFF8;
    }}
    [data-testid="stHeader"] {{ background: transparent !important; }}

    /* ── HIDE SIDEBAR ── */
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    button[kind="headerNoPadding"],
    [data-testid="stSidebarNav"] {{
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
        overflow: hidden !important;
    }}

    .main .block-container {{
        background: transparent !important;
        padding-top: 0.5rem;
        max-width: 1280px;
    }}

    /* ── CARDS ── */
    .glass-card {{
        background: rgba(255,255,255,0.06);
        border-radius: 20px;
        border: 1px solid rgba(74,158,255,0.15);
        padding: 20px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.25);
        margin-bottom: 16px;
    }}

    /* ── TOP NAV ── */
    .top-nav {{
        background: rgba(15,26,46,0.9);
        border-radius: 18px;
        border: 1px solid rgba(74,158,255,0.2);
        padding: 12px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.3);
    }}
    .top-nav-brand {{ display: flex; align-items: center; gap: 12px; }}
    .top-nav-brand-text {{ font-size: 18px; font-weight: 700; color: #4A9EFF; letter-spacing: 0.02em; }}
    .top-nav-brand-sub {{ font-size: 10px; color: rgba(255,255,255,0.35); letter-spacing: 0.1em; text-transform: uppercase; }}

    /* ── NAV TABS ── */
    .nav-tab-bar {{
        display: flex;
        gap: 6px;
        background: rgba(255,255,255,0.03);
        border-radius: 14px;
        padding: 5px;
        margin-bottom: 20px;
        border: 1px solid rgba(74,158,255,0.1);
        flex-wrap: wrap;
    }}
    .nav-tab {{
        padding: 8px 16px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 600;
        color: rgba(255,255,255,0.45);
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        background: transparent;
    }}
    .nav-tab.active {{
        background: rgba(74,158,255,0.15);
        color: #4A9EFF;
        border: 1px solid rgba(74,158,255,0.35);
    }}

    /* ── BUTTONS ── */
    .stButton > button {{
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 10px 18px !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        background: rgba(255,255,255,0.06) !important;
        color: #C8D8F0 !important;
        border: 1px solid rgba(74,158,255,0.2) !important;
    }}
    .stButton > button:hover {{
        background: rgba(74,158,255,0.12) !important;
        color: #ffffff !important;
        border-color: rgba(74,158,255,0.4) !important;
        transform: translateY(-1px);
    }}
    .btn-primary > button {{
        background: #4A9EFF !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 16px rgba(74,158,255,0.3) !important;
    }}
    .btn-primary > button:hover {{
        background: #6BB3FF !important;
        box-shadow: 0 6px 20px rgba(74,158,255,0.45) !important;
        transform: translateY(-2px) !important;
    }}
    button[kind="secondary"] {{
        background: transparent !important;
        color: #FF6B6B !important;
        border: 1px solid rgba(255,107,107,0.3) !important;
        border-radius: 12px !important;
    }}

    /* ── CHAT MESSAGES ── */
    [data-testid="stChatMessage"] {{
        background: transparent !important;
        border: none !important;
        padding: 4px 0 !important;
    }}
    [data-testid="stChatMessage"][data-author="user"] > div:last-child {{
        background: rgba(74,158,255,0.1) !important;
        border-radius: 18px 18px 4px 18px !important;
        border: 1px solid rgba(74,158,255,0.2) !important;
        padding: 14px 18px !important;
        color: #E8F0FB !important;
        margin-left: auto !important;
        max-width: 85% !important;
    }}
    [data-testid="stChatMessage"][data-author="assistant"] > div:last-child {{
        background: rgba(255,255,255,0.05) !important;
        border-radius: 18px 18px 18px 4px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        padding: 18px 22px !important;
        max-width: 95% !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span {{
        font-size: 15px !important;
        line-height: 1.85 !important;
        color: #D8E8F8 !important;
        letter-spacing: 0.01em !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong {{
        color: #4A9EFF !important;
        font-weight: 600 !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3 {{
        color: #4A9EFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        margin: 1rem 0 0.4rem !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {{
        margin-bottom: 6px !important;
        color: #D8E8F8 !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] hr {{
        border-color: rgba(74,158,255,0.3) !important;
        margin: 12px 0 !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code {{
        background: rgba(74,158,255,0.12) !important;
        color: #4A9EFF !important;
        padding: 2px 7px !important;
        border-radius: 5px !important;
        font-size: 13px !important;
    }}

    /* ── PRACTICE FEEDBACK — SELECTABLE ── */
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {{
        user-select: text !important;
        -webkit-user-select: text !important;
        cursor: text !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] * {{
        user-select: text !important;
        -webkit-user-select: text !important;
    }}

    /* ── CHAT INPUT ── */
    [data-testid="stChatInput"] {{
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(74,158,255,0.25) !important;
        border-radius: 14px !important;
        color: #E8EFF8 !important;
    }}
    [data-testid="stChatInput"]:focus-within {{
        border-color: rgba(74,158,255,0.6) !important;
        box-shadow: 0 0 0 3px rgba(74,158,255,0.12) !important;
    }}

    /* ── TEXT INPUTS ── */
    [data-testid="stTextInput"] input,
    [data-baseweb="input"] input,
    .stTextInput input,
    input[type="text"],
    input[type="email"],
    input[type="password"],
    input[type="number"] {{
        color: #1a1a2e !important;
        background: #ffffff !important;
        caret-color: #1a1a2e !important;
        border-radius: 10px !important;
    }}
    [data-testid="stTextArea"] textarea,
    [data-baseweb="textarea"] textarea {{
        color: #1a1a2e !important;
        background: #ffffff !important;
        border-radius: 10px !important;
        user-select: text !important;
        -webkit-user-select: text !important;
    }}
    [data-testid="stSelectbox"] > div > div {{
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(74,158,255,0.2) !important;
        border-radius: 10px !important;
        color: #E8EFF8 !important;
    }}
    [data-testid="stSlider"] > div > div > div {{ background: #4A9EFF !important; }}

    /* ── METRICS ── */
    [data-testid="stMetric"] {{
        background: rgba(255,255,255,0.05) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        border: 1px solid rgba(74,158,255,0.12) !important;
    }}
    [data-testid="stMetricValue"] {{ color: #4A9EFF !important; font-weight: 700 !important; }}
    [data-testid="stMetricLabel"] {{ color: rgba(255,255,255,0.4) !important; }}

    /* ── ALERTS ── */
    [data-testid="stAlert"] {{
        background: rgba(74,158,255,0.06) !important;
        border-left: 3px solid #4A9EFF !important;
        border-radius: 12px !important;
        color: #D8E8F8 !important;
    }}
    [data-testid="stStatus"], [data-testid="stStatusWidget"] {{
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(74,158,255,0.3) !important;
        border-radius: 12px !important;
        color: #D8E8F8 !important;
    }}
    [data-testid="stExpander"] {{
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(74,158,255,0.12) !important;
        border-radius: 14px !important;
    }}

    /* ── PILLS ── */
    .pill {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; margin-right: 6px; letter-spacing: 0.04em; }}
    .pill-blue {{ background: rgba(74,158,255,0.12); color: #4A9EFF; border: 1px solid rgba(74,158,255,0.3); }}
    .pill-green {{ background: rgba(46,204,113,0.1); color: #2ECC71; border: 1px solid rgba(46,204,113,0.25); }}
    .pill-red {{ background: rgba(255,107,107,0.1); color: #FF6B6B; border: 1px solid rgba(255,107,107,0.25); }}
    .pill-gold {{ background: rgba(240,192,64,0.1); color: #F0C040; border: 1px solid rgba(240,192,64,0.25); }}
    .pill-purple {{ background: rgba(167,139,250,0.1); color: #A78BFA; border: 1px solid rgba(167,139,250,0.25); }}

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(74,158,255,0.35); border-radius: 4px; }}

    /* ── PROGRESS ── */
    .progress-bar-wrap {{
        background: rgba(255,255,255,0.08);
        border-radius: 8px;
        height: 7px;
        overflow: hidden;
        margin: 6px 0;
    }}
    .progress-bar-fill {{
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #4A9EFF, #6BB3FF);
        transition: width 0.4s ease;
    }}

    /* ── BAND RING ── */
    .band-ring {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 72px;
        height: 72px;
        border-radius: 50%;
        border: 3px solid #4A9EFF;
        font-size: 22px;
        font-weight: 800;
        color: #4A9EFF;
        background: rgba(74,158,255,0.08);
    }}

    /* ── MOTIVATIONAL QUOTE BOX ── */
    .quote-box {{
        background: linear-gradient(135deg, rgba(74,158,255,0.08), rgba(74,158,255,0.03));
        border-left: 3px solid #4A9EFF;
        border-radius: 0 12px 12px 0;
        padding: 14px 18px;
        margin: 12px 0;
    }}
    .quote-text {{
        font-size: 15px;
        font-style: italic;
        color: rgba(255,255,255,0.75);
        line-height: 1.7;
        margin-bottom: 6px;
    }}
    .quote-author {{
        font-size: 11px;
        color: #4A9EFF;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }}

    /* ── CHALLENGE CALENDAR ── */
    .challenge-day {{
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 700;
        margin: 0 auto 4px auto;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.04);
        color: rgba(255,255,255,0.3);
        cursor: default;
    }}
    .challenge-day.done {{
        background: rgba(74,158,255,0.15);
        border-color: rgba(74,158,255,0.5);
        color: #4A9EFF;
    }}
    .challenge-day.today {{
        background: rgba(74,158,255,0.25);
        border-color: #4A9EFF;
        color: #ffffff;
        animation: pulse-blue 2s infinite;
    }}
    .challenge-day.locked {{ opacity: 0.25; }}
    .challenge-day.clickable {{
        cursor: pointer;
        border-color: rgba(74,158,255,0.4);
        color: rgba(255,255,255,0.6);
    }}
    .challenge-day.clickable:hover {{
        background: rgba(74,158,255,0.1);
        border-color: #4A9EFF;
        color: #4A9EFF;
    }}
    .challenge-label {{
        font-size: 9px;
        text-align: center;
        margin-top: 2px;
        color: rgba(255,255,255,0.3);
        font-weight: 400;
    }}
    .challenge-label.today-label {{
        color: #4A9EFF;
        font-weight: 700;
    }}
    @keyframes pulse-blue {{
        0%, 100% {{ box-shadow: 0 0 12px rgba(74,158,255,0.4); }}
        50% {{ box-shadow: 0 0 22px rgba(74,158,255,0.7); }}
    }}

    /* ── TABS ── */
    [data-testid="stTabs"] [role="tab"] {{
        color: rgba(255,255,255,0.5) !important;
        font-weight: 600 !important;
    }}
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
        color: #4A9EFF !important;
        border-bottom-color: #4A9EFF !important;
    }}

    /* ── MOBILE ── */
    @media screen and (max-width: 768px) {{
        .main .block-container {{
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }}
        [data-testid="stChatMessage"][data-author="assistant"] > div:last-child {{
            max-width: 100% !important;
            padding: 14px 16px !important;
        }}
        .glass-card {{ border-radius: 14px !important; padding: 14px !important; }}
        .top-nav {{ padding: 10px 14px !important; border-radius: 12px !important; }}
        .nav-tab {{ font-size: 11px !important; padding: 6px 10px !important; }}
        .band-ring {{ width: 56px; height: 56px; font-size: 18px; }}
        .challenge-day {{ width: 36px; height: 36px; font-size: 11px; border-radius: 8px; }}
    }}
    @media screen and (max-width: 480px) {{
        .main .block-container {{
            padding-left: 0.25rem !important;
            padding-right: 0.25rem !important;
        }}
        .glass-card {{ border-radius: 10px !important; padding: 10px !important; }}
    }}

    </style>
    """, unsafe_allow_html=True)
