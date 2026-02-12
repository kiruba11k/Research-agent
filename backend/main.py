import os
import operator
from typing import Annotated, List, TypedDict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from langgraph.constants import Send
import markdown2
from weasyprint import HTML

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- AGENT STATE DEFINITION ---
class SectionState(TypedDict):
    section_name: str
    target_company: str

class OverallState(TypedDict):
    target_company: str
    my_company: str
    research_data: Annotated[List[dict], operator.add]
    final_report: str

# --- MODELS & TOOLS ---
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", api_key=os.getenv("ANTHROPIC_API_KEY"))
search_tool = TavilySearchResults(max_results=5, api_key=os.getenv("TAVILY_API_KEY"))

# --- GRAPH NODES ---
def planner(state: OverallState):
    # These match your Word Document sections
    sections = [
        "Section 1: Account Business Overview (Financials/FDIC)",
        "Section 2: Key Business Initiatives (Strategy/Growth)",
        "Section 3: Account Tech Landscape (Digital/Vendors)",
        "Section 4: Relationship & Stakeholders (Executives)",
        "Section 5: Strategic Next Steps (Opportunities)"
    ]
    return [Send("researcher", {"section_name": s, "target_company": state['target_company']}) for s in sections]

def researcher(state: SectionState):
    # Real-time search for each specific section
    query = f"{state['target_company']} {state['section_name']} news 2024 2025"
    search_results = search_tool.invoke(query)
    
    prompt = f"""Summarize research for {state['section_name']} regarding {state['target_company']}.
    Search Results: {search_results}
    Format: Use clean bullet points. No emojis. Professional tone."""
    
    response = llm.invoke(prompt)
    return {"research_data": [{"section": state['section_name'], "content": response.content}]}

def writer(state: OverallState):
    # Aggregates parallel results into one document
    full_text = f"# Strategic Report: {state['target_company']}\n\n"
    sorted_sections = sorted(state['research_data'], key=lambda x: x['section'])
    for sec in sorted_sections:
        full_text += f"## {sec['section']}\n{sec['content']}\n\n"
    return {"final_report": full_text}

# --- BUILD GRAPH ---
builder = StateGraph(OverallState)
builder.add_node("planner", planner)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.set_entry_point("planner")
builder.add_conditional_edges("planner", lambda x: x)
builder.add_edge("researcher", "writer")
builder.add_edge("writer", END)
graph = builder.compile()

# --- API ENDPOINTS ---
reports_db = {}

@app.post("/generate")
async def generate_report(target: str, mine: str):
    inputs = {"target_company": target, "my_company": mine, "research_data": []}
    result = graph.invoke(inputs)
    report_id = target.replace(" ", "_").lower()
    reports_db[report_id] = result['final_report']
    return {"id": report_id, "report": result['final_report']}

@app.get("/download/{report_id}")
async def download_pdf(report_id: str):
    content = reports_db.get(report_id)
    if not content: raise HTTPException(404)
    pdf_path = f"{report_id}.pdf"
    HTML(string=markdown2.markdown(content)).write_pdf(pdf_path)
    return FileResponse(pdf_path, filename=f"Strategy_Report_{report_id}.pdf")
