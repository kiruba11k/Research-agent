import os
import operator
from typing import Annotated, List, TypedDict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from langgraph.types import Send
import markdown2
from weasyprint import HTML

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LANGGRAPH STATE ---
class SectionState(TypedDict):
    section_name: str
    target_company: str

class OverallState(TypedDict):
    target_company: str
    my_company: str
    aggregated_research: Annotated[List[dict], operator.add]
    final_report: str

# --- NODES ---
def planner_node(state: OverallState):
    sections = [
        "1. Account Business Overview",
        "2. Key Business Initiatives",
        "3. Account Tech Landscape",
        "4. Relationship & Stakeholders",
        "5. Strategic Next Steps"
    ]
    return [Send("research_worker", {"section_name": s, "target_company": state['target_company']}) for s in sections]

def research_worker_node(state: SectionState):
    # Simulated search logic (Integrate TavilySearchResults here for live data)
    summary = f"### {state['section_name']}\nDetailed research findings for {state['target_company']}..."
    return {"aggregated_research": [{"section": state['section_name'], "content": summary}]}

def writer_node(state: OverallState):
    report = f"# Strategy Report: {state['target_company']}\n\n"
    for item in sorted(state['aggregated_research'], key=lambda x: x['section']):
        report += f"{item['content']}\n\n"
    return {"final_report": report}

# --- GRAPH ---
workflow = StateGraph(OverallState)
workflow.add_node("planner", planner_node)
workflow.add_node("research_worker", research_worker_node)
workflow.add_node("writer", writer_node)
workflow.set_entry_point("planner")
workflow.add_conditional_edges("planner", lambda x: x)
workflow.add_edge("research_worker", "writer")
workflow.add_edge("writer", END)
app_graph = workflow.compile()

# --- ROUTES ---
DB = {}

@app.post("/research")
async def start_research(target: str, mine: str):
    result = app_graph.invoke({"target_company": target, "my_company": mine, "aggregated_research": []})
    run_id = target.replace(" ", "_")
    DB[run_id] = result['final_report']
    return {"run_id": run_id, "report": result['final_report']}

@app.get("/export/pdf/{run_id}")
async def export_pdf(run_id: str):
    content = DB.get(run_id, "No data")
    html_content = markdown2.markdown(content)
    pdf_file = f"{run_id}.pdf"
    HTML(string=html_content).write_pdf(pdf_file)
    return FileResponse(pdf_file, filename=pdf_file)
