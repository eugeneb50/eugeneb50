#!/usr/bin/env python3
"""Generate a visually dynamic resume PDF for Eugene L. Buchanan
   targeted at ClickUp — Staff AI Engineer, Multi-Agent Frameworks.
   Uses reportlab with gradient header, skill bars, tag clouds, and
   experience cards.  Re-uses the design system from build_resume.py.
"""

import os
import tempfile
import arabic_reshaper
import segno
from bidi.algorithm import get_display
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfdoc as _pdfdoc
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer, PageBreak,
                                NextPageTemplate, KeepTogether, Flowable,
                                Image as RLImage)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.spider import SpiderChart
from reportlab.graphics import renderPDF

import reportlab.rl_config as _rl_config
_rl_config.documentLang = "en-US"   # PDF /Lang catalog entry (a11y + l10n)

# reportlab's AcroForm appearance streams escape text via a Latin-1 table that
# chokes on Arabic/CJK. We strip those /AP appearances anyway (Acrobat
# regenerates them from /DA), so make escPDF degrade to a '?' placeholder
# instead of raising.
import reportlab.pdfbase.acroform as _acroform
_esc_pdf_orig = _acroform.escPDF
def _esc_pdf_safe(s):
    try:
        return _esc_pdf_orig(s)
    except KeyError:
        return _esc_pdf_orig(s.encode("latin-1", "replace").decode("latin-1"))
_acroform.escPDF = _esc_pdf_safe

