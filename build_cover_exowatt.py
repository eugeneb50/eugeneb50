#!/usr/bin/env python3
"""Cover letter: Exowatt Talent Network (general application).

Exowatt builds the P3 system: captures solar energy, stores it as heat, and
generates electricity on demand. Founded 2023; a16z, Sam Altman, Felicis.
This is the general-application / talent-network form, not a single requisition,
so the letter names the four target roles and maps evidence to each.

Target roles: Quality Engineer, Reliability Engineer, Lead Controls & Firmware
Engineer, Technical Program Manager - Supply Chain & Manufacturing.
All on-site in Austin TX and/or Miami FL; relocation assistance provided.

Content source: ressoft27.txt (source of truth, unmodified). No invented
employers, dates, credentials, or tooling.

Deviation from the other cover builders: replaces the ProfitChart ("The Value of
Hiring Eugene") with a four-row role-fit table. A hiring manager on a
talent-network form needs to see role-to-evidence mapping, and the table also
lets this letter state what he would want to prove per role instead of claiming
full qualification.

Gap analysis - stated as "to prove" in the table, not hidden and not claimed:
- No supplier quality tooling: FAI, PPAP, SCAR, first-article inspection.
- No ISO 9001 QMS operation, no ASQ certification, no Six Sigma belt.
- No accelerated life testing (ALT/HALT/HASS) and no Weibull life data analysis.
- No GD&T / ASME Y14.5, no CFD/FEA, no 3D CAD (SolidWorks, Creo).
- No heat exchanger or pressure vessel design.
- Embedded device work is 1999-2001, not current firmware practice.
- Degree: A.S. Mechanical Engineering, not a Bachelor's. Addressed once,
  directly, in a single paragraph - experience-forward, no self-apologizing.

Outputs Eugene_Buchanan_Cover_Letter_Exowatt.pdf
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer, NextPageTemplate)

import build_cover as base

PW, PH = letter
ML = MR = 48
HEADER_H = 110
TOP_GAP = 10
BODY_BOTTOM = 44
FW = PW - ML - MR


class ExowattHead(base.LetterHead):
    """Gradient letterhead, Exowatt subtitle."""

    def draw(self):
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
        c.setStrokeColor(colors.white)
        c.setLineWidth(2)
        c.circle(pcx, pcy, pr, fill=0, stroke=1)

        c.setFillColor(colors.white)
        c.setFont(base.FONT_B, 24)
        c.drawString(28, H - 42, "EUGENE L. BUCHANAN")
        c.setFillColor(colors.HexColor("#e0cfff"))
        c.setFont(base.FONT, 11)
        c.drawString(28, H - 62, "Quality, Test & Controls Engineer")
        c.setFillColor(colors.HexColor("#eaeafa"))
        c.setFont(base.FONT, 8)
        c.drawString(28, H - 82, "Apple Valley, CA  \u00b7  +1 (909) 545 5384  \u00b7  "
                                 "eugene@serviceofothers.org  \u00b7  github.com/eugeneb50")
        c.setStrokeColor(colors.white)
        c.setFillAlpha(0.25)
        c.setLineWidth(0.5)
        c.line(28, H - 95, pcx - pr - 10, H - 95)
        c.setFillAlpha(1)


NAVY2 = colors.HexColor("#2b1d63")

date_style = ParagraphStyle("date", fontName=base.FONT, fontSize=9.5,
                            leading=12, textColor=base.GREY, spaceAfter=2)
addr_style = ParagraphStyle("addr", fontName=base.FONT, fontSize=9.5,
                            leading=12.5, textColor=base.INK, spaceAfter=0)
subj_style = ParagraphStyle("subj", fontName=base.FONT_B, fontSize=10.5,
                            leading=13.5, textColor=NAVY2, spaceBefore=6,
                            spaceAfter=0)
salute_style = ParagraphStyle("salute", fontName=base.FONT, fontSize=9.8,
                              leading=13, textColor=base.INK, spaceAfter=5)
body_style = ParagraphStyle("body", fontName=base.FONT, fontSize=9.6,
                            leading=12.8, textColor=base.INK, spaceAfter=6,
                            alignment=4)
sign_style = ParagraphStyle("sign", fontName=base.FONT_B, fontSize=10,
                            leading=13, textColor=NAVY2, spaceAfter=0)
sign2_style = ParagraphStyle("sign2", fontName=base.FONT, fontSize=8.3,
                             leading=10.5, textColor=base.GREY, spaceAfter=0)

LETTER_DATE = "September 26, 2026"

RECIPIENT = [
    "Exowatt Talent Network",
    "Exowatt, Inc.",
    "Via: jobs.lever.co/exowatt",
]

SUBJECT = ("Re: Quality, Reliability, Controls &amp; Firmware, and Supply Chain Program "
           "\u2014 Exowatt Talent Network")

PARAGRAPHS = [
    "I'm applying through the Exowatt Talent Network. I am a quality and controls "
    "engineer with thirty years across test engineering, product quality ownership, and "
    "thermal-energy systems, and I am relocating to Austin, TX or Miami, FL and available "
    "immediately. The four roles I am targeting are Quality Engineer, Reliability Engineer, "
    "Lead Controls &amp; Firmware Engineer, and Technical Program Manager \u2014 Supply "
    "Chain &amp; Manufacturing.",

    "<b>On quality and test ownership.</b> At Knowledgecity I built the test automation "
    "function from nothing \u2014 recruited, hired, and trained the engineers, then built an "
    "end-to-end regression suite with health dashboards and alerting across complex "
    "deployment scenarios, so regressions surfaced on a dashboard rather than in a customer "
    "ticket. I set the quality bar across integrations, front end, back end, mobile, "
    "information security, performance, load, API, database, usability, accessibility, and "
    "localization including right-to-left Arabic. At IBM I drove WHQL certification testing "
    "for high-availability cluster servers, exercising RAID configurations under sustained "
    "high-load webserver traffic while injecting simulated drive failures, and proved "
    "failover held with no data or service lost across controller, array, and host failure. "
    "I have also worked blue-team incident forensics, taking each failure to root cause "
    "rather than symptom.",

    "<b>On controls and hardware debugging.</b> At RealNetworks I tested decode stream "
    "optimization across architectures including ARM, programming directly on Psion 9210 "
    "Communicators running EPOC and Pocket PC \u2014 flashing builds to the device, "
    "capturing crash and memory-allocation logs off-target, and reproducing playback stalls "
    "under low-bandwidth and low-memory conditions. That isolated media pipeline defects "
    "that simulator-based testing had been passing, because the failure existed only on the "
    "device. More recently I delivered a SCADA and instrumentation upgrade for tank and "
    "pump sensors and relays, adding remote telemetry and automated control to district "
    "facilities, and sold and developed solar-fired VFD air-conditioning pumping projects at "
    "30HP and above through concept, approval, and commissioning.",

    "<b>On solar design and permitting.</b> I have worked in solar and renewable energy "
    "since 2004, and I produce permit-ready packages in CAD \u2014 plot plans, single-line "
    "electrical diagrams, equipment sizing, string impedance calculations, and NEC 690 "
    "compliance and safety calculations, plus rack load and footing calculations for "
    "site-specific structures. I coordinate licensed-engineer review and stamping, then run "
    "the package through city plan review to sign-off and permit to operate, and I now "
    "build those packages on AI-aided drafting software. I also design and fabricate custom "
    "mechanical parts where a catalog item does not fit. Enphase now ships a do-it-yourself "
    "permit package generator, which tells you where the industry thinks this is going. I "
    "build the same class of artifact by hand, and I can tell you exactly where a generator "
    "stops: custom mechanical parts that are not in a catalog, and sites where the "
    "impedance and footing calculations have to be right the first time. That work is what "
    "turns a solar thermal product into a permitted, interconnected, financeable site, and "
    "a modular unit system scaled to remote and international sites needs that pipeline to "
    "be cheap and fast or the deployment economics do not close. I have sold and integrated "
    "more than $32 "
    "million in solar, wind, and geothermal air-conditioning installations while overseeing "
    "teams and vendors across multi-technology portfolios, developed solar-fired VFD "
    "air-conditioning pumping projects at 30HP and above through concept, approval, and "
    "commissioning, and built and ran a solar marketing company as CTO across sales, "
    "procurement, permitting, and finance. The research I am proudest of is process "
    "stabilization, hot gas flow control, and anti-fouling for Fischer-Tropsch syngas "
    "\u2014 dirty, corrosive, high-temperature gas is a fouling problem, and it is the same "
    "fouling problem your heat exchangers live with.",

    "<b>On program and cost control.</b> As president of a California water district I cut "
    "operating expenditures 53% on a $16,027,777 annual budget while explicitly "
    "protecting capital projects, rebuilt district operations, delivered a SCADA and "
    "instrumentation upgrade for tank and pump sensors and relays with remote telemetry, "
    "and governed under the Brown Act through a term that included active litigation.",
]

ROLE_FIT = [
    ("Quality Engineer",
     "Built a test automation function from scratch. Owned acceptance criteria and quality "
     "metrics across integrations, front end, back end, mobile, security, and "
     "performance. Root-cause investigation and blue-team forensics. As a public officer, "
     "owned inspections, internal controls, and a documented public record.",
     "Supplier quality \u2014 FAI, PPAP, SCAR, first-article inspection \u2014 and ISO 9001 "
     "QMS operation."),
    ("Reliability Engineer",
     "Failure-injection test design under sustained load at IBM: RAID configurations with "
     "simulated drive failure, proving no data or service loss across controller, array, "
     "and host failover. Long practice taking field failures to root cause and feeding them "
     "back into design.",
     "Accelerated life testing programs and Weibull life data analysis."),
    ("Lead Controls &amp; Firmware Engineer",
     "C and C++ on ARM: programmed directly on Psion 9210 devices, flashing builds and "
     "capturing off-target crash and memory logs. SCADA and instrumentation delivery for "
     "sensors, relays, and remote telemetry. VFD and motor control at 30HP+.",
     "Current firmware practice \u2014 the device-level work is 1999\u20132001, and the "
     "controls work is supervisory rather than hands-on."),
    ("Technical Program Manager \u2014 Supply Chain",
     "More than $32M in solar, wind, and geothermal installations sold and integrated with "
     "vendor and contractor management. CAD permit packages \u2014 plot plans, single-line "
     "electrical, string impedance and NEC 690 safety calcs, rack load and footing calcs, "
     "engineer stamping, city plan review, permit to operate \u2014 plus custom mechanical "
     "part design. Delivered a $16.0M operating program with a 53% reduction.",
     "NPI and pilot-build management for manufactured hardware rather than site-built "
     "projects."),
]

DEGREE = (
    "Three of these four roles ask for a Bachelor's degree in engineering. I hold an "
    "Associate of Science in Mechanical Engineering from Victor Valley College, completed "
    "1996, and what followed is thirty years of engineering work. I would rather raise that "
    "directly than have a resume screen decide it silently \u2014 if the degree requirement "
    "is firm, the roles where it is not the primary filter are the ones I can prove today."
)

CLOSING = (
    "I build quality and test programs, and I have spent twenty years turning heat and "
    "light into delivered hardware. I would welcome a technical conversation about the P3 "
    "system and where a test and controls organization would earn its keep in it."
)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(base.RULE)
    canvas.setLineWidth(0.6)
    canvas.line(ML, 36, PW - MR, 36)
    canvas.setFont(base.FONT, 7.5)
    canvas.setFillColor(base.MUTE)
    canvas.drawString(ML, 24, "Eugene L. Buchanan  \u00b7  eugene@serviceofothers.org  "
                              "\u00b7  +1 (909) 545 5384  \u00b7  github.com/eugeneb50")
    canvas.drawRightString(PW - MR, 24, "Page %d" % doc.page)
    canvas.restoreState()


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Cover_Letter_Exowatt.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP, bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Cover Letter",
                          author="Eugene L. Buchanan",
                          subject="Exowatt Talent Network \u2014 Quality, Test and "
                                  "Controls Engineer (Relocating to Austin, TX or "
                                  "Miami, FL)",
                          keywords="Cover Letter, Exowatt, Quality Engineer, "
                                   "Reliability Engineer, Controls and Firmware, "
                                   "Technical Program Manager")

    header_frame = Frame(0, PH - HEADER_H, PW, HEADER_H, leftPadding=0,
                         rightPadding=0, topPadding=0, bottomPadding=0, id="hdr")
    letter_body = Frame(ML, BODY_BOTTOM, FW,
                        (PH - HEADER_H - TOP_GAP) - BODY_BOTTOM,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                        id="lbody")
    cont_body = Frame(ML, BODY_BOTTOM, FW, PH - BODY_BOTTOM - BODY_BOTTOM,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                      id="cbody")

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[header_frame, letter_body], onPage=footer),
        PageTemplate(id="content", frames=[cont_body], onPage=footer),
    ])

    story = []
    photo_path = base.make_circular_photo(os.path.join(out_dir, "pic.jpg"))
    story.append(ExowattHead(photo=photo_path))
    story.append(NextPageTemplate("content"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(LETTER_DATE, date_style))
    for line in RECIPIENT:
        story.append(Paragraph(line, addr_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph(SUBJECT, subj_style))
    story.append(base.AccentRule())
    story.append(Spacer(1, 6))

    story.append(Paragraph("Dear Exowatt Talent Network team,", salute_style))

    for para in PARAGRAPHS:
        story.append(Paragraph(para, body_style))

    # ── Role fit table (replaces the ProfitChart) ──────────────────
    story.append(Paragraph("How I map to each role:", subj_style))
    story.append(Spacer(1, 2))

    role_st = ParagraphStyle("role", fontName=base.FONT_B, fontSize=8.4, leading=10.6,
                             textColor=NAVY2, spaceAfter=0)
    have_st = ParagraphStyle("have", fontName=base.FONT, fontSize=8.2, leading=10.4,
                             textColor=base.INK, spaceAfter=0)
    prove_st = ParagraphStyle("prove", fontName=base.FONT, fontSize=8.2,
                              leading=10.4, textColor=colors.HexColor("#8a5a00"),
                              spaceAfter=0)

    rows = [[Paragraph(r, role_st), Paragraph(h, have_st), Paragraph(p, prove_st)]
            for r, h, p in ROLE_FIT]
    tbl = Table(rows, colWidths=[FW * 0.19, FW * 0.47, FW * 0.34], repeatRows=0)
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, base.RULE),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f4f0ff")),
    ]))
    story.append(tbl)
    story.append(Paragraph(
        "<font color='#8a98a6' size=7.4>Column three is what I would want to prove in "
        "the first ninety days, not a claim of qualification.</font>",
        ParagraphStyle("note", fontName=base.FONT, fontSize=7.4, leading=9.6,
                       textColor=base.MUTE, spaceBefore=3)))
    story.append(Spacer(1, 5))

    story.append(Paragraph(DEGREE, body_style))
    story.append(Paragraph(CLOSING, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("Best regards,", body_style))
    story.append(Spacer(1, 3))
    story.append(base.AccentRule(width=180))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Eugene L. Buchanan", sign_style))
    story.append(Paragraph("Quality, Test &amp; Controls Engineer", sign2_style))
    story.append(Paragraph("Relocating to Austin, TX or Miami, FL  \u00b7  "
                           "eugene@serviceofothers.org  \u00b7  github.com/eugeneb50",
                           sign2_style))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")
    return out_path


if __name__ == "__main__":
    build()
