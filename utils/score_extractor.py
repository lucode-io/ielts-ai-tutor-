# ============================================================
# utils/score_extractor.py
# Robust band score extraction — replaces fragile regex parsing
# Used by: onboarding.py, mock_test.py, practice.py
# ============================================================

import re
import json
import streamlit as st
from typing import Dict, Optional


def extract_band_score_from_text(text: str, skill: str = None, default: float = 5.5) -> float:
    """
    Extract a single band score from AI response text.
    Uses multi-pattern regex with validation. Returns rounded 0.5 IELTS score.
    
    Args:
        text: The AI response text containing band scores
        skill: Optional skill name to target (speaking/writing/reading/listening)
        default: Fallback score if extraction fails
    """
    score = _regex_extract(text, skill)
    if score is not None:
        return _round_ielts(score)
    return default


def extract_all_scores_from_text(text: str, default: float = 5.5) -> Dict[str, float]:
    """
    Extract all 4 skill scores from AI diagnostic response.
    Scans entire conversation history if needed.
    
    Returns: {"speaking": X.X, "writing": X.X, "reading": X.X, "listening": X.X}
    """
    scores = {}
    for skill in ["speaking", "writing", "reading", "listening"]:
        score = _regex_extract(text, skill)
        if score is not None:
            scores[skill] = _round_ielts(score)
    return scores


def extract_all_scores_from_messages(messages: list, default: float = 5.5) -> Dict[str, float]:
    """
    Scan ALL assistant messages for band scores.
    This catches scores spread across multiple turns (e.g. diagnostic chat).
    """
    scores = {}
    # Process messages in reverse — later scores override earlier ones
    for msg in reversed(messages):
        if msg.get("role") == "assistant":
            found = extract_all_scores_from_text(msg["content"], default)
            for skill, score in found.items():
                if skill not in scores:
                    scores[skill] = score
    
    # Fill missing with default
    for skill in ["speaking", "writing", "reading", "listening"]:
        if skill not in scores:
            scores[skill] = default
    
    return scores


def extract_score_via_llm(text: str, skill: str, default: float = 5.5) -> float:
    """
    Last-resort: make a tiny Claude call to extract the score.
    Only use when regex fails on critical paths (mock test scoring).
    Costs ~200 tokens.
    """
    try:
        from utils.ai import get_claude_client
        client = get_claude_client()
        response = client.messages.create(
            model="claude-sonnet-4-5-20241022",
            max_tokens=20,
            system="Extract the IELTS band score. Return ONLY a number like 6.5 — nothing else.",
            messages=[{
                "role": "user",
                "content": f"What {skill} band score is given in this text?\n\n{text[:1500]}"
            }]
        )
        result = response.content[0].text.strip()
        match = re.search(r'(\d\.?\d?)', result)
        if match:
            val = float(match.group(1))
            if 3.0 <= val <= 9.0:
                return _round_ielts(val)
    except Exception:
        pass
    return default


# ── INTERNAL ──────────────────────────────────────────────────

def _regex_extract(text: str, skill: str = None) -> Optional[float]:
    """
    Multi-pattern regex extractor. Tries patterns from most specific to least.
    Returns raw float or None.
    """
    if not text:
        return None
    
    # Normalize skill name for matching
    skill_pattern = skill.capitalize() if skill else r"(?:Speaking|Writing|Reading|Listening|Overall)"
    
    # Ordered from most specific to least specific
    patterns = [
        # "SPEAKING BAND: 6.5" (diagnostic format)
        rf"{skill_pattern}\s*BAND[:\s]+(\d+\.?\d*)",
        # "Speaking Band: 6.5"
        rf"{skill_pattern}\s+Band[:\s]+(\d+\.?\d*)",
        # "Overall Speaking Band: 6.5"
        rf"Overall\s+{skill_pattern}\s+Band[:\s]+(\d+\.?\d*)",
        # "Overall Band Estimate: 6.5"
        rf"Overall\s+Band\s+Estimate[:\s]+(\d+\.?\d*)",
        # "Overall Band: 6.5"
        rf"Overall\s+Band[:\s]+(\d+\.?\d*)",
        # "Speaking: 6.5" (simple format)
        rf"{skill_pattern}[:\s]+(\d+\.?\d*)",
        # "Speaking — 6.5" or "Speaking – 6.5"
        rf"{skill_pattern}\s*[—–-]\s*(\d+\.?\d*)",
        # "Band 6.5" (if skill is specified, search near skill mention)
        rf"{skill_pattern}[^.]*?Band\s+(\d+\.?\d*)",
        # Bare "X.X" after skill mention (within 50 chars)
        rf"{skill_pattern}.{{0,50}}?(\d\.\d)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                val = float(match.group(1))
                if 3.0 <= val <= 9.0:
                    return val
            except (ValueError, IndexError):
                continue
    
    # If no skill specified, try to find any standalone band score
    if skill is None or skill.lower() == "overall":
        # Look for "Overall" patterns specifically
        overall_patterns = [
            r"Overall[^:]*?[:\s]+(\d+\.?\d*)",
            r"\*\*Overall[^*]*?(\d+\.?\d*)\*\*",
            r"Overall Baseline[:\s]+(\d+\.?\d*)",
        ]
        for pattern in overall_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    val = float(match.group(1))
                    if 3.0 <= val <= 9.0:
                        return val
                except (ValueError, IndexError):
                    continue
    
    return None


def _round_ielts(score: float) -> float:
    """Round to nearest 0.5 IELTS increment, clamped 3.0–9.0."""
    rounded = round(score * 2) / 2
    return max(3.0, min(9.0, rounded))
