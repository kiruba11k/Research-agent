from agents.base_model import llm
from tools.web_search import web_search
from tools.citations import normalize_sources
from models.schemas import SectionOutput

def run(state: dict):
    company = state['target_company']
    # 1. Partner and ecosystem search
    query = f"Existing partners, consulting vendors, and service providers for {company}"
    results = web_search(query)
    citations = normalize_sources(results.get("sources", []))

    structured_llm = llm.with_structured_output(SectionOutput)
    
    prompt = f"""
    Write Section 4: Speridian Account Relationship and Competitive Context for {company}.
    
    Focus:
    - Current service providers and consulting partners (Big 4, Boutique, etc.).
    - Competitive landscape: Who else is "in the room"?
    - Strategic gaps where a partner like Speridian can add value.

    Rules:
    - Be realistic and objective about competition.
    - Cite external market facts with [n].
    - NO em dashes.

    Web Sources: {citations}
    """

    response = structured_llm.invoke(prompt)
    return {"sections": {"section4": response}}
