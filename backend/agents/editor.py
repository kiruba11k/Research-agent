from agents.base_model import llm

def run(state):
    combined = ""
    for k in ["section1", "section2", "section3", "section4", "section5"]:
        combined += state[k]["content"] + "\n\n"

    final = llm.invoke(f"""
    Refine into a single executive research document.
    Logical flow.
    No em dashes.
    """).content

    return {"final_output": final}
