from agents.base_model import llm
from tools.web_search import web_search
from tools.citations import normalize_sources

def run(state):
    """
    Section 3: Account Technology Landscape
    Focus:
    - Core banking, digital channels, payments, data, security
    - Named vendors and platforms where publicly visible
    - Operating and delivery implications
    """

    query = f"""
    Technology platforms, digital banking tools, payment systems,
    vendors, and IT operating model used by {state['target_company']}.
    Include online banking, mobile, treasury, payments, cards, security,
    and technology leadership signals.
    """

    search_results = web_search(query)
    citations = normalize_sources(search_results["sources"])

    prompt = f"""
    Write Section 3: Account Technology Landscape.

    Rules:
    - Cite every factual claim using [n]
    - Use only information supported by sources
    - No em dashes
    - Executive tone, not marketing language
    - Group related technologies together
    - Explain operational implications where relevant
    - Do not speculate beyond public signals

    Sources:
    {citations}
    """

    content = llm.invoke(prompt).content

    confidence_prompt = f"""
    Based on the credibility of sources, consistency across sources,
    and clarity of public disclosures, score confidence from 0 to 1.
    Return only a number.
    """

    confidence = float(llm.invoke(confidence_prompt).content.strip())

    return {
        "section3": {
            "content": content,
            "citations": citations,
            "confidence": confidence
        }
    }
