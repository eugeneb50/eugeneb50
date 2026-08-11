#!/usr/bin/env python3
"""Generate a visually dynamic cover letter PDF for Eugene L. Buchanan using reportlab."""

import os
import tempfile
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer, Flowable)
from reportlab.pdfgen import canvas as canvas_mod

# ----------------------------------------------------------------------------
# Fonts (DejaVuSans for clean modern sans-serif)
# ----------------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DJ", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJ-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ", boldItalic="DJ-B")

# ----------------------------------------------------------------------------
# Palette (Consistent branding with Resume!)
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

FONT    = "DJ"
FONT_B  = "DJ-B"

# ----------------------------------------------------------------------------
# Page geometry (tighter to fit exactly 1 page with diagram)
# ----------------------------------------------------------------------------
PW, PH = letter                 # 612 x 792
ML = MR = 40
HEADER_H = 92
TOP_GAP = 8
BODY_BOTTOM = 35

FW = PW - ML - MR              # frame width = 532

# ----------------------------------------------------------------------------
# Circular profile photo helper
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
# Header Band Flowable
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
        c.setFont(FONT_B, 18)
        c.drawCentredString(pcx, pcy - 6, "EB")

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        draw_gradient(c, 0, 0, W, H, TEAL_D, NAVY, vertical=True)

        # profile photo (or monogram fallback)
        pcx, pcy, pr = W - 40, H - 46, 22
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
        c.setFont(FONT_B, 18)
        c.drawString(28, H - 32, "EUGENE L. BUCHANAN")
        # title
        c.setFillColor(colors.HexColor("#bfe9e4"))
        c.setFont(FONT, 9.5)
        c.drawString(28, H - 48, "Staff AI Engineer  \u2014  Agentic Systems & Multi-Agent Frameworks")
        # separator
        c.setStrokeColor(colors.white); c.setFillAlpha(0.22); c.setLineWidth(0.6)
        c.line(28, H - 58, pcx - pr - 12, H - 58); c.setFillAlpha(1)
        # contact strip
        items = [("L", "Apple Valley, CA", None),
                 ("T", "+1 (909) 545 5384", None),
                 ("M", "eugene@serviceofothers.org", "mailto:eugene@serviceofothers.org"),
                 ("G", "github.com/eugeneb50", "https://github.com/eugeneb50")]
        x = 28
        cy = H - 74
        link_rects = []
        for letter, txt, url in items:
            c.setFillColor(colors.white); c.setFillAlpha(0.20)
            c.circle(x + 5, cy + 3, 5.5, fill=1, stroke=0); c.setFillAlpha(1)
            c.setFillColor(colors.white); c.setFont(FONT_B, 6)
            c.drawCentredString(x + 5, cy + 1, letter)
            c.setFillColor(colors.HexColor("#eaf6f4")); c.setFont(FONT, 7.5)
            c.drawString(x + 13, cy, txt)
            tw = pdfmetrics.stringWidth(txt, FONT, 7.5)
            if url:
                link_rects.append((url, x + 13, cy - 2, x + 13 + tw, cy + 10))
            x += 13 + tw + 10
        for url, x1, y1, x2, y2 in link_rects:
            c.linkURL(url, (x1, y1, x2, y2), relative=1)

