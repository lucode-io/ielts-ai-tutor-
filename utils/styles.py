# ============================================================
# utils/styles.py
# Global CSS injection for the entire platform
# ============================================================

import streamlit as st


def inject_global_css(accent: str = "#F0C040"):
    """Inject all platform CSS with dynamic accent color."""
    st.markdown(f"""
    <style>
    /* ── GLOBAL ── */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 25%, #1b1b3a 50%, #0d1b2a 75%, #0a0a1a 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: #e0e0e0;
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

    /* ── GLASS CARD ── */
    .glass-card {{
        background: rgba(255,255,255,0.05);
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 20px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 16px;
    }}

    /* ── TOP NAV ── */
    .top-nav {{
        background: rgba(255,255,255,0.04);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 12px 24px;
        backdrop-filter: blur(24px);
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
    }}
    .top-nav-brand {{ display: flex; align-items: center; gap: 12px; }}
    .top-nav-brand-text {{ font-size: 18px; font-weight: 700; color: {accent}; letter-spacing: 0.03em; }}
    .top-nav-brand-sub {{ font-size: 10px; color: rgba(255,255,255,0.35); letter-spacing: 0.1em; text-transform: uppercase; }}

    /* ── NAV TABS ── */
    .nav-tab-bar {{
        display: flex;
        gap: 6px;
        background: rgba(255,255,255,0.03);
        border-radius: 16px;
        padding: 6px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.06);
        flex-wrap: wrap;
    }}
    .nav-tab {{
        padding: 8px 16px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 600;
        color: rgba(255,255,255,0.45);
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        background: transparent;
    }}
    .nav-tab.active {{
        background: {accent}22;
        color: {accent};
        border: 1px solid {accent}44;
    }}

    /* ── BUTTONS ── */
    .stButton > button {{
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 10px 18px !important;
        transition: all 0.25s ease !important;
        width: 100% !important;
        background: rgba(255,255,255,0.06) !important;
        color: #CBD5E8 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        backdrop-filter: blur(8px) !important;
    }}
    .stButton > button:hover {{
        background: rgba(255,255,255,0.12) !important;
        color: #ffffff !important;
        border-color: rgba(255,255,255,0.25) !important;
        transform: translateY(-1px);
    }}
    .btn-primary > button {{
        background: linear-gradient(135deg, {accent} 0%, {accent}cc 100%) !important;
        color: #0a0a1a !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 0 20px {accent}44 !important;
    }}
    .btn-primary > button:hover {{
        box-shadow: 0 0 30px {accent}66 !important;
        transform: translateY(-2px) scale(1.02) !important;
    }}
    button[kind="secondary"] {{
        background: transparent !important;
        color: #E74C3C !important;
        border: 1px solid rgba(231,76,60,0.3) !important;
        border-radius: 14px !important;
    }}

    /* ── CHAT MESSAGES ── */
    [data-testid="stChatMessage"] {{
        background: transparent !important;
        border: none !important;
        padding: 4px 0 !important;
    }}
    [data-testid="stChatMessage"][data-author="user"] > div:last-child {{
        background: rgba(0,123,255,0.08) !important;
        border-radius: 20px 20px 4px 20px !important;
        border: 1px solid rgba(0,123,255,0.15) !important;
        padding: 14px 18px !important;
        color: #e0e8f8 !important;
        margin-left: auto !important;
        max-width: 85% !important;
    }}
    [data-testid="stChatMessage"][data-author="assistant"] > div:last-child {{
        background: rgba(255,255,255,0.05) !important;
        border-radius: 20px 20px 20px 4px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        padding: 20px 24px !important;
        max-width: 95% !important;
    }}

    /* ── TYPOGRAPHY IN CHAT ── */
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span {{
        font-size: 15px !important;
        line-height: 1.85 !important;
        color: #dde6f0 !important;
        letter-spacing: 0.012em !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong {{
        color: {accent} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3 {{
        color: {accent} !important;
        font-weight: 700 !important;
        font-size: 17px !important;
        margin: 1.2rem 0 0.4rem !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {{
        margin-bottom: 8px !important;
        color: #dde6f0 !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] hr {{
        border-color: {accent}44 !important;
        margin: 14px 0 !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code {{
        background: {accent}18 !important;
        color: {accent} !important;
        padding: 2px 7px !important;
        border-radius: 6px !important;
        font-size: 13px !important;
    }}

    /* ── INPUTS ── */
    [data-testid="stChatInput"] {{
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        color: #e0e0e0 !important;
    }}
    [data-testid="stChatInput"]:focus-within {{
        border-color: {accent}88 !important;
        box-shadow: 0 0 0 3px {accent}18 !important;
    }}
    [data-testid="stTextInput"] input,
    [data-testid="stTextInput"] textarea {{
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #e0e0e0 !important;
    }}
    [data-testid="stSelectbox"] > div > div {{
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #e0e0e0 !important;
    }}
    [data-testid="stSlider"] > div > div > div {{ background: {accent} !important; }}

    /* ── METRICS ── */
    [data-testid="stMetric"] {{
        background: rgba(255,255,255,0.04) !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }}
    [data-testid="stMetricValue"] {{ color: {accent} !important; font-weight: 700 !important; }}
    [data-testid="stMetricLabel"] {{ color: rgba(255,255,255,0.4) !important; }}

    /* ── ALERTS / STATUS ── */
    [data-testid="stAlert"] {{
        background: rgba(255,255,255,0.04) !important;
        border-left: 4px solid {accent} !important;
        border-radius: 14px !important;
        color: #e0e0e0 !important;
    }}
    [data-testid="stStatus"], [data-testid="stStatusWidget"] {{
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid {accent}44 !important;
        border-radius: 16px !important;
        color: #e0e0e0 !important;
    }}
    [data-testid="stExpander"] {{
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
    }}

    /* ── PILLS ── */
    .pill {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 6px;
        letter-spacing: 0.04em;
    }}
    .pill-gold {{ background: {accent}22; color: {accent}; border: 1px solid {accent}44; }}
    .pill-green {{ background: rgba(46,204,113,0.12); color: #2ECC71; border: 1px solid rgba(46,204,113,0.25); }}
    .pill-red {{ background: rgba(231,76,60,0.12); color: #E74C3C; border: 1px solid rgba(231,76,60,0.25); }}
    .pill-blue {{ background: rgba(56,189,248,0.12); color: #38BDF8; border: 1px solid rgba(56,189,248,0.25); }}
    .pill-purple {{ background: rgba(167,139,250,0.12); color: #A78BFA; border: 1px solid rgba(167,139,250,0.25); }}

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: {accent}55; border-radius: 4px; }}

    /* ── PROGRESS BAR ── */
    .progress-bar-wrap {{
        background: rgba(255,255,255,0.08);
        border-radius: 8px;
        height: 8px;
        overflow: hidden;
        margin: 6px 0;
    }}
    .progress-bar-fill {{
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, {accent}, {accent}99);
        transition: width 0.4s ease;
    }}

    /* ── BAND SCORE RING ── */
    .band-ring {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 72px;
        height: 72px;
        border-radius: 50%;
        border: 3px solid {accent};
        font-size: 22px;
        font-weight: 800;
        color: {accent};
        background: {accent}11;
        box-shadow: 0 0 20px {accent}33;
    }}

    /* ── CHALLENGE CALENDAR ── */
    .challenge-day {{
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.04);
        color: rgba(255,255,255,0.3);
    }}
    .challenge-day.done {{
        background: {accent}22;
        border-color: {accent}66;
        color: {accent};
        box-shadow: 0 0 12px {accent}33;
    }}
    .challenge-day.today {{
        background: {accent}44;
        border-color: {accent};
        color: {accent};
        box-shadow: 0 0 20px {accent}55;
        animation: pulse 2s infinite;
    }}
    .challenge-day.locked {{
        opacity: 0.3;
    }}
    @keyframes pulse {{
        0%, 100% {{ box-shadow: 0 0 20px {accent}55; }}
        50% {{ box-shadow: 0 0 30px {accent}88; }}
    }}

    /* ── MOBILE ── */
    @media screen and (max-width: 768px) {{
        /* Hide side panel on mobile */
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2):not(.keep-mobile) {{
            display: none !important;
        }}
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(1) {{
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }}
        /* Keep nav gear button visible */
        [data-testid="stHorizontalBlock"]:first-of-type > [data-testid="stColumn"]:nth-child(2) {{
            display: flex !important;
            visibility: visible !important;
            width: auto !important;
            min-width: 60px !important;
            max-width: 80px !important;
        }}
        .main .block-container {{
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }}
        [data-testid="stChatMessage"][data-author="assistant"] > div:last-child {{
            max-width: 100% !important;
            padding: 14px 16px !important;
        }}
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {{
            font-size: 14px !important;
            line-height: 1.75 !important;
        }}
        .glass-card {{ border-radius: 16px !important; padding: 12px !important; }}
        .top-nav {{ padding: 10px 14px !important; border-radius: 14px !important; }}
        .nav-tab {{ font-size: 11px !important; padding: 6px 10px !important; }}
        .band-ring {{ width: 56px; height: 56px; font-size: 18px; }}
        .challenge-day {{ width: 36px; height: 36px; font-size: 11px; border-radius: 8px; }}
    }}

    @media screen and (max-width: 480px) {{
        .main .block-container {{
            padding-left: 0.25rem !important;
            padding-right: 0.25rem !important;
        }}
        .glass-card {{ border-radius: 12px !important; padding: 10px !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)
