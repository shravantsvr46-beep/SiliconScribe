from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def get_ai_response(user_input, mcu, context):
    """
    Generates an embedded systems solution using Groq LLM
    with RAG datasheet context.
    """

    prompt = f"""
You are an expert embedded systems engineer.

Your task is to help developers design embedded systems using
correct information from datasheets.

User Request:
{user_input}

Microcontroller / Board:
{mcu}

Relevant Datasheet Information:
{context}

Instructions:

1. Use the datasheet information above to answer the question.
2. If the request is impossible (wrong protocol, incompatible hardware),
   explain why and suggest an alternative solution.
3. Provide correct pin usage and interfaces.
4. Provide working embedded C / Arduino style code if needed.

Output Format:

Explanation:
Explain the solution clearly.

Pins / Interfaces:
List the relevant pins or communication interfaces.

Example Code:
Provide the working code inside triple backticks.
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert embedded systems assistant that uses datasheet information."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI model error: {str(e)}"