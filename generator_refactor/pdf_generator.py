"""Generación de PDFs para rúbricas y cronograma."""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.utils import ImageReader

from generator_refactor.writer import _win_long, ensure_directory

AZUL       = colors.HexColor("#002E62")
AMARILLO   = colors.HexColor("#FDC82C")
GRIS_CLARO = colors.HexColor("#F1F5F9")
GRIS_BORDE = colors.HexColor("#CBD5E1")
BLANCO     = colors.white
NEGRO      = colors.HexColor("#0F172A")
GRIS_TEXT  = colors.HexColor("#334155")


def _styles():
    base = getSampleStyleSheet()
    titulo = ParagraphStyle(
        "titulo", parent=base["Normal"],
        fontSize=14, textColor=AZUL, fontName="Helvetica-Bold",
        spaceAfter=4, leading=18,
    )
    subtitulo = ParagraphStyle(
        "subtitulo", parent=base["Normal"],
        fontSize=10, textColor=GRIS_TEXT, fontName="Helvetica",
        spaceAfter=8,
    )
    celda = ParagraphStyle(
        "celda", parent=base["Normal"],
        fontSize=8, textColor=NEGRO, fontName="Helvetica",
        leading=11, wordWrap="LTR",
    )
    celda_header = ParagraphStyle(
        "celda_header", parent=base["Normal"],
        fontSize=8, textColor=BLANCO, fontName="Helvetica-Bold",
        leading=11,
    )
    return titulo, subtitulo, celda, celda_header


def _header_footer(canvas, doc, course_name, section_title):
    canvas.saveState()
    w, h = doc.pagesize
    # Header bar (más grueso)
    header_height = 52  # px, más grueso
    canvas.setFillColor(AZUL)
    canvas.rect(0, h - header_height, w, header_height, fill=1, stroke=0)
    # Logo a la derecha
    logo_path = os.path.join(os.path.dirname(__file__), "UNADECA_Logo_Virtual_Oficial-H.png")
    logo_drawn = False
    try:
        logo = ImageReader(logo_path)
        logo_height = 36  # px (más grande)
        logo_width = 120  # px (ajustar según proporción real)
        # Ubicar el logo a la derecha, dejando margen
        canvas.drawImage(logo, w - logo_width - 1.1 * cm, h - header_height + (header_height - logo_height) / 2, width=logo_width, height=logo_height, mask='auto', preserveAspectRatio=True)
        logo_drawn = True
    except Exception as e:
        pass
    # Nombre del curso alineado a la izquierda, centrado verticalmente
    canvas.setFillColor(BLANCO)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawString(1.5 * cm, h - header_height / 2 + 2, course_name)
    # Footer
    canvas.setFillColor(GRIS_TEXT)
    canvas.setFont("Helvetica", 7)
    canvas.drawCentredString(w / 2, 0.6 * cm, f"Página {doc.page}")
    canvas.restoreState()


