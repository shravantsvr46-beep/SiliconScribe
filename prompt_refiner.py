from groq import Groq


def refine_prompt(user_prompt, api_key):

    client = Groq(api_key=api_key)

    refinement_prompt = f"""
You are an embedded systems expert.

The user prompt below may be vague, incomplete, or poorly written.

Your task is to convert it into a clear, professional embedded systems request.

User Prompt:
{user_prompt}

Return only the improved prompt.

Example:

Input:
"motor esp"

Output:
"Generate firmware to control a DC motor using an ESP32 microcontroller and an H-bridge motor driver."

Do not explain anything.
Only return the improved prompt.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You improve embedded engineering prompts."},
            {"role": "user", "content": refinement_prompt}
        ],
        temperature=0.2,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()