import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def generate_pdf_report(session_id, data, session_folder):
    pdf_filename = os.path.join(session_folder, f"Work_Report_{session_id}.pdf")
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"Work Activity Audit Report", styles['Heading1']))
    elements.append(Paragraph(f"Session: {session_id}", styles['Normal']))
    elements.append(Spacer(1, 0.3 * inch))

    for timestamp, app, event, img_path in data:
        text = f"<b>Time:</b> {timestamp}<br/><b>App:</b> {app}<br/><b>Event:</b> {event}"
        elements.append(Paragraph(text, styles['Normal']))
        elements.append(Spacer(1, 0.1 * inch))

        if img_path and os.path.exists(img_path):
            try:
                img = Image(img_path, width=6*inch, height=3.4*inch)
                img.hAlign = 'CENTER'
                elements.append(img)
            except:
                elements.append(Paragraph("[Image Error]", styles['Normal']))
        
        elements.append(Spacer(1, 0.4 * inch))

    doc.build(elements)
    return pdf_filename