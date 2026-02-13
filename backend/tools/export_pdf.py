from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def export_pdf(sections, path="report.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path)
    story = []

    for name, data in sections.items():
        story.append(Paragraph(name, styles["Heading1"]))
        story.append(Paragraph(data["content"], styles["Normal"]))

        story.append(Paragraph("References", styles["Heading2"]))
        for c in data["citations"]:
            story.append(
                Paragraph(
                    f"[{c['id']}] <a href='{c['url']}'>{c['title']}</a>",
                    styles["Normal"]
                )
            )

        story.append(
            Paragraph(
                f"Confidence Score: {round(data['confidence']*100)}%",
                styles["Italic"]
            )
        )

    doc.build(story)
    return path
