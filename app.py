import streamlit as st

# Page configuration
st.set_page_config(
    page_title="SiliconScribe",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 SiliconScribe")
st.subheader("AI Firmware Generator & Debug Assistant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
st.sidebar.title("Session Controls")

if st.sidebar.button("New Chat"):
    st.session_state.messages = []

st.sidebar.markdown("### Chat History")
for i in range(len(st.session_state.chat_history)):
    st.sidebar.write(f"Chat {i+1}")

st.sidebar.markdown("### Example Prompts")
st.sidebar.code(
"""Generate STM32F446RE driver for BMP280 using I2C
ESP32 UART communication for GPS module
Arduino PWM motor control using timer"""
)

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Describe firmware request or ask debugging help")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Build response safely
    response = (
        "### Parsed Hardware\n"
        "MCU: STM32F446RE\n"
        "Sensor: BMP280\n"
        "Protocol: I2C\n\n"
        "---\n\n"
        "### Generated Firmware\n\n"
        "```c\n"
        "#include \"stm32f4xx.h\"\n\n"
        "void I2C_Init() {\n"
        "    // Initialize I2C peripheral\n"
        "}\n\n"
        "void BMP280_Init() {\n"
        "    // Initialize BMP280 sensor\n"
        "}\n\n"
        "int main() {\n"
        "    I2C_Init();\n"
        "    BMP280_Init();\n\n"
        "    while(1) {\n"
        "        // Read sensor data\n"
        "    }\n"
        "}\n"
        "```\n\n"
        "---\n\n"
        "### Hardware Setup\n"
        "BMP280 → STM32F446RE\n"
        "VCC → 3.3V\n"
        "GND → GND\n"
        "SDA → PB7\n"
        "SCL → PB6\n\n"
        "---\n\n"
        "### Debug Tips\n"
        "- Check I2C pull-up resistors\n"
        "- Verify SDA/SCL pins\n"
        "- Confirm correct clock configuration\n"
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.markdown(response)