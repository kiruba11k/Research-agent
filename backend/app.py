from fastapi import FastAPI, UploadFile, Form
import tempfile

from graph.research_graph import build
from tools.pdf_reader import load_pdf
from tools.export_docx import export_docx
from tools.export_pdf import export_pdf

app = FastAPI(title="Account Research Platform")
graph = build()

@app.post("/research")
async def run_research(
    target_company: str = Form(...),
    annual_report: UploadFile = None
):
    pdf_text = ""
    if annual_report:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await annual_report.read())
            pdf_text = load_pdf(tmp.name)

    state = {
        "target_company": target_company,
        "annual_report": pdf_text
    }

    result = graph.invoke(state)
    return result


@app.post("/export/docx")
def export_docx_api(sections: dict):
    path = export_docx(sections)
    return {"file": path}


@app.post("/export/pdf")
def export_pdf_api(sections: dict):
    path = export_pdf(sections)
    return {"file": path}
