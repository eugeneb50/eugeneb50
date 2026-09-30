#!/usr/bin/env python3
"""Tailored cover letter: Nexaminds Senior Backend QA Engineer (AI System Validation).

Light restyle matching the KoBold letter (light grey header, circular photo
with segmented color ring, satellite icon bubbles, two-column body, magenta
salutation) — short, one page. Honest mapping: no Karate, ADK, MCP-application,
LLM-as-Judge, contract-testing, or retail claims (none in ressoft26.txt).
Transfers Postman + REST/API-boundary depth, white-box source reading,
structured test planning, shift-left local-env practice, and evaluation
foundations (RAG + guardrails, ZeroClaw routing/cost/lifecycle), with a ramp.
Outputs Eugene_Buchanan_Cover_Letter_Nexaminds.pdf
"""

import math
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer, Flowable,
                                NextPageTemplate)

import reportlab.rl_config as _rl_config
_rl_config.documentLang = "en-US"

# ----------------------------------------------------------------------------
# Fonts (same DejaVu set as build_cover.py)
# ----------------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/TTF"
for _reg, _f in (("DJ", "DejaVuSans.ttf"),
                 ("DJ-B", "DejaVuSans-Bold.ttf"),
                 ("DJ-I", "DejaVuSans-Oblique.ttf")):
    try:
        pdfmetrics.registerFont(TTFont(_reg, os.path.join(FONT_DIR, _f)))
    except Exception:
        pass
try:
    pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B",
                                  italic="DJ-I", boldItalic="DJ-B")
except Exception:
    pass

FONT, FONT_B, FONT_I = "DJ", "DJ-B", "DJ-I"

# ----------------------------------------------------------------------------
# Light palette (Venngage-inspired, same as KoBold letter)
# ----------------------------------------------------------------------------
HDR_BG   = colors.HexColor("#E9E9EC")
INK      = colors.HexColor("#2b2b2e")
SUBGREY  = colors.HexColor("#8a8a90")
MUTEGREY = colors.HexColor("#6f6f76")
MAGENTA  = colors.HexColor("#9c2b6e")
DEEPPURP = colors.HexColor("#4b0f5d")
PEACH    = colors.HexColor("#f2b26b")
ROSE     = colors.HexColor("#c05a78")
CORAL    = colors.HexColor("#e07a5f")
BUBBLE_BG = colors.white
BUBBLE_LN = colors.HexColor("#d8d8dc")
CONN_LN   = colors.HexColor("#cfcfd4")
RULE_C    = colors.HexColor("#c9c9ce")

PW, PH = letter
ML = MR = 48
FW = PW - ML - MR
HEADER_H = 208
TOP_GAP = 6
BODY_BOTTOM = 40

RING_COLORS = [PEACH, DEEPPURP, MAGENTA, ROSE, CORAL]
BUBBLES = [
    ("API", -130,  25),
    ("Eval", -118, -48),
    ("RAG",  148,  72),
    ("Rust",  150,   4),
    ("QA",   128, -58),
]


