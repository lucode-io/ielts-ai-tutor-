# styles.py — matches ieltsmaster.org exactly
# Colors: #01010a bg | #4A9EFF blue | #1a5fd4 blue2 | #f0f4ff white
# Effects: particle canvas, scanlines, blue glows
import streamlit as st

def inject_global_css(accent: str = "#4A9EFF"):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

    /* ══ NUCLEAR BACKGROUND LOCK ══ */
    html,
    body,
    #root,
    .stApp,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    .appview-container,
    .main,
    .reportview-container
    {{
        background: #01010a !important;
        background-color: #01010a !important;
        color: #f0f4ff !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }}

    /* Block containers — transparent so body #01010a shows through */
    .block-container,
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="element-container"],
    .element-container,
    section.main > div
    {{
        background: transparent !important;
        background-color: transparent !important;
    }}

    /* Markdown containers */
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] > div,
    div[class*="stMarkdown"]
    {{
        background: transparent !important;
        color: #f0f4ff !important;
    }}

    /* Catch Streamlit generated css- classes */
    div[class^="css-"], div[class*=" css-"]
    {{ background-color: transparent !important; }}

    /* Header */
    [data-testid="stHeader"], header[data-testid="stHeader"]
    {{ background: #01010a !important; background-color: #01010a !important; border: none !important; }}

    /* Scanlines */
    [data-testid="stApp"]::before {{
        content: '';
        position: fixed;
        inset: 0;
        background: repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(74,158,255,0.008) 3px,rgba(74,158,255,0.008) 4px);
        pointer-events: none;
        z-index: 0;
    }}

    /* Hide sidebar */
    [data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],button[kind="headerNoPadding"],[data-testid="stSidebarNav"]
    {{ display: none !important; visibility: hidden !important; width: 0 !important; min-width: 0 !important; max-width: 0 !important; overflow: hidden !important; }}

    /* Hide Streamlit branding */
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    [data-testid="stDecoration"] {{ display: none !important; }}
    div[data-testid="stStatusWidget"] {{ display: none !important; }}

    .main .block-container {{ background: transparent !important; padding-top: 0.5rem; max-width: 1280px; position: relative; z-index: 2; }}

    /* ══ GLASS CARD ══ */
    .glass-card {{ background: rgba(74,158,255,0.04); border-radius: 16px; border: 1px solid rgba(74,158,255,0.12); padding: 20px; position: relative; overflow: hidden; margin-bottom: 16px; transition: border-color 0.3s; }}
    .glass-card:hover {{ border-color: rgba(74,158,255,0.22); }}
    .glass-card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(74,158,255,0.3), transparent); }}

    /* ══ TOP NAV ══ */
    .im-top-nav {{ background: rgba(1,1,10,0.92); border-radius: 14px; border: 1px solid rgba(74,158,255,0.12); padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; backdrop-filter: blur(24px); position: relative; z-index: 10; }}
    .im-top-nav-left {{ display: flex; align-items: center; gap: 10px; }}
    .im-top-nav-right {{ display: flex; align-items: center; gap: 12px; }}
    .im-brand-text {{ font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 800; color: #f0f4ff; letter-spacing: 0.05em; }}
    .im-brand-sub {{ font-size: 10px; color: rgba(180,210,255,0.38); letter-spacing: 0.1em; text-transform: uppercase; }}
    .im-user-badge {{ font-size: 13px; color: rgba(255,255,255,0.5); }}
    .im-streak-badge {{ font-size: 13px; color: {accent}; font-weight: 700; }}

    /* ══ NAV BAR ══ */
    .im-nav-bar {{ display: flex; gap: 4px; background: rgba(74,158,255,0.03); border-radius: 12px; padding: 4px; margin-bottom: 16px; border: 1px solid rgba(74,158,255,0.08); flex-wrap: wrap; justify-content: center; position: relative; z-index: 10; }}
    .im-nav-tab {{ background: transparent; border: 1px solid transparent; border-radius: 9px; font-size: 12px; font-weight: 600; padding: 8px 20px; color: rgba(180,210,255,0.45); cursor: pointer; transition: all 0.2s; letter-spacing: 0.03em; font-family: 'Inter', sans-serif; flex: 1; text-align: center; }}
    .im-nav-tab:hover {{ background: rgba(74,158,255,0.06); color: {accent}; border-color: rgba(74,158,255,0.15); }}
    .im-nav-tab.active {{ background: rgba(74,158,255,0.1); color: {accent}; border: 1px solid rgba(74,158,255,0.25); }}

    /* ══ LEGACY NAV ══ */
    .top-nav {{ background: rgba(1,1,10,0.92); border-radius: 14px; border: 1px solid rgba(74,158,255,0.12); padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; backdrop-filter: blur(24px); position: relative; z-index: 2; }}
    .top-nav-brand {{ display: flex; align-items: center; gap: 10px; }}
    .top-nav-brand-text {{ font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 800; color: #f0f4ff; letter-spacing: 0.05em; }}
    .top-nav-brand-text span {{ color: {accent}; }}
    .top-nav-brand-sub {{ font-size: 10px; color: rgba(180,210,255,0.38); letter-spacing: 0.1em; text-transform: uppercase; }}
    .nav-tab-bar {{ display: flex; gap: 4px; background: rgba(74,158,255,0.03); border-radius: 12px; padding: 4px; margin-bottom: 20px; border: 1px solid rgba(74,158,255,0.08); flex-wrap: wrap; }}
    .nav-tab {{ padding: 8px 16px; border-radius: 9px; font-size: 12px; font-weight: 600; color: rgba(180,210,255,0.45); cursor: pointer; transition: all 0.2s; border: none; background: transparent; letter-spacing: 0.03em; }}
    .nav-tab.active {{ background: rgba(74,158,255,0.1); color: {accent}; border: 1px solid rgba(74,158,255,0.25); }}

    /* ══ BUTTONS ══ */
    .stButton > button {{ border-radius: 9px !important; font-weight: 600 !important; font-size: 13px !important; padding: 10px 18px !important; transition: all 0.25s !important; width: 100% !important; background: rgba(74,158,255,0.05) !important; color: #f0f4ff !important; border: 1px solid rgba(74,158,255,0.15) !important; letter-spacing: 0.02em !important; }}
    .stButton > button:hover {{ background: rgba(74,158,255,0.1) !important; color: #fff !important; border-color: rgba(74,158,255,0.35) !important; transform: translateY(-1px) !important; box-shadow: 0 0 20px rgba(74,158,255,0.15) !important; }}
    .btn-primary .stButton > button {{ background: linear-gradient(135deg, {accent}, #1a5fd4) !important; color: #fff !important; border: none !important; font-weight: 700 !important; box-shadow: 0 0 30px rgba(74,158,255,0.25), inset 0 1px 0 rgba(255,255,255,0.1) !important; }}
    .btn-primary .stButton > button:hover {{ transform: translateY(-2px) !important; box-shadow: 0 0 50px rgba(74,158,255,0.45), inset 0 1px 0 rgba(255,255,255,0.1) !important; }}
    button[kind="secondary"] {{ background: transparent !important; color: {accent} !important; border: 1px solid rgba(74,158,255,0.25) !important; border-radius: 9px !important; }}

    /* ══ CHAT MESSAGES ══ */
    [data-testid="stChatMessage"] {{ background: transparent !important; border: none !important; padding: 0 !important; margin: 0 0 20px 0 !important; }}
    [data-testid="stChatMessage"][data-author="user"] > div:last-child {{ background: rgba(74,158,255,0.08) !important; border-radius: 18px 18px 4px 18px !important; border: 1px solid rgba(74,158,255,0.18) !important; padding: 14px 18px !important; margin-left: 20% !important; max-width: 80% !important; float: right !important; }}
    [data-testid="stChatMessage"][data-author="assistant"] > div:last-child {{ background: rgba(255,255,255,0.03) !important; border-radius: 18px 18px 18px 4px !important; border: 1px solid rgba(74,158,255,0.08) !important; padding: 18px 22px !important; margin-right: 10% !important; max-width: 90% !important; }}
    [data-testid="stChatMessage"][data-author="user"]::after {{ content: ''; display: table; clear: both; }}
    [data-testid="stChatMessage"] [data-testid="stAvatar"] {{ width: 28px !important; height: 28px !important; min-width: 28px !important; }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span {{ font-size: 14px !important; line-height: 1.8 !important; color: rgba(200,220,255,0.88) !important; letter-spacing: 0.01em !important; user-select: text !important; -webkit-user-select: text !important; }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong {{ color: {accent} !important; font-weight: 600 !important; }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3 {{ color: {accent} !important; font-weight: 700 !important; font-size: 15px !important; margin: 0.8rem 0 0.3rem !important; }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {{ margin-bottom: 4px !important; color: rgba(180,210,255,0.75) !important; }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] hr {{ border-color: rgba(74,158,255,0.15) !important; margin: 10px 0 !important; }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code {{ background: rgba(74,158,255,0.1) !important; color: {accent} !important; padding: 2px 7px !important; border-radius: 5px !important; font-size: 13px !important; }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {{ user-select: text !important; -webkit-user-select: text !important; cursor: text !important; }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] * {{ user-select: text !important; -webkit-user-select: text !important; }}

    /* ══ CHAT INPUT ══ */
    [data-testid="stChatInput"] {{ background: rgba(74,158,255,0.04) !important; border: 1px solid rgba(74,158,255,0.18) !important; border-radius: 12px !important; color: #f0f4ff !important; }}
    [data-testid="stChatInput"]:focus-within {{ border-color: rgba(74,158,255,0.5) !important; box-shadow: 0 0 0 3px rgba(74,158,255,0.08), 0 0 20px rgba(74,158,255,0.1) !important; }}

    /* ══ FORM INPUTS ══ */
    [data-testid="stTextInput"] input,[data-baseweb="input"] input,.stTextInput input,input[type="text"],input[type="email"],input[type="password"],input[type="number"] {{ color: #0d1117 !important; background: #f0f4ff !important; caret-color: #0d1117 !important; border-radius: 8px !important; border: 1px solid rgba(74,158,255,0.2) !important; }}
    [data-testid="stTextArea"] textarea,[data-baseweb="textarea"] textarea {{ color: #0d1117 !important; background: #f0f4ff !important; border-radius: 8px !important; user-select: text !important; -webkit-user-select: text !important; }}
    [data-testid="stSelectbox"] > div > div {{ background: rgba(74,158,255,0.05) !important; border: 1px solid rgba(74,158,255,0.15) !important; border-radius: 9px !important; color: #f0f4ff !important; }}
    [data-testid="stSlider"] > div > div > div {{ background: {accent} !important; }}

    /* ══ METRICS ══ */
    [data-testid="stMetric"] {{ background: rgba(74,158,255,0.04) !important; border-radius: 12px !important; padding: 14px 18px !important; border: 1px solid rgba(74,158,255,0.1) !important; position: relative; overflow: hidden; }}
    [data-testid="stMetricValue"] {{ background: linear-gradient(135deg, #fff, {accent}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 800 !important; font-family: 'Syne', sans-serif !important; }}
    [data-testid="stMetricLabel"] {{ color: rgba(180,210,255,0.38) !important; }}

    /* ══ ALERTS / STATUS / EXPANDER / TABS ══ */
    [data-testid="stAlert"] {{ background: rgba(74,158,255,0.05) !important; border-left: 3px solid {accent} !important; border-radius: 10px !important; color: rgba(180,210,255,0.85) !important; }}
    [data-testid="stStatus"],[data-testid="stStatusWidget"] {{ background: rgba(74,158,255,0.04) !important; border: 1px solid rgba(74,158,255,0.2) !important; border-radius: 10px !important; color: #f0f4ff !important; }}
    [data-testid="stExpander"] {{ background: rgba(74,158,255,0.03) !important; border: 1px solid rgba(74,158,255,0.1) !important; border-radius: 12px !important; }}
    .stException {{ background: rgba(74,158,255,0.05) !important; border: 1px solid rgba(74,158,255,0.2) !important; color: #f0f4ff !important; }}
    div[data-baseweb="notification"] {{ background: rgba(74,158,255,0.08) !important; }}
    [data-testid="stTabs"] [role="tab"] {{ color: rgba(180,210,255,0.45) !important; font-weight: 600 !important; letter-spacing: 0.03em !important; }}
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {{ color: {accent} !important; border-bottom-color: {accent} !important; }}
    [data-testid="stTabs"] [role="tabpanel"] {{ background: transparent !important; }}

    /* ══ PILLS ══ */
    .pill {{ display: inline-block; padding: 3px 11px; border-radius: 100px; font-size: 11px; font-weight: 600; margin-right: 6px; letter-spacing: 0.05em; }}
    .pill-blue {{ background: rgba(74,158,255,0.1); color: {accent}; border: 1px solid rgba(74,158,255,0.2); }}
    .pill-green {{ background: rgba(0,232,122,0.08); color: #00e87a; border: 1px solid rgba(0,232,122,0.2); }}
    .pill-red {{ background: rgba(255,58,74,0.08); color: #ff3a4a; border: 1px solid rgba(255,58,74,0.2); }}
    .pill-gold {{ background: rgba(240,192,64,0.08); color: #F0C040; border: 1px solid rgba(240,192,64,0.2); }}
    .pill-purple {{ background: rgba(167,139,250,0.08); color: #A78BFA; border: 1px solid rgba(167,139,250,0.2); }}

    /* ══ SCROLLBAR ══ */
    ::-webkit-scrollbar {{ width: 4px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(74,158,255,0.3); border-radius: 4px; }}

    /* ══ PROGRESS BAR ══ */
    .progress-bar-wrap {{ background: rgba(74,158,255,0.08); border-radius: 100px; height: 6px; overflow: hidden; margin: 6px 0; }}
    .progress-bar-fill {{ height: 100%; border-radius: 100px; background: linear-gradient(90deg, {accent}, #1a5fd4); transition: width 0.4s ease; box-shadow: 0 0 8px rgba(74,158,255,0.4); }}

    /* ══ BAND RING ══ */
    .band-ring {{ display: inline-flex; align-items: center; justify-content: center; width: 72px; height: 72px; border-radius: 50%; border: 2px solid {accent}; font-family: 'Syne', sans-serif; font-size: 22px; font-weight: 800; color: {accent}; box-shadow: 0 0 20px rgba(74,158,255,0.2); }}

    /* ══ QUOTE BOX ══ */
    .quote-box {{ background: rgba(74,158,255,0.04); border-left: 2px solid {accent}; border-radius: 0 10px 10px 0; padding: 14px 18px; margin: 12px 0 20px; position: relative; overflow: hidden; }}
    .quote-box::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, {accent}, transparent); }}
    .quote-text {{ font-size: 14px; font-style: italic; color: rgba(180,210,255,0.7); line-height: 1.75; margin-bottom: 6px; }}
    .quote-author {{ font-size: 10px; color: {accent}; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; }}

    /* ══ CHALLENGE DAYS ══ */
    .challenge-day {{ width: 44px; height: 44px; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; margin: 0 auto 4px auto; border: 1px solid rgba(74,158,255,0.08); background: rgba(74,158,255,0.03); color: rgba(180,210,255,0.25); cursor: default; transition: all 0.2s; }}
    .challenge-day.done {{ background: rgba(74,158,255,0.12); border-color: rgba(74,158,255,0.4); color: {accent}; box-shadow: 0 0 10px rgba(74,158,255,0.15); }}
    .challenge-day.today {{ background: rgba(74,158,255,0.18); border-color: {accent}; color: #fff; animation: pulse-blue 2s infinite; box-shadow: 0 0 16px rgba(74,158,255,0.3); }}
    .challenge-day.locked {{ opacity: 0.2; }}
    .challenge-day.clickable {{ cursor: pointer; border-color: rgba(74,158,255,0.2); color: rgba(180,210,255,0.5); }}
    .challenge-day.clickable:hover {{ background: rgba(74,158,255,0.1); border-color: rgba(74,158,255,0.45); color: {accent}; box-shadow: 0 0 10px rgba(74,158,255,0.2); }}
    .challenge-label {{ font-size: 9px; text-align: center; margin-top: 2px; color: rgba(180,210,255,0.25); font-weight: 500; letter-spacing: 0.03em; }}
    .challenge-label.today-label {{ color: {accent}; font-weight: 700; }}

    @keyframes pulse-blue {{
        0%, 100% {{ box-shadow: 0 0 12px rgba(74,158,255,0.3); }}
        50% {{ box-shadow: 0 0 24px rgba(74,158,255,0.6); border-color: rgba(74,158,255,0.9); }}
    }}

    /* ══ HERO / STATS ══ */
    .hero-title {{ font-family: 'Syne', sans-serif; font-size: clamp(28px,5vw,52px); font-weight: 800; line-height: 1; letter-spacing: -0.03em; background: linear-gradient(135deg, #fff 0%, rgba(200,225,255,0.95) 40%, {accent} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
    .stat-num {{ font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #fff, {accent}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1; margin-bottom: 4px; }}
    .stat-label {{ font-size: 10px; color: rgba(180,210,255,0.38); letter-spacing: 0.1em; text-transform: uppercase; font-weight: 500; }}

    /* ══ MOBILE ══ */
    @media (max-width: 768px) {{
        [data-testid="stChatMessage"][data-author="user"] > div:last-child {{ margin-left: 5% !important; max-width: 95% !important; }}
        [data-testid="stChatMessage"][data-author="assistant"] > div:last-child {{ margin-right: 0 !important; max-width: 100% !important; padding: 14px 16px !important; }}
        .im-top-nav {{ padding: 8px 12px !important; border-radius: 10px !important; }}
        .im-brand-text {{ font-size: 14px !important; }}
        .im-nav-tab {{ font-size: 11px !important; padding: 6px 8px !important; }}
        .main .block-container {{ padding-left: 0.5rem !important; padding-right: 0.5rem !important; }}
        .glass-card {{ padding: 14px !important; border-radius: 12px !important; }}
    }}
    @media screen and (max-width: 480px) {{
        .main .block-container {{ padding-left: 0.25rem !important; padding-right: 0.25rem !important; }}
        .im-nav-tab {{ font-size: 10px !important; padding: 5px 6px !important; }}
        .band-ring {{ width: 48px; height: 48px; font-size: 16px; }}
        .challenge-day {{ width: 32px; height: 32px; font-size: 10px; border-radius: 6px; }}
    }}
    </style>

    <canvas id="ielts-bg" style="position:fixed;inset:0;z-index:0;pointer-events:none;width:100%;height:100%;"></canvas>
    <script>
    (function(){{
        if(window.__ielts_bg_init)return;
        window.__ielts_bg_init=true;
        const canvas=document.getElementById('ielts-bg');
        if(!canvas)return;
        const ctx=canvas.getContext('2d');
        let W=canvas.width=window.innerWidth,H=canvas.height=window.innerHeight;
        window.addEventListener('resize',()=>{{W=canvas.width=window.innerWidth;H=canvas.height=window.innerHeight;init()}});
        class P{{
            constructor(){{this.reset()}}
            reset(){{this.x=Math.random()*W;this.y=Math.random()*H;this.s=Math.random()*1+0.2;this.o=Math.random()*0.4+0.05;this.t=Math.random()*Math.PI*2;this.sp=Math.random()*0.004+0.001;this.vx=(Math.random()-0.5)*0.08;this.vy=(Math.random()-0.5)*0.08}}
            update(){{this.t+=this.sp;this.o=0.05+Math.abs(Math.sin(this.t))*0.35;this.x+=this.vx;this.y+=this.vy;if(this.x<0||this.x>W||this.y<0||this.y>H)this.reset()}}
        }}
        let pts=[];
        function init(){{pts=[];for(let i=0;i<160;i++)pts.push(new P())}}
        function draw(){{
            ctx.clearRect(0,0,W,H);
            pts.forEach(p=>{{p.update();ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fillStyle=`rgba(168,210,255,${{p.o}})`;ctx.fill()}});
            for(let i=0;i<pts.length;i++){{
                for(let j=i+1;j<pts.length;j++){{
                    const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.sqrt(dx*dx+dy*dy);
                    if(d<90){{ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[j].x,pts[j].y);ctx.strokeStyle=`rgba(74,158,255,${{0.05*(1-d/90)}})`;ctx.lineWidth=0.5;ctx.stroke()}}
                }}
            }}
            requestAnimationFrame(draw)
        }}
        init();draw();
    }})();
    </script>
    """, unsafe_allow_html=True)
