import google.generativeai as genai
import json


def parse_user_intent(user_input, api_key):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
Analyze the following embedded system request:

"{user_input}"

Extract the following:

1. mcu (ESP32, STM32, Arduino, etc)
2. sensor or module used
3. request summary

Return ONLY a JSON object.

Example:
{{
"mcu": "ESP32",
"sensor": "MPU6050",
"request": "Read accelerometer and gyro data"
}}
"""

    response = model.generate_content(prompt)

    clean_text = response.text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(clean_text)
    except:
        return {
            "mcu": "ESP32",
            "sensor": "Unknown",
            "request": user_input
        }