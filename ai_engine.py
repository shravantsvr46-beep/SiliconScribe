from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def generate_firmware(prompt, intent, context):

    api_key = os.getenv("GROQ_API_KEY")

    client = Groq(api_key=api_key)

    mcu = intent["mcu"]

    system_prompt = f"""
You are a senior embedded systems engineer.

User Request:
{prompt}

Detected MCU:
{mcu}

Additional technical context:
{context}

Generate a professional embedded firmware solution.

Structure:

Parsed Components
Physical Feasibility Verdict
Pinout Table
Connection Summary
Firmware Code
Engineering Review
Recommended Solution
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert embedded firmware engineer."},
            {"role": "user", "content": system_prompt}
        ],
        temperature=0.2,
        max_tokens=1500
    )

    return response.choices[0].message.content