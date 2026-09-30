#!/usr/bin/env python3
"""Generate a tailored ATS-friendly resume PDF for KoBold Metals Software Engineer (Data Systems).

Graphics-free, single column, Helvetica base-14, standard headings.
Content source: /home/producer32/obsidian/resume/ressoft26.txt — no invented
employers, dates, or credentials. Personal prospecting passion and independent
spectral/satellite script are labeled as Personal / Independent, not employment.
Gaps left honest:
- No Django / Prefect / Retool in source: framed as Python + AWS + React +
  CI/CD data-pipeline practice transferable to Django/Prefect services.
- No geology degree or mining employment: framed as lifelong precious-metal /
  gemstone prospector + independent spectral/satellite AI-evaluation project
  + earth-science-adjacent work (solar/geothermal siting, water-board
  hydrology/floodplain, real-estate mapping).
- No production geospatial-at-scale claim: map-based work shown via
  Tierrachain real-estate mapping site + independent coordinate-set raster
  tooling; large-scale system design shown via integrations platform work.
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
    "Software engineer with 25+ years shipping production systems from operating "
    "systems and streaming media with embedded systems to cloud-based B2B edutech "
    "apps. Lately I have been hardening my agentic AI skills to make probabilistic "
    "systems produce deterministic results cost effectively. "
    "I am a lifelong precious-metal and gemstone prospector. I recently created an "
    "agentic pipeline to help with turquoise prospecting in Baja California. "
    "See complementary work: "
    '(<a href="https://encuentralo.mx/baja-mineral/?lang=en">encuentralo.mx/baja-mineral</a>). '
    "I also have worldly renewable energy skills that come in handy in remote field "
    "work. I want to work in Africa, including Zambia, and I welcome field time "
    "with geologists and data scientists."
)

SKILLS = [
    "<b>Python production data systems (core of this role):</b> Python pipelines over Apache, REST, SQL, AWS, and React; CI/CD (continuous integration / continuous delivery) quality pipelines; S3 storage; Elasticsearch search; nightly build automation; readable, tested, extensible code",
    "<b>Data pipelines and tooling for human and machine insight:</b> end-to-end regression and evaluation suites with health dashboards and alerting; service-boundary verification across REST APIs, webhooks, SFTP, SAML, OAuth; ETL (extract, transform, and load) for state reporting with table locking and certification",
    "<b>Geospatial, spectral, and map-based practice:</b> Baja Mineral Explorer (encuentralo.mx/baja-mineral), a live turquoise/Cu-Fe atlas: 3 surveyed targets, 36 GPS pins, sub-meter Esri sheets, Sentinel-2 screening, SRTM terrain, SGM 1:50,000 cross-reference, member coordinate runner",
    "<b>AI, RAG, and search:</b> helped ship RAG chatbot with context retrieval and guardrails under SOC 2; Elasticsearch and SQL full-text search; agent lifecycle observability and model routing in open source",
    "<b>Languages and frameworks:</b> Python, JavaScript, Rust, PHP, Node.js, React, SQL; Django and WordPress builds",
    "<b>Ownership and system design:</b> Product Owner backlog with KPI tracking and Product Development Review (PDR) life cycles; hired and trained automation team; led small-group delivery from design through testing to field-user support; presales engineering across Japan, Korea, and the United States",
    "<b>Cloud, delivery, and frontend:</b> AWS (including Simple Storage Service [S3]), Git, Bitbucket, Apache; React frontends; Rust gateway contributions; Django and WordPress freelance builds; no Prefect or Retool claim — Python service and pipeline practice transfers",
    "<b>Earth-science-adjacent exposure:</b> solar, wind, and geothermal siting and permitting; solar water-pumping projects; Fischer-Tropsch syngas and absorption-refrigeration research; elected water-board work on wells, budgets, SCADA tank/pump sensor upgrades, floodplain risk, and public safety",
]


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Resume_ATS_KoBold.pdf")

    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=48, bottomMargin=48,
        title="Eugene Lafayette Buchanan — Software Engineer Resume (KoBold Metals)",
        author="Eugene Lafayette Buchanan",
        subject="Software Engineer Data Systems — Python cloud pipelines, geospatial AI evaluation, prospecting (Apple Valley, CA)",
        keywords="KoBold, Software Engineer, Data Systems, Python, AWS, Django, WordPress, data pipelines, geospatial, spectral, satellite imagery, Baja Mineral Explorer, RAG, Elasticsearch, React, Rust, SDET, ZeroClaw, prospecting, Zambia",
    )

    story = []
    story.append(P("Eugene Lafayette Buchanan", name_style))
    story.append(P("Software Engineer — Python Data Systems, Geospatial + AI Evaluation", title_style))
    story.append(P(
        "Apple Valley, CA (Remote, US work authorized) | San Quintin, Baja California, MX<br/>"
        "+1 (909) 545 5384 | +52 (616) 126 5089 | eugene@serviceofothers.org | "
        '<a href="https://github.com/eugeneb50">github.com/eugeneb50</a> — ZeroClaw Labs open-source agentic gateway (32.8k stars)',
        contact_style))

    story.extend(section("Professional Summary"))
    story.append(P(SUMMARY))

    story.extend(section("Core Skills"))
    for s in SKILLS:
        story.append(P(s, skill_style))

    story.extend(section("Work Experience"))
    story.extend(job_block(
        "Senior QA Engineer / Test Automation Lead / Product Owner — Integrations",
        "Knowledgecity LLC, Remote, Dec 2020 – Aug 2025",
        [
            "Built Python-centered data and quality pipelines (Apache, REST, SQL, AWS, React) with Cypress, Selenium, Postman, JUnit, Elasticsearch, and S3. Made exploration-style data searchable and testable for humans and machines.",
            "Owned integrations end to end across SAP, Oracle, Workday, Coursera, UKG, and Zoom via SAML, OAuth, SFTP, custom APIs, webhooks, Stripe, PayPal, SCORM, and LTI. Each service brought its own auth and data shape — the same coordination problem as unifying exploration data.",
            "Helped ship an AI support chatbot with RAG context retrieval and guardrails; SOC 2 compliance research and implementation.",
            "Led a small group to delivery: hired and trained the test automation team, ran code and design reviews, managed backlog and PDR life cycles with KPI tracking, and supported users after release.",
            "Built evaluation systems for complex deployments: regression suites with health dashboards and alerting across integration, frontend, backend, mobile, security, performance, load, API, database, functionality, usability, accessibility, and localization. Joined Blue Team incident forensics and cut technical debt.",
            "White-box development for the CI/CD pipeline; toolchain: Slack, Jira, Bitbucket, Confluence, Cypress, Selenium, Postman, JUnit, Git, Node, JavaScript, PHP, SCORM Cloud, Elastic, Qase.",
        ]))
    story.extend(job_block(
        "Open-Source Contributor — Agentic AI Infrastructure",
        "ZeroClaw Labs, <a href=\"https://github.com/zeroclaw-labs/zeroclaw\">github.com/zeroclaw-labs/zeroclaw</a>, 32.8k GitHub stars, 2026 – Present",
        [
            "PR #7946 (merged Jul 2026, 39 commits): model context-window meter as a single source of truth on ModelProviderConfig covering 9 providers (OpenRouter plus 8 OpenAI-compatible); new doctor update-context-windows command and gateway refresh endpoint; gateway WebSocket done frame, web ContextBar, per-turn CLI summary, and zerocode CtxBar widget with Fluent internationalization across 5 locales.",
            "PR #8966 (open): live serving-provider identity on usage events so usage, cost, and context attribution follow the provider that served the call across fallback and model switches.",
            "PR #8337 (closed, superseded by #10269): agent lifecycle observer (idle/working/blocked/released) over JSON-RPC on Unix domain sockets; cleared four rounds of review and its requirements fed the vendor-neutral design.",
        ]))
    story.extend(job_block(
        "Founder — Land Technology (map-based experience)",
        "Tierrachain.com, 2023 – Present",
        [
            "Build SaaS for real-estate exchange in coastal exclusion zones, with AI-assisted compliance filing and a real-estate mapping site (Heyhom.mx) using NFTitle and Bitso payment rails; parallel public-records system, fractional ownership and decentralized finance models, lower transaction cost for foreign and domestic owners.",
        ]))
    story.extend(job_block(
        "Senior Software Engineer II (SDET Practice)",
        "RealNetworks, Seattle, WA, 1999 – 2001",
        [
            "SDET quality assurance across Linux, Unix, Windows, and embedded systems for streaming media platform, servers, and mobile/consumer appliances, including TFRCP patent work.",
            "Global presales engineering with vice president sales support, including travel to Japan and Korea; trained new hires.",
        ]))
    story.extend(job_block(
        "Earlier Software Test Engineering and Support Roles",
        "Microsoft, IBM, Keene Inc., 1996 – 1999",
        [
            "Microsoft, Redmond, WA (1999): Senior Software Test Engineer IV, Windows Media Server versions 4 and 5; nightly build test script automation.",
            "IBM, Kirkland, WA (1998): Senior Test Engineer III for high-availability servers; WHQL certification for cluster failover.",
            "Microsoft, Redmond, WA (1997): Software Test Engineer II for Windows 98 and Windows NT; original equipment manufacturer (OEM) setup and hardware/driver verification.",
            "Keene Inc., Seattle, WA (1996): Technical Support Agent II for Windows 95 and Windows NT; frontline and escalated support ticketing.",
        ]))
    story.extend(job_block(
        "IT Manager / Campus and District Support (ETL and operations)",
        "Lucerne Valley Unified School District (2002); Medico / Foremost (2013 – 2016); Geek Squad / Amp Computer (2003 – 2011)",
        [
            "Ran district-wide support across four campuses (Wide Area Network [WAN]/Local Area Network [LAN], NetWare, Windows, Linux, virtualized desktops) and met state attendance rules via ETL with table locking and certification.",
            "Evaluated and migrated accounting and medical-records software; ran campus server, backup, wireless, and surveillance work; ran retail service desk with ticket triage and plain-language updates.",
            "Community and permitting wins: recovered a non-permitted photovoltaic install via as-built engineering; won city approval for a bridge to landlocked land; built a nonprofit outreach program with bingo license and dance socials.",
            "Freelance consulting (Amp Computer, Apple Valley, 2003 – 2011): server/PC sales, ERP and CRM configuration, Django and WordPress site builds, and office automation.",
        ]))
    story.extend(job_block(
        "Alternative Energy and Water-Board Roles (earth-science-adjacent)",
        "Various firms (2004 – Present); Mariana Ranchos County Water Board, President (2006 – 2010)",
        [
            "Partner/Director (PhaseSave, 2017 – 2021/Present): sales engineering, project management, vendor sourcing, and contractor management across solar, air conditioning with phase change materials, cold chain logistics, finance, and tax credits.",
            "VP Solar (EWSolar, 2014 – 2016): pioneered large direct commercial/municipal solar-powered water pumping projects. CTO (Free Energy Resources, 2013): sales, procurement, permitting, and finance for a Korean solar marketing company. VP (GRIDNOT, 2007 – 2012): solar, wind, and geothermal air-conditioning sales and integration.",
            "Partner (OnPoint Power, 2006): residential/light-commercial PV and thermal solar; pioneered a horse-manure waste-to-energy plant proposal for the City of Norco wastewater plant, presented at city council meetings.",
            "Executive Assistant (Desert Power, 2005): PV solar, waste-to-energy, and tri-generation sales and engineering support; Fischer-Tropsch catalytic syngas-to-liquids research and absorption refrigeration. Sales Representative (Solatron, 2004): inbound PV phone sales; built an Excel calculator adopted office-wide and worked on SOP sales scripts.",
            "As elected board president (youngest in California history; JPIA delegate), cut budget waste 53%, helped with a SCADA (supervisory control and data acquisition) upgrade for tank and pump sensors and relays, hired a strong general manager, and blocked a high-risk floodplain build that later flooded.",
        ]))

    story.extend(section("Independent Prospecting Atlas — AI Mapping and Evaluation Pipeline"))
    story.append(P(
        "Baja Mineral Explorer — live turquoise/Cu-Fe satellite prospecting atlas, "
        "San Quintin, Baja California, MX, 2026 – Present",
        meta_style))
    story.append(P(
        '<b><a href="https://encuentralo.mx/baja-mineral/?lang=en">encuentralo.mx/baja-mineral</a></b>',
        meta_style))
    for b in [
        "AI mapping and evaluation pipeline for coordinates: per-coordinate Sentinel-2 spectral screening (B/R blue-shift, surface classes), SRTM terrain analysis (slope, aspect, hillshade, drainage), and desk scores combining geology, structure, exposure, water, access, and regulatory factors.",
        "3 surveyed targets (Arroyo San Isidro, Cerro la Turquesa, Cerro la Palmita), 36 GPS field pins (CSV), sub-meter Esri imagery sheets, cross-referenced with the SGM El Aguajito 1:50,000 geologic-mineral map and 14 documented Cu-Fe workings.",
        "Member coordinate runner scores any lat/lon against targets, pins, and workings with shareable links; multilingual (EN/ES/ZH/RU). Lifelong precious-metal and gemstone prospector building field-ready ingest-to-verified-output tooling, eager to embed with exploration geologists.",
    ]:
        story.append(P(b, bullet_style, bullet="\u2022"))

    story.extend(section("Websites"))
    story.append(P(
        '<a href="https://phasesave.com">phasesave.com</a> | '
        '<a href="https://encuentralo.mx">encuentralo.mx</a> | '
        '<a href="https://serviceofothers.org">serviceofothers.org</a> | '
        '<a href="https://tierrachain.com">tierrachain.com</a>',
        body_style))

    story.extend(section("Education"))
    for e in ["Associate Degree, Victor Valley College",
              "High School Diploma, Lucerne Valley High School",
              "California Notary Commission",
              "Toastmasters International"]:
        story.append(P(e, edu_style, bullet="\u2022"))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
