#!/usr/bin/env python3
"""Generate a visually dynamic ops resume PDF for Eugene L. Buchanan
   targeted at IT Support Specialist / customer support / clerk roles —
   Ticket, User & Document Life Cycle Management. No HIPAA content.
   Uses reportlab with gradient header, skill bars, tag clouds, and
   experience cards.
"""

import os
import tempfile
import segno
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer, PageBreak,
                                NextPageTemplate, KeepTogether, Flowable,
                                Image as RLImage)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.spider import SpiderChart
from reportlab.graphics import renderPDF

import reportlab.rl_config as _rl_config
_rl_config.documentLang = "en-US"   # PDF /Lang catalog entry (a11y)

# ----------------------------------------------------------------------------
# Fonts (DejaVuSans for clean modern sans-serif)
# ----------------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/TTF"
pdfmetrics.registerFont(TTFont("DJ", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJ-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DJ-I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ-I", boldItalic="DJ-B")



# ----------------------------------------------------------------------------
# Palette  — deep navy + vibrant purple/pink gradient
# ----------------------------------------------------------------------------
NAVY    = colors.HexColor("#1a1342")
NAVY2   = colors.HexColor("#2b1d63")
PURPLE  = colors.HexColor("#7b2cf2")
PINK    = colors.HexColor("#fb2e8e")
TEAL    = colors.HexColor("#15a39a")
TEAL_D  = colors.HexColor("#0e7c75")
LIGHT   = colors.HexColor("#f0eaff")
GREY    = colors.HexColor("#5b6b7b")
DARK    = colors.HexColor("#16202b")
INK     = colors.HexColor("#2b3640")
MUTE    = colors.HexColor("#8a98a6")
RULE    = colors.HexColor("#d4dce4")
TRACK   = colors.HexColor("#e3e9ef")

FONT    = "DJ"
FONT_B  = "DJ-B"
FONT_I  = "DJ-I"

# ----------------------------------------------------------------------------
# Page geometry
# ----------------------------------------------------------------------------
PW, PH = letter                 # 612 x 792
ML = MR = 40
HEADER_H = 120
TOP_GAP = 8
BODY_BOTTOM = 40

FW = PW - ML - MR              # frame width = 532
BODY_W = FW

# ----------------------------------------------------------------------------
# Circular profile photo (masked PNG)
# ----------------------------------------------------------------------------
def make_circular_photo(src_jpg, size=240):
    try:
        im = Image.open(src_jpg).convert("RGBA")
        w, h = im.size
        m = min(w, h)
        left, top = (w - m) // 2, (h - m) // 2
        im = im.crop((left, top, left + m, top + m)).resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
        im.putalpha(mask)
        fd, path = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        im.save(path, "PNG")
        return path
    except Exception:
        return None

# ----------------------------------------------------------------------------
# Gradient helper
# ----------------------------------------------------------------------------
def draw_gradient(c, x, y, w, h, c1, c2, vertical=True, steps=48):
    for i in range(steps):
        t = i / (steps - 1)
        r = c1.red + (c2.red - c1.red) * t
        g = c1.green + (c2.green - c1.green) * t
        b = c1.blue + (c2.blue - c1.blue) * t
        col = colors.Color(r, g, b)
        c.setFillColor(col)
        if vertical:
            yy = y + h * (i / steps)
            c.rect(x, yy, w, h / steps + 1, stroke=0, fill=1)
        else:
            xx = x + w * (i / steps)
            c.rect(xx, y, w / steps + 1, h, stroke=0, fill=1)

# ----------------------------------------------------------------------------
# Custom flowables
# ----------------------------------------------------------------------------
class HeaderBand(Flowable):
    def __init__(self, width=PW, height=HEADER_H, photo=None):
        super().__init__()
        self.width = width
        self.height = height
        self.photo = photo

    def _draw_monogram(self, c, pcx, pcy, pr):
        c.setFillColor(NAVY2)
        c.rect(pcx - pr, pcy - pr, 2 * pr, 2 * pr, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_B, 22)
        c.drawCentredString(pcx, pcy - 8, "EB")

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        # gradient background (purple top → navy bottom)
        draw_gradient(c, 0, 0, W, H, PURPLE, NAVY, vertical=True)

        # accent bar on the left edge
        draw_gradient(c, 0, 0, 6, H, PINK, TEAL, vertical=True, steps=24)

        # profile photo (or monogram fallback) in top-right circle
        pcx, pcy, pr = W - 42, H - 40, 30
        if self.photo and os.path.exists(self.photo):
            try:
                c.drawImage(self.photo, pcx - pr, pcy - pr, 2 * pr, 2 * pr,
                            preserveAspectRatio=True, anchor="c", mask="auto")
            except Exception:
                self._draw_monogram(c, pcx, pcy, pr)
        else:
            self._draw_monogram(c, pcx, pcy, pr)
        c.setStrokeColor(colors.white); c.setLineWidth(1.5)
        c.circle(pcx, pcy, pr, fill=0, stroke=1)

        # name
        c.setFillColor(colors.white)
        c.setFont(FONT_B, 24)
        c.drawString(28, H - 44, "EUGENE L. BUCHANAN")
        # title
        c.setFillColor(colors.HexColor("#e0cfff"))
        c.setFont(FONT, 11)
        c.drawString(28, H - 64, "IT Support Specialist  \u2014  Ticket, User & Document Lifecycle Support")
        # separator
        c.setStrokeColor(colors.white); c.setFillAlpha(0.22); c.setLineWidth(0.5)
        c.line(28, H - 74, pcx - pr - 10, H - 74); c.setFillAlpha(1)
        # contact strip
        items = [("L", "Apple Valley, CA (Remote)", None),
                 ("T", "+1 (909) 545 5384", None),
                 ("E", "eugene@serviceofothers.org", "mailto:eugene@serviceofothers.org"),
                 ("G", "github.com/eugeneb50", "https://github.com/eugeneb50")]
        x = 28; cy = H - 88
        link_rects = []
        for letter, txt, url in items:
            c.setFillColor(colors.white); c.setFillAlpha(0.20)
            c.circle(x + 7, cy + 4, 7, fill=1, stroke=0); c.setFillAlpha(1)
            c.setFillColor(colors.white); c.setFont(FONT_B, 7.5)
            c.drawCentredString(x + 7, cy + 1, letter)
            c.setFillColor(colors.HexColor("#eaeafa")); c.setFont(FONT, 7.5)
            c.drawString(x + 17, cy - 1, txt)
            tw = pdfmetrics.stringWidth(txt, FONT, 7.5)
            if url:
                link_rects.append((url, x + 17, cy - 4, x + 17 + tw, cy + 10))
            x += 17 + tw + 12
        for url, x1, y1, x2, y2 in link_rects:
            c.linkURL(url, (x1, y1, x2, y2), relative=1)


class SectionTitle(Flowable):
    def __init__(self, text, width=FW, accent=PURPLE):
        super().__init__()
        self.text = text
        self.width = width
        self.height = 24
        self.accent = accent

    def wrap(self, a, h):
        self.width = a
        return (a, self.height)

    def draw(self):
        c = self.canv
        H = self.height
        c.setFillColor(self.accent)
        c.rect(0, H - 15, 5, 15, fill=1, stroke=0)
        c.setFont(FONT_B, 13)
        c.setFillColor(DARK)
        c.drawString(14, H - 14, self.text)
        tw = pdfmetrics.stringWidth(self.text, FONT_B, 13)
        c.setStrokeColor(RULE); c.setLineWidth(0.8)
        c.line(14 + tw + 12, H / 2 + 1, self.width, H / 2 + 1)


class SkillBar(Flowable):
    def __init__(self, label, pct, width=FW, color1=PURPLE, color2=PINK):
        super().__init__()
        self.label = label
        self.pct = pct
        self.width = width
        self.height = 19
        self.c1 = color1
        self.c2 = color2

    def wrap(self, a, h):
        self.width = a
        return (a, self.height)

    def draw(self):
        c = self.canv
        H = self.height
        c.setFont(FONT_B, 7.6); c.setFillColor(DARK)
        c.drawString(0, H - 11, self.label)
        c.setFont(FONT, 7.6); c.setFillColor(self.c1)
        c.drawRightString(self.width, H - 11, f"{self.pct}%")
        bx, by, bh = 0, 1, 4.5
        bw = self.width
        c.setFillColor(TRACK); c.roundRect(bx, by, bw, bh, 2.5, fill=1, stroke=0)
        fw = max(bw * self.pct / 100.0, 6)
        draw_gradient(c, bx, by, fw, bh, self.c1, self.c2, vertical=False, steps=24)
        c.setFillColor(self.c1); c.roundRect(bx, by, fw, bh, 2.5, fill=1, stroke=0)


class TagCloud(Flowable):
    def __init__(self, tags, width=FW, size=7.0, padx=5, pady=1.5, gap=3,
                 bg=LIGHT, fg=PURPLE):
        super().__init__()
        self.tags = tags
        self.size = size
        self.padx = padx
        self.pady = pady
        self.gap = gap
        self.bg = bg
        self.fg = fg
        self.width = width
        self.lh = size + 2 * pady + 4

    def wrap(self, a, h):
        self.width = a
        self.lines = []
        x = 0
        cur = []
        for t in self.tags:
            w = pdfmetrics.stringWidth(t, FONT, self.size) + 2 * self.padx
            if x > 0 and x + w > a:
                self.lines.append(cur)
                cur = []; x = 0
            cur.append((t, w))
            x += w + self.gap
        if cur:
            self.lines.append(cur)
        self.height = len(self.lines) * self.lh + (len(self.lines) - 1) * self.gap
        return (a, self.height)

    def draw(self):
        c = self.canv
        y = self.height - self.lh
        for items in self.lines:
            x = 0
            for (t, w) in items:
                c.setFillColor(self.bg)
                c.roundRect(x, y, w, self.lh - 4, 4, fill=1, stroke=0)
                c.setFillColor(self.fg)
                c.setFont(FONT, self.size)
                c.drawString(x + self.padx, y + (self.lh - 4 - self.size) / 2, t)
                x += w + self.gap
            y -= self.lh + self.gap


# ----------------------------------------------------------------------------
# Radar chart (reportlab.graphics SpiderChart) — skill profile visualization
# ----------------------------------------------------------------------------
class SkillRadar(Flowable):
    """Compact radar chart built with reportlab.graphics (SpiderChart)."""
    def __init__(self, labels, values, width=215, height=140):
        super().__init__()
        self.width = width
        self.height = height
        self.labels = labels
        self.values = values

    def wrap(self, aW, aH):
        return (self.width, self.height)

    def draw(self):
        d = Drawing(self.width, self.height)
        s = SpiderChart()
        s.x = 40
        s.y = 12
        s.width = 140
        s.height = 105
        s.startAngle = 90
        s.direction = "clockwise"
        s.data = [self.values]
        s.labels = self.labels
        s.spokes.strokeWidth = 0.5
        s.spokes.strokeColor = colors.Color(0.1, 0.08, 0.26, alpha=0.10)
        s.spokes.labelRadius = 1.18
        s.spokeLabels.fontName = FONT_B
        s.spokeLabels.fontSize = 6.6
        s.spokeLabels.fillColor = NAVY2
        s.strands.strokeColor = PURPLE
        s.strands.strokeWidth = 2.2
        s.strands.fillColor = colors.Color(0.48, 0.17, 0.95, alpha=0.14)
        s.strands.symbol = "Circle"
        s.strands.symbolSize = 3.2
        d.add(s)
        renderPDF.draw(d, self.canv, 0, 0)


# ----------------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------------
summary_style = ParagraphStyle("sum", fontName=FONT, fontSize=9.4, leading=12.8,
                               textColor=INK, alignment=TA_JUSTIFY)
role_style = ParagraphStyle("role", fontName=FONT_B, fontSize=11, leading=13.5,
                            textColor=DARK, spaceAfter=0)
date_style = ParagraphStyle("date", fontName=FONT, fontSize=8.6, leading=11.5,
                            textColor=GREY, alignment=2)
sub_style = ParagraphStyle("sub", fontName=FONT, fontSize=9.1, leading=11.5,
                           textColor=PURPLE, spaceAfter=3)
bullet_style = ParagraphStyle("bul", fontName=FONT, fontSize=8.6, leading=10.6,
                              leftIndent=12, bulletIndent=1, bulletColor=PURPLE,
                              spaceAfter=1.2, textColor=INK)
str_style = ParagraphStyle("str", fontName=FONT, fontSize=7.9, leading=9.6,
                           leftIndent=12, bulletIndent=0, bulletColor=PURPLE,
                           spaceAfter=1.2, textColor=INK)
edu_style = ParagraphStyle("edu", fontName=FONT, fontSize=8.2, leading=11.0,
                           leftIndent=12, bulletIndent=1, bulletColor=PURPLE,
                           spaceAfter=2, textColor=INK)
edu_inline_style = ParagraphStyle("eduin", fontName=FONT, fontSize=8.2,
                                  leading=11.0, textColor=INK)
tagcap_style = ParagraphStyle("tagcap", fontName=FONT_B, fontSize=8.6, leading=12,
                              textColor=GREY, spaceBefore=2, spaceAfter=4)
qr_cap_style = ParagraphStyle("qrcap", fontName=FONT, fontSize=6.4, leading=8,
                              alignment=1, textColor=MUTE)
int_title_style = ParagraphStyle("intt", fontName=FONT_B, fontSize=8.8, leading=10.5,
                                 textColor=PURPLE, spaceAfter=1.5)
int_body_style = ParagraphStyle("intb", fontName=FONT, fontSize=7.9, leading=9.9,
                                textColor=INK)
int_box_style = ParagraphStyle("intbox", fontName=FONT_B, fontSize=10.5, leading=13,
                               textColor=DARK, spaceAfter=2)


# QR code pointing at the GitHub repo (right-aligned block, sits under Education).
QR_URL = "https://github.com/eugeneb50/eugeneb50/"


def qr_block(size=72):
    """Generate a themed QR PNG of QR_URL and return a right-aligned flowable."""
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    segno.make_qr(QR_URL, error="m").save(
        path, scale=10, dark="#1a1342", light="#ffffff", border=0)
    qr = RLImage(path, width=size, height=size)
    caption = Paragraph("GitHub \u2014 eugeneb50", qr_cap_style)
    cell = Table([[qr], [caption]], colWidths=[size])
    cell.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return cell


INTERESTS = [
    ("Renewable Energy",
     "Solar, storage, and the grid of the future."),
    ("Permaculture",
     "Food forests, rainwater harvesting, and topsoil."),
    ("Real Estate",
     "Buy-and-hold multifamily, cash-flow-first."),
    ("Tango Dancing",
     "Argentine tango \u2014 embrace, pause, musicality."),
]


def interests_block(width):
    """Boxed 'Other Interests' panel: title bar + 2x2 grid of short blurbs."""
    half = (width - 8) / 2.0

    def cell(title, body):
        return [Paragraph(title, int_title_style),
                Paragraph(body, int_body_style)]

    grid = Table([[cell(*INTERESTS[0]), cell(*INTERESTS[1])],
                  [cell(*INTERESTS[2]), cell(*INTERESTS[3])]],
                 colWidths=[half, half])
    grid.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    box = Table([[Paragraph("Other Interests", int_box_style)], [grid]],
                colWidths=[width])
    box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.9, RULE),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return box


def strengths_block(width=BODY_W):
    """Boxed static 'Key Strengths' panel (no interactive form fields)."""
    rows = [[P('<b><font color="#2b1d63">%s.</font></b>  %s' % (t, d),
               str_style, bullet="\u2022")] for t, d in STRENGTHS]
    box = Table(rows, colWidths=[width - 16])
    box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.9, RULE),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return box


