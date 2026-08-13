#!/usr/bin/env python3
"""Generate a visually dynamic Cyber Security Specialist resume PDF
   for Eugene L. Buchanan using reportlab.
   Design system shared with build_resume_clickup.py — dark header,
   gradient accents, skill bars, tag clouds, experience cards.
   Color scheme: deep navy + red/crimson accents for security theme.
"""

import os
import tempfile
from PIL import Image, ImageDraw
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

# ── Fonts ──────────────────────────────────────────────────────────────────
FONT_DIR = "/usr/share/fonts/TTF"
pdfmetrics.registerFont(TTFont("DJ", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJ-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFontFont("DJ", normal="DJ", bold="DJ-B", italic="DJ", boldItalic="DJ-B")

# ── Palette (dark + crimson security) ──────────────────────────────────────
DARK_BG = colors.HexColor("#0d0d1a")
NAVY    = colors.HexColor("#1a1a2e")
CRIMSON = colors.HexColor("#c41e3a")
CRIM_D  = colors.HexColor("#8b0000")
RED2    = colors.HexColor("#e63946")
GOLD    = colors.HexColor("#d4a017")
LIGHT   = colors.HexColor("#fbe9ec")
GREY    = colors.HexColor("#5b6b7b")
DARK    = colors.HexColor("#16202b")
INK     = colors.HexColor("#2b3640")
MUTE    = colors.HexColor("#8a98a6")
RULE    = colors.HexColor("#d4dce4")
TRACK   = colors.HexColor("#e3e9ef")

FONT    = "DJ"
FONT_B  = "DJ-B"

# ── Page geometry ──────────────────────────────────────────────────────────
PW, PH = letter
ML = MR = 40
HEADER_H = 120
TOP_GAP = 8
BODY_BOTTOM = 40
FW = PW - ML - MR
BODY_W = FW

# ── Helpers ────────────────────────────────────────────────────────────────
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

def draw_gradient(c, x, y, w, h, c1, c2, vertical=True, steps=48):
    for i in range(steps):
        t = i / (steps - 1)
        r = c1.red + (c2.red - c1.red) * t
        g = c1.green + (c2.green - c1.green) * t
        b = c1.blue + (c2.blue - c1.blue) * t
        c.setFillColor(colors.Color(r, g, b))
        if vertical:
            c.rect(x, y + h * (i / steps), w, h / steps + 1, stroke=0, fill=1)
        else:
            c.rect(x + w * (i / steps), y, w / steps + 1, h, stroke=0, fill=1)

# ── Flowables ──────────────────────────────────────────────────────────────
class HeaderBand(Flowable):
    def __init__(self, width=PW, height=HEADER_H, photo=None):
        super().__init__()
        self.width, self.height, self.photo = width, height, photo

    def _draw_monogram(self, c, pcx, pcy, pr):
        c.setFillColor(NAVY)
        c.rect(pcx - pr, pcy - pr, 2*pr, 2*pr, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_B, 22)
        c.drawCentredString(pcx, pcy - 8, "EB")

    def draw(self):
        c, W, H = self.canv, self.width, self.height
        draw_gradient(c, 0, 0, W, H, CRIM_D, DARK_BG, vertical=True)
        draw_gradient(c, 0, 0, 6, H, CRIMSON, GOLD, vertical=True, steps=24)
        pcx, pcy, pr = W - 42, H - 40, 30
        if self.photo and os.path.exists(self.photo):
            try:
                c.drawImage(self.photo, pcx - pr, pcy - pr, 2*pr, 2*pr,
                           preserveAspectRatio=True, anchor="c", mask="auto")
            except Exception:
                self._draw_monogram(c, pcx, pcy, pr)
        else:
            self._draw_monogram(c, pcx, pcy, pr)
        c.setStrokeColor(colors.white); c.setLineWidth(1.5)
        c.circle(pcx, pcy, pr, fill=0, stroke=1)
        c.setFillColor(colors.white); c.setFont(FONT_B, 24)
        c.drawString(28, H - 44, "EUGENE L. BUCHANAN")
        c.setFillColor(colors.HexColor("#ffaabb")); c.setFont(FONT, 11)
        c.drawString(28, H - 64, "Cyber Security Specialist  \u2014  AI Security Automation & Compliance")
        c.setStrokeColor(colors.white); c.setFillAlpha(0.22); c.setLineWidth(0.5)
        c.line(28, H - 74, pcx - pr - 10, H - 74); c.setFillAlpha(1)
        items = [("L", "San Quint\u00edn, BC MX (Remote)", None),
                 ("T", "+1 (909) 545 5384", None),
                 ("E", "eugene@serviceofothers.org", "mailto:eugene@serviceofothers.org"),
                 ("G", "github.com/eugeneb50", "https://github.com/eugeneb50")]
        x, cy = 28, H - 88
        links = []
        for letter, txt, url in items:
            c.setFillColor(colors.white); c.setFillAlpha(0.20)
            c.circle(x + 7, cy + 4, 7, fill=1, stroke=0); c.setFillAlpha(1)
            c.setFillColor(colors.white); c.setFont(FONT_B, 7.5)
            c.drawCentredString(x + 7, cy + 1, letter)
            c.setFillColor(colors.HexColor("#eaeafa")); c.setFont(FONT, 7.5)
            c.drawString(x + 17, cy - 1, txt)
            tw = pdfmetrics.stringWidth(txt, FONT, 7.5)
            if url: links.append((url, x + 17, cy - 4, x + 17 + tw, cy + 10))
            x += 17 + tw + 12
        for url, x1, y1, x2, y2 in links:
            c.linkURL(url, (x1, y1, x2, y2), relative=1)


class SectionTitle(Flowable):
    def __init__(self, text, width=FW, accent=CRIMSON):
        super().__init__()
        self.text, self.width, self.height, self.accent = text, width, 22, accent

    def wrap(self, a, h):
        self.width = a
        return (a, self.height)

    def draw(self):
        c, H = self.canv, self.height
        c.setFillColor(self.accent)
        c.rect(0, H - 14, 5, 14, fill=1, stroke=0)
        c.setFont(FONT_B, 12); c.setFillColor(DARK)
        c.drawString(14, H - 13, self.text)
        tw = pdfmetrics.stringWidth(self.text, FONT_B, 12)
        c.setStrokeColor(RULE); c.setLineWidth(0.8)
        c.line(14 + tw + 10, H / 2, self.width, H / 2)


class SkillBar(Flowable):
    def __init__(self, label, pct, width=FW, c1=CRIMSON, c2=GOLD):
        super().__init__()
        self.label, self.pct, self.width = label, pct, width
        self.height = 19; self.c1, self.c2 = c1, c2

    def wrap(self, a, h):
        self.width = a
        return (a, self.height)

    def draw(self):
        c, H = self.canv, self.height
        c.setFont(FONT_B, 8.5); c.setFillColor(DARK)
        c.drawString(0, H - 10, self.label)
        c.setFont(FONT, 8.5); c.setFillColor(self.c1)
        c.drawRightString(self.width, H - 10, f"{self.pct}%")
        bw, by, bh = self.width, 2, 5
        c.setFillColor(TRACK)
        c.roundRect(0, by, bw, bh, 2.5, fill=1, stroke=0)
        fw = max(bw * self.pct / 100.0, 6)
        draw_gradient(c, 0, by, fw, bh, self.c1, self.c2, vertical=False, steps=24)


class TagCloud(Flowable):
    def __init__(self, tags, width=FW, size=8.2, padx=7, pady=4, gap=6,
                 bg=LIGHT, fg=CRIM_D):
        super().__init__()
        self.tags, self.size = tags, size
        self.padx, self.pady, self.gap = padx, pady, gap
        self.bg, self.fg = bg, fg
        self.width = width
        self.lh = size + 2 * pady + 4

    def wrap(self, a, h):
        self.width = a
        self.lines, x, cur = [], 0, []
        for t in self.tags:
            w = pdfmetrics.stringWidth(t, FONT, self.size) + 2 * self.padx
            if x > 0 and x + w > a:
                self.lines.append(cur); cur = []; x = 0
            cur.append((t, w)); x += w + self.gap
        if cur: self.lines.append(cur)
        self.height = len(self.lines) * self.lh + max(len(self.lines) - 1, 0) * self.gap
        return (a, self.height)

    def draw(self):
        c = self.canv
        y = self.height - self.lh
        for items in self.lines:
            x = 0
            for t, w in items:
                c.setFillColor(self.bg)
                c.roundRect(x, y, w, self.lh - 4, 4, fill=1, stroke=0)
                c.setFillColor(self.fg)
                c.setFont(FONT, self.size)
                c.drawString(x + self.padx, y + (self.lh - 4 - self.size) / 2, t)
                x += w + self.gap
            y -= self.lh + self.gap


# ── Styles ─────────────────────────────────────────────────────────────────
summary_style = ParagraphStyle("sum", fontName=FONT, fontSize=9.2, leading=12.5,
                               textColor=INK, alignment=TA_JUSTIFY)
role_style = ParagraphStyle("role", fontName=FONT_B, fontSize=10.5, leading=13,
                            textColor=DARK, spaceAfter=0)
date_style = ParagraphStyle("date", fontName=FONT, fontSize=8.4, leading=11,
                            textColor=GREY, alignment=2)
sub_style = ParagraphStyle("sub", fontName=FONT, fontSize=8.8, leading=11,
                           textColor=CRIMSON, spaceAfter=2)
bullet_style = ParagraphStyle("bul", fontName=FONT, fontSize=8.5, leading=11,
                              leftIndent=12, bulletIndent=1, bulletColor=CRIMSON,
                              spaceAfter=1.5, textColor=INK)
str_style = ParagraphStyle("str", fontName=FONT, fontSize=8.5, leading=10.5,
                           leftIndent=12, bulletIndent=0, bulletColor=CRIMSON,
                           spaceAfter=1.5, textColor=INK)
edu_style = ParagraphStyle("edu", fontName=FONT, fontSize=8.5, leading=11,
                           leftIndent=12, bulletIndent=1, bulletColor=CRIMSON,
                           spaceAfter=2, textColor=INK)


def P(text, style, bullet=None):
    return Paragraph(text, style, bulletText=bullet)

def bullet_p(t):
    return P(t, bullet_style, bullet="\u2022")

def experience_card(role, company_loc, dates, bullets):
    meta = Table([[P(role, role_style), P(dates, date_style)]], colWidths=[306, 200])
    meta.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, 0), "RIGHT"), ("VALIGN", (0, 0), (0, 0), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    flow = [meta, P(company_loc, sub_style)]
    for b in bullets: flow.append(bullet_p(b))
    card = Table([[flow]], colWidths=[BODY_W])
    card.setStyle(TableStyle([
        ("LINEBEFORE", (0, 0), (0, -1), 3, CRIMSON),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 12),
        ("RIGHTPADDING", (0, 0), (0, 0), 6),
        ("TOPPADDING", (0, 0), (0, 0), 2),
        ("BOTTOMPADDING", (0, 0), (0, 0), 2),
    ]))
    return [card, Spacer(1, 3)]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONTENT — Cyber Security Specialist
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY = (
    "Cyber security specialist with 27 years of software and systems engineering "
    "experience, now focused on AI-driven security automation, code auditing, and "
    "compliance. Contributed security architecture review (PR #7946, #8966, #8337) to "
    "ZeroClaw (32.2k★ Rust gateway). Deployed AI agents with /bug-reaper skill for "
    "automated vulnerability hunting across 18 CWE classes with evidence-based PoC "
    "validation. Led SOC 2 compliance evidence collection at Knowledgecity. Built "
    "test automation and CI/CD security pipelines on AWS/Postgres/React. Committed to "
    "deny-by-default, principal isolation, and adversarial FP elimination."
)

