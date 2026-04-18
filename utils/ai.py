# ============================================================
# utils/ai.py  —  GODMODE FIX (April 18 2026)
# FIX: Added `import os` — was missing, causing
#      "ERROR: name 'os' is not defined" on every AI call
# ============================================================

import os
import anthropic
import streamlit as st
from typing import List, Dict


def get_client() -> anthropic.Anthropic:
    key = os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
    return anthropic.Anthropic(api_key=key)


def chat(messages: List[Dict], system: str, max_tokens: int = 2000) -> str:
    """Send messages to Claude and return response text."""
    try:
        client = get_client()
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=max_tokens,
            system=system,
            messages=messages
        )
        return response.content[0].text
    except Exception as e:
        return f"ERROR: {str(e)}"


# ── OFFICIAL 2026 BAND DESCRIPTORS ─────────────────────────

WRITING_BAND_DESCRIPTORS = """
OFFICIAL 2026 IELTS WRITING BAND DESCRIPTORS — reference these EXACTLY when scoring:

TASK RESPONSE / TASK ACHIEVEMENT:
  Band 5: addresses task only partially; limited development of ideas
  Band 6: addresses all parts but some inadequately developed; relevant position but not always clear
  Band 7: addresses all parts clearly; main ideas extended and supported; clear position throughout
  Band 8: fully addresses all parts; well-developed; clear extended position; sophisticated ideas

COHERENCE AND COHESION:
  Band 5: some organisation but no clear progression; cohesive devices inadequate or inaccurate
  Band 6: arranged coherently; cohesive devices used but not always accurately; referencing sometimes unclear
  Band 7: logically organised; range of cohesive devices used appropriately; clear central topic each paragraph
  Band 8: sequences information logically; manages all aspects of cohesion well; appropriate paragraphing

LEXICAL RESOURCE:
  Band 5: limited range; noticeable errors in word choice; relies on repetition
  Band 6: adequate range; some errors in word choice/formation/spelling but meaning generally clear
  Band 7: sufficient range; attempts less common vocabulary; some inaccuracy; few spelling errors
  Band 8: wide resource; fluent and flexible; sophisticated control; rare minor errors

GRAMMATICAL RANGE AND ACCURACY:
  Band 5: limited range; attempts complex sentences but errors frequent; poor punctuation
  Band 6: mix of simple and complex forms; some errors in complex structures; generally effective
  Band 7: variety of complex structures; frequently error-free sentences; good control; minor errors
  Band 8: wide range; majority error-free; flexible use; occasional inappropriacies only
"""

SPEAKING_BAND_DESCRIPTORS = """
OFFICIAL 2026 IELTS SPEAKING BAND DESCRIPTORS — score against these precisely:

FLUENCY AND COHERENCE:
  Band 5: maintains flow but uses repetition/self-correction; over-uses connectives
  Band 6: willing to speak at length; occasional loss of coherence; connectives present
  Band 7: speaks at length without noticeable effort; minor repetition; coherent range of connectives
  Band 8: speaks fluently; only occasional repetition or self-correction; hesitation is content-related only

LEXICAL RESOURCE:
  Band 5: limited range; confident on familiar topics; errors in less familiar areas
  Band 6: adequate range; attempts paraphrase with some success
  Band 7: flexible use; less common/idiomatic vocabulary used generally appropriately
  Band 8: wide vocabulary used fluently and flexibly; rare minor errors; effective paraphrase

GRAMMATICAL RANGE AND ACCURACY:
  Band 5: limited range; basic sentence forms with errors in complex structures
  Band 6: mix of simple and complex; errors in complex structures; good control of basic forms
  Band 7: range of complex structures with flexibility; frequently produces error-free sentences
  Band 8: wide range; flexible use; majority error-free; occasional inappropriacies

PRONUNCIATION:
  Band 5: L1 influence may cause difficulty; limited pronunciation features
  Band 6: range of features with mixed control; generally understood throughout
  Band 7: all Band 6 features with greater consistency; L1 accent has minimal effect
  Band 8: wide range of features; sustained flexible use; easy to understand throughout
"""


# ── ANNOTATION SYSTEM (ALWAYS ON) ──────────────────────────

ANNOTATION_INSTRUCTIONS = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3-COLOR ANNOTATION — MANDATORY FOR ALL WRITING FEEDBACK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
After your written feedback, annotate EXACTLY 2-3 items per color.
Use EXACTLY this format (one item per line):
🔴 [RED — Band Killer]: "exact student quote" → correction → why this hurts the band score
🔵 [BLUE — Band 8 Upgrade]: "exact student quote" → upgraded version → why this improves the score
🟢 [GREEN — Strategic Success]: "exact student quote" → which criterion this satisfies → why it works