# ----------------------------------------------------------------------------
# Custom Flowable: Visually Stunning Skills Matching & ELT Data Diagram
# ----------------------------------------------------------------------------
class ELTFlowDiagram(Flowable):
    def __init__(self, width=FW, height=110):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, a, h):
        self.width = a
        return (a, self.height)

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        
        # Soft background container with subtle border
        c.setFillColor(colors.HexColor('#f8fafc'))
        c.setStrokeColor(colors.HexColor('#e2e8f0'))
        c.setLineWidth(0.8)
        c.roundRect(0, 0, W, H, 6, fill=1, stroke=1)
        
        box_w = 145
        box_h = 80
        box_y = 15
        
        # Draw 3 boxes representing ELT Pipeline & Skills Mapping
        c.setFillColor(colors.HexColor('#1e293b')) # Slate Navy - EXTRACT
        c.roundRect(24, box_y, box_w, box_h, 4, fill=1, stroke=0)
        
        c.setFillColor(colors.HexColor('#0e7c75')) # Deep Teal - TRANSFORM
        c.roundRect(193, box_y, box_w, box_h, 4, fill=1, stroke=0)
        
        c.setFillColor(colors.HexColor('#15a39a')) # Vibrant Teal - LOAD
        c.roundRect(362, box_y, box_w, box_h, 4, fill=1, stroke=0)
        
        # Connecting lines
        c.setStrokeColor(colors.HexColor('#0ea5e9')) # Accent blue
        c.setLineWidth(1.5)
        c.line(169, 55, 193, 55)
        c.line(338, 55, 362, 55)
        
        # Arrow heads
        c.setFillColor(colors.HexColor('#0ea5e9'))
        p1 = c.beginPath()
        p1.moveTo(193, 55)
        p1.lineTo(187, 51)
        p1.lineTo(187, 59)
        p1.close()
        c.drawPath(p1, fill=1, stroke=1)
        
        p2 = c.beginPath()
        p2.moveTo(362, 55)
        p2.lineTo(356, 51)
        p2.lineTo(356, 59)
        p2.close()
        c.drawPath(p2, fill=1, stroke=1)
        
        # Text Styles
        style_t = ParagraphStyle('t', fontName='DJ-B', fontSize=7.2, leading=9.5, textColor=colors.white)
        style_b = ParagraphStyle('b', fontName='DJ', fontSize=6.2, leading=8.2, textColor=colors.white)
        
        # Box 1 (EXTRACT) Content
        p_t1 = Paragraph('1. EXTRACT (Telemetry/Metrics)', style_t)
        p_t1.wrap(135, 11)
        p_t1.drawOn(c, 29, 78)
        p_b1 = Paragraph('• <i>sysinfo</i> CPU/RAM profiles<br/>• LLM token/latency logs<br/>• herdr multiplexer event logs<br/>• DB query metrics', style_b)
        p_b1.wrap(135, 55)
        p_b1.drawOn(c, 29, 20)
        
        # Box 2 (TRANSFORM) Content
        p_t2 = Paragraph('2. TRANSFORM (Orchestration)', style_t)
        p_t2.wrap(135, 11)
        p_t2.drawOn(c, 198, 78)
        p_b2 = Paragraph('• <b>PR #8966:</b> Context Resolution<br/>• <b>PR #8337:</b> Bounded I/O Sockets<br/>• <b>PR #7946:</b> RAM/CPU Profiler<br/>• herdr-mcp secure sandboxing', style_b)
        p_b2.wrap(135, 55)
        p_b2.drawOn(c, 198, 20)

        # Box 3 (LOAD) Content
        p_t3 = Paragraph('3. LOAD (ClickUp Agent Desk)', style_t)
        p_t3.wrap(135, 11)
        p_t3.drawOn(c, 367, 78)
        p_b3 = Paragraph('• Multi-agent shared context<br/>• Real-time TUI status tracking<br/>• High-reliability integrations<br/>• Automated behavior evaluation', style_b)
        p_b3.wrap(135, 55)
        p_b3.drawOn(c, 367, 20)

# ----------------------------------------------------------------------------
# Styles (Tighter line-heights and spacing for single-page constraint)
# ----------------------------------------------------------------------------
body_style = ParagraphStyle("body", fontName=FONT, fontSize=8.8, leading=11.8,
                            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=4)
meta_style = ParagraphStyle("meta", fontName=FONT, fontSize=8.5, leading=11.0,
                            textColor=DARK, alignment=TA_LEFT, spaceAfter=2)
meta_bold = ParagraphStyle("meta_b", fontName=FONT_B, fontSize=8.5, leading=11.0,
                           textColor=DARK, alignment=TA_LEFT, spaceAfter=2)
subj_style = ParagraphStyle("subj", fontName=FONT_B, fontSize=9.0, leading=12.0,
                            textColor=NAVY, alignment=TA_LEFT, spaceAfter=5)
bullet_style = ParagraphStyle("bullet", fontName=FONT, fontSize=8.6, leading=11.5,
                              leftIndent=11, bulletIndent=2, bulletColor=TEAL,
                              spaceAfter=2.8, textColor=INK)

def P(text, style, bullet=None):
    return Paragraph(text, style, bulletText=bullet)

# ----------------------------------------------------------------------------
# Document assembly
# ----------------------------------------------------------------------------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE); canvas.setLineWidth(0.6)
    canvas.line(ML, 30, PW - MR, 30)
    canvas.setFont(FONT, 7.0); canvas.setFillColor(MUTE)
    canvas.drawString(ML, 20, "Eugene L. Buchanan  \u00b7  Staff AI Engineer  \u00b7  eugene@serviceofothers.org")
    canvas.drawRightString(PW - MR, 20, "Page 1 of 1")
    canvas.restoreState()

