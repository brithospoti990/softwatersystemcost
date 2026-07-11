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

## Affiliate links — single source of truth
All SpringWell links point to internal `/go/<product>` routes, resolved by the
`redirects` block in `vercel.json` (affid=40 + oid per product). To change a
destination, edit vercel.json ONCE — no page edits.
⚠️ BEFORE LAUNCH: replace each destination with the exact tracking URL from the
Everflow dashboard link generator for that product/oid. The paths here follow the
product-path convention but must be verified against the dashboard output.
Anchor convention (already applied): rel="sponsored nofollow noopener" target="_blank".

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
- [ ] Replace the six `/go/` destinations in `vercel.json` with tracking URLs from the Everflow dashboard
- [ ] `npm run check` passes locally (CI runs the same on every push)
- [ ] Search Console: add property, submit `sitemap.xml`
- [ ] Spot-check `/embed/cost-calculator/` inside an iframe on a test page

### CI
`.github/workflows/qa.yml` runs the full QA suite (div balance, FAQ length,
affiliate rel attributes, all calculator branches) on every push and PR.
A red X on a commit = do not deploy that commit.
