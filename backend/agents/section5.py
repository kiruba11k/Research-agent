from agents.base_model import llm

def run(state):
    content = llm.invoke("""
    Write Section 5: Speridian Next Steps.
    No em dashes. Concrete, fundable actions.
    No citations required.
    """).content

    confidence = float(llm.invoke(
        "Score confidence 0 to 1. Return only number."
    ).content.strip())

    return {"section5": {
        "content": content,
        "citations": [],
        "confidence": confidence
    }}