def P(text, style, bullet=None):
    return Paragraph(text, style, bulletText=bullet)

def bullet_p(t):
    return P(t, bullet_style, bullet="\u2022")

# ----------------------------------------------------------------------------
# Experience builder
# ----------------------------------------------------------------------------
def experience_card(role, company_loc, dates, bullets):
    meta = Table([[P(role, role_style), P(dates, date_style)]],
                 colWidths=[306, 200])
    meta.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (0, 0), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    flow = [meta, P(company_loc, sub_style)]
    for b in bullets:
        flow.append(bullet_p(b))
    card = Table([[flow]], colWidths=[BODY_W])
    card.setStyle(TableStyle([
        ("LINEBEFORE", (0, 0), (0, -1), 3, PURPLE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 12),
        ("RIGHTPADDING", (0, 0), (0, 0), 6),
        ("TOPPADDING", (0, 0), (0, 0), 2),
        ("BOTTOMPADDING", (0, 0), (0, 0), 2),
    ]))
    return [card, Spacer(1, 1)]

# Content — IT Support Specialist, Ticket / User / Document Lifecycle
# ----------------------------------------------------------------------------
SUMMARY = ("IT support specialist with 25+ years helping users and keeping systems "
           "running \u2014 from help-desk and campus IT to freelance consulting and SaaS "
           "support tooling. I own Ticket Life Cycle Management end to end: intake, triage, resolution, "
           "and follow-up \u2014 plus user onboarding and offboarding, access provisioning, "
           "and the knowledge-base documentation teams actually use. I explain fixes in "
           "plain language, escalate cleanly, lead QA, and build AI helpdesk tooling "
           "that keep queues short.")

