#!/usr/bin/env python3
"""Vision letter: Exowatt — thermal platform extension to waste-to-heat + biochar.

Third document in the Exowatt set, alongside build_resume_exowatt.py and
build_cover_exowatt.py. This one is a technical strategy proposal, not an
application letter: it shows a specific, buildable integration of three real
systems and argues why a second market is strategic rather than a diversion.

The three systems (all independently published; figures cited as published):
  1. Exowatt P3 — proprietary fresnel lenses + heat exchangers for solar capture,
     a heat battery for storage, a proprietary heat engine for on-demand
     dispatch. Up to 24 h dispatchable, factory-built, 30-year service life,
     deployable with or without interconnection, domestically manufactured
     without rare earth minerals. Industries served: utility, data center.
  2. GEMCO Energy mobile waste gasification station, models HG-60 and HG-120
     (Anyang, Henan, China). Updraft rotating-bed gasifier; 2x or 4x 30 kW
     Stirling engines; waste heat boiler to hot water or steam; desulfurization
     and pulse dust collection; secondary combustion held 950-1100 C with
     >2 s flue-gas residence for dioxin and NOx decomposition; emissions stated
     to meet EU 2010 limits. HG-120: 120 kW electrical, 100 kW net electrical,
     252 kW thermal, 180 kg/h feedstock, 36 kg/h ash, 2x40 ft containers, 30 t.
     Feedstock 3-5 cm, moisture <=25%. Stainless steel and nickel alloys,
     15-20 year life, slight negative pressure, interlocking controls. Optional
     modules: seawater desalination, mobile energy storage, gas purification.
     Units can be run in parallel. Ash stated usable as construction material.

POSITIONING: the letter sells the CANDIDATE as the enabler as much as the idea.
A "C-class" operator - the person who crosses functions, closes the jurisdiction,
and moves the money - rather than a specialist. The role inventory and the capital
stack sections exist to make that claim checkable rather than asserted. Every row
is drawn from the author's own record; nothing is claimed that is not in source.

ARCHITECTURE (as directed): this is a SHARED THERMAL BUS, not a replacement of
GEMCO's power train. Two independent heat sources charge one heat battery, and
that storage feeds one shared Stirling generator stack:
  - Heat input A (solar): P3 fresnel lens collectors and heat exchangers.
  - Heat input B (waste, solar-independent): GEMCO gasifier, 950-1100 C
    secondary combustion, 252 kW thermal on HG-120.
  - Common heat transport bus to all downstream users.
  - Shared heat battery buffers both sources and decouples source intermittency
    from generation.
  - Shared Stirling gensets (2x or 4x 30 kW) on the bus, external combustion.
  - Useful-heat tap: hot water, steam, laundry, process load.
  - Solid outputs: biochar (STPC) and residual ash (36 kg/h, HG-120).
Why Stirling is the right machine on a poly-source bus: external combustion
means the working fluid and seals never contact syngas, and Stirlings tolerate
cyclic heat input, which is exactly what buffering two sources of different
duty cycles demands. Converting the solar-only system to a poly-fuel bus is what
attacks P3's actual problem - intermittency - using a fuel stream somebody else
wants removed.
Contamination caveat stated in the letter, not hidden: routing syngas into a
30-year-life solar asset couples a clean system to a dirty source. Mitigation is
a separated secondary loop - particulate filtration and scrubbing upstream, a
gas-side heat exchanger, and a working fluid that never sees syngas. Ash and
char carryover must be excluded. This is where the author's Fischer-Tropsch
anti-fouling work becomes load-bearing rather than decorative.
  3. STPC — San Quintin Thermal Processing Cooperative, a nonprofit community
     cooperative in the Valle de San Quintin, Baja California, Mexico. Converts
     agricultural residue into biochar, distilled water, hot showers, and
     community laundry service, on a basalt thermal battery technology.
     Published reach: more than 5,000 seasonal agricultural workers.
     Aligned to SDG 6, 7, 11, 13. Pilot stage, community-operated.
     Contact: stpc@encuentralo.mx, +52 616 126 5089.

Author's role: provides the technical and permitting work and helps build the
market ethos. Claims in this letter are limited to: 22 years of solar and
renewable engineering including permit-ready CAD packages (plot plans,
single-line electrical, string impedance, NEC 690 compliance and safety calcs,
rack load and footing calcs) through licensed-engineer stamping, city plan
review, sign-off, and permit to operate; $32M+ in installations sold and
integrated; process stabilization, hot gas flow control, and anti-fouling
research on Fischer-Tropsch syngas; air conditioning estimation, air flow and
BTU calculation, envelope analysis, seasonal thermal load; custom mechanical
part design and fabrication; and water district SCADA and instrumentation
delivery. Author is not a licensed professional engineer and does not stamp
his own work.

Honest limits stated in the letter, not hidden: this is a different market from
AI data centers with different unit economics and financing; GEMCO is a Chinese
manufacturer and that collides with Exowatt's domestic-sourcing positioning;
agricultural residue frequently exceeds the 25% moisture gasifier spec; biochar
is carbon-sequestering rather than automatically carbon-negative; and some
jurisdictions classify gasifiers as incinerators for permitting purposes.

Outputs Eugene_Buchanan_Vision_Letter_Exowatt.pdf
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
BODY_BOTTOM = 38
FW = PW - ML - MR

NAVY2 = colors.HexColor("#2b1d63")
AMBER = colors.HexColor("#8a5a00")
MUTE = colors.HexColor("#8a98a6")


class VisionHead(base.LetterHead):
    """Gradient letterhead, vision-proposal subtitle."""

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
        c.drawString(28, H - 62, "Technical Proposal \u2014 Thermal Platform Extension")
        c.setFillColor(colors.HexColor("#eaeafa"))
        c.setFont(base.FONT, 8)
        c.drawString(28, H - 82, "Apple Valley, CA  \u00b7  +1 (909) 545 5384  \u00b7  "
                                 "eugene@serviceofothers.org  \u00b7  github.com/eugeneb50")
        c.setStrokeColor(colors.white)
        c.setFillAlpha(0.25)
        c.setLineWidth(0.5)
        c.line(28, H - 95, pcx - pr - 10, H - 95)
        c.setFillAlpha(1)


class ThermalBusDiagram(base.Flowable):
    """Combined topology: two heat sources, one bus, shared storage, shared Stirlings."""

    def __init__(self, width, height=242):
        base.Flowable.__init__(self)
        self.width = width
        self.height = height

    def _box(self, x, y, w, h, title, lines, fill, edge, tcol, lcol):
        c = self.canv
        c.setFillColor(fill)
        c.setStrokeColor(edge)
        c.setLineWidth(0.8)
        c.roundRect(x, y, w, h, 3, fill=1, stroke=1)
        c.setFillColor(tcol)
        c.setFont(base.FONT_B, 7.2)
        ty = y + h - 9
        c.drawString(x + 5, ty, title)
        c.setFillColor(lcol)
        c.setFont(base.FONT, 6.5)
        ty -= 9.5
        for ln in lines:
            if ln:
                for seg in _wrap(ln, c, base.FONT, 6.5, w - 10):
                    ty -= 7.4
                    c.drawString(x + 5, ty, seg)
                ty -= 1.6
            else:
                ty -= 4.5
        return ty

    def _harrow(self, x0, x1, y):
        """Horizontal connector, arrowhead at the x1 end."""
        c = self.canv
        c.setStrokeColor(colors.HexColor("#9aa6b4"))
        c.setLineWidth(1.1)
        c.line(x0, y, x1 - 4.5, y)
        c.setFillColor(base.PINK)
        c.setStrokeColor(base.PINK)
        p = c.beginPath()
        p.moveTo(x1, y)
        p.lineTo(x1 - 5.2, y + 3.2)
        p.lineTo(x1 - 5.2, y - 3.2)
        p.close()
        c.drawPath(p, fill=1, stroke=0)


    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        c.setFillColor(colors.HexColor("#faf9ff"))
        c.setStrokeColor(base.RULE)
        c.setLineWidth(0.6)
        c.roundRect(0, 0, W, H, 4, fill=1, stroke=1)

        c.setFillColor(base.GREY)
        c.setFont(base.FONT_B, 6.5)
        c.drawString(9, H - 12,
                     "COMBINED TOPOLOGY \u2014 ONE THERMAL BUS, TWO HEAT SOURCES")
        c.setStrokeColor(base.RULE)
        c.setLineWidth(0.5)
        c.line(9, H - 16, W - 9, H - 16)

        LX = colors.HexColor("#f4f0ff")
        MX = colors.HexColor("#eefaf7")
        RX = colors.HexColor("#fff6e8")
        TL = colors.HexColor("#d4c8f5")
        TE = colors.HexColor("#a8ded6")
        OE = colors.HexColor("#e8c88a")

        self._box(9, H - 92, 112, 70, "HEAT INPUT A \u2014 SOLAR",
                  ["P3 fresnel lens collectors",
                   "and heat exchangers.",
                   "Daylight-driven.",
                   "Source: Exowatt P3 (published)"],
                  LX, TL, NAVY2, base.INK)
        self._box(9, H - 172, 112, 70, "HEAT INPUT B \u2014 WASTE",
                  ["180 kg/h residue gasifier,",
                   "secondary combustion held",
                   "950\u20131100 \u00b0C. Sunlight-",
                   "independent. Source: GEMCO"],
                  LX, TL, NAVY2, base.INK)

        self._box(155, H - 176, 100, 154, "COMMON THERMAL BUS",
                  ["Single heat transport",
                   "system serving every",
                   "downstream user.",
                   "",
                   "SHARED HEAT BATTERY",
                   "buffers both sources;",
                   "decouples source duty",
                   "cycle from generation.",
                   "",
                   "Source: Exowatt P3",
                   "(published)"],
                  MX, TE, NAVY2, base.INK)

        self._box(289, H - 142, 100, 86, "SHARED STIRLING STACK",
                  ["2\u00d7 or 4\u00d7 30 kW gensets,",
                   "external combustion.",
                   "",
                   "Working fluid and seals",
                   "never contact syngas.",
                   "Tolerant of cyclic input \u2014",
                   "what a two-source bus",
                   "demands."],
                  RX, OE, NAVY2, base.INK)

        self._box(423, H - 100, W - 432, 58, "USEFUL HEAT",
                  ["252 kW thermal to a heat",
                   "boiler: hot water, steam,",
                   "laundry, process load."],
                  RX, OE, NAVY2, base.INK)
        self._box(423, H - 168, W - 432, 58, "SOLID PRODUCT",
                  ["Biochar \u2014 the STPC",
                   "cooperative's principal good.",
                   "Residual ash 36 kg/h."],
                  RX, OE, NAVY2, base.INK)

        self._harrow(121, 155, H - 57)
        self._harrow(121, 155, H - 137)
        self._harrow(255, 289, H - 99)
        self._harrow(389, 423, H - 71)
        self._harrow(389, 423, H - 139)

        c.setFillColor(colors.HexColor("#8a5a00"))
        c.setFont(base.FONT_B, 6.3)
        c.drawString(9, 26, "DESIGN REQUIREMENT \u2014 how it is built:")
        c.setFillColor(base.INK)
        c.setFont(base.FONT, 6.3)
        note = ("The syngas path stays in a separated secondary loop with filtration and "
                "scrubbing upstream, a dedicated gas-side heat exchanger, and a working "
                "fluid that never sees syngas. Separate the gas from the solar asset and a "
                "30-year-life heat battery can sit behind a dirty feedstream; share the "
                "loop and it cannot.")
        ty = 17
        for seg in _wrap(note, c, base.FONT, 6.3, W - 20):
            c.drawString(9, ty, seg)
            ty -= 8


def _wrap(text, canvas, font, size, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if canvas.stringWidth(t, font, size) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


date_style = ParagraphStyle("date", fontName=base.FONT, fontSize=9.5, leading=12,
                            textColor=base.GREY, spaceAfter=2)
addr_style = ParagraphStyle("addr", fontName=base.FONT, fontSize=9.5, leading=12.5,
                            textColor=base.INK, spaceAfter=0)
subj_style = ParagraphStyle("subj", fontName=base.FONT_B, fontSize=10.5,
                            leading=13.5, textColor=NAVY2, spaceBefore=6,
                            spaceAfter=0)
salute_style = ParagraphStyle("salute", fontName=base.FONT, fontSize=9.8,
                              leading=13, textColor=base.INK, spaceAfter=5)
body_style = ParagraphStyle("body", fontName=base.FONT, fontSize=8.9,
                            leading=11.6, textColor=base.INK, spaceAfter=4.5,
                            alignment=4)
h3_style = ParagraphStyle("h3", fontName=base.FONT_B, fontSize=9.4, leading=11.6,
                          textColor=NAVY2, spaceBefore=3, spaceAfter=2)
note_style = ParagraphStyle("note", fontName=base.FONT, fontSize=7.6, leading=9.8,
                            textColor=MUTE, spaceAfter=2)
sign_style = ParagraphStyle("sign", fontName=base.FONT_B, fontSize=9.6, leading=11.5,
                            textColor=NAVY2, spaceAfter=0)
sign2_style = ParagraphStyle("sign2", fontName=base.FONT, fontSize=7.8, leading=9.6,
                             textColor=base.GREY, spaceAfter=0)

LETTER_DATE = "September 26, 2026"

RECIPIENT = [
    "Exowatt \u2014 Founders, Engineering, and Commercial",
    "Miami, FL",
    "International deployment \u2014 community energy hubs in developing nations",
    "Attached: follow-up to Exowatt Talent Network application",
]

SUBJECT = ("Re: The P3 platform as a community energy hub \u2014 agricultural residue to "
           "biochar, heat, and power, built on one shared thermal bus")

OPEN = [
    "The P3 platform concentrates solar heat with proprietary fresnel lenses and heat "
    "exchangers, stores it in a heat battery, and dispatches it through your own heat "
    "engine on demand. That is a capture-store-dispatch architecture, and those three "
    "functions are also the three functions of a different product. There is a second "
    "market sitting on the hardware you have already built, and it runs on the same bus: "
    "a gasification unit charging your heat battery and feeding your Stirling stack, so the "
    "plant keeps dispatching when the sun is not out. I would like to work on it.",

    "I am not proposing that Exowatt change strategy. Data centers pay for the R&amp;D, "
    "the manufacturing scale, and the 30-year service life. I am proposing a second "
    "application where the feedstock is a liability somebody else wants removed and the "
    "heat value is consumed locally rather than exported to a grid. That is a deployment "
    "problem, not a technology development problem, and it is the part I can carry.",
]

# --- The three systems, side by side -----------------------------------
SYSTEM_HEAD = ["Function in the combined system", "Contributor",
               "Published figure relied on"]
SYSTEM_ROWS = [
    ("Heat input A \u2014 solar", "Exowatt P3",
     "Proprietary fresnel lens collectors and heat exchangers"),
    ("Heat input B \u2014 waste, sunlight-independent", "GEMCO HG-120",
     "180 kg/h feedstock; 3\u20135 cm at \u226425% moisture; 950\u20131100 \u00b0C "
     "secondary combustion"),
    ("Heat transport", "Combined \u2014 new", "One common bus to every downstream user"),
    ("Thermal storage", "Exowatt P3 \u2014 shared",
     "Heat battery; extended storage with low losses"),
    ("Power conversion", "GEMCO \u2014 shared stack",
     "2\u00d7 or 4\u00d7 30 kW external-combustion Stirling gensets"),
    ("Useful-heat tap", "GEMCO + STPC",
     "252 kW thermal (HG-120) to hot water, steam, laundry, distilled water"),
    ("Solid product", "STPC + GEMCO",
     "Biochar; 36 kg/h residual ash, stated usable as construction material"),
    ("Site output", "Combined",
     "Electricity, useful heat, and biochar, off-grid capable; 1\u20132 \u00d7 40 ft "
     "modular; 15\u201320 yr gasifier life"),
]

INTEGRATION = [
    "<b>One bus, two heat sources.</b> The gasification plant does not replace your power "
    "train \u2014 it feeds the same heat storage and the same Stirling generator stack "
    "your solar concentrators feed. Solar charges the battery by day; the gasifier charges "
    "it at night, in cloud, and in winter. Solar concentration is the cheaper, cleaner "
    "source and carries the base load, but it is the source you cannot schedule. A second, "
    "sunlight-independent source on the same bus turns an intermittent plant into a "
    "dispatchable one, running on a fuel stream that is a liability somebody is already "
    "paying to remove.",

    "<b>Stirling is the right machine on a bus like this, and I would keep it.</b> GEMCO's "
    "gensets are external-combustion, so the working fluid and the seals never contact "
    "syngas. Stirlings also tolerate cyclic heat input, which is exactly what buffering two "
    "sources with different duty cycles demands. A single prime mover sized for one source "
    "is a compromise; a shared stack fed from a buffered bus is not.",

    "<b>Feedstock arrives presorted and dried.</b> Sorted by material and moisture, and dried "
    "to the gasifier specification before it reaches the feed hopper. That is a "
    "specification, not a topic \u2014 it is how the unit is fed, and the rest of the "
    "system is designed on the assumption that it has already been met.",

    "<b>Keeping the gas path separate is what makes the shared bus work.</b> Syngas carries "
    "sulfur, tars, and particulates, and a 30-year-life solar asset should never meet them "
    "directly. So the design separates them: a dedicated gas-side heat exchanger, "
    "particulate filtration and scrubbing upstream, and a working fluid that never contacts "
    "syngas. At Desert Power I did process stabilization, hot gas flow control, and "
    "anti-fouling research for Fischer-Tropsch syngas \u2014 the same contamination problem "
    "in a different reactor. That experience is what makes this a solvable design problem "
    "instead of an open risk, and it is why the thermal margin on the solar side stays where "
    "your warranty put it.",
]

ROLE_HEAD = ["Function this project needs", "What I have actually done"]
ROLE_ROWS = [
    ("Thermal and energy engineering",
     "Twenty-two years in solar and waste-to-energy. More than $32M in solar, wind, and "
     "geothermal installations sold and integrated. Air conditioning estimation, air flow "
     "and BTU calculation, envelope analysis, seasonal thermal load."),
    ("Test and reliability programs",
     "Built a test automation function from scratch. WHQL certification testing of "
     "high-availability clusters under sustained load with injected drive failure. "
     "WHQL-quality evidence programs, 30 years of test ownership."),
    ("Permitting and entitlement",
     "Permit-ready CAD packages \u2014 plot plans, single-line electrical, string "
     "impedance, NEC 690 safety calcs, rack load and footing calcs \u2014 through "
     "licensed-engineer stamping, city plan review, sign-off, and permit to operate. "
     "Recovered a non-permitted PV installation into compliance."),
    ("Public governance and board process",
     "Four years as an elected California public-agency president. Brown Act and "
     "open-meetings compliance through active litigation; board handbook and policy "
     "revisions; hiring and replacing executive staff."),
    ("Capital and cost control",
     "Cut operating expenditures 53% on a $16,027,777 annual budget while protecting "
     "capital projects. Tax credit applications, grant and licence filings at Federal, "
     "State, and City level. Insurance and risk-coverage delegate."),
    ("Community and social enterprise",
     "Built a nonprofit and community outreach program from nothing, including the "
     "Federal, State, and City licensing needed to stand it up. Public speaking and "
     "community events in front of residents and staff."),
    ("International operations",
     "Chief Technology Officer of a Korean solar marketing company \u2014 sales, "
     "procurement, permitting, and finance across an international operation."),
    ("Software, telemetry, and data",
     "Author of a 51-tool Rust Model Context Protocol server, 299 tests passing. "
     "RAG assistant shipped under SOC 2 controls. Satellite prospecting pipeline using "
     "Sentinel-2 spectral screening, SRTM terrain analysis, and GIS field data."),
]

FUND_HEAD = ["Tranche", "Capital source", "What it funds", "My part"]
FUND_ROWS = [
    ("Stage 0\u20131", "Founder capital, CSR, or a feasibility grant",
     "Desktop study, feedstock survey, bench gasifier, first stakeholder sign-offs.",
     "Build the business case, mass and energy balance, and a funder-ready dossier."),
    ("Stage 2", "Impact and catalytic capital, diaspora and diaspora-adjacent "
     "investment, development finance, CSR partnerships",
     "One container-class pilot: gasifier on the same bus as the solar array, "
     "community heat, water and laundry load, LEO backhaul and WiFi node stations.",
     "Structure the deal, write the investor materials, run co-application, hold the "
     "permitting schedule."),
    ("Stage 3", "Carbon and biochar offtake, plus equipment debt",
     "Replication of the hub into additional communities.",
     "Measurement, reporting and verification, offtake contracting, unit sequencing, "
     "local manufacture ramp."),
    ("Stage 4", "Blended finance \u2014 GCF, GEF, World Bank DevelopEx, bilateral "
     "windows, via an accredited entity",
     "Portfolio scale across regions.",
     "Partner selection, accreditation, project documents, environmental and social "
     "impact assessment, and the reporting that keeps the money flowing."),
]

FUND_NOTE = (
    "The one structural fact worth stating plainly: GCF and GEF capital is accessible "
    "to accredited entities, not to a small company directly. So the realistic sequence "
    "is a small first pilot funded by impact capital, with the accredited-finance track "
    "opened as a co-application once a hub has measured data behind it. Companies that "
    "go to GCF first with nothing operating generally do not get funded. The order "
    "matters more than the ambition."
)

C_AND_MONEY = [
    "<b>What makes me useful here is that I am not a specialist.</b> A project like this "
    "fails at the seams: the heat exchanger gets designed and nobody can permit it; the "
    "cooperative is formed and nobody can raise the money; the unit is funded and nobody "
    "can keep it running for fifteen years. Those are the seams I have spent thirty years "
    "working, and they are why my record is broad rather than deep. A company of "
    "specialists delivers the heat exchanger. This project needs somebody who can get a "
    "permit stamped in one jurisdiction, restructure a procurement chain in another, and "
    "sit down with a cooperative board in a third.",

    "<b>I can work the capital stack, and I would rather it be sequenced than rushed.</b> "
    "This kind of project has three distinct funding populations, and they are not "
    "interchangeable. Early-stage feasibility and a small pilot come from impact and "
    "catalytic capital, corporate social responsibility, diaspora and development-finance "
    "money, where the ticket is small and the diligence is light. Commercial scale comes "
    "from carbon and biochar offtake plus equipment debt \u2014 the biochar is the "
    "line that makes it bankable, because a verified carbon drawdown on a real waste "
    "stream is a product with a market, not a projection. And institutional money "
    "\u2014 Green Climate Fund, Global Environment Facility, World Bank DevelopEx, the "
    "bilateral windows \u2014 is the tranche that makes a portfolio possible. Each has "
    "different diligence, different timelines, and different paperwork, and most of these "
    "projects die between tranches rather than inside any one of them.",

    "<b>The honest sequence, which is why I am proposing Stage 0 first.</b> Small money "
    "gets a measured pilot. Measured pilots get the accredited-finance track open, as a "
    "co-application with an entity that holds the accreditation. Of the four tranches, "
    "only the first two are things I would ask for before there is operating data, and "
    "both of them are within reach of a company of your size and mine. I would not bring "
    "you a GCF application and ask you to wait two years for a first disbursement.",
]

HUB = [
    "<b>The unit is a community hub, not a power plant with a customer.</b> Every output "
    "lands on something somebody in the village uses every day: electricity for the "
    "cooperative's processing and lighting, hot water and laundry through the useful-heat "
    "tap, clean water, and biochar as a soil amendment and a cooking-fuel substitute that "
    "takes pressure off the surrounding woodland. Nothing on that list is an export. The "
    "value is created on site and consumed on site, which is what makes the economics work "
    "at a scale too small to interest a utility.",

    "<b>Connectivity is part of the same system, not a separate problem.</b> A hub this "
    "disruptive to daily life needs a communications link to run on \u2014 remote "
    "monitoring, dispatch decisions, payments for biochar and surplus energy, and the "
    "telemetry that makes a 15\u201320 year asset serviceable instead of a mystery. LEO "
    "satellite backhaul with local WiFi node stations gives the hub a link that does not "
    "depend on a grid that was never going to reach it, and it lets a fleet of hubs be "
    "monitored and dispatched as one system from anywhere in the world. Connectivity is "
    "where a remote deployment either becomes operable or becomes a photograph.",

    "<b>The fuel is local, so the supply chain can be too.</b> The published GEMCO "
    "configuration is modular and containerised by design, and that modularity is exactly "
    "what makes local manufacture practical \u2014 vessels, frames, heat exchangers, "
    "skids, and control cabinets can be built and serviced in the regions where the units "
    "deploy, with no import logistics, no tariff exposure, and a spare-parts supply chain "
    "that is not an ocean away from the technician. For a product whose entire purpose is "
    "local resilience, depending on a single international manufacturing origin is a "
    "liability, and a distributed one is an advantage. The first deployment should be "
    "assembled locally with locally made parts, and that should be the standard, not the "
    "exception.",

    "<b>Ecologically, the arithmetic is favourable and the numbers should be published.</b> "
    "Agricultural residue that is currently burned in the field is removed from the "
    "equation, and open-burning of crop residue is a recognised seasonal air-quality and "
    "health problem across the regions this would serve. Biochar returned to agricultural "
    "soil holds carbon and improves water retention on exactly the land that produced the "
    "feedstock. This is a measurable, verifiable improvement rather than a claim, and I "
    "would want the carbon accounting done properly and published, because that is what "
    "makes it financeable and what keeps it honest.",
]

MARKET = [
    "<b>Data center revenue is concentrated, and concentration is a limit.</b> A handful of "
    "very large buyers produce very large contracts \u2014 and they also produce a "
    "reputational position that is contested in the communities those facilities are being "
    "sited in. That contention is real and it is a permitting and community-relations "
    "exposure that no amount of good engineering removes.",

    "<b>Distributed municipal and community power is diffuse, and diffusion is a funnel.</b> "
    "Many small buyers, many small communities, and a revenue base with no single point of "
    "failure. It opens channels a data center sale does not \u2014 distributors, "
    "development-finance capital, municipal and cooperative procurement \u2014 and reference "
    "installations are reusable in a way that one hyperscale win is not. Every hub that goes "
    "in makes the next one easier to permit, to finance, and to sell.",

    "<b>The social enterprise frame is the differentiator, and it is also the most durable "
    "thing here.</b> STPC is a community cooperative serving more than 5,000 seasonal "
    "agricultural workers in the San Quint\u00edn Valley \u2014 biochar, clean water, hot "
    "showers, and a community laundry on infrastructure the community operates. That is not "
    "a marketing angle bolted onto a technology. It is the reason the technology is "
    "permitted, staffed, and politically durable where a private operator would struggle to "
    "site at all. For an investor base that includes climate-focused funds, a demonstrable "
    "operating asset serving a migrant-worker valley survives scrutiny in a way a purchased "
    "carbon offset increasingly does not.",

    "<b>The environmental stance improves, it does not get a paragraph bolted on.</b> A "
    "company that powers AI data centers has a real and increasingly awkward question to "
    "answer about what its hardware does to the places it is built. A platform that also "
    "converts a local waste liability into heat, power, water, and soil amendment \u2014 and "
    "that does it in the developing-world communities those questions are usually asked "
    "about \u2014 has an answer that is demonstrable rather than asserted. That is worth "
    "having before anyone asks. It is worth more after they ask.",
]

ROADMAP = [
    ("Stage 0 \u2014 desktop",
     "Pick one target region and one partner community. Feedstock audit: volume, material "
     "mix, seasonality. Energy and mass balance. Connectivity survey. Permitting and "
     "local-content review. No capital."),
    ("Stage 1 \u2014 bench",
     "Gasifier on a bench scale, measured. Does the syngas drive the Stirling, and at what "
     "efficiency? Does the char come out to spec? Most important: fouling rate on a heat "
     "exchanger across weeks rather than days, and whether the separated gas loop holds the "
     "working fluid clean."),
    ("Stage 2 \u2014 pilot",
     "One container-class gasifier on the same bus as the solar array, feeding a community "
     "heat load, a water and laundry load, and a measured electrical load through the shared "
     "Stirling stack. LEO backhaul and WiFi node stations commissioned with the monitoring "
     "plan, not after it. Full permitting package, stamped and through plan review."),
    ("Stage 3 \u2014 cooperative ownership",
     "Local manufacture of vessels, frames, heat exchangers, skids, and control cabinets. "
     "Transfer operations, maintenance, and revenue share to the partner cooperative. Where "
     "value is created locally, and where the second, third, and fourth hub stop being an "
     "ask."),
]

CLOSEE = (
    "What I am proposing is not a role on your team. It is a function you probably do not "
    "have: somebody who can take this from a published reference design to a permitted, "
    "financed, monitored, cooperatively operated hub in a country neither of us has worked "
    "in, and who can raise the money for the next one while the first is still running. "
    "Waste out of the environment, power and heat and water and soil amendment into a "
    "community, a cooperative holding the asset, a supply chain that is local because the "
    "product is. The environmental story does not need to be written for this platform "
    "\u2014 it gets built in. I would start at Stage 0, because it costs nothing and it is "
    "where an honest answer comes out. I am ready to relocate to Austin or Miami, and I "
    "would like to start on this."
)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(base.RULE)
    canvas.setLineWidth(0.6)
    canvas.line(ML, 36, PW - MR, 36)
    canvas.setFont(base.FONT, 7.5)
    canvas.setFillColor(base.MUTE)
    canvas.drawString(ML, 24, "Eugene L. Buchanan  \u00b7  Technical Proposal to "
                              "Exowatt  \u00b7  stpc@encuentralo.mx")
    canvas.drawRightString(PW - MR, 24, "Page %d" % doc.page)
    canvas.restoreState()


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Vision_Letter_Exowatt.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP, bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Technical Proposal to Exowatt",
                          author="Eugene L. Buchanan",
                          subject="Thermal platform extension: agricultural residue to "
                                  "biochar, heat, and power, built on the Exowatt P3")

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
    story.append(VisionHead(photo=photo_path))
    story.append(NextPageTemplate("content"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(LETTER_DATE, date_style))
    for line in RECIPIENT:
        story.append(Paragraph(line, addr_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph(SUBJECT, subj_style))
    story.append(base.AccentRule())
    story.append(Spacer(1, 6))

    story.append(Paragraph("Dear Exowatt team,", salute_style))

    for para in OPEN:
        story.append(Paragraph(para, body_style))

    # --- what I do: role inventory ---
    story.append(Paragraph("Why I am the person to work on this", h3_style))
    story.append(Paragraph(
        "The role inventory below is not a capability list. It is the set of functions this "
        "project needs, each matched to something I have already done. Everything in it is "
        "drawn from my own record.", note_style))
    story.append(Spacer(1, 2))
    rh = ParagraphStyle("rh", fontName=base.FONT_B, fontSize=7.5, leading=9.4,
                        textColor=colors.white, spaceAfter=0)
    rl = ParagraphStyle("rl", fontName=base.FONT_B, fontSize=7.2, leading=9.0,
                        textColor=NAVY2, spaceAfter=0)
    rd = ParagraphStyle("rd", fontName=base.FONT, fontSize=7.2, leading=9.0,
                        textColor=base.INK, spaceAfter=0)
    rrows = [[Paragraph(ROLE_HEAD[0], rh), Paragraph(ROLE_HEAD[1], rh)]]
    for fn, done in ROLE_ROWS:
        rrows.append([Paragraph(fn, rl), Paragraph(done, rd)])
    rt = Table(rrows, colWidths=[FW * 0.26, FW * 0.74], repeatRows=1)
    rt.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("GRID", (0, 0), (-1, -1), 0.35, base.RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f7f4ff")]),
    ]))
    story.append(rt)
    story.append(Spacer(1, 5))

    # --- topology diagram ---
    story.append(Spacer(1, 2))
    story.append(ThermalBusDiagram(FW, height=228))
    story.append(Spacer(1, 4))

    # --- system mapping table ---
    story.append(Paragraph("Who supplies what, and what is already published",
                           h3_style))
    story.append(Spacer(1, 1))
    sh_st = ParagraphStyle("sh", fontName=base.FONT_B, fontSize=7.3, leading=9.0,
                           textColor=colors.white, spaceAfter=0)
    sd_st = ParagraphStyle("sd", fontName=base.FONT, fontSize=7.3, leading=9.0,
                           textColor=base.INK, spaceAfter=0)
    sl_st = ParagraphStyle("sl", fontName=base.FONT_B, fontSize=7.3, leading=9.0,
                           textColor=NAVY2, spaceAfter=0)

    rows = [[Paragraph(h, sh_st) for h in SYSTEM_HEAD]]
    for fn, who, fig in SYSTEM_ROWS:
        rows.append([Paragraph(fn, sl_st), Paragraph(who, sd_st),
                     Paragraph(fig, sd_st)])
    tbl = Table(rows, colWidths=[FW * 0.34, FW * 0.22, FW * 0.44], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("GRID", (0, 0), (-1, -1), 0.35, base.RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f4ff")]),
    ]))
    story.append(tbl)
    story.append(Paragraph(
        "All figures as published by the named source. GEMCO models are HG-60 and HG-120; "
        "the HG-120 is quoted. P3 details from Exowatt's published product description. "
        "STPC details from the cooperative's published programme. Nothing above is a "
        "Exowatt commitment \u2014 it is a map of what exists.",
        note_style))
    story.append(Spacer(1, 3))

    # --- integration ---
    story.append(Paragraph("Where the integration is real", h3_style))
    for para in INTEGRATION:
        story.append(Paragraph(para, body_style))

    # --- community hub section ---
    story.append(Paragraph("What the unit actually is", h3_style))
    for para in HUB:
        story.append(Paragraph(para, body_style))

    # --- market argument ---
    story.append(Paragraph("Why the second market is strategy, not diversion", h3_style))
    for para in MARKET:
        story.append(Paragraph(para, body_style))

    # --- capital stack ---
    story.append(Paragraph("How this gets funded, and my part in it", h3_style))
    for para in C_AND_MONEY:
        story.append(Paragraph(para, body_style))
    story.append(Spacer(1, 1))
    fh = ParagraphStyle("fh", fontName=base.FONT_B, fontSize=7.5, leading=9.4,
                        textColor=colors.white, spaceAfter=0)
    f1 = ParagraphStyle("f1", fontName=base.FONT_B, fontSize=7.2, leading=9.0,
                        textColor=NAVY2, spaceAfter=0)
    f2 = ParagraphStyle("f2", fontName=base.FONT, fontSize=7.2, leading=9.0,
                        textColor=base.INK, spaceAfter=0)
    frows = [[Paragraph(h, fh) for h in FUND_HEAD]]
    for a, b, cc, d in FUND_ROWS:
        frows.append([Paragraph(a, f1), Paragraph(b, f2), Paragraph(cc, f2),
                      Paragraph(d, f2)])
    ft = Table(frows, colWidths=[FW * 0.09, FW * 0.22, FW * 0.33, FW * 0.36],
               repeatRows=1)
    ft.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0e7c75")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("GRID", (0, 0), (-1, -1), 0.35, base.RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#eefaf7")]),
    ]))
    story.append(ft)
    story.append(Paragraph(FUND_NOTE, note_style))
    story.append(Spacer(1, 5))

    # --- roadmap ---
    story.append(Paragraph("What I would want to validate, in order", h3_style))
    story.append(Spacer(1, 1))
    rs_st = ParagraphStyle("rs", fontName=base.FONT_B, fontSize=7.7, leading=9.8,
                           textColor=NAVY2, spaceAfter=0)
    rd_st = ParagraphStyle("rd", fontName=base.FONT, fontSize=7.7, leading=9.8,
                           textColor=base.INK, spaceAfter=0)
    rrows = [[Paragraph(a, rs_st), Paragraph(b, rd_st)] for a, b in ROADMAP]
    rtbl = Table(rrows, colWidths=[FW * 0.24, FW * 0.76])
    rtbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, base.RULE),
    ]))
    story.append(rtbl)
    story.append(Spacer(1, 5))

    story.append(Paragraph(CLOSEE, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("Best regards,", body_style))
    story.append(Spacer(1, 2))
    story.append(base.AccentRule(width=180))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Eugene L. Buchanan", sign_style))
    story.append(Paragraph("Quality, Test &amp; Controls Engineer  \u00b7  Relocating to "
                           "Austin, TX or Miami, FL", sign2_style))
    story.append(Paragraph("eugene@serviceofothers.org  \u00b7  +1 (909) 545 5384  \u00b7  "
                           "github.com/eugeneb50", sign2_style))
    story.append(Paragraph("STPC \u00b7 stpc@encuentralo.mx", sign2_style))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")
    return out_path


if __name__ == "__main__":
    build()
