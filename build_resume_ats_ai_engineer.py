#!/usr/bin/env python3
"""Generate a generic ATS-friendly Senior AI Engineer resume PDF.

Employer-nonspecific: no company, location, or requisition mentions — reuse
for any Senior AI Engineer (Agentic AI, MCP, RAG) application.
Results are the highlights: a Selected Results section up front, STAR bullets
(Situation -> Action -> Result, one short line each) throughout.

Graphics-free, single column, Helvetica base-14, standard headings.
Content source: ressoft26.txt — no invented employers, dates, or credentials.
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
    "Senior software engineer with 25+ years shipping production systems, "
    "including Product Owner, Test Automation Lead, and Senior Quality "
    "Assurance (QA) roles. Author of herdr-mcp, a Rust Model Context Protocol "
    "(MCP) server exposing an agent multiplexer as 51 tools with an HTTP "
    "bridge and React playground. Helped ship a retrieval-augmented "
    "generation (RAG) AI support chatbot with guardrails under SOC 2 "
    "controls. Contributor to a 32.8k-star open-source Rust agentic gateway "
    "(model routing, lifecycle observability, serving-provider usage "
    "identity). Open to remote and onsite roles."
)

HIGHLIGHTS = [
    "<b>Authored herdr-mcp:</b> Rust MCP server, 51 tools, HTTP bridge plus React playground, recipe engine and scheduler — 299 tests passing.",
    "<b>Merged into a 32.8k-star gateway:</b> 39-commit context-window meter across 9 providers; 94-commit serving-provider usage identity.",
    "<b>Shipped RAG under compliance:</b> support chatbot with context retrieval and guardrails that cleared SOC 2 review.",
    "<b>Unified six enterprise platforms:</b> SAP, Oracle, Workday, Coursera, UKG, Zoom over SAML, OAuth, SFTP, REST, and webhooks.",
    "<b>Built the quality org:</b> hired and trained the automation team; regression suites with health dashboards and alerting.",
    "<b>Cut public-agency waste 53%:</b> youngest water board president in California history; blocked a floodplain build that later flooded.",
]

SKILLS = [
    "<b>MCP servers:</b> herdr-mcp in Rust — MCP stdio for Claude Desktop, Cursor, Claude Code, Continue, OpenCode",
    "<b>MCP tools and context management:</b> 51 tools (discovery, lifecycle, read/write, sync, agent-to-agent, trim, recipes, scheduler, folder-key, clipboard); live agent registry over Unix socket events",
    "<b>MCP transports and UI:</b> Axum HTTP bridge with JSON API; single-file React playground (run tools, chain recipes, inspect results); ratatui dashboard with mouse and keyboard nav",
    "<b>Agentic orchestration and trim:</b> recipe engine with variable interpolation; cron scheduler; lifecycle observer (idle/working/blocked/released); usage ledger with serving-provider identity; caveman/pfc1 trim pipeline with per-pane policies and per-folder keys",
    "<b>RAG and search:</b> shipped RAG chatbot with context retrieval and guardrails under SOC 2; Elasticsearch and SQL full-text search; evaluation of AI-generated code",
    "<b>LLM provider exposure:</b> 9-provider routing via OpenRouter plus 8 OpenAI-compatible endpoints; per-dimension pricing with explicit unpriced-usage provenance",
    "<b>Languages, delivery, leadership:</b> Rust, Python (Django/WordPress, scripting), JavaScript/TypeScript, Node.js, React, SQL; AWS (ECS, S3); CI/CD gates; dashboards; SOC 2; hired/trained automation team; backlog, KPIs, PDRs",
]


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Resume_ATS_AI_Engineer.pdf")

    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=48, bottomMargin=48,
        title="Eugene Lafayette Buchanan — Senior AI Engineer Resume",
        author="Eugene Lafayette Buchanan",
        subject="Senior AI Engineer Agentic AI MCP RAG — herdr-mcp server, RAG chatbot, agent orchestration",
        keywords="Senior AI Engineer, Agentic AI, MCP, herdr-mcp, RAG, LLM, Python, Rust, OpenRouter, Elasticsearch, CI/CD, SOC 2, ZeroClaw",
    )

    story = []
    story.append(P("Eugene Lafayette Buchanan", name_style))
    story.append(P("Senior AI Engineer — Agentic AI, MCP, RAG, LLM Routing", title_style))
    story.append(P(
        "Apple Valley, CA | San Quintin, Baja California, MX<br/>"
        "+1 (909) 545 5384 | +52 (616) 126 5089 | eugene@serviceofothers.org | "
        "github.com/eugeneb50 — herdr-mcp MCP server + ZeroClaw agentic gateway (32.8k stars)",
        contact_style))

    story.extend(section("Professional Summary"))
    story.append(P(SUMMARY))

    story.extend(section("Selected Results"))
    for h in HIGHLIGHTS:
        story.append(P(h, bullet_style, bullet="\u2022"))

    story.extend(section("Core Skills"))
    for s in SKILLS:
        story.append(P(s, skill_style))

    story.extend(section("Work Experience"))
    story.extend(job_block(
        "Senior QA Engineer / Test Automation Lead / Product Owner — Integrations (incl. RAG chatbot)",
        "Knowledgecity LLC, Remote, Dec 2020 – Aug 2025",
        [
            "Support team needed grounded answers over scattered content: helped ship a RAG chatbot with context retrieval and guardrails that cleared SOC 2 review.",
            "Six platforms, six auth dialects: shipped SAP, Oracle, Workday, Coursera, UKG, Zoom integrations over SAML, OAuth, SFTP, REST APIs, webhooks, SCORM, LTI.",
            "Complex deployments needed fast feedback: ran CI/CD quality pipelines with Cypress, Selenium, Postman, JUnit, Elasticsearch, S3 plus health dashboards and alerting.",
            "Inherited thin coverage and owned delivery: hired and trained the test team, built regression suites, and ran backlog and PDR life cycles with KPI tracking.",
        ]))
    story.extend(job_block(
        "Author — herdr-mcp MCP Server (github.com/eugeneb50/herdr-mcp)",
        "Independent, Rust, 2026 – Present",
        [
            "Agents had no MCP path into herdr workspaces: authored a Rust MCP server exposing the multiplexer as 51 tools.",
            "Needed browser access and repeatability: added an Axum HTTP bridge with a React playground plus a recipe engine with variable interpolation and a cron scheduler.",
            "Agent-to-agent messages wasted context: added a caveman/pfc1 trim pipeline with per-pane policies and per-folder keys.",
            "Result: 4-crate workspace with 299 passing tests, working from Claude Desktop, Cursor, Claude Code, Continue, and OpenCode.",
        ]))
    story.extend(job_block(
        "Open-Source Contributor — Agentic AI Infrastructure",
        "ZeroClaw Labs, github.com/zeroclaw-labs/zeroclaw, 32.8k GitHub stars, 2026 – Present",
        [
            "Routing and cost data scattered across 9 providers: built one context-window source of truth (PR #7946, merged Jul 2026, 39 commits).",
            "Fallbacks misattributed usage and cost: shipped live serving-provider identity on usage events with a per-attempt ledger and recovery policy (PR #8966, merged Sep 18, 2026, 94 commits).",
            "Agent state invisible to operators: built a lifecycle observer over JSON-RPC whose requirements fed the vendor-neutral design (PR #8337, superseded by #10269).",
        ]))
    story.extend(job_block(
        "Senior Software Engineer II (SDET Practice)",
        "RealNetworks, Seattle, WA, 1999 – 2001",
        [
            "SDET quality assurance across Linux, Unix, Windows, and embedded systems for streaming media; global presales across Japan, Korea, and the US.",
        ]))
    story.extend(job_block(
        "Earlier Software Test Engineering and Support Roles",
        "Microsoft, IBM, Keene Inc., 1996 – 1999",
        [
            "Microsoft (1999): Senior Test Engineer IV, Windows Media Server 4/5; nightly build automation. IBM (1998): high-availability servers; WHQL cluster failover.",
            "Microsoft (1997) / Keene (1996): OEM setup verification; frontline and escalated support ticketing.",
        ]))
    story.extend(job_block(
        "Business Consultant — Campus IT, Software Evaluation and Migration",
        "Medico Investments LLC / Foremost Senior Care / Foremost Organization, Hesperia, CA, 2013 – 2016",
        [
            "Evaluated and migrated accounting and medical-records software; ran campus IT support (security/backup policies, surveillance, wireless).",
        ]))
    story.extend(job_block(
        "IT Manager; Freelance IT Consultant (Django / WordPress); Retail Service Desk",
        "Lucerne Valley Unified School District (2002); Amp Computer, Apple Valley (2003 – 2011); Geek Squad, Best Buy, Victorville (2007)",
        [
            "District support across four campuses with ETL for state reporting; freelance Django/WordPress builds with ERP and CRM.",
            "Retail service desk: ticket triage, PC setup, data migration, hardware repair.",
        ]))
    story.extend(section("Education"))
    for e in ["Associate Degree, Victor Valley College",
              "Toastmasters International (technical communication and documentation)"]:
        story.append(P(e, edu_style, bullet="\u2022"))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
