import json
from shelf_agent import analyze_shelf
from queue_agent import analyze_queue
from layout_agent import analyze_layout
from promotion_agent import analyze_promotions
from langchain_ollama import ChatOllama
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0    
)
def ask_retail_ai(question):

    question_lower = question.lower()

    # ====================================
    # GREETINGS
    # ====================================

    if question_lower in ["hi", "hello", "hey"]:

        return """
Hello! I'm your Retail AI Assistant.

You can ask me:

• Which shelf should I move?
• Which area gets the most traffic?
• Are promotions performing well?
• Where are queues forming?
• Give me a complete store report.
"""

    # ====================================
    # DECIDE WHICH AGENTS TO RUN
    # ====================================

    reports = ""

    if any(
        word in question_lower
        for word in [
            "shelf",
            "product",
            "move",
            "pickup"
        ]
    ):

        print("Running Shelf Agent...")

        reports += f"""

Shelf Agent:

{analyze_shelf()}

"""

    if any(
        word in question_lower
        for word in [
            "queue",
            "line",
            "checkout",
            "waiting"
        ]
    ):

        print("Running Queue Agent...")

        reports += f"""

Queue Agent:

{analyze_queue()}

"""

    if any(
        word in question_lower
        for word in [
            "layout",
            "traffic",
            "area",
            "zone"
        ]
    ):

        print("Running Layout Agent...")

        reports += f"""

Layout Agent:

{analyze_layout()}

"""

    if any(
        word in question_lower
        for word in [
            "promotion",
            "offer",
            "discount"
        ]
    ):

        print("Running Promotion Agent...")

        reports += f"""

Promotion Agent:

{analyze_promotions()}

"""

    # ====================================
    # COMPLETE REPORT
    # ====================================

    if "complete" in question_lower or "overall" in question_lower:

        print("Running All Agents...")

        reports = f"""

Shelf Agent:

{analyze_shelf()}

Queue Agent:

{analyze_queue()}

Layout Agent:

{analyze_layout()}

Promotion Agent:

{analyze_promotions()}

"""

    # ====================================
    # FALLBACK
    # ====================================

    if reports == "":

        reports = """
No specific agent selected.
Answer using general retail knowledge.
"""

    prompt = f"""

You are a senior retail consultant.

Manager Question:

{question}

Available Reports:

{reports}

Answer professionally.

Provide:

1. Problems detected
2. Recommendations
3. Expected impact

"""

    print("Calling Qwen...")

    response = llm.invoke(
        prompt
    )

    return response.content


# =====================================
# TERMINAL CHAT
# =====================================

if __name__ == "__main__":

    while True:

        question = input("\nManager: ")

        if question.lower() == "exit":
            break

        answer = ask_retail_ai(
            question
        )

        print("\nRetail AI:\n")

        print(answer)