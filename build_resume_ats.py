#!/usr/bin/env python3
"""Generate an ATS-friendly resume PDF for Eugene Lafayette Buchanan.

Deliberately graphics-free: single column, no images/charts/tables, standard
section headings, one font family (Helvetica base-14), "Month YYYY" dates,
acronyms spelled out on first use, plain-English copy (deslop skill).
Content source: ressoft27.txt (single source of truth). Revised Nov 8, 2026.
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                HRFlowable)

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"

# ----------------------------------------------------------------------------
# Styles — one font family only
# ----------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------
# Content — plain English, active voice, acronyms spelled out on first use
# ----------------------------------------------------------------------------
SUMMARY = (
    "Senior SDET and QA Automation Lead with 25+ years testing and shipping "
    "software, from streaming media and operating systems to learning management "
    "integrations, now training and evaluating frontier AI models as an Expert AI "
    "Trainer at micro1. I lead test automation teams, build regression suites with "
    "health dashboards and alerting, evaluate AI-generated code, and ship SaaS "
    "integrations (SAP, Oracle, Workday, Coursera, UKG, Zoom). I also bring "
    "hands-on IT operations: campus support, retail service desk, ticket queues, "
    "and software evaluation and migration. "
    "I write clean code, build reliable test systems, and explain complex ideas clearly."
)

SKILLS = [
    "<b>Testing and QA:</b> Cypress, Selenium, Postman, JUnit, Qase, Software Development Engineer in Test (SDET) practice, white-box testing, regression suites, health dashboards and alerting, performance and load testing, accessibility testing, security testing, usability and localization testing",
    "<b>AI Code Evaluation and Automation:</b> AI model training and evaluation against defined quality criteria, evaluation of AI-generated code, AI support chatbot with retrieval-augmented generation (RAG) and guardrails, prompt engineering, large language model (LLM) integration in shipped products, AI automation",
    "<b>Integrations and Auth:</b> SAP, Oracle, Workday, Coursera, UKG, Zoom, SAML, OAuth, SFTP, REST APIs, webhooks, SCORM, LTI",
    "<b>Languages and Frameworks:</b> JavaScript, TypeScript, Python, Rust, PHP, Node.js, React, SQL",
    "<b>Cloud, CI/CD and DevOps:</b> AWS (ECS, S3), Apache, CI/CD pipelines, Docker, Git, Bitbucket, Elasticsearch, nightly build automation",
    "<b>Collaboration and Tooling:</b> Slack, Jira, Confluence, SCORM Cloud",
    "<b>Support and Operations:</b> ticket triage and queue support, retail service desk, campus IT support, security and backup policies, wireless and video surveillance, software evaluation and migration, IT asset tracking",
    "<b>Compliance and Quality Practice:</b> SOC 2 compliance research and implementation, Blue Team incident forensics, technical debt reduction, Standard Operating Procedure (SOP) guides, technical writing",
    "<b>Platforms and Domains:</b> ERP, CRM, learning management systems (LMS), streaming media, enterprise software, alternative energy, real estate",
    "<b>Leadership and Communication:</b> Team building, mentoring, training, cross-functional collaboration, product ownership, backlog management, PDR life cycles, presales engineering",
]


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Resume_ATS.pdf")

    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=48, bottomMargin=48,
        title="Eugene Lafayette Buchanan — Resume",
        author="Eugene Lafayette Buchanan",
        subject="Senior SDET / QA Automation Lead + AI code evaluator + SaaS integrations engineer (Apple Valley, CA)",
        keywords="Senior SDET, QA Automation Lead, AI code evaluator, SaaS integrations, SAP, Oracle, Workday, RAG, SOC 2, Blue Team, Cypress, Selenium, JUnit, streaming media, WHQL, campus IT support, retail service desk, Geek Squad, knowledge base, SOP, Rust",
    )

    story = []
    story.append(P("Eugene Lafayette Buchanan", name_style))
    story.append(P("Senior SDET / QA Automation Lead + AI Code Evaluator + SaaS Integrations Engineer", title_style))
    story.append(P(
        "Apple Valley, CA, San Quintin, Baja California, MX | +1 (909) 545 5384 | "
        "+52 (616) 126 5089 | eugene@serviceofothers.org", contact_style))

    story.extend(section("Professional Summary"))
    story.append(P(SUMMARY))

    story.extend(section("Skills"))
    for s in SKILLS:
        story.append(P(s, skill_style))

    story.extend(section("Work Experience — Software Engineering"))
    story.extend(job_block(
        "Expert AI Trainer, Senior Software Engineer",
        "micro1, Remote (contract), Sep 2026 – Present",
        [
            "Train and evaluate frontier AI models on senior engineering work, grading model-generated code, designs, and reasoning against defined quality criteria and documenting each defect for training.",
            "Certified by assessment in System Architecture, Software Testing, and quality evaluation at volume.",
        ]))
    story.extend(job_block(
        "Senior QA Engineer / Test Automation Lead / Product Owner — Integrations",
        "Knowledgecity LLC, Remote, Dec 2020 – Aug 2025",
        [
            "Led QA across integration, frontend, backend, mobile, security, performance, load, API, database, functionality, usability, accessibility, and localization testing. Reduced technical debt and joined Blue Team incident forensics.",
            "Built and maintained a CI/CD quality pipeline (Apache, REST, SQL, AWS, React) with Cypress, Selenium, Postman, JUnit, and Qase.",
            "Built the test automation function from nothing: recruited, hired, and trained the engineers. Built end-to-end regression suites with health dashboards and alert systems for complex deployment scenarios.",
            "Shipped integrations with SAP, Oracle, Workday, Coursera, UKG, and Zoom using SAML, OAuth, SFTP, custom APIs, webhooks, SCORM, and LTI.",
            "As Integrations Product Owner, led two developers and two test engineers through the full software development life cycle against written KPIs.",
            "Shipped an AI support assistant with retrieval-augmented generation (RAG) and guardrails, working with engineering on context retrieval, and implemented the SOC 2 controls it passed compliance review on.",
        ]))
    story.extend(job_block(
        "Business Consultant — Campus IT and Community Programs",
        "Medico Investments LLC / Foremost Senior Care / Foremost Organization, Hesperia, CA, 2013 – 2016",
        [
            "Provided campus IT support: wrote security and backup policies for campus servers and PCs, upgraded video surveillance for better quality and remote access, and installed campus-wide wireless. Set up sound and video equipment and MC'ed events.",
            "Evaluated and migrated accounting and medical-records software.",
            "Brought a non-permitted solar installation to city permit to operate using as-built engineering.",
            "Reviewed business plans and cut procurement, operations, and staffing costs; built a nonprofit community outreach program and won city approval for a bridge to landlocked land.",
        ]))
    story.extend(job_block(
        "Computer Service Technician — Geek Squad",
        "Best Buy, Victorville, CA, 2007",
        [
            "Ran the retail service desk: logged tickets, triaged walk-in customers, tracked units through check-in, repair, and pickup, and gave plain-language status updates.",
            "Set up new PCs, migrated user data, and fixed virus, operating system, and hardware issues; handled service plans, payments, and refunds.",
        ]))
    story.extend(job_block(
        "Freelance IT Consultant",
        "Amp Computer, Apple Valley, CA, 2003 – 2011",
        [
            "Sold and supported servers and PCs; configured ERP, CRM, and office automation systems.",
        ]))
    story.extend(job_block(
        "IT Manager",
        "Lucerne Valley Unified School District, Lucerne Valley, CA, 2002",
        [
            "Provided district-wide support across four school campuses, including WAN/LAN, NetWare servers, Windows, Linux, and virtualized desktops, plus audio/video equipment.",
            "Met state attendance submission requirements, running data extract, transform, and load (ETL) with database table locking and certification.",
        ]))
    story.extend(job_block(
        "Senior Software Engineer II",
        "RealNetworks, Seattle, WA, 1999 – 2001",
        [
            "Ran Software Development Engineer in Test (SDET) quality assurance across Linux, Unix, Windows, and embedded systems for a streaming media platform.",
            "Served on the advanced research team (appliances, mobile, stream servers, cellular networks) and validated the scalable video streaming technology behind RealNetworks patent US 7,075,986.",
            "Delivered global presales engineering for consumer devices with the VP of Sales in Japan, Korea, and the United States. Trained new hires.",
        ]))
    story.extend(job_block(
        "Earlier Software Test Engineering and Support Roles",
        "Microsoft, IBM, Keene Inc., 1996 – 1999",
        [
            "Microsoft, Redmond, WA (1999): Senior Software Test Engineer IV, Windows Media Server versions 4 and 5; nightly build test script automation.",
            "IBM, Kirkland, WA (1998): Senior Test Engineer III; WHQL cluster-failover certification for high-availability servers.",
            "Microsoft, Redmond, WA (1997): Software Test Engineer II for Windows 98 and Windows NT; original equipment manufacturer (OEM) setup and hardware/driver verification.",
            "Keene Inc., Seattle, WA (1996): Technical Support Agent II for Windows 95 and Windows NT; frontline and escalated support ticketing.",
        ]))
    story.extend(section("Work Experience — Additional Professional Roles"))
    story.extend(job_block(
        "Alternative Energy Consultant",
        "2004 – Present",
        [
            "PhaseSave.com, Palm Springs, CA (2017 – 2021 / Present): Partner and Director of research and development, sales engineering, project management, product and vendor sourcing, and contractor management. Runs air conditioning engineering: building envelope, heat load and heat loss, air flow and BTU sizing, and hydraulic pressure-drop calculations; developing phase-change material thermal shelving.",
            "EWSolar.net LLC, Homeland, CA (2014 – 2016): Vice President, direct solar-fired variable frequency drive (VFD) well pumping projects at 30HP and above, with pumps sized from site peak sun hours and storage reservoirs sized to daily pumping volume.",
            "Free Energy Resources Inc., Phelan, CA (2013): Chief Technology Officer of a Korean solar marketing company; sales, procurement, project management, permitting, and finance.",
            "GRIDNOT Inc., Lucerne Valley, CA (2007 – 2012): Vice President, sales and integration of solar, wind, and geothermal air-conditioning systems.",
            "OnPoint Power Inc., Norco, CA (2006): Partner, residential and light-commercial solar; pioneered a waste-to-energy proposal to city council.",
            "Desert Power Inc., Palm Springs, CA (2005): Executive Assistant, solar, waste-to-energy, and tri-generation support; Fischer-Tropsch syngas research.",
            "Solatron Inc., Victorville, CA (2004): Sales Representative; built an office-wide Excel solar sales calculator.",
        ]))
    story.extend(job_block(
        "Founder — Land Technology",
        "Tierrachain.com, 2023 – Present",
        [
            "Founder of a Mexican land corporation building software as a service (SaaS) that uses AI and blockchain to improve real estate exchange in coastal exclusion zones.",
            "Developing a parallel public records system with AI-automated compliance filing for arbitrage, plus fintech extensions using NFTitle and Bitso payment rails on a real estate mapping site.",
        ]))
    story.extend(job_block(
        "Elected Board President",
        "Mariana Ranchos County Water Board, 2006 – 2010",
        [
            "California public officer and elected board president, the youngest in the district's history; versed in public ethics, Roberts Rules of Order, the Brown Act, and state and federal agency law. California JPIA delegate with public accounting, insurance, and safety expertise.",
            "Cut operating expenditures 53% on a $16 million annual budget while protecting capital projects; replaced the General Manager, tightened purchasing and personnel policy, and kept a high-risk floodplain project out of the approval path before the basin later flooded.",
        ]))
    story.extend(job_block(
        "Open-Source Contributor — AI Code Evaluation and SDET Tooling",
        "ZeroClaw Labs, github.com/zeroclaw-labs/zeroclaw, 32.8k GitHub stars, 2026 – Present",
        [
            "PR #7946 (merged Jul 2026): built the context window meter across TUI, gateway, and CLI for 9 providers.",
            "PR #8966 (merged Sep 2026): carried live provider identity on usage events so usage, cost, and context-meter attribution follow the serving provider across fallback and model switches.",
        ]))

    story.extend(section("Education"))
    for e in ["Associate of Science, Mechanical Engineering, Victor Valley College",
              "California Notary Commission; Toastmasters International"]:
        story.append(P(e, edu_style, bullet="\u2022"))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
