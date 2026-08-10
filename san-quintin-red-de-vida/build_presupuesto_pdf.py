#!/usr/bin/env python3
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
WINE = colors.HexColor("#7A1931")
WINE_D = colors.HexColor("#5A1220")
WINE_L = colors.HexColor("#fdf0f3")
GOLD = colors.HexColor("#C5A880")
GOLD_D = colors.HexColor("#8c6a2e")
TEAL = colors.HexColor("#13807a")
TEAL_D = colors.HexColor("#0e5e59")
TEAL_L = colors.HexColor("#e6f4f3")
MUTED = colors.HexColor("#6b6f73")
LINE = colors.HexColor("#ede6d6")
LIGHT_BG = colors.HexColor("#fdfbf3")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
try:
    pdfmetrics.registerFont(TTFont("DJ", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DJ-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DJ-I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")))
    FONT="DJ"; FONTB="DJ-B"; FONTI="DJ-I"
except:
    FONT="Helvetica"; FONTB="Helvetica-Bold"; FONTI="Helvetica-Oblique"
styles = getSampleStyleSheet()
s_h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName=FONTB, fontSize=13, leading=15, textColor=WINE_D, spaceBefore=10, spaceAfter=6)
s_h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName=FONTB, fontSize=9.5, leading=12, textColor=TEAL_D, spaceBefore=8, spaceAfter=4)
s_body = ParagraphStyle('Body', parent=styles['Normal'], fontName=FONT, fontSize=7, leading=10, textColor=colors.HexColor("#1e2329"), alignment=TA_JUSTIFY, spaceAfter=4)
s_caption = ParagraphStyle('Caption', parent=styles['Normal'], fontName=FONTI, fontSize=6, leading=7, textColor=MUTED, alignment=TA_CENTER, spaceAfter=4)
s_th = ParagraphStyle('TH', parent=styles['Normal'], fontName=FONTB, fontSize=6, leading=7, textColor=colors.white, alignment=TA_CENTER)
s_tc = ParagraphStyle('TC', parent=styles['Normal'], fontName=FONT, fontSize=6, leading=7, textColor=colors.HexColor("#1e2329"), alignment=TA_LEFT)
s_tc_r = ParagraphStyle('TCR', parent=s_tc, alignment=TA_RIGHT)
s_tc_c = ParagraphStyle('TCC', parent=s_tc, alignment=TA_CENTER)
s_kpi = ParagraphStyle('KPI', parent=styles['Normal'], fontName=FONTB, fontSize=11, leading=12, textColor=WINE_D, alignment=TA_CENTER)
s_kpi_l = ParagraphStyle('KPIL', parent=styles['Normal'], fontName=FONTB, fontSize=5.5, leading=6, textColor=TEAL_D, alignment=TA_CENTER)
def hdr_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(WINE)
    canvas.rect(0, doc.pagesize[1]-30, doc.pagesize[0], 30, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, doc.pagesize[1]-30, doc.pagesize[0], 3, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont(FONTB, 6.5)
    canvas.drawString(36, doc.pagesize[1]-14, "RED DE VIDA SAN QUINTÍN  —  PLAN Y PRESUPUESTO DETALLADO 2026-2028")
    canvas.setFont(FONT, 5)
    canvas.setFillColor(colors.HexColor("#f8e6ea"))
    canvas.drawString(36, doc.pagesize[1]-22, "Municipio de San Quintín, BCN  •  Imprimible para Tesorería y Cabildo  •  Agosto 2026  •  CC BY-SA 4.0")
    canvas.setFont(FONT, 5)
    canvas.setFillColor(colors.white)
    canvas.drawRightString(doc.pagesize[0]-36, doc.pagesize[1]-14, "CONFIDENCIAL — USO MUNICIPAL")
    canvas.drawRightString(doc.pagesize[0]-36, doc.pagesize[1]-22, "eugene@serviceofothers.org")
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(36, 32, doc.pagesize[0]-36, 32)
    canvas.setFont(FONT, 5)
    canvas.setFillColor(MUTED)
    canvas.drawString(36, 22, "Red de Vida San Quintín — Esterilizar. Adoptar. Honrar. Regenerar. — 5 capas + Red de Guardianes")
    canvas.drawRightString(doc.pagesize[0]-36, 22, f"Pág. {doc.page}")
    canvas.restoreState()
def style_table(t, header=True):
    s=[('GRID', (0,0), (-1,-1), 0.4, LINE),('TOPPADDING', (0,0), (-1,-1), 3),('BOTTOMPADDING', (0,0), (-1,-1), 3),('LEFTPADDING', (0,0), (-1,-1), 4),('RIGHTPADDING', (0,0), (-1,-1), 4),('VALIGN', (0,0), (-1,-1), 'MIDDLE')]
    if header:
        s.extend([('BACKGROUND', (0,0), (-1,0), WINE), ('TEXTCOLOR', (0,0), (-1,0), colors.white), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])])
    else:
        s.append(('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, LIGHT_BG]))
    t.setStyle(TableStyle(s))
    return t
def P(txt, style=s_tc): return Paragraph(txt, style)
def build():
    out = os.path.join(os.path.dirname(__file__), "Plan-Presupuesto-Red-de-Vida-2026-2028.pdf")
    doc = SimpleDocTemplate(out, pagesize=letter, leftMargin=32, rightMargin=32, topMargin=42, bottomMargin=34, title="Plan y Presupuesto Red de Vida 2026-2028", author="Eugene Buchanan")
    story=[]
    story.append(Spacer(1, 6))
    story.append(Paragraph("MUNICIPIO DE SAN QUINTÍN, BAJA CALIFORNIA", ParagraphStyle('eyeb', parent=styles['Normal'], fontName=FONTB, fontSize=6.5, leading=7, textColor=GOLD_D, spaceAfter=4)))
    story.append(Paragraph("Plan y Presupuesto<br/>Detallado por Programa", ParagraphStyle('cover', parent=styles['Title'], fontName=FONTB, fontSize=28, leading=28, textColor=WINE_D, spaceAfter=2)))
    story.append(Paragraph("Red de Vida San Quintín — 5 capas + Red de Guardianes Solidarios", ParagraphStyle('sub', parent=styles['Normal'], fontName=FONT, fontSize=10, leading=12, textColor=TEAL_D, spaceAfter=6)))
    story.append(HRFlowable(width="18%", thickness=2.5, color=GOLD, spaceAfter=6, spaceBefore=2, hAlign='LEFT'))
    story.append(Paragraph("2026-2028  •  Imprimible para Tesorería y Cabildo  •  CAPEX + OPEX por programa, flujo trimestral y fuentes", ParagraphStyle('lead', parent=styles['Normal'], fontName=FONT, fontSize=7.5, leading=10, textColor=MUTED, spaceAfter=8)))
    kpis = [[P("<b>5,500,000</b>", s_kpi), P("<b>4,772,000</b>", s_kpi), P("<b>31 MXN</b>", s_kpi), P("<b>40%</b>", s_kpi)],[P("CAPEX total", s_kpi_l), P("OPEX neto año2", s_kpi_l), P("por hab./año", s_kpi_l), P("autosustentable año2", s_kpi_l)]]
    tk = Table(kpis, colWidths=[1.8*inch]*4)
    tk.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), WINE_L), ('BOX', (0,0), (-1,-1), 0.6, LINE), ('INNERGRID', (0,0), (-1,-1), 0.4, LINE), ('ROUNDEDCORNERS', [6,6,6,6]), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
    story.append(tk)
    story.append(Spacer(1, 8))
    info = [[P("<b>Elaboró</b><br/>Eugene L. Buchanan<br/>San Quintín BCN<br/>eugene@serviceofothers.org", s_body), P("<b>Vigencia</b><br/>Precios 2026 (IPC 4.2% BC)<br/>1 USD = 18.8 MXN<br/>IVA incluido", s_body), P("<b>Adjunto a</b><br/>PROPUESTA_INTEGRAL.md<br/>docs/01-08<br/>site/index.html + tablero", s_body)]]
    ti = Table(info, colWidths=[2.0*inch, 1.6*inch, 2.8*inch])
    ti.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), LIGHT_BG), ('BOX', (0,0), (-1,-1), 0.5, LINE), ('INNERGRID', (0,0), (-1,-1), 0.4, LINE), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6), ('LEFTPADDING', (0,0), (-1,-1), 6)]))
    story.append(ti)
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Cómo usar:</b> cada programa trae lista de insumos, CAPEX/OPEX mensual/anual y supuestos auditables. Últimas páginas: resumen 3 años, flujo trimestral piloto y checklist Tesorería. Para editar: <i>PLAN-Y-PRESUPUESTO-DETALLADO.md</i> + <i>presupuesto/csv/*.csv</i>.", ParagraphStyle('use', parent=s_body, fontSize=6, leading=7, textColor=TEAL_D, borderPadding=(4,4,4), backColor=TEAL_L, borderColor=TEAL)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Resumen Ejecutivo — CAPEX (una vez)", ParagraphStyle('h1', parent=styles['Heading1'], fontName=FONTB, fontSize=13, leading=15, textColor=WINE_D, spaceBefore=10, spaceAfter=6)))
    capex = [[P("<b>#</b>", s_th), P("<b>Programa</b>", s_th), P("<b>Concepto principal</b>", s_th), P("<b>Monto</b>", s_th), P("<b>Vida</b>", s_th)],[P("1", s_tc_c), P("—", s_tc_c), P("Fondo inicial Vales (1,000 vales, capital trabajo)", s_tc), P("$1,000,000", s_tc_r), P("rotativo", s_tc_c)],[P("2", s_tc_c), P("Móviles", s_tc_c), P("Remolque 2 mesas reacond. + equipamiento", s_tc), P("$550,000", s_tc_r), P("10a", s_tc_c)],[P("3", s_tc_c), P("CEBISQ", s_tc_c), P("Adecuación 800m² + 2,000m² patios + 5kW solar", s_tc), P("$1,200,000", s_tc_r), P("10a", s_tc_c)],[P("4", s_tc_c), P("Aquamación", s_tc_c), P("PET-400 reacond. + instalación + sala 6m²", s_tc), P("$1,100,000", s_tc_r), P("15a", s_tc_c)],[P("5", s_tc_c), P("Bioliquidadora", s_tc_c), P("Reactor 2,400L móvil 20' + tanques", s_tc), P("$1,350,000", s_tc_r), P("15a", s_tc_c)],[P("6", s_tc_c), P("Guardianes", s_tc_c), P("Kits sombra/agua/cuarentena 20 hogares", s_tc), P("$65,000", s_tc_r), P("3a", s_tc_c)],[P("7", s_tc_c), P("Transversal", s_tc_c), P("Tecnología, mobiliario, señalética", s_tc), P("$45,000", s_tc_r), P("3a", s_tc_c)],[P("", s_tc), P("", s_tc), P("<b>Subtotal CAPEX</b>", s_tc_r), P("<b>$5,310,000</b>", s_tc_r), P("", s_tc)],[P("", s_tc), P("", s_tc), P("Imprevistos 4%", s_tc_r), P("$190,000", s_tc_r), P("", s_tc)],[P("", s_tc), P("<b>TOTAL CAPEX</b>", s_tc_c), P("", s_tc), P("<b>$5,500,000</b>", s_tc_r), P("", s_tc)]]
    story.append(style_table(Table(capex, colWidths=[0.35*inch, 0.9*inch, 3.2*inch, 1.1*inch, 0.7*inch])))
    story.append(Paragraph("Nota: piloto 90d con carpa (85k) en vez de remolque → CAPEX baja a 5.03 MDP (ahorro 465k). Remolque mes 6.", ParagraphStyle('cap', parent=styles['Normal'], fontName=FONTI, fontSize=6, leading=7, textColor=MUTED, alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph("Resumen — OPEX anual régimen (12 meses)", s_h1))
    opex = [[P("<b>Programa</b>", s_th), P("<b>Bruto anual</b>", s_th), P("<b>Ingresos</b>", s_th), P("<b>Neto</b>", s_th), P("<b>% neto</b>", s_th)],[P("1+2 Esterilización 3,600/año", s_tc), P("$3,364,000", s_tc_r), P("$378,000", s_tc_r), P("$2,986,000", s_tc_r), P("63%", s_tc_c)],[P("3 CEBISQ 48+24", s_tc), P("$948,000", s_tc_r), P("$90,000", s_tc_r), P("$858,000", s_tc_r), P("18%", s_tc_c)],[P("4 Aquamación", s_tc), P("$418,000", s_tc_r), P("$480,000", s_tc_r), P("-$62,000", s_tc_r), P("-1%", s_tc_c)],[P("5 Bioliquidadora", s_tc), P("$516,000", s_tc_r), P("$680,000", s_tc_r), P("-$164,000", s_tc_r), P("-3%", s_tc_c)],[P("6 Guardianes 90", s_tc), P("$714,000", s_tc_r), P("$252,000", s_tc_r), P("$462,000", s_tc_r), P("10%", s_tc_c)],[P("7 Transversal", s_tc), P("$692,000", s_tc_r), P("$0", s_tc_r), P("$692,000", s_tc_r), P("15%", s_tc_c)],[P("<b>TOTAL régimen</b>", s_tc), P("<b>$6,652,000</b>", s_tc_r), P("<b>$1,880,000</b>", s_tc_r), P("<b>$4,772,000</b>", s_tc_r), P("100%", s_tc_c)],[P("Año1 piloto 2,200 +40 guard.", s_tc), P("$4,920,000", s_tc_r), P("$1,140,000", s_tc_r), P("$3,780,000", s_tc_r), P("", s_tc_c)],[P("<b>Año2 optim. 40 padrinos</b>", s_tc), P("$6,652,000", s_tc_r), P("$2,450,000", s_tc_r), P("<b>$4,202,000</b>", s_tc_r), P("31 MXN/hab", s_tc_c)]]
    story.append(style_table(Table(opex, colWidths=[2.1*inch, 1.15*inch, 1.15*inch, 1.15*inch, 0.85*inch])))
    story.append(Paragraph("Financiamiento neto año2: Municipal 45% (1,890k) + Padrinazgos 20% (840k) + Aquamación 11% (480k) + Fertilizante 16% (680k) + Donaciones 5% (210k) + Copagos 8% (378k).", s_caption))
    story.append(Paragraph("Supuestos base 2026: IPC 4.2%, MVZ 22k/mes, cuidador 8k, promotora 3,500+bono, diésel 25.8/L, KOH 45/kg. Compra consolidada -12%. Contingencia 5%.", ParagraphStyle('sup', parent=s_body, fontSize=6, leading=7, textColor=MUTED, borderPadding=(4,4,4), backColor=LIGHT_BG, borderColor=LINE)))
    story.append(Paragraph("Programa 1+2 — Esterilización Híbrida (Vales + Quirófanos) — 3,600/año", s_h1))
    hibr = [[P("<b>Canal</b>", s_th), P("<b>Animales</b>", s_th), P("<b>Costo unit.</b>", s_th), P("<b>Subtotal</b>", s_th)],[P("Móvil — 36 jornadas ×50 =1,800", s_tc), P("1,800", s_tc_c), P("$650", s_tc_r), P("$1,170,000", s_tc_r)],[P("Vet afiliada — 1,800 canjes", s_tc), P("1,800", s_tc_c), P("$960 pond.", s_tc_r), P("$1,728,000", s_tc_r)],[P("<b>Total cirugías</b>", s_tc), P("<b>3,600</b>", s_tc_c), P("$805 prom.", s_tc_r), P("$2,898,000", s_tc_r)],[P("Logística móvil (perifoneo, sombra)", s_tc), P("—", s_tc_c), P("—", s_tc_c), P("$186,000", s_tc_r)],[P("Gestión vales (talón, SPEI, audit 10%)", s_tc), P("—", s_tc_c), P("—", s_tc_c), P("$78,000", s_tc_r)],[P("Contingencia 5%", s_tc), P("—", s_tc_c), P("—", s_tc_c), P("$145,000", s_tc_r)],[P("<b>TOTAL BRUTO</b>", s_tc), P("—", s_tc_c), P("—", s_tc_c), P("<b>$3,364,000</b>", s_tc_r)],[P("Copago 30% (1,080×350)", s_tc), P("—", s_tc_c), P("—", s_tc_c), P("-$378,000", s_tc_r)],[P("<b>NETO</b>", s_tc), P("—", s_tc_c), P("—", s_tc_c), P("<b>$2,986,000</b>", s_tc_r)]]
    story.append(style_table(Table(hibr, colWidths=[2.5*inch, 0.9*inch, 1.0*inch, 1.3*inch])))
    story.append(Paragraph("Móvil — por jornada (50 cirugías)", s_h2))
    perj = [[P("<b>Concepto</b>", s_th), P("<b>Unitario</b>", s_th), P("<b>Cant</b>", s_th), P("<b>Por jornada</b>", s_th), P("<b>×36/año</b>", s_th)],[P("MVZ cirujana + anestesista", s_tc), P("$4,500+2,000", s_tc_c), P("1 c/u", s_tc_c), P("$6,500", s_tc_r), P("$234,000", s_tc_r)],[P("Técnicos 2×900", s_tc), P("$900", s_tc_c), P("2", s_tc_c), P("$1,800", s_tc_r), P("$64,800", s_tc_r)],[P("Promotoras 3×400", s_tc), P("$400", s_tc_c), P("3", s_tc_c), P("$1,200", s_tc_r), P("$43,200", s_tc_r)],[P("Insumos (ket, sutura, antibiót.)", s_tc), P("$285", s_tc_c), P("50", s_tc_c), P("$14,250", s_tc_r), P("$513,000", s_tc_r)],[P("Diésel van+planta 25L", s_tc), P("$25.8", s_tc_c), P("25L", s_tc_c), P("$645", s_tc_r), P("$23,220", s_tc_r)],[P("Agua/hielo/RPBI", s_tc), P("—", s_tc_c), P("—", s_tc_c), P("$450", s_tc_r), P("$16,200", s_tc_r)],[P("Difusión (carteles+perifoneo)", s_tc), P("—", s_tc_c), P("—", s_tc_c), P("$640", s_tc_r), P("$23,040", s_tc_r)],[P("<b>Total por jornada</b>", s_tc), P("—", s_tc_c), P("—", s_tc_c), P("<b>$26,485</b>", s_tc_r), P("<b>$953,460</b>", s_tc_r)],[P("Por animal (50/jornada)", s_tc), P("—", s_tc_c), P("—", s_tc_c), P("$529", s_tc_r), P("", s_tc_c)]]
    story.append(style_table(Table(perj, colWidths=[1.85*inch, 0.9*inch, 0.6*inch, 0.95*inch, 0.95*inch])))
    story.append(Paragraph("CAPEX móvil", s_h2))
    capexm = [[P("<b>Ítem</b>", s_th), P("<b>Nuevo</b>", s_th), P("<b>Usado reacond. (rec.)</b>", s_th), P("<b>Vida</b>", s_th)],[P("Remolque 20' 2 mesas, A/C", s_tc), P("$620,000", s_tc_r), P("$320,000", s_tc_r), P("10a", s_tc_c)],[P("Autoclave 18L", s_tc), P("$55,000", s_tc_r), P("$35,000", s_tc_r), P("7a", s_tc_c)],[P("Lámparas LED 2×", s_tc), P("$38,000", s_tc_r), P("$22,000", s_tc_r), P("7a", s_tc_c)],[P("Instrumentales 2 sets", s_tc), P("$72,000", s_tc_r), P("$45,000", s_tc_r), P("5a", s_tc_c)],[P("Planta 5kW + tanque 200L", s_tc), P("$48,000", s_tc_r), P("$32,000", s_tc_r), P("7a", s_tc_c)],[P("Toldo sombra 6×6m + señalética", s_tc), P("$22,000", s_tc_r), P("$18,000", s_tc_r), P("3a", s_tc_c)],[P("Kit TNR 4 trampas", s_tc), P("$18,000", s_tc_r), P("$18,000", s_tc_r), P("5a", s_tc_c)],[P("<b>Total</b>", s_tc), P("$873,000", s_tc_r), P("$490,000", s_tc_r), P("", s_tc_c)],[P("+10% IVA/conting.", s_tc), P("$87,000", s_tc_r), P("$60,000", s_tc_r), P("", s_tc_c)],[P("<b>Total recomendado</b>", s_tc), P("", s_tc), P("<b>$550,000</b>", s_tc_r), P("", s_tc_c)],[P("Opción carpa piloto", s_tc), P("—", s_tc_c), P("$103,000", s_tc_r), P("", s_tc_c)]]
    story.append(style_table(Table(capexm, colWidths=[2.3*inch, 1.05*inch, 1.3*inch, 0.6*inch])))
    story.append(Paragraph("Programa 3 — CEBISQ (48 caniles + 24 gateras)", s_h1))
    capex_ceb = [[P("<b>Partida</b>", s_th), P("<b>Costo</b>", s_th)],[P("Obra ligera 800m² piso lavable, drenaje, epóxica, sombra", s_tc), P("$380,000", s_tc_r)],[P("48 caniles 2×3m (6,500 c/u)", s_tc), P("$312,000", s_tc_r)],[P("Gatera 24 jaulas (4,200 c/u)", s_tc), P("$101,000", s_tc_r)],[P("Cuarentena/lactario 14 + lavandería", s_tc), P("$95,000", s_tc_r)],[P("Patios 2,000m² sombra + bebederos", s_tc), P("$110,000", s_tc_r)],[P("Cisterna 10kL + hidro + calentador", s_tc), P("$68,000", s_tc_r)],[P("Eléctrico + solar 5kW LED", s_tc), P("$72,000", s_tc_r)],[P("Oficina/sala adopción/archivo", s_tc), P("$42,000", s_tc_r)],[P("Señalética + jardín memorial", s_tc), P("$20,000", s_tc_r)],[P("<b>Total CAPEX</b>", s_tc), P("<b>$1,200,000</b>", s_tc_r)]]
    story.append(style_table(Table(capex_ceb, colWidths=[4.6*inch, 1.2*inch])))
    opex_ceb = [[P("<b>Concepto</b>", s_th), P("<b>Mensual</b>", s_th), P("<b>Anual</b>", s_th)],[P("MVZ ½ tiempo", s_tc), P("$11,000", s_tc_r), P("$132,000", s_tc_r)],[P("Cuidadores 4×8,000", s_tc), P("$32,000", s_tc_r), P("$384,000", s_tc_r)],[P("Etóloga 2 visitas/mes", s_tc), P("$3,000", s_tc_r), P("$36,000", s_tc_r)],[P("Croqueta 1,200kg ×38", s_tc), P("$15,200", s_tc_r), P("$182,400", s_tc_r)],[P("Arena gato + latas", s_tc), P("$2,800", s_tc_r), P("$33,600", s_tc_r)],[P("Vacunas 70×85", s_tc), P("$5,950", s_tc_r), P("$71,400", s_tc_r)],[P("Desparasitantes", s_tc), P("$1,800", s_tc_r), P("$21,600", s_tc_r)],[P("Luz (solar 40%)", s_tc), P("$2,200", s_tc_r), P("$26,400", s_tc_r)],[P("Agua 2 pipas", s_tc), P("$1,600", s_tc_r), P("$19,200", s_tc_r)],[P("RPBI + internet + mant. + seguro", s_tc), P("$4,600", s_tc_r), P("$55,200", s_tc_r)],[P("<b>Total bruto</b>", s_tc), P("<b>$79,150</b>", s_tc_r), P("<b>$948,000</b>", s_tc_r)],[P("Adopción 120×300 + alimento donado", s_tc), P("—", s_tc_c), P("-$90,000", s_tc_r)],[P("<b>NETO</b>", s_tc), P("—", s_tc_c), P("<b>$858,000</b>", s_tc_r)]]
    story.append(style_table(Table(opex_ceb, colWidths=[3.2*inch, 1.0*inch, 1.0*inch])))
    story.append(Paragraph("Costo/animal/día: 43.3 MXN (948k / 60 prom ×365). Vs perrera 68 + incineración. Estancia media 18d, ocupación 62%.", s_caption))
    story.append(Paragraph("Programa 4 — Aquamación PET-400", s_h1))
    capex_aqua = [[P("<b>Ítem</b>", s_th), P("<b>Costo</b>", s_th)],[P("PET-400 reacond. (950k) garantía 1a", s_tc), P("$950,000", s_tc_r)],[P("Instalación eléctrica/agua/drenaje/extractor", s_tc), P("$80,000", s_tc_r)],[P("Sala despedida 6m² + kit huellas", s_tc), P("$48,000", s_tc_r)],[P("Urnas stock 100", s_tc), P("$22,000", s_tc_r)],[P("<b>Total</b>", s_tc), P("<b>$1,100,000</b>", s_tc_r)]]
    story.append(style_table(Table(capex_aqua, colWidths=[4.6*inch, 1.2*inch])))
    opex_aqua = [[P("<b>Concepto</b>", s_th), P("<b>Por ciclo 90kg</b>", s_th), P("<b>Anual 300 ciclos</b>", s_th)],[P("KOH 4.5kg×45", s_tc), P("$202", s_tc_r), P("$60,600", s_tc_r)],[P("Electricidad 18kWh×3.2", s_tc), P("$58", s_tc_r), P("$17,400", s_tc_r)],[P("Agua 110L", s_tc), P("$4.4", s_tc_r), P("$1,320", s_tc_r)],[P("Ácido cítrico 0.8kg", s_tc), P("$38", s_tc_r), P("$11,400", s_tc_r)],[P("Mantenimiento", s_tc), P("—", s_tc_c), P("$28,000", s_tc_r)],[P("Análisis trimestral 4×6,500", s_tc), P("—", s_tc_c), P("$26,000", s_tc_r)],[P("Urnas 400×85 + personal + duelo", s_tc), P("—", s_tc_c), P("$126,400", s_tc_r)],[P("<b>Total OPEX + overhead</b>", s_tc), P("—", s_tc_c), P("<b>$418,000</b>", s_tc_r)],[P("Ingresos privada 400×1,250", s_tc), P("—", s_tc_c), P("$480,000", s_tc_r)],[P("<b>Resultado neto</b>", s_tc), P("—", s_tc_c), P("<b>+$62,000</b>", s_tc_r)]]
    story.append(style_table(Table(opex_aqua, colWidths=[2.8*inch, 1.3*inch, 1.3*inch])))
    story.append(Paragraph("Punto equilibrio 260 privadas/año. Piloto 180 servicios (100 privada) → -85k subsidiado.", s_caption))
    story.append(Paragraph("Programa 5 — Bioliquidadora 2,400L + Fertilizante", s_h1))
    capex_bio = [[P("<b>Ítem</b>", s_th), P("<b>Costo</b>", s_th)],[P("Reactor 2,400L + chaqueta + bomba + controles (ENS/MXL)", s_tc), P("$1,100,000", s_tc_r)],[P("Remolque tandem + rampa + tecle", s_tc), P("$150,000", s_tc_r)],[P("Tanques agua/KOH/neutralización", s_tc), P("$50,000", s_tc_r)],[P("Instalación + capacitación 3d", s_tc), P("$50,000", s_tc_r)],[P("<b>Total</b>", s_tc), P("<b>$1,350,000</b>", s_tc_r)]]
    story.append(style_table(Table(capex_bio, colWidths=[4.6*inch, 1.2*inch])))
    opex_bio = [[P("<b>Concepto por ciclo 500kg</b>", s_th), P("<b>Por ciclo</b>", s_th), P("<b>160 ciclos/año (80t)</b>", s_th)],[P("Diésel 60L×25.8", s_tc), P("$1,548", s_tc_r), P("$247,680", s_tc_r)],[P("KOH 6kg×45", s_tc), P("$270", s_tc_r), P("$43,200", s_tc_r)],[P("Agua 800L", s_tc), P("$32", s_tc_r), P("$5,120", s_tc_r)],[P("Transporte 50km", s_tc), P("$600", s_tc_r), P("$96,000", s_tc_r)],[P("Análisis 12×2,800 + mant. 42k + operador 132k", s_tc), P("—", s_tc_c), P("$167,600", s_tc_r)],[P("<b>Total OPEX</b>", s_tc), P("—", s_tc_c), P("<b>$516,000</b>", s_tc_r)],[P("Fertilizante Lote A ahorro 1.28M L×0.15", s_tc), P("—", s_tc_c), P("$192,000", s_tc_r)],[P("Lote B ranchos 1.92M L×0.25", s_tc), P("—", s_tc_c), P("$480,000", s_tc_r)],[P("Ahorro disposición 80t×2,500", s_tc), P("—", s_tc_c), P("$200,000", s_tc_r)],[P("<b>Neto (ingreso 680k)</b>", s_tc), P("—", s_tc_c), P("<b>+$164,000</b>", s_tc_r)]]
    story.append(style_table(Table(opex_bio, colWidths=[2.7*inch, 1.1*inch, 1.5*inch])))
    story.append(Paragraph("Rendimiento 1t →2,500L bruto →40,000L diluido. 80t →1.28M L parques +1.92M L ranchos.", s_caption))
    story.append(Paragraph("Programa 6 — Red de Guardianes (90 régimen / 40 piloto)", s_h1))
    capex_guard = [[P("<b>Kit</b>", s_th), P("<b>Unit.</b>", s_th), P("<b>Cant</b>", s_th), P("<b>Total</b>", s_th)],[P("Lona sombra 3×3m + postes", s_tc), P("$4,200", s_tc_r), P("8", s_tc_c), P("$33,600", s_tc_r)],[P("Bebedero 20L + tarima", s_tc), P("$850", s_tc_r), P("16", s_tc_c), P("$13,600", s_tc_r)],[P("Jaula cuarentena 1×1.5m (préstamo)", s_tc), P("$3,800", s_tc_r), P("4", s_tc_c), P("$15,200", s_tc_r)],[P("Credenciales 40 PVC + señalética", s_tc), P("$45", s_tc_r), P("40", s_tc_c), P("$1,800", s_tc_r)],[P("<b>Total CAPEX inicial</b>", s_tc), P("", s_tc), P("—", s_tc_c), P("<b>$65,000</b>", s_tc_r)]]
    story.append(style_table(Table(capex_guard, colWidths=[2.9*inch, 0.9*inch, 0.6*inch, 1.0*inch])))
    opex_guard = [[P("<b>Subprograma</b>", s_th), P("<b>Mensual 40</b>", s_th), P("<b>Anual 40</b>", s_th), P("<b>Anual 90</b>", s_th)],[P("A. Alimento neto (con 30% donado)", s_tc), P("$23,583", s_tc_r), P("$283,000", s_tc_r), P("$640,000", s_tc_r)],[P("B. Salud vale 30/mes + botiquín", s_tc), P("$9,700", s_tc_r), P("$116,400", s_tc_r), P("$356,400", s_tc_r)],[P("C. Infra reposición", s_tc), P("$900", s_tc_r), P("$10,800", s_tc_r), P("$21,600", s_tc_r)],[P("D. Taller 12×2,800 + WA", s_tc), P("$2,400", s_tc_r), P("$28,800", s_tc_r), P("$45,600", s_tc_r)],[P("E. Relevo + emergencia + ruta + foto", s_tc), P("$4,200", s_tc_r), P("$50,400", s_tc_r), P("$107,700", s_tc_r)],[P("<b>Total bruto</b>", s_tc), P("<b>$40,783</b>", s_tc_r), P("<b>$489,400</b>", s_tc_r), P("<b>$714,000</b>", s_tc_r)],[P("Padrinazgos + donado", s_tc), P("-$10,200", s_tc_r), P("-$122,400", s_tc_r), P("-$252,000", s_tc_r)],[P("<b>NETO</b>", s_tc), P("<b>$30,583</b>", s_tc_r), P("<b>$367,000</b>", s_tc_r), P("<b>$462,000</b>", s_tc_r)]]
    story.append(style_table(Table(opex_guard, colWidths=[2.6*inch, 1.1*inch, 1.1*inch, 1.1*inch])))
    story.append(Paragraph("KPI: 75% esterilizados, 6 adop/guard/año, 85% satisfacción respaldo. Piloto 90d (40×3m): 115,500.", s_caption))
    story.append(Paragraph("Transversales — Coordinación, Tecnología, Auditoría", s_h1))
    trans = [[P("<b>Concepto</b>", s_th), P("<b>Mensual</b>", s_th), P("<b>Anual</b>", s_th)],[P("Coordinadora General", s_tc), P("$18,000", s_tc_r), P("$216,000", s_tc_r)],[P("Contadora + SAT donataria", s_tc), P("$6,000", s_tc_r), P("$72,000", s_tc_r)],[P("Promotoras 8×3,500+bono 500", s_tc), P("$32,000", s_tc_r), P("$384,000", s_tc_r)],[P("Seguro + tecnología (WA Business) + talón", s_tc), P("$4,500", s_tc_r), P("$54,000", s_tc_r)],[P("Auditoría 2×30k + comisiones", s_tc), P("—", s_tc_c), P("$64,800", s_tc_r)],[P("Comunicación + Pasarela 12×4k", s_tc), P("—", s_tc_c), P("$96,000", s_tc_r)],[P("<b>Total año1 sin reserva</b>", s_tc), P("—", s_tc_c), P("<b>$577,000</b>", s_tc_r)],[P("Reserva 3m (1× año1)", s_tc), P("—", s_tc_c), P("$115,000", s_tc_r)],[P("<b>Total año1 con reserva</b>", s_tc), P("—", s_tc_c), P("<b>$692,000</b>", s_tc_r)]]
    story.append(style_table(Table(trans, colWidths=[3.4*inch, 1.0*inch, 1.1*inch])))
    story.append(Paragraph("Resumen 3 años (CAPEX + OPEX neto)", s_h1))
    tres = [[P("<b>Año</b>", s_th), P("<b>CAPEX</b>", s_th), P("<b>OPEX neto</b>", s_th), P("<b>Total</b>", s_th), P("<b>Ingresos</b>", s_th), P("<b>% cub.</b>", s_th)],[P("2026 H2 (6m piloto)", s_tc), P("$5,500,000", s_tc_r), P("$1,890,000", s_tc_r), P("$7,390,000", s_tc_r), P("$570,000", s_tc_r), P("8%", s_tc_c)],[P("2027 régimen 3,600+90", s_tc), P("$120,000", s_tc_r), P("$4,772,000", s_tc_r), P("$4,892,000", s_tc_r), P("$1,880,000", s_tc_r), P("38%", s_tc_c)],[P("2028 escala 4,200+140", s_tc), P("$180,000", s_tc_r), P("$5,180,000", s_tc_r), P("$5,360,000", s_tc_r), P("$2,650,000", s_tc_r), P("49%", s_tc_c)],[P("<b>3a acumulado</b>", s_tc), P("<b>$5,800,000</b>", s_tc_r), P("<b>$11,842,000</b>", s_tc_r), P("<b>$17,642,000</b>", s_tc_r), P("$5,100,000", s_tc_r), P("29%", s_tc_c)]]
    story.append(style_table(Table(tres, colWidths=[1.55*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.0*inch, 0.6*inch])))
    story.append(Paragraph("Costo/hab. neto 2027: 31.0 MXN. Esc. pesimista -30% padrinos/fertilizante =34.5 MXN. Optimista +20% aqua =29.8 MXN.", s_caption))
    story.append(Paragraph("Flujo trimestral piloto 90 días (M3-M5)", ParagraphStyle('h2b', parent=s_h1, fontName=FONTB, fontSize=9.5, leading=12, textColor=WINE_D, spaceBefore=8, spaceAfter=4)))
    flujo = [[P("<b>Trim.</b>", s_th), P("<b>Actividad</b>", s_th), P("<b>Entregable</b>", s_th), P("<b>Costo</b>", s_th)],[P("M3 S1-2", s_tc_c), P("Taller + censo 400 hog. +15 guardianes", s_tc), P("Acta, censo, 15 credenc.", s_tc_c), P("$18,000", s_tc_r)],[P("M3 S3-4", s_tc_c), P("Carpa 2 jornadas + ruta bio demo", s_tc), P("100 cirug., 400L, cat 20", s_tc_c), P("$62,000", s_tc_r)],[P("M4 S1-2", s_tc_c), P("2 jornadas + 300kg alimento + Taller #1", s_tc), P("100 cirug., 15 kits", s_tc_c), P("$58,000", s_tc_r)],[P("M4 S3-4", s_tc_c), P("2 jornadas +10 guard. nuevos + Pasarela #1", s_tc), P("100 cirug., 8 adop.", s_tc_c), P("$61,000", s_tc_r)],[P("M5 S1-2", s_tc_c), P("2 jornadas +10 aqua +4 padrinos", s_tc), P("100 cirug., 10 aqua", s_tc_c), P("$72,000", s_tc_r)],[P("M5 S3-4", s_tc_c), P("2 jornadas + auditoría interna", s_tc), P("80 cirug., informe", s_tc_c), P("$48,000", s_tc_r)],[P("<b>Total 90d OPEX</b>", s_tc_c), P("<b>12 jorn. +40 guard. demo</b>", s_tc), P("<b>580 cirug., 20 adop., 800kg</b>", s_tc_c), P("<b>$319,000</b>", s_tc_r)],[P("CAPEX carpa (no remolque)", s_tc_c), P("—", s_tc_c), P("—", s_tc_c), P("$103,000", s_tc_r)],[P("<b>Flujo total 90d</b>", s_tc_c), P("—", s_tc_c), P("—", s_tc_c), P("<b>$422,000</b>", s_tc_r)]]
    story.append(style_table(Table(flujo, colWidths=[0.75*inch, 2.2*inch, 1.65*inch, 0.9*inch])))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Para imprimir: cada programa ocupa 1 página con tabla línea por línea, total y firma. Código partida FAIS y QR tablero en PDF incluyen espacio firma Tesorería/AC.", ParagraphStyle('imp', parent=s_body, fontSize=6, leading=7, textColor=MUTED, borderPadding=(4,4,4), backColor=LIGHT_BG, borderColor=LINE)))
    story.append(Paragraph("Checklist Tesorería", ParagraphStyle('h2c', parent=s_h1, fontName=FONTB, fontSize=9.5, leading=12, textColor=WINE_D, spaceBefore=8, spaceAfter=4)))
    checks = ["Aprobación Cabildo partida etiquetada <b>“Bienestar Animal — Red de Vida”</b> 3.78M (año1 piloto escalado) en Presupuesto Egresos 2026.","Firma Convenio Marco AC-Ayuntamiento (3 años) + apertura cuenta mancomunada 2 firmas (BBVA/Santander).","Liberación 422k piloto 90d contra entregables (ver flujo trimestral) — SPEI con QR tablero.","Captación 15 padrinos mes 3-5 (ranchos/empacadoras/hoteles) — Coordinadora.","Auditoría mes 6 y publicación tablero + ajuste tabulador IPC febrero."]
    for ch in checks:
        story.append(Paragraph(f"☐  {ch}", ParagraphStyle('bullet2', parent=s_body, fontName=FONT, fontSize=6.5, leading=8, leftIndent=10)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Anexos — Proveedores auditables: Vet SQ/Vet Mascotas/Vet del Valle/Vet Camalú (tabulador firmado), Taller Acero Inox ENS (490k), Bio-Response Indiana (950k reacond.), Química ENS KOH 45/kg, Empacadora Berry Veg (merma pollo 12t/año), Despacho ENS auditor 60k/año. Ajuste IPC: cláusula convenio actualiza tabuladores cada febrero con INPC BC.", ParagraphStyle('anex', parent=s_body, fontSize=6, leading=7, textColor=MUTED)))
    story.append(Spacer(1, 6))
    cta = [[P("<b>Siguiente paso — Taller 1 día en 30 días</b><br/><font size=5>4 guardianes + Huellitas SQ + 2 vets + Jurisdicción #4 + Desarrollo Rural  •  Vte. Guerrero / L. Cárdenas</font>", ParagraphStyle('cta1', parent=s_body, fontSize=7, leading=8, textColor=colors.white)), P("<b><font color='#ffffff'>eugene@serviceofothers.org</font></b><br/><font size=5 color='#C5A880'>Asunto: QUIERO TEJER + tu colonia</font>", ParagraphStyle('cta2', parent=s_body, fontSize=7, leading=7, textColor=colors.white, alignment=TA_RIGHT))]]
    tcta = Table(cta, colWidths=[4.4*inch, 1.8*inch])
    tcta.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), WINE), ('ROUNDEDCORNERS', [6,6,6,6]), ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8), ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8)]))
    story.append(tcta)
    story.append(Spacer(1, 4))
    story.append(Paragraph("Documento vivo v1.0 — 10 ago 2026. Editar markdown y regenerar: <i>python3 build_presupuesto_pdf.py</i>. CSVs en <i>presupuesto/csv/</i> para Excel. CC BY-SA 4.0. Diseñado en San Quintín, para San Quintín.", s_caption))
    doc.build(story, onFirstPage=hdr_footer, onLaterPages=hdr_footer)
    print(f"PDF presupuesto generado: {out}")
if __name__ == "__main__":
    build()
