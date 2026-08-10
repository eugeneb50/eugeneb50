#!/usr/bin/env python3
"""Generate Red de Vida San Quintín proposal PDF."""
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image, ListFlowable, ListItem
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, String, Rect, Line

# Colors
NAVY = colors.HexColor("#0e2a47")
NAVY2 = colors.HexColor("#16395f")
TEAL = colors.HexColor("#15a39a")
TEAL_D = colors.HexColor("#0e7c75")
TEAL_L = colors.HexColor("#e7f4f2")
SAND = colors.HexColor("#fdf8ef")
ACCENT = colors.HexColor("#f59e0b")
MUTED = colors.HexColor("#5b6b7b")
LINE = colors.HexColor("#e3e9ef")
LIGHT_BG = colors.HexColor("#f8fafc")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
try:
    pdfmetrics.registerFont(TTFont("DJ", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DJ-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DJ-I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")))
    FONT="DJ"
    FONTB="DJ-B"
    FONTI="DJ-I"
except:
    FONT="Helvetica"
    FONTB="Helvetica-Bold"
    FONTI="Helvetica-Oblique"

styles = getSampleStyleSheet()

s_title = ParagraphStyle('Title2', parent=styles['Title'], fontName=FONTB, fontSize=26, leading=28, textColor=NAVY, alignment=TA_LEFT, spaceAfter=6)
s_subtitle = ParagraphStyle('Subtitle2', parent=styles['Normal'], fontName=FONT, fontSize=9, leading=12, textColor=MUTED, alignment=TA_LEFT, spaceAfter=4)
s_h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName=FONTB, fontSize=15, leading=18, textColor=NAVY, spaceBefore=18, spaceAfter=8, keepWithNext=True)
s_h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName=FONTB, fontSize=11, leading=14, textColor=TEAL_D, spaceBefore=12, spaceAfter=6, keepWithNext=True)
s_h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName=FONTB, fontSize=10, leading=13, textColor=NAVY2, spaceBefore=8, spaceAfter=4)
s_body = ParagraphStyle('Body', parent=styles['Normal'], fontName=FONT, fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=6)
s_bullet = ParagraphStyle('Bullet', parent=s_body, leftIndent=18, spaceAfter=3, bulletIndent=8)
s_caption = ParagraphStyle('Caption', parent=styles['Normal'], fontName=FONTI, fontSize=7, leading=9, textColor=MUTED, alignment=TA_CENTER, spaceAfter=8)
s_table_header = ParagraphStyle('TH', parent=styles['Normal'], fontName=FONTB, fontSize=7, leading=9, textColor=colors.white, alignment=TA_CENTER)
s_table_cell = ParagraphStyle('TC', parent=styles['Normal'], fontName=FONT, fontSize=7, leading=9, textColor=colors.HexColor("#1e293b"), alignment=TA_LEFT)
s_table_cell_center = ParagraphStyle('TCC', parent=s_table_cell, alignment=TA_CENTER)
s_kpi = ParagraphStyle('KPI', parent=styles['Normal'], fontName=FONTB, fontSize=16, leading=18, textColor=NAVY, alignment=TA_CENTER)
s_kpi_label = ParagraphStyle('KPIL', parent=styles['Normal'], fontName=FONTB, fontSize=6.5, leading=8, textColor=TEAL_D, alignment=TA_CENTER)

def header_footer(canvas, doc):
    canvas.saveState()
    # top bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, doc.pagesize[1]-38, doc.pagesize[0], 38, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont(FONTB, 7)
    canvas.drawString(36, doc.pagesize[1]-16, "RED DE VIDA  SAN QUINTÍN")
    canvas.setFont(FONT, 6)
    canvas.setFillColor(colors.HexColor("#bfe9e4"))
    canvas.drawString(36, doc.pagesize[1]-26, "Tejido de Ayuda Mutua por el Bienestar Animal y la Tierra  •  Municipio de San Quintín, BCN  •  Agosto 2026")
    canvas.setFont(FONT, 6)
    canvas.setFillColor(colors.white)
    canvas.drawRightString(doc.pagesize[0]-36, doc.pagesize[1]-16, "PROPUESTA INTEGRAL  •  CONFIDENCIAL - USO MUNICIPAL")
    canvas.setFont(FONT, 5)
    canvas.setFillColor(colors.HexColor("#8abdb7"))
    canvas.drawRightString(doc.pagesize[0]-36, doc.pagesize[1]-26, "CC BY-SA 4.0  •  eugene@serviceofothers.org")
    # footer line
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(36, 34, doc.pagesize[0]-36, 34)
    canvas.setFont(FONT, 6)
    canvas.setFillColor(MUTED)
    canvas.drawString(36, 24, "Red de Vida San Quintín  •  Esterilizar. Adoptar. Honrar. Regenerar.")
    canvas.drawRightString(doc.pagesize[0]-36, 24, f"Pág. {doc.page}")
    canvas.restoreState()

def hr():
    return HRFlowable(width="100%", thickness=0.6, color=LINE, spaceAfter=8, spaceBefore=8)

def badge(text, bg=TEAL, fg=colors.white):
    return Table([[Paragraph(f"<font color='{fg}'><b>{text}</b></font>", ParagraphStyle('b', parent=styles['Normal'], fontName=FONTB, fontSize=6, leading=7, textColor=fg, alignment=TA_CENTER))]],
                 colWidths=[None], style=TableStyle([
                     ('BACKGROUND', (0,0), (-1,-1), bg),
                     ('ROUNDEDCORNERS', [4,4,4,4]),
                     ('TOPPADDING', (0,0), (-1,-1), 4),
                     ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                     ('LEFTPADDING', (0,0), (-1,-1), 8),
                     ('RIGHTPADDING', (0,0), (-1,-1), 8),
                 ]))