EXPERIENCE = [
    ("Cyber Security Engineer / AI Security Automation Contributor",
     "ZeroClaw Labs (github.com/zeroclaw-labs/zeroclaw)  \u00b7  Rust  \u00b7  32.2k\u2605",
     "2026 \u2013 Present", [
        "PR #7946 (MERGED) \u2014 feat(runtime): context window visibility across TUI/gateway/CLI "
        "(+1,109/-22, 25 files). Established context_window as single source of truth in provider "
        "config for 9 LLM providers, preventing silent token overflow that could truncate security "
        "audit output. Added doctor command for config integrity verification.",
        "PR #8966 (OPEN) \u2014 feat(agent): live provider identity on usage events (+2,742/-141, 20 files). "
        "Fixed a frozen 32k context-meter stub on 1M-token models that could mask incomplete security "
        "analysis. Separated trim budget from model capacity. Added per-provider usage breakdown for "
        "cost attribution \u2014 critical when routing security scans across multiple LLMs.",
        "PR #8337 (OPEN) \u2014 feat(observability): herdr agent reporting (+1,712/-17, 13 files). "
        "Observer reports agent lifecycle (idle/working/blocked/released) via JSON-RPC over UDS. "
        "Approval-gate events drive blocked state for supervised tool calls \u2014 security audit trail "
        "for agent actions. Zero-config env detection, crash recovery via pane.release_agent.",
        "Built herdr-mcp MCP server (github.com/eugeneb50/herdr-mcp) providing pane control and "
        "inter-agent communication for multi-agent security orchestration over MCP protocol.",
        "Deployed /bug-reaper AI agent skill (github.com/shaniidev/bug-reaper) for automated "
        "vulnerability hunting: 18 CWE classes, 4-phase recon, exploit validation with working PoC, "
        "false-positive elimination, CVSS scoring, WAF bypass (15 products), bug chaining (P3\u2192P1). "
        "Targets HackerOne, Bugcrowd, Intigriti, YesWeHack triage standards.",
     ]),

    ("Senior QA Engineer / Test Automation Lead / SOC 2 Compliance Lead",
     "Knowledgecity LLC  \u00b7  Remote  \u00b7  AWS / Postgres / React",
     "Dec 2020 \u2013 Aug 2025", [
        "SOC 2 Type II compliance: collected and organized evidence for security audits across "
        "access controls (SAML/SSO), data encryption, network security, change management, and "
        "incident response. Mapped CI/CD pipeline controls to SOC 2 trust service criteria "
        "(CC1\u2013CC7). Worked with auditors to verify control effectiveness.",
        "Security testing across integration surfaces: SAML/OAuth/SFTP authentication, REST API "
        "payload validation, SQL injection prevention, XSS/CSRF verification, and data exposure "
        "audits for integrations with SAP, Oracle, Workday, UKG, Coursera, Zoom.",
        "Built CI/CD security pipeline with Cypress, Selenium, Postman, JUnit, Elastic, S3 \u2014 "
        "automated regression suites, health dashboards, alert systems covering security, "
        "performance, and API integrity across multi-environment deployments.",
        "Applied AI prompt engineering and chatbot security: validated LLM-powered tooling for "
        "prompt injection resistance, data leakage prevention, and access boundary enforcement.",
        "Conducted code reviews and security audits across integration, backend, API, database, "
        "and frontend surfaces. Reduced technical debt and security vulnerabilities.",
        "Mentored and trained test automation team in security testing best practices.",
     ]),

    ("Senior Software Test Engineer IV",
     "Microsoft  \u00b7  Redmond, WA  \u00b7  Windows Media Server",
     "1997 \u2013 1999", [
        "White-box testing and security analysis for Windows Media Server, Windows 98/NT \u2014 "
        "building evaluation frameworks for complex system-level security testing.",
        "Deep debugging across server infrastructure, network protocols, and media codecs \u2014 "
        "identifying attack surfaces and verifying access controls.",
     ]),

    ("Senior Software Engineer II / QA & Security Research",
     "RealNetworks  \u00b7  Seattle, WA  \u00b7  Streaming Media Platform",
     "1999 \u2013 2001", [
        "QA on advanced research team evaluating consumer appliances, mobile platforms, stream "
        "servers, and cellular networks \u2014 vulnerability assessment across distributed systems.",
        "Global presales engineering: security architecture review for enterprise deployments.",
     ]),
]

