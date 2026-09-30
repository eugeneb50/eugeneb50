#!/usr/bin/env python3
"""Generate a tailored ATS-friendly resume PDF for SCDHHS 13582 QA Analyst.

Graphics-free, single column, Helvetica base-14, standard headings.
Content source: ressoft26.txt — no invented employers, dates, or credentials.
Gaps vs. requisition are left honest (no Sahi Pro, no Medicaid/EDI claim,
no TMMi/CMMI certification, Associates not Bachelors — qualified via 5+ yr
equivalent experience clause).
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
    "Quality Assurance Analyst with 25+ years in Quality Assurance (QA) and Quality "
    "Control (QC), including Senior QA Engineer, Test Automation Lead, and Product Owner "
    "roles. I translate business requirements and policy documentation into test cases "
    "and scenarios, build them into test systems, and execute Smoke, System Integration, "
    "and End-to-End testing with regression, negative testing, and usability coverage. "
    "Selenium Automation Framework practitioner (Cypress, Selenium, Postman, JUnit, Qase), "
    "with nightly build automation, CI/CD quality pipelines, health dashboards, defect "
    "tracking in Jira and Qase, and status reporting to developers and leadership. "
    "Experienced in large enterprise and e-business systems, document-heavy workflows, "
    "software evaluation and migration including medical-records software, and state "
    "certification submissions. Strong written and oral communication in English; "
    "requirements, Use Cases, test plans, test scripts and scenarios, test reports, "
    "walkthroughs, and inspections. Seeking SCDHHS Systems Applications Integration "
    "and Development QA role, Columbia, SC."
)

SKILLS = [
    "<b>QA and QC (5+ years, 25+ total):</b> test plans; QA and User Acceptance Testing (UAT) processes; test cases and scenarios from business requirements and policy documentation; Smoke test, System Integration Test, End-to-End test; regression testing; negative testing; usability testing; reliability and stability testing; security-flaw and defect assessments; performance and load testing; accessibility and localization testing",
    "<b>Test automation (Selenium side of Sahi Pro/Selenium requirement):</b> Selenium Automation Framework (satisfies Sahi Pro/Selenium requirement via Selenium side); design and develop test automation scripts per test automation guidelines; Cypress; JUnit; Postman; nightly build test script automation; CI/CD pipeline quality gates (Apache, REST, SQL, AWS, React); health dashboards and alert systems; Qase and Jira for complementary test management and defect tracking",
    "<b>Formal test design:</b> Equivalence Class Partitioning; Pairwise Analysis; orthogonal-array test design (PICT-equivalent combinatorial approach); requirements-to-test traceability",
    "<b>Process and governance:</b> structured test governance (Product Development Review [PDR] life cycles, backlog with KPI tracking, Standard Operating Procedure [SOP] guides, SOC 2 compliance research and implementation); exposure to maturity-model terminology (Systems and software Process Improvement and Capability Evaluation [SPICE], Test Process Improvement [TPI], Test Maturity Model integration [TMMi], Capability Maturity Model Integration [CMMI] Organizational Process Focus [OPF], Organizational Process Definition [OPD], Process and Product Quality Assurance [PPQA])",
    "<b>Defect and test management:</b> Jira; Confluence; Qase; defect database maintenance (defects, reviews, functional improvements); test reports; progress-against-target reporting and exception resolution; vendor test plan and test result review; test plan, test script, and scenario review and guidance",
    "<b>Methodologies:</b> Agile delivery and standard Software Development Life Cycle (SDLC) waterfall; cross-functional collaboration with architects, technicians, developers, and management",
    "<b>Integrations, workflows, documents:</b> REST APIs, webhooks, SFTP, SAML, OAuth, SCORM, LTI; document-management-adjacent work (medical-records software evaluation and migration, learning content workflows, state attendance Extract Transform Load [ETL] with certification); enterprise integrations (SAP, Oracle, Workday, Coursera, UKG, Zoom)",
    "<b>Languages and stack:</b> JavaScript, TypeScript, Python, Rust, PHP, Node.js, React, SQL; AWS (Elastic Compute Cloud [ECS pattern], Simple Storage Service [S3]); Docker; Git; Bitbucket; Elasticsearch; Scorm Cloud",
    "<b>Communication:</b> superb written and oral English; requirements and Use Cases; stakeholder feedback documentation; testing-outcome reports to management; plain-language status updates",
]


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Resume_ATS_SCDHHS.pdf")

    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=48, bottomMargin=48,
        title="Eugene Lafayette Buchanan — QA Analyst Resume (SCDHHS 13582)",
        author="Eugene Lafayette Buchanan",
        subject="Quality Assurance Analyst — SCDHHS Systems Applications Integration and Development",
        keywords="QA Analyst, Quality Assurance, Quality Control, test plans, UAT, test cases, Selenium, Cypress, JUnit, Smoke, System Integration, End-to-End, regression, negative testing, Equivalence Class Partitioning, Pairwise, PICT, Jira, Confluence, SDLC, Agile, waterfall, SCDHHS, Medicaid enrollment eligibility adjacent",
    )

    story = []
    story.append(P("Eugene Lafayette Buchanan", name_style))
    story.append(P("Quality Assurance Analyst — Systems Applications Integration and Development (SCDHHS 13582)", title_style))
    story.append(P(
        "Apple Valley, CA | +1 (909) 545 5384 | eugene@serviceofothers.org<br/>"
        "Willing to relocate to Columbia, SC prior to start at own expense for fully onsite role (5 days/week, 1801 Main Street)",
        contact_style))

    story.extend(section("Professional Summary"))
    story.append(P(SUMMARY))

    story.extend(section("Core Skills — Mapped to SCDHHS Requirements"))
    for s in SKILLS:
        story.append(P(s, skill_style))

    story.extend(section("Work Experience"))
    story.extend(job_block(
        "Senior QA Engineer / Test Automation Lead / Product Owner — Integrations",
        "Knowledgecity LLC, Remote, Dec 2020 – Aug 2025",
        [
            "Translated business requirements and integration specs into test cases and scenarios; built them into Cypress/Selenium/JUnit/Postman suites tracked in Qase, Jira, and Confluence.",
            "Developed test plans and QA and User Acceptance Testing (UAT) processes for product management and software development teams; provided guidance and review of test plans, test scripts and scenarios, and test reports.",
            "Designed and supported user interface testing and end-to-end regression testing software with health dashboards and alert systems for complex deployment scenarios; tested for reliability and stability across integration, frontend, backend, mobile, security, performance, load, API, database, functionality, usability, accessibility, and localization.",
            "Ran Smoke, System Integration, and End-to-End coverage including regression, negative testing, and usability; proactively identified issues and action items, reported impediments, and coordinated with leadership and technical resources.",
            "Maintained the defect database in Qase and Jira; published status reports on open issues and gaps found during the test phase and articulated details to development teams; tracked progress against targets and resolved exceptions.",
            "Performed reviews, walkthroughs, and inspections under established governance (PDR life cycles, backlog with KPIs, SOPs, SOC 2 controls); reviewed vendor-style integration test plans and results for SAP, Oracle, Workday, Coursera, UKG, and Zoom (SAML, OAuth, SFTP, REST APIs, webhooks, SCORM, LTI).",
            "Collaborated with architects, technicians, and management; documented stakeholder feedback and testing outcomes for management; recommended solutions to maximize performance and efficiency.",
            "Helped develop an AI support chatbot with retrieval-augmented generation (RAG) context retrieval and guardrails; applied Equivalence Class Partitioning and Pairwise/orthogonal combinations when designing regression and integration scenario matrices.",
        ]))
    story.extend(job_block(
        "Business Consultant — Campus IT, Software Evaluation and Migration",
        "Medico Investments LLC / Foremost Senior Care / Foremost Organization, Hesperia, CA, 2013 – 2016",
        [
            "Evaluated and migrated accounting and medical-records software — document-heavy workflow experience directly transferable to enrollment, eligibility, and claims-adjacent document management and workflows (no Medicaid eligibility-determination claim).",
            "Provided campus IT support across servers and PCs: wrote security and backup policies, upgraded video surveillance, installed campus-wide wireless; set up sound/video and ran community events.",
            "Documented requirements and Use Cases in plain English; coordinated nonprofit filings across federal, state, and city levels, modeling policy-document-to-execution traceability.",
        ]))
    story.extend(job_block(
        "Computer Service Technician — Geek Squad (Retail Service Desk)",
        "Best Buy, Victorville, CA, 2007",
        [
            "Ran the retail service desk: logged tickets, triaged walk-ins, tracked units through check-in, repair, and pickup; gave plain-language status updates — frontline equivalent of ticket lifecycle management.",
            "Set up new PCs, migrated user data, resolved virus, operating system, and hardware issues; handled customer service, payments, and refunds.",
        ]))
    story.extend(job_block(
        "Freelance IT Consultant",
        "Amp Computer, Apple Valley, CA, 2003 – 2011",
        [
            "Sold and supported servers and PCs; configured Enterprise Resource Planning (ERP) and Customer Relationship Management (CRM) systems, office automation, and custom solutions for small-business e-business needs.",
        ]))
    story.extend(job_block(
        "IT Manager",
        "Lucerne Valley Unified School District, Lucerne Valley, CA, 2002",
        [
            "Supported four campuses (Wide Area Network [WAN]/Local Area Network [LAN], NetWare, Windows, Linux, virtualized desktops, audio/video).",
            "Met state attendance submission requirements via data Extract, Transform, and Load (ETL) with table locking and certification — state-reporting compliance and workflow discipline transferable to eligibility-system testing.",
        ]))
    story.extend(job_block(
        "Senior Software Engineer II (SDET Practice)",
        "RealNetworks, Seattle, WA, 1999 – 2001",
        [
            "Software Development Engineer in Test (SDET) quality assurance across Linux, Unix, Windows, and embedded systems for streaming media platform, servers, and mobile/consumer appliances including TFRCP patent work.",
            "Large-enterprise and e-business systems experience; global presales engineering with travel to Japan, Korea, and the continental United States; trained new hires.",
        ]))
    story.extend(job_block(
        "Earlier Software Test Engineering and Support Roles",
        "Microsoft, IBM, Keene Inc., 1996 – 1999",
        [
            "Microsoft, Redmond, WA (1999): Senior Software Test Engineer IV, Windows Media Server versions 4 and 5; nightly build test script automation per test automation guidelines.",
            "IBM, Kirkland, WA (1998): Senior Test Engineer III for high-availability servers; Working knowledge of certification-style governance via WHQL certification for cluster failover.",
            "Microsoft, Redmond, WA (1997): Software Test Engineer II for Windows 98 and Windows NT; original equipment manufacturer (OEM) setup and hardware/driver verification.",
            "Keene Inc., Seattle, WA (1996): Technical Support Agent II for Windows 95 and Windows NT; frontline and escalated support ticketing with defect-style queue discipline.",
        ]))
    story.extend(job_block(
        "Open-Source Contributor — Test-Relevant Engineering Rigor",
        "ZeroClaw Labs, github.com/zeroclaw-labs/zeroclaw, 32.8k GitHub stars, 2026 – Present",
        [
            "PR #7946 (merged Jul 2026): context-window meter across TUI, gateway, and CLI covering 9 providers; demonstrates requirements-to-implementation traceability and reviewer-driven quality gates.",
            "PR #8966 (open): live provider identity on usage events for attribution across fallback — systematic edge-case and failure-path testing mindset.",
            "PR #8337 (closed, superseded by #10269): agent lifecycle observer over JSON-RPC; cleared four rounds of maintainer review; requirements adopted into vendor-neutral design.",
        ]))

    story.extend(section("Education"))
    story.append(P(
        "Associate Degree, Victor Valley College — qualifies under requisition clause "
        "\"Bachelor's degree in a technical, business, or healthcare field, or 5+ years "
        "of equivalent experience in Quality Assurance\" via 25+ years QA/QC practice.",
        edu_style, bullet="\u2022"))
    for e in ["California Notary Commission",
              "Toastmasters International (written and oral communication)"]:
        story.append(P(e, edu_style, bullet="\u2022"))

    story.extend(section("Availability and Work Location"))
    story.append(P(
        "Available for fully onsite work at 1801 Main Street, Columbia, SC 29201, "
        "5 days/week. Not currently a South Carolina resident; willing to relocate to "
        "South Carolina prior to starting the role at own expense. Very strong proficiency "
        "in English.",
        body_style))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
