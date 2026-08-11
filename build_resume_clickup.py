#!/usr/bin/env python3
"""Generate a visually dynamic resume PDF for Eugene L. Buchanan
   targeted at ClickUp — Staff AI Engineer, Multi-Agent Frameworks.
   Uses reportlab with gradient header, skill bars, tag clouds, and
   experience cards.  Re-uses the design system from build_resume.py.
"""

import os
import tempfile
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer,
                                NextPageTemplate, KeepTogether, Flowable)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.spider import SpiderChart
from reportlab.graphics import renderPDF

import reportlab.rl_config as _rl_config
_rl_config.documentLang = "en-US"   # PDF /Lang catalog entry (a11y + l10n)

# ----------------------------------------------------------------------------
# Fonts (DejaVuSans for clean modern sans-serif)
# ----------------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/TTF"
pdfmetrics.registerFont(TTFont("DJ", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJ-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DJ-I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ-I", boldItalic="DJ-B")

# ----------------------------------------------------------------------------
# Palette  — ClickUp-ish (deep navy + vibrant purple/pink gradient)
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
        # gradient background (purple top → navy bottom, ClickUp vibe)
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
        # title — targeted at ClickUp
        c.setFillColor(colors.HexColor("#e0cfff"))
        c.setFont(FONT, 11)
        c.drawString(28, H - 64, "Staff AI Engineer  \u2014  Multi-Agent Frameworks & Agentic Infrastructure")
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
        self.height = 21
        self.c1 = color1
        self.c2 = color2

    def wrap(self, a, h):
        self.width = a
        return (a, self.height)

    def draw(self):
        c = self.canv
        H = self.height
        c.setFont(FONT_B, 8.8); c.setFillColor(DARK)
        c.drawString(0, H - 11, self.label)
        c.setFont(FONT, 8.8); c.setFillColor(self.c1)
        c.drawRightString(self.width, H - 11, f"{self.pct}%")
        bx, by, bh = 0, 2, 5.5
        bw = self.width
        c.setFillColor(TRACK); c.roundRect(bx, by, bw, bh, 2.5, fill=1, stroke=0)
        fw = max(bw * self.pct / 100.0, 6)
        draw_gradient(c, bx, by, fw, bh, self.c1, self.c2, vertical=False, steps=24)
        c.setFillColor(self.c1); c.roundRect(bx, by, fw, bh, 2.5, fill=1, stroke=0)


class TagCloud(Flowable):
    def __init__(self, tags, width=FW, size=8.3, padx=7, pady=3, gap=4,
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
    def __init__(self, labels, values, width=215, height=200):
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
        s.y = 20
        s.width = 140
        s.height = 145
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
str_style = ParagraphStyle("str", fontName=FONT, fontSize=8.2, leading=10.0,
                           leftIndent=12, bulletIndent=0, bulletColor=PURPLE,
                           spaceAfter=1.5, textColor=INK)
edu_style = ParagraphStyle("edu", fontName=FONT, fontSize=8.2, leading=11.0,
                           leftIndent=12, bulletIndent=1, bulletColor=PURPLE,
                           spaceAfter=2, textColor=INK)
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
        ("LINEBEFORE", (0, 0), (0, -1), 3, PURPLE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 12),
        ("RIGHTPADDING", (0, 0), (0, 0), 6),
        ("TOPPADDING", (0, 0), (0, 0), 2),
        ("BOTTOMPADDING", (0, 0), (0, 0), 2),
    ]))
    return [card, Spacer(1, 3)]

# ----------------------------------------------------------------------------
# Content — targeted at ClickUp Staff AI Engineer, Multi-Agent Frameworks
# ----------------------------------------------------------------------------
SUMMARY = ("Staff AI engineer with 27 years in software and systems, focused on agentic AI "
           "infrastructure and multi-agent orchestration. I've shipped three production PRs to "
           "ZeroClaw (32.2k\u2605 Rust gateway): a merged context-window meter for 9 LLM providers, "
           "a live provider-identity PR for usage events (cost attribution), and an agent "
           "lifecycle observer over JSON-RPC. I've built test automation, integration platforms, "
           "and CI/CD pipelines on AWS/Postgres/React. I focus on automatic model routing and "
           "platforms that deploy intelligent agents at scale.")

