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
    """Initialize and cache Supabase client."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)


# ── AUTH ──

def sign_up(email: str, password: str, full_name: str) -> Dict:
    """Register a new user."""
    supabase = get_supabase_client()
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"full_name": full_name}}
        })
        if res.user:
            # Create user profile row
            supabase.table("users").insert({
                "id": res.user.id,
                "email": email,
                "full_name": full_name
            }).execute()
        return {"success": True, "user": res.user}
    except Exception as e:
        return {"success": False, "error": str(e)}


def sign_in(email: str, password: str) -> Dict:
    """Sign in existing user."""
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
    """Sign out current user."""
    supabase = get_supabase_client()
    try:
        supabase.auth.sign_out()
    except Exception:
        pass


def get_current_user():
    """Get current authenticated user."""
    supabase = get_supabase_client()
    try:
        return supabase.auth.get_user()
    except Exception:
        return None


# ── USER PROFILE ──

def get_user_profile(user_id: str) -> Optional[Dict]:
    """Fetch full user profile from DB."""
    supabase = get_supabase_client()
    try:
        res = supabase.table("users").select("*").eq("id", user_id).single().execute()
        return res.data
    except Exception:
        return None


def update_user_profile(user_id: str, updates: Dict) -> bool:
    """Update user profile fields."""
    supabase = get_supabase_client()
    try:
        updates["last_seen"] = datetime.utcnow().isoformat()
        supabase.table("users").update(updates).eq("id", user_id).execute()
        return True
    except Exception:
        return False


# ── SESSIONS ──

def create_session(user_id: str, mode: str, topic: str, target_band: float) -> Optional[str]:
    """Create a new practice session, return session_id."""
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
    """Update session with score and duration."""
    supabase = get_supabase_client()
    try:
        supabase.table("sessions").update(updates).eq("id", session_id).execute()
        return True
    except Exception:
        return False


def get_user_sessions(user_id: str, limit: int = 20) -> List[Dict]:
    """Get recent sessions for a user."""
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


# ── BAND SCORES ──

def save_band_score(user_id: str, session_id: str, skill: str,
                    band_score: float, sub_scores: Dict = None) -> bool:
    """Save a band score record."""
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
    """Get score history for charts."""
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
    """Save a chat message to the session."""
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
    """Get all messages for a session."""
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
    """Add or increment a recurring error."""
    supabase = get_supabase_client()
    try:
        # Check if this error type already exists
        existing = supabase.table("recurring_errors")\
            .select("id, frequency")\
            .eq("user_id", user_id)\
            .eq("error_type", error_type)\
            .execute()

        if existing.data:
            # Increment frequency
            supabase.table("recurring_errors").update({
                "frequency": existing.data[0]["frequency"] + 1,
                "last_seen": datetime.utcnow().isoformat(),
                "example": example or existing.data[0].get("example")
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
    """Get top recurring errors for a user."""
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
    """Get completed challenge days."""
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
    """Mark a challenge day as complete."""
    supabase = get_supabase_client()
    try:
        supabase.table("challenge_days").upsert({
            "user_id": user_id,
            "day_number": day_number,
            "task_type": task_type,
            "band_score": band_score,
            "completed_at": datetime.utcnow().isoformat()
        }).execute()

        # Update streak on user profile
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
                    new_streak = current_streak  # same day, no change
                else:
                    new_streak = 1  # streak broken
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
    """Save diagnostic test results."""
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
        # Update baseline on user profile
        update_user_profile(user_id, {"baseline_band": overall})
        return True
    except Exception:
        return False


def get_latest_diagnostic(user_id: str) -> Optional[Dict]:
    """Get the most recent diagnostic test."""
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
