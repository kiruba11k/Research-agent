from agents.base_model import llm

def run(state: dict):
    # Context aggregation from previous parallel steps
    context = "\n".join([v.content for v in state['sections'].values()])
    
    prompt = f"Based on this research: {context}\nGenerate 3-5 high-impact strategic next steps."
    response = llm.with_structured_output(SectionOutput).invoke(prompt)
    return {"sections": {"section5": response}}
