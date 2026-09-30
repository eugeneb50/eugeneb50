#!/usr/bin/env python3
"""Generate a tailored resume PDF for Exowatt (talent network / multi-role).

Exowatt builds the P3 system: captures solar energy, stores it as heat, and
generates electricity on demand. Founded 2023; a16z, Sam Altman, Felicis.
Roles targeted (Austin TX and/or Miami FL, on-site, relocation required):
Quality Engineer, Reliability Engineer, Lead Controls & Firmware Engineer,
Technical Program Manager - Supply Chain & Manufacturing.

Content source: ressoft27.txt (source of truth, unmodified). No invented
employers, dates, credentials, or tooling.

Positioning decision: this resume REORDERS rather than rewords. Energy and
test/quality engineering lead; the software and AI work compresses into a
short Selected Technical Work block. The A.S. is stated once, in Education.

Gap analysis vs. the four JDs - deliberately NOT claimed because they are not
in source (no fabrication):
- No GD&T / ASME Y14.5, no ISO 9001 QMS, no ASQ cert, no Six Sigma belt.
- No SPC, Cpk, MSA, DOE, Weibull, life data analysis, confidence bounds.
- No FMEA, FTA, RBD, FRACAS, RCM.
- No ALT, HALT, HASS life-test program ownership.
- No supplier quality tooling: FAI, PPAP, SCAR, first-article inspection.
- No metrology: CMM, optical comparator, calipers, micrometers.
- No CFD/FEA (ANSYS, Nastran), no 3D CAD (SolidWorks, Creo).
- No heat exchanger or pressure vessel design, no ASME BPVC / TEMA.
- No power electronics or MW-class power conversion design.
Root cause, failure analysis, test planning, quality metrics, cost reduction,
and quality-system building from zero ARE shown - those are real.

Gap vs. requisition, positive transferable framing only: the test-automation
leadership, device-level debugging, and high-availability hardware verification
map onto test-program ownership, inspection rigor, and field-failure analysis.

Direct, non-narrative, non-apologetic copy. No run-local trivia.
Outputs Eugene_Buchanan_Resume_Exowatt.pdf
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                HRFlowable, KeepTogether)

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"

OUT = "Eugene_Buchanan_Resume_Exowatt.pdf"

PW, PH = letter
ML = MR = 46
TOP = 32
BOT = 32
FW = PW - ML - MR

name_style = ParagraphStyle("name", fontName=FONT_B, fontSize=16.5, leading=19,
                            alignment=TA_LEFT, spaceAfter=1)
title_style = ParagraphStyle("title", fontName=FONT, fontSize=10, leading=12.5,
                             alignment=TA_LEFT, spaceAfter=1)
contact_style = ParagraphStyle("contact", fontName=FONT, fontSize=8.5,
                               leading=10.5, alignment=TA_LEFT, spaceAfter=1)
target_style = ParagraphStyle("target", fontName=FONT_B, fontSize=8.5,
                              leading=10.5, alignment=TA_LEFT, spaceAfter=1)
h2_style = ParagraphStyle("h2", fontName=FONT_B, fontSize=10.5, leading=12,
                          alignment=TA_LEFT, spaceBefore=3, spaceAfter=1.5)
job_style = ParagraphStyle("job", fontName=FONT_B, fontSize=9.5, leading=11,
                           alignment=TA_LEFT, spaceBefore=1.5, spaceAfter=0)
meta_style = ParagraphStyle("meta", fontName=FONT, fontSize=8.5, leading=10.5,
                            alignment=TA_LEFT, spaceAfter=1)
body_style = ParagraphStyle("body", fontName=FONT, fontSize=8.9, leading=10.8,
                            alignment=TA_LEFT, spaceAfter=2)
bullet_style = ParagraphStyle("bullet", fontName=FONT, fontSize=8.9,
                              leading=10.1, alignment=TA_LEFT, leftIndent=14,
                              bulletIndent=5, spaceAfter=0)
cluster_style = ParagraphStyle("cluster", fontName=FONT, fontSize=8.6,
                               leading=10.6, alignment=TA_LEFT, leftIndent=10,
                               bulletIndent=0, spaceAfter=1)
edu_style = ParagraphStyle("edu", fontName=FONT, fontSize=8.9, leading=10.6,
                           alignment=TA_LEFT, leftIndent=14, bulletIndent=5,
                           spaceAfter=0)


def P(text, style=body_style, bullet=None):
    return Paragraph(text, style, bulletText=bullet)


def section(title):
    return [P(title, h2_style),
            HRFlowable(width="100%", thickness=0.6, spaceAfter=2)]


def job_block(role, meta, bullets):
    out = [P(role, job_style), P(meta, meta_style)]
    for b in bullets:
        out.append(P(b, bullet_style, bullet="\u2022"))
    return out


def cluster(label, terms):
    return P("<b>%s</b> \u2014 %s" % (label, terms), cluster_style)


HEADER = [
    P("EUGENE L. BUCHANAN", name_style),
    P("Quality, Test &amp; Controls Engineer \u2014 Solar Thermal, Waste-to-Energy "
      "&amp; Embedded Systems", title_style),
    P("Apple Valley, CA | +1 (909) 545-5384 | eugene@serviceofothers.org | "
      "github.com/eugeneb50", contact_style),
    P("San Quint\u00edn, BC, MX | +52 (616) 126 5089 | "
      "Relocating to Austin, TX or Miami, FL \u00b7 Available immediately",
      contact_style),
    P("<b>Target roles:</b> Quality Engineer \u00b7 Reliability Engineer \u00b7 "
      "Lead Controls &amp; Firmware Engineer \u00b7 Technical Program Manager, "
      "Supply Chain &amp; Manufacturing", target_style),
    Spacer(1, 4),
]

SUMMARY = (
    "Quality and controls engineer with 30 years across test engineering, product "
    "quality ownership, and thermal-energy systems. Twenty-two years in solar and "
    "renewable energy, where I produce permit-ready CAD packages \u2014 plot plans, "
    "single-line electrical diagrams, string impedance calculations, and NEC 690 "
    "compliance and safety calculations \u2014 coordinate engineer stamping, and run them "
    "through city plan review to permit to operate, and design custom mechanical parts "
    "where a catalog item does not fit. Sold "
    "and integrated more than $32M in solar, wind, and geothermal air-conditioning "
    "installations. Process research on Fischer-Tropsch syngas stabilization, hot gas flow "
    "control, and anti-fouling. Ten years of test ownership spanning embedded device "
    "hardware, high-availability server hardware, and production software \u2014 from "
    "device-level debugging on ARM/EPOC through WHQL certification testing of RAID clusters "
    "under sustained high-load traffic. Built a test automation function from nothing and "
    "drove a 53% reduction in operating expenditures on a $16,027,777 annual public-agency "
    "budget. A.S. Mechanical Engineering, 1996."
)

CLUSTERS = [
    cluster("Quality &amp; Test Engineering",
            "quality management \u00b7 quality standards \u00b7 quality assurance \u00b7 "
            "test planning \u00b7 test cases \u00b7 inspection \u00b7 calibration \u00b7 "
            "root cause analysis \u00b7 5-Why \u00b7 defect triage \u00b7 white-box "
            "testing \u00b7 end-to-end regression \u00b7 load and performance testing \u00b7 "
            "security and usability testing \u00b7 quality metrics \u00b7 technical "
            "documentation \u00b7 blue-team incident forensics"),
    cluster("Embedded &amp; Controls",
            "C \u00b7 C++ \u00b7 ARM \u00b7 embedded Linux \u00b7 device flashing \u00b7 "
            "off-target crash and memory-log capture \u00b7 on-device debugging \u00b7 "
            "SCADA \u00b7 instrumentation \u00b7 sensors and relays \u00b7 VFD and motor "
            "control"),
    cluster("Solar Design &amp; Permitting",
            "photovoltaic and solar thermal system design \u00b7 off-grid and on-grid systems "
            "\u00b7 CAD plot plans \u00b7 single-line electrical diagrams \u00b7 equipment "
            "sizing \u00b7 string impedance calculations \u00b7 NEC 690 compliance and "
            "safety calculations \u00b7 rack load calculations \u00b7 footing calculations "
            "\u00b7 licensed-engineer stamping coordination \u00b7 electrical permit packages "
            "\u00b7 city plan review \u00b7 permit to operate \u00b7 interconnection and "
            "utility coordination \u00b7 custom mechanical engineered parts \u00b7 contract "
            "administration \u00b7 EPC documentation \u00b7 AI-aided drafting \u00b7 "
            "technical sales engineering"),
    cluster("Energy &amp; Thermal",
            "air conditioning estimation \u00b7 air flow and BTU calculations \u00b7 "
            "building envelope analysis \u00b7 seasonal thermal load calculations \u00b7 "
            "passive solar design \u00b7 solar azimuth and inclination \u00b7 site shading "
            "analysis \u00b7 solar thermal \u00b7 phase-change materials \u00b7 thermal "
            "energy storage \u00b7 heat pumps \u00b7 absorption and evaporative cooling "
            "\u00b7 waste-to-energy \u00b7 Fischer-Tropsch synthesis \u00b7 syngas "
            "conditioning \u00b7 hot gas flow control \u00b7 anti-fouling \u00b7 heat "
            "transfer \u00b7 VFD and motor control \u00b7 SCADA and instrumentation "
            "\u00b7 commissioning"),

    cluster("Program, Operations &amp; Governance",
            "program and project management \u00b7 project delivery \u00b7 pilot builds "
            "and deployment \u00b7 procurement \u00b7 vendor and contractor management "
            "\u00b7 cost reduction \u00b7 budget management \u00b7 KPIs \u00b7 "
            "cross-functional teams \u00b7 operations management \u00b7 continuous "
            "improvement \u00b7 client relationships \u00b7 regulatory compliance "
            "\u00b7 inspections \u00b7 policy development \u00b7 internal controls "
            "\u00b7 audits \u00b7 risk management \u00b7 litigation \u00b7 open-meetings "
            "law \u00b7 technical communication"),
]

EXPERIENCE = [
    ("PHASESAVE.COM \u2014 PARTNER / DIRECTOR, RESEARCH & DEVELOPMENT", "Palm Springs, "
     "CA \u00b7 2017 \u2013 2021, Present", [
         "Produces permit-ready solar packages in CAD: plot plans, single-line electrical "
         "diagrams, equipment sizing, string impedance calculations, and NEC 690 "
         "compliance and safety calculations. Coordinates licensed-engineer review and "
         "stamping, then runs the package through city plan review to sign-off and permit "
         "to operate. Recovered a non-permitted photovoltaic installation by working the "
         "City on a permit-to-operate backed by as-built engineering, bringing an "
         "unapproved system into compliance and back online.",
         "Designs and fabricates custom mechanical engineered parts where a catalog item "
         "does not fit \u2014 racking and mounting hardware and site-specific assemblies "
         "\u2014 and produces permit packages on AI-aided drafting software.",
         "Estimates and sizes cooling loads for air conditioning work \u2014 air flow and "
         "BTU calculations, building envelope analysis, and seasonal thermal load "
         "calculation for desert and data center applications \u2014 and develops "
         "waterless phase-change material thermal shelving for those cooling loads.",
         "Directs R&amp;D and consulting delivery across sales engineering, project "
         "management, vendor sourcing, and contractor management, with depth in solar "
         "power, air conditioning, phase-change materials, cold-chain logistics, and tax "
         "credits. Brought Monobloc air-to-water heat pumps into California as sales and "
         "engineering representative.",
     ]),
    ("KNOWLEDGECITY LLC \u2014 PRODUCT OWNER, INTEGRATIONS", "Senior Quality "
     "Assurance Engineer \u2192 Test Automation Lead (years 2\u20134) \u2192 Product "
     "Owner \u00b7 December 2020 \u2013 August 2025", [
         "Owned product quality for six enterprise integrations \u2014 SAP, Oracle, "
         "Workday, Coursera, UKG, and Zoom \u2014 over SAML, OAuth, SFTP, REST, custom "
         "APIs, and webhooks, with SCIM, SCORM, and LTI extending coverage across HRIS and "
         "learning platforms.",
         "Built the test automation function from nothing as Test Automation Lead: "
         "recruited, hired, and trained the engineers, then built an end-to-end regression "
         "suite with health dashboards and alerting across deployment scenarios.",
         "Owned white-box test development against a CI/CD pipeline on Apache, REST, SQL, "
         "and AWS behind a React front end \u2014 Cypress, Selenium, Postman, JUnit, Git, "
         "Node, Elastic, Qase, Jira.",
         "Set the quality bar across integrations, front end, back end, mobile, security, "
         "performance, load, API, database, usability, accessibility, and localization "
         "including right-to-left Arabic. Shipped an AI support assistant with "
         "retrieval-augmented generation and guardrails under SOC 2 controls. Worked "
         "blue-team incident forensics to root cause.",
     ]),
    ("EARLY RENEWABLE ENERGY COMPANIES \u2014 EWSOLAR.NET (VP), FREE ENERGY RESOURCES "
     "(CTO), GRIDNOT (VP), ONPOINT POWER (Partner), DESERT POWER, SOLATRON",
     "Lucerne Valley, Homeland, Phelan, Norco and Palm Springs, CA \u00b7 2004 \u2013 2016", [
         "GRIDNOT: oversaw teams and vendors for the sales and integration of solar, wind, "
         "and geothermal air-conditioning systems, and did the passive solar design work "
         "\u2014 solar azimuth and inclination selection and site shading analysis for each "
         "installation. Sold more than $32 million in installations.",
         "EWSOLAR: sold and developed large direct solar-fired VFD air-conditioning pumping "
         "projects at 30HP and above, from concept through customer approval and field "
         "deployment. Owned sales engineering and contractor management, site "
         "documentation, and commissioning.",
         "DESERT POWER: supported projects across PV solar, waste-to-energy, and "
         "tri-generation combined electricity, heat, and refrigeration. Researched "
         "Fischer-Tropsch syngas conversion to liquids \u2014 process stabilization, "
         "anti-fouling, hot gas flow control, and absorption refrigeration.",
         "ONPOINT POWER: sold and engineered residential and light-commercial "
         "photovoltaic and thermal solar. Pioneered a waste-to-energy proposal for the City "
         "of Norco in 2006, presenting at an agendized council meeting on converting horse "
         "manure at the wastewater plant into energy; Chevron subsequently built the "
         "facility. FREE ENERGY RESOURCES: built and ran a Korean solar marketing company "
         "as CTO over sales, procurement, permitting, and finance.",
     ]),

    ("MARIANA RANCHOS COUNTY WATER DISTRICT \u2014 PRESIDENT, BOARD OF DIRECTORS",
     "Apple Valley, CA \u00b7 2006 \u2013 2010 \u00b7 California special district", [
         "Delivered a SCADA and instrumentation upgrade for tank and pump sensors and "
         "relays, adding remote telemetry and automated control. Cut operating "
         "expenditures 53% on a $16,027,777 annual budget while explicitly protecting "
         "capital expenditure projects.",
         "Rebuilt district operations: replaced the General Manager, tightened purchasing "
         "and internal controls, and moved water testing and monitoring to trained staff. "
         "Governed under the Brown Act through a term including active litigation.",
     ]),
    ("AMP COMPUTER AND LUCERNE VALLEY UNIFIED SCHOOL DISTRICT \u2014 FREELANCE CONSULTANT "
     "AND IT MANAGER", "Apple Valley and Lucerne Valley, CA \u00b7 2002 \u2013 2011", [
         "Consulted and sold for eight years covering server and PC hardware, ERP, CRM, "
         "and office automation, then moved into web development with Django and "
         "WordPress, owning client relationships end to end.",
         "Provided district-wide IT infrastructure for four campuses across WAN and LAN, "
         "NetWare servers, and Windows, Linux, and virtualized desktops. Owned the extract, "
         "transform, and load path for state attendance reporting \u2014 data quality, "
         "database table locking, and certification testing against a fixed deadline.",
     ]),
    ("REALNETWORKS \u2014 SENIOR SOFTWARE ENGINEER II, STREAMING MEDIA PLATFORM",
     "Seattle, WA \u00b7 1999 \u2013 2001", [
         "Tested decode stream optimization across architectures including ARM, "
         "programming directly on Psion 9210 Communicators running EPOC and Pocket PC "
         "\u2014 flashing builds to the device, capturing crash and memory-allocation logs "
         "off-target, and reproducing playback stalls under low-bandwidth and low-memory "
         "conditions. That isolated media pipeline defects simulator-based testing had been "
         "passing, because the failure existed only on the device.",
         "Started on front-end SDET, then joined the advanced research team covering "
         "servers, embedded, Linux, and Unix back-end testing. Delivered presales "
         "engineering for the embedded Linux consumer electronics stack internationally "
         "with the VP of Sales.",
     ]),
    ("MICROSOFT AND KEENE INC. \u2014 SOFTWARE TEST ENGINEER AND TECHNICAL SUPPORT",
     "Redmond, WA and Seattle, WA \u00b7 1996 \u2013 1999", [
         "Automated nightly build test scripts and verification for Windows Media Server 4 "
         "and 5, the streaming media product line and a direct lead-in to RealNetworks. "
         "Verified OEM setup across hardware and driver combinations for Windows 98 and NT.",
     ]),
    ("IBM \u2014 SENIOR TEST ENGINEER III, HIGH AVAILABILITY SERVERS", "Kirkland, WA \u00b7 1998", [
         "Drove WHQL certification testing for high-availability cluster servers by "
         "exercising RAID configurations under sustained high-load webserver traffic while "
         "injecting simulated drive failures \u2014 proving failover held under real "
         "production load, with no data or service lost across controller, array, and host "
         "failure. Designed the failure-injection and load harness it ran on.",
     ]),
]

INDEPENDENT = ("INDEPENDENT SOFTWARE ENGINEER \u2014 FREELANCE",
               "September 2025 \u2013 Present", [
                   "Web and AI development across a portfolio of client projects, each "
                   "taken from scoping through build, deployment, and support: a business "
                   "system for a lapidary shop, real estate operations in Nevada County, an "
                   "animal shelter project in San Quint\u00edn, and an AI literacy program. "
                   "Also bid and priced solar engineering work through PhaseSave.",
               ])

SELECTED_WORK = [
    "herdr-mcp (github.com/eugeneb50/herdr-mcp) \u2014 author. 51-tool Rust Model Context "
    "Protocol server with an Axum HTTP bridge and React playground, recipe engine, cron "
    "scheduler, and agent lifecycle observability.",
]


def build():
    doc = SimpleDocTemplate(OUT, pagesize=letter,
                            leftMargin=ML, rightMargin=MR,
                            topMargin=TOP, bottomMargin=BOT,
                            title="Eugene L. Buchanan - Resume - Exowatt",
                            author="Eugene L. Buchanan",
                            subject="Quality, Test and Controls Engineer")

    story = []
    story += HEADER
    story += section("SUMMARY")
    story.append(P(SUMMARY, body_style))
    story += section("CORE COMPETENCIES")
    story += CLUSTERS
    story += section("EXPERIENCE")
    story += job_block(*INDEPENDENT)
    for role, meta, bullets in EXPERIENCE:
        story += job_block(role, meta, bullets)
    story += section("SELECTED TECHNICAL WORK")
    for b in SELECTED_WORK:
        story.append(P(b, bullet_style, bullet="\u2022"))
    story += section("EDUCATION &amp; CREDENTIALS")
    story.append(P("Associate of Science, <b>Mechanical Engineering</b> \u2014 Victor "
                   "Valley College, 1994 \u2013 1996", edu_style, bullet="\u2022"))
    story.append(P("WHQL certification testing, high-availability cluster servers \u2014 "
                   "IBM, 1998", edu_style, bullet="\u2022"))
    story.append(P("California Notary Public \u2014 commissioned \u00b7 Bilingual "
                   "English and Spanish, with right-to-left Arabic localization work on "
                   "production software", edu_style, bullet="\u2022"))


    doc.build(story, onFirstPage=_page, onLaterPages=_page)
    return OUT


def _page(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 7)
    canvas.setFillGray(0.45)
    canvas.drawString(ML, 26, "Eugene L. Buchanan  \u00b7  Exowatt Talent Network  "
                              "\u00b7  eugene@serviceofothers.org")
    canvas.drawRightString(PW - MR, 26, "Page %d" % doc.page)
    canvas.setStrokeGray(0.8)
    canvas.setLineWidth(0.5)
    canvas.line(ML, 34, PW - MR, 34)
    canvas.restoreState()


if __name__ == "__main__":
    print("wrote", build())
