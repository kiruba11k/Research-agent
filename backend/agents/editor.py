from agents.base_model import llm

def run(state: dict):
    combined = "\n\n".join([v.content for v in state['sections'].values()])
    final = llm.invoke(f"Refine this into a single executive document: {combined}").content
    return {"final_output": final}
