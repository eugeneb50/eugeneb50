# Deploying PhaseSave to phasesave.com

The site is **plain static files** — no WordPress, no build step, no database.
Everything under this folder maps directly to the root of `phasesave.com`.

```
phasesave-site/
├── index.html              ← home page (root)
├── 404.html                ← custom not-found page
├── blog/
│   └── zero-water-data-centers-coachella-valley/
│       └── index.html      ← journal post
├── css/styles.css
├── js/app.js
├── assets/                 ← images + logo + og.jpg
├── robots.txt
├── sitemap.xml
├── llms.txt                ← AI/answer-engine digest
├── .htaccess               ← Apache/cPanel redirects + headers
├── _redirects              ← Netlify/Cloudflare Pages redirects
└── DEPLOY.md
```

## Option A — Replace WordPress on your existing host (cPanel)

1. Back up the current WordPress site (files + database).
2. Delete (or move aside) everything in `public_html`.
3. Upload the contents of `phasesave-site/` into `public_html/` (so `index.html`
   sits at the domain root).
4. Keep `.htaccess` — it 301-redirects the old WordPress URLs
   (`/service/solar/`, `/about/`, `/contact/`, etc.) to the new pages so you
   keep your search rankings.
5. Confirm HTTPS is on and `https://phasesave.com/` loads.

## Option B — Static host (recommended)

Netlify, Cloudflare Pages, or Vercel:

1. Point the repo at the `phasesave-site/` folder as the publish directory.
2. Configure the custom domain `phasesave.com` (and `www` → apex).
3. Netlify/Cloudflare pick up `_redirects` automatically for the legacy URLs.
4. In Cloudflare, enable "Always Use HTTPS".

## After going live

1. **Google Search Console** → add `phasesave.com`, submit `sitemap.xml`.
2. Verify the **canonical** tag is `https://phasesave.com/` (it already is).
3. Confirm the social card loads: `https://phasesave.com/assets/og.jpg`.
4. Test the redirects: `/about/`, `/contact/`, `/service/solar/`.
5. Keep `llms.txt` and `sitemap.xml` updated when you add pages.

## Domain settings

- Canonical domain (already set in markup): `https://phasesave.com/`
- Journal post: `https://phasesave.com/blog/zero-water-data-centers-coachella-valley/`
- Apex → prefer serving from `phasesave.com` (no `www`) to match the canonicals.
