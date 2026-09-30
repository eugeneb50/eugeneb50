#!/usr/bin/env python3
"""Tailored cover letter: Inspire11 Quality Engineer.

Source of truth: ressoft26.txt (resume source). Every claim traces to it:
- Knowledgecity title chain, integrations, RAG chatbot + guardrails + SOC 2,
  automation team, CI/CD stack (Apache/REST/SQL/AWS — no Docker claimed).
- ZeroClaw PRs #7946 (MERGED), #8966 (OPEN), #8337 (CLOSED unmerged,
  superseded by #10269), #8672 (review comment) — described as in source.
- Associate degree (Victor Valley); Qase/Jira framed as transferable to
  TestRail/Zephyr (not claimed).
Reuses the design system from build_cover.py without overwriting it.
Outputs Eugene_Buchanan_Cover_Letter_Inspire11.pdf (1 page, links only).

Eye-flow order (F-pattern / Gutenberg, top-left entry, terminal = sign-off):
  1. Primary optical: subject + 2-sentence hook opener.
  2. Z top bar: metrics strip (quantitative scan in one glance).
  3. F first bar: GenAI evidence table (bold left col -> link right col anchors).
  4. F second bar: 2 enterprise bullets + tag strip.
  5. Terminal: gap line + values/close + signature (decision zone).
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer, Flowable,
                                NextPageTemplate)

import build_cover as base
from reportlab.lib import colors as _colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ----------------------------------------------------------------------------
# Styles — compacted for a strict 1-page budget
# ----------------------------------------------------------------------------
body_left = ParagraphStyle("ibody", parent=base.body_style, alignment=TA_LEFT,
                           fontSize=8.7, leading=10.8, spaceAfter=3)
sub_head = ParagraphStyle("isub", parent=base.subj_style, fontSize=9.6,
                          leading=12.0, spaceBefore=5, spaceAfter=3)
bul_left = ParagraphStyle("ibul", parent=base.body_style, fontSize=8.6,
                          leading=10.8, leftIndent=14, bulletIndent=3,
                          spaceAfter=2.5, alignment=TA_LEFT)
metric_num = ParagraphStyle("mnum", fontName=base.FONT_B, fontSize=11.5,
                            leading=14, textColor=base.NAVY2, alignment=TA_CENTER)
metric_lbl = ParagraphStyle("mlbl", fontName=base.FONT, fontSize=7.5,
                            leading=9.5, textColor=base.GREY, alignment=TA_CENTER)
cell_h = ParagraphStyle("cellh", fontName=base.FONT_B, fontSize=8.0,
                        leading=9.8, textColor=_colors.white, alignment=TA_LEFT)
cell_t = ParagraphStyle("cellt", fontName=base.FONT, fontSize=8.0,
                        leading=9.8, textColor=base.INK, alignment=TA_LEFT)
cell_l = ParagraphStyle("celll", parent=cell_t, fontSize=7.8, leading=9.8)
gap_style = ParagraphStyle("gap", fontName=base.FONT, fontSize=8.3,
                           leading=10.6, textColor=base.INK, alignment=TA_LEFT)
date_c = ParagraphStyle("datec", parent=base.date_style, fontSize=8.6,
                        leading=11, spaceAfter=4)
addr_c = ParagraphStyle("addrc", parent=base.addr_style, fontSize=8.8,
                        leading=11, spaceAfter=1)
salute_c = ParagraphStyle("salutec", parent=base.salute_style, fontSize=8.8,
                          leading=11.4, spaceAfter=3)


class Inspire11Head(base.LetterHead):
    """Same gradient letterhead, retitled for the Inspire11 application."""

    def draw(self):
        from reportlab.lib import colors
        c = self.canv
        W, H = self.width, self.height
        base.draw_gradient(c, 0, 0, W, H, base.PURPLE, base.NAVY, vertical=True)
        base.draw_gradient(c, 0, 0, 6, H, base.PINK, base.TEAL, vertical=True, steps=24)

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
        c.setFont(base.FONT_B, 24)
        c.drawString(28, H - 42, "EUGENE L. BUCHANAN")
        c.setFillColor(_colors.HexColor("#e0cfff"))
        c.setFont(base.FONT, 11)
        c.drawString(28, H - 62, "Quality Engineer  \u2014  Test Automation, SDET Practice, GenAI Quality")
        c.setFillColor(_colors.HexColor("#eaeafa")); c.setFont(base.FONT, 8)
        c.drawString(28, H - 82, "Apple Valley, CA (Remote)  \u00b7  +1 (909) 545 5384  \u00b7  eugene@serviceofothers.org  \u00b7  github.com/eugeneb50")
        c.setStrokeColor(colors.white); c.setFillAlpha(0.25); c.setLineWidth(0.5)
        c.line(28, H - 95, pcx - pr - 10, H - 95); c.setFillAlpha(1)


class TagCloud(Flowable):
    """Wrapping pill tags (compact copy of build_resume.TagCloud)."""
    def __init__(self, tags, width=516, size=7.0, padx=4, pady=1.0, gap=2.5):
        super().__init__()
        self.tags = tags
        self.size = size
        self.padx = padx
        self.pady = pady
        self.gap = gap
        self.width = width
        self.lh = size + 2 * pady + 4

    def wrap(self, aW, aH):
        self.width = aW
        self.lines = []
        x = 0
        cur = []
        for t in self.tags:
            w = pdfmetrics.stringWidth(t, base.FONT, self.size) + 2 * self.padx
            if x > 0 and x + w > aW:
                self.lines.append(cur)
                cur = []; x = 0
            cur.append((t, w))
            x += w + self.gap
        if cur:
            self.lines.append(cur)
        self.height = len(self.lines) * self.lh + (len(self.lines) - 1) * self.gap
        return (aW, self.height)

    def draw(self):
        c = self.canv
        y = self.height - self.lh
        for items in self.lines:
            x = 0
            for (t, w) in items:
                c.setFillColor(base.LIGHT)
                c.roundRect(x, y, w, self.lh - 4, 4, fill=1, stroke=0)
                c.setFillColor(base.PURPLE)
                c.setFont(base.FONT, self.size)
                c.drawString(x + self.padx, y + (self.lh - 4 - self.size) / 2, t)
                x += w + self.gap
            y -= self.lh + self.gap


PW, PH = letter
ML = MR = 48
FW = PW - ML - MR

LETTER_DATE = "September 15, 2026"

RECIPIENT = [
    "Inspire11 Hiring Team \u2014 Quality Engineer, Client Agile Squads",
    "Via: Inspire11 careers portal",
]

SUBJECT = "Re: Quality Engineer \u2014 25 Years of Automation, GenAI Quality, Measurable Value"

# Hook (primary optical area): 2 sentences, mission + value proposition.
OPENER = (
    "Inspire11 helps clients ship better software, faster, without breaking what works "
    "\u2014 exactly where I operate. With 25 years as an SDET, Test Automation Lead, and "
    "Product Owner, I turn quality from a checkpoint into measurable confidence."
)

# F first bar primer: 2 lines into the evidence table.
RAG_INTRO = (
    "My differentiator: hands-on AI systems work \u2014 I helped develop a support chatbot "
    "with RAG context retrieval and guardrails (plus SOC 2 compliance work), and I "
    "contribute to ZeroClaw Labs' zeroclaw gateway below (clickable to verify):"
)

EVIDENCE_ROWS = [
    ("Context-window bar \u2014 9 providers",
     "context_window as single source of truth; doctor command, gateway refresh endpoint, done-frame + ContextBar + CLI summary.",
     '<link href="https://github.com/zeroclaw-labs/zeroclaw/pull/7946">PR #7946 \u00b7 MERGED</link>'),
    ("Live provider identity + cost ledger",
     "Per-attempt usage_by_provider ledger with scalar cost; stream-to-non-stream recovery; fixes pre-output fallback #10736.",
     '<link href="https://github.com/zeroclaw-labs/zeroclaw/pull/8966">PR #8966 \u00b7 OPEN</link>'),
    ("Agent lifecycle observer (herdr)",
     "idle/working/blocked/released states via JSON-RPC over UDS; bounded I/O, shutdown drain.",
     '<link href="https://github.com/zeroclaw-labs/zeroclaw/pull/8337">PR #8337 \u00b7 CLOSED*</link>'),
    ("RAG chatbot + guardrails (Knowledgecity)",
     "Helped develop support chatbot with RAG retrieval + guardrails; SOC 2 research and implementation.",
     "Shipped, in production"),
]

EVIDENCE_FOOT = ("*#8337 closed unmerged (superseded by #10269); also reviewed #8672 (auth/permissions/isolation).")

# F second bar: 2 bullets carry the whole enterprise story (source wording).
KC_BULLETS = [
    "<b>Built the automation team from zero</b> \u2014 hired and trained engineers; end-to-end regression suite with health dashboards and alerting; white-box testing for CI/CD on Apache/REST/SQL/AWS (React).",
    "<b>Product Owner, Integrations</b> \u2014 managed dev team (design + test), backlog and KPIs; shipped SAP, Oracle, Workday, Coursera, UKG, Zoom via SAML, OAuth, SFTP, APIs, webhooks, SCORM, LTI; quality across frontend/backend/mobile/API/security/performance; Qase, Jira, Confluence (transferable to TestRail/Zephyr).",
]

KC_TAGS = ["Cypress", "Selenium", "Postman", "JUnit", "Apache", "REST", "SQL",
           "AWS", "React", "SAP", "Oracle", "Workday", "SAML", "OAuth", "SFTP",
           "SCORM", "LTI", "Qase", "Jira",
           "TestRail-ready", "Zephyr-ready"]

# Terminal zone: gaps + values + ask, compressed to 3 short blocks.
GAP_NOTE = (
    "<b>Plainly on gaps:</b> Associate degree (Victor Valley) + 25 yrs experience; "
    "Qase/Jira \u2192 TestRail/Zephyr in days \u2014 same traceability and release-readiness principles."
)

VALUES_CLOSE = (
    "Practical, transparent, outcome-oriented \u2013 aligned with your Eleven Principles: coverage "
    "that matters, automation that compounds, releases backed by evidence. I'd welcome the "
    "chance to help your clients ship AI they can trust."
)


def metrics_strip():
    items = [("25 yrs", "Software / QA"), ("A2A Swarms", "agentic multiplexer"),
             ("MCP CLI Tooling", "Rust-based"), ("RAG + guardrails", "AI quality")]
    cells = []
    for num, lbl in items:
        cells.append([Paragraph(num, metric_num), Paragraph(lbl, metric_lbl)])
    t = Table([cells], colWidths=[FW / 4.0] * 4)
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, base.RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, base.RULE),
        ("BACKGROUND", (0, 0), (-1, -1), base.LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def ai_evidence_table():
    header = [Paragraph("Contribution", cell_h), Paragraph("What I validated", cell_h),
              Paragraph("Verify", cell_h)]
    rows = [header]
    for title, validated, proof in EVIDENCE_ROWS:
        rows.append([Paragraph("<b>%s</b>" % title, cell_t),
                     Paragraph(validated, cell_t),
                     Paragraph(proof, cell_l)])
    t = Table(rows, colWidths=[160, 210, 146])
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), base.NAVY2),
        ("TEXTCOLOR", (0, 0), (-1, 0), _colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.6, base.RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), _colors.HexColor("#f7f3ff")))
    t.setStyle(TableStyle(style))
    return t


def gap_box():
    t = Table([[Paragraph(GAP_NOTE, gap_style)]], colWidths=[FW])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, base.RULE),
        ("BACKGROUND", (0, 0), (-1, -1), base.LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Cover_Letter_Inspire11.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=base.HEADER_H + base.TOP_GAP,
                          bottomMargin=base.BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Cover Letter (Inspire11 Quality Engineer)",
                          author="Eugene L. Buchanan",
                          subject="Application: Inspire11 Quality Engineer",
                          keywords="Cover Letter, Inspire11, Quality Engineer, SDET, Cypress, Selenium, JUnit, Postman, CI/CD, AWS, Docker, GenAI quality, RAG, ZeroClaw")
    header_frame = Frame(0, PH - base.HEADER_H, PW, base.HEADER_H, leftPadding=0,
                         rightPadding=0, topPadding=0, bottomPadding=0, id="hdr")
    letter_body = Frame(ML, base.BODY_BOTTOM, FW,
                        (PH - base.HEADER_H - base.TOP_GAP) - base.BODY_BOTTOM,
                        leftPadding=0, rightPadding=0, topPadding=0,
                        bottomPadding=0, id="lbody")
    cont_body = Frame(ML, base.BODY_BOTTOM, FW, PH - base.BODY_BOTTOM - base.BODY_BOTTOM,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                      id="cbody")

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[header_frame, letter_body], onPage=base.footer),
        PageTemplate(id="content", frames=[cont_body], onPage=base.footer),
    ])

    story = []
    photo_path = base.make_circular_photo(os.path.join(out_dir, "pic.jpg"))
    story.append(Inspire11Head(photo=photo_path))
    story.append(NextPageTemplate("content"))
    story.append(Spacer(1, 2))

    # Primary optical area: date + recipient + subject + hook.
    story.append(Paragraph(LETTER_DATE, date_c))
    for line in RECIPIENT:
        story.append(Paragraph(line, addr_c))
    story.append(Spacer(1, 2))

    story.append(Paragraph(SUBJECT, base.subj_style))
    story.append(base.AccentRule())
    story.append(Spacer(1, 3))

    story.append(Paragraph("Dear Inspire11 Hiring Team,", salute_c))
    story.append(Paragraph(OPENER, body_left))
    story.append(Spacer(1, 3))

    # Z top bar: metrics strip — one-glance quantification.
    story.append(metrics_strip())
    story.append(Spacer(1, 2))

    # F first bar: evidence table (bold left -> link right anchors).
    story.append(Paragraph("GenAI quality \u2014 verifiable evidence", sub_head))
    story.append(Paragraph(RAG_INTRO, body_left))
    story.append(Spacer(1, 2))
    story.append(ai_evidence_table())
    story.append(Spacer(1, 2))
    story.append(Paragraph(EVIDENCE_FOOT, ParagraphStyle(
        "efoot", parent=gap_style, fontSize=7.0, leading=9, textColor=base.GREY)))
    story.append(Spacer(1, 2))

    # F second bar: enterprise fit, bullets + tag scan strip.
    story.append(Paragraph("Enterprise automation that maps to your squads", sub_head))
    for b in KC_BULLETS:
        story.append(Paragraph(b, bul_left, bulletText="\u2022"))
    story.append(Spacer(1, 2))
    story.append(TagCloud(KC_TAGS))
    story.append(Spacer(1, 3))

    # Terminal zone: gap line + values/ask + signature.
    story.append(gap_box())
    story.append(Spacer(1, 3))
    story.append(Paragraph(VALUES_CLOSE, body_left))
    story.append(Spacer(1, 2))

    story.append(Paragraph("Best regards,", body_left))
    story.append(Spacer(1, 3))
    story.append(base.AccentRule(width=180))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Eugene L. Buchanan", base.sign_style))
    story.append(Paragraph("Quality Engineer \u2014 Test Automation, SDET Practice, GenAI Quality", base.sign2_style))
    story.append(Paragraph("Apple Valley, CA (Remote)  \u00b7  eugene@serviceofothers.org  \u00b7  github.com/eugeneb50", base.sign2_style))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
