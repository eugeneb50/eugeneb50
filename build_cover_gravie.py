#!/usr/bin/env python3
"""Tailored cover letter: Gravie Staff AI Test Automation Engineer.

Honest mapping to the requisition: no Playwright, GitLab, Geb/Spock, Pact,
or claims-system claims (none in ressoft26.txt). Transfers Cypress/Selenium/
JUnit + CI + API-boundary + agentic-infrastructure depth, with a ramp plan.
Reuses the design system from build_cover.py without overwriting it.
Outputs Eugene_Buchanan_Cover_Letter_Gravie.pdf
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer,
                                NextPageTemplate)

import build_cover as base
from reportlab.lib import colors as _colors


class GravieHead(base.LetterHead):
    """Same gradient letterhead, retitled for the Gravie application."""

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
        c.drawString(28, H - 62, "Staff AI Test Automation Engineer  \u2014  Agentic Automation Systems")
        c.setFillColor(_colors.HexColor("#eaeafa")); c.setFont(base.FONT, 8)
        c.drawString(28, H - 82, "Apple Valley, CA (Remote)  \u00b7  +1 (909) 545 5384  \u00b7  eugene@serviceofothers.org  \u00b7  github.com/eugeneb50")
        c.setStrokeColor(colors.white); c.setFillAlpha(0.25); c.setLineWidth(0.5)
        c.line(28, H - 95, pcx - pr - 10, H - 95); c.setFillAlpha(1)


PW, PH = letter
ML = MR = 48
FW = PW - ML - MR

LETTER_DATE = "September 15, 2026"

RECIPIENT = [
    "Gravie Hiring Team",
    "Staff AI Test Automation Engineer \u2014 AI-Driven Playwright Automation",
    "Via: Gravie careers portal",
]

SUBJECT = "Re: Staff AI Test Automation Engineer \u2014 Automation Systems, Agentic AI, SDET Depth"

PARAGRAPHS = [
    "I'm applying for the Staff AI Test Automation Engineer role. You need someone who "
    "picks up an in-flight Playwright migration, drives it to completion, and builds the "
    "systems \u2014 frameworks, feedback loops, CI gates, instrumentation \u2014 that let AI "
    "agents generate, execute, and maintain tests at scale. That is how I work: I build "
    "automation systems, not individual test cases, and I bring 25+ years of SDET and "
    "Test Automation Lead practice plus hands-on agentic infrastructure to prove it.",

    "At Knowledgecity (Dec 2020\u2013Aug 2025) I hired and trained the test automation team "
    "and shipped end-to-end regression suites with health dashboards and alert systems over "
    "complex deployments. I ran the CI/CD quality pipeline (Apache, REST, SQL, AWS, React) "
    "with Cypress, Selenium, Postman, and JUnit under Git merge workflows \u2014 pipeline "
    "stages, per-change quality gates, and fast-feedback optimization that transfer directly "
    "to GitLab. I practiced your API-vs-UI judgment daily, verifying integrations at service "
    "boundaries (custom REST APIs, webhooks, SFTP, SAML, OAuth) across SAP, Oracle, Workday, "
    "Coursera, UKG, and Zoom, and reserving end-to-end UI tests for real user journeys. I "
    "also shipped a RAG support chatbot with guardrails under SOC 2 controls, iterating "
    "prompts, context structures, and validation patterns \u2014 the same loop that raises "
    "AI first-pass test-generation rates.",

    "My agentic depth is current and hands-on. On ZeroClaw's 32.8k-star Rust gateway I ship "
    "the infrastructure AI agents run on: a merged context-window meter unifying 9 LLM "
    "providers for model routing and cost attribution (PR #7946), live serving-provider "
    "identity on usage events across fallback and model switches (PR #8966, open), and an "
    "agent lifecycle observer (idle/working/blocked/released) over JSON-RPC (PR #8337, "
    "requirements adopted into the vendor-neutral design). I work daily in "
    "build-validate-fix-resubmit loops with AI coding agents through structured context "
    "and reviewer-driven validation \u2014 the exact workflow your Playwright generation "
    "loops need.",

    "Two honest gaps and my ramp plan. Playwright itself is not in my employment history \u2014 "
    "my modern end-to-end base is Cypress, Selenium, JUnit, and Postman \u2014 so I ramp through "
    "transferable page-object, fixture, and convention discipline, starting with your existing "
    "framework's patterns. Likewise my CI history is Git/Bitbucket rather than GitLab, and I "
    "hold no Geb/Spock, Pact, or claims-system background, so I make no claim there; I bring "
    "migration discipline from production software conversions plus API-boundary testing "
    "judgment instead. What I offer from day one is the builder mindset: systems, feedback "
    "loops, and automation leverage that increase regression coverage and keep defects out "
    "of production.",
]

QUALIFICATIONS = [
    ("Automation systems, not test cases",
     "Regression suites with dashboards and alerting; CI quality gates per change; instrumentation aimed at highest-value gaps."),
    ("Agentic AI, hands-on",
     "Daily AI-agent build loops; RAG + guardrails shipped; provider routing, cost attribution, and lifecycle observability in a 32.8k-star gateway."),
    ("API vs. UI judgment",
     "REST, webhooks, and service-boundary verification across six enterprise integrations; end-to-end UI reserved for user journeys."),
    ("Honest ramp, fast start",
     "Cypress/Selenium page-object discipline into Playwright; Git CI into GitLab; migration and review rigor from day one."),
]

CLOSING = (
    "Gravie's mission \u2014 benefits people can actually use \u2014 deserves delivery machinery "
    "that moves fast without shipping defects. I'd welcome the chance to drive your "
    "Playwright migration to completion and scale the AI loops around it \u2014 happy to walk "
    "through any ZeroClaw PR or Knowledgecity pipeline decision in an interview."
)


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Cover_Letter_Gravie.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=base.HEADER_H + base.TOP_GAP,
                          bottomMargin=base.BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Cover Letter (Gravie Staff AI Test Automation Engineer)",
                          author="Eugene L. Buchanan",
                          subject="Application: Gravie Staff AI Test Automation Engineer",
                          keywords="Cover Letter, Gravie, AI Test Automation, Playwright, Agentic AI, SDET, CI/CD, GitLab, API testing, ZeroClaw")
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
    story.append(GravieHead(photo=photo_path))
    story.append(NextPageTemplate("content"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(LETTER_DATE, base.date_style))
    for line in RECIPIENT:
        story.append(Paragraph(line, base.addr_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph(SUBJECT, base.subj_style))
    story.append(base.AccentRule())
    story.append(Spacer(1, 6))

    story.append(Paragraph("Dear Gravie Hiring Team,", base.salute_style))

    for para in PARAGRAPHS:
        story.append(Paragraph(para, base.body_style))

    story.append(Paragraph("How I fit this role:", base.subj_style))
    qual_style = ParagraphStyle("qual3", parent=base.body_style, fontSize=8.4,
                                leading=11.4, leftIndent=12, bulletIndent=2,
                                spaceAfter=3.5)
    qual_col = []
    for title, desc in QUALIFICATIONS:
        txt = f'<b><font color="#2b1d63">{title}.</font></b>  {desc}'
        qual_col.append(Paragraph(txt, qual_style, bulletText="\u2022"))
    chart_col = [base.ProfitChart(
        "Value: Coverage Up, Defects Down",
        ["Gates", "Loops", "API", "Agents", "Scale", "Cover"],
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
    story.append(Paragraph("Staff AI Test Automation Engineer \u2014 Agentic Automation Systems", base.sign2_style))
    story.append(Paragraph("Apple Valley, CA (Remote)  \u00b7  eugene@serviceofothers.org  \u00b7  github.com/eugeneb50", base.sign2_style))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
