import parser
import knowledge_manager
import ai_engine


def generate_embedded_solution(user_input):
    """
    Main pipeline controller for SiliconScribe
    """

    try:

        # Step 1 — Parse the user request
        intent = parser.parse_user_intent(user_input)

        mcu = intent.get("mcu", "Unknown")

        # Step 2 — Retrieve datasheet context
        context = knowledge_manager.get_datasheet_context(
            mcu,
            user_input
        )

        # Step 3 — Generate AI embedded solution
        answer = ai_engine.get_ai_response(
            user_input,
            mcu,
            context
        )

        return answer, intent

    except Exception as e:

        return f"""
⚠️ Internal processing error

Details:
{str(e)}

Possible causes:
• GROQ API issue
• Invalid GROQ_API_KEY in .env
• Datasheet not found
• Internet connection issue
""", {}