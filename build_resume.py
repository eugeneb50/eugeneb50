#!/usr/bin/env python3
"""Generate a visually dynamic resume PDF for Eugene L. Buchanan
   targeted at Cyber Security Engineer roles — Offensive Security, Application
   & Product Security, SOC 2 / Compliance, and AI Secure Development.
   Uses reportlab with gradient header, skill bars, tag clouds, and
   experience cards.
"""

import os
import tempfile
import arabic_reshaper
import segno
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
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
from reportlab.lib.utils import ImageReader
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
        c.drawString(28, H - 64, "Cyber Security Engineer  \u2014  Offensive & AI-Powered Secure Development")
        # separator
        c.setStrokeColor(colors.white); c.setFillAlpha(0.22); c.setLineWidth(0.5)
        c.line(28, H - 74, pcx - pr - 10, H - 74); c.setFillAlpha(1)
        # contact strip — plain text so ATS parsers read one clean line
        items = [("Apple Valley, CA (Remote)", None),
                 ("+1 (909) 545-5384", None),
                 ("eugene@serviceofothers.org", "mailto:eugene@serviceofothers.org"),
                 ("github.com/eugeneb50", "https://github.com/eugeneb50")]
        x = 28; cy = H - 88
        link_rects = []
        for i, (txt, url) in enumerate(items):
            if i:
                sep = "   \u00b7   "
                c.setFillColor(colors.HexColor("#cfc5ee")); c.setFont(FONT, 7.5)
                c.drawString(x, cy - 1, sep)
                x += pdfmetrics.stringWidth(sep, FONT, 7.5)
            c.setFillColor(colors.HexColor("#eaeafa")); c.setFont(FONT, 7.5)
            c.drawString(x, cy - 1, txt)
            tw = pdfmetrics.stringWidth(txt, FONT, 7.5)
            if url:
                link_rects.append((url, x, cy - 4, x + tw, cy + 10))
            x += tw + 12
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
     ["Evidence-based vulnerability discovery — agentic offensive tooling (bug-reaper, MCP, LLM agents) finds only real, exploitable bugs; every finding needs a working PoC and passes triage.",
      "Identity, access & API security — enforce SAML, OAuth, OIDC boundaries and deny-by-default principal isolation across multitenant products and integrations.",
      "Compliance & audit (SOC 2) — own SOC 2 Type II filing end-to-end: control mapping, evidence collection, gap closure, and auditor management.",
      "Secure SDLC & white-box testing — deep white-box and code-review testing across backend, API, database, and frontend, backed by automated CI/CD security verification.",
      "Cross-functional leadership — lead as QA Lead, product/compliance owner, and presales engineer, partnering with PMs, developers, and auditors."],
     False),
    ("es", "es-ES", "Español", FONT,
     ["Descubrimiento de vulnerabilidades basado en evidencia — la herramienta ofensiva agéntica (bug-reaper, MCP, agentes LLM) encuentra solo errores reales y explotables; cada hallazgo requiere un PoC funcional y pasa el triaje.",
      "Seguridad de identidad, acceso y API — aplico límites SAML, OAuth y OIDC y aislamiento de principal por defecto en productos multiinquilino e integraciones.",
      "Cumplimiento y auditoría (SOC 2) — lidero el proceso SOC 2 Tipo II de principio a fin: mapeo de controles, evidencia, cierre de brechas y gestión de auditores.",
      "SDLC seguro y pruebas de caja blanca — pruebas profundas de caja blanca y revisión de código en backend, API, base de datos y frontend, respaldadas por verificación de seguridad CI/CD.",
      "Liderazgo multifuncional — lidero como QA Lead, responsable de producto/cumplimiento e ingeniero de preventa."],
     False),
    ("ar", "ar-AE", "العربية", FONT_AR,
     ["اكتشاف الثغرات القائم على الأدلة — الأدوات الهجومية الوكيلة (bug-reaper وMCP وعوامل LLM) تجد فقط الأخطاء الحقيقية القابلة للاستغلال؛ كل اكتشاف يتطلب إثبات عمل ناجح واجتياز الفرز.",
      "أمن الهوية والوصول وAPI — فرض حدود SAML وOAuth وOIDC وعزل المبدأ بالرفض الافتراضي عبر المنتجات متعددة المستأجرين والتكاملات.",
      "الامتثال والتدقيق (SOC 2) — قيادة ملف SOC 2 من النوع الثاني بالكامل: رسم الضوابط وجمع الأدلة وسد الفجوات وإدارة المدققين.",
      "دورة تطوير آمنة واختبار الصندوق الأبيض — اختبار عميق للصندوق الأبيض ومراجعة الكود عبر الواجهة الخلفية وAPI وقاعدة البيانات والواجهة الأمامية، مدعوم بتحقق أمني تلقائي في CI/CD.",
      "قيادة متعددة التخصصات — القيادة كقائد ضمان الجودة ومالك المنتج/الامتثال ومهندس ما قبل البيع."],
     True),
    ("zh", "zh-CN", "中文", FONT_ZH,
     ["基于证据的漏洞发现 — 代理攻击工具（bug-reaper、MCP、LLM 代理）只发现真实可利用的漏洞；每项发现都需可复现 PoC 并通过分级。",
      "身份、访问与 API 安全 — 在多租户产品和集成中落实 SAML、OAuth、OIDC 边界与默认拒绝的主体隔离。",
      "合规与审计（SOC 2）— 全流程主导 SOC 2 Type II：控制映射、证据收集、缺口修复与审计师管理。",
      "安全 SDLC 与白盒测试 — 对后端、API、数据库和前端进行深度白盒与代码审查测试，并由自动化 CI/CD 安全验证支撑。",
      "跨职能领导力 — 以 QA 负责人、产品/合规负责人和售前工程师身份领导团队。"],
     False),
    ("ru", "ru-RU", "Русский", FONT,
     ["Обнаружение уязвимостей на основе доказательств — агентные атакующие инструменты (bug-reaper, MCP, LLM-агенты) находят только реальные эксплуатируемые баги; каждый недочёт требует рабочего PoC и проходит триаж.",
      "Безопасность идентификации, доступа и API — обеспечиваю границы SAML, OAuth и OIDC и изоляцию субъектов с отказом по умолчанию в многопользовательских продуктах и интеграциях.",
      "Соответствие и аудит (SOC 2) — веду заполнение SOC 2 Type II от начала до конца: карта контролей, сбор доказательств, закрытие пробелов и работа с аудитором.",
      "Безопасный SDLC и тестирование белого ящика — глубокое тестирование белого ящика и ревью кода на бэкенде, API, БД и фронтенде, подкреплённое автоматической CI/CD-проверкой безопасности.",
      "Межфункциональное лидерство — лидирую как QA Lead, владелец продукта/комплаенса и инженер пресейла."],
     False),
    ("de", "de-DE", "Deutsch", FONT,
     ["Evidenzbasiertes Schwachstellen-Finding — agentische offensive Tools (bug-reaper, MCP, LLM-Agenten) finden nur echte, ausnutzbare Bugs; jeder Fund benötigt einen funktionierenden PoC und besteht das Triage.",
      "Identitäts-, Zugriffs- und API-Sicherheit — SAML-, OAuth- und OIDC-Grenzen sowie Principal-Isolation nach Deny-by-Default in Multi-Tenant-Produkten und Integrationen durchsetzen.",
      "Compliance & Audit (SOC 2) — SOC-2-Type-II-Einreichung end-to-end verantworten: Kontroll-Mapping, Evidenz, Gap-Schließung und Auditoren-Management.",
      "Sichere SDLC & White-Box-Testing — tiefes White-Box-Testing und Code-Review über Backend, API, Datenbank und Frontend, abgesichert durch automatisierte CI/CD-Sicherheitsprüfung.",
      "Funktionsübergreifende Führung — als QA Lead, Produkt-/Compliance-Owner und Presales-Ingenieur führen."],
     False),
    ("ja", "ja-JP", "日本語", FONT_JA,
     ["エビデンスに基づく脆弱性発見 — エージェント型攻撃ツール（bug-reaper、MCP、LLMエージェント）は実在する悪用可能なバグのみを検出。すべての発見には動作するPoCが必要でトリアージを通過。",
      "アイデンティティ・アクセス・APIセキュリティ — マルチテナント製品と連携でSAML/OAuth/OIDC境界とデフォルト拒否のプリンシパル分離を徹底。",
      "コンプライアンスと監査（SOC 2）— SOC 2 Type II 対応を一貫して主導：コントロール整理、証跡収集、ギャップ解消、監査人対応。",
      "セキュアSDLCとホワイトボックステスト — バックエンド・API・DB・フロントエンドの深いホワイトボックステストとコードレビューを、自動化されたCI/CDセキュリティ検証で支える。",
      "部門横断的リーダーシップ — QAリード、プロダクト/コンプライアンスオーナー、プリセールスエンジニアとして率いる。"],
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
    def __init__(self, width=FW, height=178):
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
        # Words listed in bold_idx (the strength label + trailing em-dash) are
        # measured with bold_font so wrapped lines that end in a bold run never
        # overflow; each returned line carries its per-word bold flags.
        def wrap_line(text, font, size, max_w, bold_idx=(), bold_font=None):
            out, line, line_w, flags = [], "", 0.0, []
            for g, wd in enumerate(text.split(" ")):
                b = g in bold_idx
                f = bold_font if (b and bold_font) else font
                w = pdfmetrics.stringWidth(wd, f, size)
                sep = pdfmetrics.stringWidth(" ", font, size) if line else 0
                cand = line_w + sep + w
                if cand <= max_w or not line:
                    line = (line + " " + wd).strip() if line else wd
                    line_w, flags = cand, flags + [b]
                else:
                    out.append((line, flags))
                    line, line_w, flags = wd, w, [b]
            if line:
                out.append((line, flags))
            return out

        # Split a wrapped line into (text, is_bold) runs, keeping the inter-word
        # spaces so segment widths sum exactly to the full line width.
        def split_segments(line, flags):
            if not flags or not any(flags):
                return [(line, False)]
            if all(flags):
                return [(line, True)]
            words = line.split(" ")
            offs, acc = [0], 0
            for wd in words[:-1]:
                acc += len(wd) + 1
                offs.append(acc)
            first = flags.index(True)
            last = len(flags) - 1 - flags[::-1].index(True)
            start = 0 if flags[0] else offs[first]
            end = len(line) if flags[-1] else offs[last] + len(words[last])
            return [(line[:start], False), (line[start:end], True),
                    (line[end:], False)]

        dd_x, dd_y, dd_w, dd_h = 14, 16, w - 28, 112
        fsize, flead, pad = 7.8, 9.36, 5
        gap = 1.5
        ap_refs = {}
        # RTL fields are pre-rendered as an IMAGE appearance instead of text:
        # reportlab's TrueType subsetting records /Widths per list-index while
        # assigning some codes by append, so the embedded widths never equal
        # stringWidth for multi-script strings, and poppler/Ghostscript then
        # render Arabic text short of the right edge. Noto Sans Arabic also
        # lacks Latin glyphs (bug-reaper, LLM, MCP, —, (...)), which made it
        # worse. Pixels are immune to both, so right-alignment is exact.
        _ink_rgb = tuple(round(ch * 255) for ch in INK.rgb())
        _navy2_rgb = tuple(round(ch * 255) for ch in NAVY2.rgb())
        _ar_ttf = os.path.join(FONT_DIR, "DejaVuSans.ttf")
        _ar_ttf_b = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
        img_scale = 4
        for code, tag, label, font, lines, rtl in I18N:
            fname = "l10n_ap_%s" % code
            # wrap once to count lines so the block can be vertically centered
            # (avoids a dead empty band under the last strength); wrap RTL with
            # the same DejaVu metrics that draw the image so lines never
            # overflow the pad margin. The strength label (up to the first
            # em-dash) is bolded as a visual cue — it sits at the START of LTR
            # lines and (after bidi) at the RIGHT end of RTL lines.
            wrap_font = FONT if rtl else font
            bold_font = "DJ-B" if wrap_font == FONT else None
            plan = []
            for ln in lines:
                disp = get_display(arabic_reshaper.reshape(ln)) if rtl else ln
                words = disp.split(" ")
                parts = ln.split(" — ", 1)
                if len(parts) > 1:
                    n_label = (len(get_display(arabic_reshaper.reshape(parts[0]))
                                   .split(" ")) + 1) if rtl \
                        else len(parts[0].split(" ")) + 1
                else:
                    n_label = len(words)
                n_label = min(n_label, len(words))
                if rtl:                 # label is the rightmost run
                    bold_idx = set(range(len(words) - n_label, len(words)))
                else:                   # label is the leading run
                    bold_idx = set(range(0, n_label))
                plan.append(wrap_line(disp, wrap_font, fsize, dd_w - 2 * pad,
                                      bold_idx, bold_font))
            total_lines = sum(len(p) for p in plan)
            drop = (total_lines - 1) * flead + (len(lines) - 1) * gap
            y = (dd_h + drop) / 2.0          # first baseline, centered vertically
            c.beginForm(fname, 0, 0, dd_w, dd_h)
            if rtl:
                img = Image.new("RGB",
                                (round(dd_w * img_scale), round(dd_h * img_scale)),
                                "white")
                d = ImageDraw.Draw(img)
                d.rectangle([round(0.4 * img_scale), round(0.4 * img_scale),
                             round((dd_w - 0.4) * img_scale),
                             round((dd_h - 0.4) * img_scale)],
                            outline=_navy2_rgb, width=round(0.8 * img_scale))
                pref = ImageFont.truetype(_ar_ttf, round(fsize * img_scale))
                pbf = ImageFont.truetype(_ar_ttf_b, round(fsize * img_scale))
                for pieces in plan:
                    for piece, flags in pieces:
                        segs = split_segments(piece, flags)
                        x = (dd_w - pad) * img_scale - sum(
                            d.textlength(s, pbf if b else pref) for s, b in segs)
                        for s, b in segs:
                            if not s:
                                continue
                            d.text((round(x), round((dd_h - y) * img_scale)),
                                   s, font=pbf if b else pref,
                                   fill=_ink_rgb, anchor="ls")
                            x += d.textlength(s, pbf if b else pref)
                        y -= flead
                    y -= gap
                c.drawImage(ImageReader(img), 0, 0, dd_w, dd_h)
            else:
                c.setFillColor(colors.white)
                c.rect(0, 0, dd_w, dd_h, fill=1, stroke=0)
                c.setStrokeColor(NAVY2); c.setLineWidth(0.8)
                c.rect(0.4, 0.4, dd_w - 0.8, dd_h - 0.8, fill=0, stroke=1)
                c.setFillColor(INK)
                for pieces in plan:
                    for piece, flags in pieces:
                        x = pad
                        for s, b in split_segments(piece, flags):
                            if not s:
                                continue
                            f = bold_font if (b and bold_font) else font
                            c.setFont(f, fsize)
                            c.drawString(x, y, s)
                            x += pdfmetrics.stringWidth(s, f, fsize)
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
                    "%s 7.8 Tf 0 g" % FORM_RES[code])
                annotation["AP"] = _pdfdoc.PDFDictionary({"N": ap_refs[code]})
                combo_idx[0] += 1
            return orig_add(annotation, name, addtopage)
        c._addAnnotation = add_with_aa

        # radio strip: radio + language label on one horizontal line
        rx = 14
        ry = h - 36                       # radio box bottom
        c.setFont(FONT, 6.4); c.setFillColor(MUTE)
        c.drawString(rx, h - 12, "Translations — select a language:")
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
                           fontSize=7.8, borderColor=NAVY2, borderWidth=0.8,
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
bullet_style = ParagraphStyle("bul", fontName=FONT, fontSize=8.6, leading=10.3,
                              leftIndent=12, bulletIndent=1, bulletColor=PURPLE,
                              spaceAfter=1.2, textColor=INK)
