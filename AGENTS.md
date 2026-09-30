# AGENTS.md — eugeneb50 Resume Generator

## Project Overview
Personal portfolio project: Python scripts generate polished PDF resumes (Staff AI Engineer visual in English + Spanish, IT Support Specialist ops visual), ATS-friendly graphics-free resumes, and a cover letter using **reportlab** + **Pillow**. Targeted at Staff AI Engineer roles, with the ops track positioned for IT Support Specialist roles.

## Quick Commands

| Task | Command |
|------|---------|
| Build general resume (EN visual) | `./.venv/bin/python build_resume.py` |
| Build general resume (ES visual) | `./.venv/bin/python build_resume_es.py` |
| Build ATS-friendly resume | `./.venv/bin/python build_resume_ats.py` |
| Build ops (IT Support) resume | `./.venv/bin/python build_resume_ops.py` |
| Build ops ATS resume | `./.venv/bin/python build_resume_ops_ats.py` |
| Build cover letter | `./.venv/bin/python build_cover.py` |
| Build all | `./.venv/bin/python build_resume.py && ./.venv/bin/python build_cover.py` |

Outputs: `Eugene_Buchanan_Resume.pdf`, `Eugene_Buchanan_Resume_ES.pdf`, `Eugene_Buchanan_Resume_ATS.pdf`, `Eugene_Buchanan_Resume_Ops.pdf`, `Eugene_Buchanan_Resume_Ops_ATS.pdf`, `Eugene_Buchanan_Cover_Letter.pdf`

## ATS-Friendly Resume (`build_resume_ats.py`)
- Deliberately graphics-free: single column, no images/charts/tables, standard section headings, one font family (Helvetica base-14), "Month YYYY" dates, acronyms spelled out on first use, plain-English copy rewritten with the deslop skill.
- Full job history, source-faithful, no invented claims (HIPAA/IAM/Okta/RBAC/PII material removed — none of it is in the source). Software-Engineering section in chronological flow: Knowledgecity → Business Consultant/Medico/Foremost → Geek Squad → Freelance AMP → IT Manager → RealNetworks → Microsoft/IBM/Keene; then Additional Roles (Alternative Energy → Tierrachain → Water Board → ZeroClaw with all 4 PR statuses) → Education. 3 pages.
- Tight section spacing (`h2` spaceBefore 6, `job` spaceBefore 5, bullets spaceAfter 1) + no trailing spacer — the file is at exactly 3 pages; additions will spill. Dropping the HS diploma line or trimming the KC toolchain bullet are the approved levers.
- **Employer-facing copy rule (no negative disclaimers):** rendered PDF text must NEVER contain "no X claim", "honest gap", "gap vs. requisition", or any sentence advertising what the candidate lacks. Missing JD keywords are handled by omission + positive transferable framing (show the adjacent real experience, never name the missing tech as a deficiency). Gap analysis lives ONLY in script docstrings/comments as build notes — it must not leak into `SUMMARY`, `SKILLS`, `PARAGRAPHS`, `QUALIFICATIONS`, or any `story.append()` content.
- **STAR bullets + no port trivia:** experience bullets follow STAR in one short line each — Situation (the problem), Task/Action (what was built), Result (the outcome). Never print internal port numbers (e.g. `:7676`) or other run-local trivia in employer-facing copy.

## Environment
- **Python**: 3.14 (via `.venv`)
- **Dependencies**: `reportlab==5.0.0`, `pillow==12.3.0`, `charset-normalizer==3.4.9`, `arabic-reshaper==3.0.0`, `python-bidi`, `segno`
- **System fonts required**: DejaVuSans family at `/usr/share/fonts/TTF/` (`DejaVuSans.ttf`, `DejaVuSans-Bold.ttf`, `DejaVuSans-Oblique.ttf`); Noto Sans Arabic at `/usr/share/fonts/noto/NotoSansArabic-Regular.ttf` (RTL panel). zh/ja use reportlab CID fonts `STSong-Light` / `HeiseiKakuGo-W5` (no file needed).
- **Profile photo**: `pic.jpg` in repo root (auto-cropped to circle)

