# ============================================================
# utils/database.py
# Supabase client and all DB operations
# ============================================================

import streamlit as st
from supabase import create_client, Client
from datetime import datetime, date, timedelta
from typing import Optional, Dict, List, Any
import json


@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)


# ── AUTH ──

def sign_up(email: str, password: str, full_name: str) -> Dict:
    supabase = get_supabase_client()
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"full_name": full_name}}
        })
        if res.user:
            try:
                supabase.table("users").insert({
                    "id": res.user.id,
                    "email": email,
                    "full_name": full_name
                }).execute()
            except Exception:
                pass  # Row may already exist
        return {"success": True, "user": res.user}
    except Exception as e:
        return {"success": False, "error": str(e)}


def sign_in(email: str, password: str) -> Dict:
    supabase = get_supabase_client()
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return {"success": True, "user": res.user, "session": res.session}
    except Exception as e:
        return {"success": False, "error": str(e)}


def sign_out():
    supabase = get_supabase_client()
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    # Clear the cache so next user gets a fresh client with no auth state
    try:
        get_supabase_client.clear()
    except Exception:
        pass


def get_current_user():
    supabase = get_supabase_client()
    try:
        return supabase.auth.get_user()
    except Exception:
        return None


# ── USER PROFILE ──

def get_user_profile(user_id: str) -> Optional[Dict]:
    supabase = get_supabase_client()
    try:
        res = supabase.table("users").select("*").eq("id", user_id).single().execute()
        return res.data
    except Exception:
        return None


def update_user_profile(user_id: str, updates: Dict) -> bool:
    supabase = get_supabase_client()
    try:
        updates["last_seen"] = datetime.utcnow().isoformat()
        supabase.table("users").update(updates).eq("id", user_id).execute()
        return True
    except Exception:
        return False


# ── SESSIONS ──

def create_session(user_id: str, mode: str, topic: str, target_band: float) -> Optional[str]:
    supabase = get_supabase_client()
    try:
        res = supabase.table("sessions").insert({
            "user_id": user_id,
            "mode": mode,
            "topic": topic,
            "target_band": target_band,
        }).execute()
        return res.data[0]["id"] if res.data else None
    except Exception:
        return None


def update_session(session_id: str, updates: Dict) -> bool:
    supabase = get_supabase_client()
    try:
        supabase.table("sessions").update(updates).eq("id", session_id).execute()
        return True
    except Exception:
        return False


def get_user_sessions(user_id: str, limit: int = 20) -> List[Dict]:
    supabase = get_supabase_client()
    try:
        res = supabase.table("sessions")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        return res.data or []
    except Exception:
        return []


def get_session_count(user_id: str) -> int:
    """Count total sessions for a user. Used by paywall gate."""
    supabase = get_supabase_client()
    try:
        res = supabase.table("sessions")\
            .select("id", count="exact")\
            .eq("user_id", user_id)\
            .execute()
        return res.count if res.count is not None else len(res.data or [])
    except Exception:
        return 0


def is_user_paid(user_id: str) -> bool:
    """Check if user has any paid subscription."""
    profile = get_user_profile(user_id)
    if not profile:
        return False
    return profile.get("subscription_status") in ("lifetime", "pro", "starter", "intensive", "paid")


def get_user_tier(user_id: str) -> str:
    """Return user's subscription tier."""
    profile = get_user_profile(user_id)
    if not profile:
        return "free"
    return profile.get("subscription_status", "free")


def get_daily_session_count(user_id: str) -> int:
    """Count sessions created today for this user."""
    supabase = get_supabase_client()
    try:
        today = date.today().isoformat()
        res = supabase.table("sessions")\
            .select("id", count="exact")\
            .eq("user_id", user_id)\
            .gte("created_at", today + "T00:00:00")\
            .execute()
        return res.count if res.count is not None else len(res.data or [])
    except Exception:
        return 0


def get_daily_tts_count(user_id: str) -> int:
    """Count TTS calls today. Stored in session_state, persisted per day."""
    key = f"tts_count_{date.today().isoformat()}"
    return st.session_state.get(key, 0)


def increment_tts_count(user_id: str):
    """Increment daily TTS counter."""
    key = f"tts_count_{date.today().isoformat()}"
    st.session_state[key] = st.session_state.get(key, 0) + 1


# ── BAND SCORES ──

def save_band_score(user_id: str, session_id: str, skill: str,
                    band_score: float, sub_scores: Dict = None) -> bool:
    supabase = get_supabase_client()
    try:
        data = {
            "user_id": user_id,
            "session_id": session_id,
            "skill": skill,
            "band_score": band_score,
        }
        if sub_scores:
            data.update(sub_scores)
        supabase.table("band_scores").insert(data).execute()
        return True
    except Exception:
        return False


def get_score_history(user_id: str, skill: str = None, days: int = 30) -> List[Dict]:
    supabase = get_supabase_client()
    try:
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        query = supabase.table("band_scores")\
            .select("*")\
            .eq("user_id", user_id)\
            .gte("recorded_at", since)\
            .order("recorded_at", desc=False)
        if skill:
            query = query.eq("skill", skill)
        res = query.execute()
        return res.data or []
    except Exception:
        return []


# ── MESSAGES ──

def save_message(session_id: str, user_id: str, role: str,
                 content: str, audio_url: str = None) -> bool:
    supabase = get_supabase_client()
    try:
        supabase.table("practice_messages").insert({
            "session_id": session_id,
            "user_id": user_id,
            "role": role,
            "content": content,
            "audio_url": audio_url
        }).execute()
        return True
    except Exception:
        return False


