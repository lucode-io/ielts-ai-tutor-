# ============================================================
# utils/score_extractor.py
# Robust band score extraction — replaces fragile regex parsing
# Used by: onboarding.py, mock_test.py, practice.py
# ============================================================

import re
import streamlit as st
from typing import Dict, Optional


def extract_band_score_from_text(text: str, skill: str = None, default: float = None) -> Optional[float]:
    """
    Extract a single band score from AI response text.
    Uses multi-pattern regex with validation. Returns rounded 0.5 IELTS score.
    """
    score = _regex_extract(text, skill)
    if score is not None:
        return _round_ielts(score)
    return default


def extract_all_scores_from_text(text: str) -> Dict[str, float]:
    """
    Extract all skill scores from a single AI response.
    Returns dict with only the scores found (no defaults).
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
    Catches scores spread across multiple turns (e.g. diagnostic chat).
    Later messages override earlier ones.
    """
    scores = {}
    for msg in reversed(messages):
        if msg.get("role") == "assistant":
            found = extract_all_scores_from_text(msg["content"])
            for skill, score in found.items():
                if skill not in scores:
                    scores[skill] = score

    for skill in ["speaking", "writing", "reading", "listening"]:
        if skill not in scores:
            scores[skill] = default

    return scores


def extract_score_via_llm(text: str, skill: str, default: float = 5.5) -> float:
    """
    Last-resort: tiny Claude call to extract the score.
    Only for critical paths (mock test). Costs ~200 tokens.
    """
    try:
        from utils.ai import get_claude_client
        client = get_claude_client()
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
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
    """Multi-pattern regex extractor. Most specific → least specific."""
    if not text:
        return None

    skill_pat = skill.capitalize() if skill else r"(?:Speaking|Writing|Reading|Listening|Overall)"

    patterns = [
        rf"{skill_pat}\s*BAND[:\s]+(\d+\.?\d*)",
        rf"{skill_pat}\s+Band[:\s]+(\d+\.?\d*)",
        rf"Overall\s+{skill_pat}\s+Band[:\s]+(\d+\.?\d*)",
        rf"Overall\s+Band\s+Estimate[:\s]+(\d+\.?\d*)",
        rf"Overall\s+Band[:\s]+(\d+\.?\d*)",
        rf"Overall\s+Baseline[:\s]+(\d+\.?\d*)",
        rf"\*\*{skill_pat}[^*]*?(\d+\.\d)\*\*",
        rf"{skill_pat}[:\s]+(\d+\.?\d*)",
        rf"{skill_pat}\s*[—–\-]\s*(\d+\.?\d*)",
        rf"{skill_pat}[^.]*?Band\s+(\d+\.?\d*)",
        rf"{skill_pat}.{{0,50}}?(\d\.\d)",
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

    if skill is None or (skill and skill.lower() == "overall"):
        overall_patterns = [
            r"Overall[^:]*?[:\s]+(\d+\.?\d*)",
            r"\*\*Overall[^*]*?(\d+\.?\d*)\*\*",
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
    """Round to nearest 0.5, clamped 3.0–9.0."""
    return max(3.0, min(9.0, round(score * 2) / 2))
