# ============================================================
# PATCH FILE — modules/practice.py
#
# BUG 4 FIX: Autocorrect corrupts vocabulary on mobile
#   Root cause: st.text_area() renders a plain <textarea> with
#   no autocorrect="off" attribute — iOS/Android autocorrect
#   silently replaces C1/C2 words students type.
#
# BUG 5 FIX: No live word count while typing on phone
#   Root cause: Word count computed server-side only on rerun.
#   On mobile, keyboard covers screen for minutes with no feedback.
#
# HOW TO APPLY:
#   In modules/practice.py, find the entire function:
#     def _render_writing_input(mode, topic, target_band, profile, user_id):
#   Replace it completely with the function below.
#   All other code in practice.py is UNCHANGED.
#
# ALSO ADD THIS IMPORT at the top of practice.py (with other imports):
#   import streamlit.components.v1 as components
# ============================================================

import streamlit as st
import streamlit.components.v1 as components


def _render_writing_input(mode: str, topic: str, target_band: float,
                           profile: dict, user_id: str):
    """
    Writing input with:
    - BUG 4 FIX: autocorrect/spellcheck disabled on mobile via JS attribute injection
    - BUG 5 FIX: live word count via JS input event (zero server round-trips)
    - Autocorrect toggle button so users can re-enable if they want
    """
    min_words  = 150 if "Task 1" in mode else 250
    task_label = "Task 1" if "Task 1" in mode else "Task 2"

    val_key    = f"essay_val_{mode}"
    widget_key = f"essay_widget_{mode}"

    # ── Autocorrect toggle ──
    ac_key = f"autocorrect_on_{mode}"
    if ac_key not in st.session_state:
        st.session_state[ac_key] = False  # Default: OFF (better for IELTS vocabulary)

    ac_col, label_col = st.columns([1, 5])
    with ac_col:
        if st.button(
            "🔤 AC ON" if st.session_state[ac_key] else "🔤 AC OFF",
            key=f"ac_toggle_{mode}",
            use_container_width=True,
            help="Toggle autocorrect. Disable to prevent phone from changing your vocabulary."
        ):
            st.session_state[ac_key] = not st.session_state[ac_key]
            st.rerun()
    with label_col:
        ac_status = "Autocorrect ON" if st.session_state[ac_key] else "Autocorrect OFF (recommended for IELTS)"
        ac_color  = "rgba(240,192,64,0.8)" if st.session_state[ac_key] else "rgba(0,232,122,0.7)"
        st.markdown(
            f'<div style="font-size:11px;color:{ac_color};padding-top:10px">{ac_status}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div style="font-size:11px;color:rgba(180,210,255,0.45);'
        f'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;margin-top:8px">'
        f'Paste or type your {task_label} essay below (minimum {min_words} words)'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Standard st.text_area ──
    essay_text = st.text_area(
        label=f"{task_label} essay",
        height=220,
        placeholder=(
            f"Paste your essay here or ask for a question first...\n\n"
            f"Minimum {min_words} words for accurate scoring."
        ),
        key=widget_key,
        label_visibility="collapsed",
    )
    st.session_state[val_key] = essay_text

    # ── BUG 4+5 FIX: JS injected after text_area renders ──
    # Finds the textarea in the DOM, sets autocorrect attrs, adds live word counter.
    # Uses a unique marker class on a sibling div to locate the right textarea.
    autocorrect_val = "on" if st.session_state[ac_key] else "off"
    spellcheck_val  = "true" if st.session_state[ac_key] else "false"

    components.html(
        f"""
        <div id="wc_container_{widget_key}" style="
            font-size:13px;
            color:#4A9EFF;
            font-weight:700;
            padding:4px 0 8px 2px;
            font-family:Inter,sans-serif;
        ">
            <span id="wc_count_{widget_key}">0</span>
            <span style="color:rgba(180,210,255,0.4);font-weight:400"> / {min_words} words</span>
            <span id="wc_status_{widget_key}" style="margin-left:12px;font-size:11px"></span>
        </div>

        <script>
        (function() {{
            var MIN = {min_words};
            var KEY = "{widget_key}";

            function updateCount(text) {{
                var words = text.trim() === "" ? 0 : text.trim().split(/\\s+/).length;
                var countEl  = document.getElementById("wc_count_" + KEY);
                var statusEl = document.getElementById("wc_status_" + KEY);
                if (!countEl) return;

                countEl.textContent = words;
                if (words >= MIN) {{
                    countEl.style.color = "#00e87a";
                    statusEl.textContent = "✓ Ready to submit";
                    statusEl.style.color = "#00e87a";
                }} else if (words >= Math.floor(MIN * 0.8)) {{
                    countEl.style.color = "#F0C040";
                    statusEl.textContent = (MIN - words) + " more words needed";
                    statusEl.style.color = "rgba(240,192,64,0.7)";
                }} else {{
                    countEl.style.color = "#ff3a4a";
                    statusEl.textContent = (MIN - words) + " more words needed";
                    statusEl.style.color = "rgba(255,58,74,0.7)";
                }}
            }}

            function applyAttrs(textarea) {{
                textarea.setAttribute("autocorrect", "{autocorrect_val}");
                textarea.setAttribute("autocapitalize", "off");
                textarea.setAttribute("spellcheck", "{spellcheck_val}");
                textarea.setAttribute("autocomplete", "off");
                textarea.removeEventListener("input", onInput);
                textarea.addEventListener("input", onInput);
                updateCount(textarea.value);
            }}

            function onInput(e) {{
                updateCount(e.target.value);
            }}

            function findAndPatch() {{
                // Walk up from this script's container to find Streamlit textareas
                // Streamlit renders textareas with data-testid or aria-label matching our key
                var textareas = window.parent.document.querySelectorAll("textarea");
                if (!textareas.length) textareas = document.querySelectorAll("textarea");
                textareas.forEach(function(ta) {{
                    applyAttrs(ta);
                }});
            }}

            // Run immediately and again after short delay for late-rendering
            findAndPatch();
            setTimeout(findAndPatch, 300);
            setTimeout(findAndPatch, 800);
        }})();
        </script>
        """,
        height=50,
    )

    # Server-side word count (fallback display, updates on any rerun)
    word_count  = len(essay_text.split()) if essay_text.strip() else 0
    bar_pct     = min(100, int(word_count / min_words * 100))
    cnt_color   = ("#00e87a" if word_count >= min_words
                   else "#F0C040" if word_count >= int(min_words * 0.8)
                   else "#ff3a4a")

    st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">
  <div style="flex:1;height:4px;background:rgba(74,158,255,0.1);border-radius:2px">
    <div style="width:{bar_pct}%;height:100%;background:{cnt_color};
                border-radius:2px;transition:width 0.3s"></div>
  </div>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Submit for Scoring", use_container_width=True,
                     key=f"submit_{mode}", disabled=(word_count < 30)):
            if essay_text.strip():
                _send_message(essay_text, mode, topic, target_band, profile, user_id)
    with col2:
        if st.button("❓ Give me a question", use_container_width=True,
                     key=f"getq_{mode}"):
            _send_message(
                f"Give me an IELTS {task_label} question about {topic}.",
                mode, topic, target_band, profile, user_id,
            )
    with col3:
        if st.button("💡 Strategy tips", use_container_width=True,
                     key=f"strat_{mode}"):
            _send_message(
                f"Explain the best strategy for IELTS Writing {task_label}.",
                mode, topic, target_band, profile, user_id,
            )

    chat_in = st.chat_input("Ask anything about writing strategy, vocab, or grammar…")
    if chat_in:
        _send_message(chat_in, mode, topic, target_band, profile, user_id)
