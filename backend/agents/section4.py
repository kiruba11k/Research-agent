from agents.base_model import llm
from tools.web_search import web_search
from tools.citations import normalize_sources

def run(state):
    """
    Section 4: Speridian Account Relationship and Competitive Context
    Focus:
    - Existing vendors and partners inside the account
    - Competitors to Speridian
    - Buying center and stakeholder signals
    - Where Speridian can and cannot realistically fit
    """

    query = f"""
    Vendors, partners, service providers, and competitive landscape
    associated with {state['target_company']}.
    Include payments partners, technology vendors, consulting firms,
    and ecosystem memberships.
    """

    search_results = web_search(query)
    citations = normalize_sources(search_results["sources"])

    prompt = f"""
    Write Section 4: Speridian Account Relationship and Competitive Context.

    Rules:
    - Cite all target-company and market claims using [n]
    - Do not cite Speridian capabilities
    - No em dashes
    - Be realistic and grounded
    - Clearly separate:
        1. Existing vendors and partners
        2. Competitive context
        3. Practical implications for Speridian

    Sources:
    {citations}
    """

    content = llm.invoke(prompt).content

    confidence_prompt = f"""
    Score confidence from 0 to 1 based on:
    - Visibility of vendors and partners
    - Public disclosures
    - Source reliability
    Return only a number.
    """

    confidence = float(llm.invoke(confidence_prompt).content.strip())

    return {
        "section4": {
            "content": content,
            "citations": citations,
            "confidence": confidence
        }
    }
