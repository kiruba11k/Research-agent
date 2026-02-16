from agents.base_model import llm
from tools.web_search import web_search
from tools.citations import normalize_sources
from models.schemas import SectionOutput

def run(state: dict):
    company = state['target_company']
    # 1. Gather Data
    results = web_search(f"Business overview and regulatory profile of {company}")
    citations = normalize_sources(results.get("sources", []))

    # 2. Structured Prompting (Merging writing + scoring into one step)
    structured_llm = llm.with_structured_output(SectionOutput)
    
    prompt = f"""
    Write Section 1: Business Overview for {company}.
    Context from Report: {state.get('annual_report', 'None')}
    Sources: {citations}
    
    Rules: Cite facts with [n]. Professional tone. No em dashes. 
    Score confidence based on data consistency.
    """

    response = structured_llm.invoke(prompt)
    return {"sections": {"section1": response}}
