# ============================================================
# verify.py
# Standalone public certificate verification page
# ============================================================

import streamlit as st
from utils.database import verify_certificate
from utils.styles import inject_global_css
from datetime import datetime

st.set_page_config(
    page_title="Verify Certificate — IELTS Master",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

inject_global_css("#F0C040")

# Check for hash in URL params
params = st.query_params
url_hash = params.get("verify", "")

st.markdown("""
<div style="text-align:center;padding:40px 0 24px">
    <div style="font-size:48px;margin-bottom:12px">🏆</div>
    <div style="font-size:24px;font-weight:800;color:#F0C040;margin-bottom:6px">
        Certificate Verification
    </div>
    <div style="font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:32px">
        Enter a certificate code to verify its authenticity
    </div>
</div>
""", unsafe_allow_html=True)

col = st.columns([1, 3, 1])[1]

with col:
    cert_hash = st.text_input(
        "Certificate Code",
        value=url_hash,
        placeholder="IELTS-MASTER-2026-XXXXXXXX-XXXX",
        label_visibility="collapsed"
    )

    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    verify_clicked = st.button("Verify Certificate", use_container_width=True, key="verify_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    if verify_clicked or url_hash:
        hash_to_check = cert_hash.strip() if verify_clicked else url_hash.strip()

        if not hash_to_check:
            st.warning("Please enter a certificate code.")
        else:
            with st.spinner("Checking certificate..."):
                result = verify_certificate(hash_to_check)

            if result["found"]:
                data = result["data"]
                cert_type = data.get("cert_type", "silver")
                is_gold = cert_type == "gold"
                primary = "#F0C040" if is_gold else "#C0C0C0"
                trophy = "🏆" if is_gold else "🥈"
                issued = data.get("issued_at", "")[:10] if data.get("issued_at") else "Unknown"
                verified_count = data.get("verified_count", 0)

                st.markdown(f"""
                <div style="background:{'rgba(240,192,64,0.08)' if is_gold else 'rgba(255,255,255,0.04)'};
                            border:2px solid {primary};border-radius:20px;padding:28px;
                            text-align:center;margin:20px 0">
                    <div style="font-size:44px;margin-bottom:12px">{trophy}</div>
                    <div style="font-size:20px;font-weight:800;color:{primary};margin-bottom:6px">
                        Certificate Verified
                    </div>
                    <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:20px">
                        This certificate is authentic and was issued by IELTS Master
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:360px;margin:0 auto;text-align:left">
                        <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px">
                            <div style="font-size:10px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">Student Name</div>
                            <div style="font-size:14px;font-weight:600;color:#fff">{data.get('full_name','—')}</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px">
                            <div style="font-size:10px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">Certificate Type</div>
                            <div style="font-size:14px;font-weight:600;color:{primary}">{'Gold Achievement' if is_gold else 'Silver Completion'}</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px">
                            <div style="font-size:10px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">Overall Band</div>
                            <div style="font-size:24px;font-weight:800;color:{primary}">{data.get('achieved_band','—')}</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px">
                            <div style="font-size:10px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">Target Band</div>
                            <div style="font-size:24px;font-weight:800;color:rgba(255,255,255,0.6)">{data.get('target_band','—')}</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px">
                            <div style="font-size:10px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">Issue Date</div>
                            <div style="font-size:13px;font-weight:600;color:#fff">{issued}</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px">
                            <div style="font-size:10px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">Times Verified</div>
                            <div style="font-size:13px;font-weight:600;color:#fff">{verified_count}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Score breakdown if available
                sp = data.get("speaking_band")
                wr = data.get("writing_band")
                rd = data.get("reading_band")
                ls = data.get("listening_band")

                if any([sp, wr, rd, ls]):
                    st.markdown(f"""
                    <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:12px">
                        <div style="background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.3);border-radius:10px;padding:10px 16px;text-align:center">
                            <div style="font-size:10px;color:#A78BFA;text-transform:uppercase;margin-bottom:4px">Speaking</div>
                            <div style="font-size:20px;font-weight:800;color:#A78BFA">{sp or '—'}</div>
                        </div>
                        <div style="background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.3);border-radius:10px;padding:10px 16px;text-align:center">
                            <div style="font-size:10px;color:#38BDF8;text-transform:uppercase;margin-bottom:4px">Writing</div>
                            <div style="font-size:20px;font-weight:800;color:#38BDF8">{wr or '—'}</div>
                        </div>
                        <div style="background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.3);border-radius:10px;padding:10px 16px;text-align:center">
                            <div style="font-size:10px;color:#34D399;text-transform:uppercase;margin-bottom:4px">Reading</div>
                            <div style="font-size:20px;font-weight:800;color:#34D399">{rd or '—'}</div>
                        </div>
                        <div style="background:rgba(252,211,77,0.1);border:1px solid rgba(252,211,77,0.3);border-radius:10px;padding:10px 16px;text-align:center">
                            <div style="font-size:10px;color:#FCD34D;text-transform:uppercase;margin-bottom:4px">Listening</div>
                            <div style="font-size:20px;font-weight:800;color:#FCD34D">{ls or '—'}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("""
                <div style="text-align:center;margin-top:20px;font-size:11px;color:rgba(255,255,255,0.2);font-style:italic">
                    This is an AI-based practice assessment certificate. Not an official IELTS certificate.
                    For official certification, visit ielts.org.
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown("""
                <div style="background:rgba(231,76,60,0.08);border:1px solid rgba(231,76,60,0.3);
                            border-radius:16px;padding:24px;text-align:center;margin:20px 0">
                    <div style="font-size:36px;margin-bottom:10px">❌</div>
                    <div style="font-size:18px;font-weight:700;color:#E74C3C;margin-bottom:6px">
                        Certificate Not Found
                    </div>
                    <div style="font-size:13px;color:rgba(255,255,255,0.4)">
                        This code does not match any certificate in our system.
                        Please check the code and try again.
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:40px">
    <div style="font-size:12px;color:rgba(255,255,255,0.2)">IELTS Master — ielts-ai-tutor.streamlit.app</div>
</div>
""", unsafe_allow_html=True)
