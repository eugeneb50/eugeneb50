#!/usr/bin/env python3
"""Genera un CV en PDF visualmente dinámico para Eugene L. Buchanan
   orientado a puestos de Ingeniero de IA Senior — Marcos Multiagente.
   Usa reportlab con encabezado degradado, barras de habilidades,
   nubes de etiquetas y tarjetas de experiencia.
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
_rl_config.documentLang = "es-ES"   # PDF /Lang catalog entry (a11y + l10n)

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
        c.drawString(28, H - 64, "Ingeniero de IA Senior  \u2014  Marcos Multiagente e Infraestructura Agéntica")
        # separator
        c.setStrokeColor(colors.white); c.setFillAlpha(0.22); c.setLineWidth(0.5)
        c.line(28, H - 74, pcx - pr - 10, H - 74); c.setFillAlpha(1)
        # contact strip
        items = [                 ("L", "Apple Valley, CA (Remoto)", None),
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
    def __init__(self, tags, width=FW, size=6.0, padx=4, pady=1.0, gap=2,
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
I18N_DEFAULT = "es"


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
    def __init__(self, width=FW, height=172):
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
        c.drawString(rx, h - 12, "Fortalezas Clave — selecciona un idioma:")
        for i, (code, tag, label, font, lines, rtl) in enumerate(I18N):
            form.radioRelative(name="l10n_lang", value=code, selected=(code == I18N_DEFAULT),
                               size=10, x=rx, y=ry, buttonStyle="circle",
                               fillColor=PURPLE, borderColor=PURPLE,
                               tooltip="Mostrar Fortalezas Clave en " + label)
            c.saveState()
            c.setFont(FONT_B, 7.0); c.setFillColor(NAVY2)
            c.drawString(rx + 13, ry + 5 - 2.4, code.upper())   # centered on radio
            c.restoreState()
            rx += 13 + pdfmetrics.stringWidth(code.upper(), FONT_B, 7.0) + 14

        # one read-only multiline field per language, stacked at the same rect
        # right under the radio strip; only the selected language's field shows.
        c.setFont(FONT, 6.4); c.setFillColor(MUTE)
        c.drawString(14, 133, "Traducciones:")
        for i, (code, tag, label, font, lines, rtl) in enumerate(I18N):
            form.textfield(name="l10n_dd_%s" % code,
                           value="",
                           tooltip="Fortalezas Clave en %s" % label,
                           x=dd_x, y=dd_y, width=dd_w, height=dd_h,
                           fontSize=8.4, borderColor=NAVY2, borderWidth=0.8,
                           fillColor=colors.white, fieldFlags="multiline readOnly",
                           relative=True, maxlen=0,
                           annotationFlags="print hidden" if code != I18N_DEFAULT else "print")
        c._addAnnotation = orig_add


# ----------------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------------
summary_style = ParagraphStyle("sum", fontName=FONT, fontSize=9.0, leading=12.0,
                                textColor=INK, alignment=TA_JUSTIFY)
role_style = ParagraphStyle("role", fontName=FONT_B, fontSize=10.4, leading=12.8,
                             textColor=DARK, spaceAfter=0)
date_style = ParagraphStyle("date", fontName=FONT, fontSize=8.2, leading=10.8,
                             textColor=GREY, alignment=2)
sub_style = ParagraphStyle("sub", fontName=FONT, fontSize=8.7, leading=11.0,
                            textColor=PURPLE, spaceAfter=2)
bullet_style = ParagraphStyle("bul", fontName=FONT, fontSize=8.2, leading=10.0,
                               leftIndent=12, bulletIndent=1, bulletColor=PURPLE,
                               spaceAfter=1.0, textColor=INK)
str_style = ParagraphStyle("str", fontName=FONT, fontSize=7.9, leading=9.6,
                            leftIndent=12, bulletIndent=0, bulletColor=PURPLE,
                            spaceAfter=1.2, textColor=INK)
edu_style = ParagraphStyle("edu", fontName=FONT, fontSize=8.0, leading=10.4,
                            leftIndent=12, bulletIndent=1, bulletColor=PURPLE,
                            spaceAfter=1.5, textColor=INK)
tagcap_style = ParagraphStyle("tagcap", fontName=FONT_B, fontSize=8.6, leading=12,
                              textColor=GREY, spaceBefore=2, spaceAfter=4)
qr_cap_style = ParagraphStyle("qrcap", fontName=FONT, fontSize=6.4, leading=8,
                              alignment=1, textColor=MUTE)
int_title_style = ParagraphStyle("intt", fontName=FONT_B, fontSize=8.2, leading=10.0,
                                  textColor=PURPLE, spaceAfter=1.0)
int_body_style = ParagraphStyle("intb", fontName=FONT, fontSize=7.5, leading=9.3,
                                 textColor=INK)
int_box_style = ParagraphStyle("intbox", fontName=FONT_B, fontSize=9.6, leading=12,
                                textColor=DARK, spaceAfter=1.5)


# QR code pointing at the GitHub repo (right-aligned block, sits under Education).
QR_URL = "https://github.com/eugeneb50/eugeneb50/"


def qr_block(size=84):
    """Generate a themed QR PNG of QR_URL and return a right-aligned flowable."""
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    segno.make_qr(QR_URL, error="m").save(
        path, scale=10, dark="#1a1342", light="#ffffff", border=0)
    qr = RLImage(path, width=size, height=size)
    caption = Paragraph("Escanea para ver mi perfil de GitHub", qr_cap_style)
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
    ("Energ\u00eda Renovable",
     "Solar, almacenamiento y la red del futuro \u2014 siguiendo la tecnolog\u00eda y la misi\u00f3n."),
    ("Permacultura",
     "Dise\u00f1o regenerativo: bosques de alimentos, captaci\u00f3n de agua de lluvia y construcci\u00f3n de suelo en casa."),
    ("Bienes Ra\u00edces",
     "Compra y retenci\u00f3n de multifamiliares y operaciones de valor agregado, analizadas con criterio de flujo de efectivo primero."),
    ("Baile de Tango",
     "Tango argentino \u2014 el abrazo, la pausa, la musicalidad del caminar."),
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
    box = Table([[Paragraph("Otros Intereses", int_box_style)], [grid]],
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
    return [card, Spacer(1, 2)]

# ----------------------------------------------------------------------------
# Content — Staff AI Engineer, Multi-Agent Frameworks
# ----------------------------------------------------------------------------
SUMMARY = ("Uso sistemas probabilísticos para crear soluciones deterministas con fiabilidad. "
           "Ese es el centro de mi trabajo: dise\u00f1ar y lanzar infraestructura de IA ag\u00e9ntica "
           "donde los equipos construyen, despliegan y coordinan agentes inteligentes a gran escala. "
           "Convierto el comportamiento ambiguo de los modelos en sistemas predecibles, observables "
           "y bien delimitados en los que los equipos pueden confiar en producci\u00f3n \u2014 orquestaci\u00f3n "
           "multiagente, enrutamiento multimodelo, evaluaci\u00f3n y los cimientos de privacidad y "
           "b\u00fasqueda que hacen reales las plataformas nativas de IA.")

EXPERIENCE = [
    ("Ingeniero de IA Senior / Contribuidor de Infraestructura Ag\u00e9ntica (C\u00f3digo Abierto)",
     "ZeroClaw Labs (github.com/zeroclaw-labs/zeroclaw)  \u00b7  Rust  \u00b7  32.2k stars",
     "2026 \u2013 Presente", [
        "PR #7946 (FUSIONADA) \u2014 barra medidora de ventana de contexto en TUI/gateway/CLI "
        "(+1.109 / -22, 25 archivos). Una sola fuente de verdad context_window para 9 proveedores; "
        "configuraci\u00f3n autopoblada, comando doctor, API del gateway, ContextBar en vivo. Elimin\u00f3 la "
        "deriva entre superficies \u2014 directamente relevante para el enrutamiento autom\u00e1tico de modelos de Brain2.",
        "PR #8966 (ABIERTA) \u2014 porta la identidad en vivo del proveedor en los eventos de uso (+2.742 / -141, 20 archivos). "
        "Correg\u00ed el medidor congelado de 32k en modelos de 1M de tokens; separ\u00e9 el presupuesto de recorte de la "
        "capacidad del modelo; eventos Usage incondicionales con identidad del proveedor de servicio; desglose de uso "
        "por proveedor en el marco done \u2014 infraestructura de atribuci\u00f3n de costos para orquestaci\u00f3n multi-LLM.",
        "PR #8337 (ABIERTA) \u2014 integraci\u00f3n de reportes de agentes herdr (+1.712 / -17, 13 archivos). "
        "El observador reporta el ciclo de vida del agente (inactivo/trabajando/bloqueado/liberado) v\u00eda JSON-RPC sobre UDS. "
        "Detecci\u00f3n de entorno sin configuraci\u00f3n, estado bloqueado por puerta de aprobaci\u00f3n, recuperaci\u00f3n de fallos "
        "v\u00eda pane.release_agent. Infraestructura de coordinaci\u00f3n multiagente; se mapea a la colaboraci\u00f3n humano-agente de Super Agents.",
     ]),
    ("Ingeniero de Software Senior / QA Lead / Product Owner de Integraciones",
     "Knowledgecity LLC  \u00b7  Remoto  \u00b7  AWS / Postgres / React",
     "Dic 2020 \u2013 Ago 2025", [
        "Product Owner de Integraciones: lanc\u00e9 integraciones con SAP, Oracle, Workday, Coursera, UKG y Zoom "
        "v\u00eda SAML, OAuth, SFTP y APIs REST personalizadas \u2014 orquestando m\u00faltiples servicios con distintos "
        "modelos de autenticaci\u00f3n, formatos de datos y sem\u00e1nticas de error. El mismo desaf\u00edo de coordinaci\u00f3n que los sistemas multiagente.",
        "Constru\u00ed y mantuve pipelines de calidad CI/CD con Cypress, Selenium, Postman, JUnit, Elastic, S3 \u2014 "
        "un marco de evaluaci\u00f3n para probar escenarios complejos de despliegue en superficies de integraci\u00f3n, backend, API, "
        "base de datos y frontend.",
        "Apliqu\u00e9 ingenier\u00eda de prompts de IA y lanc\u00e9 herramientas de chatbot con LLM en producci\u00f3n, "
        "integr\u00e1ndolas en asistencia al cliente y flujos de automatizaci\u00f3n interna.",
        "Dise\u00f1\u00e9 marcos de evaluaci\u00f3n, suites de regresi\u00f3n, paneles de salud y alertas "
        "para medir la din\u00e1mica a nivel de sistema en despliegues multi-entorno.",
        "Mentoric\u00e9 y capacit\u00e9 al equipo de automatizaci\u00f3n de pruebas; dirig\u00ed revisiones de c\u00f3digo; elev\u00e9 los est\u00e1ndares de ingenier\u00eda.",
     ]),
    ("Ingeniero de Software Senior II / Ingenier\u00eda de Preventa",
     "RealNetworks  \u00b7  Seattle, WA  \u00b7  Plataforma de Streaming de Medios",
     "", [
        "QA en un equipo de investigaci\u00f3n avanzada evaluando el comportamiento de sistemas distribuidos en "
        "electrodom\u00e9sticos de consumo, plataformas m\u00f3viles, servidores de streaming y redes celulares \u2014 escenarios complejos y multicomponente.",
        "Ingenier\u00eda de preventa global: convert\u00ed capacidades del producto en soluciones para clientes en diversos "
        "entornos t\u00e9cnicos. Capacit\u00e9 nuevos ingresos; lider\u00e9 colaboraci\u00f3n multifuncional.",
     ]),
    ("Ingeniero de Pruebas de Software Senior IV",
     "Microsoft  \u00b7  Redmond, WA  \u00b7  Windows Media Server",
     "", [
        "Pruebas de caja blanca y automatizaci\u00f3n para Windows Media Server, Windows 98/NT \u2014 marcos de evaluaci\u00f3n para pruebas complejas de sistemas.",
        "Depuraci\u00f3n profunda en infraestructura de servidores, protocolos de red y c\u00f3decs multimedia.",
     ]),
    # (IBM 1998 omitido \u2014 una sola vi\u00f1eta, mismo enfoque de fiabilidad cubierto en el rol de Microsoft)
]

SKILLS = [
    ("Frontend - HTML, XML, Javascript, CSS", 94),
    ("Marcos Multiagente y Orquestaci\u00f3n", 88),
    ("Integraci\u00f3n de LLM y Enrutamiento Multimodelo", 90),
    ("Ciclo de Vida del Agente y Observabilidad", 92),
    ("Marcos de Evaluaci\u00f3n y Pruebas", 92),
    ("Ingenier\u00eda Backend (Rust, Python, Node)", 90),
    ("Ventana de Contexto y Atribuci\u00f3n de Costos", 87),
    ("Integraci\u00f3n de B\u00fasqueda (Elastic, Postgres)", 85),
    ("Privacidad de IA, Autenticaci\u00f3n y Protecci\u00f3n de Datos", 82),
]

STRENGTHS = [
    ("Orquestaci\u00f3n multiagente",
     "Dise\u00f1o y lanzo sistemas multiagente en producci\u00f3n \u2014 observabilidad del ciclo de vida, "
     "E/S delimitadas y recuperaci\u00f3n de fallos que mantienen a los agentes auditables, "
     "controlables y fiables."),
    ("Enrutamiento multimodelo y costos",
     "Unifico m\u00faltiples proveedores de LLM tras una sola ventana de contexto con atribuci\u00f3n "
     "de costos por modelo, para que las decisiones de enrutamiento sean transparentes y responsables."),
    ("Marcos de evaluaci\u00f3n",
     "Construyo entornos de evaluaci\u00f3n, suites de regresi\u00f3n, paneles de salud y alertas que "
     "miden el comportamiento real en sistemas distribuidos."),
    ("Integraci\u00f3n de LLM",
     "Llevo la ingenier\u00eda de prompts y las herramientas de chatbot a productos en producci\u00f3n "
     "y automatizaci\u00f3n interna de los que dependen usuarios reales."),
    ("Liderazgo multifuncional",
     "Lidero como Product Owner, QA Lead e ingeniero de preventa \u2014 colaborando a diario con "
     "PMs, dise\u00f1adores, investigadores e ingenieros."),
]

EDUCATION = [
    "Grado de Asociado, Victor Valley College",
    "Comisi\u00f3n de Notario de California",
    "Toastmasters International",
]

TAG_SECTIONS = [
    ("Multiagente y Orquestaci\u00f3n", [
        "LangGraph", "Coordinaci\u00f3n Multiagente", "Ciclo de Vida del Agente", "JSON-RPC",
        "E/S Delimitadas", "Fire-and-Forget", "Sockets de Dominio Unix",
        "OpenCode", "Codex Agents", "ZeroCode", "Hermes Agent",
        "Claude Code",
    ]),
    ("LLM, Multimodelo y MCP", [
        "Enrutamiento de Ventana de Contexto", "Atribuci\u00f3n de Costos Multimodelo",
        "MCP (Model Context Protocol)", "Servidor herdr-mcp",
        "Acceso a Herramientas Externas", "Ingenier\u00eda de Prompts",
        "OpenAI", "Anthropic", "Cohere", "Gemini",
        "Ollama", "Hugging Face",
    ]),
    ("Backend y Plataforma", [
        "Rust", "Python", "Node.js", "PostgreSQL", "AWS (ECS, S3)",
        "REST", "GraphQL", "Docker", "Git",
    ]),
    ("Evaluaci\u00f3n y Pruebas", [
        "Cypress", "Selenium", "JUnit", "Postman", "Elasticsearch",
        "Suites de Regresi\u00f3n", "Paneles de Salud", "Alertas",
    ]),
    ("Autenticaci\u00f3n y Privacidad", [
        "SAML", "OAuth", "OIDC", "Perfiles de Permisos",
        "Aislamiento de Principal", "Denegar por Defecto",
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
        "Eugene L. Buchanan  \u00b7  Ingeniero de IA Senior \u2014 Marcos Multiagente")
    canvas.drawRightString(PW - MR, 24, "Page %d" % doc.page)
    canvas.restoreState()


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Resume_ES.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP, bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Currículum de Ingeniero de IA Senior",
                          author="Eugene L. Buchanan",
                          subject="Ingeniero de IA Senior \u2014 Marcos Multiagente e Infraestructura Agéntica de IA (Apple Valley, CA)",
                          keywords="Ingeniero de IA Senior, Multiagente, LangGraph, LLM, Rust, Orquestación de Agentes")
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
    story.append(SectionTitle("Resumen Profesional"))
    story.append(Spacer(1, 1))
    story.append(P(SUMMARY, summary_style))
    story.append(Spacer(1, 1))

    # ── Technical Expertise (skill bars + radar chart) ────────────────
    story.append(SectionTitle("Experiencia T\u00e9cnica"))
    story.append(Spacer(1, 1))
    bars_col = [SkillBar(label, pct) for label, pct in SKILLS]
    radar_col = [SkillRadar(
        ["Coordinaci\u00f3n\nMultiagente", "M\u00faltiples\nLLMs", "Orquestaci\u00f3n\nLangGraph",
         "Marcos de\nEvaluaci\u00f3n", "Privacidad\nde IA", "B\u00fasqueda y\nBackend"],
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
    story.append(SectionTitle("Tecnolog\u00edas"))
    story.append(Spacer(1, 1))
    for cat_name, cat_tags in TAG_SECTIONS:
        story.append(TagCloud(cat_tags))
        story.append(Spacer(1, 1))
    story.append(Spacer(1, 6))

    # ── Key Strengths — interactive localization panel (bottom of page 1)
    story.append(SectionTitle("Fortalezas Clave"))
    story.append(Spacer(1, 1))
    story.append(L10nPanel())
    story.append(PageBreak())

    # ── Experience (second page) ────────────────────────────────────
    story.append(SectionTitle("Experiencia"))
    story.append(Spacer(1, 1))
    for role, cl, dates, bullets in EXPERIENCE:
        story.extend(experience_card(role, cl, dates, bullets))
    story.append(Spacer(1, 1))

    # ── Education ────────────────────────────────────────────────
    story.append(SectionTitle("Educaci\u00f3n"))
    story.append(Spacer(1, 1))
    for e in EDUCATION:
        story.append(P(e, edu_style, bullet="\u2022"))

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
