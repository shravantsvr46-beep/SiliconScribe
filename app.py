import streamlit as st
import streamlit.components.v1 as components
import main_controller
import re

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="SiliconScribe",
    page_icon="🧠",
    layout="wide"
)

# ---------- SESSION STORAGE ----------
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"New Chat": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

if "show_code" not in st.session_state:
    st.session_state.show_code = True


# ---------- SIDEBAR ----------
st.sidebar.title("💬 Chats")

if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_sessions["New Chat"] = []
    st.session_state.current_chat = "New Chat"
    st.rerun()

st.sidebar.markdown("---")

for chat_name in list(st.session_state.chat_sessions.keys()):

    col1, col2 = st.sidebar.columns([4,1])

    if col1.button(chat_name, key=f"open_{chat_name}"):
        st.session_state.current_chat = chat_name
        st.rerun()

    if col2.button("❌", key=f"delete_{chat_name}"):

        del st.session_state.chat_sessions[chat_name]

        if len(st.session_state.chat_sessions) == 0:
            st.session_state.chat_sessions["New Chat"] = []

        st.session_state.current_chat = list(st.session_state.chat_sessions.keys())[0]

        st.rerun()


messages = st.session_state.chat_sessions[st.session_state.current_chat]


# ---------- HEADER ----------
if len(messages) == 0:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown(
            "<h1 style='text-align:center;'>🧠 SiliconScribe</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align:center;'>AI Assistant for Embedded Systems</p>",
            unsafe_allow_html=True
        )

else:

    st.markdown("# 🧠 SiliconScribe")
    st.caption("AI Assistant for Embedded Systems")

st.markdown("---")


# ---------- DISPLAY CHAT ----------
for i, msg in enumerate(messages):

    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])

    if msg["role"] == "assistant":

        clean_text = re.sub(r"```.*?```", "", msg["explanation"], flags=re.DOTALL)

        if msg["code"] and st.session_state.show_code:
            col_left, col_right = st.columns([2,1])
        else:
            col_left, col_right = st.columns([1,0.01])

        with col_left:
            st.chat_message("assistant").markdown(clean_text)

        if msg["code"] and st.session_state.show_code:

            with col_right:

                st.markdown("### 💻 Code")

                st.code(msg["code"], language="c")

                st.download_button(
                    label="📋 Copy / Download Code",
                    data=msg["code"],
                    file_name="embedded_code.c",
                    mime="text/plain",
                    key=f"copy_{i}_{st.session_state.current_chat}"
                )


# ---------- TOGGLE CODE PANEL ----------
if any(m.get("code") for m in messages):

    col1, col2 = st.columns([6,1])

    with col2:
        if st.button("Toggle Code Panel"):
            st.session_state.show_code = not st.session_state.show_code
            st.rerun()


# ---------- USER INPUT ----------
if len(messages) == 0:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        user_input = st.chat_input("Ask an embedded systems question...")

else:

    user_input = st.chat_input("Ask an embedded systems question...")


if user_input:

    st.chat_message("user").write(user_input)

    messages.append({
        "role": "user",
        "content": user_input
    })

    # Rename chat based on first prompt
    if st.session_state.current_chat == "New Chat":

        title = " ".join(user_input.split()[:4])

        st.session_state.chat_sessions[title] = st.session_state.chat_sessions.pop("New Chat")

        st.session_state.current_chat = title

        messages = st.session_state.chat_sessions[title]

    # ---------- SCROLL ANCHOR ----------
    st.markdown("<div id='response-anchor'></div>", unsafe_allow_html=True)

    # Generate AI response
    with st.spinner("Analyzing datasheets..."):

        answer, intent = main_controller.generate_embedded_solution(user_input)

    code_match = re.search(r"```(.*?)```", answer, re.DOTALL)

    code = None

    if code_match:
        code = code_match.group(1).strip()

    messages.append({
        "role": "assistant",
        "explanation": answer,
        "code": code
    })

    st.rerun()


# ---------- AUTO SCROLL TO RESPONSE ----------
components.html(
    """
    <script>
        const scrollToResponse = () => {
            const anchor = parent.document.getElementById("response-anchor");
            if(anchor){
                anchor.scrollIntoView({behavior: "smooth", block: "start"});
            }
        };
        setTimeout(scrollToResponse, 300);
    </script>
    """,
    height=0
)