def generate_rubrica_pdf(rubrica_title, table_obj, out_path, course_name):
    """Genera un PDF para una rúbrica a partir de su tabla DOCX."""
    titulo_s, subtitulo_s, celda_s, header_s = _styles()

    doc = SimpleDocTemplate(
        _win_long(out_path),
        pagesize=landscape(A4),
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=1.8 * cm, bottomMargin=1.2 * cm,
    )

    story = [
        Spacer(1, 0.3 * cm),
        Paragraph(rubrica_title, titulo_s),
        HRFlowable(width="100%", thickness=2, color=AMARILLO, spaceAfter=8),
    ]

    if table_obj is not None:
        rows = table_obj.rows
        data = []
        for r_idx, row in enumerate(rows):
            data_row = []
            for cell in row.cells:
                txt = cell.text.strip().replace("\n", "<br/>")
                style = header_s if r_idx == 0 else celda_s
                data_row.append(Paragraph(txt, style))
            data.append(data_row)

        if data:
            col_count = len(data[0])
            page_w = landscape(A4)[0] - 3 * cm
            col_w = page_w / col_count

            tbl = Table(data, colWidths=[col_w] * col_count, repeatRows=1)
            tbl.setStyle(TableStyle([
                # Encabezado
                ("BACKGROUND",   (0, 0), (-1, 0), AZUL),
                ("TEXTCOLOR",    (0, 0), (-1, 0), BLANCO),
                ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE",     (0, 0), (-1, 0), 8),
                # Cuerpo
                ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE",     (0, 1), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLANCO, GRIS_CLARO]),
                # Bordes
                ("GRID",         (0, 0), (-1, -1), 0.4, GRIS_BORDE),
                ("VALIGN",       (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING",   (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
                ("LEFTPADDING",  (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(tbl)
    else:
        story.append(Paragraph("Tabla no disponible en el documento.", celda_s))

    doc.build(
        story,
        onFirstPage=lambda c, d: _header_footer(c, d, course_name, None),
        onLaterPages=lambda c, d: _header_footer(c, d, course_name, None),
    )


def generate_cronograma_pdf(weeks_map, out_path, course_name):
    """Genera un PDF del cronograma completo."""
    titulo_s, subtitulo_s, celda_s, header_s = _styles()

    doc = SimpleDocTemplate(
        _win_long(out_path),
        pagesize=landscape(A4),
        leftMargin=(1.0 if sum(len(u) for u in weeks_map.values()) > 14 else 1.5) * cm,
        rightMargin=(1.0 if sum(len(u) for u in weeks_map.values()) > 14 else 1.5) * cm,
        topMargin=1.8 * cm,
        bottomMargin=(1.0 if sum(len(u) for u in weeks_map.values()) > 14 else 1.2) * cm,
    )

    story = [
        Spacer(1, 0.3 * cm),
        Paragraph("Cronograma del curso", titulo_s),
        HRFlowable(width="100%", thickness=2, color=AMARILLO, spaceAfter=8),
    ]

    headers = ["Semana(s)", "Unidad / Tema", "Resultado de aprendizaje", "Contenidos", "Bibliografía"]
    header_row = [Paragraph(h, header_s) for h in headers]
    data = [header_row]

    from generator_refactor.schedule_parser import format_week_range
    for weeks, units in weeks_map.items():
        week_label = format_week_range(weeks)
        for unit in units:
            row = [
                Paragraph(week_label, celda_s),
                Paragraph((unit.get("unit") or "").replace("\n", "<br/>"), celda_s),
                Paragraph((unit.get("resultado") or "").replace("\n", "<br/>"), celda_s),
                Paragraph((unit.get("contenidos") or "").replace("\n", "<br/>"), celda_s),
                Paragraph((unit.get("bibliografia") or "").replace("\n", "<br/>"), celda_s),
            ]
            data.append(row)

    if len(data) > 1:
        page_w = landscape(A4)[0] - 3 * cm
        col_widths = [
            page_w * 0.09,
            page_w * 0.18,
            page_w * 0.22,
            page_w * 0.28,
            page_w * 0.23,
        ]
        tbl = Table(data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, 0), AZUL),
            ("TEXTCOLOR",    (0, 0), (-1, 0), BLANCO),
            ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, 0), 8),
            ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE",     (0, 1), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLANCO, GRIS_CLARO]),
            ("GRID",         (0, 0), (-1, -1), 0.4, GRIS_BORDE),
            ("VALIGN",       (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",   (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
            ("LEFTPADDING",  (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(tbl)
    else:
        story.append(Paragraph("No se encontraron datos de cronograma.", celda_s))

    doc.build(
        story,
        onFirstPage=lambda c, d: _header_footer(c, d, course_name, None),
        onLaterPages=lambda c, d: _header_footer(c, d, course_name, None),
    )


def generate_pdfs_for_class(class_name, doc, paragraphs, weeks_map, class_dir):
    """Genera todos los PDFs de rúbricas y cronograma para una clase."""
    from generator_refactor.docx_reader import extract_rubricas_with_tables

    pdf_dir = os.path.join(class_dir, "Rubricas y Cronograma")
    ensure_directory(pdf_dir)

    # Cronograma
    if weeks_map:
        cron_path = os.path.join(pdf_dir, "Cronograma.pdf")
        try:
            generate_cronograma_pdf(weeks_map, cron_path, class_name)
        except Exception as e:
            print(f"    [PDF] Error en cronograma: {e}")

    # Rúbricas
    rubricas = extract_rubricas_with_tables(doc, paragraphs)
    for i, rubrica in enumerate(rubricas, start=1):
        safe_title = rubrica['title'][:80].replace("/", "-").replace("\\", "-")
        pdf_path = os.path.join(pdf_dir, f"{safe_title}.pdf")
        try:
            generate_rubrica_pdf(rubrica['title'], rubrica['table'], pdf_path, class_name)
        except Exception as e:
            print(f"    [PDF] Error en rúbrica '{rubrica['title']}': {e}")
