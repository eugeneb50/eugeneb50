#!/usr/bin/env python3
"""Generate a visually dynamic resume PDF for Eugene L. Buchanan using reportlab."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer,
                                NextPageTemplate, KeepTogether, Flowable)
from reportlab.pdfgen import canvas as canvas_mod

# ----------------------------------------------------------------------------
# Fonts (DejaVuSans for clean modern sans-serif)
# ----------------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DJ", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJ-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ", boldItalic="DJ-B")

# ----------------------------------------------------------------------------
# Palette
# ----------------------------------------------------------------------------
NAVY   = colors.HexColor("#0e2a47")
NAVY2  = colors.HexColor("#16395f")
TEAL   = colors.HexColor("#15a39a")
TEAL_D = colors.HexColor("#0e7c75")
LIGHT  = colors.HexColor("#e7f4f2")
GREY   = colors.HexColor("#5b6b7b")
DARK   = colors.HexColor("#16202b")
INK    = colors.HexColor("#2b3640")
MUTE   = colors.HexColor("#8a98a6")
RULE   = colors.HexColor("#d4dce4")
TRACK  = colors.HexColor("#e3e9ef")

FONT    = "DJ"
FONT_B  = "DJ-B"

# ----------------------------------------------------------------------------
# Page geometry
# ----------------------------------------------------------------------------
PW, PH = letter                 # 612 x 792
ML = MR = 40
HEADER_H = 140
TOP_GAP = 16
BODY_BOTTOM = 46

FW = PW - ML - MR              # frame width = 532
BODY_W = FW                    # card width

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

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        # gradient background (navy top -> dark teal bottom)
        draw_gradient(c, 0, 0, W, H, TEAL_D, NAVY, vertical=True)

        # profile photo (or monogram fallback) in top-right circle
        pcx, pcy, pr = W - 46, H - 46, 34
        c.saveState()
        path = c.beginPath()
        path.circle(pcx, pcy, pr)
        c.clipPath(path, stroke=0, fill=0)
        if self.photo and os.path.exists(self.photo):
            c.drawImage(self.photo, pcx - pr, pcy - pr, 2 * pr, 2 * pr,
                        preserveAspectRatio=True, anchor="c", mask="auto")
        else:
            c.setFillColor(NAVY2)
            c.rect(pcx - pr, pcy - pr, 2 * pr, 2 * pr, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont(FONT_B, 26)
            c.drawCentredString(pcx, pcy - 9, "EB")
        c.restoreState()
        c.setStrokeColor(colors.white); c.setLineWidth(2)
        c.circle(pcx, pcy, pr, fill=0, stroke=1)

        # name
        c.setFillColor(colors.white)
        c.setFont(FONT_B, 27)
        c.drawString(28, H - 50, "EUGENE L. BUCHANAN")
        # title
        c.setFillColor(colors.HexColor("#bfe9e4"))
        c.setFont(FONT, 13)
        c.drawString(28, H - 74, "Technical Support Specialist  \u2014  Healthcare Technology")
        # separator (stops before the photo)
        c.setStrokeColor(colors.white); c.setFillAlpha(0.22); c.setLineWidth(0.6)
        c.line(28, H - 88, pcx - pr - 12, H - 88); c.setFillAlpha(1)
        # contact strip
        items = [("L", "Apple Valley, CA", None),
                 ("T", "+1 (909) 545 5384", None),
                 ("M", "eugene@serviceofothers.org", "mailto:eugene@serviceofothers.org"),
                 ("G", "github.com/eugeneb50", "https://github.com/eugeneb50")]
        x = 28
        cy = H - 106
        link_rects = []
        for letter, txt, url in items:
            c.setFillColor(colors.white); c.setFillAlpha(0.20)
            c.circle(x + 8, cy + 4, 8, fill=1, stroke=0); c.setFillAlpha(1)
            c.setFillColor(colors.white); c.setFont(FONT_B, 8.5)
            c.drawCentredString(x + 8, cy + 1, letter)
            c.setFillColor(colors.HexColor("#eaf6f4")); c.setFont(FONT, 8.5)
            c.drawString(x + 19, cy, txt)
            tw = pdfmetrics.stringWidth(txt, FONT, 8.5)
            if url:
                link_rects.append((url, x + 19, cy - 2, x + 19 + tw, cy + 12))
            x += 19 + tw + 16
        for url, x1, y1, x2, y2 in link_rects:
            c.linkURL(url, (x1, y1, x2, y2), relative=1)


class SectionTitle(Flowable):
    def __init__(self, text, width=FW):
        super().__init__()
        self.text = text
        self.width = width
        self.height = 24

    def wrap(self, a, h):
        self.width = a
        return (a, self.height)

    def draw(self):
        c = self.canv
        H = self.height
        c.setFillColor(TEAL)
        c.rect(0, H - 15, 5, 15, fill=1, stroke=0)
        c.setFont(FONT_B, 13)
        c.setFillColor(DARK)
        c.drawString(14, H - 14, self.text)
        tw = pdfmetrics.stringWidth(self.text, FONT_B, 13)
        c.setStrokeColor(RULE); c.setLineWidth(0.8)
        c.line(14 + tw + 12, H / 2 + 1, self.width, H / 2 + 1)


class SkillBar(Flowable):
    def __init__(self, label, pct, width=FW):
        super().__init__()
        self.label = label
        self.pct = pct
        self.width = width
        self.height = 21

    def wrap(self, a, h):
        self.width = a
        return (a, self.height)

    def draw(self):
        c = self.canv
        H = self.height
        c.setFont(FONT_B, 8.8); c.setFillColor(DARK)
        c.drawString(0, H - 11, self.label)
        c.setFont(FONT, 8.8); c.setFillColor(TEAL_D)
        c.drawRightString(self.width, H - 11, f"{self.pct}%")
        bx, by, bh = 0, 2, 5.5
        bw = self.width
        c.setFillColor(TRACK); c.roundRect(bx, by, bw, bh, 2.5, fill=1, stroke=0)
        fw = max(bw * self.pct / 100.0, 6)
        draw_gradient(c, bx, by, fw, bh, TEAL_D, TEAL, vertical=False, steps=24)
        c.setFillColor(TEAL); c.roundRect(bx, by, fw, bh, 2.5, fill=1, stroke=0)


class TagCloud(Flowable):
    def __init__(self, tags, width=FW, size=8.3, padx=7, pady=4, gap=6,
                 bg=LIGHT, fg=TEAL_D):
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
# Styles
# ----------------------------------------------------------------------------
summary_style = ParagraphStyle("sum", fontName=FONT, fontSize=9.4, leading=12.8,
                               textColor=INK, alignment=TA_JUSTIFY)
role_style = ParagraphStyle("role", fontName=FONT_B, fontSize=11, leading=13.5,
                            textColor=DARK, spaceAfter=0)
date_style = ParagraphStyle("date", fontName=FONT, fontSize=8.6, leading=11.5,
                            textColor=GREY, alignment=2)
sub_style = ParagraphStyle("sub", fontName=FONT, fontSize=9.1, leading=11.5,
                           textColor=TEAL_D, spaceAfter=3)
bullet_style = ParagraphStyle("bul", fontName=FONT, fontSize=8.9, leading=11.8,
                              leftIndent=12, bulletIndent=1, bulletColor=TEAL,
                              spaceAfter=2.2, textColor=INK)
str_style = ParagraphStyle("str", fontName=FONT, fontSize=9.2, leading=12.6,
                           leftIndent=12, bulletIndent=0, bulletColor=TEAL,
                           spaceAfter=4.5, textColor=INK)
edu_style = ParagraphStyle("edu", fontName=FONT, fontSize=9.3, leading=13,
                           leftIndent=12, bulletIndent=1, bulletColor=TEAL,
                           spaceAfter=3, textColor=INK)
tagcap_style = ParagraphStyle("tagcap", fontName=FONT_B, fontSize=8.6, leading=12,
                              textColor=GREY, spaceBefore=2, spaceAfter=4)


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
        ("LINEBEFORE", (0, 0), (0, -1), 3, TEAL),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 12),
        ("RIGHTPADDING", (0, 0), (0, 0), 6),
        ("TOPPADDING", (0, 0), (0, 0), 2),
        ("BOTTOMPADDING", (0, 0), (0, 0), 2),
    ]))
    return [card, Spacer(1, 5)]

# ----------------------------------------------------------------------------
# Content
# ----------------------------------------------------------------------------
EXPERIENCE = [
    ("Senior Quality Assurance Engineer / Test Automation Lead / Product Owner, Integrations",
     "Knowledgecity LLC  \u00b7  Remote", "Dec 2020 \u2013 Aug 2025", [
        "On average actively working 10\u201315 concurrent tickets across integration, backend, API, database, and frontend surfaces using SQL queries, Elastic logs, and application code review.",
        "Used co-pilot assisted code reading to understand expected behavior and identify root causes of complex cross-service failures.",
        "Authored internal runbooks and knowledge base articles for common failure patterns, reducing repeat escalations.",
        "Managed customer integrations via REST APIs, SFTP, SAML, and OAuth \u2014 debugging authentication issues, data discrepancies, and payload mismatches.",
        "Communicated technical findings to both engineering teams and non-technical stakeholders, translating database anomalies and API errors into clear remediation steps.",
     ]),
    ("Business Consultant \u2014 Foremost Senior Center",
     "Foremost Organization  \u00b7  Hesperia, CA", "2013 \u2013 2016", [
        "Evaluated, selected, and troubleshot medical billing software for senior center operations.",
        "Investigated software billing discrepancies, claims submission workflows, and eligibility verification processes.",
        "Served as technical liaison between clinical staff and software vendors, translating operational requirements into system configurations.",
     ]),
    ("Senior Software Engineer / Technical Support & Presales Engineering",
     "RealNetworks  \u00b7  Seattle, WA", "1999 \u2013 2001", [
        "Provided global presales engineering and technical support for a streaming media platform.",
        "Investigated customer-reported issues across server infrastructure, mobile platforms, and network configurations.",
     ]),
    ("Technical Support Agent II",
     "Keene Inc.  \u00b7  Seattle, WA", "1996", [
        "Provided Tier 2 technical support for Windows 95/NT systems across enterprise clients.",
        "Managed multiple concurrent customer issues, triaging by urgency and impact.",
     ]),
    ("Senior Software Test Engineer",
     "Microsoft  \u00b7  Redmond, WA", "1997 \u2013 1999", [
        "White box testing for Windows 98/NT and Windows Media Server.",
        "Built automated regression suites and defect tracking workflows.",
     ]),
]

SKILLS = [
    ("Investigation & Debugging", 95),
    ("Development & Code Reading", 90),
    ("Integration & APIs", 88),
    ("Tools & Platforms", 92),
    ("Healthcare Domain", 80),
    ("Technical Communication", 95),
]

TAGS = ["SQL", "REST APIs", "HTTP", "JSON", "Elasticsearch", "Sentry", "Root Cause Analysis",
        "Python", "JavaScript", "PHP", "Django", "React", "TypeScript", "GraphQL",
        "AI Co-pilot", "White-box Testing", "FHIR", "SAML", "OAuth", "SFTP",
        "API Design", "PostgreSQL", "MySQL", "Slack", "Jira", "Confluence",
        "Bitbucket", "Cypress", "Selenium", "Postman", "JUnit", "Git", "Node.js"]

STRENGTHS = [
    ("Systematic investigation", "Check logs, query data, and read code before forming hypotheses."),
    ("Customer empathy", "Equally comfortable investigating a database anomaly and walking a stakeholder through a workflow change."),
    ("Technical communication", "Experienced explaining complex concepts to both developers and non-technical users."),
    ("Healthcare-adjacent experience", "Understanding of compliance, operational workflows, and mission-critical system reliability."),
    ("AI-assisted workflow", "Active contributor to ZeroClaw agentic AI infrastructure with practical experience building and debugging AI-powered tooling."),
]

EDUCATION = [
    "California Notary Commission",
    "Toastmasters International",
    "Associate Degree, Victor Valley College",
    "High School Diploma, Lucerne Valley High School",
]

SUMMARY = ("Technical support specialist and senior software engineer with 25+ years of "
           "experience bridging customers and engineering teams. Proven track record "
           "investigating complex technical issues across REST APIs, SQL databases, and "
           "distributed systems. Skilled at translating clinical and operational "
           "requirements into actionable technical guidance. Comfortable working with "
           "clinicians, developers, and practice managers to resolve high-impact issues "
           "under pressure.")

# ----------------------------------------------------------------------------
# Document assembly
# ----------------------------------------------------------------------------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE); canvas.setLineWidth(0.6)
    canvas.line(ML, 34, PW - MR, 34)
    canvas.setFont(FONT, 7.5); canvas.setFillColor(MUTE)
    canvas.drawString(ML, 24, "Eugene L. Buchanan  \u00b7  Technical Support Specialist \u2014 Healthcare Technology")
    canvas.drawRightString(PW - MR, 24, "Page %d" % doc.page)
    canvas.restoreState()


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Resume.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP, bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Resume",
                          author="Eugene L. Buchanan")
    # frames
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
    story.append(HeaderBand(photo=os.path.join(out_dir, "profile.jpg")))
    story.append(NextPageTemplate("content"))
    story.append(Spacer(1, 4))

    # Summary
    story.append(KeepTogether([SectionTitle("Professional Summary"), Spacer(1, 3),
                               P(SUMMARY, summary_style)]))
    story.append(Spacer(1, 8))

    # Technical Expertise
    story.append(SectionTitle("Technical Expertise"))
    story.append(Spacer(1, 4))
    for label, pct in SKILLS:
        story.append(SkillBar(label, pct))
    story.append(Spacer(1, 8))

    # Experience
    story.append(SectionTitle("Experience"))
    story.append(Spacer(1, 4))
    for role, cl, dates, bullets in EXPERIENCE:
        story.extend(experience_card(role, cl, dates, bullets))
    story.append(Spacer(1, 4))

    # Education & Certifications  +  Key Strengths (side-by-side)
    edu_col = [SectionTitle("Education & Certifications"), Spacer(1, 3)]
    for e in EDUCATION:
        edu_col.append(P(e, edu_style, bullet="\u2022"))
    str_col = [SectionTitle("Key Strengths"), Spacer(1, 3)]
    for title, desc in STRENGTHS:
        txt = f'<b><font color="#0e2c4c">{title}.</font></b>  {desc}'
        str_col.append(P(txt, str_style, bullet="\u25aa"))
    two_col = Table([[edu_col, str_col]], colWidths=[FW * 0.42, FW * 0.58])
    two_col.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 14),
        ("LEFTPADDING", (1, 0), (1, 0), 0),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(two_col)

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
