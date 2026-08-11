# AGENTS.md — eugeneb50 Resume Generator

## Project Overview
Personal portfolio project: three Python scripts generate polished PDF resumes/cover letters using **reportlab** + **Pillow**. Targeted at Staff AI Engineer roles (ClickUp-specific versions exist).

## Quick Commands

| Task | Command |
|------|---------|
| Build general resume | `./.venv/bin/python build_resume.py` |
| Build ClickUp resume | `./.venv/bin/python build_resume_clickup.py` |
| Build ClickUp cover letter | `./.venv/bin/python build_cover_clickup.py` |
| Build all | `./.venv/bin/python build_resume.py && ./.venv/bin/python build_resume_clickup.py && ./.venv/bin/python build_cover_clickup.py` |

Outputs: `Eugene_Buchanan_Resume.pdf`, `ClickUp_Eugene_Buchanan_Resume.pdf`, `ClickUp_Eugene_Buchanan_Cover_Letter.pdf`

## Environment
- **Python**: 3.14 (via `.venv`)
- **Dependencies**: `reportlab==5.0.0`, `pillow==12.3.0`, `charset-normalizer==3.4.9`
- **System fonts required**: DejaVuSans family at `/usr/share/fonts/TTF/` (`DejaVuSans.ttf`, `DejaVuSans-Bold.ttf`, `DejaVuSans-Oblique.ttf`)
- **Profile photo**: `pic.jpg` in repo root (auto-cropped to circle)

## Architecture Notes
- **No shared module** — each script duplicates the design system (colors, flowables, helpers). Changes to visual style must be applied in all three files.
- **Scripts are self-contained** — no imports between them, no config files.
- **Two-page layout**: cover page (header band + photo) + content page(s) with footer.

## Key Design System Components (duplicated across scripts)
- `HeaderBand` / `LetterHead` — gradient header with circular photo/monogram
- `SectionTitle` — colored accent bar + title + rule
- `SkillBar` — label + percentage + gradient progress bar
- `TagCloud` — wrapping pill tags
- `experience_card()` — role/date table + company + bullet list with left rule
- `draw_gradient()` — stepwise rectangle gradient helper
- `make_circular_photo()` — PIL crop + alpha mask → temp PNG

## Colors (ClickUp versions use purple/pink/navy palette; general uses teal/navy)
- `NAVY`/`NAVY2`, `PURPLE`, `PINK`, `TEAL`/`TEAL_D`, `LIGHT`, `GREY`, `DARK`, `INK`, `MUTE`, `RULE`, `TRACK`

## Common Gotchas
1. **Font path hardcoded** — fails if DejaVuSans not at `/usr/share/fonts/TTF/`
2. **Photo path hardcoded** — expects `pic.jpg` in same directory as script
3. **No requirements.txt** — dependencies only in `.venv`; recreate with `pip install reportlab pillow`
4. **Page geometry constants** differ slightly between scripts (HEADER_H, margins)
5. **Temp files** — `make_circular_photo` creates temp PNGs in `/tmp/` (cleaned on reboot)

## Making Changes
- Visual tweaks: edit all three `.py` files (no shared library)
- Content updates: modify `EXPERIENCE`, `SKILLS`, `TAGS`, `STRENGTHS`, `EDUCATION`, `SUMMARY` constants in each script
- Adding sections: follow existing `story.append()` pattern in `build()` function