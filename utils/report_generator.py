# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# import os

# def generate_pdf_report(data: dict, filename: str = "report.pdf"):
#     os.makedirs("reports", exist_ok=True)
#     filepath = os.path.join("reports", filename)
#     c = canvas.Canvas(filepath, pagesize=A4)
#     c.setFont("Helvetica", 12)
    
#     y = 800
#     c.drawString(50, y, "AI Resume Analysis Report")
#     y -= 30
#     for key, value in data.items():
#         c.drawString(50, y, f"{key}: {value}")
#         y -= 20
#         if y < 100:
#             c.showPage()
#             y = 800
    
#     c.save()
# #     return filepath
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# import os

# def format_value(value):
#     if isinstance(value, list):
#         if all(isinstance(item, str) for item in value):
#             return ", ".join(value)
#         elif all(isinstance(item, dict) for item in value):
#             return "; ".join(", ".join(f"{k}: {v}" for k, v in d.items()) for d in value)
#         else:
#             return str(value)
#     elif isinstance(value, dict):
#         return ", ".join(f"{k}: {v}" for k, v in value.items())
#     else:
#         return str(value)

# def generate_pdf_report(data: dict, filename: str = "report.pdf"):
#     os.makedirs("reports", exist_ok=True)
#     filepath = os.path.join("reports", filename)
#     c = canvas.Canvas(filepath, pagesize=A4)
#     c.setFont("Helvetica", 12)

#     y = 800
#     c.drawString(50, y, "AI Resume Analysis Report")
#     y -= 30

#     for key, value in data.items():
#         formatted_value = format_value(value)
#         lines = formatted_value.split("\n")

#         for line in lines:
#             if y < 50:
#                 c.showPage()
#                 c.setFont("Helvetica", 12)
#                 y = 800
#             c.drawString(50, y, f"{key}: {line}" if line == lines[0] else f"    {line}")
#             y -= 20

#     c.save()
#     return filepath
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

def format_value(value):
    if isinstance(value, list):
        if all(isinstance(item, str) for item in value):
            return "\n".join(f"- {item}" for item in value)
        elif all(isinstance(item, dict) for item in value):
            return "\n".join(
                "; ".join(f"{k}: {v}" for k, v in d.items()) for d in value
            )
        else:
            return str(value)
    elif isinstance(value, dict):
        return "\n".join(f"{k}: {v}" for k, v in value.items())
    else:
        return str(value)

def generate_pdf_report(data: dict, filename: str = "report.pdf"):
    os.makedirs("reports", exist_ok=True)
    filepath = os.path.join("reports", filename)
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 60, "AI Resume Analysis Report")
    c.setLineWidth(1)
    c.setStrokeColor(colors.grey)
    c.line(50, height - 70, width - 50, height - 70)
    y = height - 100

    c.setFont("Helvetica", 12)
    page_num = 1

    for key, value in data.items():
        # Section header
        if y < 100:
            c.showPage()
            page_num += 1
            c.setFont("Helvetica-Bold", 20)
            c.drawCentredString(width / 2, height - 60, "AI Resume Analysis Report")
            c.setLineWidth(1)
            c.setStrokeColor(colors.grey)
            c.line(50, height - 70, width - 50, height - 70)
            y = height - 100
            c.setFont("Helvetica", 12)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"{key}:")
        y -= 22

        c.setFont("Helvetica", 12)
        formatted_value = format_value(value)
        lines = formatted_value.split("\n")
        for line in lines:
            if y < 70:
                c.showPage()
                page_num += 1
                c.setFont("Helvetica-Bold", 20)
                c.drawCentredString(width / 2, height - 60, "AI Resume Analysis Report")
                c.setLineWidth(1)
                c.setStrokeColor(colors.grey)
                c.line(50, height - 70, width - 50, height - 70)
                y = height - 100
                c.setFont("Helvetica", 12)
            c.drawString(70, y, line)
            y -= 18
        y -= 10  # Extra space between sections

    # Footer with page number
    for i in range(page_num):
        c.showPage()
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, 30, f"Page {i+1}")

    c.save()
    return filepath