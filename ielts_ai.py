# ============================================================
# IELTS Conversational AI — Day 1 + Day 2
# Built with Claude API + Streamlit
# ============================================================
# SETUP (run these commands in your terminal first):
#   pip install streamlit anthropic
#
# RUN THE APP:
#   streamlit run ielts_ai.py
#
# You need a Claude API key from: console.anthropic.com
# ============================================================

import streamlit as st          # builds the web UI automatically
import anthropic                # connects to Claude API

# ============================================================
# STEP 1 — PAGE CONFIGURATION
# This sets the browser tab title and layout
# ============================================================
st.set_page_config(
    page_title="IELTS AI Tutor",
    page_icon="🎓",
    layout="centered"
)

# ============================================================
# STEP 2 — THE SYSTEM PROMPT
# This is the brain of your AI — it tells Claude exactly
# how to behave as an IELTS examiner
# Change {{MODE}} and {{TASK}} dynamically based on user choice
# ============================================================
def get_system_prompt(mode, task):
    # This function builds the system prompt based on the
    # mode the user selected (Speaking or Writing)
    return f"""
You are an expert IELTS examiner with 10 years of experience
scoring candidates from band 4.0 to 9.0. You specialize in
helping non-native English speakers — especially from Mongolia
and Central Asia — improve their IELTS scores fast.

Current mode: {mode}
Current task: {task}

YOUR BEHAVIOR RULES:
1. Always be encouraging but brutally honest — never inflate scores
2. Never say "great job" without a specific reason
3. Always give actionable, specific feedback — not generic advice
4. Use simple English — the student may not be advanced yet
5. Never switch topics unless the student asks you to

WHEN EVALUATING SPEAKING OR WRITING:
Score on the official IELTS 4 criteria (band 4.0 to 9.0):

- Fluency & Coherence (FC): Does it flow? Is it logical?
- Lexical Resource (LR): Is the vocabulary range good?
- Grammatical Range & Accuracy (GRA): Grammar correctness?
- Task Achievement (TA): Did they answer the question fully?

FORMAT YOUR FEEDBACK EXACTLY LIKE THIS:
---
📊 IELTS BAND SCORES
• Fluency & Coherence: X.X — [one specific comment]
• Lexical Resource: X.X — [one specific improvement tip]
• Grammatical Range: X.X — [one specific grammar note]
• Task Achievement: X.X — [did they answer the task?]

🎯 Overall Band Estimate: X.X

💡 Top Priority to Improve:
[One concrete thing they should practice TODAY]
---

IF THE STUDENT IS JUST CHATTING OR ASKING A QUESTION:
Answer helpfully as their personal IELTS tutor.
Give vocabulary tips, explain grammar rules, encourage them.
"""

# ============================================================
# STEP 3 — CLAUDE API FUNCTION
# This sends messages to Claude and gets a response back
# ============================================================
def chat_with_claude(messages, mode, task, api_key):
    # Create the Anthropic client using the API key
    client = anthropic.Anthropic(api_key=api_key)

    # Send the full conversation history + system prompt to Claude
    response = client.messages.create(
        model="claude-sonnet-4-5",      # best model for this task
        max_tokens=1024,                 # max length of response
        system=get_system_prompt(mode, task),  # the brain
        messages=messages                # full chat history
    )

    # Extract just the text from Claude's response
    return response.content[0].text

# ============================================================
# STEP 4 — SESSION STATE
# Streamlit reruns the whole script on every interaction
# st.session_state stores data between reruns
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []     # stores chat history

if "mode" not in st.session_state:
    st.session_state.mode = "Speaking" # default mode

if "task" not in st.session_state:
    st.session_state.task = "General Practice"