def make_circular_photo(src_jpg, size=300):
    """Circular-cropped PNG of pic.jpg (larger source so the big ring stays crisp)."""
    try:
        from PIL import Image, ImageDraw
        import tempfile
        im = Image.open(src_jpg).convert("RGBA")
        w, h = im.size
        m = min(w, h)
        _resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS", 1)
        im = im.crop(((w - m) // 2, (h - m) // 2,
                      (w + m) // 2, (h + m) // 2)).resize((size, size), _resample)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
        im.putalpha(mask)
        fd, path = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        im.save(path, "PNG")
        return path
    except Exception:
        return None


class LightHead(Flowable):
    """Venngage-style light header: grey band, name/contact left, large
    segmented-ring photo center, white icon bubbles on spokes."""

    def __init__(self, width=PW, height=HEADER_H, photo=None):
        super().__init__()
        self.width = width
        self.height = height
        self.photo = photo

    def _contact_row(self, c, x, y, glyph, text):
        c.setStrokeColor(INK)
        c.setLineWidth(1.1)
        c.circle(x + 8, y + 4, 8, fill=0, stroke=1)
        c.setFillColor(INK)
        c.setFont(FONT_B, 7.5)
        c.drawCentredString(x + 8, y + 1.5, glyph)
        c.setFillColor(MUTEGREY)
        c.setFont(FONT, 8.5)
        c.drawString(x + 21, y, text)
        return pdfmetrics.stringWidth(text, FONT, 8.5)

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        c.setFillColor(HDR_BG)
        c.rect(0, 0, W, H, fill=1, stroke=0)

        c.setFillColor(INK)
        c.setFont(FONT_B, 24)
        c.drawString(28, H - 44, "Eugene L. Buchanan")
        c.setFillColor(SUBGREY)
        c.setFont(FONT_I, 11)
        c.drawString(28, H - 62, "Senior Backend QA \u2014 AI System Validation")
        cy = H - 84
        self._contact_row(c, 28, cy, "T", "+1 (909) 545 5384")
        cy -= 20
        self._contact_row(c, 28, cy, "E", "eugene@serviceofothers.org")
        cy -= 20
        self._contact_row(c, 28, cy, "G", "github.com/eugeneb50")

        pcx, pcy, pr = W / 2 + 60, 90, 55
        segs = len(RING_COLORS)
        c.setLineWidth(11)
        c.setLineCap(1)
        for i, col in enumerate(RING_COLORS):
            c.setStrokeColor(col)
            c.arc(pcx - pr - 7, pcy - pr - 7, pcx + pr + 7, pcy + pr + 7,
                  i * 360.0 / segs, 360.0 / segs)
        if self.photo and os.path.exists(self.photo):
            try:
                c.drawImage(self.photo, pcx - pr, pcy - pr, 2 * pr, 2 * pr,
                            preserveAspectRatio=True, anchor="c", mask="auto")
            except Exception:
                c.setFillColor(DEEPPURP)
                c.circle(pcx, pcy, pr, fill=1, stroke=0)
                c.setFillColor(colors.white)
                c.setFont(FONT_B, 22)
                c.drawCentredString(pcx, pcy - 8, "EB")
        else:
            c.setFillColor(DEEPPURP)
            c.circle(pcx, pcy, pr, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont(FONT_B, 22)
            c.drawCentredString(pcx, pcy - 8, "EB")

        br = 22
        for (label, dx, dy), col in zip(BUBBLES, RING_COLORS * 2):
            bx, by = pcx + dx, pcy + dy
            ang = math.atan2(dy, dx)
            x1 = pcx + (pr + 12) * math.cos(ang)
            y1 = pcy + (pr + 12) * math.sin(ang)
            x2 = bx - (br + 1) * math.cos(ang)
            y2 = by - (br + 1) * math.sin(ang)
            c.setStrokeColor(CONN_LN)
            c.setLineWidth(1.0)
            c.line(x1, y1, x2, y2)
            c.setFillColor(BUBBLE_BG)
            c.setStrokeColor(BUBBLE_LN)
            c.setLineWidth(0.8)
            c.circle(bx, by, br, fill=1, stroke=1)
            c.setFillColor(DEEPPURP)
            c.setFont(FONT_B, 9 if len(label) <= 2 else 7.5)
            c.drawCentredString(bx, by - 3, label)


# ----------------------------------------------------------------------------
# Light body styles (ragged-left like the template, not justified)
# ----------------------------------------------------------------------------
date_style = ParagraphStyle("ldate", fontName=FONT, fontSize=8.6, leading=11,
                            textColor=INK, alignment=TA_LEFT, spaceAfter=2)
addr_style = ParagraphStyle("laddr", fontName=FONT, fontSize=8.4, leading=10.5,
                            textColor=MUTEGREY, alignment=TA_LEFT, spaceAfter=0)
salute_style = ParagraphStyle("lsal", fontName=FONT_B, fontSize=12, leading=15,
                              textColor=MAGENTA, spaceBefore=2, spaceAfter=6)
subj_style = ParagraphStyle("lsubj", fontName=FONT_B, fontSize=11, leading=14,
                            textColor=INK, spaceBefore=2, spaceAfter=4)
body_style = ParagraphStyle("lbody", fontName=FONT, fontSize=10.5, leading=14.5,
                            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=5)
fit_title = ParagraphStyle("lfit", fontName=FONT_B, fontSize=8.4, leading=10.5,
                           textColor=INK, spaceAfter=0)
fit_desc = ParagraphStyle("lfitd", fontName=FONT, fontSize=8.1, leading=10.5,
                          textColor=MUTEGREY, spaceAfter=3)
sign2_style = ParagraphStyle("lsign2", fontName=FONT, fontSize=8.2, leading=10.5,
                             textColor=MUTEGREY, spaceAfter=0)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE_C)
    canvas.setLineWidth(0.6)
    canvas.line(ML, 36, PW - MR, 36)
    canvas.setFont(FONT, 7.5)
    canvas.setFillColor(SUBGREY)
    canvas.drawString(ML, 24,
        "Eugene L. Buchanan  \u00b7  eugene@serviceofothers.org  \u00b7  +1 (909) 545 5384  \u00b7  github.com/eugeneb50")
    canvas.drawRightString(PW - MR, 24, "Page %d" % doc.page)
    canvas.restoreState()


LETTER_DATE = "September 16, 2026"

RECIPIENT = [
    "Nexaminds Hiring Team",
    "Senior Backend QA Engineer \u2014 AI System Validation (Canada)",
]

SUBJECT = "Re: Senior Backend QA \u2014 API Automation, AI Agent Validation"

PARAGRAPHS = [
    "I am applying for your Senior Backend QA Engineer role. You validate "
    "AI systems where exact-match assertions fail \u2014 and that is "
    "exactly where I do my best work.",

    "At Knowledgecity (Dec 2020\u2013Aug 2025) I hired and trained the "
    "automation team and ran the CI/CD quality pipeline with Cypress, "
    "Selenium, Postman, and JUnit.",

    "I test at service boundaries: REST APIs, webhooks, SFTP, SAML and "
    "OAuth across SAP, Oracle, Workday \u2014 with concise test plans "
    "from dense requirements.",

    "I shift left: local-env setup, white-box code reading for dependencies "
    "and upstream impacts, dashboards and alerting over complex deployments.",

    "On ZeroClaw's 32.8k-star Rust gateway I ship agent infrastructure: "
    "context-window routing, cost attribution, lifecycle observability \u2014 "
    "scoring behavior, not just output.<br/>"
    '<a href="https://github.com/eugeneb50">github.com/eugeneb50</a>',

    "My API automation base \u2014 Postman plus Cypress/Selenium/JUnit over "
    "REST/SQL pipelines \u2014 maps directly onto Karate conventions, and my "
    "daily agent-infrastructure work ramps fast into ADK and MCP validation.",

    "I am ready to work. I communicate directly, plan precisely, and build "
    "frameworks where deterministic tools stop.",
]

# (bubble tag, title, desc) — tags echo the header bubbles
QUALIFICATIONS = [
    ("API", "Backend API automation",
     "Postman manual + automated REST; OpenAPI suites; service-boundary judgment."),
    ("Eval", "AI validation",
     "RAG + guardrails under SOC 2; routing, cost, lifecycle scoring in gateway."),
    ("Rust", "White-box + shift-left",
     "Code reading, dependency mapping, local-env testing, dashboards."),
    ("QA", "Karate + ADK ramp",
     "Cypress/Selenium discipline into Karate; agent loops into ADK/MCP."),
]

CLOSING = (
    "You redefine industries with AI. I hold non-deterministic systems to "
    "production standards. Happy to walk through any PR."
)


def fit_cell(tag, title, desc):
    dot = '<font color="#4b0f5d"><b>\u25cf %s</b></font>  <b>%s.</b>' % (tag, title)
    return [Paragraph(dot, fit_title), Paragraph(desc, fit_desc)]


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Cover_Letter_Nexaminds.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP,
                          bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Cover Letter (Nexaminds Senior Backend QA)",
                          author="Eugene L. Buchanan",
                          subject="Application: Nexaminds Senior Backend QA Engineer, AI Validation",
                          keywords="Cover Letter, Nexaminds, Backend QA, API automation, Postman, AI validation, ZeroClaw, Rust, SDET")
    header_frame = Frame(0, PH - HEADER_H, PW, HEADER_H, leftPadding=0,
                         rightPadding=0, topPadding=0, bottomPadding=0, id="hdr")
    letter_body = Frame(ML, BODY_BOTTOM, FW,
                        (PH - HEADER_H - TOP_GAP) - BODY_BOTTOM,
                        leftPadding=0, rightPadding=0, topPadding=0,
                        bottomPadding=0, id="lbody")
    cont_body = Frame(ML, BODY_BOTTOM, FW, PH - BODY_BOTTOM - BODY_BOTTOM,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                      id="cbody")

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[header_frame, letter_body], onPage=footer),
        PageTemplate(id="content", frames=[cont_body], onPage=footer),
    ])

    story = []
    photo_path = make_circular_photo(os.path.join(out_dir, "pic.jpg"))
    story.append(LightHead(photo=photo_path))
    story.append(NextPageTemplate("content"))
    story.append(Spacer(1, 2))

    story.append(Paragraph(LETTER_DATE, date_style))
    rule = Table([[""]], colWidths=[FW])
    rule.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.7, RULE_C),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story.append(rule)
    for line in RECIPIENT:
        story.append(Paragraph(line, addr_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(SUBJECT, subj_style))
    story.append(Paragraph("Dear Nexaminds Hiring Team,", salute_style))

    # -- two-column justified body --
    left = [Paragraph(p, body_style) for p in PARAGRAPHS[:4]]
    right = [Paragraph(p, body_style) for p in PARAGRAPHS[4:]]
    half = (FW - 18) / 2.0
    two_col = Table([[left, right]], colWidths=[half, half])
    two_col.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 18),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(two_col)
    story.append(Spacer(1, 2))

    story.append(Paragraph("How I fit this role:", subj_style))
    half = (FW - 18) / 2.0
    grid = Table([[fit_cell(*QUALIFICATIONS[0]), fit_cell(*QUALIFICATIONS[1])],
                  [fit_cell(*QUALIFICATIONS[2]), fit_cell(*QUALIFICATIONS[3])]],
                 colWidths=[half, half])
    grid.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(grid)

    story.append(Paragraph("Sincerely, Eugene L. Buchanan", body_style))
    story.append(Paragraph("Senior Backend QA Engineer \u2014 AI System Validation", sign2_style))
    story.append(Paragraph('Apple Valley, CA (Remote)  \u00b7  eugene@serviceofothers.org  \u00b7  <a href="https://github.com/eugeneb50">github.com/eugeneb50</a>', sign2_style))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