def get_session_messages(session_id: str) -> List[Dict]:
    supabase = get_supabase_client()
    try:
        res = supabase.table("practice_messages")\
            .select("*")\
            .eq("session_id", session_id)\
            .order("created_at", desc=False)\
            .execute()
        return res.data or []
    except Exception:
        return []


# ── RECURRING ERRORS ──

def upsert_recurring_error(user_id: str, error_type: str,
                            category: str, description: str, example: str = None) -> bool:
    supabase = get_supabase_client()
    try:
        existing = supabase.table("recurring_errors")\
            .select("id, frequency")\
            .eq("user_id", user_id)\
            .eq("error_type", error_type)\
            .execute()
        if existing.data:
            supabase.table("recurring_errors").update({
                "frequency": existing.data[0]["frequency"] + 1,
                "last_seen": datetime.utcnow().isoformat(),
            }).eq("id", existing.data[0]["id"]).execute()
        else:
            supabase.table("recurring_errors").insert({
                "user_id": user_id,
                "error_type": error_type,
                "error_category": category,
                "description": description,
                "example": example
            }).execute()
        return True
    except Exception:
        return False


def get_recurring_errors(user_id: str) -> List[Dict]:
    supabase = get_supabase_client()
    try:
        res = supabase.table("recurring_errors")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("frequency", desc=True)\
            .limit(10)\
            .execute()
        return res.data or []
    except Exception:
        return []


# ── CHALLENGE ──

def get_challenge_days(user_id: str) -> List[Dict]:
    supabase = get_supabase_client()
    try:
        res = supabase.table("challenge_days")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("day_number", desc=False)\
            .execute()
        return res.data or []
    except Exception:
        return []


def complete_challenge_day(user_id: str, day_number: int,
                            task_type: str, band_score: float = None) -> bool:
    supabase = get_supabase_client()
    try:
        supabase.table("challenge_days").upsert({
            "user_id": user_id,
            "day_number": day_number,
            "task_type": task_type,
            "band_score": band_score,
            "completed_at": datetime.utcnow().isoformat()
        }).execute()
        profile = get_user_profile(user_id)
        if profile:
            today = date.today()
            last_date = profile.get("streak_last_date")
            current_streak = profile.get("streak_count", 0)
            if last_date:
                last = date.fromisoformat(str(last_date))
                if (today - last).days == 1:
                    new_streak = current_streak + 1
                elif today == last:
                    new_streak = current_streak
                else:
                    new_streak = 1
            else:
                new_streak = 1
            update_user_profile(user_id, {
                "streak_count": new_streak,
                "streak_last_date": today.isoformat(),
                "challenge_day": day_number,
                "challenge_completed": day_number >= 21
            })
        return True
    except Exception:
        return False


# ── DIAGNOSTIC ──

def save_diagnostic(user_id: str, scores: Dict) -> bool:
    supabase = get_supabase_client()
    try:
        overall = round(
            (scores.get("speaking", 0) + scores.get("writing", 0) +
             scores.get("reading", 0) + scores.get("listening", 0)) / 4, 1
        )
        supabase.table("diagnostic_tests").insert({
            "user_id": user_id,
            "speaking_band": scores.get("speaking"),
            "writing_band": scores.get("writing"),
            "reading_band": scores.get("reading"),
            "listening_band": scores.get("listening"),
            "overall_band": overall,
            "raw_results": json.dumps(scores)
        }).execute()
        update_user_profile(user_id, {"baseline_band": overall})
        return True
    except Exception:
        return False


def get_latest_diagnostic(user_id: str) -> Optional[Dict]:
    supabase = get_supabase_client()
    try:
        res = supabase.table("diagnostic_tests")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("taken_at", desc=True)\
            .limit(1)\
            .execute()
        return res.data[0] if res.data else None
    except Exception:
        return None
# ============================================================
# ADD THESE FUNCTIONS TO utils/database.py
# Paste at the bottom of your existing database.py
# ============================================================

# ── CERTIFICATES ──

def save_certificate(user_id: str, cert_hash: str, full_name: str,
                     target_band: float, achieved_band: float,
                     cert_type: str, scores: dict) -> bool:
    """Save a certificate record to Supabase."""
    supabase = get_supabase_client()
    try:
        supabase.table("certificates").insert({
            "hash": cert_hash,
            "user_id": user_id,
            "full_name": full_name,
            "target_band": target_band,
            "achieved_band": achieved_band,
            "cert_type": cert_type,
            "speaking_band": scores.get("speaking"),
            "writing_band": scores.get("writing"),
            "reading_band": scores.get("reading"),
            "listening_band": scores.get("listening"),
        }).execute()
        return True
    except Exception:
        return False


def verify_certificate(cert_hash: str) -> dict:
    """Look up a certificate by hash. Public — no auth required."""
    supabase = get_supabase_client()
    try:
        res = supabase.table("certificates")\
            .select("*")\
            .eq("hash", cert_hash)\
            .eq("is_valid", True)\
            .single()\
            .execute()
        if res.data:
            # Increment verified count
            supabase.table("certificates")\
                .update({"verified_count": res.data["verified_count"] + 1})\
                .eq("hash", cert_hash)\
                .execute()
            return {"found": True, "data": res.data}
        return {"found": False}
    except Exception:
        return {"found": False}


def get_user_certificates(user_id: str) -> list:
    """Get all certificates for a user."""
    supabase = get_supabase_client()
    try:
        res = supabase.table("certificates")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("issued_at", desc=True)\
            .execute()
        return res.data or []
    except Exception:
        return []
