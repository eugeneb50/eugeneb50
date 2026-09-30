#!/usr/bin/env python3
"""Generate a tailored ATS-friendly resume PDF for Gravie Staff AI Test Automation Engineer.

Graphics-free, single column, Helvetica base-14, standard headings.
Content source: /home/producer32/obsidian/resume/ressoft26.txt — no invented
employers, dates, or credentials. Gaps vs. requisition are left honest:
- No Playwright in source: framed as Cypress/Selenium/JUnit modern-E2E
  practitioner with page-object/fixture discipline transferable to Playwright.
- No GitLab in source (Git/Bitbucket CI): framed as transferable pipeline,
  quality-gate, parallelization/caching practice.
- No Geb/Spock/Groovy, no Pact, no claims/health-insurance background:
  no claim made; migration + API/contract-adjacent integration work shown instead.
- No HIPAA/PII/Okta/RBAC content (none in source).
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                HRFlowable)

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"

name_style = ParagraphStyle("name", fontName=FONT_B, fontSize=18, leading=22,
                            alignment=TA_LEFT, spaceAfter=2)
title_style = ParagraphStyle("title", fontName=FONT, fontSize=11, leading=14,
                             alignment=TA_LEFT, spaceAfter=2)
contact_style = ParagraphStyle("contact", fontName=FONT, fontSize=9,
                               leading=12, alignment=TA_LEFT, spaceAfter=6)
h2_style = ParagraphStyle("h2", fontName=FONT_B, fontSize=12, leading=15,
                          alignment=TA_LEFT, spaceBefore=6, spaceAfter=4)
job_style = ParagraphStyle("job", fontName=FONT_B, fontSize=10.5, leading=13.5,
                           alignment=TA_LEFT, spaceBefore=5, spaceAfter=1)
meta_style = ParagraphStyle("meta", fontName=FONT, fontSize=9.5, leading=12,
                            alignment=TA_LEFT, spaceAfter=3)
body_style = ParagraphStyle("body", fontName=FONT, fontSize=9.5, leading=13,
                            alignment=TA_LEFT, spaceAfter=4)
bullet_style = ParagraphStyle("bullet", fontName=FONT, fontSize=9.5,
                              leading=13, alignment=TA_LEFT, leftIndent=18,
                              bulletIndent=6, spaceAfter=1)
skill_style = ParagraphStyle("skill", fontName=FONT, fontSize=9.5, leading=13,
                             alignment=TA_LEFT, leftIndent=0, spaceAfter=2)
edu_style = ParagraphStyle("edu", fontName=FONT, fontSize=9.5, leading=13,
                           alignment=TA_LEFT, leftIndent=18, bulletIndent=6,
                           spaceAfter=2)


def P(text, style=body_style, bullet=None):
    return Paragraph(text, style, bulletText=bullet)


def section(title):
    return [P(title, h2_style),
            HRFlowable(width="100%", thickness=0.6, spaceAfter=4)]


def job_block(role, meta, bullets):
    out = [P(role, job_style), P(meta, meta_style)]
    for b in bullets:
        out.append(P(b, bullet_style, bullet="\u2022"))
    return out


SUMMARY = (
    "Staff-level test automation engineer with 25+ years in Software Development "
    "Engineer in Test (SDET) and Quality Assurance (QA) practice, including Test "
    "Automation Lead and Product Owner roles. I build automation systems, not just "
    "test cases: end-to-end regression suites with health dashboards and alerting, "
    "CI/CD (continuous integration / continuous delivery) quality pipelines with "
    "gates on every change, and API-layer coverage at service boundaries. I evaluate "
    "AI-generated code in production, shipped a retrieval-augmented generation (RAG) "
    "support chatbot with guardrails, and contribute agentic AI infrastructure to a "
    "32.8k-star open-source Rust gateway (agent lifecycle observability, model routing "
    "and cost attribution). Modern end-to-end frameworks are Cypress, Selenium, JUnit, "
    "and Postman; I ramp that page-object, fixture, and feedback-loop discipline to "
    "Playwright conventions. Git-based CI practice (Git, Bitbucket) transfers to GitLab "
    "pipelines, merge request workflows, parallelization, and caching."
)

SKILLS = [
    "<b>AI-driven automation systems (core of this role):</b> agentic AI infrastructure in production Rust gateway; evaluation of AI-generated code; RAG chatbot with context retrieval and guardrails; prompt, context-structure, and validation-pattern iteration through maintainer review; feedback loops between local runs, CI results, and resubmission",
    "<b>End-to-end automation (Playwright-transferable):</b> Cypress, Selenium, JUnit, Postman, Qase; page-object and fixture discipline; end-to-end regression suites with health dashboards and alert systems; pass/fail trend, flakiness, and coverage-gap instrumentation used to aim new tests at highest-value gaps; white-box testing",
    "<b>API and contract-adjacent testing:</b> REST API testing with Postman and custom APIs; webhooks; SFTP; service-boundary judgment (UI vs. API layer); integration verification across SAP, Oracle, Workday, Coursera, UKG, Zoom via SAML, OAuth, SFTP, SCORM, LTI (no Pact claim; no claims-system claim)",
    "<b>CI/CD and delivery:</b> CI/CD quality pipelines (Apache, REST, SQL, AWS, React frontend); nightly build test script automation; quality gates per change; Git and Bitbucket merge workflows transferable to GitLab; parallelization and caching for fast feedback; Elasticsearch, S3, Docker",
    "<b>Migration practice:</b> software evaluation and migration (accounting and medical-records software), nightly-build automation across OS generations, and large-suite maintenance with coverage continuity — transferable to Geb/Spock-to-Playwright conversion with AI agents (no Geb/Spock/Groovy claim)",
    "<b>Languages and stack:</b> JavaScript, TypeScript, Python, Rust, PHP, Node.js, React, SQL; AWS (Elastic Compute Cloud [ECS pattern], Simple Storage Service [S3]); Apache; Git; Bitbucket; Elasticsearch; Scorm Cloud",
    "<b>Leadership and communication:</b> hired and trained test automation team; Product Owner backlog with KPI tracking and Product Development Review (PDR) life cycles; cross-functional work with QA, Engineering, and Product; plain-language trade-off explanations, documentation, and SOP guides",
    "<b>Quality practice:</b> SOC 2 compliance research and implementation; Blue Team incident forensics; regression, performance, load, security, usability, accessibility, and localization testing; technical debt reduction",
]


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Resume_ATS_Gravie.pdf")

    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=48, bottomMargin=48,
        title="Eugene Lafayette Buchanan — Staff AI Test Automation Engineer Resume (Gravie)",
        author="Eugene Lafayette Buchanan",
        subject="Staff AI Test Automation Engineer — AI-driven Playwright automation, CI/CD, API testing (Apple Valley, CA)",
        keywords="Staff AI Test Automation Engineer, SDET, Agentic AI, AI test generation, Cypress, Selenium, JUnit, Postman, Playwright-transferable, REST API, CI/CD, GitLab-transferable, regression dashboards, flakiness, RAG, guardrails, SOC 2, Rust, ZeroClaw, Gravie",
    )

    story = []
    story.append(P("Eugene Lafayette Buchanan", name_style))
    story.append(P("Staff AI Test Automation Engineer — Agentic Automation Systems, SDET Lead", title_style))
    story.append(P(
        "Apple Valley, CA (Remote) | +1 (909) 545 5384 | eugene@serviceofothers.org<br/>"
        "github.com/eugeneb50/eugeneb50 — ZeroClaw Labs open-source agentic gateway (32.8k stars)",
        contact_style))

    story.extend(section("Professional Summary"))
    story.append(P(SUMMARY))

    story.extend(section("Core Skills — Mapped to Gravie Requirements"))
    for s in SKILLS:
        story.append(P(s, skill_style))

    story.extend(section("Work Experience"))
    story.extend(job_block(
        "Senior QA Engineer / Test Automation Lead / Product Owner — Integrations",
        "Knowledgecity LLC, Remote, Dec 2020 – Aug 2025",
        [
            "Built the automation system, not just test cases: hired and trained the test automation team and shipped end-to-end regression suites with health dashboards and alert systems covering complex deployment scenarios — the same pass/fail, flakiness, and coverage-gap instrumentation Gravie uses to aim AI test generation.",
            "Ran a CI/CD quality pipeline (Apache, REST, SQL, AWS, React) with Cypress, Selenium, Postman, JUnit, Elasticsearch, and S3 under Git/Bitbucket merge workflows — pipeline configuration, test stages, and per-change quality gates transferable to GitLab, with parallelization and caching for fast feedback.",
            "Practiced API-vs-UI judgment daily: verified integrations at service boundaries (custom REST APIs, webhooks, SFTP, SAML, OAuth, SCORM, LTI) across SAP, Oracle, Workday, Coursera, UKG, and Zoom, reserving end-to-end UI tests for real user journeys.",
            "Iterated prompts, context structures, and validation patterns on a shipped AI support chatbot with RAG context retrieval and guardrails; evaluated AI-generated code under SOC 2 controls — directly transferable to raising AI first-pass test-generation rates.",
            "Led quality across integration, frontend, backend, mobile, security, performance, load, API, database, functionality, usability, accessibility, and localization testing; reduced technical debt and joined Blue Team incident forensics.",
            "Managed dev and test teams, product backlog, and PDR life cycles with KPI tracking as Integrations Product Owner; coordinated QA, Engineering, and Product on coverage, delivery timelines, and defect risk.",
        ]))
    story.extend(job_block(
        "Open-Source Contributor — Agentic AI Infrastructure (hands-on agent workflows at scale)",
        "ZeroClaw Labs, github.com/zeroclaw-labs/zeroclaw, 32.8k GitHub stars, 2026 – Present",
        [
            "PR #7946 (merged Jul 2026, 39 commits): model context-window meter across TUI, gateway agent chat, and CLI covering 9 providers — one source of truth for model routing and cost attribution, the same provider/model bookkeeping AI test-generation infrastructure needs.",
            "PR #8966 (open, needs-maintainer-review, 80 commits): live serving-provider identity on usage events so usage, cost, and context attribution follow the provider that actually served the call across fallback and model switches, with per-attempt ledger and failure-recovery policy.",
            "PR #8337 (closed, superseded by #10269): agent lifecycle observer (idle/working/blocked/released) over JSON-RPC on Unix domain sockets — feedback-loop infrastructure letting agents run, interpret results, and resubmit; cleared four rounds of maintainer review and its requirements were adopted into the vendor-neutral lifecycle design.",
            "Daily hands-on agentic development: build-validate-fix-resubmit loops with AI coding agents, structured context assembly, and reviewer-driven validation — the exact workflow Gravie applies to AI-generated Playwright tests.",
        ]))
    story.extend(job_block(
        "Senior Software Engineer II (SDET Practice)",
        "RealNetworks, Seattle, WA, 1999 – 2001",
        [
            "SDET quality assurance across Linux, Unix, Windows, and embedded systems for streaming media platform, servers, and mobile/consumer appliances, including TFRCP patent work.",
            "Global presales engineering with vice president sales support, including travel to Japan, Korea, and the continental United States; trained new hires.",
        ]))
    story.extend(job_block(
        "Earlier Software Test Engineering and Support Roles",
        "Microsoft, IBM, Keene Inc., 1996 – 1999",
        [
            "Microsoft, Redmond, WA (1999): Senior Software Test Engineer IV, Windows Media Server versions 4 and 5; nightly build test script automation — early local-execution-to-CI feedback loop.",
            "IBM, Kirkland, WA (1998): Senior Test Engineer III for high-availability servers; WHQL certification for cluster failover.",
            "Microsoft, Redmond, WA (1997): Software Test Engineer II for Windows 98 and Windows NT; original equipment manufacturer (OEM) setup and hardware/driver verification.",
            "Keene Inc., Seattle, WA (1996): Technical Support Agent II for Windows 95 and Windows NT; frontline and escalated support ticketing.",
        ]))
    story.extend(job_block(
        "Business Consultant — Campus IT, Software Evaluation and Migration",
        "Medico Investments LLC / Foremost Senior Care / Foremost Organization, Hesperia, CA, 2013 – 2016",
        [
            "Evaluated and migrated accounting and medical-records software — migration discipline (coverage continuity during conversion) transferable to legacy-to-modern framework migration.",
            "Ran campus IT support: security and backup policies for servers and PCs, video surveillance upgrade, campus-wide wireless; set up sound/video and ran events.",
        ]))
    story.extend(job_block(
        "IT Manager",
        "Lucerne Valley Unified School District, Lucerne Valley, CA, 2002",
        [
            "Supported four campuses (Wide Area Network [WAN]/Local Area Network [LAN], NetWare, Windows, Linux, virtualized desktops, audio/video).",
            "Met state attendance submission requirements via data Extract, Transform, and Load (ETL) with table locking and certification.",
        ]))

    story.extend(section("Education"))
    for e in ["Associate Degree, Victor Valley College",
              "California Notary Commission",
              "Toastmasters International (technical trade-off communication and documentation)"]:
        story.append(P(e, edu_style, bullet="\u2022"))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
