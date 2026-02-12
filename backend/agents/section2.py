# Example: section2.py
from agents.base_model import llm
from tools.web_search import web_search
from tools.citations import normalize_sources

def run(state):
    results = web_search(
        f"Strategic initiatives and milestones of {state['target_company']}"
    )
    citations = normalize_sources(results["sources"])

    content = llm.invoke(f"""
    Write Section 2: Account Key Initiatives.
    Cite facts using [n].
    No em dashes.
    Sources: {citations}
    """).content

    confidence = float(llm.invoke(
        "Score confidence 0 to 1. Return only number."
    ).content.strip())

    return {
        "section2": {
            "content": content,
            "citations": citations,
            "confidence": confidence
        }
    }
