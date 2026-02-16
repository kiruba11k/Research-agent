import os
import operator
import json
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

# --- REFRESHED CORS MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with your frontend URL (e.g. https://your-site.com)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

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
# Updated to stable model version to avoid 404 errors
llm = ChatAnthropic(
    model="claude-3-5-sonnet-latest", 
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)
search_tool = TavilySearchResults(
    max_results=5, 
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

# --- GRAPH NODES ---
def planner(state: OverallState):
    sections = [
        "Section 1: Account Business Overview (Financials/FDIC)",
        "Section 2: Key Business Initiatives (Strategy/Growth)",
        "Section 3: Account Tech Landscape (Digital/Vendors)",
        "Section 4: Relationship & Stakeholders (Executives)",
        "Section 5: Strategic Next Steps (Opportunities)"
    ]
    # This triggers the parallel 'researcher' instances
    return [Send("researcher", {"section_name": s, "target_company": state['target_company']}) for s in sections]

def researcher(state: SectionState):
    query = f"{state['target_company']} {state['section_name']} news 2024 2025"
    search_results = search_tool.invoke(query)
    
    prompt = f"""Summarize research for {state['section_name']} regarding {state['target_company']}.
    Search Results: {search_results}
    Format: Use clean bullet points. No emojis. Professional tone."""
    
    response = llm.invoke(prompt)
    return {"research_data": [{"section": state['section_name'], "content": response.content}]}

def writer(state: OverallState):
    full_text = f"# Strategic Report: {state['target_company']}\n\n"
    # Sort by section name to keep document order
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

# Correcting the parallel routing logic
builder.add_conditional_edges("planner", lambda x: x)
builder.add_edge("researcher", "writer")
builder.add_edge("writer", END)

graph = builder.compile()

# --- API ENDPOINTS ---
reports_db = {}

@app.post("/research")
async def generate_report(target: str, mine: str):
    try:
        inputs = {"target_company": target, "my_company": mine, "research_data": []}
        result = graph.invoke(inputs)
        
        report_id = target.replace(" ", "_").lower()
        reports_db[report_id] = result['final_report']
        
        return {"id": report_id, "report": result['final_report']}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{report_id}")
async def download_pdf(report_id: str):
    content = reports_db.get(report_id)
    if not content:
        raise HTTPException(status_code=404, detail="Report not found")
    
    pdf_path = f"/tmp/{report_id}.pdf" # Use /tmp for Render environments
    HTML(string=markdown2.markdown(content)).write_pdf(pdf_path)
    return FileResponse(pdf_path, filename=f"Strategy_Report_{report_id}.pdf")