EXPERIENCE = [
    ("Staff AI Engineer / Agentic Infrastructure Contributor (Open-Source)",
     "ZeroClaw Labs (github.com/zeroclaw-labs/zeroclaw)  \u00b7  Rust  \u00b7  32.2k stars",
     "2026 \u2013 Present", [
        "PR #7946 (MERGED) \u2014 context-window meter bar across TUI/gateway/CLI "
        "(+1,109 / -22, 25 files). One context_window source of truth for 9 providers; auto-populated "
        "config, doctor command, gateway API, live ContextBar. Removed drift between surfaces \u2014 "
        "directly relevant to Brain2's automatic model routing.",
        "PR #8966 (OPEN) \u2014 carry live provider identity on usage events (+2,742 / -141, 20 files). "
        "Fixed frozen 32k meter on 1M-token models; separated trim budget from model capacity; "
        "unconditional Usage events with serving-provider identity; per-provider usage breakdown on done frame \u2014 "
        "cost-attribution infra for multi-LLM orchestration.",
        "PR #8337 (OPEN) \u2014 herdr agent reporting integration (+1,712 / -17, 13 files). "
        "Observer reports agent lifecycle (idle/working/blocked/released) via JSON-RPC over UDS. "
        "Zero-config env detection, approval-gate blocked state, crash recovery via pane.release_agent. "
        "Multi-agent coordination infrastructure; maps to Super Agents' human-agent collaboration.",
     ]),
    ("Senior Software Engineer / QA Lead / Integrations Product Owner",
     "Knowledgecity LLC  \u00b7  Remote  \u00b7  AWS / Postgres / React",
     "Dec 2020 \u2013 Aug 2025", [
        "Product Owner, Integrations: shipped SAP, Oracle, Workday, Coursera, UKG, and Zoom integrations "
        "via SAML, OAuth, SFTP, and custom REST APIs \u2014 orchestrating multiple services with different "
        "auth models, data formats, and error semantics. Same coordination challenge as multi-agent systems.",
        "Built and maintained CI/CD quality pipelines with Cypress, Selenium, Postman, JUnit, Elastic, S3 \u2014 "
        "an evaluation framework for testing complex deployment scenarios across integration, backend, API, "
        "database, and frontend surfaces.",
        "Applied AI prompt engineering and shipped LLM-powered chatbot tooling in production, "
        "integrating it into customer-facing assistance and internal automation workflows.",
        "Designed evaluation frameworks, regression suites, health dashboards, and alerting "
        "to measure system-level dynamics across multi-environment deployments.",
        "Mentored and trained the test automation team; ran code reviews; raised engineering standards.",
     ]),
    ("Senior Software Engineer II / Presales Engineering",
     "RealNetworks  \u00b7  Seattle, WA  \u00b7  Streaming Media Platform",
     "1999 \u2013 2001", [
        "QA on an advanced research team evaluating distributed system behavior across consumer "
        "appliances, mobile platforms, stream servers, and cellular networks \u2014 complex, multi-component scenarios.",
        "Global presales engineering: turned product capabilities into customer solutions "
        "across diverse technical environments. Trained new hires; led cross-functional collaboration.",
     ]),
    ("Senior Software Test Engineer IV",
     "Microsoft  \u00b7  Redmond, WA  \u00b7  Windows Media Server",
     "1997 \u2013 1999", [
        "White-box testing and automation for Windows Media Server, Windows 98/NT \u2014 evaluation frameworks for complex system testing.",
        "Deep debugging across server infrastructure, network protocols, and media codecs.",
     ]),
    # (IBM 1998 omitted \u2014 single bullet, same reliability mindset covered in Microsoft role)
]

SKILLS = [
    ("Multi-Agent Frameworks & Orchestration", 88),
    ("LLM Integration & Multi-Model Routing", 90),
    ("Agent Lifecycle & Observability", 92),
    ("Evaluation Frameworks & Testing", 92),
    ("Backend Engineering (Rust, Python, Node)", 90),
    ("Context Window & Cost Attribution", 87),
    ("Search Integration (Elastic, Postgres)", 85),
    ("AI Privacy, Auth & Data Protection", 82),
]

TAGS = [
    "Rust", "Python", "TypeScript", "Node.js", "React", "LangGraph",
    "Multi-Agent Systems", "Agent Orchestration", "LLM Integration",
    "JSON-RPC", "Unix Domain Sockets", "MCP (Model Context Protocol)",
    "Context Window Routing", "Multi-Model Cost Attribution",
    "OpenAI / Anthropic / Cohere / Gemini",
    "PostgreSQL", "AWS (ECS, S3)", "Elasticsearch", "GraphQL", "REST APIs",
    "SAML", "OAuth", "OIDC", "SFTP", "CI/CD", "Cypress", "Selenium",
    "JUnit", "Postman", "Evaluation Frameworks", "Code Review",
    "Mentoring", "Git", "Docker",
]

