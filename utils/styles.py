# styles.py — matches ieltsmaster.org exactly
# Colors: #01010a bg | #4A9EFF blue | #1a5fd4 blue2 | #f0f4ff white
# Effects: particle canvas, scanlines, blue glows
import streamlit as st

def inject_global_css(accent: str = "#4A9EFF"):
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

    html,body,[data-testid="stAppViewContainer"],[data-testid="stApp"]{background:#01010a!important;font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#f0f4ff}
    [data-testid="stHeader"]{background:transparent!important;border:none!important}

    [data-testid="stApp"]::before{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(74,158,255,0.008) 3px,rgba(74,158,255,0.008) 4px);pointer-events:none;z-index:0}

    [data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],button[kind="headerNoPadding"],[data-testid="stSidebarNav"]{display:none!important;visibility:hidden!important;width:0!important;min-width:0!important;max-width:0!important;overflow:hidden!important}

    .main .block-container{background:transparent!important;padding-top:0.5rem;max-width:1280px;position:relative;z-index:2}

    .glass-card{background:rgba(74,158,255,0.04);border-radius:16px;border:1px solid rgba(74,158,255,0.12);padding:20px;position:relative;overflow:hidden;margin-bottom:16px;transition:border-color 0.3s}
    .glass-card:hover{border-color:rgba(74,158,255,0.22)}
    .glass-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(74,158,255,0.3),transparent)}

    .top-nav{background:rgba(1,1,10,0.92);border-radius:14px;border:1px solid rgba(74,158,255,0.12);padding:12px 24px;display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;backdrop-filter:blur(24px);position:relative;z-index:2}
    .top-nav-brand{display:flex;align-items:center;gap:10px}
    .top-nav-brand-text{font-family:'Syne',sans-serif;font-size:16px;font-weight:800;color:#f0f4ff;letter-spacing:0.05em}
    .top-nav-brand-text span{color:#4A9EFF}
    .top-nav-brand-sub{font-size:10px;color:rgba(180,210,255,0.38);letter-spacing:0.1em;text-transform:uppercase}

    .nav-tab-bar{display:flex;gap:4px;background:rgba(74,158,255,0.03);border-radius:12px;padding:4px;margin-bottom:20px;border:1px solid rgba(74,158,255,0.08);flex-wrap:wrap}
    .nav-tab{padding:8px 16px;border-radius:9px;font-size:12px;font-weight:600;color:rgba(180,210,255,0.45);cursor:pointer;transition:all 0.2s;border:none;background:transparent;letter-spacing:0.03em}
    .nav-tab.active{background:rgba(74,158,255,0.1);color:#4A9EFF;border:1px solid rgba(74,158,255,0.25)}

    .stButton>button{border-radius:9px!important;font-weight:600!important;font-size:13px!important;padding:10px 18px!important;transition:all 0.25s!important;width:100%!important;background:rgba(74,158,255,0.05)!important;color:#f0f4ff!important;border:1px solid rgba(74,158,255,0.15)!important;letter-spacing:0.02em!important}
    .stButton>button:hover{background:rgba(74,158,255,0.1)!important;color:#fff!important;border-color:rgba(74,158,255,0.35)!important;transform:translateY(-1px)!important;box-shadow:0 0 20px rgba(74,158,255,0.15)!important}
    .btn-primary>button{background:linear-gradient(135deg,#4A9EFF,#1a5fd4)!important;color:#fff!important;border:none!important;font-weight:700!important;box-shadow:0 0 30px rgba(74,158,255,0.25),inset 0 1px 0 rgba(255,255,255,0.1)!important}
    .btn-primary>button:hover{transform:translateY(-2px)!important;box-shadow:0 0 50px rgba(74,158,255,0.45),inset 0 1px 0 rgba(255,255,255,0.1)!important}
    button[kind="secondary"]{background:transparent!important;color:#ff3a4a!important;border:1px solid rgba(255,58,74,0.25)!important;border-radius:9px!important}

    [data-testid="stChatMessage"]{background:transparent!important;border:none!important;padding:4px 0!important}
    [data-testid="stChatMessage"][data-author="user"]>div:last-child{background:rgba(74,158,255,0.07)!important;border-radius:16px 16px 4px 16px!important;border:1px solid rgba(74,158,255,0.15)!important;padding:14px 18px!important;color:#f0f4ff!important;margin-left:auto!important;max-width:85%!important}
    [data-testid="stChatMessage"][data-author="assistant"]>div:last-child{background:rgba(74,158,255,0.03)!important;border-radius:16px 16px 16px 4px!important;border:1px solid rgba(74,158,255,0.1)!important;padding:20px 24px!important;max-width:95%!important}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span{font-size:15px!important;line-height:1.85!important;color:rgba(180,210,255,0.85)!important;letter-spacing:0.01em!important;user-select:text!important;-webkit-user-select:text!important}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong{color:#4A9EFF!important;font-weight:600!important}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3{color:#4A9EFF!important;font-weight:700!important;font-size:16px!important;margin:1rem 0 0.4rem!important}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li{margin-bottom:6px!important;color:rgba(180,210,255,0.75)!important}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] hr{border-color:rgba(74,158,255,0.2)!important;margin:12px 0!important}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code{background:rgba(74,158,255,0.1)!important;color:#4A9EFF!important;padding:2px 7px!important;border-radius:5px!important;font-size:13px!important}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"]{user-select:text!important;-webkit-user-select:text!important;cursor:text!important}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] *{user-select:text!important;-webkit-user-select:text!important}

    [data-testid="stChatInput"]{background:rgba(74,158,255,0.04)!important;border:1px solid rgba(74,158,255,0.18)!important;border-radius:12px!important;color:#f0f4ff!important}
    [data-testid="stChatInput"]:focus-within{border-color:rgba(74,158,255,0.5)!important;box-shadow:0 0 0 3px rgba(74,158,255,0.08),0 0 20px rgba(74,158,255,0.1)!important}

    [data-testid="stTextInput"] input,[data-baseweb="input"] input,.stTextInput input,input[type="text"],input[type="email"],input[type="password"],input[type="number"]{color:#0d1117!important;background:#f0f4ff!important;caret-color:#0d1117!important;border-radius:8px!important;border:1px solid rgba(74,158,255,0.2)!important}
    [data-testid="stTextArea"] textarea,[data-baseweb="textarea"] textarea{color:#0d1117!important;background:#f0f4ff!important;border-radius:8px!important;user-select:text!important;-webkit-user-select:text!important}
    [data-testid="stSelectbox"]>div>div{background:rgba(74,158,255,0.05)!important;border:1px solid rgba(74,158,255,0.15)!important;border-radius:9px!important;color:#f0f4ff!important}
    [data-testid="stSlider"]>div>div>div{background:#4A9EFF!important}

    [data-testid="stMetric"]{background:rgba(74,158,255,0.04)!important;border-radius:12px!important;padding:14px 18px!important;border:1px solid rgba(74,158,255,0.1)!important;position:relative;overflow:hidden}
    [data-testid="stMetricValue"]{background:linear-gradient(135deg,#fff,#4A9EFF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:800!important;font-family:'Syne',sans-serif!important}
    [data-testid="stMetricLabel"]{color:rgba(180,210,255,0.38)!important}

    [data-testid="stAlert"]{background:rgba(74,158,255,0.05)!important;border-left:3px solid #4A9EFF!important;border-radius:10px!important;color:rgba(180,210,255,0.85)!important}
    [data-testid="stStatus"],[data-testid="stStatusWidget"]{background:rgba(74,158,255,0.04)!important;border:1px solid rgba(74,158,255,0.2)!important;border-radius:10px!important;color:#f0f4ff!important}
    [data-testid="stExpander"]{background:rgba(74,158,255,0.03)!important;border:1px solid rgba(74,158,255,0.1)!important;border-radius:12px!important}

    [data-testid="stTabs"] [role="tab"]{color:rgba(180,210,255,0.45)!important;font-weight:600!important;letter-spacing:0.03em!important}
    [data-testid="stTabs"] [role="tab"][aria-selected="true"]{color:#4A9EFF!important;border-bottom-color:#4A9EFF!important}
    [data-testid="stTabs"] [role="tabpanel"]{background:transparent!important}

    .pill{display:inline-block;padding:3px 11px;border-radius:100px;font-size:11px;font-weight:600;margin-right:6px;letter-spacing:0.05em}
    .pill-blue{background:rgba(74,158,255,0.1);color:#4A9EFF;border:1px solid rgba(74,158,255,0.2)}
    .pill-green{background:rgba(0,232,122,0.08);color:#00e87a;border:1px solid rgba(0,232,122,0.2)}
    .pill-red{background:rgba(255,58,74,0.08);color:#ff3a4a;border:1px solid rgba(255,58,74,0.2)}
    .pill-gold{background:rgba(240,192,64,0.08);color:#F0C040;border:1px solid rgba(240,192,64,0.2)}
    .pill-purple{background:rgba(167,139,250,0.08);color:#A78BFA;border:1px solid rgba(167,139,250,0.2)}

    ::-webkit-scrollbar{width:4px}
    ::-webkit-scrollbar-track{background:transparent}
    ::-webkit-scrollbar-thumb{background:rgba(74,158,255,0.3);border-radius:4px}

    .progress-bar-wrap{background:rgba(74,158,255,0.08);border-radius:100px;height:6px;overflow:hidden;margin:6px 0}
    .progress-bar-fill{height:100%;border-radius:100px;background:linear-gradient(90deg,#4A9EFF,#1a5fd4);transition:width 0.4s ease;box-shadow:0 0 8px rgba(74,158,255,0.4)}

    .band-ring{display:inline-flex;align-items:center;justify-content:center;width:72px;height:72px;border-radius:50%;border:2px solid #4A9EFF;font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#4A9EFF;box-shadow:0 0 20px rgba(74,158,255,0.2)}

    .quote-box{background:rgba(74,158,255,0.04);border-left:2px solid #4A9EFF;border-radius:0 10px 10px 0;padding:14px 18px;margin:12px 0 20px;position:relative;overflow:hidden}
    .quote-box::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,#4A9EFF,transparent)}
    .quote-text{font-size:14px;font-style:italic;color:rgba(180,210,255,0.7);line-height:1.75;margin-bottom:6px}
    .quote-author{font-size:10px;color:#4A9EFF;font-weight:600;letter-spacing:0.1em;text-transform:uppercase}

    .challenge-day{width:44px;height:44px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;margin:0 auto 4px auto;border:1px solid rgba(74,158,255,0.08);background:rgba(74,158,255,0.03);color:rgba(180,210,255,0.25);cursor:default;transition:all 0.2s}
    .challenge-day.done{background:rgba(74,158,255,0.12);border-color:rgba(74,158,255,0.4);color:#4A9EFF;box-shadow:0 0 10px rgba(74,158,255,0.15)}
    .challenge-day.today{background:rgba(74,158,255,0.18);border-color:#4A9EFF;color:#fff;animation:pulse-blue 2s infinite;box-shadow:0 0 16px rgba(74,158,255,0.3)}
    .challenge-day.locked{opacity:0.2}
    .challenge-day.clickable{cursor:pointer;border-color:rgba(74,158,255,0.2);color:rgba(180,210,255,0.5)}
    .challenge-day.clickable:hover{background:rgba(74,158,255,0.1);border-color:rgba(74,158,255,0.45);color:#4A9EFF;box-shadow:0 0 10px rgba(74,158,255,0.2)}
    .challenge-label{font-size:9px;text-align:center;margin-top:2px;color:rgba(180,210,255,0.25);font-weight:500;letter-spacing:0.03em}
    .challenge-label.today-label{color:#4A9EFF;font-weight:700}

    @keyframes pulse-blue{0%,100%{box-shadow:0 0 12px rgba(74,158,255,0.3)}50%{box-shadow:0 0 24px rgba(74,158,255,0.6);border-color:rgba(74,158,255,0.9)}}

    .hero-title{font-family:'Syne',sans-serif;font-size:clamp(28px,5vw,52px);font-weight:800;line-height:1;letter-spacing:-0.03em;background:linear-gradient(135deg,#fff 0%,rgba(200,225,255,0.95) 40%,#4A9EFF 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
    .stat-num{font-family:'Syne',sans-serif;font-size:28px;font-weight:800;background:linear-gradient(135deg,#fff,#4A9EFF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1;margin-bottom:4px}
    .stat-label{font-size:10px;color:rgba(180,210,255,0.38);letter-spacing:0.1em;text-transform:uppercase;font-weight:500}

    @media screen and (max-width:768px){
        .main .block-container{padding-left:0.5rem!important;padding-right:0.5rem!important}
        [data-testid="stChatMessage"][data-author="assistant"]>div:last-child{max-width:100%!important;padding:14px 16px!important}
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li{font-size:14px!important;line-height:1.75!important}
        .glass-card{border-radius:12px!important;padding:14px!important}
        .top-nav{padding:10px 14px!important;border-radius:10px!important}
        .nav-tab{font-size:11px!important;padding:6px 10px!important}
        .band-ring{width:54px;height:54px;font-size:18px}
        .challenge-day{width:36px;height:36px;font-size:11px;border-radius:7px}
    }
    @media screen and (max-width:480px){.main .block-container{padding-left:0.25rem!important;padding-right:0.25rem!important}}
    </style>

    <canvas id="ielts-bg" style="position:fixed;inset:0;z-index:0;pointer-events:none;width:100%;height:100%;"></canvas>
    <script>
    (function(){
        const canvas=document.getElementById('ielts-bg');
        if(!canvas)return;
        const ctx=canvas.getContext('2d');
        let W=canvas.width=window.innerWidth,H=canvas.height=window.innerHeight;
        window.addEventListener('resize',()=>{W=canvas.width=window.innerWidth;H=canvas.height=window.innerHeight;init()});
        class P{
            constructor(){this.reset()}
            reset(){this.x=Math.random()*W;this.y=Math.random()*H;this.s=Math.random()*1+0.2;this.o=Math.random()*0.4+0.05;this.t=Math.random()*Math.PI*2;this.sp=Math.random()*0.004+0.001;this.vx=(Math.random()-0.5)*0.08;this.vy=(Math.random()-0.5)*0.08}
            update(){this.t+=this.sp;this.o=0.05+Math.abs(Math.sin(this.t))*0.35;this.x+=this.vx;this.y+=this.vy;if(this.x<0||this.x>W||this.y<0||this.y>H)this.reset()}
        }
        let pts=[];
        function init(){pts=[];for(let i=0;i<160;i++)pts.push(new P())}
        function draw(){
            ctx.clearRect(0,0,W,H);
            pts.forEach(p=>{p.update();ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fillStyle=`rgba(168,210,255,${p.o})`;ctx.fill()});
            for(let i=0;i<pts.length;i++){
                for(let j=i+1;j<pts.length;j++){
                    const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.sqrt(dx*dx+dy*dy);
                    if(d<90){ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[j].x,pts[j].y);ctx.strokeStyle=`rgba(74,158,255,${0.05*(1-d/90)})`;ctx.lineWidth=0.5;ctx.stroke()}
                }
            }
            requestAnimationFrame(draw)
        }
        init();draw();
    })();
    </script>
    """, unsafe_allow_html=True)