def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Cover_Letter.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP, bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Cover Letter",
                          author="Eugene L. Buchanan")

    header_frame = Frame(0, PH - HEADER_H, PW, HEADER_H, leftPadding=0,
                         rightPadding=0, topPadding=0, bottomPadding=0, id="hdr")
    cover_body = Frame(ML, BODY_BOTTOM, FW, (PH - HEADER_H - TOP_GAP) - BODY_BOTTOM,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                        id="cbody")

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[header_frame, cover_body], onPage=footer),
    ])

    story = []
    photo_path = make_circular_photo(os.path.join(out_dir, "pic.jpg"))
    story.append(HeaderBand(photo=photo_path))
    story.append(Spacer(1, 4))

    # Recipient Info & Date
    story.append(P("<b>Date:</b> August 11, 2026", meta_style))
    story.append(P("<b>To:</b>", meta_bold))
    story.append(P("ClickUp Recruiting Team  \u00b7  Mango Technologies, Inc. (ClickUp)  \u00b7  San Diego, CA (Remote, US)", meta_style))
    story.append(Spacer(1, 2))

    # Subject
    story.append(P("<b>SUBJECT: Application for Staff AI Engineer - Multi-Agent Frameworks (JID: 1203026f-5c19-45e5-a0c2-b5cc0338a1e8)</b>", subj_style))

    # Body
    story.append(P("Dear ClickUp Recruiting Team,", meta_bold))
    story.append(Spacer(1, 2))

    p1 = ("I am writing to express my enthusiastic interest in the Staff AI Engineer - Multi-Agent Frameworks "
          "position at ClickUp. Your mission to maximize human productivity fundamentally aligns with my software "
          "engineering philosophy. While other companies scramble to bundle fragmented tools or bolt on AI as an "
          "afterthought, ClickUp is doing it correct—building the world's first truly converged AI workspace "
          "unifying tasks, docs, chat, and search, all supercharged by context-driven AI. Your culture of grit, speed, "
          "and breaking the status quo (especially your core value 'Normal f*cking sucks') is precisely the "
          "high-intensity environment where I excel.")
    story.append(P(p1, body_style))

    p2 = ("As an active contributor to the **ZeroClaw** Rust autonomous AI agent infrastructure and "
          "**herdr** multi-agent multiplexer, I have spent the last several years designing, debugging, "
          "and deploying the exact systems-level patterns ClickUp is leveraging. I specialize in high-performance "
          "LLM orchestration, context-management protocols, and rigorous evaluation frameworks. I am highly confident "
          "in my ability to immediately add value to your AI Platform team.")
    story.append(P(p2, body_style))

    p3 = "Here are several concrete ways my systems engineering work translates to what I can do for ClickUp:"
    story.append(P(p3, body_style))

    b1 = ("<b>Dynamic Context Window Resolution (PR #8966):</b> I designed and implemented live LLM provider identity "
          "propagation on usage events, dynamically resolving the active context window boundaries from the serving provider "
          "at runtime. This guarantees accurate token-use observability and prevents context overflow errors during multi-provider fallback.")
    story.append(P(b1, bullet_style, bullet="\u2022"))

    b2 = ("<b>Robust High-Performance Communication (PR #8337):</b> I engineered a JSON-RPC communication layer "
          "over Unix sockets to bind agent lifecycle events to persistent terminal sessions. By establishing strict "
          "bounded I/O budgets, I resolved memory leaks and prevented loops from hanging during high-frequency "
          "agent executions.")
    story.append(P(b2, bullet_style, bullet="\u2022"))

    b3 = ("<b>System Observability & Safety (PR #7946):</b> I built cross-platform CPU/RAM sampling using the "
          "<i>sysinfo</i> crate in Rust to profile agent resource consumption, alongside a real-time model-context-window "
          "visual status bar in the ZeroCode TUI to proactively prevent context-budget token overflows.")
    story.append(P(b3, bullet_style, bullet="\u2022"))

    b4 = ("<b>QA Automation & AI Evaluation:</b> Leveraging my background as QA Lead at Knowledgecity, where I managed "
          "test automation across 15+ concurrent microservices, I can establish robust, automated verification and "
          "evaluation frameworks to benchmark agent behaviors, security boundaries, and data privacy compliance.")
    story.append(P(b4, bullet_style, bullet="\u2022"))

    # Visually Stunning ELT Data Mapping and Visualization Graph
    story.append(Spacer(1, 2))
    story.append(P("<b>Skills Matching &amp; Agentic ELT Architecture Data Flow:</b>", meta_bold))
    story.append(Spacer(1, 2))
    story.append(ELTFlowDiagram())
    story.append(Spacer(1, 2))

    p4 = ("I am highly fluent in leveraging AI in my daily workflows and have built and deployed tools like the "
          "<i>herdr-mcp</i> server, which exposes CLI controls to LLMs. I am excited about the prospect of applying "
          "my deep systems expertise in Rust, LLM integration, and QA automation to help ClickUp build the "
          "next chapter of collaborative multi-agentic workflows.")
    story.append(P(p4, body_style))

    story.append(Spacer(1, 2))
    story.append(P("Sincerely,", meta_bold))
    story.append(Spacer(1, 3))
    story.append(P("<b>Eugene L. Buchanan</b>", meta_bold))

    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")

if __name__ == "__main__":
    build()