# ----------------------------------------------------------------------------
# Fonts (DejaVuSans for clean modern sans-serif)
# ----------------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/TTF"
pdfmetrics.registerFont(TTFont("DJ", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJ-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DJ-I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ-I", boldItalic="DJ-B")

# International fonts for the interactive localization panel.
FONT_AR = "AR-I18N"          # Arabic (RTL) — Noto Sans Arabic
FONT_ZH = "STSong-Light"     # Simplified Chinese   — reportlab CID font
FONT_JA = "HeiseiKakuGo-W5"  # Japanese             — reportlab CID font
pdfmetrics.registerFont(TTFont(FONT_AR, "/usr/share/fonts/noto/NotoSansArabic-Regular.ttf"))
pdfmetrics.registerFont(UnicodeCIDFont(FONT_ZH))
pdfmetrics.registerFont(UnicodeCIDFont(FONT_JA))



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
        self.height = 17
        self.c1 = color1
        self.c2 = color2

    def wrap(self, a, h):
        self.width = a
        return (a, self.height)

    def draw(self):
        c = self.canv
        H = self.height
        c.setFont(FONT_B, 7.6); c.setFillColor(DARK)
        c.drawString(0, H - 10, self.label)
        c.setFont(FONT, 7.6); c.setFillColor(self.c1)
        c.drawRightString(self.width, H - 10, f"{self.pct}%")
        bx, by, bh = 0, 1.5, 5
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
# Interactive localization panel — Key Strengths in 7 languages
# PDF form radio buttons toggle Optional Content (OCG) layers; the active
# layer is tagged with its /Lang so it renders RTL for Arabic and is
# announced by screen readers.
# ----------------------------------------------------------------------------
I18N = [
    # (code, lang-tag, label, font, translations of the 5 STRENGTHS, is_rtl)
    ("en", "en-US", "English", FONT,
     ["Multi-agent orchestration — design and ship multi-agent systems in production with lifecycle observability.",
      "Multi-model routing & cost — unify LLM providers behind one context window with per-model cost attribution.",
      "Evaluation frameworks — build harnesses, regression suites, health dashboards, and alerting.",
      "LLM integration — prompt engineering and chatbot tooling in shipped products and automation.",
      "Cross-functional leadership — lead as Product Owner, QA Lead, and presales engineer."],
     False),
    ("es", "es-ES", "Español", FONT,
     ["Orquestación multiagente — diseño y entrega de sistemas multiagente en producción con control de ciclo de vida.",
      "Enrutamiento multimodelo — unifico proveedores de LLM tras una sola ventana de contexto con costo por modelo.",
      "Marcos de evaluación — construyo bancos de pruebas, suites de regresión, paneles de salud y alertas.",
      "Integración de LLM — ingeniería de prompts y herramientas de chat en productos y automatización en producción.",
      "Liderazgo multifuncional — lidero como Product Owner, QA Lead e ingeniero de preventa."],
     False),
    ("ar", "ar-AE", "العربية", FONT_AR,
     ["تنسيق متعدد الوكلاء — التصميم وتقديم أنظمة متعددة الوكلاء في الإنتاج مع مراقبة طول العمر.",
      "توجيه متعدد النماذج — توحيد مزوّدي النماذج اللغوية خلف نافذة سياق واحدة مع احتساب التكلفة لكل نموذج.",
      "أطر التقييم — بناء منصّات تقييم، ومجموعات انحدار، ولوحات صحية، وتنبيهات تقيس السلوك الفعلي.",
      "تكامل نُماذج اللغة — هندسة الأوامر وأدوات الدردشة في منتجات تُشحن وتُبني عليها.",
      "قيادة متعددة التخصصات — القيادة كمالك منتج وقائد ضمان الجودة ومهندس ما قبل البيع."],
     True),
    ("zh", "zh-CN", "中文", FONT_ZH,
     ["多智能体编排 — 设计并在生产中交付具有生命周期可观测性的多智能体系统。",
      "多模型路由与成本 — 将 LLM 提供商统一到一个上下文窗口并核算每个模型的成本。",
      "评估框架 — 构建测试平台、回归套件、健康仪表板和告警。",
      "LLM 集成 — 提示工程与聊天工具在产品及自动化中交付落地。",
      "跨职能领导力 — 以产品负责人、QA 负责人和售前工程师的身份领导团队。"],
     False),
    ("ru", "ru-RU", "Русский", FONT,
     ["Мультиагентная оркестрация — проектирую и внедряю мультиагентные системы с наблюдаемостью жизненного цикла.",
      "Мультимодельная маршрутизация и стоимость — объединяю LLM-провайдеров в одно контекстное окно с учётом стоимости.",
      "Среды оценки — строю испытательные стенды, регрессионные наборы, панели здоровья и алертинг.",
      "Интеграция LLM — промпт-инжиниринг и чат-инструменты в выпущенных продуктах и автоматизации.",
      "Межфункциональное лидерство — лидирую как Product Owner, QA Lead и инженер пресейла."],
     False),
    ("de", "de-DE", "Deutsch", FONT,
     ["Multi-Agenten-Orchestrierung — Design und Auslieferung von Multi-Agenten-Systemen mit Lifecycle-Observability.",
      "Multi-Modell-Routing und Kosten — LLM-Anbieter in einem Kontextfenster vereinen, Kosten pro Modell zuordenbar.",
      "Evaluations-Frameworks — Prüfstände, Regressions-Suiten, Health-Dashboards und Alerting.",
      "LLM-Integration — Prompt-Engineering und Chatbot-Tooling in ausgelieferten Produkten.",
      "Funktionsübergreifende Führung — als Product Owner, QA Lead und Presales-Ingenieur führen."],
     False),
    ("ja", "ja-JP", "日本語", FONT_JA,
     ["マルチエージェントオーケストレーション — ライフサイクル観測性を持つマルチエージェントシステムを設計し本番提供。",
      "マルチモデルルーティングとコスト — 複数LLMを一つのコンテキストウィンドウに統合しモデルごとにコストを割り当て。",
      "評価フレームワーク — テストハーネス、リグレッションスイート、ヘルスダッシュボード、アラートを構築。",
      "LLM統合 — プロンプトエンジニアリングとチャットツールを本番製品や自動化に組み込み。",
      "部門横断的リーダーシップ — プロダクトオーナー、QAリード、プリセールスエンジニアとしてリード。"],
     False),
]
I18N_DEFAULT = "en"


# The dropdown /DA references these resource names (keys in the AcroForm /DR
# /Font dict). We hand-write the DR because reportlab's standard-14 only AcroForm
# DR cannot render Arabic/Cyrillic/CJK.
FORM_RES = {           # l10n code -> AcroForm font resource name
    "ar": "/AR",
    "es": "/DJF",
    "en": "/DJF",
    "ru": "/DJF",
    "de": "/DJF",
    "zh": "/ZH",
    "ja": "/JA",
}


def _build_form_dr(doc):
    """Force-embed the fonts used by the AcroForm and return their /DR /Font
    dictionary (resource-name -> reference).

    * /DJF  — DejaVu subset seeded with the es/en/ru/de translation text
              (covers latin + Cyrillic), a dedicated instance so the page's
              main "DJ" subset is left untouched.
    * /AR   — Noto Sans Arabic subset seeded with the Arabic translations.
    * /ZH, /JA — Acrobat built-in CID fonts, referenced by object (no embed).
    """
    bf = doc.idToObject["BasicFonts"].dict

    def embed_dynamic(ps_name, texts):
        f = pdfmetrics.getFont(ps_name)
        f.splitString(" ".join(texts), doc)
        # getSubsetInternalName seeds the subset (registers it in fontMapping /
        # delayedFonts so reportlab embeds it once, at save time, together with
        # the page text). We do NOT call addObjects() here: freezing the page
        # font mid-build would double-embed it. The returned name resolves to
        # the real font object once save-time embedding runs.
        subname = f.getSubsetInternalName(0, doc)   # '/F2+0'
        return _pdfdoc.PDFObjectReference(subname[1:])

    latin_texts = [t for c, _, _, fn, lines, _ in I18N for t in lines
                   if fn == FONT and c != "ar"]
    arabic_texts = [t for c, _, _, fn, lines, _ in I18N for t in lines
                    if fn == FONT_AR]

    Font = _pdfdoc.PDFDictionary()
    Font["DJF"] = embed_dynamic(FONT, latin_texts)
    Font["AR"] = embed_dynamic(FONT_AR, arabic_texts)
    doc.getInternalFontName(FONT_ZH)             # registers '/F4' in fontMapping
    doc.getInternalFontName(FONT_JA)             # registers '/F5'
    Font["ZH"] = bf[doc.fontMapping[FONT_ZH][1:]]
    Font["JA"] = bf[doc.fontMapping[FONT_JA][1:]]

    DR = _pdfdoc.PDFDictionary()
    DR["Font"] = Font
    return DR


class L10nPanel(Flowable):
    """Interactive multi-language Key Strengths panel.

    A horizontal radio strip selects a language; each language owns one
    read-only multiline text field stacked at the same rect, pre-rendered with
    that language's full five-strength block (wrapped, with Arabic reshaped and
    right-aligned). Selecting a radio runs JavaScript that shows the matching
    field and hides the other six. Every viewer renders the block because each
    field carries its own appearance stream (/AP /N) — no reliance on Acrobat
    regenerating a single-line appearance from /V. English is default.
    """
    def __init__(self, width=FW, height=185):
        super().__init__()
        self.width = width
        self.height = height
        self._injected = False

    def wrap(self, aW, aH):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        x0, y0, w, h = 0, 0, self.width, self.height

        # panel background
        c.saveState()
        c.setFillColor(LIGHT)
        c.roundRect(x0, y0, w, h, 10, fill=1, stroke=0)
        c.restoreState()

        # AcroForm default resources: /DR (fonts for the dropdowns' /DA) is
        # built from the embedded DejaVu/Noto subsets + Acrobat CID fonts so
        # every translation renders instead of '?????'.
        form = c.acroForm
        form.extras["DR"] = _build_form_dr(c._doc)

        # Pre-render a wrapped multi-line appearance form per language. Each
        # form is referenced as its widget's /AP /N so every viewer (incl.
        # PDF.js in Chrome/Firefox) shows the full five-strength block, instead
        # of Acrobat having to regenerate a truncated single-line appearance.
        def wrap_line(text, font, size, max_w):
            words = text.split(" ")
            out, line = [], ""
            for wd in words:
                cand = (line + " " + wd).strip() if line else wd
                if pdfmetrics.stringWidth(cand, font, size) <= max_w or not line:
                    line = cand
                else:
                    out.append(line)
                    line = wd
            if line:
                out.append(line)
            return out

        dd_x, dd_y, dd_w, dd_h = 14, 40, w - 28, 88
        fsize, flead, pad = 8.4, 10.08, 5
        gap = 1.5
        ap_refs = {}
        for code, tag, label, font, lines, rtl in I18N:
            fname = "l10n_ap_%s" % code
            # wrap once to count lines so the block can be vertically centered
            # (avoids a dead empty band under the last strength)
            plan = []
            for ln in lines:
                disp = get_display(arabic_reshaper.reshape(ln)) if rtl else ln
                plan.append(wrap_line(disp, font, fsize, dd_w - 2 * pad))
            total_lines = sum(len(p) for p in plan)
            drop = (total_lines - 1) * flead + (len(lines) - 1) * gap
            y = (dd_h + drop) / 2.0          # first baseline, centered vertically
            c.beginForm(fname, 0, 0, dd_w, dd_h)
            c.setFillColor(colors.white)
            c.rect(0, 0, dd_w, dd_h, fill=1, stroke=0)
            c.setStrokeColor(NAVY2); c.setLineWidth(0.8)
            c.rect(0.4, 0.4, dd_w - 0.8, dd_h - 0.8, fill=0, stroke=1)
            c.setFont(font, fsize); c.setFillColor(INK)
            for pieces in plan:
                for piece in pieces:
                    if rtl:
                        c.drawRightString(dd_w - pad, y, piece)
                    else:
                        c.drawString(pad, y, piece)
                    y -= flead
                y -= gap
            c.endForm()
            ap_refs[code] = _pdfdoc.PDFObjectReference(
                c._doc.getXObjectName(fname))

        # inject radio->field JS + point each field at its pre-rendered /AP
        pending = list(I18N)
        combo_idx = [0]
        orig_add = c._addAnnotation
        def add_with_aa(annotation, name=None, addtopage=1):
            if pending and isinstance(annotation, _pdfdoc.PDFDictionary) and \
                    "FT" in annotation and annotation["FT"] == _pdfdoc.PDFName("Btn"):
                code, tag, label, font, lines, rtl = pending.pop(0)
                codes_js = "','".join(o for o, *_ in I18N)
                body = ("var sel='%s';var cs=['%s'];var f;"
                        "for(var i=0;i<cs.length;i++){f=this.getField('l10n_dd_'+cs[i]);"
                        "if(f){if(cs[i]==sel){f.hidden=false;}else{f.hidden=true;}}}" % (code, codes_js))
                aa = _pdfdoc.PDFDictionary()
                u = _pdfdoc.PDFDictionary()
                u["S"] = _pdfdoc.PDFName("JavaScript")
                u["JS"] = _pdfdoc.PDFString(body)
                aa["U"] = u
                annotation["AA"] = aa
            elif isinstance(annotation, _pdfdoc.PDFDictionary) and \
                    "FT" in annotation and annotation["FT"] == _pdfdoc.PDFName("Tx"):
                code, tag, label, font, lines, rtl = I18N[combo_idx[0]]
                annotation["V"] = _pdfdoc.PDFString("\n".join(lines))
                annotation["DV"] = _pdfdoc.PDFString("\n".join(lines))
                annotation["DA"] = _pdfdoc.PDFString(
                    "%s 8.4 Tf 0 g" % FORM_RES[code])
                annotation["AP"] = _pdfdoc.PDFDictionary({"N": ap_refs[code]})
                combo_idx[0] += 1
            return orig_add(annotation, name, addtopage)
        c._addAnnotation = add_with_aa

        # radio strip: radio + language label on one horizontal line
        rx = 14
        ry = h - 36                       # radio box bottom
        c.setFont(FONT, 6.4); c.setFillColor(MUTE)
        c.drawString(rx, h - 12, "Key Strengths — select a language:")
        for i, (code, tag, label, font, lines, rtl) in enumerate(I18N):
            form.radioRelative(name="l10n_lang", value=code, selected=(code == I18N_DEFAULT),
                               size=10, x=rx, y=ry, buttonStyle="circle",
                               fillColor=PURPLE, borderColor=PURPLE,
                               tooltip="Show Key Strengths in " + label)
            c.saveState()
            c.setFont(FONT_B, 7.0); c.setFillColor(NAVY2)
            c.drawString(rx + 13, ry + 5 - 2.4, code.upper())   # centered on radio
            c.restoreState()
            rx += 13 + pdfmetrics.stringWidth(code.upper(), FONT_B, 7.0) + 14

        # one read-only multiline field per language, stacked at the same rect
        # right under the radio strip; only the selected language's field shows.
        c.setFont(FONT, 6.4); c.setFillColor(MUTE)
        c.drawString(14, 133, "Translations:")
        for i, (code, tag, label, font, lines, rtl) in enumerate(I18N):
            form.textfield(name="l10n_dd_%s" % code,
                           value="",
                           tooltip="Key Strengths in %s" % label,
                           x=dd_x, y=dd_y, width=dd_w, height=dd_h,
                           fontSize=8.4, borderColor=NAVY2, borderWidth=0.8,
                           fillColor=colors.white, fieldFlags="multiline readOnly",
                           relative=True, maxlen=0,
                           annotationFlags="print hidden" if code != I18N_DEFAULT else "print")
        c._addAnnotation = orig_add


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


def qr_block(size=84):
    """Generate a themed QR PNG of QR_URL and return a right-aligned flowable."""
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    segno.make_qr(QR_URL, error="m").save(
        path, scale=10, dark="#1a1342", light="#ffffff", border=0)
    qr = RLImage(path, width=size, height=size)
    caption = Paragraph("Scan to view my GitHub profile", qr_cap_style)
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
     "Solar, storage, and the grid of the future — following the tech and the mission."),
    ("Permaculture",
     "Regenerative design: food forests, rainwater harvesting, and building topsoil at home."),
    ("Real Estate",
     "Buy-and-hold multifamily and value-add deals, analyzed with a cash-flow-first lens."),
    ("Tango Dancing",
     "Argentine tango — the embrace, the pause, the musicality of the walk."),
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
SUMMARY = ("Using probabilistic systems to create deterministic solutions reliably. "
           "That is the core of my work: designing and shipping agentic AI infrastructure "
           "where teams build, deploy, and coordinate intelligent agents at scale. "
           "I turn ambiguous model behavior into predictable, observable, well-bounded "
           "systems teams can trust in production \u2014 multi-agent orchestration, "
           "multi-model routing, evaluation, and the privacy and search foundations "
           "that make AI-native platforms real.")

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
     "", [
        "QA on an advanced research team evaluating distributed system behavior across consumer "
        "appliances, mobile platforms, stream servers, and cellular networks \u2014 complex, multi-component scenarios.",
        "Global presales engineering: turned product capabilities into customer solutions "
        "across diverse technical environments. Trained new hires; led cross-functional collaboration.",
     ]),
    ("Senior Software Test Engineer IV",
     "Microsoft  \u00b7  Redmond, WA  \u00b7  Windows Media Server",
     "", [
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
     "Design and ship multi-agent systems in production \u2014 lifecycle observability, bounded I/O, "
     "and crash recovery that keep agents auditable, controllable, and dependable."),
    ("Multi-model routing & cost",
     "Unify many LLM providers behind one context window with per-model cost attribution, "
     "so routing decisions stay transparent and accountable."),
    ("Evaluation frameworks",
     "Build evaluation harnesses, regression suites, health dashboards, and alerting that "
     "measure real behavior across distributed systems."),
    ("LLM integration",
     "Bring prompt engineering and chatbot tooling into production products and "
     "internal automation that real users depend on."),
    ("Cross-functional leadership",
     "Lead as Product Owner, QA Lead, and presales engineer \u2014 partnering daily with "
     "PMs, designers, researchers, and engineers."),
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
        "OpenCode", "Codex Agents", "ZeroCode", "Hermes Agent",
        "Claude Code",
    ]),
    ("LLM, Multi-Model & MCP", [
        "Context Window Routing", "Multi-Model Cost Attribution",
        "MCP (Model Context Protocol)", "herdr-mcp Server",
        "External Tool Access", "Prompt Engineering",
        "OpenAI", "Anthropic", "Cohere", "Gemini",
        "Ollama", "Hugging Face",
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
    story.append(Spacer(1, 6))

    # ── Key Strengths — interactive localization panel (bottom of page 1)
    story.append(SectionTitle("Key Strengths"))
    story.append(Spacer(1, 1))
    story.append(L10nPanel())
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
    for e in EDUCATION:
        story.append(P(e, edu_style, bullet="\u2022"))

    # ── Other Interests + GitHub QR (bottom of page 2) ─────────────
    story.append(Spacer(1, 4))
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
