#!/usr/bin/env python3
"""Tailored cover letter: KoBold Metals Software Engineer (Data Systems Engineering).

Light restyle inspired by Venngage light-college cover template
(light grey header, circular photo with segmented color ring, satellite icon
bubbles, two-column body, magenta salutation) — content unchanged and honest:
no Django/Prefect/Retool, geology degree, or mining-employment claim
(none in ressoft26.txt). Transfers Python + AWS + React pipeline practice,
RAG/evaluation depth, map-based work, and an independent spectral/satellite
prospecting tool, plus lifelong prospecting passion and eagerness for field
time in Africa. Standalone (does not reuse the dark gradient letterhead).
Outputs Eugene_Buchanan_Cover_Letter_KoBold.pdf
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
# Light palette (Venngage-inspired)
# ----------------------------------------------------------------------------
HDR_BG   = colors.HexColor("#E9E9EC")   # light grey header band
INK      = colors.HexColor("#2b2b2e")   # near-black name / body
SUBGREY  = colors.HexColor("#8a8a90")   # italic subtitle
MUTEGREY = colors.HexColor("#6f6f76")   # contact text
MAGENTA  = colors.HexColor("#9c2b6e")   # salutation + accents
DEEPPURP = colors.HexColor("#4b0f5d")   # ring segment + bubble glyphs
PEACH    = colors.HexColor("#f2b26b")   # ring segment
ROSE     = colors.HexColor("#c05a78")   # ring segment
CORAL    = colors.HexColor("#e07a5f")   # ring segment
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
# (bubble label, bubble x-offset, bubble y-offset) relative to photo center
# kept clear of the left contact column (email address is long)
BUBBLES = [
    ("Agent", -130,  25),
    ("React", -118, -48),
    ("RAG",  148,  72),
    ("Rust",  150,   4),
    ("Au",   128, -58),
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

        # -- name + subtitle + contact (left) --
        c.setFillColor(INK)
        c.setFont(FONT_B, 24)
        c.drawString(28, H - 44, "Eugene L. Buchanan")
        c.setFillColor(SUBGREY)
        c.setFont(FONT_I, 11)
        c.drawString(28, H - 62, "Software Engineer \u2014 Data Systems")
        cy = H - 84
        self._contact_row(c, 28, cy, "T", "+1 (909) 545 5384")
        cy -= 20
        self._contact_row(c, 28, cy, "E", "eugene@serviceofothers.org")
        cy -= 20
        self._contact_row(c, 28, cy, "G", "github.com/eugeneb50")

        # -- photo center, lower-middle of band (shifted right to clear contacts) --
        pcx, pcy, pr = W / 2 + 60, 90, 55
        # segmented ring: thick stroked arcs, one color per segment
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

        # -- satellite bubbles on spokes --
        br = 22
        for (label, dx, dy), col in zip(BUBBLES, RING_COLORS * 2):
            bx, by = pcx + dx, pcy + dy
            # spoke line from ring edge toward bubble edge
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
body_style = ParagraphStyle("lbody", fontName=FONT, fontSize=11.5, leading=16,
                            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)
fit_title = ParagraphStyle("lfit", fontName=FONT_B, fontSize=8.4, leading=10.5,
                           textColor=INK, spaceAfter=0)
fit_desc = ParagraphStyle("lfitd", fontName=FONT, fontSize=8.1, leading=10.5,
                          textColor=MUTEGREY, spaceAfter=3)
sign_style = ParagraphStyle("lsign", fontName=FONT_B, fontSize=10, leading=13,
                            textColor=INK, spaceBefore=6, spaceAfter=0)
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
    "KoBold Metals Hiring Team",
    "Software Engineer \u2014 Data Systems Engineering",
]

SUBJECT = "Re: Software Engineer, Data Systems \u2014 Python pipelines, geospatial AI"

PARAGRAPHS = [
    "I did not ever think I would be applying to be a KoBold. "
    "However here I find myself bringing a wide skill set to "
    "your table with the gleam of treasure in my eyes.",

    "You are driving the edge of geologic data exploration "
    "with AI making discoveries with less guessing and more "
    "knowing.",

    "That is a craft I can be excited about as a lifelong "
    "gem and mineral prospector and information systems "
    "enthusiast.",

    "I am looking for a long term role that I can grow with. "
    "I have sharpened my skills lately with Rust and self-improving "
    "agentic harnesses with RAG, MCP, knowledge graphing.",

    "Here is a sample of my work for an AI sampling project "
    "I am working on using Python that scouts turquoise "
    "prospects in Baja California.<br/>"
    '<a href="https://encuentralo.mx/baja-mineral/?lang=en">encuentralo.mx/baja-mineral</a>',

    "Please take time to review my resume and consider me "
    "for the role as a software engineer. "
    "My worldly off-grid renewable experience is for hire as "
    "well, and is useful in remote field operations.",

    "I am ready to work. I can act as a corporate Swiss Army knife "
    "with LoRa GPS.",
]

# (bubble tag, title, desc) — tags echo the header bubbles
QUALIFICATIONS = [
    ("Agent", "Agentic AI infrastructure",
     "Lifecycle observer, model routing + cost attribution in a 32.8k-star Rust gateway."),
    ("RAG", "Retrieval and evaluation",
     "RAG + guardrails shipped under SOC 2; regression suites with dashboards."),
    ("React", "Frontends, Rust gateway, Django builds",
     "React frontends; Rust gateway contributions; Django/WordPress builds."),
    ("Au", "Prospector who embeds",
     "Lifelong prospector; field-ready; learns geology fast, supports users."),
]

CLOSING = (
    "You pair human and machine intelligence to find the metals the energy transition "
    "needs. I build that pairing — and chase it in the field. Happy to demo the Baja "
    "atlas or walk through any PR."
)


def fit_cell(tag, title, desc):
    dot = '<font color="#4b0f5d"><b>\u25cf %s</b></font>  <b>%s.</b>' % (tag, title)
    return [Paragraph(dot, fit_title), Paragraph(desc, fit_desc)]


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Cover_Letter_KoBold.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP,
                          bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Cover Letter (KoBold Software Engineer, Data Systems)",
                          author="Eugene L. Buchanan",
                          subject="Application: KoBold Software Engineer Data Systems",
                          keywords="Cover Letter, KoBold, Data Systems, Python, Django, WordPress, React, Rust, RAG, Agentic AI, Baja Mineral Explorer, SIP, DataKit, prospecting, Zambia")
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
    # thin rule like the template, drawn as a table line
    rule = Table([[""]], colWidths=[FW])
    rule.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.7, RULE_C),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story.append(rule)
    for line in RECIPIENT:
        story.append(Paragraph(line, addr_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(SUBJECT, subj_style))
    story.append(Paragraph("Dear KoBold Hiring Team,", salute_style))

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
    story.append(Paragraph("Software Engineer \u2014 Data Systems, Geospatial + AI Evaluation", sign2_style))
    story.append(Paragraph('Apple Valley, CA (Remote, US authorized)  \u00b7  eugene@serviceofothers.org  \u00b7  <a href="https://github.com/eugeneb50">github.com/eugeneb50</a>', sign2_style))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
