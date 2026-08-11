#!/usr/bin/env python3
"""Generate a visually dynamic cover-letter PDF for Eugene L. Buchanan
   targeted at ClickUp — Staff AI Engineer, Multi-Agent Frameworks.
   Uses the same design system as build_resume_clickup.py (gradient header,
   accent bars, tag strip) but laid out as a letter.
"""

import os
import tempfile
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer,
                                NextPageTemplate, KeepTogether, Flowable)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF

import reportlab.rl_config as _rl_config
_rl_config.documentLang = "en-US"   # PDF /Lang catalog entry (a11y + l10n)

# ----------------------------------------------------------------------------
# Fonts
# ----------------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/TTF"
pdfmetrics.registerFont(TTFont("DJ", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJ-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DJ-I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ-I", boldItalic="DJ-B")

# ----------------------------------------------------------------------------
# Palette (same as resume)
# ----------------------------------------------------------------------------
NAVY    = colors.HexColor("#1a1342")
NAVY2   = colors.HexColor("#2b1d63")
PURPLE  = colors.HexColor("#7b2cf2")
PINK    = colors.HexColor("#fb2e8e")
TEAL    = colors.HexColor("#15a39a")
TEAL_D  = colors.HexColor("#0e7c75")
LIGHT   = colors.HexColor("#f0eaff")
GREY    = colors.HexColor("#5b6b7b")
DARK    = colors.HexColor("#16202b")
INK     = colors.HexColor("#2b3640")
MUTE    = colors.HexColor("#8a98a6")
RULE    = colors.HexColor("#d4dce4")

FONT    = "DJ"
FONT_B  = "DJ-B"
FONT_I  = "DJ-I"

# ----------------------------------------------------------------------------
# Page geometry
# ----------------------------------------------------------------------------
PW, PH = letter
ML = MR = 48
HEADER_H = 110
TOP_GAP = 10
BODY_BOTTOM = 44
FW = PW - ML - MR

# ----------------------------------------------------------------------------
# Gradient & photo helpers (copied from resume for visual consistency)
# ----------------------------------------------------------------------------
def make_circular_photo(src_jpg, size=240):
    try:
        im = Image.open(src_jpg).convert("RGBA")
        w, h = im.size
        m = min(w, h)
        left, top = (w - m) // 2, (h - m) // 2
        im = im.crop((left, top, left + m, top + m)).resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
        im.putalpha(mask)
        fd, path = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        im.save(path, "PNG")
        return path
    except Exception:
        return None

def draw_gradient(c, x, y, w, h, c1, c2, vertical=True, steps=48):
    for i in range(steps):
        t = i / (steps - 1)
        r = c1.red + (c2.red - c1.red) * t
        g = c1.green + (c2.green - c1.green) * t
        b = c1.blue + (c2.blue - c1.blue) * t
        col = colors.Color(r, g, b)
        c.setFillColor(col)
        if vertical:
            yy = y + h * (i / steps)
            c.rect(x, yy, w, h / steps + 1, stroke=0, fill=1)
        else:
            xx = x + w * (i / steps)
            c.rect(xx, y, w / steps + 1, h, stroke=0, fill=1)

# ----------------------------------------------------------------------------
# Header band (compact version for letterhead)
# ----------------------------------------------------------------------------
class LetterHead(Flowable):
    def __init__(self, width=PW, height=HEADER_H, photo=None):
        super().__init__()
        self.width = width
        self.height = height
        self.photo = photo

    def _draw_monogram(self, c, pcx, pcy, pr):
        c.setFillColor(NAVY2)
        c.rect(pcx - pr, pcy - pr, 2 * pr, 2 * pr, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_B, 24)
        c.drawCentredString(pcx, pcy - 8, "EB")

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        draw_gradient(c, 0, 0, W, H, PURPLE, NAVY, vertical=True)
        draw_gradient(c, 0, 0, 6, H, PINK, TEAL, vertical=True, steps=24)

        pcx, pcy, pr = W - 42, H - 40, 30
        if self.photo and os.path.exists(self.photo):
            try:
                c.drawImage(self.photo, pcx - pr, pcy - pr, 2 * pr, 2 * pr,
                            preserveAspectRatio=True, anchor="c", mask="auto")
            except Exception:
                self._draw_monogram(c, pcx, pcy, pr)
        else:
            self._draw_monogram(c, pcx, pcy, pr)
        c.setStrokeColor(colors.white); c.setLineWidth(2)
        c.circle(pcx, pcy, pr, fill=0, stroke=1)

        c.setFillColor(colors.white)
        c.setFont(FONT_B, 24)
        c.drawString(28, H - 42, "EUGENE L. BUCHANAN")
        c.setFillColor(colors.HexColor("#e0cfff"))
        c.setFont(FONT, 11)
        c.drawString(28, H - 62, "Staff AI Engineer  \u2014  Multi-Agent Frameworks & Agentic Infrastructure")
        # contact
        c.setFillColor(colors.HexColor("#eaeafa")); c.setFont(FONT, 8)
        c.drawString(28, H - 82, "Apple Valley, CA (Remote)  \u00b7  +1 (909) 545 5384  \u00b7  eugene@serviceofothers.org  \u00b7  github.com/eugeneb50")
        # separator
        c.setStrokeColor(colors.white); c.setFillAlpha(0.25); c.setLineWidth(0.5)
        c.line(28, H - 95, pcx - pr - 10, H - 95); c.setFillAlpha(1)


class AccentRule(Flowable):
    """Thin gradient accent line between sections of the letter."""
    def __init__(self, width=FW, height=4):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, a, h):
        self.width = a
        return (a, self.height)

    def draw(self):
        c = self.canv
        draw_gradient(c, 0, 0, self.width, self.height, PURPLE, PINK,
                      vertical=False, steps=32)


class ProfitChart(Flowable):
    """Parabolic value bar chart: 'ClickUp's Value Hiring Eugene' (VerticalBarChart)."""
    def __init__(self, title, labels, values, width=FW, height=190):
        super().__init__()
        self.width = width
        self.height = height
        self.title = title
        self.labels = labels
        self.values = values

    def wrap(self, a, h):
        return (self.width, self.height)

    def draw(self):
        from reportlab.graphics.shapes import String, Group, PolyLine

        d = Drawing(self.width, self.height)
        # title first (paragraph-free, rendered as a graphic text)
        d.add(String(self.width / 2, self.height - 14, self.title,
                     fontName=FONT_B, fontSize=9.5, fillColor=NAVY2,
                     textAnchor="middle"))

        bc = VerticalBarChart()
        bc.x = 24
        bc.y = 30
        bc.width = self.width - 48
        bc.height = self.height - 56
        bc.data = [self.values]
        bc.categoryAxis.categoryNames = self.labels
        bc.categoryAxis.labels.fontName = FONT_B
        bc.categoryAxis.labels.fontSize = 6.4
        bc.categoryAxis.labels.fillColor = NAVY2
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = max(self.values) * 1.12
        bc.valueAxis.valueStep = 50
        bc.valueAxis.labelTextFormat = "%.0f"
        bc.valueAxis.labels.fontName = FONT
        bc.valueAxis.labels.fontSize = 6.0
        bc.valueAxis.labels.fillColor = GREY
        for i, v in enumerate(self.values):
            bc.bars[i].fillColor = PURPLE
            bc.bars[i].strokeColor = PINK
            bc.bars[i].strokeWidth = 0.6
        # parabolic curve over the bars
        pts = []
        n = len(self.values)
        for i, v in enumerate(self.values):
            xx = bc.x + bc.width * (i + 0.5) / n
            yy = bc.y + (v / (max(self.values) * 1.12)) * bc.height
            pts.append((xx, yy))
        pc = Group()
        pc.add(PolyLine(pts, strokeColor=PINK, strokeWidth=1.4,
                        strokeDashArray=[2, 1.5]))
        d.add(bc)
        d.add(pc)
        renderPDF.draw(d, self.canv, 0, 0)


# ----------------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------------
date_style = ParagraphStyle("date", fontName=FONT, fontSize=8.6, leading=11,
                            textColor=GREY, alignment=TA_LEFT, spaceAfter=7)
addr_style = ParagraphStyle("addr", fontName=FONT, fontSize=8.8, leading=11,
                            textColor=INK, alignment=TA_LEFT, spaceAfter=1)
subj_style = ParagraphStyle("subj", fontName=FONT_B, fontSize=10.5, leading=14,
                           textColor=NAVY2, spaceBefore=4, spaceAfter=6)
body_style = ParagraphStyle("body", fontName=FONT, fontSize=9.1, leading=12.6,
                            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6,
                            firstLineIndent=0)
salute_style = ParagraphStyle("salute", fontName=FONT, fontSize=9.2, leading=12.6,
                              textColor=INK, spaceAfter=6)
sign_style = ParagraphStyle("sign", fontName=FONT_B, fontSize=10, leading=13,
                           textColor=NAVY2, spaceBefore=6, spaceAfter=0)
sign2_style = ParagraphStyle("sign2", fontName=FONT, fontSize=8.3, leading=10.5,
                            textColor=GREY, spaceAfter=0)

# ----------------------------------------------------------------------------
# Letter content — targeted at ClickUp
# ----------------------------------------------------------------------------
LETTER_DATE = "August 11, 2026"

RECIPIENT = [
    "ClickUp Hiring Team",
    "AI Platform \u2014 Staff AI Engineer, Multi-Agent Frameworks",
    "Via: clickup.com/careers",
]

SUBJECT = "Re: Staff AI Engineer \u2014 Multi-Agent Frameworks (#LI-REMOTE)"

PARAGRAPHS = [
    "I'm applying for the Staff AI Engineer \u2014 Multi-Agent Frameworks role on your AI "
    "Platform team. I build backend platforms where users create, deploy, and coordinate "
    "intelligent agents. That work needs full context for humans and agents to act side by "
    "side \u2014 exactly the problem I've been solving in production.",

    "On ZeroClaw's 32.2k-star Rust gateway, I ship multi-agent orchestration. An observer "
    "reports agent lifecycle state \u2014 idle, working, blocked, released \u2014 through JSON-RPC "
    "over Unix domain sockets (PR #8337). A merged context-window meter unifies 9 LLM "
    "providers \u2014 OpenAI, Anthropic, Cohere, and more \u2014 into one source of truth. That drives "
    "model routing and cost attribution (PR #7946). I prototype workflows with LangGraph, "
    "build MCP servers in Rust, and cover the backend stack (Rust, Python, Node on "
    "PostgreSQL/AWS).",

    "At Knowledgecity, I owned integrations as Product Owner. I shipped SAP, Oracle, Workday, "
    "UKG, Coursera, and Zoom over SAML, OAuth, SFTP, and REST APIs. Each service uses "
    "different auth and error semantics \u2014 the same coordination puzzle that multi-agent "
    "frameworks solve. I also built evaluation tooling (Cypress, Selenium, JUnit, health "
    "dashboards, alerting) to test complex deployments at the system level. I handled AI "
    "privacy (deny-by-default permissions, principal isolation, OIDC) and tied in search "
    "(Elasticsearch, PostgreSQL) \u2014 27 years of it.",
]

QUALIFICATIONS = [
    ("Multi-Agent Frameworks & orchestration",
     "Agent lifecycle observer, LangGraph workflows, and an MCP server in a 32k-star Rust gateway."),
    ("Multiple LLMs & model routing",
     "OpenAI, Anthropic, Cohere, Gemini \u2014 one context window and per-provider cost attribution."),
    ("Evaluation frameworks",
     "27 years testing complex systems; evaluation at both agent and system-level dynamics."),
    ("AI privacy & search",
     "Deny-by-default permissions, principal isolation; Elasticsearch and Postgres full-text."),
]

CHART_TITLE = "ClickUp's Value Hiring Eugene"

CLOSING = (
    "I'm AI-native the way ClickUp means it: I use agents daily, I build the infrastructure "
    "they run on, and I evaluate their behavior under real-world complexity. I'd welcome the "
    "chance to bring that to your AI Platform team \u2014 happy to walk through any PR in an interview."
)

# ----------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE); canvas.setLineWidth(0.6)
    canvas.line(ML, 36, PW - MR, 36)
    canvas.setFont(FONT, 7.5); canvas.setFillColor(MUTE)
    canvas.drawString(ML, 24,
        "Eugene L. Buchanan  \u00b7  eugene@serviceofothers.org  \u00b7  +1 (909) 545 5384  \u00b7  github.com/eugeneb50")
    canvas.drawRightString(PW - MR, 24, "Page %d" % doc.page)
    canvas.restoreState()


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "ClickUp_Eugene_Buchanan_Cover_Letter.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP, bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Cover Letter (ClickUp)",
                          author="Eugene L. Buchanan",
                          subject="Application: Staff AI Engineer \u2014 Multi-Agent Frameworks (Apple Valley, CA)",
                          keywords="Cover Letter, Staff AI Engineer, Multi-Agent Frameworks, LangGraph, LLM, ClickUp")
    header_frame = Frame(0, PH - HEADER_H, PW, HEADER_H, leftPadding=0,
                         rightPadding=0, topPadding=0, bottomPadding=0, id="hdr")
    letter_body = Frame(ML, BODY_BOTTOM, FW, (PH - HEADER_H - TOP_GAP) - BODY_BOTTOM,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                        id="lbody")
    cont_body = Frame(ML, BODY_BOTTOM, FW, PH - BODY_BOTTOM - BODY_BOTTOM,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                      id="cbody")

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[header_frame, letter_body], onPage=footer),
        PageTemplate(id="content", frames=[cont_body], onPage=footer),
    ])

    story = []
    photo_path = make_circular_photo(os.path.join(out_dir, "pic.jpg"))
    story.append(LetterHead(photo=photo_path))
    story.append(NextPageTemplate("content"))
    story.append(Spacer(1, 4))

    # ── Date & recipient block ────────────────────────────────────
    story.append(Paragraph(LETTER_DATE, date_style))
    for line in RECIPIENT:
        story.append(Paragraph(line, addr_style))
    story.append(Spacer(1, 4))

    # ── Subject ────────────────────────────────────────────────────
    story.append(Paragraph(SUBJECT, subj_style))
    story.append(AccentRule())
    story.append(Spacer(1, 6))

    # ── Salutation ─────────────────────────────────────────────────
    story.append(Paragraph("Dear ClickUp AI Platform Team,", salute_style))

    # ── Body paragraphs ────────────────────────────────────────────
    for para in PARAGRAPHS:
        story.append(Paragraph(para, body_style))

    # ── Role fit: parabolic value chart + qualification bullets side-by-side ──
    story.append(Paragraph("How I fit this role:", subj_style))
    qual_style = ParagraphStyle("qual", fontName=FONT, fontSize=8.4, leading=11.4,
                                leftIndent=12, bulletIndent=2, bulletColor=PURPLE,
                                spaceAfter=3.5, textColor=INK)
    qual_col = []
    for title, desc in QUALIFICATIONS:
        txt = f'<b><font color="#2b1d63">{title}.</font></b>  {desc}'
        qual_col.append(Paragraph(txt, qual_style, bulletText="\u2022"))
    chart_col = [ProfitChart(
        CHART_TITLE,
        ["Yr 1", "Yr 2", "Yr 3", "Yr 4", "Yr 5", "Yr 6"],
        [10, 42, 96, 172, 270, 390],
        width=190, height=150)]
    fit_table = Table([[qual_col, chart_col]], colWidths=[FW - 190, 190])
    fit_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(fit_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph(CLOSING, body_style))
    story.append(Spacer(1, 3))

    # ── Sign-off ───────────────────────────────────────────────────
    story.append(Paragraph("Best regards,", body_style))
    story.append(Spacer(1, 3))
    story.append(AccentRule(width=180))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Eugene L. Buchanan", sign_style))
    story.append(Paragraph("Staff AI Engineer \u2014 Multi-Agent Frameworks", sign2_style))
    story.append(Paragraph("Apple Valley, CA  \u00b7  eugene@serviceofothers.org  \u00b7  github.com/eugeneb50", sign2_style))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