EXPERIENCE = [
    ("Support Tooling Contributor (Open-Source)",
     "ZeroClaw Labs (github.com/zeroclaw-labs/zeroclaw)  \u00b7  Rust",
     "2026 \u2013 Present", [
        "Built lifecycle-state ctx monitoring and usage metering for queue "
        "visibility and cost logging, terminal state reporting for agentic "
        "multiplexer.",
     ]),
    ("Test Automation Lead / QA Lead \u2014 AI Helpdesk Support",
     "Knowledgecity LLC  \u00b7  Remote  \u00b7  AWS / Postgres / React",
     "Dec 2020 \u2013 Aug 2025", [
        "Led QA for LMS integrations (SAP, Oracle, Workday, Coursera, UKG, Zoom, "
        "SCORM, LTI, webhooks): hired and trained the automation team; shipped "
        "the regression suite with health dashboards and alerting.",
        "Helped develop the AI helpdesk chatbot (RAG retrieval + guardrails) that "
        "deflects repetitive tickets; carried users through auth, data, and error "
        "issues to closure.",
        "White-box tested the CI/CD pipeline (Apache/REST/SQL/AWS/React); drove "
        "SOC 2 research and implementation; joined blue-team incident forensics.",
     ]),
    ("Consultant - IT Support",
     "Foremost Senior Care / Foremost Organization  \u00b7  Hesperia, CA",
     "2013 \u2013 2016", [
        "Provided campus IT support: wrote security and backup policies for "
        "servers and PCs; upgraded video surveillance with remote access; "
        "installed campus-wide wireless.",
        "Evaluated and migrated accounting and medical-records software for "
        "the care campus.",
        "Built the nonprofit community outreach program; developed and filed "
        "federal, state, and city applications; ran a community social program.",
     ]),
    ("Computer Service Technician \u2014 Geek Squad",
     "Best Buy  \u00b7  Victorville, CA",
     "2007", [
        "Ran the retail service desk: logged tickets, triaged walk-ins, tracked "
        "units through check-in/repair/pickup, and gave plain-language updates.",
        "Set up new PCs, migrated user data, fixed virus/OS/hardware issues "
        "\u2014 and matched customers to service plans, accessories, and upgrades; "
        "handled payments and refunds.",
     ]),
    ("Freelance IT Consultant",
     "AMP Computer  \u00b7  Apple Valley, CA",
     "2003 \u2013 2011", [
        "Sold, set up, and supported PCs and servers for small offices; configured "
        "ERP/CRM systems and office automation.",
     ]),
    ("IT Manager",
     "Lucerne Valley Unified School District  \u00b7  Lucerne Valley, CA",
     "2002", [
        "Supported four campuses: WAN/LAN, servers, desktops, and classroom A/V \u2014 "
        "first responder for staff and student issues; ran attendance ETL with "
        "table locking and certification.",
     ]),
    ("Earlier Roles \u2014 SDET & Helpdesk",
     "Microsoft  \u00b7  RealNetworks  \u00b7  IBM  \u00b7  Keene Inc.  \u00b7  Seattle / Redmond / Kirkland, WA",
     "1996 \u2013 2001", [
        "SDET, RealNetworks Sr. Engineer II (1999\u20132001): streaming-media QA across "
        "Linux/Unix/Windows/Embedded; research team (TFRCP patent); presales in "
        "Japan/Korea; new-hire training.",
        "SDET, Microsoft (1999): Windows Media Server nightly automation; (1997): "
        "Win 98/NT OEM setup/driver verification. IBM (1998): high-availability "
        "servers, WHQL cluster-failover certification.",
        "Helpdesk, Keene Inc. Technical Support Agent II (1996): frontline and "
        "escalated support ticketing for Windows 95/NT.",
     ]),
]

