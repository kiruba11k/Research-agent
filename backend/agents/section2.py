from agents.base_model import llm
from tools.web_search import web_search
from tools.citations import normalize_sources
from models.schemas import SectionOutput

def run(state: dict):
    company = state['target_company']
    # 1. Targeted search for strategy and milestones
    query = f"Strategic initiatives, growth plans, and recent milestones of {company} 2024-2025"
    results = web_search(query)
    citations = normalize_sources(results.get("sources", []))

    # 2. Single LLM call using Pydantic for structure
    structured_llm = llm.with_structured_output(SectionOutput)
    
    prompt = f"""
    Write Section 2: Account Key Initiatives for {company}.
    
    Focus:
    - Major strategic growth initiatives and business transformations.
    - Key milestones achieved in the last 12-18 months.
    - Future-looking business goals mentioned in public filings.

    Rules:
    - Cite every factual claim using [n].
    - Use an executive, professional tone.
    - NO em dashes.
    - Use the provided context from the annual report if available.

    Context from Report: {state.get('annual_report', 'Not provided')}
    Web Sources: {citations}
    """

    response = structured_llm.invoke(prompt)
    return {"sections": {"section2": response}}