def build():
    out = os.path.join(os.path.dirname(__file__), "Red-de-Vida-San-Quintin-Propuesta-Integral-2026.pdf")
    doc = SimpleDocTemplate(out, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=52, bottomMargin=40,
                            title="Red de Vida San Quintín - Propuesta Integral 2026",
                            author="Eugene L. Buchanan")
    story=[]
    # COVER
    # big title
    story.append(Spacer(1, 10))
    story.append(Paragraph("MUNICIPIO DE SAN QUINTÍN, BAJA CALIFORNIA", ParagraphStyle('eyeb', parent=styles['Normal'], fontName=FONTB, fontSize=7, leading=9, textColor=TEAL, alignment=TA_LEFT, spaceAfter=6)))
    story.append(Paragraph("Red de Vida<br/>San Quintín", ParagraphStyle('coverTitle', parent=s_title, fontSize=38, leading=38, textColor=NAVY, spaceAfter=4)))
    story.append(Paragraph("Tejido de Ayuda Mutua por el Bienestar Animal y la Tierra", ParagraphStyle('coverSub', parent=styles['Normal'], fontName=FONT, fontSize=12, leading=14, textColor=TEAL_D, spaceAfter=12)))
    story.append(HRFlowable(width="22%", thickness=3, color=TEAL, spaceAfter=12, spaceBefore=4, hAlign='LEFT'))
    story.append(Paragraph("Un estándar municipal replicable para México<br/><b>Esterilizar. Adoptar. Honrar. Regenerar.</b>", ParagraphStyle('coverLead', parent=styles['Normal'], fontName=FONT, fontSize=9.5, leading=13, textColor=MUTED, spaceAfter=14)))
    # cover kpi row
    kpi_data = [
        [Paragraph("<b>5</b> capas", s_kpi), Paragraph("<b>3,600</b> esteril.", s_kpi), Paragraph("<b>31 MXN</b>", s_kpi), Paragraph("<b>5.2 MDP</b>", s_kpi)],
        [Paragraph("tejido integral", s_kpi_label), Paragraph("por año", s_kpi_label), Paragraph("por habitante/año", s_kpi_label), Paragraph("arranque", s_kpi_label)],
    ]
    t = Table(kpi_data, colWidths=[1.6*inch]*4)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), TEAL_L),
        ('BOX', (0,0), (-1,-1), 0.6, LINE),
        ('INNERGRID', (0,0), (-1,-1), 0.4, LINE),
        ('ROUNDEDCORNERS', [8,8,8,8]),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    # cover info box
    info = [
        [Paragraph("<b>Proponente</b><br/>Eugene L. Buchanan<br/>San Quintín BCN / Apple Valley CA<br/>eugene@serviceofothers.org", s_body)],
        [Paragraph("<b>Co-diseño abierto con</b><br/>Huellitas de Amor SQ • Veterinarias voluntarias • Ejidos y ranchos del Valle • Jurisdicción Sanitaria #4 • Delegaciones municipales", s_body)],
        [Paragraph("<b>Fecha / Licencia</b><br/>10 de agosto de 2026 • v1.0<br/>CC BY-SA 4.0 — Cópiame, mejórame, comparte", s_body)],
    ]
    tt = Table([[info[0][0], info[1][0], info[2][0]]], colWidths=[2.0*inch, 2.4*inch, 2.0*inch])
    tt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.5, LINE),
        ('INNERGRID', (0,0), (-1,-1), 0.4, LINE),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tt)
    story.append(Spacer(1, 12))
    # resumen ejecutivo box
    story.append(Paragraph("RESUMEN EJECUTIVO — 60 SEGUNDOS", ParagraphStyle('resTitle', parent=styles['Normal'], fontName=FONTB, fontSize=7, leading=9, textColor=TEAL_D, spaceAfter=4)))
    story.append(Paragraph(
        "Cinco capas que se sostienen entre sí: <b>(1)</b> Vales para esterilizar gratis en tu veterinaria de confianza + <b>(2)</b> Quirófanos móviles que van al barrio + <b>(3)</b> Centro de Bienestar que recupera, no mata, y ofrece adopción + <b>(4)</b> Aquamación digna y ecológica (agua, no fuego) + <b>(5)</b> Bioliquidadora móvil que convierte mortalidad pecuaria y restos no reclamados en fertilizante líquido certificado para parques y ranchos. Todo con fondo común, promotoras de colonia, WhatsApp + papel, y tablero público. <b>Costo de arranque 5.2 MDP. Autosustentable 40% desde año 2 vía fertilizante, padrinazgos y ahorro en salud pública.</b>",
        ParagraphStyle('resBody', parent=s_body, fontSize=8.5, leading=12, borderColor=TEAL, borderWidth=0.6, borderPadding=(8,8,8), backColor=TEAL_L, spaceAfter=8)
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Lectura guiada: Gobierno → §9 Gobernanza. Veterinaria → §4 Vales. Rescatista → §5-6. Productor → §7-8. Tecnología → §10.", s_caption))
    story.append(Spacer(1, 8))
    # principios table
    story.append(Paragraph("Principios — cambio de paradigma", s_h2))
    princ = [
        [Paragraph("<b>Viejo paradigma</b>", s_table_header), Paragraph("<b>Nuevo estándar Red de Vida</b>", s_table_header)],
        [Paragraph("Perrera = captura y sacrificio a 72h", s_table_cell), Paragraph("Centro de Vida = resguardo, foto en 2h, difusión, salud, adopción", s_table_cell)],
        [Paragraph("Esterilización = campaña anual aislada", s_table_cell), Paragraph("Esterilización = red continua + vales + móviles", s_table_cell)],
        [Paragraph("Incineración / fosa común", s_table_cell), Paragraph("Aquamación (agua) + bioliquidación (fertilizante)", s_table_cell)],
        [Paragraph("Multa al vecino por perro en calle", s_table_cell), Paragraph("Promotora + vale + educación + registro", s_table_cell)],
        [Paragraph("Gasto municipal hundido", s_table_cell), Paragraph("Fondo común + valor del fertilizante + padrinazgos", s_table_cell)],
        [Paragraph("Trámite solo en palacio", s_table_cell), Paragraph("WhatsApp, papel en tienda/iglesia, app opcional", s_table_cell)],
    ]
    pt = Table(princ, colWidths=[2.6*inch, 4.0*inch])
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('GRID', (0,0), (-1,-1), 0.4, LINE),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(pt)
    story.append(Spacer(1, 8))
    story.append(Paragraph("Documento vivo v1.0 — 10 ago 2026. La versión interactiva con generador de vales y tablero está en <b>site/index.html</b> (preview en vivo).", s_caption))
    # TOC
    story.append(Paragraph("Índice", s_h1))
    toc_items = [
        "1. Contexto: por qué San Quintín puede liderar",
        "2. Arquitectura de 5 capas — cómo se sostienen",
        "3. Capa 1 — Vales Solidarios para Esterilización",
        "4. Capa 2 — Quirófanos de Barrio (Pop-Up Clinics)",
        "5. Capa 3 — Centro de Bienestar, Adopción y Reencuentro",
        "6. Capa 4 — Honra Final: Aquamación (Alkaline Hydrolysis)",
        "7. Capa 5 — Unidad Móvil de Bioliquidación y Ciclo de Fertilizante",
        "8. Gobernanza, marco legal y finanzas (5.2 MDP arranque)",
        "9. Tecnología: papel primero, app después",
        "10. Plan 0-24 meses + Métricas + Riesgos + Anexos (plantillas)",
    ]
    for i, it in enumerate(toc_items, 1):
        story.append(Paragraph(f"<b>{it}</b>", ParagraphStyle(f'toc{i}', parent=s_body, fontSize=8.5, leading=11, leftIndent=12, spaceAfter=2)))
    story.append(hr())
    story.append(Paragraph("Cómo leer esta propuesta: Si eres <b>gobierno</b> ve a §8. Si eres <b>veterinaria/o</b> a §3. Si eres <b>rescatista</b> a §4-5. Si eres <b>productor</b> a §7.", ParagraphStyle('howto', parent=s_body, fontSize=8, leading=11, textColor=TEAL_D, borderColor=TEAL, borderWidth=0.4, borderPadding=(6,6,6), backColor=colors.HexColor("#f0fdfa"))))
    # 1 Contexto
    story.append(Paragraph("1. Contexto: por qué San Quintín puede liderar", s_h1))
    story.append(Paragraph("1.1 Municipio joven, lienzo en blanco", s_h2))
    story.append(Paragraph(
        "San Quintín se constituyó como sexto municipio de Baja California el 27 de febrero de 2020. Con 32,883 km² es el más extenso del estado y con ~117 mil habitantes (Censo 2020) más población flotante agrícola, es el más disperso y rural. Heredó de Ensenada la carencia histórica: cero infraestructura municipal de control animal digna. La “perrera” nunca existió; el vacío lo llenan colectivos que operan desde casas particulares. El 4 de junio de 2026, <i>El Imparcial</i> documentó el reclamo de Huellitas de Amor SQ: “Necesitamos un Centro de Bienestar Animal, que malamente antes se le conocía como perrera, no tenemos aquí en San Quintín”. No piden más redadas. Piden resguardo, atención veterinaria, esterilización y adopción. Ese reclamo es mandato de diseño.",
        s_body))
    story.append(Paragraph("1.2 Lo que ya funciona", s_h2))
    story.append(Paragraph(
        "La Secretaría de Salud de BC, vía Programa de Zoonosis de la Jurisdicción Sanitaria #4, reportó <b>21,085 esterilizaciones caninas y felinas en 2024</b> en colonias con rezago social de todo el estado, incluido San Quintín. Jornadas de 80-120 cirugías ya se han hecho en San Quintín (2018). La capacidad quirúrgica existe; falta la <b>red permanente</b> que evite picos y valles.",
        s_body))
    story.append(Paragraph("1.3 Valle productivo: el desecho como activo", s_h2))
    story.append(Paragraph(
        "El Valle de San Quintín es potencia agrícola (fresa, tomate, berries) y pecuaria (bovino, caprino, avícola de traspatio). Cada ciclo genera mortalidad pecuaria (1-3% bovinos), necropsias, restos de rastros y animales de compañía fallecidos sin destino digno (fosas clandestinas, quema). Hoy son costo sanitario. Con hidrólisis alcalina pueden ser <b>2,000-3,000 litros de hidrolizado estéril por tonelada</b>, convertible en fertilizante líquido N-P-K + aminoácidos, validado en cultivo de chile, lechuga hidropónica y maíz.",
        s_body))
    story.append(Paragraph("1.4 Ventana normativa", s_h2))
    story.append(Paragraph(
        "La Ley de Protección a los Animales Domésticos de BC (reforma 2023) obliga a municipios a campañas permanentes de esterilización y a transitar de “centros de control” a “centros de atención y bienestar”. Las NOM-042-SSA2 y NOM-033-SAG/ZOO permiten hidrólisis alcalina como disposición. San Quintín aún no publica su Reglamento Municipal — <b>puede nacer ya alineado a este modelo</b>.",
        s_body))
    # 2 Arquitectura
    story.append(Paragraph("2. Arquitectura de 5 capas — cómo se sostienen", s_h1))
    story.append(Paragraph(
        "Ninguna capa funciona sola. Sin vales y quirófanos, el Centro se satura. Sin aquamación y bioliquidadora, el municipio paga disposición y pierde valor. Con la bioliquidadora, el fertilizante financia 30-40% de la operación al segundo año.",
        s_body))
    # diagram replacement as table
    arch = [
        [Paragraph("<b>Capa 1 — Vales</b><br/><font size=7 color='#0e7c75'>financia demanda</font>", s_table_cell_center), Paragraph("→", s_table_cell_center), Paragraph("<b>Capa 3 — Centro de Vida</b><br/><font size=7>acoge, cura, conecta</font>", s_table_cell_center)],
        [Paragraph("<b>Capa 2 — Quirófanos</b><br/><font size=7 color='#b45309'>ejecuta en territorio</font>", s_table_cell_center), Paragraph("→", s_table_cell_center), Paragraph("<b>Capa 4 — Aquamación</b><br/><font size=7>honra con agua</font>", s_table_cell_center)],
        [Paragraph("<b>Capa 5 — Bioliquidadora</b><br/><font size=7>2,400L móvil</font>", s_table_cell_center), Paragraph("→", s_table_cell_center), Paragraph("<b>Fertilizante</b><br/><font size=7>parques + ranchos → padrinan vales ↺</font>", s_table_cell_center)],
    ]
    at = Table(arch, colWidths=[2.2*inch, 0.4*inch, 2.4*inch])
    at.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), TEAL_L),
        ('BACKGROUND', (0,1), (0,1), colors.HexColor("#fff7ed")),
        ('BACKGROUND', (0,2), (0,2), colors.HexColor("#ecfdf5")),
        ('BACKGROUND', (2,0), (2,0), NAVY),
        ('TEXTCOLOR', (2,0), (2,0), colors.white),
        ('BACKGROUND', (2,1), (2,1), colors.HexColor("#e0f2fe")),
        ('BACKGROUND', (2,2), (2,2), colors.HexColor("#fef3c7")),
        ('BOX', (0,0), (-1,-1), 0.5, LINE),
        ('INNERGRID', (0,0), (-1,-1), 0.4, LINE),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [6,6,6,6]),
    ]))
    story.append(at)
    story.append(Spacer(1,6))
    story.append(Paragraph("Unidad operativa mínima: 1 coordinadora + 3 promotoras por delegación + 1 quirófano móvil + 2 veterinarias afiliadas + 1 centro base.", s_caption))
    # 3 Vales
    story.append(Paragraph("3. Capa 1 — Vales Solidarios para Esterilización", s_h1))
    story.append(Paragraph(
        "Vale nominativo QR (y en papel) que cubre 100% de esterilización (cirugía + analgésico + antibiótico + 1 noche si requiere) en cualquier veterinaria voluntaria afiliada. El tutor no paga. La veterinaria cobra al Fondo Común en 72h por SPEI.",
        s_body))
    story.append(Paragraph("Quién califica (criterio simple, sin humillación)", s_h2))
    bullets = [
        "Vive en colonia/ejido con índice de rezago (CONEVAL municipal) — ~60% del valle",
        "Es jornalera/o, persona mayor, madre sola, discapacidad, estudiante, o ingreso <2 salarios mínimos (autodeclaración)",
        "Animal rescatado / comunitario / feral (validado por promotora)",
        "Ya tiene 2+ animales sin esterilizar (prevención de camada) — resto co-pago 30% (300-400 MXN)",
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", s_bullet))
    story.append(Paragraph("Tres vías para obtenerlo", s_h2))
    story.append(Paragraph(
        "<b>1) WhatsApp Red de Vida:</b> foto del animal + colonia → bot responde vale QR en &lt;5 min (validación promotora remota). <b>2) Papel en punto comunitario:</b> tienda, iglesia, escuela, casa de promotora — talonario numerado con sello. Sin celular necesario. <b>3) Derivación:</b> veterinaria afiliada, Jurisdicción Sanitaria o quirófano móvil lo emite en sitio. Vigencia 30 días, reagendable 1 vez.",
        s_body))
    story.append(Paragraph("Tabulador único 2026 y afiliación veterinaria", s_h2))
    vals = [
        [Paragraph("<b>Concepto</b>", s_table_header), Paragraph("<b>Reembolso</b>", s_table_header)],
        [Paragraph("Felino (M/H)", s_table_cell), Paragraph("850 MXN", s_table_cell_center)],
        [Paragraph("Canino &lt;15 kg", s_table_cell), Paragraph("1,100 MXN", s_table_cell_center)],
        [Paragraph("Canino 15-30 kg", s_table_cell), Paragraph("1,400 MXN", s_table_cell_center)],
        [Paragraph("Canino &gt;30 kg", s_table_cell), Paragraph("1,750 MXN", s_table_cell_center)],
        [Paragraph("Feral/TNR + marcaje", s_table_cell), Paragraph("+150 MXN bono", s_table_cell_center)],
    ]
    vt = Table(vals, colWidths=[3.0*inch, 1.8*inch])
    vt.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), NAVY), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]), ('GRID', (0,0), (-1,-1), 0.4, LINE), ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('LEFTPADDING', (0,0), (-1,-1), 6)]))
    story.append(vt)
    story.append(Spacer(1,6))
    story.append(Paragraph(
        "<b>Afiliación voluntaria:</b> firma Carta de Adhesión, acepta tabulador y protocolo analgésico, foto pre/post. <b>Beneficios:</b> flujo constante, difusión oficial, crédito fiscal como donación, compras consolidadas. <b>Anti-fraude:</b> QR único, geocerca, tope 3 vales/hogar/semestre, auditoría 10%.",
        s_body))
    story.append(Paragraph("Costo anual 3,600 esterilizaciones: ~3.9 MDP; con copagos y padrinazgos, carga municipal neta ~2.1 MDP.", ParagraphStyle('cost', parent=s_body, fontName=FONTB, fontSize=8, leading=11, textColor=TEAL_D, backColor=TEAL_L, borderPadding=(6,6,6))))
    # 4 Clinicas
    story.append(Paragraph("4. Capa 2 — Quirófanos de Barrio (Pop-Up Clinics)", s_h1))
    story.append(Paragraph(
        "El quirófano va a la colonia. Unidad van + remolque quirúrgico (2 mesas) o carpa certificada + equipo portátil, con coordinación previa de 2 semanas con promotoras. Insumos por cirugía 280-350 MXN; costo por animal en móvil 650-750 MXN (más barato que vale en clínica por escala).",
        s_body))
    story.append(Paragraph("Operación tipo", s_h2))
    pasos = [
        "<b>T-14 días:</b> Promotora recorre 3 colonias, perifoneo, grupo WhatsApp, lista 50-70 animales (prioriza hembras y ferales).",
        "<b>T-2 días:</b> Confirmación, ayuno, ubicación (cancha/iglesia/escuela) con agua, luz, sombra.",
        "<b>Día Q:</b> Equipo 1 cirujano + 1 anestesista + 2 técnicos + 3 voluntarias. Flujo recepción→pesaje→pre→cirugía→recuperación con cobija→foto con tutor + carnet. <b>40-60 cirugías/día</b>. TNR con muesca oreja.",
        "<b>Post:</b> Base de datos, reporte al tablero, retorno día 10 para retiro puntos.",
    ]
    for p in pasos:
        story.append(Paragraph(f"• {p}", s_bullet))
    story.append(Paragraph("Calendario rotativo piloto (12 jornadas / 90 días)", s_h2))
    cal = [
        [Paragraph("<b>Semana</b>", s_table_header), Paragraph("<b>Sede</b>", s_table_header), Paragraph("<b>Meta</b>", s_table_header)],
        [Paragraph("1", s_table_cell_center), Paragraph("Vicente Guerrero (Zapata + Flores Magón)", s_table_cell), Paragraph("55 cirugías", s_table_cell_center)],
        [Paragraph("2", s_table_cell_center), Paragraph("Lázaro Cárdenas + Ejido Papalote", s_table_cell), Paragraph("50 cirugías", s_table_cell_center)],
        [Paragraph("3", s_table_cell_center), Paragraph("Camalú + Ejido E. Zapata", s_table_cell), Paragraph("50 cirugías", s_table_cell_center)],
        [Paragraph("4", s_table_cell_center), Paragraph("Bahía de los Ángeles (3 días)", s_table_cell), Paragraph("70 cirugías", s_table_cell_center)],
    ]
    ct = Table(cal, colWidths=[0.9*inch, 3.6*inch, 1.3*inch])
    ct.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), NAVY), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]), ('GRID', (0,0), (-1,-1), 0.4, LINE), ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(ct)
    # 5 Centro
    story.append(Paragraph("5. Capa 3 — Centro de Bienestar, Adopción y Reencuentro (CEBISQ)", s_h1))
    story.append(Paragraph("<b>No es perrera. Es Centro de Vida.</b> Cambio de nombre es cambio de norma. 4 funciones: Resguardo, Salud, Reencuentro, Adopción.", ParagraphStyle('vida', parent=s_body, fontName=FONTB, fontSize=9, leading=12, textColor=NAVY, backColor=colors.HexColor("#fef3c7"), borderPadding=(6,6,6))))
    story.append(Paragraph("Flujo de un animal que ingresa", s_h2))
    flujo = [
        "<b>0-2h — Foto y publicación:</b> Foto, video 15s, chip, publicación automática en FB/WA/Tablero. Collar ID temporal.",
        "<b>2-48h — Salud:</b> Desparasitación, vacuna, evaluación conductual, esterilización, cuarentena separada.",
        "<b>0-10 días — Reencuentro:</b> Ventana 10 días (no 72h), difusión diaria. Tutor paga solo esterilización si faltaba, no multa punitiva.",
        "<b>Día 5+ — Adopción:</b> Entrevista + visita domiciliaria + contrato + seguimiento 30-90 días. Si no adoptable: rehabilitación u hogar temporal.",
        "<b>Si no adoptado:</b> No se sacrifica por cupo. Hogar temporal, traslado a Ensenada/Tijuana/US, o residente con padrino.",
    ]
    for f in flujo:
        story.append(Paragraph(f"• {f}", s_bullet))
    story.append(Paragraph("Infraestructura", s_h2))
    story.append(Paragraph(
        "<b>Módulo piloto (mes 3-6):</b> 12 caniles 2x3m + gatera 8 + cuarentena 4, 400m², predio en comodato. <b>Centro completo (mes 6-18):</b> 48 caniles + 24 felinos + patios 2,000m² + sala duelo/aquamación 20m² + jardín memorial. Costo adecuación 1.2 MDP. Dotación: 1 MVZ ½ tiempo + 4 cuidadores + etóloga voluntaria + coordinadora adopciones.",
        s_body))
    story.append(Paragraph(
        "<b>Protocolo no sacrificio:</b> Eutanasia solo por sufrimiento irreversible o agresión grave con dictamen 2 MVZ + etóloga, acta y publicación. Meta &lt;5% eutanasia médica, 0% por cupo. Auditoría trimestral Colegio MVZ.",
        ParagraphStyle('nosac', parent=s_body, fontName=FONTB, fontSize=8, leading=11, textColor=colors.HexColor("#065f46"), backColor=colors.HexColor("#dcfce7"), borderPadding=(6,6,6))
    ))
    story.append(Paragraph("Indicadores CEBISQ: Reencuentro &gt;30% • Adopción &gt;60% • Estancia media &lt;22 días • Mortalidad intrahospitalaria &lt;3%", s_caption))
    # 6 Aquamacion
    story.append(Paragraph("6. Capa 4 — Honra Final: Aquamación", s_h1))
    story.append(Paragraph(
        "Hidrólisis alcalina a 93-98°C: 95% agua + 5% álcali (KOH/NaOH), circulación suave, 12-20h. Acelera lo natural. Queda: cenizas minerales + efluente estéril. Sin fuego, sin humo, sin dioxinas ni mercurio.",
        s_body))
    # compare table
    comp = [
        [Paragraph("<b></b>", s_table_header), Paragraph("<b>Incineración (1,500°C)</b>", s_table_header), Paragraph("<b>Aquamación (95°C, agua)</b>", s_table_header)],
        [Paragraph("Energía", s_table_cell), Paragraph("Alta (gas)", s_table_cell_center), Paragraph("90% menos", s_table_cell_center)],
        [Paragraph("Emisiones", s_table_cell), Paragraph("CO, dioxinas, Hg", s_table_cell_center), Paragraph("Cero", s_table_cell_center)],
        [Paragraph("Cenizas retornables", s_table_cell), Paragraph("Base", s_table_cell_center), Paragraph("+20%", s_table_cell_center)],
        [Paragraph("Ruido/humo", s_table_cell), Paragraph("Sí", s_table_cell_center), Paragraph("Silencioso, sin humo", s_table_cell_center)],
        [Paragraph("Efluente", s_table_cell), Paragraph("Gases", s_table_cell_center), Paragraph("Líquido estéril → fertilizante", s_table_cell_center)],
    ]
    cpt = Table(comp, colWidths=[1.6*inch, 1.8*inch, 1.8*inch])
    cpt.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), NAVY), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]), ('GRID', (0,0), (-1,-1), 0.4, LINE), ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(cpt)
    story.append(Spacer(1,6))
    story.append(Paragraph(
        "<b>Dos modalidades en CEBISQ:</b> <b>Comunal solidaria</b> (no reclamados y comunitarios, cenizas a urna colectiva o jardín memorial, sin costo) y <b>Privada con retorno</b> (urna biodegradable + certificado + huella, 800-2,200 MXN según peso; familias vulnerables con vale 70% subsidio). Equipo: Bio-Response PET-400 (180 kg, 3-6 por ciclo, 2 ciclos/día), 1.1 MDP reacondicionado, cuarto 20m². Sala de despedida 6m² + taller mensual de duelo.",
        s_body))
    # 7 Bioliquidadora
    story.append(Paragraph("7. Capa 5 — Unidad Móvil de Bioliquidación y Ciclo de Fertilizante", s_h1))
    story.append(Paragraph(
        "Problema: cada año San Quintín paga por enterrar, quemar o abandonar toneladas de biomasa (vacas, cabras, aves, restos de rastro, animales no reclamados) con riesgo sanitario. Solución: hidrolizador alcalino móvil que esteriliza y licúa en &lt;24h en el sitio.",
        s_body))
    story.append(Paragraph("Unidad móvil propuesta", s_h2))
    story.append(Paragraph(
        "Remolque 20' con reactor 2,400L (acero 316), chaqueta diésel 80k BTU, bomba 2HP, canasta para huesos. <b>Capacidad:</b> 400-600 kg/ciclo (1 vaca o 8 perros grandes), 1 ciclo/día → 150 ton/año. <b>Proceso:</b> agua + álcali 5% + 90-100°C + recirculación → hidrolizado estéril (pH &gt;12.8 por 10+ días mata todos los patógenos relevantes) + minerales óseos. <b>Costo:</b> 1.35 MDP reacondicionada/fabricación local vs 2.1 nueva. Operación 38k/mes (20 ciclos: diésel + KOH + análisis).",
        s_body))
    story.append(Paragraph("De hidrolizado a fertilizante — “Fertilizante de Retorno”", s_h2))
    story.append(Paragraph(
        "Hidrolizado bruto pH ~13 → neutralización con ensilaje ácido (pH 3.9) o ácido cítrico hasta pH 6.8 → líquido ámbar sin olor con N-P-K-Ca + aminoácidos. Validación científica: Akdeniz & Yi 2021 (Trans ASABE): hidrolizado neutralizado + aerobio 15 días, diluido 20x + fertilizante comercial → +18.2% peso fresco lechuga, +clorofila, -50% costo fertilizante. Kang 2019: mejora en chile.",
        s_body))
    # lots table
    lots = [
        [Paragraph("<b>Lote</b>", s_table_header), Paragraph("<b>Formulación</b>", s_table_header), Paragraph("<b>Uso</b>", s_table_header), Paragraph("<b>Dilución</b>", s_table_header)],
        [Paragraph("A — FLD Parques", s_table_cell_center), Paragraph("Hidrolizado filtrado", s_table_cell), Paragraph("Camellones, plazas, vivero", s_table_cell), Paragraph("15-20:1", s_table_cell_center)],
        [Paragraph("B — Mezcla Rancho", s_table_cell_center), Paragraph("FLD + compost + biochar 30%", s_table_cell), Paragraph("Parcelas tomate/fresa/alfalfa con esparcidora 3,000L", s_table_cell), Paragraph("10:1 + 2t compost/ha", s_table_cell_center)],
        [Paragraph("C — Enmienda", s_table_cell_center), Paragraph("Sedimento óseo molido", s_table_cell), Paragraph("Corrección suelos alcalinos", s_table_cell), Paragraph("200 kg/ha", s_table_cell_center)],
    ]
    lt = Table(lots, colWidths=[1.2*inch, 1.8*inch, 2.0*inch, 1.2*inch])
    lt.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), NAVY), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]), ('GRID', (0,0), (-1,-1), 0.4, LINE), ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(lt)
    story.append(Spacer(1,6))
    story.append(Paragraph(
        "<b>Rendimiento:</b> 1 ton mortalidad → ~2,500L hidrolizado → ~2,000L neutralizado → ~40,000L diluido → 2-3 ha parque o 1 ha cultivo/ciclo. <b>Economía año 2 (80 ton):</b> 200,000L bruto → 3.2M L diluido → ~872k MXN valor (fertilizante + ahorro disposición evitada 200k). Cubre 30-40% de operación capas 1-3.",
        ParagraphStyle('rend', parent=s_body, fontName=FONTB, fontSize=8, leading=11, textColor=TEAL_D, backColor=TEAL_L, borderPadding=(6,6,6))
    ))
    story.append(Paragraph("Logística: pipa municipal 10,000L + barra fertirriego en parques; remolque esparcidor 3,000L en ranchos. Cada lote con QR: fecha, NPK, patógeno negativo, mapa GIS. Primeros 6 meses como “programa piloto UABC” mientras se tramita registro SADER (fertilizante orgánico líquido).", s_body))
    # 8 Gobernanza
    story.append(Paragraph("8. Gobernanza, marco legal y finanzas", s_h1))
    story.append(Paragraph("Figura jurídica", s_h2))
    story.append(Paragraph(
        "<b>AC “Red de Vida San Quintín AC”</b> en convenio 3 años con Ayuntamiento (renovable, cláusula continuidad). <b>Consejo (7):</b> 2 municipio (Salud + Desarrollo Rural), 2 colectivos, 1 Colegio MVZ, 1 ejido/rancho, 1 academia (UABC/CICESE). <b>Asamblea comunitaria trimestral</b> abierta con tablero proyectado. Fondo común en cuenta mancomunada AC-municipio, 2 firmas obligatorias, auditoría semestral, publicación mensual.",
        s_body))
    story.append(Paragraph("Marco legal a aprobar", s_h2))
    legal = [
        "Reglamento Municipal de Protección y Bienestar Animal: define Centro de Bienestar, prohíbe sacrificio por cupo/tiempo/raza, instituye vales y quirófanos, autoriza hidrólisis y uso de hidrolizado como fertilizante, legaliza TNR.",
        "Convenio con Jurisdicción Sanitaria #4 (protocolos quirúrgicos, RPBI).",
        "Permiso CONAGUA/CESPEQ + SADER para reúso de efluente neutralizado en riego y registro de fertilizante.",
        "Lineamientos de transparencia: padrones de vales, pagos, análisis fertilizante y actas eutanasia publicados mensual.",
    ]
    for l in legal:
        story.append(Paragraph(f"• {l}", s_bullet))
    story.append(Paragraph("Presupuesto", s_h2))
    pres = [
        [Paragraph("<b>Concepto arranque (0-6m)</b>", s_table_header), Paragraph("<b>MDP</b>", s_table_header), Paragraph("<b>Fuente</b>", s_table_header)],
        [Paragraph("Adecuación CEBISQ módulo 1", s_table_cell), Paragraph("1.20", s_table_cell_center), Paragraph("FAIS", s_table_cell_center)],
        [Paragraph("Quirófano móvil (remolque usado)", s_table_cell), Paragraph("0.55", s_table_cell_center), Paragraph("Coop. intl", s_table_cell_center)],
        [Paragraph("Equipo aquamación PET-400 reacond.", s_table_cell), Paragraph("1.10", s_table_cell_center), Paragraph("Coop. intl + donación", s_table_cell_center)],
        [Paragraph("Bioliquidadora móvil 2,400L", s_table_cell), Paragraph("1.35", s_table_cell_center), Paragraph("Estado + padrinazgo", s_table_cell_center)],
        [Paragraph("Fondo inicial 1,000 vales", s_table_cell), Paragraph("1.00", s_table_cell_center), Paragraph("Municipal + padrinazgo", s_table_cell_center)],
        [Paragraph("<b>Total arranque</b>", s_table_cell), Paragraph("<b>5.20</b>", s_table_cell_center), Paragraph("", s_table_cell)],
    ]
    prt = Table(pres, colWidths=[3.0*inch, 0.8*inch, 2.0*inch])
    prt.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), NAVY), ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#fef3c7")), ('ROWBACKGROUNDS', (0,1), (-1,5), [colors.white, LIGHT_BG]), ('GRID', (0,0), (-1,-1), 0.4, LINE), ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(prt)
    story.append(Spacer(1,6))
    story.append(Paragraph(
        "<b>Operación anual régimen:</b> Egresos brutos 6.0 MDP (vales 3.9 + móviles 1.15 + CEBISQ 0.95 + aqua/bio 0.42 + coordinación 0.58) — Ingresos propios 1.8 MDP (fertilizante 0.76 + aquamación privada 0.50 + padrinazgos 0.84 + donaciones 0.21) = <b>Neto 4.2 MDP</b> (3.6 año 2 optimizado). <b>Per cápita:</b> 31 MXN/hab/año.",
        s_body))
    story.append(Paragraph(
        "Anticorrupción por diseño: SPEI + 2 firmas, nada en efectivo &gt;2k, vales numerados y publicados, compras &gt;20k con 3 cotizaciones, tope gasto administrativo &lt;12%, Coordinadora no firma sola.",
        ParagraphStyle('antic', parent=s_body, fontName=FONTB, fontSize=8, leading=11, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderPadding=(6,6,6))
    ))
    # 9 Tecnologia
    story.append(Paragraph("9. Tecnología: papel primero, app después", s_h1))
    story.append(Paragraph(
        "<b>Principio:</b> si no funciona con cuaderno y WhatsApp en colonia sin señal, no funciona. <b>Papel obligatorio:</b> talonario numerado QR + sello + copia carbón, cartel jornada, libro ingresos. <b>WhatsApp primario:</b> bot “Hola, quiero esterilizar” → foto + colonia → vale PDF + audio instrucciones; difusión extraviados a 5 grupos por delegación. <b>Tablero público:</b> site/index.html estático alimentado por CSV de Sheets (vales, cirugías, adopciones, litros, cuenta). 10 min actualización diaria. Costo &lt;2k/mes. <b>App PWA solo mes 12+</b>, nunca obligatoria.",
        s_body))
    # 10 Plan
    story.append(Paragraph("10. Plan 0-24 meses • Métricas • Riesgos • Anexos", s_h1))
    plan = [
        [Paragraph("<b>Fase</b>", s_table_header), Paragraph("<b>Periodo</b>", s_table_header), Paragraph("<b>Hitos clave</b>", s_table_header), Paragraph("<b>Meta</b>", s_table_header)],
        [Paragraph("0 Preparación", s_table_cell_center), Paragraph("M0-2", s_table_cell_center), Paragraph("Taller co-diseño 1 día, AC + convenio, censo 400 hogares, 8 promotoras, 3 vets afiliadas", s_table_cell), Paragraph("Base lista", s_table_cell_center)],
        [Paragraph("1 Piloto 90d", s_table_cell_center), Paragraph("M3-5", s_table_cell_center), Paragraph("300 vales, 12 jornadas, CEBISQ 12 caniles, demo aquamación/bio 1sem/mes, tablero vivo", s_table_cell), Paragraph("450 cirugías<br/>40 adopciones<br/>2,000L fertilizante", s_table_cell_center)],
        [Paragraph("2 Escalamiento", s_table_cell_center), Paragraph("M6-12", s_table_cell_center), Paragraph("CEBISQ 48 caniles + aqua, bio propia, 2 días/semana móviles, 1,800 vales/semestre, 5 ranchos", s_table_cell), Paragraph("2,200/año", s_table_cell_center)],
        [Paragraph("3 Consolidación", s_table_cell_center), Paragraph("M12-24", s_table_cell_center), Paragraph("3,600/año, &gt;60% adopción, 60-80 ton/año → 150k L, reglamento, manual réplica", s_table_cell), Paragraph("45% cobertura valle", s_table_cell_center)],
    ]
    plt = Table(plan, colWidths=[1.1*inch, 0.7*inch, 3.2*inch, 1.4*inch])
    plt.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), NAVY), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]), ('GRID', (0,0), (-1,-1), 0.4, LINE), ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(plt)
    story.append(Spacer(1,8))
    story.append(Paragraph("Métricas de éxito", s_h2))
    met = [
        [Paragraph("<b>Indicador</b>", s_table_header), Paragraph("<b>Base 2026</b>", s_table_header), Paragraph("<b>12m</b>", s_table_header), Paragraph("<b>24m</b>", s_table_header)],
        [Paragraph("Esterilizaciones/año", s_table_cell), Paragraph("~600", s_table_cell_center), Paragraph("2,200", s_table_cell_center), Paragraph("3,600", s_table_cell_center)],
        [Paragraph("% hembras esterilizadas", s_table_cell), Paragraph("&lt;15%", s_table_cell_center), Paragraph("35%", s_table_cell_center), Paragraph("55%", s_table_cell_center)],
        [Paragraph("Animales en calle", s_table_cell), Paragraph("~8,000", s_table_cell_center), Paragraph("-25%", s_table_cell_center), Paragraph("-45%", s_table_cell_center)],
        [Paragraph("Reencuentro CEBISQ", s_table_cell), Paragraph("~0%", s_table_cell_center), Paragraph("25%", s_table_cell_center), Paragraph("35%", s_table_cell_center)],
        [Paragraph("Adopción no reclamados", s_table_cell), Paragraph("~10%", s_table_cell_center), Paragraph("45%", s_table_cell_center), Paragraph("65%", s_table_cell_center)],
        [Paragraph("Eutanasia por cupo", s_table_cell), Paragraph("n/a", s_table_cell_center), Paragraph("0%", s_table_cell_center), Paragraph("0%", s_table_cell_center)],
        [Paragraph("Aquamaciones/año", s_table_cell), Paragraph("0", s_table_cell_center), Paragraph("180", s_table_cell_center), Paragraph("400", s_table_cell_center)],
        [Paragraph("Ton bioliquidadas", s_table_cell), Paragraph("0", s_table_cell_center), Paragraph("35", s_table_cell_center), Paragraph("80", s_table_cell_center)],
        [Paragraph("Litros fertilizante", s_table_cell), Paragraph("0", s_table_cell_center), Paragraph("70k", s_table_cell_center), Paragraph("150k", s_table_cell_center)],
    ]
    mt = Table(met, colWidths=[2.2*inch, 1.0*inch, 1.0*inch, 1.0*inch])
    mt.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), NAVY), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]), ('GRID', (0,0), (-1,-1), 0.4, LINE), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(mt)
    story.append(Spacer(1,6))
    story.append(Paragraph("Riesgos y mitigación (extracto)", s_h2))
    riesgos = [
        [Paragraph("Vets no se afilian (desconfianza pago)", s_table_cell), Paragraph("Pago 72h garantizado con fideicomiso + anticipo 20%, primer mes pago semanal", s_table_cell)],
        [Paragraph("Rechazo cultural a esterilización", s_table_cell), Paragraph("Promotoras locales + mixteco, testimonios, esterilización + desparasitación regalo", s_table_cell)],
        [Paragraph("Sobrecupo CEBISQ", s_table_cell), Paragraph("Tope 85% → hogares temporales + traslados, no sacrificio", s_table_cell)],
        [Paragraph("Falla bio / efluente no autorizado", s_table_cell), Paragraph("Stock 60 días KOH, análisis previos, neutralización, permiso riego restringido", s_table_cell)],
        [Paragraph("Cambio de administración", s_table_cell), Paragraph("AC titular de equipos, convenio trianual, padrinazgos diversificados", s_table_cell)],
    ]
    rt = Table([[Paragraph("<b>Riesgo</b>", s_table_header), Paragraph("<b>Mitigación</b>", s_table_header)]] + riesgos, colWidths=[2.2*inch, 4.2*inch])
    rt.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#92400e")), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#fef3c7")]), ('GRID', (0,0), (-1,-1), 0.4, LINE), ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(rt)
    story.append(Spacer(1,8))
    story.append(Paragraph("Anexos — plantillas listas para fotocopiar", s_h2))
    story.append(Paragraph(
        "El documento completo incluye anexos operativos listos para imprimir: <b>Anexo A</b> Vale (frente/reverso con mapa), <b>B</b> Consentimiento quirúrgico, <b>C</b> Contrato adopción, <b>D</b> Carta adhesión veterinaria (1 pág.), <b>E</b> Especificación bioliquidadora (remolque 20', 2,400L, 316, 80k BTU), <b>F</b> Extracto Reglamento municipal (Art. 12, 18, 24, 27, 31), <b>G</b> Campos del tablero CSV. Ver archivos <i>docs/01 a 07</i> y <i>PROPUESTA_INTEGRAL.md §14</i>.",
        s_body))
    story.append(Spacer(1,8))
    story.append(Paragraph("Cierre: por qué hacerlo bonito y hacerlo ya", s_h1))
    story.append(Paragraph(
        "San Quintín no necesita una perrera más grande. Necesita un tejido. Un tejido donde la señora que alimenta a 6 perros sea promotora pagada, no denunciada. Donde el veterinario gane atendiendo a los que nunca podían pagarle. Donde el niño que perdió a su perro reciba cenizas dignas y no una bolsa negra. Donde la vaca que murió no contamine el arroyo sino alimente la milpa. Eso no es “animalismo”. Es salud pública, economía circular y orgullo municipal. Y es replicable: si San Quintín — disperso, joven, con poco presupuesto — puede, cualquier municipio de México puede.",
        ParagraphStyle('cierre', parent=s_body, fontName=FONTI, fontSize=9, leading=13, textColor=NAVY, borderPadding=(8,8,8), backColor=TEAL_L, borderColor=TEAL)
    ))
    story.append(Spacer(1,10))
    # CTA box
    cta_data = [
        [Paragraph("<b>Siguiente paso — Taller de co-diseño en 30 días</b><br/><font size=7>1 día • Huellitas de Amor SQ + 2 veterinarias + Jurisdicción #4 + Desarrollo Rural • En Vicente Guerrero o Lázaro Cárdenas</font>", ParagraphStyle('cta1', parent=s_body, fontSize=9, leading=12, textColor=colors.white)),
         Paragraph("<b><font color='#ffffff'>eugene@serviceofothers.org</font></b><br/><font size=7 color='#bfe9e4'>Asunto: QUIERO TEJER + tu colonia</font>", ParagraphStyle('cta2', parent=s_body, fontSize=9, leading=11, textColor=colors.white, alignment=TA_RIGHT))]
    ]
    cta = Table(cta_data, colWidths=[4.6*inch, 1.8*inch])
    cta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('ROUNDEDCORNERS', [8,8,8,8]),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(cta)
    story.append(Spacer(1,8))
    story.append(Paragraph("Documento vivo v1.0 — 10 ago 2026. Licencia CC BY-SA 4.0. Comentarios y mejoras por pull request o correo. Diseñado en San Quintín, para San Quintín, con el mundo como testigo.", s_caption))
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado: {out}")

if __name__ == "__main__":
    build()
