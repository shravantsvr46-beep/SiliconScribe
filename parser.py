import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def parse_user_intent(user_input):

    prompt = f"""
You are an embedded systems assistant.

Extract structured information from the following request.

User Request:
{user_input}

Return ONLY valid JSON in this format:

{{
  "mcu": "",
  "components": [],
  "protocols": []
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You extract structured embedded systems information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        result = response.choices[0].message.content

        intent = json.loads(result)

    except Exception:
        intent = {
            "mcu": "Unknown",
            "components": [],
            "protocols": []
        }

    return intent