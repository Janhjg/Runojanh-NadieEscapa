import os
from io import BytesIO
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from datetime import datetime

def draw_background_and_stamp(canvas, doc):
    # 1. Fondo de papel antiguo (beige muy suave)
    canvas.saveState()
    canvas.setFillColorRGB(0.95, 0.92, 0.88)
    canvas.rect(0, 0, LETTER[0], LETTER[1], fill=1)
    
    # 2. Líneas de ruido de "escáner" (opcional, sutiles)
    canvas.setStrokeColorRGB(0.9, 0.88, 0.85)
    canvas.setLineWidth(0.5)
    for i in range(0, int(LETTER[1]), 50):
        canvas.line(0, i, LETTER[0], i)

    # 3. Sello de Confidencialidad Rotado
    canvas.rotate(45)
    canvas.setFont("Courier-Bold", 60)
    canvas.setFillColorRGB(0.8, 0.2, 0.2, alpha=0.15) # Rojo pálido semitransparente
    canvas.drawCentredString(LETTER[0] / 1.5, LETTER[1] / 6, "CONFIDENCIAL")
    canvas.restoreState()

def generate_case_pdf(case_data: dict):
    """
    Genera un PDF estilizado como un expediente policial antiguo de Los Ángeles.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=LETTER, 
        rightMargin=72, 
        leftMargin=72, 
        topMargin=72, 
        bottomMargin=18
    )
    
    styles = getSampleStyleSheet()
    
    # Estilo de máquina de escribir
    typewriter_style = ParagraphStyle(
        'Typewriter',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=11,
        leading=14,
        spaceAfter=12
    )
    
    typewriter_bold = ParagraphStyle(
        'TypewriterBold',
        parent=typewriter_style,
        fontName='Courier-Bold',
        fontSize=12,
    )

    header_style = ParagraphStyle(
        'PoliceHeader',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=18,
        alignment=1, # Center
        spaceAfter=5
    )
    
    subtitled_style = ParagraphStyle(
        'Subtitle',
        parent=typewriter_style,
        fontSize=10,
        alignment=1,
        textColor=colors.grey
    )

    elements = []

    # 1. Cabecera Institucional
    elements.append(Paragraph("LOS ANGELES POLICE DEPARTMENT", header_style))
    elements.append(Paragraph("CENTRAL OPERATIONS - DIVISION NARRATIVA", typewriter_style))
    elements.append(Paragraph("--------------------------------------------------", typewriter_style))
    elements.append(Paragraph(f"FECHA DE REPORTE: {datetime.now().strftime('%d/%m/%Y %H:%M')}", typewriter_style))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Sello de Clasificación
    elements.append(Paragraph("<font color='red' size='14'><b>[ CLASIFICADO - NIVEL 4 ]</b></font>", typewriter_style))
    elements.append(Spacer(1, 0.3 * inch))

    # 2. Información del Sujeto/Caso
    elements.append(Paragraph("DETALLES DEL EXPEDIENTE:", typewriter_bold))
    
    # Tabla de datos con estilo retro
    datos_tabla = [
        ["ID EXPEDIENTE", case_data.get("id", "N/A")],
        ["FECHA DEL CRIMEN", case_data.get("DATE OCC", case_data.get("DATE_OCC", "N/A"))],
        ["ÁREA / DISTRITO", case_data.get("AREA NAME", case_data.get("AREA_NAME", "N/A"))],
        ["DESCRIPCIÓN", case_data.get("Crm Cd Desc", case_data.get("Crm_Cd_Desc", "N/A"))],
        ["PREDICCIÓN ARRESTO", "INVESTIGACIÓN CERRADA" if case_data.get("prediccion", {}).get("clase_predicha") == "Arrestado" else "EN CURSO / SIN ARRESTO"],
    ]
    
    t = Table(datos_tabla, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Courier'),
        ('GRID', (0,0), (-1,-1), 0.7, colors.black),
        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.4 * inch))

    # 3. Crónica Noir (El cuerpo del informe)
    elements.append(Paragraph("CRÓNICA DE LOS HECHOS (TRANSCRIPCIÓN):", typewriter_bold))
    elements.append(Paragraph("-----------------------------------------", typewriter_style))
    cronica = case_data.get("cronica", "No hay narrativa disponible para este caso.")
    elements.append(Paragraph(cronica.replace("\n", "<br/>"), typewriter_style))

    # 4. Footer de Seguridad
    elements.append(Spacer(1, 0.6 * inch))
    elements.append(Paragraph("________________________________", typewriter_style))
    elements.append(Paragraph("Firma del Detective a cargo", typewriter_style))
    elements.append(Paragraph("Runojanh Criminal Analysis · Los Angeles District", subtitled_style))

    # Construir con el fondo y sello
    doc.build(elements, onFirstPage=draw_background_and_stamp, onLaterPages=draw_background_and_stamp)
    
    pdf_value = buffer.getvalue()
    buffer.close()
    return pdf_value
