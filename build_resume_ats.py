#!/usr/bin/env python3
"""Generate an ATS-friendly resume PDF for Eugene L. Buchanan.

Design rules from the ATS best-practice playbook (see AGENTS.md / novoresume):
  * No headers/footers, no images, no charts, no graphics, no text boxes.
  * Single column, simple bulleted lists, standard section headings.
  * One font family (Helvetica base-14 — embedded in no subset, always parseable).
  * Consistent "Month YYYY" dates, plain job titles, acronyms spelled out on
    first use, keyword-rich plain-English copy.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, HRFlowable, KeepTogether)

PW, PH = letter                 # 612 x 792
ML = MR = 0.65 * inch
MT = 0.5 * inch
MB = 0.5 * inch
FW = PW - ML - MR

INK    = colors.HexColor("#1a1a1a")
MUTE   = colors.HexColor("#444444")
RULE   = colors.HexColor("#888888")
ACCENT = colors.HexColor("#222222")

# ----------------------------------------------------------------------------
# Styles — one family (Helvetica), body 10–12pt, left aligned.
# ----------------------------------------------------------------------------
name_style = ParagraphStyle(
    "Name", fontName="Helvetica-Bold", fontSize=17, leading=20,
    alignment=TA_CENTER, textColor=INK, spaceAfter=2)
title_style = ParagraphStyle(
    "Title", fontName="Helvetica-Bold", fontSize=11, leading=14,
    alignment=TA_CENTER, textColor=INK, spaceAfter=2)
contact_style = ParagraphStyle(
    "Contact", fontName="Helvetica", fontSize=9.5, leading=13,
    alignment=TA_CENTER, textColor=INK, spaceAfter=0)

h1_style = ParagraphStyle(
    "H1", fontName="Helvetica-Bold", fontSize=12, leading=15,
    alignment=TA_LEFT, textColor=INK, spaceBefore=9, spaceAfter=2)
job_style = ParagraphStyle(
    "Job", fontName="Helvetica-Bold", fontSize=10.5, leading=14,
    alignment=TA_LEFT, textColor=INK, spaceBefore=5, spaceAfter=0)
sub_style = ParagraphStyle(
    "Sub", fontName="Helvetica-Oblique", fontSize=9.5, leading=12.5,
    alignment=TA_LEFT, textColor=MUTE, spaceBefore=1, spaceAfter=1)
body_style = ParagraphStyle(
    "Body", fontName="Helvetica", fontSize=9.5, leading=12.5,
    alignment=TA_LEFT, textColor=INK, spaceAfter=0)
bullet_style = ParagraphStyle(
    "Bullet", fontName="Helvetica", fontSize=9.5, leading=12.2,
    alignment=TA_LEFT, textColor=INK, leftIndent=14, bulletIndent=3,
    spaceAfter=0.5)
skill_style = ParagraphStyle(
    "Skill", fontName="Helvetica", fontSize=9.5, leading=12.5,
    alignment=TA_LEFT, textColor=INK, spaceAfter=1)
edu_style = ParagraphStyle(
    "Edu", fontName="Helvetica", fontSize=9.5, leading=12.2,
    alignment=TA_LEFT, textColor=INK, leftIndent=14, bulletIndent=3,
    spaceAfter=0.5)


def P(text, style, bulletText=None):
    return Paragraph(text, style, bulletText=bulletText)

def bullet(text):
    return Paragraph(text, bullet_style, bulletText="\u2022")

def rule():
    return HRFlowable(width="100%", thickness=0.7, color=RULE, spaceBefore=1,
                      spaceAfter=3)

def section(title):
    return [P(title, h1_style), rule()]


# ----------------------------------------------------------------------------
# Content — general-employment rewrite (plain English, deslop'd)
# ----------------------------------------------------------------------------
NAME    = "Eugene Lafayette Buchanan"
TITLE   = "Senior Software Engineer &amp; Technical Consultant"
CONTACT = ("Apple Valley, CA &middot; San Quintin, Baja California, MX &nbsp;|&nbsp; "
           "+1 (909) 545 5384 &nbsp;|&nbsp; +52 (616) 126 5089 &nbsp;|&nbsp; "
           "eugene@serviceofothers.org")

SUMMARY = ("Senior software engineer with 25+ years building, shipping, implementing "
           "and supporting solutions. Expert quality assurance (QA), test automation "
           "integrations for ERP, education and streaming platforms. I also work as a "
           "renewable energy consultant and real estate professional, so I move "
           "easily between technical depth and business operations. I write clean "
           "code, build reliable test systems, and explain complex ideas clearly.")

SKILL_GROUPS = [
    ("Languages &amp; Frameworks",
     "JavaScript, TypeScript, Python, Rust, PHP, Node.js, React, SQL"),
    ("Testing &amp; QA",
     "Cypress, Selenium, Postman, JUnit, Qase, white-box testing, regression "
     "suites, performance and load testing, accessibility testing, security testing"),
    ("Cloud, CI/CD &amp; DevOps",
     "AWS (ECS, S3), CI/CD pipelines, Docker, Git, Bitbucket, Elasticsearch, "
     "Unix domain sockets, JSON-RPC"),
    ("Integrations &amp; Auth",
     "SAP, Oracle, Workday, Coursera, UKG, Zoom, SAML, OAuth, SFTP, REST APIs"),
    ("AI &amp; Automation",
     "AI automation, prompt engineering, large language model (LLM) integration, "
     "agentic AI, LangGraph, Model Context Protocol (MCP)"),
    ("Platforms &amp; Domains",
     "ERP, CRM, learning management systems (LMS), streaming media, enterprise "
     "software, alternative energy, real estate"),
    ("Leadership &amp; Communication",
     "Team building, mentoring, training, cross-functional collaboration, product "
     "ownership, backlog management, presales engineering, technical writing"),
]

EXPERIENCE_SWE = [
    ("Senior QA Engineer / Test Automation Lead / Product Owner \u2014 Integrations",
     "Knowledgecity LLC &middot; Remote &middot; Dec 2020 \u2013 Aug 2025",
     [
        "Led QA across integration, frontend, backend, mobile, security, "
        "performance, load, API, database, functionality, usability, "
        "accessibility, and localization testing. Reduced technical debt.",
        "Built and maintained a CI/CD quality pipeline with Cypress, Selenium, "
        "Postman, JUnit, Elasticsearch, and S3 on AWS.",
        "Hired and trained the test automation team. Built regression suites, "
        "health dashboards, and alert systems for complex deployments.",
        "Shipped integrations with SAP, Oracle, Workday, Coursera, UKG, and Zoom "
        "using SAML, OAuth, SFTP, and custom REST APIs.",
        "Managed dev and test teams, the product backlog, and design reviews as "
        "Integrations Product Owner.",
        "Applied AI prompt engineering and shipped chatbot support tooling to "
        "production.",
     ]),
    ("Senior Software Engineer II",
     "RealNetworks &middot; Seattle, WA &middot; 1999 \u2013 2001",
     [
        "Ran QA on an advanced research team covering consumer appliances, "
        "mobile platforms, stream servers, and cellular networks.",
        "Led global presales engineering for consumer devices and trained new hires.",
     ]),
    ("Earlier Software Test Engineering Roles",
     "Microsoft &middot; IBM &middot; Keene Inc.",
     [
        "Microsoft, Redmond, WA (1999): Senior Software Test Engineer IV, "
        "Windows Media Server; white-box testing and development.",
        "IBM, Kirkland, WA (1998): Senior Test Engineer III, high-availability "
        "servers.",
        "Microsoft, Redmond, WA (1997): Software Test Engineer II, Windows 98 "
        "and Windows NT.",
        "Keene Inc., Seattle, WA (1996): Technical Support Agent II, Windows 95 "
        "and Windows NT.",
     ]),
    ("IT Manager",
     "Lucerne Valley Unified School District &middot; Lucerne Valley, CA &middot; 2002",
     [
        "Maintained IT systems across four school campuses, including WAN/LAN, "
        "NetWare servers, virtualized desktops, and audio/video equipment.",
        "Met state attendance reporting requirements.",
     ]),
    ("Freelance IT Consultant",
     "Amp Computer &middot; Apple Valley, CA &middot; 2003 \u2013 2011",
     [
        "Sold and supported servers and PCs. Configured ERP and CRM systems, "
        "office automation, and custom solutions.",
     ]),
]

EXPERIENCE_OTHER = [
    ("Alternative Energy Consultant",
     "2004 \u2013 Present",
     [
        "PhaseSave.com, Palm Springs, CA (2017 \u2013 Present): Director of product "
        "development, sales engineering, project management, and sourcing. "
        "Expertise in solar power, air conditioning, phase-change materials, and "
        "cold chain logistics.",
        "EWSolar.net, Homeland, CA (2014 \u2013 2016): Vice President, large-scale "
        "solar-powered water pumping projects.",
        "Free Energy Resources Inc., Phelan, CA (2013): Chief Technology Officer, "
        "solar marketing; sales, procurement, and project management.",
        "GRIDNOT Inc., Lucerne Valley, CA (2007 \u2013 2012): Vice President, sales "
        "and integration of solar, wind, and geothermal air-conditioning systems.",
        "OnPoint Power Inc. (2006), Desert Power Inc. (2005), Solatron Inc. "
        "(2004): renewable energy sales and support.",
     ]),
    ("Business Consultant",
     "2013 \u2013 2016",
     [
        "Medico Investments LLC, Hesperia, CA: recovered a non-permitted "
        "photovoltaic installation and worked with the city for permission to "
        "operate using as-built engineering.",
        "Foremost Organization, Hesperia, CA: built a nonprofit and community "
        "outreach program; filed federal, state, and city applications, and ran "
        "a community social program.",
        "Provided campus IT support and security and backup policies; upgraded "
        "video surveillance and installed campus-wide wireless.",
        "Reviewed business plans and cut procurement, operations, and staffing "
        "costs. Won city approval for a bridge to landlocked land.",
     ]),
    ("Real Estate Professional &amp; Elected Board President",
     "1999 \u2013 Present",
     [
        "Tierrachain.com (2023 \u2013 Present): founder of a land technology company "
        "building software as a service (SaaS) that uses AI and blockchain to "
        "improve real estate exchange.",
        "Mariana Ranchos County Water Board (2006 \u2013 2010): elected board "
        "president; youngest in California history. Cut budget waste by 53%, "
        "replaced corrupt personnel, hired a strong general manager, and blocked "
        "a high-risk floodplain project that later flooded.",
     ]),
]

EXPERIENCE_OSS = [
    ("Open-Source Contributor \u2014 Agentic AI Infrastructure",
     "ZeroClaw Labs &middot; github.com/zeroclaw-labs/zeroclaw &middot; 32.2k GitHub stars &middot; 2026 \u2013 Present",
     [
        "Designed and shipped an observer that reports agent lifecycle states "
        "over JSON-RPC on Unix domain sockets. Resolved four rounds of review "
        "feedback, including bounded I/O to prevent hangs and env-driven "
        "discovery.",
        "Reviewed and contributed architecture feedback on a multi-user "
        "authentication feature: permission profiles, principal isolation, and a "
        "workspace multi-tenant axis.",
     ]),
]

EDUCATION = [
    "Associate Degree, Victor Valley College",
    "California Notary Commission",
    "Toastmasters International",
    "High School Diploma, Lucerne Valley High School",
]


# ----------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------
def build(path="Eugene_Buchanan_Resume_ATS.pdf"):
    doc = BaseDocTemplate(path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
                          title="Eugene Lafayette Buchanan \u2014 Resume",
                          author="Eugene Lafayette Buchanan")
    frame = Frame(ML, MB, FW, PH - MT - MB, id="body")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame])])

    story = []
    story.append(P(NAME, name_style))
    story.append(P(TITLE, title_style))
    story.append(P(CONTACT, contact_style))
    story.append(rule())

    # Professional Summary
    story.extend(section("Professional Summary"))
    story.append(P(SUMMARY, body_style))

    # Skills
    story.extend(section("Skills"))
    for label, items in SKILL_GROUPS:
        story.append(P(f"<b>{label}:</b> {items}", skill_style))

    # Work Experience — Software Engineering
    story.extend(section("Work Experience \u2014 Software Engineering"))
    for role, org, bullets in EXPERIENCE_SWE:
        block = [P(role, job_style), P(org, sub_style)]
        block += [bullet(b) for b in bullets]
        story.append(KeepTogether(block))

    # Work Experience — Other Professional Roles
    story.extend(section("Work Experience \u2014 Additional Professional Roles"))
    for role, org, bullets in EXPERIENCE_OTHER:
        block = [P(role, job_style), P(org, sub_style)]
        block += [bullet(b) for b in bullets]
        story.append(KeepTogether(block))

    # Open-Source Contributions
    story.extend(section("Open-Source Contributions"))
    for role, org, bullets in EXPERIENCE_OSS:
        block = [P(role, job_style), P(org, sub_style)]
        block += [bullet(b) for b in bullets]
        story.append(KeepTogether(block))

    # Education
    story.extend(section("Education"))
    for e in EDUCATION:
        story.append(P(e, edu_style, bulletText="\u2022"))

    doc.build(story)


if __name__ == "__main__":
    build()
