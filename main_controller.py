import parser
import ai_engine
import review_engine
import cache_manager
import rag_engine
import re


def generate_embedded_solution(prompt):

    steps = []

    # ---------- STEP 1: USER PROMPT ----------
    steps.append(f"Step 1: User Prompt Received\n{prompt}")

    # ---------- STEP 2: PARSE HARDWARE ----------
    intent = parser.parse_prompt(prompt)
    parsed_display = parser.format_intent(intent)

    steps.append(
        f"Step 2: Hardware Intent Detection\nMCU: {intent['mcu']}\nSensor: {intent['sensor']}"
    )

    # ---------- STEP 3: CACHE CHECK ----------
    cache_key = cache_manager.get_cache_key(prompt)
    cached = cache_manager.load_cache(cache_key)

    if cached:

        steps.append("Step 3: Cache Check\nResult: Cached solution found")

        final_answer = parsed_display + "\n\n" + cached["answer"]

        return final_answer, intent, steps

    steps.append("Step 3: Cache Check\nResult: No cache found → Generating new solution")

    # ---------- STEP 4: RAG RETRIEVAL ----------
    context = rag_engine.retrieve_context(prompt)

    steps.append("Step 4: RAG Retrieval\nRelevant documentation retrieved")

    # ---------- STEP 5: AI FIRMWARE GENERATION ----------
    answer = ai_engine.generate_firmware(prompt, intent, context)

    steps.append("Step 5: Firmware Generation Complete")

    # ---------- STEP 6: ENGINEERING REVIEW ----------
    review = review_engine.review_solution(answer)

    steps.append("Step 6: Engineering Review Complete")

    # ---------- FIX SCORE FORMATTING ----------
    review = re.sub(r"Reliability Score:", "\nReliability Score:", review)
    review = re.sub(r"Protocol Safety:", "\nProtocol Safety:", review)
    review = re.sub(r"Memory Safety:", "\nMemory Safety:", review)
    review = re.sub(r"Hardware Compatibility:", "\nHardware Compatibility:", review)
    review = re.sub(r"Power Considerations:", "\nPower Considerations:", review)

    # ---------- FINAL ANSWER ----------
    final_answer = (
        parsed_display
        + "\n\n"
        + answer
        + "\n\n"
        + review
    )

    # ---------- STEP 7: SAVE CACHE ----------
    cache_manager.save_cache(
        cache_key,
        {"answer": final_answer}
    )

    steps.append("Step 7: Response Saved to Cache")

    return final_answer, intent, steps