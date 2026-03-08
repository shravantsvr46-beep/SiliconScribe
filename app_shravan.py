import streamlit as st
import main_controller
import re

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

        with st.chat_message("assistant"):

            # SHOW STEPS
            if "steps" in msg:
                st.markdown("### 🔍 Execution Flow")
                for step in msg["steps"]:
                    st.write(step)

            # CLEAN TEXT
            clean_text = re.sub(r"```.*?```", "", msg["explanation"], flags=re.DOTALL)
            st.markdown(clean_text)

            # CODE PANEL
            if msg.get("code") and st.session_state.show_code:

                st.markdown("### 💻 Firmware Code")

                st.code(msg["code"], language="cpp")

                st.download_button(
                    label="📋 Download Code",
                    data=msg["code"],
                    file_name="embedded_code.c",
                    mime="text/plain",
                    key=f"copy_{i}_{st.session_state.current_chat}"
                )


# ---------- USER INPUT ----------
if len(messages) == 0:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        user_input = st.chat_input("Ask an embedded systems question...")

else:

    user_input = st.chat_input("Ask an embedded systems question...")


# ---------- HANDLE USER INPUT ----------
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

    # ---------- GENERATE RESPONSE ----------
    with st.spinner("Analyzing datasheets..."):

        answer, intent, steps = main_controller.generate_embedded_solution(user_input)

    # Extract code block
    code_match = re.search(r"```(.*?)```", answer, re.DOTALL)

    code = None

    if code_match:
        code = code_match.group(1).strip()

    messages.append({
        "role": "assistant",
        "explanation": answer,
        "code": code,
        "steps": steps
    })

    st.rerun()