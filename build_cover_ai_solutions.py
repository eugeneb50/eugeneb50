#!/usr/bin/env python3
"""Tailored cover letter: AI Solutions Strategic Consultant (100% Remote).

Covers, per applicant: HNWI finder on county recorder public records (real
estate agency), eBay listing assistant on Hermes agent, ZeroClaw Rust gateway
work. Reuses the design system from build_cover.py without overwriting it.
Outputs Eugene_Buchanan_Cover_Letter_AI_Solutions.pdf
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer,
                                NextPageTemplate)

import build_cover as base
from reportlab.lib import colors as _colors


class ConsultantHead(base.LetterHead):
    """Same gradient letterhead, retitled for the consultant application."""

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
        c.drawString(28, H - 62, "AI Solutions Strategic Consultant  \u2014  Use Cases to Production ROI")
        c.setFillColor(_colors.HexColor("#eaeafa")); c.setFont(base.FONT, 8)
        c.drawString(28, H - 82, "Apple Valley, CA (Remote)  \u00b7  +1 (909) 545 5384  \u00b7  eugene@serviceofothers.org  \u00b7  github.com/eugeneb50")
        c.setStrokeColor(colors.white); c.setFillAlpha(0.25); c.setLineWidth(0.5)
        c.line(28, H - 95, pcx - pr - 10, H - 95); c.setFillAlpha(1)

PW, PH = letter
ML = MR = 48
FW = PW - ML - MR

LETTER_DATE = "September 15, 2026"

RECIPIENT = [
    "Hiring Team",
    "AI Solutions Strategic Consultant \u2014 100% Remote (12 Months)",
    "Via: requisition portal",
]

SUBJECT = "Re: AI Solutions Strategic Consultant \u2014 15+ Years, Concept to Production"

PARAGRAPHS = [
    "I'm applying for the AI Solutions Strategic Consultant role. For 15+ years I've "
    "turned business needs into production systems \u2014 most recently into AI solution "
    "architectures with clear use cases, technical roadmaps, and measurable ROI. I "
    "identify where AI/GenAI pays, evaluate the platforms, models, and vendors honestly, "
    "and work with business, data, engineering, and product teams to ship.",

    "For a real estate agency I built and shipped an HNWI finder on county recorder "
    "public records. It scores public-records signals into a ranked prospect list with "
    "lead enrichment \u2014 owner, property, equity, and contactability signals resolved "
    "through graph engineering over owners, parcels, and transactions \u2014 so agents "
    "spend time on the highest-value owners first. The architecture is a data "
    "pipeline with API and microservices boundaries feeding existing agency workflows: "
    "ingest and normalize public filings, resolve entities, enrich leads, score and "
    "rank, and deliver results where agents already work. Retrieval uses RAG patterns "
    "with pre- and post-filtering, and failure-model logging feeds a self-improving "
    "loop that tightens scoring and enrichment over time. The use case was chosen on "
    "value and feasibility \u2014 prospecting time is the costliest input \u2014 and scoped so "
    "it runs on compliant public data within current integrations. That public-records "
    "foundation extends my Tierrachain work on parallel records systems and AI-assisted "
    "compliance filing for real estate exchange.",

    "I also shipped an eBay listing assistant built on a Hermes agent around a photo "
    "upload pipeline: sellers upload item photos, visual reverse image search finds "
    "comparable listings, and description generation drafts titles, descriptions, and "
    "pricing from the images plus retrieved comparables. The seller problem "
    "was concrete: titles, descriptions, and pricing that move inventory without hours of "
    "manual drafting. RAG over visual and text comparables applies pre- and post-filtering, "
    "the seller stays in the approval loop, "
    "and results iterate toward what sells. MCP tool boundaries expose pricing, search, and "
    "publishing actions to the agent; failure-model logging captures bad drafts, "
    "rejections, and corrections into a self-improving loop. I treated it as a GenAI use "
    "case end to end \u2014 business value first, then model and platform choice, then evaluation "
    "of output quality before release, then hardening from prototype into a tool sellers "
    "can use daily.",

    "That product-level delivery rests on agentic infrastructure depth. On ZeroClaw's "
    "32.8k-star Rust gateway I shipped production agent systems: a merged context-window "
    "meter unifying 9 LLM providers into one source of truth for model routing and cost "
    "attribution (PR #7946), live serving-provider identity on usage events across "
    "fallback and model switches (PR #8966, open), and an observability, steering, and "
    "interruptible layer over the herdr multiplexer reporting agent lifecycle "
    "(idle/working/blocked/released) via JSON-RPC (PR #8337, requirements adopted into "
    "the vendor-neutral design) \u2014 the coordination plane for A2A-style team frameworks "
    "where agents hand off, escalate, and get interrupted safely. At "
    "Knowledgecity I owned integrations as Product Owner and shipped SAP, Oracle, "
    "Workday, UKG, Coursera, and Zoom over SAML, OAuth, SFTP, and REST APIs, plus a RAG "
    "support chatbot with guardrails under SOC 2 controls. I stay current by building "
    "where the field moves: MCP servers, graph engineering, and evaluation tooling "
    "(Cypress, Selenium, JUnit, dashboards) that proves behavior at the system level.",
]

QUALIFICATIONS = [
    ("AI/GenAI use cases tied to ROI",
     "HNWI finder with lead enrichment (agent prospecting time) and eBay listing assistant (sell-through per labor hour) \u2014 prioritized on value and feasibility."),
    ("RAG, MCP, graph engineering",
     "RAG retrieval with pre- and post-filtering; MCP tool boundaries; owner-parcel-transaction graphs for entity resolution and enrichment."),
    ("Observability, steering, safe interruption",
     "Herdr-multiplexer lifecycle layer (idle/working/blocked/released) as the coordination plane for A2A-style team handoffs and escalation."),
    ("Evaluate, learn, ship",
     "Failure-model logging into a self-improving loop; platform, model, and vendor best-fit analysis; delivery with business, data, engineering, and product teams."),
]

CLOSING = (
    "I consult the way I build: name the business outcome, map the feasible AI use "
    "cases, recommend the simplest architecture that reaches production, and measure "
    "whether it paid. I'd welcome a working session on your highest-priority use case \u2014 "
    "happy to walk through the HNWI scoring pipeline, the listing assistant's evaluation "
    "loop, or any ZeroClaw PR."
)


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Cover_Letter_AI_Solutions.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=base.HEADER_H + base.TOP_GAP,
                          bottomMargin=base.BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Cover Letter (AI Solutions Strategic Consultant)",
                          author="Eugene L. Buchanan",
                          subject="Application: AI Solutions Strategic Consultant, 100% Remote",
                          keywords="Cover Letter, AI Solutions Strategic Consultant, GenAI use cases, ROI, RAG, MCP, graph engineering, observability, herdr, A2A, lead enrichment, Hermes agent, ZeroClaw")
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
    story.append(ConsultantHead(photo=photo_path))
    story.append(NextPageTemplate("content"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(LETTER_DATE, base.date_style))
    for line in RECIPIENT:
        story.append(Paragraph(line, base.addr_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph(SUBJECT, base.subj_style))
    story.append(base.AccentRule())
    story.append(Spacer(1, 6))

    story.append(Paragraph("Dear Hiring Team,", base.salute_style))

    for para in PARAGRAPHS:
        story.append(Paragraph(para, base.body_style))

    story.append(Paragraph("How I fit this role:", base.subj_style))
    qual_style = ParagraphStyle("qual2", parent=base.body_style, fontSize=8.4,
                                leading=11.4, leftIndent=12, bulletIndent=2,
                                spaceAfter=3.5)
    qual_col = []
    for title, desc in QUALIFICATIONS:
        txt = f'<b><font color="#2b1d63">{title}.</font></b>  {desc}'
        qual_col.append(Paragraph(txt, qual_style, bulletText="\u2022"))
    chart_col = [base.ProfitChart(
        "Value: Use Case to Production",
        ["Scope", "Build", "Eval", "Ship", "Scale", "ROI"],
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
    story.append(Paragraph("AI Solutions Strategic Consultant \u2014 Concept to Production", base.sign2_style))
    story.append(Paragraph("Apple Valley, CA (Remote)  \u00b7  eugene@serviceofothers.org  \u00b7  github.com/eugeneb50", base.sign2_style))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
