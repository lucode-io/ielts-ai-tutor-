# ============================================================
# utils/certificate.py
# Visual HTML certificate - Gold and Silver versions
# ============================================================

from datetime import date


def generate_certificate_html(full_name: str, target_band: float,
                               achieved_band: float = None,
                               cert_type: str = "gold",
                               completed_date: str = None) -> str:
    if not completed_date:
        completed_date = date.today().strftime("%B %d, %Y")

    is_gold = cert_type == "gold"

    if is_gold:
        primary = "#F0C040"
        secondary = "#E8A020"
        bg_gradient = "linear-gradient(145deg, #0d1b2a, #1b1b3a, #0d1b2a)"
        cert_title = "Achievement Certificate"
        cert_subtitle = "Gold — Band Target Achieved"
        trophy = "🏆"
        badge_text = "GOLD<br>CERTIFIED"
        achievement_score = f"Band {achieved_band}" if achieved_band else f"Band {target_band}+"
        desc = f"For achieving <strong style='color:{primary}'>Band {achieved_band}</strong> in the Final Mock Test, surpassing the target of Band {target_band} after completing the 21-Day IELTS Speedrun Challenge."
    else:
        primary = "#C0C0C0"
        secondary = "#A0A0A0"
        bg_gradient = "linear-gradient(145deg, #0d1b2a, #1a1a2e, #0d1b2a)"
        cert_title = "Completion Certificate"
        cert_subtitle = "Silver — 21-Day Challenge Completed"
        trophy = "🥈"
        badge_text = "SILVER<br>CERTIFIED"
        achievement_score = f"Band {achieved_band}" if achieved_band else "Completed"
        desc = f"For successfully completing the 21-Day IELTS Speedrun Challenge with dedication and commitment. Target: Band {target_band}. Keep training to achieve your goal!"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IELTS Master Certificate — {full_name}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#0a0a1a; display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; padding:24px; font-family:'Inter',sans-serif; }}
  .cert-wrap {{ width:860px; max-width:100%; }}
  .cert {{ background:{bg_gradient}; border:2px solid {primary}; border-radius:8px; padding:56px; position:relative; overflow:hidden; }}
  .cert::before {{ content:''; position:absolute; inset:10px; border:1px solid {primary}44; border-radius:4px; pointer-events:none; }}
  .corner {{ position:absolute; width:52px; height:52px; }}
  .corner svg {{ width:100%; height:100%; }}
  .tl {{ top:16px; left:16px; }}
  .tr {{ top:16px; right:16px; transform:scaleX(-1); }}
  .bl {{ bottom:16px; left:16px; transform:scaleY(-1); }}
  .br {{ bottom:16px; right:16px; transform:scale(-1); }}
  .divider {{ display:flex; align-items:center; gap:14px; margin:20px 0; }}
  .divider-line {{ flex:1; height:1px; background:linear-gradient(90deg,transparent,{primary}66,transparent); }}
  .divider-dot {{ width:6px; height:6px; background:{primary}; transform:rotate(45deg); flex-shrink:0; }}
  .header {{ text-align:center; margin-bottom:20px; }}
  .logo {{ width:72px; height:72px; border-radius:50%; border:2px solid {primary}; background:{primary}11; display:flex; align-items:center; justify-content:center; margin:0 auto 14px; font-size:32px; }}
  .brand {{ font-family:'Cinzel',serif; font-size:12px; font-weight:600; color:{primary}; letter-spacing:0.3em; text-transform:uppercase; margin-bottom:3px; }}
  .brand-sub {{ font-size:10px; color:rgba(255,255,255,0.3); letter-spacing:0.2em; text-transform:uppercase; }}
  .cert-type {{ display:inline-block; background:{primary}22; border:1px solid {primary}55; border-radius:20px; padding:4px 16px; font-size:10px; font-weight:600; color:{primary}; letter-spacing:0.15em; text-transform:uppercase; margin-top:8px; }}
  .title-block {{ text-align:center; }}
  .title-label {{ font-size:10px; color:rgba(255,255,255,0.4); letter-spacing:0.4em; text-transform:uppercase; margin-bottom:8px; }}
  .title-main {{ font-family:'Cinzel',serif; font-size:30px; font-weight:700; color:{primary}; margin-bottom:4px; }}
  .title-sub {{ font-size:11px; color:rgba(255,255,255,0.3); letter-spacing:0.15em; text-transform:uppercase; }}
  .recipient {{ text-align:center; margin:24px 0; }}
  .presented {{ font-size:12px; color:rgba(255,255,255,0.4); letter-spacing:0.1em; margin-bottom:10px; }}
  .name {{ font-family:'Cinzel',serif; font-size:38px; font-weight:600; color:#fff; margin-bottom:12px; }}
  .desc {{ font-size:13px; color:rgba(255,255,255,0.55); line-height:1.75; max-width:540px; margin:0 auto; }}
  .badges {{ display:flex; justify-content:center; gap:28px; margin:24px 0; flex-wrap:wrap; }}
  .badge {{ text-align:center; }}
  .badge-ring {{ width:64px; height:64px; border-radius:50%; border:2px solid {primary}55; background:{primary}0d; display:flex; align-items:center; justify-content:center; margin:0 auto 6px; font-size:11px; font-weight:700; color:{primary}; }}
  .badge-label {{ font-size:9px; color:rgba(255,255,255,0.35); letter-spacing:0.08em; text-transform:uppercase; }}
  .badge-val {{ font-size:12px; color:rgba(255,255,255,0.6); margin-top:2px; }}
  .footer {{ display:flex; justify-content:space-between; align-items:flex-end; margin-top:24px; flex-wrap:wrap; gap:14px; }}
  .sig {{ text-align:center; }}
  .sig-line {{ width:140px; height:1px; background:rgba(255,255,255,0.25); margin:0 auto 6px; }}
  .sig-name {{ font-size:11px; color:rgba(255,255,255,0.55); }}
  .sig-title {{ font-size:9px; color:rgba(255,255,255,0.3); letter-spacing:0.1em; text-transform:uppercase; margin-top:2px; }}
  .seal {{ text-align:center; }}
  .seal-ring {{ width:72px; height:72px; border-radius:50%; border:2px solid {primary}55; background:{primary}08; display:flex; flex-direction:column; align-items:center; justify-content:center; margin:0 auto; }}
  .seal-text {{ font-size:7px; color:{primary}; letter-spacing:0.08em; text-transform:uppercase; text-align:center; line-height:1.5; font-weight:600; }}
  .url {{ text-align:center; margin-top:14px; font-size:9px; color:rgba(255,255,255,0.2); }}
  .print-btn {{ display:block; margin:20px auto 0; padding:12px 32px; background:{primary}; color:#0a0a1a; border:none; border-radius:8px; font-size:14px; font-weight:700; cursor:pointer; letter-spacing:0.05em; font-family:'Inter',sans-serif; }}
  @media print {{ body {{ background:white; }} .print-btn {{ display:none; }} }}
</style>
</head>
<body>
<div class="cert-wrap">
  <div class="cert">
    <div class="corner tl"><svg viewBox="0 0 52 52" fill="none"><path d="M4 48 L4 4 L48 4" stroke="{primary}" stroke-width="1.5" fill="none" opacity="0.7"/><circle cx="4" cy="4" r="2.5" fill="{primary}" opacity="0.7"/></svg></div>
    <div class="corner tr"><svg viewBox="0 0 52 52" fill="none"><path d="M4 48 L4 4 L48 4" stroke="{primary}" stroke-width="1.5" fill="none" opacity="0.7"/><circle cx="4" cy="4" r="2.5" fill="{primary}" opacity="0.7"/></svg></div>
    <div class="corner bl"><svg viewBox="0 0 52 52" fill="none"><path d="M4 48 L4 4 L48 4" stroke="{primary}" stroke-width="1.5" fill="none" opacity="0.7"/><circle cx="4" cy="4" r="2.5" fill="{primary}" opacity="0.7"/></svg></div>
    <div class="corner br"><svg viewBox="0 0 52 52" fill="none"><path d="M4 48 L4 4 L48 4" stroke="{primary}" stroke-width="1.5" fill="none" opacity="0.7"/><circle cx="4" cy="4" r="2.5" fill="{primary}" opacity="0.7"/></svg></div>

    <div class="header">
      <div class="logo">{trophy}</div>
      <div class="brand">IELTS Master</div>
      <div class="brand-sub">Powered by Claude AI</div>
      <div class="cert-type">{cert_subtitle}</div>
    </div>

    <div class="divider"><div class="divider-line"></div><div class="divider-dot"></div><div class="divider-line"></div></div>

    <div class="title-block">
      <div class="title-label">Certificate of</div>
      <div class="title-main">{cert_title}</div>
      <div class="title-sub">21-Day IELTS Speedrun Challenge</div>
    </div>

    <div class="divider"><div class="divider-line"></div><div class="divider-dot"></div><div class="divider-line"></div></div>

    <div class="recipient">
      <div class="presented">This certificate is proudly presented to</div>
      <div class="name">{full_name}</div>
      <div class="desc">{desc}</div>
    </div>

    <div class="badges">
      <div class="badge">
        <div class="badge-ring" style="font-size:22px;font-weight:900">21</div>
        <div class="badge-label">Days</div>
        <div class="badge-val">Completed</div>
      </div>
      <div class="badge">
        <div class="badge-ring">🎯</div>
        <div class="badge-label">Target</div>
        <div class="badge-val">Band {target_band}+</div>
      </div>
      <div class="badge">
        <div class="badge-ring" style="font-size:18px;font-weight:900">{achievement_score}</div>
        <div class="badge-label">Achieved</div>
        <div class="badge-val">Final Score</div>
      </div>
      <div class="badge">
        <div class="badge-ring">⭐</div>
        <div class="badge-label">Skills</div>
        <div class="badge-val">All 4 Tested</div>
      </div>
    </div>

    <div class="divider"><div class="divider-line"></div><div class="divider-dot"></div><div class="divider-line"></div></div>

    <div class="footer">
      <div class="sig">
        <div class="sig-line"></div>
        <div class="sig-name">IELTS Master AI</div>
        <div class="sig-title">Examiner & Platform</div>
      </div>
      <div class="seal">
        <div class="seal-ring">
          <div class="seal-text">{badge_text}</div>
        </div>
      </div>
      <div class="sig">
        <div class="sig-line"></div>
        <div class="sig-name">{completed_date}</div>
        <div class="sig-title">Date of Completion</div>
      </div>
    </div>
    <div class="url">ielts-ai-tutor.streamlit.app</div>
  </div>
  <button class="print-btn" onclick="window.print()">Save / Print Certificate</button>
</div>
</body>
</html>"""
    return html
