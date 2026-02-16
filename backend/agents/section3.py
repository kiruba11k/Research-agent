from agents.base_model import llm
from tools.web_search import web_search
from tools.citations import normalize_sources
from models.schemas import SectionOutput

def run(state: dict):
    company = state['target_company']
    # 1. Technical stack and vendor search
    query = f"Technology stack, core banking platforms, IT vendors, and digital transformation of {company}"
    results = web_search(query)
    citations = normalize_sources(results.get("sources", []))

    structured_llm = llm.with_structured_output(SectionOutput)
    
    prompt = f"""
    Write Section 3: Account Technology Landscape for {company}.
    
    Focus:
    - Core infrastructure and digital channels (mobile/online).
    - Known technology vendors (e.g., AWS, Azure, Finastra, FIS).
    - Recent IT investments or leadership signals.

    Rules:
    - Group related technologies logically.
    - Cite claims with [n].
    - NO em dashes.
    - Avoid marketing fluff; focus on operational facts.

    Web Sources: {citations}
    """

    response = structured_llm.invoke(prompt)
    return {"sections": {"section3": response}}