str_style = ParagraphStyle("str", fontName=FONT, fontSize=7.9, leading=9.6,
                           leftIndent=12, bulletIndent=0, bulletColor=PURPLE,
                           spaceAfter=1.2, textColor=INK)
edu_style = ParagraphStyle("edu", fontName=FONT, fontSize=8.2, leading=10.6,
                           leftIndent=12, bulletIndent=1, bulletColor=PURPLE,
                           spaceAfter=2, textColor=INK)
tagcap_style = ParagraphStyle("tagcap", fontName=FONT_B, fontSize=8.6, leading=12,
                              textColor=GREY, spaceBefore=2, spaceAfter=4)
qr_cap_style = ParagraphStyle("qrcap", fontName=FONT, fontSize=6.4, leading=8,
                              alignment=1, textColor=MUTE)
int_title_style = ParagraphStyle("intt", fontName=FONT_B, fontSize=8.8, leading=10.2,
                                 textColor=PURPLE, spaceAfter=1.5)
int_body_style = ParagraphStyle("intb", fontName=FONT, fontSize=7.9, leading=9.6,
                                textColor=INK)
int_box_style = ParagraphStyle("intbox", fontName=FONT_B, fontSize=10.5, leading=12,
                               textColor=DARK, spaceAfter=2)
comp_style = ParagraphStyle("comp", fontName=FONT, fontSize=8, leading=10.5,
                           textColor=INK, spaceAfter=2.5, alignment=TA_JUSTIFY)


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
    ("Security Research",
     "Reading vulnerability write-ups and open-source exploit tooling; exploring agentic security and MCP-based offense."),
    ("Renewable Energy",
     "Solar, storage, and the grid of the future — off-grid/on-grid systems and the engineering behind them."),
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
    return [card, Spacer(1, 2)]

