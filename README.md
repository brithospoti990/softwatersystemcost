# softwatersystemcost.com — production static site

Converted from the design team's .dc.html prototypes to plain static HTML/CSS/JS.
Deploy target: Vercel (no build step — the repo IS the site).

## Structure
- `index.html` — T1 homepage (live calculator hero)
- `water-softener-system-cost/` — T2 pillar (A1, live)
- `water-softener-maintenance-cost/` — T3 money page (live)
- `templates/brand-expose/` — T4 template ([Brand] placeholders, noindexed; duplicate + fill per brand)
- `calculators/cost-calculator/` — T5 tool page · `calculators/` hub
- `embed/cost-calculator/` — embeddable widget route (attribution link = link building)
- `data/water-hardness-study/` — T6 data study
- `about/`, `how-we-make-money/`, `privacy/`, `brands/` hub, `404.html`
- `styleguide/` — component library (noindexed). Copy markup from here for new pages.
- `assets/site.css` — the entire design system (tokens + components)
- `assets/calc-core.js` — cost model + sizing math + ZIP lookup
- `assets/calculator.js` — mounts on any `<div data-calc data-variant="full|embed">`

## Affiliate link cloaking — /pick/ routes (single source of truth)
All SpringWell links use internal `/pick/<slug>` routes (e.g. `/pick/salt-softener`).
- `pick-links.json` = the source of truth: slug → Everflow tracking URL (real dashboard
  links, full 33-product catalog, affid=40). Edit this file, then run
  `python3 qa/gen_redirects.py` to regenerate the redirects block in `vercel.json`.
- Redirects are 302 (`permanent: false`) — no link equity passed, destinations swappable.
- `/pick/*` responses carry `X-Robots-Tag: noindex, nofollow`; robots.txt disallows `/pick/`.
- Anchor convention (QA-enforced): `rel="sponsored nofollow noopener" target="_blank"`.
- QA fails the build if any page links a /pick/ slug missing from pick-links.json.
Writer usage: pick the most specific product slug for the context — `salt-softener` for
SS CTAs, `salt-free-softener`/`futuresoft` on conditioner content, combo slugs on combo
content, `test-kit` before sizing advice, `replacement-prefilters` on maintenance topics.
Category/utility slugs (`softeners`, `shop`, `reviews`, `well-water`) only when no single
product fits.

## Mobile rules for new articles (QA-enforced)
The site is mobile-majority; CI fails builds that break these:
1. Every `<table>` goes inside `.quote-sheet` or `.data-table-wrap` (horizontal scroll + sticky first column on phones). Never a bare table.
2. No fixed inline widths over 390px (`max-width` is fine).
3. Every `<img>` needs `width` + `height` attributes (CLS).
4. Charts: prefer the `.bar-row` pattern or `.chart-panel` blocks — they reflow; don't embed wide SVGs with fixed viewport-busting widths.
5. Keep Quote Sheet item names ≤60 chars (schema-enforced) so rows stay readable at 360px.
6. Interactive embeds: use `data-calc` variants only; they stack below 760px automatically.

## Adding an article
1. Generate content with the master article prompt (Input Block per topical map).
2. Copy the matching template page, replace body sections, keep section order.
3. Quote Sheets: reuse `.quote-sheet` markup (styleguide has canonical block).
4. Every figure needs a line in the Sources block. FAQ answers ≤300 chars.
5. Add URL to `sitemap.xml`.

## QA before every deploy (portfolio protocol)
- `python3 qa/qa_checks.py` — div balance walk, FAQ length, affiliate rel check
- `node qa/calc.test.mjs` — jsdom: all calculator branches + data-result assertions
- Render check (wkhtmltoimage) on changed pages

## Known TODOs
- Self-host fonts (5 woff2 subsets) to replace Google Fonts CDN — perf spec §7
- Replace calc-core ZIP stub with generated `assets/data/zip-hardness.json` (USGS)
- Real avatar illustration to replace inline line-art SVG placeholder
- Verify /go/ destinations against Everflow dashboard (see above)

## Deploy: GitHub + Vercel (exact steps)

### 1. Push to GitHub
```bash
# from inside this folder (repo is already initialized and committed)
git remote add origin git@github.com:brithospoti990/softwatersystemcost.git
git push -u origin main
```
(Create the empty repo on GitHub first: New repository → `softwatersystemcost` → private → no README/gitignore.)

### 2. Import to Vercel
1. Vercel dashboard → Add New → Project → import `brithospoti990/softwatersystemcost`
2. Framework preset: **Other** · Build command: **(leave empty)** · Output directory: **(leave empty / root)**
3. Deploy. `vercel.json` handles clean URLs, trailing slashes, /go/ redirects, headers, caching.

### 3. Domain
Vercel project → Settings → Domains → add `softwatersystemcost.com` and `www` (redirect www → apex).
At the registrar: A record `76.76.21.21` for apex, CNAME `cname.vercel-dns.com` for www.

### 4. Before flipping DNS — launch gate
- [ ] `npm run check` passes locally (CI runs the same on every push)
- [ ] Search Console: add property, submit `sitemap.xml`
- [ ] Spot-check `/embed/cost-calculator/` inside an iframe on a test page

### CI
`.github/workflows/qa.yml` runs the full QA suite (div balance, FAQ length,
affiliate rel attributes, all calculator branches) on every push and PR.
A red X on a commit = do not deploy that commit.
