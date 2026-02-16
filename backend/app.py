from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import StreamingResponse
import tempfile
import json
from graph.research_graph import build
from tools.pdf_reader import load_pdf
from tools.export_docx import export_docx
from tools.export_pdf import export_pdf

app = FastAPI(title="Account Research Platform")
graph = build()

@app.post("/research")
async def run_research(target_company: str = Form(...), annual_report: UploadFile = None):
    # Process PDF logic remains same...
    state = {"target_company": target_company, "sections": {}}

    async def stream():
        # Prevent timeout with initial pulse
        yield json.dumps({"type": "status", "message": "Parallel Agents Dispatched"}) + "\n"
        
        async for event in graph.astream(state):
            for node, output in event.items():
                yield json.dumps({"type": "update", "node": node, "data": output}) + "\n"
        
        yield json.dumps({"type": "complete"}) + "\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
    async def stream():
        yield json.dumps({"type": "status", "message": "Starting research"}) + "\n"
        for step in graph.stream(state):
            if "section" in step:
                yield json.dumps({"type": "section", "data": step}) + "\n"
            if "citations" in step:
                yield json.dumps({"type": "citations", "data": step}) + "\n"
        yield json.dumps({"type": "complete"}) + "\n"

    return StreamingResponse(stream(), media_type="text/event-stream")

@app.post("/export/docx")
def export_docx_api(sections: dict):
    path = export_docx(sections)
    return {"file": path}

@app.post("/export/pdf")
def export_pdf_api(sections: dict):
    path = export_pdf(sections)
    return {"file": path}