# ----------------------------------------------------------------------------
# Content — Cyber Security Engineer
# ----------------------------------------------------------------------------
SUMMARY = ("Hands-on security engineer with deep application- and product-security experience \u2014 "
           "white-box testing, integration security, and evidence-based vulnerability discovery \u2014 "
           "who now runs that same discipline through agentic AI. I ship secure software and verify "
           "it: SOC 2 / compliance-driven testing, SAML/OAuth identity and API security, and "
           "OWASP-aligned agentic offensive tooling (/bug-reaper, MCP, security-focused agents) "
           "covering prompt-injection and AI/LLM red-teaming with a zero-false-positive "
           "bias. I turn attacker pathways and compliance requirements into observable, tested, "
           "well-bounded controls teams can trust in production \u2014 Rust, AWS, and the reliability "
           "mindset that makes security verification repeatable, not anecdotal.")

EXPERIENCE = [
    ("Security Engineer / Agentic Security Contributor (Open-Source)",
     "ZeroClaw Labs (github.com/zeroclaw-labs/zeroclaw)  \u00b7  Rust  \u00b7  32.2k stars",
     "2026 \u2013 Present", [
        "Run agentic security testing and verification against the codebase using offensive AI skills "
        "(/bug-reaper) \u2014 evidence-based web2 bug-bounty methodology that finds only real, triage-able "
        "bugs: IDOR/access control, auth/session bypass, SSRF, XSS, SQLi/NoSQLi, RCE, and API/GraphQL "
        "flaws. 4-phase workflow (recon \u2192 audit \u2192 validate \u2192 report); every finding requires a "
        "working PoC with zero false positives.",
        "Build and operate a security-focused agent stack (LLM agents + MCP tool servers + Unix-domain-socket "
        "JSON-RPC) to automate vulnerability verification across the codebase, closing the loop between "
        "discovery and verified fix.",
        "Contributed architectural review of a multi-user auth & isolation PR (62 files, 6,684 additions) \u2014 "
        "peercred, native pairing, SSH challenge-response, and OIDC providers; deny-by-default permission "
        "profiles; principal isolation at RPC dispatch. Mapped the workspace_id multi-tenant axis into the "
        "principal abstraction to avoid a second security migration.",
     ]),
    ("Senior Software Engineer / QA Lead / Product Security & Compliance",
     "Knowledgecity LLC  \u00b7  Remote  \u00b7  AWS / Postgres / React",
     "Dec 2020 \u2013 Aug 2025", [
        "Owned and drove the SOC 2 Type II filing across security, engineering, and operations \u2014 mapped "
        "controls (access, change management, logical & physical security, availability, confidentiality, "
        "privacy), gathered evidence from AWS / CI/CD / identity systems, closed gaps, and managed the "
        "auditor relationship through successful certification.",
        "Led product/integration security: shipped SAP, Oracle, Workday, Coursera, UKG, and Zoom integrations "
        "hardened across SAML, OAuth, SFTP, and custom REST APIs \u2014 enforcing identity, session, and API "
        "security boundaries across partner auth models and data flows.",
        "Ran white-box security testing across integration, backend, API, database, and frontend surfaces; "
        "built the CI/CD test-and-verification pipeline (Cypress, Selenium, Postman, JUnit, S3) used to "
        "prove security and compliance controls continuously.",
        "Designed security regression suites, health dashboards, and alerting to detect and prove remediation "
        "across multi-environment deployments; reduced technical debt behind security controls.",
        "Mentored and trained the test automation team; ran code reviews with a security-first lens; raised "
        "engineering standards.",
     ]),
    ("Senior Software Engineer II / Presales Engineering",
     "RealNetworks  \u00b7  Seattle, WA  \u00b7  Streaming Media Platform",
     "", [
        "QA on an advanced research team evaluating distributed system behavior across consumer "
        "appliances, mobile platforms, stream servers, and cellular networks \u2014 complex, multi-component "
        "reliability and protocol scenarios.",
        "Global presales engineering: turned product capabilities into customer solutions across diverse "
        "technical environments; trained new hires; led cross-functional collaboration.",
     ]),
    ("Senior Software Test Engineer IV",
     "Microsoft  \u00b7  Redmond, WA  \u00b7  Windows Media Server",
     "", [
        "White-box testing and automation for Windows Media Server, Windows 98/NT \u2014 security and "
        "verification frameworks for complex system and network-protocol testing.",
        "Deep debugging across server infrastructure, network protocols, and media codecs.",
     ]),
    # (IBM 1998 omitted \u2014 single bullet, same reliability mindset covered in Microsoft role)
]

