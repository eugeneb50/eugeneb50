#!/usr/bin/env python3
"""Generic cover letter: Senior AI Engineer (Agentic AI, MCP, RAG).

Employer-nonspecific: no company, location, or requisition mentions — reuse
for any Senior AI Engineer application by editing RECIPIENT and SUBJECT.
Results-led STAR paragraphs (Situation -> Action -> Result), short lines for
visual scanning. Reuses the design system from build_cover.py without
overwriting it.
Outputs Eugene_Buchanan_Cover_Letter_AI_Engineer.pdf
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer,
                                NextPageTemplate)

import build_cover as base
from reportlab.lib import colors as _colors


class AIEngineerHead(base.LetterHead):
    """Same gradient letterhead, generic Senior AI Engineer subtitle."""

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
        c.drawString(28, H - 62, "Senior AI Engineer  \u2014  Agentic AI, RAG, LLM Routing")
        c.setFillColor(_colors.HexColor("#eaeafa")); c.setFont(base.FONT, 8)
        c.drawString(28, H - 82, "Apple Valley, CA  \u00b7  +1 (909) 545 5384  \u00b7  eugene@serviceofothers.org  \u00b7  github.com/eugeneb50")
        c.setStrokeColor(colors.white); c.setFillAlpha(0.25); c.setLineWidth(0.5)
        c.line(28, H - 95, pcx - pr - 10, H - 95); c.setFillAlpha(1)


PW, PH = letter
ML = MR = 48
FW = PW - ML - MR

LETTER_DATE = "September 20, 2026"

# Generic — edit per application.
RECIPIENT = [
    "Hiring Manager",
]

SUBJECT = "Re: Senior AI Engineer \u2014 Agentic AI, MCP, RAG"

PARAGRAPHS = [
    "I'm applying for the Senior AI Engineer role. You need agentic workflows, RAG knowledge systems, LLM orchestration, and MCP context management.",

    "Agents had no MCP path into herdr terminal workspaces, so I authored herdr-mcp (github.com/eugeneb50/herdr-mcp): a Rust MCP server exposing the multiplexer as 51 tools.",
    "It runs MCP stdio for Claude Desktop, Cursor, Claude Code, Continue, and OpenCode, plus an HTTP bridge serving a React playground for running tools and chaining recipes.",
    "Result: repeatable multi-step agent work through a recipe engine, cron scheduler, and trim pipeline — 299 tests passing across a 4-crate workspace.",

    "At Knowledgecity (Dec 2020\u2013Aug 2025) support needed grounded answers over scattered enterprise content, so I helped ship a RAG chatbot with guardrails that cleared SOC 2 review.",
    "Six platforms, six auth dialects: I shipped SAP, Oracle, Workday, Coursera, UKG, and Zoom over SAML, OAuth, SFTP, REST APIs, and webhooks.",
    "Result: deployments gated by CI/CD pipelines with health dashboards and alerting — deploy, monitor, and govern.",

    "On ZeroClaw's 32.8k-star Rust gateway, routing and cost data were scattered across 9 providers — PR #7946 unified them behind one context-window source of truth (merged Jul 2026).",
    "Fallbacks then misattributed usage and cost, so PR #8966 put live serving-provider identity on every usage event with a per-attempt ledger (merged Sep 18, 2026, 94 commits).",
    "Agent state was invisible to operators, so PR #8337's lifecycle observer fed the vendor-neutral design.",

    "What I bring from day one is the builder mindset: grounded retrieval, honest context, "
    "and every fallback accounted for — plus 25+ years shipping production systems.",
    "I am open to remote and onsite roles and welcome the chance to dig into your agent stack.",
]

QUALIFICATIONS = [
    ("MCP server, authored",
     "herdr-mcp: 51 tools, HTTP bridge, React playground, recipes, scheduler, 299 tests."),
    ("Agentic workflows",
     "Lifecycle observer, usage ledger, retry/recovery across a 32.8k-star gateway."),
    ("RAG knowledge systems",
     "RAG chatbot with guardrails under SOC 2; Elastic/SQL search; trim pipelines."),
    ("Deploy, monitor, govern",
     "Regression dashboards and alerting; CI/CD gates; Blue Team and SOC 2 practice."),
]

CLOSING = (
    "Enterprise agents only earn trust when retrieval is grounded, context is honest, "
    "and every fallback is accounted for. That is what I build — happy to walk through "
    "any ZeroClaw PR, herdr-mcp tool, or Knowledgecity integration decision in an interview."
)


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Cover_Letter_AI_Engineer.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=base.HEADER_H + base.TOP_GAP,
                          bottomMargin=base.BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Cover Letter (Senior AI Engineer)",
                          author="Eugene L. Buchanan",
                          subject="Application: Senior AI Engineer Agentic AI MCP RAG",
                          keywords="Cover Letter, Senior AI Engineer, Agentic AI, MCP, RAG, LLM, Python, ZeroClaw, herdr-mcp")
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
    story.append(AIEngineerHead(photo=photo_path))
    story.append(NextPageTemplate("content"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(LETTER_DATE, base.date_style))
    for line in RECIPIENT:
        story.append(Paragraph(line, base.addr_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph(SUBJECT, base.subj_style))
    story.append(base.AccentRule())
    story.append(Spacer(1, 6))

    story.append(Paragraph("Dear Hiring Manager,", base.salute_style))

    for para in PARAGRAPHS:
        story.append(Paragraph(para, base.body_style))

    story.append(Paragraph("How I fit this role:", base.subj_style))
    qual_style = ParagraphStyle("qual5", parent=base.body_style, fontSize=8.4,
                                leading=11.4, leftIndent=12, bulletIndent=2,
                                spaceAfter=3.5)
    qual_col = []
    for title, desc in QUALIFICATIONS:
        txt = f'<b><font color="#2b1d63">{title}.</font></b>  {desc}'
        qual_col.append(Paragraph(txt, qual_style, bulletText="\u2022"))
    chart_col = [base.ProfitChart(
        "Value: Grounded, Routed, Governed",
        ["Agent", "RAG", "Ctx", "Route", "Gov", "Scale"],
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

    story.append(Paragraph(CLOSING, base.body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("Best regards,", base.body_style))
    story.append(Spacer(1, 3))
    story.append(base.AccentRule(width=180))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Eugene L. Buchanan", base.sign_style))
    story.append(Paragraph("Senior AI Engineer \u2014 Agentic AI, RAG, LLM Routing", base.sign2_style))
    story.append(Paragraph("Apple Valley, CA  \u00b7  eugene@serviceofothers.org  \u00b7  github.com/eugeneb50", base.sign2_style))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