STRENGTHS = [
    ("Multi-agent orchestration",
     "Agent lifecycle observer (PR #8337) + MCP server in 32k-star Rust gateway \u2014 shipped, not demoed."),
    ("Multi-model routing & cost",
     "Merged context-window meter for 9 LLMs (PR #7946); open PR adds live provider identity on usage events (PR #8966)."),
    ("Evaluation frameworks",
     "27 years test automation, regression suites, quality pipelines for complex distributed systems."),
    ("LLM integration",
     "Prompt engineering + chatbot tooling in production; orchestrates multiple providers daily."),
    ("Cross-functional collaboration",
     "Product Owner, QA Lead, presales engineer \u2014 works with PMs, designers, and engineers."),
]

EDUCATION = [
    "Associate Degree, Victor Valley College",
    "California Notary Commission",
    "Toastmasters International",
]

TAG_SECTIONS = [
    ("Multi-Agent & Orchestration", [
        "LangGraph", "Multi-Agent Coordination", "Agent Lifecycle", "JSON-RPC",
        "Bounded I/O", "Fire-and-Forget", "Unix Domain Sockets",
    ]),
    ("LLM, Multi-Model & MCP", [
        "Context Window Routing", "Multi-Model Cost Attribution",
        "MCP (Model Context Protocol)", "herdr-mcp Server",
        "External Tool Access", "Prompt Engineering",
        "OpenAI", "Anthropic", "Cohere", "Gemini",
    ]),
    ("Backend & Platform", [
        "Rust", "Python", "Node.js", "PostgreSQL", "AWS (ECS, S3)",
        "REST", "GraphQL", "Docker", "Git",
    ]),
    ("Evaluation & Testing", [
        "Cypress", "Selenium", "JUnit", "Postman", "Elasticsearch",
        "Regression Suites", "Health Dashboards", "Alerting",
    ]),
    ("Auth & Privacy", [
        "SAML", "OAuth", "OIDC", "Permission Profiles",
        "Principal Isolation", "Deny-by-Default",
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
        "Eugene L. Buchanan  \u00b7  Staff AI Engineer \u2014 Multi-Agent Frameworks")
    canvas.drawRightString(PW - MR, 24, "Page %d" % doc.page)
    canvas.restoreState()


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "ClickUp_Eugene_Buchanan_Resume.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP, bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Staff AI Engineer Resume",
                          author="Eugene L. Buchanan",
                          subject="Staff AI Engineer \u2014 Multi-Agent Frameworks & Agentic AI Infrastructure (Apple Valley, CA)",
                          keywords="Staff AI Engineer, Multi-Agent, LangGraph, LLM, Rust, Agent Orchestration, ClickUp")
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
        ["Multi-Agent\nCoordination", "Multiple\nLLMs", "LangGraph\nOrchestration",
         "Evaluation\nFrameworks", "AI\nPrivacy", "Search &\nBackend"],
        [90, 88, 94, 92, 84, 86])]
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
        story.append(Spacer(1, 1))
    story.append(Spacer(1, 1))

    # ── Experience ────────────────────────────────────────────────────
    story.append(SectionTitle("Experience"))
    story.append(Spacer(1, 1))
    for role, cl, dates, bullets in EXPERIENCE:
        story.extend(experience_card(role, cl, dates, bullets))
    story.append(Spacer(1, 1))

    # ── Education + Key Strengths (stacked) ───────────────────────
    edu_col = [SectionTitle("Education"), Spacer(1, 1)]
    for e in EDUCATION:
        edu_col.append(P(e, edu_style, bullet="\u2022"))
    str_col = [SectionTitle("Key Strengths"), Spacer(1, 1)]
    for title, desc in STRENGTHS:
        txt = f'<b><font color="#2b1d63">{title}.</font></b>  {desc}'
        str_col.append(P(txt, str_style, bullet="\u25aa"))
    # Stack vertically instead of side-by-side to save width and avoid overflow
    for item in edu_col + [Spacer(1, 1)] + str_col:
        story.append(item)

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