SKILLS = [
    ("Application & Web Security Testing", 92),
    ("Identity & Access Mgmt (SAML, OAuth, OIDC)", 90),
    ("SOC 2 & Compliance (Evidence, Audits)", 88),
    ("Agentic Offensive Security (bug-reaper, MCP)", 90),
    ("White-Box Code Review & Secure SDLC", 91),
    ("Cloud Security (AWS, IAM, Logging)", 84),
]

TAGS = [
    "Application Security", "Offensive Security", "Bug Bounty", "bug-reaper",
    "White-Box Testing", "Secure Code Review", "Vulnerability Assessment",
    "SOC 2", "Compliance", "Access Control", "IDOR", "Auth Bypass",
    "SSRF", "XSS", "SQLi", "NoSQLi", "RCE", "API / GraphQL Security",
    "SSO", "SAML", "OAuth", "OIDC", "SFTP", "MCP (Model Context Protocol)",
    "Rust", "Python", "TypeScript", "Node.js", "React",
    "PostgreSQL", "AWS (IAM, ECS, S3)", "Cloud Security", "CI/CD", "Cypress",
    "Selenium", "Postman", "JUnit", "Penetration Testing", "Threat Modeling",
    "Risk Assessment", "Audit Evidence", "Docker", "Git",
]

