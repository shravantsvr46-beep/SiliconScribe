from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from main_controller import generate_embedded_solution


st.set_page_config(page_title="SyncConX", layout="wide")

st.title("⚡ SyncConX: AI Firmware Designer")

st.sidebar.header("Settings")

import os

# Try to read API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# If not found, ask user
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

user_input = st.text_input(
    "Describe your circuit:",
    placeholder="Example: Read UV sensor using ESP32"
)


if st.button("Generate Solution"):

    if not api_key:
        st.error("Please enter a Gemini API key")

    else:

        with st.spinner("Analyzing hardware..."):

            result, intent = generate_embedded_solution(user_input, api_key)

        st.success(f"Detected Hardware: {intent['mcu']} + {intent['sensor']}")

        st.subheader("Generated Embedded Solution")

        st.markdown(result)

        if "```" in result:
            code_block = result.split("```")[1]
            code_block = code_block.replace("cpp", "").replace("c", "")

            st.download_button(
                "Download Firmware",
                code_block,
                file_name="firmware.cpp"
            )