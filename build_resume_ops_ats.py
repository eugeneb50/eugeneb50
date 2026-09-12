#!/usr/bin/env python3
"""Generate an ATS-friendly resume PDF for Eugene Lafayette Buchanan.

Deliberately graphics-free: single column, no images/charts/tables, standard
section headings, one font family (Helvetica base-14), "Month YYYY" dates,
acronyms spelled out on first use, plain-English copy (deslop skill).
Content source: /home/producer32/obsidian/resume/ressoft26.txt
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
    "IT support specialist with 25+ years helping users and keeping systems "
    "running, from help-desk and campus IT to QA leadership, freelance consulting, "
    "and software support tooling. I own Ticket Life Cycle Management end to end: intake, triage, resolution, "
    "and follow-up. I also handle User Life Cycle Management and Document Life "
    "Cycle Management, including onboarding and offboarding, access provisioning, "
    "and the knowledge base guides teams use. As a test automation lead I hired "
    "and trained QA staff, built regression suites with health dashboards, and "
    "helped develop an AI helpdesk chatbot. I explain fixes in plain language, "
    "escalate cleanly, and build small automations that keep queues short."
)

SKILLS = [
    "<b>Ticket and Queue Support:</b> Ticket Life Cycle Management, triage, escalation, status updates, follow-up, backlog grooming, Jira, Confluence, Slack",
    "<b>User Lifecycle and Access:</b> User Life Cycle Management, Access Provisioning, onboarding and offboarding, Okta single sign-on, Role-Based Access Control (RBAC), SAML, OAuth, account merging",
    "<b>Documentation and Records:</b> Document Life Cycle Management, Knowledge Base authoring, Standard Operating Procedure (SOP) guides, technical writing, IT asset tracking",
    "<b>Desktop and Systems Support:</b> Windows, Linux, virtualized desktops, WAN/LAN, SFTP, servers, PCs, audio/video equipment",
    "<b>Business Systems Support:</b> ERP, CRM, learning management systems (LMS), office automation, SAP, Oracle, Workday, Zoom integrations",
    "<b>Testing and Release Support:</b> QA leadership, test automation, regression suites, health dashboards, alerting, white-box testing, accessibility testing, Cypress, Selenium, Postman, JUnit, Qase, SQL, Git, Bitbucket, SOC 2 compliance",
    "<b>Support Automation:</b> AI helpdesk chatbot, retrieval-augmented generation (RAG), guardrails, prompt engineering, small workflow automations",
    "<b>Customer Communication:</b> plain-language explanations, training, mentoring, cross-functional collaboration, presales support",
]

FOREmost_BULLETS = [
    "Provided campus IT support: wrote security and backup policies for campus servers and personal computers (PCs), upgraded video surveillance for better quality and remote access, and installed campus-wide wireless.",
    "Evaluated and migrated accounting and medical-records software for the care campus.",
    "Built the nonprofit and community outreach program, developed and filed federal, state, and city applications, and ran a community social program.",
]


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Resume_Ops_ATS.pdf")

    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=48, bottomMargin=48,
        title="Eugene Lafayette Buchanan — IT Support Specialist Resume",
        author="Eugene Lafayette Buchanan",
        subject="IT Support Specialist — Ticket, User and Document Lifecycle Support (Apple Valley, CA)",
        keywords="IT Support Specialist, help desk, Ticket Life Cycle Management, User Life Cycle Management, Document Life Cycle Management, access provisioning, Okta, RBAC, Knowledge Base, SOP, Jira, customer support, retail customer support, Geek Squad, upselling, onboarding, offboarding, IT asset tracking",
    )

    story = []
    story.append(P("Eugene Lafayette Buchanan", name_style))
    story.append(P("IT Support Specialist — Ticket, User and Document Lifecycle Support", title_style))
    story.append(P(
        "Apple Valley, CA, San Quintin, Baja California, MX | +1 (909) 545 5384 | "
        "+52 (616) 126 5089 | eugene@serviceofothers.org", contact_style))

    story.extend(section("Professional Summary"))
    story.append(P(SUMMARY))

    story.extend(section("Skills"))
    for s in SKILLS:
        story.append(P(s, skill_style))

    story.extend(section("Work Experience"))
    story.extend(job_block(
        "Support Tooling Contributor (Open-Source)",
        "ZeroClaw Labs, github.com/zeroclaw-labs/zeroclaw, 2026 – Present",
        [
            "Built lifecycle-state ctx monitoring and usage metering for queue visibility and cost logging, terminal state reporting for agentic multiplexer.",
        ]))
    story.extend(job_block(
        "Test Automation Lead / QA Lead — AI Helpdesk Support",
        "Knowledgecity LLC, Remote, Dec 2020 – Aug 2025",
        [
            "Led quality assurance for learning management integrations (SAP, Oracle, Workday, Coursera, UKG, Zoom), plus custom APIs, webhooks, SCORM, and LTI. Hired and trained the test automation team and built an end-to-end regression suite with health dashboards and alerting.",
            "Helped develop an AI helpdesk chatbot with retrieval-augmented generation (RAG) retrieval and guardrails that deflects repetitive tickets. Carried users through login, authentication (SAML, OAuth), data, and error-message issues until each ticket closed clean.",
            "Ran white-box testing across the continuous integration and delivery (CI/CD) pipeline (Apache, REST, SQL, AWS, React), covering frontend, backend, mobile, security, performance, API, database, usability, accessibility, and localization, and joined blue-team incident forensics. Researched and implemented SOC 2 controls.",
        ]))
    story.extend(job_block(
        "Consultant - IT Support",
        "Foremost Senior Care / Foremost Organization, Hesperia, CA, 2013 – 2016",
        FOREmost_BULLETS))
    story.extend(job_block(
        "Computer Service Technician — Geek Squad",
        "Best Buy, Victorville, CA, 2007",
        [
            "Staffed the retail service desk: greeted walk-in customers, logged repair tickets, triaged issues, tracked assets through check-in, repair, and pickup, and gave plain-language status updates through closure.",
            "Set up new PCs, transferred user data, and fixed virus, operating system, and hardware issues, while recommending service plans, accessories, and upgrades matched to each customer. Handled payments and refunds.",
        ]))
    story.extend(job_block(
        "IT Manager",
        "Lucerne Valley Unified School District, Lucerne Valley, CA, 2002",
        [
            "Maintained IT systems across four school campuses, including WAN/LAN, NetWare servers, virtualized desktops, and audio/video equipment.",
            "Met state attendance reporting requirements, running data extract, transform, and load (ETL) with database table locking and certification.",
        ]))
    story.extend(job_block(
        "Senior Software Engineer II — Software Development Engineer in Test (SDET)",
        "RealNetworks, Seattle, WA, 1999 – 2001",
        [
            "Ran quality assurance as a Software Development Engineer in Test (SDET) across Linux, Unix, Windows, and embedded systems for a streaming media platform.",
            "Served on an advanced research team covering appliances, mobile, stream servers, and cellular networks, including patent work on transport-friendly real-time control protocol (TFRCP).",
            "Provided global presales engineering for consumer devices and vice president sales support, with travel to Japan, Korea, and the United States. Trained new hires.",
        ]))
    story.extend(job_block(
        "Senior Software Test Engineer IV",
        "Microsoft, Redmond, WA, 1999",
        [
            "Built nightly build test script automation for Windows Media Server versions 4 and 5.",
        ]))
    story.extend(job_block(
        "Senior Test Engineer III",
        "IBM, Kirkland, WA, 1998",
        [
            "Tested high-availability servers, including Windows Hardware Quality Labs (WHQL) certification for cluster failover.",
        ]))
    story.extend(job_block(
        "Software Test Engineer II",
        "Microsoft, Redmond, WA, 1997",
        [
            "Verified original equipment manufacturer (OEM) setup, hardware, and drivers for Windows 98 and Windows NT.",
        ]))
    story.extend(job_block(
        "Technical Support Agent II — Helpdesk",
        "Keene Inc., Seattle, WA, 1996",
        [
            "Provided frontline and escalated helpdesk support ticketing for Windows 95 and Windows NT.",
        ]))

    story.extend(section("Education"))
    for e in ["Associate Degree, Victor Valley College",
              "California Notary Commission",
              "Toastmasters International"]:
        story.append(P(e, edu_style, bullet="\u2022"))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