SKILLS = [
    ("Ticket Queue Management (Triage & SLA)", 90),
    ("User Lifecycle & Access Provisioning", 88),
    ("Technical Troubleshooting (Windows/Linux)", 90),
    ("Customer Communication & Support", 92),
    ("Knowledge Base & SOP Documentation", 86),
    ("Identity & Access (Okta, RBAC, SAML/OAuth)", 84),
    ("Networking Basics (LAN/WAN, SFTP)", 82),
    ("Test & Release Support (QA Lead, Cypress, Selenium, SQL, Git)", 85),
    ("AI Helpdesk & Chatbot Tooling (RAG)", 83),
]

STRENGTHS = [
    ("Ticket lifecycle ownership",
     "Intake, triage, escalation, resolution, and closure \u2014 with status updates "
     "users can follow and follow-up that sticks."),
    ("User lifecycle & access",
     "Onboarding and offboarding, Okta and RBAC provisioning, and account merging "
     "that keeps records clean."),
    ("Documentation people use",
     "Knowledge Base articles and SOP guides written in plain language, "
     "kept current, and easy to find."),
    ("Support tooling that helps",
     "Chatbot assistance, monitoring dashboards, and small automations that "
     "deflect tickets and shorten queues."),
    ("Plain-language communication",
     "Explain fixes to non-technical users, train new staff, and partner daily "
     "with teams across the organization."),
]