# ============================================================
# STEP 5 — SIDEBAR (Settings Panel)
# This is the left panel where users configure their session
# ============================================================
with st.sidebar:
    st.title("⚙️ Settings")

    # API Key input — user pastes their key here
    # type="password" hides the key so it's not visible
    api_key = st.text_input(
        "Claude API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Get your key at console.anthropic.com"
    )

    st.divider()

    # Practice mode selector
    st.subheader("Practice Mode")
    mode = st.selectbox(
        "Choose what to practice:",
        [
            "Speaking — Part 1 (Personal questions)",
            "Speaking — Part 2 (Long turn / cue card)",
            "Speaking — Part 3 (Discussion)",
            "Writing — Task 1 (Graph/Chart description)",
            "Writing — Task 2 (Essay)",
            "Vocabulary Builder",
            "General Practice"
        ]
    )
    st.session_state.mode = mode

    st.divider()

    # Topic selector — changes what questions Claude asks
    st.subheader("Topic")
    topic = st.selectbox(
        "Choose a topic:",
        [
            "Technology",
            "Environment",
            "Education",
            "Health",
            "Work & Career",
            "Culture & Society",
            "Travel",
            "Food",
            "Family",
            "Free choice"
        ]
    )
    st.session_state.task = f"Topic: {topic}"

    st.divider()

    # Target band score
    target_band = st.slider(
        "Your target band score:",
        min_value=5.0,
        max_value=9.0,
        value=7.0,
        step=0.5
    )
    st.session_state.task += f" | Target band: {target_band}"

    st.divider()

    # Clear chat button — resets the conversation
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Quick start buttons — sends preset messages
    st.subheader("Quick Start")

    if st.button("🎤 Start Speaking Test", use_container_width=True):
        starter = "Please start my IELTS speaking practice. Ask me the first question."
        st.session_state.messages.append({
            "role": "user",
            "content": starter
        })

    if st.button("✍️ I want to submit an essay", use_container_width=True):
        starter = "I want to practice IELTS Writing Task 2. Please give me a question to answer."
        st.session_state.messages.append({
            "role": "user",
            "content": starter
        })

    if st.button("📚 Teach me vocabulary", use_container_width=True):
        starter = f"Teach me 5 advanced IELTS vocabulary words for the topic: {topic}. Give examples."
        st.session_state.messages.append({
            "role": "user",
            "content": starter
        })

# ============================================================
# STEP 6 — MAIN CHAT INTERFACE
# This is the main area where the conversation happens
# ============================================================

# App title and description
st.title("🎓 IELTS AI Tutor")
st.caption(f"Mode: **{mode}** | Topic: **{topic}** | Target: **Band {target_band}**")

# Show a welcome message if no chat yet
if not st.session_state.messages:
    st.info(
        "👋 Welcome! I'm your personal IELTS examiner.\n\n"
        "**How to use me:**\n"
        "- Select your practice mode in the sidebar\n"
        "- Click a Quick Start button OR type your own message\n"
        "- Submit your speaking answer or essay and I'll score it\n\n"
        "**I'll score your English on all 4 IELTS criteria and give you "
        "a band estimate after every response.**"
    )

# Display all previous messages in the chat
for message in st.session_state.messages:
    # role is either "user" or "assistant"
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================================
# STEP 7 — HANDLE NEW MESSAGES
# This runs when the user types and sends a message
# Also runs if a Quick Start button added a message above
# ============================================================

# Check if a Quick Start button added a message that hasn't
# been processed yet (no assistant reply after it)
needs_response = (
    st.session_state.messages and
    st.session_state.messages[-1]["role"] == "user"
)

# The chat input box at the bottom of the screen
user_input = st.chat_input("Type your answer, essay, or question here...")

# Process typed input
if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    needs_response = True

# Get Claude's response if needed
if needs_response:
    # Check API key is provided
    if not api_key:
        st.error(
            "⚠️ Please enter your Claude API key in the sidebar.\n\n"
            "Get your free key at: console.anthropic.com"
        )
        st.stop()

    # Show the latest user message
    with st.chat_message("user"):
        st.markdown(st.session_state.messages[-1]["content"])

    # Show a spinner while Claude is thinking
    with st.chat_message("assistant"):
        with st.spinner("Evaluating your English..."):
            try:
                # Send to Claude and get response
                response = chat_with_claude(
                    messages=st.session_state.messages,
                    mode=st.session_state.mode,
                    task=st.session_state.task,
                    api_key=api_key
                )

                # Display Claude's response
                st.markdown(response)

                # Save Claude's response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except anthropic.AuthenticationError:
                # Wrong API key
                st.error(
                    "❌ Invalid API key. Please check your key in the sidebar.\n"
                    "Make sure you copied the full key from console.anthropic.com"
                )
            except anthropic.RateLimitError:
                # Too many requests
                st.error(
                    "⏳ Rate limit hit. Wait 30 seconds and try again.\n"
                    "This happens when you send too many messages too fast."
                )
            except Exception as e:
                # Any other error — show what went wrong
                st.error(f"❌ Something went wrong: {str(e)}")

# ============================================================
# STEP 8 — FOOTER
# Shows helpful info at the bottom
# ============================================================
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Messages sent",
        len([m for m in st.session_state.messages if m["role"] == "user"])
    )

with col2:
    st.metric("Practice mode", mode.split("—")[0].strip())

with col3:
    st.metric("Target band", f"{target_band}")