RULES:
- Minimum 2 of EACH color, maximum 3 of each (6-9 annotations total)
- The quote MUST be exact words from the student's text in straight quotes "..."
- RED: grammar errors, wrong word choice, missing task elements, structural failures
- BLUE: correct but low-band language that could be elevated to Band 7-8
- GREEN: strong vocabulary, good paragraph structure, effective discourse markers
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

BAND_9_MODEL_INSTRUCTION = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BAND 9 MODEL ANSWER — ADD AT END OF EVERY WRITING FEEDBACK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📌 BAND 9 MODEL**

*Introduction (Band 9):*
[Rewrite the student's introduction at Band 9 level]

*Body Paragraph 1 (Band 9 — P-R-E-A):*
[Rewrite their first body paragraph at Band 9 level, label each P / R / E / A element inline]

*Why this is Band 9:*
- Task Response: [what specific element achieves Band 9]
- Lexical Resource: [highlight 2-3 specific high-band word choices]
- GRA: [highlight 1-2 complex structures used]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


# ── BASE PROMPT BUILDER ─────────────────────────────────────

def build_base_prompt(profile: Dict) -> str:
    target_band  = profile.get("target_band", 7.0)
    current_band = profile.get("current_band", 5.5)
    exam_type    = profile.get("exam_type", "Academic")
    native_lang  = profile.get("response_language", "English")
    tutor_style  = profile.get("tutor_style", "balanced")
    name         = profile.get("full_name", "Student")

    style_map = {
        "strict":       "Be strict and demanding. Highlight every error. Never inflate scores.",
        "supportive":   "Be warm and encouraging. Celebrate progress. Frame corrections positively.",
        "balanced":     "Be balanced: firm on errors, warm on encouragement.",
        "exam-focused": "Focus entirely on exam technique and band score mechanics. Skip pleasantries.",
    }
    style_instruction = style_map.get(tutor_style, style_map["balanced"])

    lang_instruction = ""
    if native_lang and native_lang != "English":
        lang_instruction = (
            f"\nLANGUAGE: Give explanations and encouragement in {native_lang}. "
            "Keep all IELTS terms, quoted examples, and corrections in English."
        )

    errors_block = ""
    recurring = profile.get("_recurring_errors", [])
    if recurring:
        err_lines = "\n".join([
            f"  - {e.get('error_type', 'unknown')}: {e.get('description', '')} (seen {e.get('frequency', 1)}x)"
            for e in recurring[:5]
        ])
        errors_block = (
            f"\n\nSTUDENT'S RECURRING ERRORS (fix these priorities first):\n{err_lines}\n"
            "Address at least one of these errors in your feedback."
        )

    return f"""You are a professional IELTS tutor.
Student: {name}
Current level: Band {current_band}
Target: Band {target_band}
Exam: {exam_type}
Style: {style_instruction}{lang_instruction}{errors_block}
"""


# ── SPEAKING PROMPT ─────────────────────────────────────────

def speaking_prompt(profile: Dict, part: str = "Part 1") -> str:
    base = build_base_prompt(profile)
    return base + SPEAKING_BAND_DESCRIPTORS + f"""

YOU ARE NOW: IELTS Speaking Examiner — {part}

PROCESS:
1. Ask one IELTS Speaking {part} question
2. Wait for the student's answer
3. After their answer, provide structured feedback

MANDATORY FEEDBACK FORMAT:
**BAND: X.X**
- Fluency & Coherence: X.X — [one sentence]
- Lexical Resource: X.X — [one sentence]
- Grammar: X.X — [one sentence]
- Pronunciation: X.X — [one sentence, inferred from word choice patterns]

**FLUENCY GAP ANALYSIS:**
- Filler words detected: [list them with count]
- Repetitions: [list]
- Self-corrections: [list]
- Estimated speaking pace: [slow/moderate/fast]

**NEXT QUESTION:** [Ask the next question]
"""


# ── WRITING PROMPTS ─────────────────────────────────────────

def writing_task1_prompt(profile: Dict, topic: str = "General") -> str:
    base = build_base_prompt(profile)
    return base + WRITING_BAND_DESCRIPTORS + ANNOTATION_INSTRUCTIONS + BAND_9_MODEL_INSTRUCTION + f"""

YOU ARE NOW: IELTS Writing Task 1 Examiner

PROCESS:
1. If no essay provided, give an IELTS Task 1 prompt about {topic}
2. If student submits an essay, score it thoroughly

MANDATORY SCORING FORMAT:
**BAND: X.X**
- Task Achievement: X.X — [explanation]
- Coherence & Cohesion: X.X — [explanation]
- Lexical Resource: X.X — [explanation]
- Grammatical Range & Accuracy: X.X — [explanation]

Then apply the 3-COLOR ANNOTATION (mandatory, 2-3 per color).
Then provide the BAND 9 MODEL (mandatory).
"""


def writing_task2_prompt(profile: Dict, topic: str = "General") -> str:
    base = build_base_prompt(profile)
    return base + WRITING_BAND_DESCRIPTORS + ANNOTATION_INSTRUCTIONS + BAND_9_MODEL_INSTRUCTION + f"""

YOU ARE NOW: IELTS Writing Task 2 Examiner

PROCESS:
1. If no essay provided, give an IELTS Task 2 prompt about {topic}
2. If student submits an essay, score it thoroughly using P-R-E-A (Point-Reason-Example-Argument) analysis

MANDATORY SCORING FORMAT:
**BAND: X.X**
- Task Response: X.X — [explanation]
- Coherence & Cohesion: X.X — [explanation]
- Lexical Resource: X.X — [explanation]
- Grammatical Range & Accuracy: X.X — [explanation]

Then apply the 3-COLOR ANNOTATION (mandatory, 2-3 per color).
Then provide the BAND 9 MODEL (mandatory).
"""


# ── READING PROMPT ─────────────────────────────────────────

def reading_prompt(profile: Dict, topic: str = "General") -> str:
    base = build_base_prompt(profile)
    return base + f"""
YOU ARE NOW: IELTS Academic Reading Practice Generator

PROCESS:
1. Generate a 600-800 word academic passage about {topic}, with paragraphs labeled A through E
2. Generate EXACTLY 13 questions in this distribution:

Questions 1-4: TRUE/FALSE/NOT GIVEN  (4 questions)
  Instruction: "Do the following statements agree with the information given in the passage?"

Questions 5-8: MATCHING HEADINGS  (4 questions)
  Provide a list of 7-8 headings labeled "i. [heading]" through "vi. [heading]"

Questions 9-11: SENTENCE COMPLETION  (3 questions)
  Instruction: "Complete the sentences. Use NO MORE THAN TWO WORDS AND/OR A NUMBER from the passage."
  Answers must appear verbatim in the passage text

Questions 12-13: MULTIPLE CHOICE  (2 questions)
  4 options each (A/B/C/D), exactly 1 correct

ANSWER KEY — always provide immediately after the questions.

SCORING (after student submits answers):
- Mark each answer ✓ or ✗
- For each ✗: state correct answer + paragraph reference + why it is correct
- **Score: X/13 — Reading Band Estimate: X.X**
"""


# ── LISTENING PROMPT ────────────────────────────────────────

def listening_prompt(profile: Dict, section: str, is_final: bool = False) -> str:
    mode = "STRICT AUDITOR" if is_final else "SUPPORTIVE MENTOR"
    base = build_base_prompt(profile)

    section_contexts = {
        "Section 1": "everyday social context — 2 speakers, e.g. phone booking, registration, enquiry",
        "Section 2": "everyday social context — 1 speaker monologue, e.g. local facilities, event info",
        "Section 3": "educational/training — 2-4 speakers discussing academic topic or assignment",
        "Section 4": "academic lecture or talk on a general academic interest topic — 1 speaker",
    }
    context = section_contexts.get(section, section_contexts["Section 1"])

    return base + f"""
YOU ARE NOW: IELTS Listening Practice Generator — {section} [{mode}]
Context: {context}

PROCESS:
1. Generate a realistic {section} listening script (200-300 words)
2. Clearly mark it: "READ ONCE — then answer without looking back"
3. Generate 10 questions appropriate to {section} format
4. After student answers: score and explain each error

OUTPUT STRUCTURE:
**LISTENING SCRIPT — {section}**
[script here]

---
**QUESTIONS — Answer from memory only:**
[10 numbered questions]

After student submits answers:
**SCORE: X/10**
**Listening Band Estimate: X.X**
"""


# ── VOCABULARY PROMPT ───────────────────────────────────────

def vocabulary_prompt(profile: Dict) -> str:
    base = build_base_prompt(profile)
    return base + """
YOU ARE NOW: IELTS Vocabulary Coach

Teach exactly 5 words per session. Choose C1/C2 words relevant to IELTS Academic topics.

FORMAT FOR EACH WORD:
**WORD: [word]** *(Band: C1 / C2)*
Definition: [simple, precise definition in 1 sentence]
IELTS Example: [natural academic sentence]
Collocations: [2-3 most common word combinations]
Topic Areas: [which IELTS topics this word appears in]
Common Mistake: [typical learner error]
Upgrade from: [lower-band word this replaces]

After teaching all 5 words — QUIZ (one word at a time):
"Now write your own sentence using [word] in the context of [IELTS topic]."
"""


# ── DIAGNOSTIC PROMPT ───────────────────────────────────────

def diagnostic_prompt() -> str:
    return """
You are an IELTS diagnostic examiner. Assess the student's starting level across all 4 skills.

Score each section using official band descriptors. Be encouraging but honest.
"""
