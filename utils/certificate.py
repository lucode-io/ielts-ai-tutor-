# ============================================================
# utils/certificate.py
# Visual HTML certificate with verified hash
# ============================================================

import hashlib
import secrets
import string
from datetime import date


def generate_cert_hash(user_id: str, full_name: str,
                        achieved_band: float, cert_type: str) -> str:
    """Generate a unique, verifiable certificate hash."""
    salt = secrets.token_hex(4).upper()
    raw = f"{user_id}{full_name}{achieved_band}{cert_type}{salt}"
    digest = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    prefix = "IELTS-MASTER"
    year = date.today().year
    return f"{prefix}-{year}-{digest}-{salt}"


def generate_certificate_html(full_name: str, target_band: float,
                               achieved_band: float = None,
                               cert_type: str = "gold",
                               completed_date: str = None,
                               cert_hash: str = None,
                               scores: dict = None) -> str:
    if not completed_date:
        completed_date = date.today().strftime("%B %d, %Y")
    if not cert_hash:
        cert_hash = f"IELTS-MASTER-{date.today().year}-DEMO0000-ABCD"
    if not scores:
        scores = {}

    verify_url = f"https://ielts-ai-tutor.streamlit.app/?verify={cert_hash}"
    is_gold = cert_type == "gold"

    primary = "#F0C040" if is_gold else "#C0C0C0"
    bg = "linear-gradient(145deg, #0d1b2a, #1b1b3a, #0d1b2a)" if is_gold else "linear-gradient(145deg, #0d1b2a, #1a1a2e, #0d1b2a)"
    trophy = "🏆" if is_gold else "🥈"
    cert_title = "Achievement Certificate" if is_gold else "Completion Certificate"
    cert_subtitle = "Gold — Band Target Achieved" if is_gold else "Silver — 21-Day Challenge Completed"
    badge_text = "GOLD<br>CERTIFIED" if is_gold else "SILVER<br>CERTIFIED"

    if is_gold:
        desc = f"For achieving <strong style='color:{primary}'>Band {achieved_band}</strong> in the Final Mock Test, surpassing the target of Band {target_band} after completing the 21-Day IELTS Speedrun Challenge."
    else:
        desc = f"For successfully completing the 21-Day IELTS Speedrun Challenge with dedication. Target: Band {target_band}. Keep training to achieve your goal!"

    speaking = scores.get("speaking", "-")
    writing = scores.get("writing", "-")
    reading = scores.get("reading", "-")
    listening = scores.get("listening", "-")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IELTS Master Certificate — {full_name}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:#0a0a1a;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:24px;font-family:'Inter',sans-serif}}
  .cert-wrap{{width:900px;max-width:100%}}
  .cert{{background:{bg};border:2px solid {primary};border-radius:8px;padding:52px;position:relative;overflow:hidden}}
  .cert::before{{content:'';position:absolute;inset:10px;border:1px solid {primary}44;border-radius:4px;pointer-events:none}}
  .corner{{position:absolute;width:56px;height:56px}}
  .tl{{top:16px;left:16px}}.tr{{top:16px;right:16px;transform:scaleX(-1)}}
  .bl{{bottom:16px;left:16px;transform:scaleY(-1)}}.br{{bottom:16px;right:16px;transform:scale(-1)}}
  .divider{{display:flex;align-items:center;gap:14px;margin:18px 0}}
  .dl{{flex:1;height:1px;background:linear-gradient(90deg,transparent,{primary}66,transparent)}}
  .dd{{width:6px;height:6px;background:{primary};transform:rotate(45deg);flex-shrink:0}}
  .header{{text-align:center;margin-bottom:18px}}
  .logo{{width:70px;height:70px;border-radius:50%;border:2px solid {primary};background:{primary}11;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;font-size:30px}}
  .brand{{font-family:'Cinzel',serif;font-size:12px;font-weight:600;color:{primary};letter-spacing:0.3em;text-transform:uppercase;margin-bottom:3px}}
  .brand-sub{{font-size:10px;color:rgba(255,255,255,0.3);letter-spacing:0.2em;text-transform:uppercase}}
  .cert-type{{display:inline-block;background:{primary}22;border:1px solid {primary}55;border-radius:20px;padding:4px 16px;font-size:10px;font-weight:600;color:{primary};letter-spacing:0.12em;text-transform:uppercase;margin-top:8px}}
  .title-block{{text-align:center}}
  .title-label{{font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:0.4em;text-transform:uppercase;margin-bottom:8px}}
  .title-main{{font-family:'Cinzel',serif;font-size:28px;font-weight:700;color:{primary};margin-bottom:4px}}
  .title-sub{{font-size:11px;color:rgba(255,255,255,0.3);letter-spacing:0.15em;text-transform:uppercase}}
  .recipient{{text-align:center;margin:22px 0}}
  .presented{{font-size:12px;color:rgba(255,255,255,0.4);letter-spacing:0.1em;margin-bottom:10px}}
  .name{{font-family:'Cinzel',serif;font-size:36px;font-weight:600;color:#fff;margin-bottom:12px;line-height:1.2}}
  .desc{{font-size:13px;color:rgba(255,255,255,0.55);line-height:1.75;max-width:560px;margin:0 auto}}
  .badges{{display:flex;justify-content:center;gap:24px;margin:20px 0;flex-wrap:wrap}}
  .badge{{text-align:center}}
  .badge-ring{{width:62px;height:62px;border-radius:50%;border:2px solid {primary}55;background:{primary}0d;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;font-size:11px;font-weight:700;color:{primary}}}
  .badge-label{{font-size:9px;color:rgba(255,255,255,0.35);letter-spacing:0.08em;text-transform:uppercase}}
  .badge-val{{font-size:12px;color:rgba(255,255,255,0.6);margin-top:2px}}
  .scores-row{{display:flex;justify-content:center;gap:12px;margin:16px 0;flex-wrap:wrap}}
  .score-box{{background:{primary}0d;border:1px solid {primary}33;border-radius:10px;padding:8px 16px;text-align:center;min-width:80px}}
  .score-skill{{font-size:9px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px}}
  .score-val{{font-size:20px;font-weight:800;color:{primary}}}
  .footer{{display:flex;justify-content:space-between;align-items:flex-end;margin-top:20px;flex-wrap:wrap;gap:12px}}
  .sig{{text-align:center}}
  .sig-line{{width:140px;height:1px;background:rgba(255,255,255,0.25);margin:0 auto 6px}}
  .sig-name{{font-size:11px;color:rgba(255,255,255,0.55)}}
  .sig-title{{font-size:9px;color:rgba(255,255,255,0.3);letter-spacing:0.1em;text-transform:uppercase;margin-top:2px}}
  .seal{{text-align:center}}
  .seal-ring{{width:70px;height:70px;border-radius:50%;border:2px solid {primary}55;background:{primary}08;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:0 auto}}
  .seal-text{{font-size:7px;color:{primary};letter-spacing:0.08em;text-transform:uppercase;text-align:center;line-height:1.5;font-weight:600}}
  .verify-section{{margin-top:16px;padding-top:14px;border-top:1px solid {primary}22;text-align:center}}
  .verify-hash{{font-family:'Courier New',monospace;font-size:12px;color:{primary};background:{primary}11;border:1px solid {primary}33;border-radius:6px;padding:6px 14px;display:inline-block;letter-spacing:0.08em;margin-bottom:6px}}
  .verify-label{{font-size:10px;color:rgba(255,255,255,0.25);letter-spacing:0.06em}}
  .verify-url{{font-size:10px;color:rgba(255,255,255,0.3);margin-top:4px}}
  .disclaimer{{font-size:9px;color:rgba(255,255,255,0.2);text-align:center;margin-top:10px;font-style:italic}}
  .print-btn{{display:block;margin:20px auto 0;padding:12px 32px;background:{primary};color:#0a0a1a;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;letter-spacing:0.05em;font-family:'Inter',sans-serif}}
  @media print{{body{{background:white}}.print-btn{{display:none}}}}
</style>
</head>
<body>
<div class="cert-wrap">
  <div class="cert">
    <div class="corner tl"><svg width="56" height="56" viewBox="0 0 56 56" fill="none"><path d="M4 52 L4 4 L52 4" stroke="{primary}" stroke-width="1.5" fill="none" opacity="0.7"/><circle cx="4" cy="4" r="3" fill="{primary}" opacity="0.7"/></svg></div>
    <div class="corner tr"><svg width="56" height="56" viewBox="0 0 56 56" fill="none"><path d="M4 52 L4 4 L52 4" stroke="{primary}" stroke-width="1.5" fill="none" opacity="0.7"/><circle cx="4" cy="4" r="3" fill="{primary}" opacity="0.7"/></svg></div>
    <div class="corner bl"><svg width="56" height="56" viewBox="0 0 56 56" fill="none"><path d="M4 52 L4 4 L52 4" stroke="{primary}" stroke-width="1.5" fill="none" opacity="0.7"/><circle cx="4" cy="4" r="3" fill="{primary}" opacity="0.7"/></svg></div>
    <div class="corner br"><svg width="56" height="56" viewBox="0 0 56 56" fill="none"><path d="M4 52 L4 4 L52 4" stroke="{primary}" stroke-width="1.5" fill="none" opacity="0.7"/><circle cx="4" cy="4" r="3" fill="{primary}" opacity="0.7"/></svg></div>

    <div class="header">
      <div class="logo">{trophy}</div>
      <div class="brand">IELTS Master</div>
      <div class="brand-sub">Powered by Claude AI</div>
      <div class="cert-type">{cert_subtitle}</div>
    </div>

    <div class="divider"><div class="dl"></div><div class="dd"></div><div class="dl"></div></div>

    <div class="title-block">
      <div class="title-label">Certificate of</div>
      <div class="title-main">{cert_title}</div>
      <div class="title-sub">21-Day IELTS Speedrun Challenge</div>
    </div>

    <div class="divider"><div class="dl"></div><div class="dd"></div><div class="dl"></div></div>

    <div class="recipient">
      <div class="presented">This certificate is proudly presented to</div>
      <div class="name">{full_name}</div>
      <div class="desc">{desc}</div>
    </div>

    <div class="scores-row">
      <div class="score-box"><div class="score-skill">Speaking</div><div class="score-val">{speaking}</div></div>
      <div class="score-box"><div class="score-skill">Writing</div><div class="score-val">{writing}</div></div>
      <div class="score-box"><div class="score-skill">Reading</div><div class="score-val">{reading}</div></div>
      <div class="score-box"><div class="score-skill">Listening</div><div class="score-val">{listening}</div></div>
      <div class="score-box" style="background:{primary}22;border-color:{primary}66"><div class="score-skill">Overall</div><div class="score-val" style="font-size:24px">{achieved_band if achieved_band else "-"}</div></div>
    </div>

    <div class="badges">
      <div class="badge"><div class="badge-ring" style="font-size:20px;font-weight:900">21</div><div class="badge-label">Days</div><div class="badge-val">Completed</div></div>
      <div class="badge"><div class="badge-ring">🎯</div><div class="badge-label">Target</div><div class="badge-val">Band {target_band}+</div></div>
      <div class="badge"><div class="badge-ring" style="font-size:16px;font-weight:800">{achieved_band if achieved_band else "?"}</div><div class="badge-label">Achieved</div><div class="badge-val">Final Score</div></div>
      <div class="badge"><div class="badge-ring">⭐</div><div class="badge-label">Skills</div><div class="badge-val">All 4 Tested</div></div>
    </div>

    <div class="divider"><div class="dl"></div><div class="dd"></div><div class="dl"></div></div>

    <div class="footer">
      <div class="sig"><div class="sig-line"></div><div class="sig-name">IELTS Master AI</div><div class="sig-title">Examiner & Platform</div></div>
      <div class="seal"><div class="seal-ring"><div class="seal-text">{badge_text}</div></div></div>
      <div class="sig"><div class="sig-line"></div><div class="sig-name">{completed_date}</div><div class="sig-title">Date of Completion</div></div>
    </div>

    <div class="verify-section">
      <div class="verify-hash">{cert_hash}</div><br>
      <div class="verify-label">Certificate Verification Code</div>
      <div class="verify-url">Verify at: {verify_url}</div>
    </div>

    <div class="disclaimer">
      This is an AI-based practice assessment certificate. It is not an official IELTS certificate.
      For official IELTS certification, please register at ielts.org.
    </div>
  </div>
  <button class="print-btn" onclick="window.print()">Save / Print Certificate</button>
</div>
</body>
</html>"""
    return html