SKILLS = [
    ("Security Auditing & Code Review", 92),
    ("AI Agent Security Automation (/bug-reaper)", 88),
    ("SOC 2 / Compliance Evidence Collection", 85),
    ("Vulnerability Assessment (18 CWE Classes)", 87),
    ("Auth Security (SAML, OAuth, OIDC, SSH)", 88),
    ("CI/CD Security Pipelines", 90),
    ("Pen Testing & Exploit Validation", 82),
    ("Rust / Python / Backend Security", 88),
]

TAG_SECTIONS = [
    ["SOC 2", "ISO 27001", "Compliance Evidence", "Trust Service Criteria",
     "Change Management", "Access Controls", "Incident Response"],
    ["Bug-Reaper", "AI Vulnerability Hunting", "PoC Validation",
     "CVSS Scoring", "WAF Bypass", "Bug Chaining", "Recon Methodology"],
    ["SAML", "OAuth", "OIDC", "SSH Challenge-Response", "Peercred",
     "Deny-by-Default", "Principal Isolation"],
    ["SQL Injection", "XSS", "CSRF", "SSRF", "IDOR", "RCE",
     "Auth Bypass", "Data Exposure", "API Security"],
    ["Rust", "Python", "PostgreSQL", "AWS (ECS, S3)", "Elasticsearch",
     "JSON-RPC", "MCP Protocol", "REST APIs", "Docker", "Git"],
]

