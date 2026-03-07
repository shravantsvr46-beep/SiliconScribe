import google.generativeai as genai


def get_ai_response(user_input, mcu, context, api_key):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are an Expert Embedded Systems Engineer helping design microcontroller circuits.

Context extracted from datasheet:
{context}

User Request:
{user_input}

Target MCU:
{mcu}

Your task is to generate a COMPLETE embedded solution.

STRICT RULES:

1. Detect all components mentioned in the request.

2. ALWAYS generate a COMPLETE PINOUT TABLE using this format:

| Component | Pin Name | Connects To | MCU Pin | Description |

3. Choose SAFE pins for the MCU.
Avoid:
- ESP32 boot pins
- ADC2 pins when WiFi may be used
- restricted pins

4. After the pinout table provide:

### Connection Summary
Example:
Sensor VCC → ESP32 3.3V
Sensor GND → ESP32 GND

5. After that generate CLEAN AND COMMENTED firmware code.

Requirements:
- Arduino IDE compatible
- Complete and compilable
- Well commented

6. Explain briefly how the circuit works.

Output format:

Pinout Table  
Connection Summary  
Firmware Code  
Explanation
"""

    response = model.generate_content(prompt)

    return response.text