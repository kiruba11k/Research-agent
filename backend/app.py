from fastapi import FastAPI, UploadFile, Form
import tempfile
from graph.research_graph import build
from tools.pdf_reader import load_pdf
from tools.export_docx import export_docx
from tools.export_pdf import export_pdf

app = FastAPI()
graph = build()

@app.post("/research")
async def research(
    target_company: str = Form(...),
    annual_report: UploadFile = None
):
    text = ""
    if annual_report:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(await annual_report.read())
            text = load_pdf(f.name)

    state = {
        "target_company": target_company,
        "annual_report": text
    }

    result = graph.invoke(state)
    return result

@app.post("/export/docx")
def export_docx_api(sections: dict):
    return {"file": export_docx(sections)}

@app.post("/export/pdf")
def export_pdf_api(sections: dict):
    return {"file": export_pdf(sections)}
