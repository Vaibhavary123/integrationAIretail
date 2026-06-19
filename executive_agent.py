from langchain_ollama import ChatOllama

from shelf_agent import analyze_shelf
from queue_agent import analyze_queue
from layout_agent import analyze_layout
from promotion_agent import analyze_promotions


llm = ChatOllama(

    model="qwen3:8b"

)


def executive_report():

    # ===================================
    # REPORTS FROM SUB-AGENTS
    # ===================================

    shelf_report = analyze_shelf()

    queue_report = analyze_queue()

    layout_report = analyze_layout()

    promotion_report = analyze_promotions()

    # ===================================
    # PROMPT
    # ===================================

    prompt = f"""

You are a senior retail consultant.

Below are reports from specialist agents.

Shelf Agent:

{shelf_report}

Queue Agent:

{queue_report}

Layout Agent:

{layout_report}

Promotion Agent:

{promotion_report}

Analyze the store.

Provide:

1. Overall health.
2. Problems detected.
3. Shelf optimization.
4. Product placement recommendations.
5. Expected impact.

"""

    response = llm.invoke(

        prompt

    )

    return response.content


if __name__ == "__main__":

    print(

        "\n===== EXECUTIVE REPORT =====\n"

    )

    print(

        executive_report()

    )

    print(

        "\n===========================\n"

    )