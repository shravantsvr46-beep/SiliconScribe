import parser
import knowledge_manager
import ai_engine


def generate_embedded_solution(user_input, api_key):

    # Step 1: Parse the user request
    intent = parser.parse_user_intent(user_input, api_key)

    # Step 2: Get datasheet context
    context = knowledge_manager.get_datasheet_context(
        intent["mcu"],
        user_input,
        api_key
    )

    # Step 3: Generate AI response
    answer = ai_engine.get_ai_response(
        user_input,
        intent["mcu"],
        context,
        api_key
    )

    return answer, intent