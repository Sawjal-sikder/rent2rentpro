from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer
) #type: ignore
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle #type: ignore
from reportlab.lib.pagesizes import letter #type: ignore
from reportlab.lib.enums import TA_CENTER #type: ignore
import os, time


def generate_pdf(data):
    filename = f"contact_{int(time.time())}.pdf"
    file_path = f"media/contracts/{filename}"
    os.makedirs("media/contracts", exist_ok=True)

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    story = []

    # 🔹 Title
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=20,
        bold=True
    )

    story.append(Paragraph("RENTAL AGREEMENT", title_style))
    story.append(Spacer(1, 12))

    # 🔹 Intro Paragraph
    intro = f"""
    This Rental Agreement is made between <b>{data['landlord_name']}</b>,
    residing at <b>{data['landlord_address']}</b> (hereinafter referred to as
    <b>“Landlord”</b>) and <b>{data['tenant_name']}</b>, residing at
    <b>{data['tenant_address']}</b> (hereinafter referred to as <b>“Tenant”</b>).
    """
    story.append(Paragraph(intro, styles["Normal"]))
    story.append(Spacer(1, 15))

    # 🔹 Property Details Section
    story.append(Paragraph("<b>1. Property Details</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    property_text = f"""
    The Landlord agrees to rent the property located at
    <b>{data['property_address']}</b>.
    The property contains <b>{data['property_room_count']}</b> rooms and is
    {"furnished" if data['property_is_furnished'] else "not furnished"}.
    """
    story.append(Paragraph(property_text, styles["Normal"]))
    story.append(Spacer(1, 15))

    # 🔹 Rent Details
    story.append(Paragraph("<b>2. Rent & Payment</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    rent_text = f"""
    The Tenant agrees to pay a monthly rent of <b>{data['rent_amount']} EUR</b>.
    The rent type is <b>{data['rent_type']}</b>.
    A security deposit of <b>{data['rent_security_deposit']} EUR</b> is required.
    """
    story.append(Paragraph(rent_text, styles["Normal"]))
    story.append(Spacer(1, 15))

    # 🔹 Contract Duration
    story.append(Paragraph("<b>3. Contract Duration</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    duration_text = f"""
    This agreement begins on <b>{data['rent_start_date']}</b> and shall continue
    for <b>{data['rent_contract_duration_months']}</b> months.
    """
    story.append(Paragraph(duration_text, styles["Normal"]))
    story.append(Spacer(1, 20))

    # 🔹 Signatures
    story.append(Paragraph("<b>Landlord Signature:</b> _______________________", styles["Normal"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Tenant Signature:</b> _______________________", styles["Normal"]))

    # Build PDF
    doc.build(story)

    return file_path


















































# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from datetime import datetime
# import io
# import os
# import time

# def generate_pdf(data):
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer, pagesize=letter)
#     p.setFont("Helvetica", 12)

#     y = 750
#     for key, value in data.items():
#         p.drawString(50, y, f"{key}: {value}")
#         y -= 20

#     p.save()
#     buffer.seek(0)

#     filename = f"contact_{int(time.time())}.pdf"
#     file_path = f"media/contracts/{filename}"

#     os.makedirs("media/contracts", exist_ok=True)

#     with open(file_path, "wb") as f:
#         f.write(buffer.read())

#     return file_path