## Architecture Notes
- **No shared module** — each script duplicates the design system (colors, flowables, helpers). Changes to visual style must be applied in all files.
- **Page-budget discipline**: all PDFs are at exact page counts (EN 2, ES 2, ATS 3, Ops 2, Ops ATS 2). Page 2 of the EN visual has ~0pt slack and page 2 of the visual ops resume has ~8pt slack; the ATS files rely on tight spacing (`h2` spaceBefore 6, `job` spaceBefore 5, bullets spaceAfter 1) and no trailing spacers — verify with pypdf after any content change.

## Key Design System Components (duplicated across scripts)
- `HeaderBand` / `LetterHead` — gradient header with circular photo/monogram
- `SectionTitle` — colored accent bar + title + rule
- `SkillBar` — label + percentage + gradient progress bar
- `TagCloud` — wrapping pill tags
- `experience_card()` — role/date table + company + bullet list with left rule
- `SkillRadar` (resume) — spider/radar chart of skill strengths (spider `symbol` names are capitalized, e.g. `"Circle"`)
- `L10nPanel` (resume) — interactive Key Strengths localization: PDF form radio buttons (`l10n_lang` group) whose `/AA` JavaScript actions toggle the visibility of 7 read-only multiline text fields (`l10n_dd_<code>`, one per language; EN visible by default, `/F 4`, others hidden `/F 6`). Each field carries a **pre-rendered `/AP /N` appearance Form XObject** (`l10n_ap_<code>`) drawn via `canv.beginForm`/`endForm` (white fill + navy border + wrapped lines), so every viewer renders the full multi-line block without relying on Acrobat regenerating the appearance. Field `V`/`DV` = `PDFString("\n".join(lines))`; `maxlen=0` (no `/MaxLen`, which previously truncated browser display at 100 chars). `/DR` fonts registered via `_build_form_dr` (DejaVu subset for Latin, Noto Arabic subset for RTL, CID `STSong-Light`/`HeiseiKakuGo-W5` for zh/ja). Arabic is reshaped via `arabic_reshaper` + `python-bidi` and drawn right-aligned. `Canvas._addAnnotation` is monkey-patched to inject `/AA` into the radio widgets.
- `qr_block()` (resume) — right-aligned GitHub QR (`segno.make_qr` → themed PNG → `RLImage` + caption) in the boxed area under Education at the bottom of page 2; encodes `https://github.com/eugeneb50/eugeneb50/`
- `interests_block()` (resume) — boxed "Other Interests" panel (Renewable Energy, Permaculture, Real Estate, Tango Dancing) beside the QR
- `ProfitChart` (cover) — `VerticalBarChart` of parabolic value growth; `CategoryAxis` is abstract — configure the auto-created `bc.categoryAxis`/`bc.valueAxis` instead. Cover letter content (`RECIPIENT`, `SUBJECT`, `PARAGRAPHS`, `CLOSING`, `CHART_TITLE`) is a generic template to edit per application.
- `draw_gradient()` — stepwise rectangle gradient helper
- `make_circular_photo()` — PIL crop + alpha mask → temp PNG

## Colors (resume uses purple/pink/navy palette; cover letter uses the same design system)
- `NAVY`/`NAVY2`, `PURPLE`, `PINK`, `TEAL`/`TEAL_D`, `LIGHT`, `GREY`, `DARK`, `INK`, `MUTE`, `RULE`, `TRACK`

## Common Gotchas
1. **Font path hardcoded** — fails if DejaVuSans not at `/usr/share/fonts/TTF/`
2. **Photo path hardcoded** — expects `pic.jpg` in same directory as script
3. **No requirements.txt** — dependencies only in `.venv`; recreate with `pip install reportlab pillow segno arabic-reshaper python-bidi charset-normalizer`
4. **Page geometry constants** differ slightly between scripts (HEADER_H, margins)
5. **Temp files** — `make_circular_photo` creates temp PNGs in `/tmp/` (cleaned on reboot)

## Making Changes
- Visual tweaks: edit all `.py` files (no shared library)
- Content updates: modify `EXPERIENCE`, `SKILLS`, `TAGS`, `STRENGTHS`, `EDUCATION`, `SUMMARY` constants in each script
- Adding sections: follow existing `story.append()` pattern in `build()` function