STRENGTHS = [
    ("Evidence-based vulnerability discovery",
     "Use agentic offensive tooling (bug-reaper, MCP, LLM agents) to find only real, exploitable bugs \u2014 "
     "every finding requires a working PoC and passes triage, with aggressive false-positive elimination."),
    ("Identity, access & API security",
     "Enforce SAML, OAuth, and OIDC boundaries and principal/deny-by-default isolation across multitenant "
     "products and third-party integrations \u2014 closing access-control and auth-bypass classes."),
    ("Compliance & audit (SOC 2)",
     "Own SOC 2 Type II filing end-to-end: control mapping, evidence collection, gap closure, and auditor "
     "management through successful certification."),
    ("Secure SDLC & white-box testing",
     "Deep white-box and code-review testing across backend, API, database, and frontend surfaces, backed by "
     "automated CI/CD security verification."),
    ("Cross-functional leadership",
     "Lead as QA Lead, product/compliance owner, and presales engineer \u2014 partnering daily with PMs, "
     "designers, developers, and auditors."),
]

EDUCATION = [
    "Associate Degree, Victor Valley College",
    "California Notary Commission",
    "Toastmasters International",
]

TAG_SECTIONS = [
    ("Offensive & Application Security", [
        "bug-reaper", "Bug Bounty", "Penetration Testing", "OWASP Top 10",
        "IDOR", "Auth Bypass", "SSRF", "XSS", "SQLi", "NoSQLi", "RCE",
        "SSTI", "Prompt Injection", "AI Red-Teaming", "API / GraphQL",
        "White-Box Testing", "Secure Code Review", "Threat Modeling",
        "HackerOne", "Bugcrowd", "Working PoC",
    ]),
    ("Identity & Compliance", [
        "SOC 2 (Type II)", "SAML", "OAuth", "OIDC", "SSO", "SFTP",
        "Permission Profiles", "Principal Isolation", "Deny-by-Default",
        "Risk Assessment", "Audit Evidence",
    ]),
    ("Platform & Backend", [
        "LLM Agents", "MCP (Model Context Protocol)", "JSON-RPC",
        "Unix Domain Sockets", "OpenCode", "Codex Agents", "Hermes Agent",
        "Rust", "Python", "Node.js", "React", "PostgreSQL",
        "AWS (IAM, ECS, S3)", "Cloud Security", "Docker", "Kubernetes",
        "Terraform / IaC", "Git",
    ]),
]

