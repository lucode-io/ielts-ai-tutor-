# utils/styles.py
import streamlit as st


def inject_global_css(accent: str = "#4A9EFF"):
    """Global CSS matching ieltsmaster.org theme. Accepts dynamic accent color."""
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;800&family=Inter:wght@400;500;600;700&display=swap');

    /* ===== THEME ===== */
    html, body, [class*="css"], .stApp {{
        background: #01010a !important;
        color: #f0f4ff !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }}
    h1, h2, h3, h4, h5 {{
        font-family: 'Syne', sans-serif !important;
        color: #f0f4ff !important;
    }}

    /* Hide Streamlit chrome */
    #MainMenu, footer, header[data-testid="stHeader"] {{ display: none !important; }}
    [data-testid="stSidebarNav"] {{ display: none !important; }}

    /* Page padding */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 960px !important;
    }}

    /* ===== TOP NAV HEADER (im-top-nav) ===== */
    .im-top-nav {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 18px;
        background: rgba(74,158,255,0.04);
        border: 1px solid rgba(74,158,255,0.12);
        border-radius: 14px;
        margin-bottom: 14px;
        gap: 10px;
    }}
    .im-top-nav-left {{
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
        flex: 1;
    }}
    .im-brand-text {{
        font-family: 'Syne', sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: #f0f4ff;
        letter-spacing: -0.3px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .im-brand-sub {{
        font-size: 0.62rem;
        color: rgba(180,210,255,0.38);
        letter-spacing: 1.5px;
        font-weight: 600;
    }}
    .im-top-nav-right {{
        display: flex;
        align-items: center;
        gap: 6px;
        flex-shrink: 0;
    }}
    .im-user-badge, .im-streak-badge {{
        display: inline-block;
        padding: 6px 12px;
        background: rgba(74,158,255,0.08);
        border: 1px solid rgba(74,158,255,0.15);
        border-radius: 10px;
        font-size: 0.82rem;
        color: #f0f4ff;
        white-space: nowrap;
        max-width: 140px;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .im-streak-badge {{
        background: rgba(240,192,64,0.1);
        border-color: rgba(240,192,64,0.25);
        color: #F0C040;
    }}

    /* ===== STREAMLIT BUTTONS ===== */
    .stButton {{ margin-bottom: 6px !important; }}
    .stButton > button {{
        background: rgba(74,158,255,0.04) !important;
        color: #F0C040 !important;
        border: 1px solid rgba(74,158,255,0.15) !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        min-height: 48px !important;
    }}
    .stButton > button:hover {{
        background: rgba(74,158,255,0.1) !important;
        border-color: rgba(74,158,255,0.35) !important;
        transform: translateY(-1px);
    }}
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {accent} 0%, #1a5fd4 100%) !important;
        color: #fff !important;
        border: 1px solid rgba(74,158,255,0.4) !important;
    }}

    /* ===== GLASS CARD ===== */
    .glass-card {{
        background: rgba(74,158,255,0.04);
        border: 1px solid rgba(74,158,255,0.12);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 14px;
    }}

    /* ===== PRIMARY BTN CLASS ===== */
    .btn-primary {{
        background: linear-gradient(135deg, {accent} 0%, #1a5fd4 100%);
        color: #fff;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
    }}

    /* ===== INPUTS ===== */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {{
        background: rgba(74,158,255,0.04) !important;
        color: #f0f4ff !important;
        border: 1px solid rgba(74,158,255,0.15) !important;
        border-radius: 10px !important;
    }}

    /* ===== MOBILE ===== */
    @media (max-width: 480px) {{
        .block-container {{ padding-left: 12px !important; padding-right: 12px !important; }}
        .im-brand-text {{ font-size: 1.05rem; }}
        .im-brand-sub {{ font-size: 0.55rem; letter-spacing: 1px; }}
        .im-user-badge, .im-streak-badge {{
            max-width: 90px;
            font-size: 0.72rem;
            padding: 5px 9px;
        }}
        .stButton > button {{
            font-size: 0.85rem !important;
            padding: 10px 6px !important;
            min-height: 44px !important;
        }}
    }}

    /* Kill orphan </div> text rendering */
    .stMarkdown code:empty {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)