EDUCATION = [
    "Associate Degree, Victor Valley College",
    "California Notary Commission",
    "Toastmasters International",
]

TAG_SECTIONS = [
    ("Support & Ticketing", [
        "Ticket Life Cycle Management", "Triage", "Escalation", "SLA Ownership",
        "Jira", "Confluence", "Status Updates", "Follow-up",
    ]),
    ("Users & Access", [
        "User Life Cycle Management", "Access Provisioning", "Onboarding",
        "Offboarding", "Okta", "RBAC", "SAML", "OAuth", "Account Merging",
    ]),
    ("Documentation & Records", [
        "Document Life Cycle Management", "Knowledge Base", "SOP",
        "Technical Writing", "Records Migration", "IT Asset Tracking",
        "Vendor Notes",
    ]),
    ("Systems & Tooling", [
        "Windows", "Linux", "LAN/WAN", "SFTP", "ERP/CRM Support",
        "Regression Testing", "Health Dashboards", "Chatbot Support",
        "Prompt Engineering",
    ]),
]

# ----------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE); canvas.setLineWidth(0.6)
    canvas.line(ML, 34, PW - MR, 34)
    canvas.setFont(FONT, 7.5); canvas.setFillColor(MUTE)
    canvas.drawString(ML, 24,
        "Eugene L. Buchanan  \u00b7  IT Support Specialist \u2014 Ticket, User & Document Lifecycle")
    canvas.drawRightString(PW - MR, 24, "Page %d" % doc.page)
    canvas.restoreState()


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Resume_Ops.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP, bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 IT Support Specialist Resume",
                          author="Eugene L. Buchanan",
                          subject="IT Support Specialist \u2014 Ticket, User & Document Lifecycle Support (Apple Valley, CA)",
                           keywords="IT Support Specialist, help desk, ticket life cycle, user life cycle, document life cycle, access provisioning, Okta, RBAC, SOP, knowledge base, customer support, retail support, Geek Squad")
    header_frame = Frame(0, PH - HEADER_H, PW, HEADER_H, leftPadding=0,
                         rightPadding=0, topPadding=0, bottomPadding=0, id="hdr")
    cover_body = Frame(ML, BODY_BOTTOM, FW, (PH - HEADER_H - TOP_GAP) - BODY_BOTTOM,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                        id="cbody")
    content_body = Frame(ML, BODY_BOTTOM, FW, PH - BODY_BOTTOM - BODY_BOTTOM,
                         leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                         id="body")

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[header_frame, cover_body], onPage=footer),
        PageTemplate(id="content", frames=[content_body], onPage=footer),
    ])

    story = []
    photo_path = make_circular_photo(os.path.join(out_dir, "pic.jpg"))
    story.append(HeaderBand(photo=photo_path))
    story.append(NextPageTemplate("content"))
    story.append(Spacer(1, 1))

    # ── Professional Summary ─────────────────────────────────────────
    story.append(SectionTitle("Professional Summary"))
    story.append(Spacer(1, 1))
    story.append(P(SUMMARY, summary_style))
    story.append(Spacer(1, 1))

    # ── Technical Expertise (skill bars + radar chart) ────────────────
    story.append(SectionTitle("Technical Expertise"))
    story.append(Spacer(1, 1))
    bars_col = [SkillBar(label, pct) for label, pct in SKILLS]
    radar_col = [SkillRadar(
        ["Ticket\nTriage", "User\nSupport", "Trouble-\nshooting",
         "Documenta-\ntion", "Support\nTooling", "Communi-\ncation"],
        [90, 92, 90, 86, 83, 92])]
    expertise = Table([[bars_col, radar_col]], colWidths=[FW - 215, 215])
    expertise.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(expertise)
    story.append(Spacer(1, 1))

    # ── Technology Stack (tag clouds by category) ────────────────────
    story.append(SectionTitle("Technology Stack"))
    story.append(Spacer(1, 1))
    for cat_name, cat_tags in TAG_SECTIONS:
        story.append(TagCloud(cat_tags))
        story.append(Spacer(1, 0.5))
    story.append(Spacer(1, 1))

    # ── Key Strengths (static panel, bottom of page 1) ──────────────
    story.append(SectionTitle("Key Strengths"))
    story.append(Spacer(1, 1))
    story.append(strengths_block())
    story.append(PageBreak())

    # ── Experience (second page) ────────────────────────────────────
    story.append(SectionTitle("Experience"))
    story.append(Spacer(1, 1))
    for role, cl, dates, bullets in EXPERIENCE:
        story.extend(experience_card(role, cl, dates, bullets))
    story.append(Spacer(1, 1))

    # ── Education ────────────────────────────────────────────────
    story.append(SectionTitle("Education"))
    story.append(Spacer(1, 1))
    story.append(P("  \u2022  ".join(EDUCATION), edu_inline_style))

    # ── Other Interests + GitHub QR (bottom of page 2) ─────────────
    story.append(Spacer(1, 2))
    bottom_row = Table([[interests_block(FW - 104), qr_block()]],
                       colWidths=[FW - 104, 104])
    bottom_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(bottom_row)


    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
