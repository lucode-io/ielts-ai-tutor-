# utils/styles.py
import streamlit as st

def inject_global_css():
    st.markdown("""
    <style>
    /* ===== GLOBAL THEME ===== */
    html, body, [class*="css"], .stApp {
        background: #01010a !important;
        color: #f0f4ff !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    h1, h2, h3, h4, h5 { font-family: 'Syne', sans-serif !important; }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header[data-testid="stHeader"] { display: none !important; }

    /* Reduce top padding on mobile */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 720px !important;
    }

    /* ===== APP HEADER ===== */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 16px;
        background: rgba(74,158,255,0.04);
        border: 1px solid rgba(74,158,255,0.12);
        border-radius: 14px;
        margin-bottom: 18px;
        gap: 10px;
    }
    .app-header-left {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
        flex: 1;
    }
    .app-logo {
        font-size: 1.6rem;
        width: 44px; height: 44px;
        display: flex; align-items: center; justify-content: center;
        background: rgba(74,158,255,0.08);
        border-radius: 10px;
        flex-shrink: 0;
    }
    .app-title-group { min-width: 0; }
    .app-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: #f0f4ff;
        letter-spacing: -0.3px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .app-subtitle {
        font-size: 0.65rem;
        color: rgba(180,210,255,0.38);
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    .app-header-right { flex-shrink: 0; }
    .app-greet {
        display: inline-block;
        padding: 8px 14px;
        background: rgba(74,158,255,0.08);
        border: 1px solid rgba(74,158,255,0.15);
        border-radius: 10px;
        font-size: 0.85rem;
        color: #f0f4ff;
        white-space: nowrap;
        max-width: 140px;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* ===== NAV BUTTONS (mobile-optimized spacing) ===== */
    .stButton { margin-bottom: 8px !important; }
    .stButton > button {
        background: rgba(74,158,255,0.04) !important;
        color: #F0C040 !important;
        border: 1px solid rgba(74,158,255,0.15) !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        min-height: 52px !important;
    }
    .stButton > button:hover {
        background: rgba(74,158,255,0.1) !important;
        border-color: rgba(74,158,255,0.35) !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4A9EFF 0%, #1a5fd4 100%) !important;
        color: #fff !important;
        border: 1px solid rgba(74,158,255,0.4) !important;
    }

    /* ===== GLASS CARD ===== */
    .glass-card {
        background: rgba(74,158,255,0.04);
        border: 1px solid rgba(74,158,255,0.12);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 14px;
    }

    /* ===== MOBILE OPTIMIZATION ===== */
    @media (max-width: 480px) {
        .block-container { padding-left: 12px !important; padding-right: 12px !important; }
        .app-title { font-size: 1.1rem; }
        .app-subtitle { font-size: 0.6rem; }
        .app-greet { max-width: 100px; font-size: 0.75rem; padding: 6px 10px; }
        .app-logo { width: 38px; height: 38px; font-size: 1.3rem; }
        .stButton > button { font-size: 0.95rem !important; padding: 12px 10px !important; }
    }

    /* KILL any orphaned literal text like </div> rendering */
    .stMarkdown code:empty { display: none; }
    </style>
    """, unsafe_allow_html=True)