COMPETENCIES = [
    ("App & Web Security",
     "OWASP-aligned web2: IDOR, auth, SSRF, XSS, SQLi, RCE, API/GraphQL."),
    ("Identity & Access",
     "SAML, OAuth, OIDC; deny-by-default principal isolation."),
    ("Compliance (SOC 2)",
     "End-to-end Type II: controls, evidence, audits."),
    ("Agentic Offensive",
     "LLM agents + MCP; /bug-reaper; AI red-teaming."),
    ("White-Box SDLC",
     "White-box + code review across backend, API, DB, frontend."),
    ("Cloud Security",
     "AWS IAM/ECS/S3; Docker, Kubernetes, Terraform."),
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
        "Eugene L. Buchanan  \u00b7  Cyber Security Engineer \u2014 Offensive & AI Secure Development")
    canvas.drawRightString(PW - MR, 24, "Page %d" % doc.page)
    canvas.restoreState()


def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Eugene_Buchanan_Resume.pdf")

    doc = BaseDocTemplate(out_path, pagesize=letter,
                          leftMargin=ML, rightMargin=MR,
                          topMargin=HEADER_H + TOP_GAP, bottomMargin=BODY_BOTTOM,
                          title="Eugene L. Buchanan \u2014 Cyber Security Engineer Resume",
                          author="Eugene L. Buchanan",
                          subject="Cyber Security Engineer \u2014 Offensive Security, Application & Product Security, AI Secure Development (Apple Valley, CA)",
                          keywords="Cyber Security, Offensive Security, Application Security, SOC 2, AI Security, Rust, Bug Bounty, Vulnerability Assessment")
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
    comp_col = [Paragraph("<b>%s</b> \u2014 %s" % (name, desc), comp_style)
                for name, desc in COMPETENCIES]
    expertise = Table([[bars_col, comp_col]], colWidths=[FW - 215, 215])
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

    # ── Key Strengths — interactive localization panel (under Tech Stack)
    story.append(SectionTitle("Key Strengths"))
    story.append(Spacer(1, 1))
    story.append(L10nPanel())
    story.append(Spacer(1, 1))

    # ── Experience ────────────────────────────────────────
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