STRENGTHS = [
    ("AI-driven security automation",
     "Deployed /bug-reaper agent skill for 18 CWE classes with PoC validation, targeting HackerOne/Bugcrowd triage standards."),
    ("Compliance evidence",
     "Led SOC 2 Type II evidence collection at Knowledgecity \u2014 mapped CI/CD controls to CC1\u2013CC7 trust criteria."),
    ("Security architecture review",
     "Reviewed 2,742-line provider identity PR and 1,712-line observability PR for ZeroClaw \u2014 deny-by-default, isolation, audit trails."),
    ("Auth security",
     "Tested SAML/OAuth/SFTP auth across 6 enterprise integrations; reviewed SSH challenge-response and OIDC for ZeroClaw."),
    ("27 years systems engineering",
     "Microsoft, IBM, RealNetworks \u2014 deep debugging across protocols, infrastructure, and access controls."),
    ("Mentoring & training",
     "Trained test automation team in security testing best practices; conducted code reviews and security audits."),
]

EDUCATION = [
    "Associate Degree, Victor Valley College",
    "California Notary Commission (Background-Checked, Bonded)",
    "Toastmasters International",
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Build
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE); canvas.setLineWidth(0.6)
    canvas.line(ML, 34, PW - MR, 34)
    canvas.setFont(FONT, 7.5); canvas.setFillColor(MUTE)
    canvas.drawString(ML, 24, "Eugene L. Buchanan  \u00b7  Cyber Security Specialist")
    canvas.drawRightString(PW - MR, 24, "Page %d" % doc.page)
    canvas.restoreState()


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "CyberSec_Eugene_Buchanan_Resume.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP, bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Cyber Security Specialist Resume",
                          author="Eugene L. Buchanan")
    header_frame = Frame(0, PH - HEADER_H, PW, HEADER_H, leftPadding=0,
                         rightPadding=0, topPadding=0, bottomPadding=0, id="hdr")
    cover_body = Frame(ML, BODY_BOTTOM, FW, (PH - HEADER_H - TOP_GAP) - BODY_BOTTOM,
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="cbody")
    content_body = Frame(ML, BODY_BOTTOM, FW, PH - BODY_BOTTOM - BODY_BOTTOM,
                         leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="body")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[header_frame, cover_body], onPage=footer),
        PageTemplate(id="content", frames=[content_body], onPage=footer),
    ])

    story = []
    photo_path = make_circular_photo(os.path.join(out_dir, "pic.jpg"))
    story.append(HeaderBand(photo=photo_path))
    story.append(NextPageTemplate("content"))
    story.append(Spacer(1, 4))

    # Summary
    story.append(SectionTitle("Professional Summary"))
    story.append(Spacer(1, 1))
    story.append(P(SUMMARY, summary_style))
    story.append(Spacer(1, 3))

    # Skills
    story.append(SectionTitle("Security Expertise"))
    story.append(Spacer(1, 1))
    for label, pct in SKILLS:
        story.append(SkillBar(label, pct))
    story.append(Spacer(1, 3))

    # Tag clouds
    story.append(SectionTitle("Security Domains & Tooling"))
    story.append(Spacer(1, 1))
    for tags in TAG_SECTIONS:
        story.append(TagCloud(tags))
        story.append(Spacer(1, 1))
    story.append(Spacer(1, 2))

    # Experience
    story.append(SectionTitle("Experience"))
    story.append(Spacer(1, 1))
    for role, cl, dates, bullets in EXPERIENCE:
        story.extend(experience_card(role, cl, dates, bullets))
    story.append(Spacer(1, 2))

    # Education
    edu_col = [SectionTitle("Education"), Spacer(1, 1)]
    for e in EDUCATION:
        edu_col.append(P(e, edu_style, bullet="\u2022"))
    # Strengths
    str_col = [SectionTitle("Key Strengths"), Spacer(1, 1)]
    for title, desc in STRENGTHS:
        txt = f'<b><font color="#8b0000">{title}.</font></b>  {desc}'
        str_col.append(P(txt, str_style, bullet="\u25aa"))
    for item in edu_col + [Spacer(1, 2)] + str_col:
        story.append(item)

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build()
