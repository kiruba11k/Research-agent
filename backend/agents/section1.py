from agents.base_model import llm
from tools.web_search import web_search
from tools.citations import normalize_sources

def run(state):
    results = web_search(
        f"Business overview regulatory profile of {state['target_company']}"
    )
    citations = normalize_sources(results["sources"])

    prompt = f"""
    Write Section 1: Account Business Overview.

    Rules:
    - Cite every factual claim using [n]
    - Executive tone
    - No em dashes
    - Natural human writing

    Sources:
    {citations}

    Annual Report:
    {state['annual_report']}
    """

    content = llm.invoke(prompt).content

    confidence = float(
        llm.invoke(
            "Score confidence 0 to 1 based on source credibility and consistency. Return only a number."
        ).content.strip()
    )

    return {
        "section1": {
            "content": content,
            "citations": citations,
            "confidence": confidence
        }
    }
