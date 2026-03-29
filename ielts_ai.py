# ============================================================
# IELTS AI Tutor — Production Version 2.0
# Built with Claude API + Streamlit
# Author: Logshir (lucode-io)
# ============================================================

import streamlit as st
import anthropic

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IELTS AI Tutor",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# CONSTANTS
# ============================================================

MODES = [
    "Speaking — Part 1 (Personal questions)",
    "Speaking — Part 2 (Long turn / cue card)",
    "Speaking — Part 3 (Discussion)",
    "Writing — Task 1 (Graph/Chart description)",
    "Writing — Task 2 (Essay)",
    "Listening — Section 1 (Conversation)",
    "Listening — Section 2 (Monologue)",
    "Listening — Section 3 (Academic discussion)",
    "Listening — Section 4 (Academic lecture)",
    "Reading — Academic passage",
    "Vocabulary Builder",
    "General Practice"
]

TOPICS = [
    "Technology", "Environment", "Education", "Health",
    "Work and Career", "Culture and Society", "Travel",
    "Food", "Family", "Crime and Law", "Economy", "Free choice"
]

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def init_session_state():
    defaults = {
        "messages": [],
        "mode": MODES[0],
        "task": "General Practice",
        "essay_count": 0,
        "target_band": 7.0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================
# SYSTEM PROMPTS
# ============================================================

def get_system_prompt(mode, task, target_band):
    base = f"""
You are an expert IELTS examiner with 15 years of experience.
You specialize in helping Mongolian and Central Asian students reach band 7.0+.
You are honest, specific, and encouraging.

Target band: {target_band}
Current task: {task}

RULES FOR ALL MODES:
- Never inflate scores. Honest feedback only.
- Never say "great job" without a specific reason.
- Always give ONE concrete thing to improve today.
- Use simple English — student may not be advanced.
- Never switch topics unless student asks.
"""

    if "Speaking" in mode:
        part = "Part 1" if "Part 1" in mode else "Part 2" if "Part 2" in mode else "Part 3"
        return base + f"""
YOU ARE NOW: IELTS Speaking Examiner — {part}

HOW TO HANDLE SPEAKING PRACTICE:
- Ask ONE question at a time
- Wait for student answer
- Score their answer using 4 criteria
- Ask the NEXT question naturally

SPEAKING SCORING CRITERIA:
1. Fluency and Coherence (FC)
2. Lexical Resource (LR)
3. Grammatical Range and Accuracy (GRA)
4. Pronunciation (P) — evaluate from written text

FORMAT YOUR SPEAKING FEEDBACK EXACTLY LIKE THIS:
---
IELTS SPEAKING BAND SCORES
Fluency and Coherence: X.X — [specific comment]
Lexical Resource: X.X — [specific vocabulary tip]
Grammatical Range: X.X — [specific grammar note]
Pronunciation: X.X — [note from written clues]

Overall Speaking Band: X.X to X.X

Priority Fix This Week:
[One specific thing to practice — very concrete]

Better Phrases You Could Have Used:
[2 to 3 upgraded phrases based on what they said]
---
After feedback — ask the next question naturally.
"""

    elif "Task 1" in mode:
        return base + f"""
YOU ARE NOW: IELTS Writing Task 1 Examiner

TASK 1 SCORING CRITERIA:
1. Task Achievement (TA) — Key features described? Overview present?
2. Coherence and Cohesion (CC) — Logical organization?
3. Lexical Resource (LR) — Vocabulary for describing data?
4. Grammatical Range and Accuracy (GRA)

BAND 7+ TASK 1 REQUIRES:
- Overview paragraph starting with "Overall..."
- Specific data with numbers and dates
- Comparisons and contrasts
- No personal opinion — describe only
- Minimum 150 words

IF USER ASKS FOR A QUESTION:
Generate a realistic bar chart, line graph, table, pie chart, map, or process question with realistic data.

FORMAT YOUR TASK 1 FEEDBACK EXACTLY LIKE THIS:
---
IELTS BAND SCORES — Writing Task 1
Task Achievement: X.X — [overview present? key features covered?]
Coherence and Cohesion: X.X — [paragraph structure]
Lexical Resource: X.X — [data vocabulary]
Grammatical Range: X.X — [specific error noted]

Overall Band Estimate: X.X to X.X

What Worked:
[2 specific things done well]

What To Fix:
[2 specific improvements with examples]

Improved Version of Your Weakest Paragraph:
[Rewrite their weakest paragraph at band 7 level]
---
"""

    elif "Task 2" in mode:
        return base + f"""
YOU ARE NOW: IELTS Writing Task 2 Examiner

TASK 2 SCORING CRITERIA:
1. Task Response (TR) — All parts answered? Position clear?
2. Coherence and Cohesion (CC) — Essay structure and flow?
3. Lexical Resource (LR) — Vocabulary range and accuracy?
4. Grammatical Range and Accuracy (GRA)

BAND 7+ TASK 2 REQUIRES:
- Clear position in introduction
- 2 fully developed body paragraphs with examples
- Counter-argument addressed and refuted properly
- Consistent position throughout
- Minimum 250 words

IF USER ASKS FOR A QUESTION:
Generate a realistic Task 2 question — opinion, discussion, problem-solution, or two-part style.

FORMAT YOUR TASK 2 FEEDBACK EXACTLY LIKE THIS:
---
IELTS BAND SCORES — Writing Task 2
Task Response: X.X — [all parts answered fully?]
Coherence and Cohesion: X.X — [structure comment]
Lexical Resource: X.X — [vocabulary range comment]
Grammatical Range: X.X — [grammar accuracy comment]

Overall Band Estimate: X.X to X.X

What Worked:
[2 specific things with quotes from their essay]

What To Fix:
[2 specific improvements with rewritten examples]

Improved Version of Your Introduction:
[Rewrite their introduction at band 7+ level]

Vocabulary Upgrades:
[5 word or phrase upgrades from their essay]
---
"""

    elif "Listening" in mode:
        section = mode.split("—")[1].strip() if "—" in mode else "Section 1"
        return base + f"""
YOU ARE NOW: IELTS Listening Practice Generator — {section}

HOW LISTENING PRACTICE WORKS:
1. Generate a realistic listening script for {section}
2. Student reads it carefully once (simulates listening once)
3. Generate 10 questions based only on the script
4. Student answers from memory
5. Score and explain every error

QUESTION TYPES TO USE:
- Form or note completion (write exact words — 1 to 3 words)
- Multiple choice (A, B, or C)
- Matching
- Short answer (maximum 3 words)

IMPORTANT RULES:
- Answers must come ONLY from the script
- Note completion answers should be 1 to 3 words only
- Multiple choice must have 3 clear options

FORMAT:
1. Show script labeled "LISTENING SCRIPT — Read once carefully"
2. Tell student to answer questions without looking back
3. Show questions labeled "QUESTIONS — Answer from memory"
4. After answers — show scores and explain each error
"""

    elif "Reading" in mode:
        return base + f"""
YOU ARE NOW: IELTS Reading Practice Generator

HOW READING PRACTICE WORKS:
1. Generate a realistic academic passage — 600 to 800 words
2. Generate 13 questions of mixed types
3. Student answers all questions
4. Score every answer and explain each error

QUESTION TYPES TO INCLUDE:
- True False Not Given (most important)
- Yes No Not Given
- Matching headings to paragraphs
- Multiple choice
- Short answer (3 words maximum)
- Sentence completion

TFNG STRICT RULES — explain these clearly:
TRUE = passage clearly and directly confirms it
FALSE = passage clearly and directly contradicts it
NOT GIVEN = passage does not mention it at all
If in doubt — NOT GIVEN. Never guess TRUE or FALSE.

PASSAGE REQUIREMENTS:
- Academic topic — science, history, society, technology
- Realistic Cambridge IELTS style
- Include specific facts, numbers, and names
- Paragraphs labeled A, B, C, D

FORMAT:
1. Show passage with labeled paragraphs
2. Show all 13 questions
3. After student answers — score each one
4. Explain every wrong answer with paragraph reference
5. Identify which question type they struggle with most
"""

    elif "Vocabulary" in mode:
        return base + f"""
YOU ARE NOW: IELTS Vocabulary Coach

HOW VOCABULARY SESSIONS WORK:
1. Teach 5 words per session connected to IELTS topics
2. Test student on previous words first
3. Give definition plus example plus collocations
4. Quiz the student at the end

FORMAT FOR EACH WORD:
WORD: [word]
Definition: [simple clear definition]
IELTS example: [natural sentence using this word]
Collocations: [2 to 3 common word combinations]
Band level: [B2 or C1 or C2]
Topic: [which IELTS topic this helps]

After teaching — quiz the student:
Use [word] in your own sentence about [topic].
Give specific feedback on their sentence.
"""

    else:
        return base + """
YOU ARE NOW: Personal IELTS Tutor

Help the student with whatever they need.
Answer questions about IELTS format, scoring, strategies.
Give vocabulary tips. Explain grammar rules.
Encourage them. Point them toward the right practice mode.
"""

# ============================================================
# CLAUDE API CALL
# ============================================================

def chat_with_claude(messages, mode, task, target_band, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        system=get_system_prompt(mode, task, target_band),
        messages=messages
    )
    return response.content[0].text

# ============================================================
# HELPER — START SESSION CLEANLY
# ============================================================

def start_session(mode, topic, starter_message):
    st.session_state.mode = mode
    st.session_state.messages = [{"role": "user", "content": starter_message}]
    st.rerun()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.title("⚙️ Settings")

    api_key = st.secrets.get("ANTHROPIC_API_KEY", "") or st.text_input(
        "Claude API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Get your key at console.anthropic.com"
    )

    st.divider()

    st.subheader("Practice Mode")
    mode = st.selectbox("Choose what to practice:", MODES)
    st.session_state.mode = mode

    mode_hints = {
        "Speaking": "Type your answers as if speaking. Claude scores each answer and asks the next question.",
        "Task 1": "Ask for a graph question or paste your essay. 20 minutes. 150 words minimum.",
        "Task 2": "Ask for an essay question or paste your essay. 40 minutes. 250 words minimum.",
        "Listening": "Claude generates a script. Read it once carefully. Then answer questions from memory.",
        "Reading": "Claude generates a passage and 13 questions. When in doubt — NOT GIVEN.",
        "Vocabulary": "Claude teaches 5 words then quizzes you. Daily habit builds to 450 words by June."
    }
    for key, hint in mode_hints.items():
        if key in mode:
            st.info(hint)
            break

    st.divider()

    st.subheader("Topic")
    topic = st.selectbox("Choose a topic:", TOPICS)

    st.divider()

    target_band = st.slider(
        "Your target band score:",
        min_value=5.0, max_value=9.0, value=7.0, step=0.5
    )
    st.session_state.target_band = target_band
    st.session_state.task = f"Topic: {topic} | Target: Band {target_band}"

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.essay_count = 0
        st.rerun()

    st.divider()

    st.subheader("🚀 Quick Start")

    # Universal 4-skill buttons always visible
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 Speaking", use_container_width=True):
            start_session(
                "Speaking — Part 1 (Personal questions)",
                topic,
                f"Please start my IELTS Speaking Part 1 practice. Ask me the first question about {topic}."
            )
        if st.button("📖 Reading", use_container_width=True):
            start_session(
                "Reading — Academic passage",
                topic,
                f"Give me an IELTS Academic Reading passage about {topic} with 13 mixed questions."
            )
    with col2:
        if st.button("✍️ Writing", use_container_width=True):
            start_session(
                "Writing — Task 2 (Essay)",
                topic,
                f"Give me a realistic IELTS Writing Task 2 question about {topic}."
            )
        if st.button("🎧 Listening", use_container_width=True):
            start_session(
                "Listening — Section 1 (Conversation)",
                topic,
                f"Give me an IELTS Listening Section 1 practice about {topic}. Generate the script and 10 questions."
            )

    st.divider()

    # Mode-specific detailed buttons
    if "Speaking" in mode:
        part = "Part 1" if "Part 1" in mode else "Part 2" if "Part 2" in mode else "Part 3"
        if st.button(f"▶ Start {part} Test", use_container_width=True):
            starter = f"Please start my IELTS Speaking {part} practice. Ask me the first question about {topic}."
            st.session_state.messages.append({"role": "user", "content": starter})
            st.rerun()

    elif "Task 1" in mode:
        if st.button("📊 Give me a Task 1 question", use_container_width=True):
            starter = f"Give me an IELTS Writing Task 1 question about {topic}. Make it realistic like Cambridge books."
            st.session_state.messages.append({"role": "user", "content": starter})
            st.rerun()
        if st.button("📝 Submit my Task 1 essay", use_container_width=True):
            starter = "I want to submit my IELTS Writing Task 1 essay for scoring. Please wait for me to paste it."
            st.session_state.messages.append({"role": "user", "content": starter})
            st.rerun()

    elif "Task 2" in mode:
        if st.button("❓ Give me a Task 2 question", use_container_width=True):
            starter = f"Give me a realistic IELTS Writing Task 2 question about {topic}."
            st.session_state.messages.append({"role": "user", "content": starter})
            st.rerun()
        if st.button("📝 Submit my essay", use_container_width=True):
            starter = "I want to submit my IELTS Writing Task 2 essay for scoring. Please wait for me to paste it."
            st.session_state.messages.append({"role": "user", "content": starter})
            st.rerun()

    elif "Listening" in mode:
        section = mode.split("—")[1].strip() if "—" in mode else "Section 1"
        if st.button(f"▶ Start {section} Practice", use_container_width=True):
            starter = f"Give me an IELTS Listening {section} practice about {topic}. Generate the script and 10 questions."
            st.session_state.messages.append({"role": "user", "content": starter})
            st.rerun()

    elif "Reading" in mode:
        if st.button("▶ Start Reading Practice", use_container_width=True):
            starter = f"Give me an IELTS Academic Reading passage about {topic} with 13 mixed questions."
            st.session_state.messages.append({"role": "user", "content": starter})
            st.rerun()

    elif "Vocabulary" in mode:
        if st.button("📚 Teach me vocabulary", use_container_width=True):
            starter = f"Teach me 5 advanced IELTS vocabulary words for {topic}. Then quiz me."
            st.session_state.messages.append({"role": "user", "content": starter})
            st.rerun()

    else:
        if st.button("▶ Start Practice", use_container_width=True):
            starter = "I want to improve my IELTS score. What should I practice first based on my weak areas?"
            st.session_state.messages.append({"role": "user", "content": starter})
            st.rerun()

# ============================================================
# MAIN LAYOUT
# ============================================================

main_col, info_col = st.columns([3, 1])

with main_col:
    st.title("🎓 IELTS AI Tutor")
    st.caption(f"Mode: **{mode}** | Topic: **{topic}** | Target: **Band {target_band}**")

    if not st.session_state.messages:
        welcome_messages = {
            "Speaking": "**Speaking Practice Active**\n\nType your answers naturally — write exactly how you would speak.\nClaude asks questions one at a time and scores each answer.\n\nClick a Quick Start button in the sidebar to begin.",
            "Task 1": "**Writing Task 1 Active**\n\n20 minutes. Minimum 150 words.\nAsk for a question or paste your own essay.\n\n4 criteria: Task Achievement | Coherence | Vocabulary | Grammar",
            "Task 2": "**Writing Task 2 Active**\n\n40 minutes. Minimum 250 words.\nAsk for a question or paste your own essay.\n\n4 criteria: Task Response | Coherence | Vocabulary | Grammar",
            "Listening": "**Listening Practice Active**\n\nClaude generates a realistic script.\nRead it once only. Then answer questions from memory.\n\nClick Start Listening Practice in the sidebar to begin.",
            "Reading": "**Reading Practice Active**\n\nClaude generates an academic passage and 13 questions.\n20 minutes per passage. Read questions first.\n\nRemember: When in doubt — NOT GIVEN",
            "Vocabulary": "**Vocabulary Builder Active**\n\n5 new words per session. Quiz after each set.\nTarget: 450 words retained by June exam.\n\nClick Teach me vocabulary to begin."
        }
        default_msg = "**Welcome to IELTS AI Tutor**\n\nSelect your practice mode in the sidebar.\nUse the Quick Start buttons to begin instantly.\n\nAll 4 skills: Speaking | Writing | Listening | Reading"

        shown = False
        for key, msg in welcome_messages.items():
            if key in mode:
                st.info(msg)
                shown = True
                break
        if not shown:
            st.info(default_msg)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ============================================================
# INFO PANEL
# ============================================================

with info_col:
    st.subheader("📋 Quick Reference")

    reference_content = {
        "Speaking": "**Speaking Tips:**\n- Extend every answer\n- Use linking words\n- Avoid maybe and actually\n- Speak for 2+ min in Part 2\n\n**Band 7 needs:**\n- Wide vocabulary\n- Complex sentences\n- Fluent delivery",
        "Task 1": "**Task 1 Formula:**\n1. Paraphrase question\n2. Overview — start with Overall\n3. Key detail plus numbers\n4. Comparison\n\n**Must have:**\n- Specific numbers\n- No opinion\n- 150+ words",
        "Task 2": "**Task 2 Formula:**\n1. Introduction plus position\n2. Body 1 — main argument\n3. Body 2 — second argument\n4. Counter plus refute\n5. Conclusion\n\n**Must have:**\n- Clear position\n- Real examples\n- 250+ words",
        "Listening": "**Listening Strategy:**\n- Read questions first\n- Predict answer type\n- Listen for keywords\n- Check spelling\n\n**Common errors:**\n- Missing plurals\n- Wrong spelling\n- Extra words",
        "Reading": "**TFNG Rules:**\n- TRUE = text confirms\n- FALSE = text contradicts\n- NOT GIVEN = not mentioned\n\n**Strategy:**\n1. Read questions first\n2. Scan for keywords\n3. 2 min max per question\n4. Never get stuck",
        "Vocabulary": "**Vocab System:**\n- 5 words per session\n- Say each in a sentence\n- Review previous 5 first\n- Target: 450 by June\n\n**B2 to C1 upgrade:**\n- Use rare words\n- Use collocations\n- Avoid repetition"
    }

    default_ref = "**IELTS Band Scale:**\n- Band 9: Expert\n- Band 8: Very Good\n- Band 7: Good\n- Band 6: Competent\n- Band 5: Modest\n\n**Your target: 7.0+**\nAll 4 skills matter equally."

    shown = False
    for key, content in reference_content.items():
        if key in mode:
            st.markdown(content)
            shown = True
            break
    if not shown:
        st.markdown(default_ref)

    st.divider()

    st.subheader("📊 Session Stats")
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.metric("Messages sent", user_msgs)
    st.metric("Target band", f"{target_band}")
    st.metric("Essays scored", st.session_state.essay_count)

# ============================================================
# CHAT INPUT AND CLAUDE RESPONSE
# ============================================================

needs_response = (
    st.session_state.messages and
    st.session_state.messages[-1]["role"] == "user"
)

user_input = st.chat_input("Type your answer, essay, or question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    needs_response = True

if needs_response:
    if not api_key:
        st.error("Please enter your Claude API key in the sidebar.\n\nGet your free key at: console.anthropic.com")
        st.stop()

    with main_col:
        with st.chat_message("user"):
            st.markdown(st.session_state.messages[-1]["content"])

        with st.chat_message("assistant"):
            with st.spinner("Evaluating your English..."):
                try:
                    response = chat_with_claude(
                        messages=st.session_state.messages,
                        mode=st.session_state.mode,
                        task=st.session_state.task,
                        target_band=st.session_state.target_band,
                        api_key=api_key
                    )
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

                    if "Task" in st.session_state.mode and len(st.session_state.messages[-2]["content"]) > 100:
                        st.session_state.essay_count += 1

                except anthropic.AuthenticationError:
                    st.error("Invalid API key. Check your key at console.anthropic.com")
                except anthropic.RateLimitError:
                    st.error("Rate limit hit. Wait 30 seconds and try again.")
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
