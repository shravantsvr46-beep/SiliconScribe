import streamlit as st

# Page setup
st.set_page_config(
    page_title="SiliconScribe",
    page_icon="🧠",
    layout="wide"
)

# Header
st.markdown("""
# 🧠 SiliconScribe
### AI-Powered Embedded Firmware Generator
""")

st.write(
"Describe your hardware setup and SiliconScribe will generate firmware code, wiring instructions and compilation steps."
)

# Example prompts
st.markdown("### Example Prompts")

st.code(
"""Generate STM32F446RE driver for BMP280 using I2C
ESP32 UART communication for GPS module
Arduino PWM motor control using timer"""
)

# Prompt input
st.markdown("### Firmware Request")

prompt = st.text_area(
    "Enter your firmware request",
    placeholder="Example: Generate STM32F446RE driver for BMP280 using I2C",
    height=120
)

# Generate button
if st.button("Generate Firmware"):

    st.success("Processing request...")

    # Pipeline
    st.markdown("### Processing Pipeline")
    st.write("Prompt → Parsing → Firmware Generation → Documentation")

    # Parsed hardware spec
    st.markdown("### Parsed Hardware Specification")

    col1, col2, col3 = st.columns(3)

    col1.info("MCU: STM32F446RE")
    col2.info("Sensor: BMP280")
    col3.info("Protocol: I2C")

    # Tabs for outputs
    tab1, tab2, tab3 = st.tabs(
        ["Firmware Code", "Hardware Setup", "Flash Instructions"]
    )

    with tab1:
        code = """
#include "stm32f4xx.h"

void I2C_Init() {
    // Initialize I2C peripheral
}

void BMP280_Init() {
    // Initialize BMP280 sensor
}

int main() {

    I2C_Init();
    BMP280_Init();

    while(1) {
        // Read sensor data
    }
}
"""
        st.code(code, language="c")

        st.download_button(
            "Download Firmware",
            data=code,
            file_name="siliconscribe_driver.c",
            mime="text/plain"
        )

    with tab2:
        st.write("""
BMP280 → STM32F446RE

VCC → 3.3V  
GND → GND  
SDA → PB7  
SCL → PB6
""")

    with tab3:
        st.write("""
1. Open STM32CubeIDE  
2. Create project for STM32F446RE  
3. Add generated firmware  
4. Build project  
5. Flash using ST-Link
""")