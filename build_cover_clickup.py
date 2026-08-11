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
        c.drawString(28, H - 82, "San Quint\u00edn, BC MX (Remote / PT)  \u00b7  +1 (909) 545 5384  \u00b7  eugene@serviceofothers.org  \u00b7  github.com/eugeneb50")
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


# ----------------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------------
date_style = ParagraphStyle("date", fontName=FONT, fontSize=9, leading=12,
                            textColor=GREY, alignment=TA_LEFT, spaceAfter=10)
addr_style = ParagraphStyle("addr", fontName=FONT, fontSize=9, leading=12,
                            textColor=INK, alignment=TA_LEFT, spaceAfter=1)
subj_style = ParagraphStyle("subj", fontName=FONT_B, fontSize=10.5, leading=14,
                           textColor=NAVY2, spaceBefore=6, spaceAfter=8)
body_style = ParagraphStyle("body", fontName=FONT, fontSize=9.5, leading=13.5,
                            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7,
                            firstLineIndent=0)
salute_style = ParagraphStyle("salute", fontName=FONT, fontSize=9.5, leading=13,
                              textColor=INK, spaceAfter=7)
sign_style = ParagraphStyle("sign", fontName=FONT_B, fontSize=10, leading=13,
                           textColor=NAVY2, spaceBefore=6, spaceAfter=0)
sign2_style = ParagraphStyle("sign2", fontName=FONT, fontSize=8.5, leading=11,
                            textColor=GREY, spaceAfter=0)

# ----------------------------------------------------------------------------
# Letter content — targeted at ClickUp
# ----------------------------------------------------------------------------
LETTER_DATE = "August 3, 2026"

RECIPIENT = [
    "ClickUp Hiring Team",
    "AI Platform \u2014 Staff AI Engineer, Multi-Agent Frameworks",
    "Via: clickup.com/careers",
]

SUBJECT = "Re: Staff AI Engineer \u2014 Multi-Agent Frameworks (#LI-REMOTE)"

PARAGRAPHS = [
    "I'm applying for the Staff AI Engineer position on the Multi-Agent Frameworks team. "
    "ClickUp's vision of a converged AI workspace \u2014 unifying tasks, docs, chat, calendar, and "
    "search through context-driven AI \u2014 is the exact problem space I've been working in: "
    "building platforms that let agents coordinate, evaluate, and operate at scale.",

    "On the ZeroClaw agentic AI gateway (32.2k stars, Rust), I shipped an observer that reports "
    "agent lifecycle state \u2014 idle, working, blocked, released \u2014 via JSON-RPC over Unix "
    "domain sockets (PR #8337, 1,132 additions). That work is multi-agent orchestration: bounded "
    "I/O threading, env-driven discovery, and reliability guards for unresponsive sockets without "
    "hanging the agent loop. I also reviewed a 6,684-line security PR adding multi-user auth, "
    "deny-by-default permission profiles, and principal isolation at RPC dispatch (PR #8672) \u2014 "
    "the same isolation problem multi-agent platforms face.",

    "At Knowledgecity I was Product Owner for Integrations, shipping SAP, Oracle, Workday, UKG, "
    "Coursera, and Zoom via SAML, OAuth, SFTP, and custom APIs on AWS/Postgres/React. Orchestrating "
    "six enterprise services with different auth models and error semantics is the same coordination "
    "challenge multi-agent frameworks solve. I also built the evaluation framework (Cypress, Selenium, "
    "JUnit, health dashboards, alerting) for testing those integrations in complex scenarios, and "
    "applied AI prompt engineering and chatbot tooling in production.",

    "Here's how I map to your qualifications:",
]

QUALIFICATIONS = [
    ("Multiple LLMs & orchestration",
     "Integrating OpenAI, Anthropic, and Gemini providers daily through Hermes Agent; "
     "agent lifecycle orchestration in production via Rust + JSON-RPC."),
    ("Evaluation frameworks",
     "27 years building test automation and quality pipelines; four rounds of reviewer "
     "blockers resolved on the ZeroClaw PR through targeted evaluation of each failure mode."),
    ("Multi-agent frameworks",
     "Shipped herdr agent reporting integration (multi-agent coordination without requiring "
     "a herdr adapter); coordinating on a standardized generic agent integration adapter."),
    ("AI privacy & compliance",
     "Reviewed deny-by-default permission profiles, peercred, SSH challenge-response, and OIDC "
     "auth flows plus 27 years in regulated, compliance-driven environments."),
    ("Search technologies",
     "Elasticsearch, PostgreSQL full-text, and integration search across enterprise platforms "
     "at Knowledgecity and in the ZeroClaw ecosystem."),
]

CLOSING = (
    "I'm AI-native in the way ClickUp means it: I use AI agents daily, I build the infrastructure "
    "they run on, and I evaluate their behavior under real-world complexity. I'd welcome the "
    "chance to bring that to ClickUp's AI Platform team and help build the future of converged "
    "work. Happy to walk through any of the PRs or code in a technical interview."
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
                          author="Eugene L. Buchanan")
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
    story.append(Spacer(1, 6))

    # ── Date & recipient block ────────────────────────────────────
    story.append(Paragraph(LETTER_DATE, date_style))
    for line in RECIPIENT:
        story.append(Paragraph(line, addr_style))
    story.append(Spacer(1, 6))

    # ── Subject ────────────────────────────────────────────────────
    story.append(Paragraph(SUBJECT, subj_style))
    story.append(AccentRule())
    story.append(Spacer(1, 8))

    # ── Salutation ─────────────────────────────────────────────────
    story.append(Paragraph("Dear ClickUp AI Platform Team,", salute_style))

    # ── Body paragraphs ────────────────────────────────────────────
    for para in PARAGRAPHS:
        story.append(Paragraph(para, body_style))

    # ── Qualification bullets ──────────────────────────────────────
    qual_style = ParagraphStyle("qual", fontName=FONT, fontSize=9, leading=12.5,
                                leftIndent=14, bulletIndent=2, bulletColor=PURPLE,
                                spaceAfter=4, textColor=INK)
    for title, desc in QUALIFICATIONS:
        txt = f'<b><font color="#2b1d63">{title}.</font></b>  {desc}'
        story.append(Paragraph(txt, qual_style, bulletText="\u2022"))

    story.append(Spacer(1, 6))
    story.append(Paragraph(CLOSING, body_style))
    story.append(Spacer(1, 4))

    # ── Sign-off ───────────────────────────────────────────────────
    story.append(Paragraph("Best regards,", body_style))
    story.append(Spacer(1, 4))
    story.append(AccentRule(width=180))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Eugene L. Buchanan", sign_style))
    story.append(Paragraph("Staff AI Engineer \u2014 Multi-Agent Frameworks", sign2_style))
    story.append(Paragraph("eugene@serviceofothers.org  \u00b7  +1 (909) 545 5384  \u00b7  github.com/eugeneb50", sign2_style))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
