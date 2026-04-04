# ============================================================
# utils/elevenlabs_audio.py
# ElevenLabs TTS integration for all listening sections
# ============================================================

import streamlit as st
import base64
import requests
from typing import Optional


def generate_audio(text: str, voice_id: str = None) -> Optional[str]:
    """
    Generate audio using ElevenLabs TTS.
    Returns base64-encoded MP3 string or None if failed.
    """
    try:
        api_key = st.secrets.get("ELEVENLABS_API_KEY", "")
        if not voice_id:
            voice_id = st.secrets.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

        if not api_key:
            return _fallback_tts(text)

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
        payload = {
            "text": text.strip(),
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.85,
                "style": 0.2,
                "use_speaker_boost": True
            }
        }
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode()
        else:
            st.warning(f"ElevenLabs error {response.status_code}. Using fallback audio.")
            return _fallback_tts(text)
    except Exception as e:
        return _fallback_tts(text)


def _fallback_tts(text: str) -> Optional[str]:
    """Fallback to gTTS if ElevenLabs fails."""
    try:
        from gtts import gTTS
        import io
        tts = gTTS(text=text.strip(), lang='en', slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode()
    except Exception:
        return None


def render_audio_player(
    audio_b64: str,
    title: str = "Listen carefully",
    subtitle: str = "You will hear this only once",
    color: str = "#FCD34D",
    autoplay: bool = False
):
    """Render a styled audio player with title."""
    if not audio_b64:
        return

    autoplay_attr = "autoplay" if autoplay else ""

    st.markdown(f"""
    <div style="background:rgba(252,211,77,0.06);border:1px solid rgba(252,211,77,0.25);
                border-radius:16px;padding:20px;margin-bottom:16px">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
            <div style="font-size:24px">🎧</div>
            <div>
                <div style="font-size:14px;font-weight:700;color:{color}">{title}</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.4)">{subtitle}</div>
            </div>
        </div>
        <audio controls {autoplay_attr}
               style="width:100%;border-radius:10px;accent-color:{color}">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            Your browser does not support audio.
        </audio>
        <div style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:8px;text-align:center">
            Press play — listen once, then answer the questions below
        </div>
    </div>
    """, unsafe_allow_html=True)


def get_cached_audio(cache_key: str, text: str) -> Optional[str]:
    """
    Get audio from session cache or generate new.
    Caches in session_state to avoid regenerating on every rerun.
    """
    cache_store = st.session_state.get("audio_cache", {})
    if cache_key in cache_store:
        return cache_store[cache_key]

    audio = generate_audio(text)
    if audio:
        cache_store[cache_key] = audio
        st.session_state.audio_cache = cache_store
    return audio
