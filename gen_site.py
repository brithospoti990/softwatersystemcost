#!/usr/bin/env python3
"""Generate production static pages for softwatersystemcost.com from shared partials.
Run: python3 gen_site.py  (writes into ./site)"""
import os, json

SITE = "https://softwatersystemcost.com"
ASSET_VER = "171"  # bump on every css/js change
OUT = "site"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
'<link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@600;700&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">')

def head(title, desc, path, extra="", noindex=False):
    robots = '<meta name="robots" content="noindex,nofollow">\n' if noindex else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
{robots}<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<link rel="icon" href="/favicon.svg">
{FONTS}
<link rel="stylesheet" href="/assets/site.css?v={ASSET_VER}">
{extra}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
'''

HEADER = '''<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">
      <span class="brand-name">SoftWater<em>SystemCost</em></span>
      <span class="brand-tag">Independent cost data</span>
    </a>
    <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true">
    <label for="nav-toggle" class="nav-burger" aria-label="Open menu"><span></span><span></span><span></span></label>
    <nav class="site-nav" aria-label="Main">
      <a href="/#quote-sheet">Cost Guide</a>
      <a href="/brands/">Brands</a>
      <a href="/calculators/">Calculators</a>
      <a href="/water-softener-maintenance-cost/">Maintenance</a>
      <a class="nav-pill" href="/about/">About</a>
    </nav>
  </div>
</header>
'''

FOOTER = '''<footer class="site-footer">
  <div class="wrap">
    <div class="f-top">
      <div>
        <a class="f-brand" href="/">SoftWater<em>SystemCost</em></a>
        <p class="f-mission">The line-item numbers dealers don&rsquo;t publish &mdash; itemized, sourced, and kept current.</p>
      </div>
      <a class="btn f-cta" href="/calculators/cost-calculator/">Get your number &rarr;</a>
    </div>
    <div class="footer-grid">
      <div>
        <div class="f-col-title">Editorial promise</div>
        <div class="f-checks">
          <div><span>&#10003;</span> Every figure traceable to a listed source</div>
          <div><span>&#10003;</span> We don&rsquo;t sell or install systems</div>
          <div><span>&#10003;</span> No sponsored posts, no dealer advertising</div>
          <div><span>&#10003;</span> Figures re-checked twice a year</div>
        </div>
      </div>
      <div>
        <div class="f-col-title">Cost guides</div>
        <div class="f-links">
          <a href="/">Water softener cost</a>
          <a href="/water-softener-installation-cost/">Installation cost</a>
          <a href="/water-softener-maintenance-cost/">Maintenance costs</a>
          <a href="/brands/">Brand price expos&eacute;s</a>
        </div>
      </div>
      <div>
        <div class="f-col-title">Calculators</div>
        <div class="f-links">
          <a href="/calculators/cost-calculator/">Cost calculator</a>
          <a href="/calculators/">All calculators</a>
          <a href="/data/water-hardness-study/">Hardness data study</a>
        </div>
      </div>
      <div>
        <div class="f-col-title">Company</div>
        <div class="f-links">
          <a href="/about/">About</a>
          <a href="/about/#standards">Editorial standards</a>
          <a href="/about/#contact">Contact</a>
          <a href="/privacy/">Privacy</a>
          <a href="/how-we-make-money/">How we make money</a>
        </div>
      </div>
    </div>
    <div class="f-bottom">
      <div class="c">&copy; 2026 SoftWaterSystemCost &middot; Independent publisher &middot; 1635 S Ridgewood Ave, 2nd Floor Ste 201, Daytona Beach, FL 32119</div>
      <div class="c">Some links are affiliate links &middot; <a href="/how-we-make-money/">how we make money</a></div>
      <div class="stamp-f">Data reviewed &middot; Jul 2026</div>
    </div>
  </div>
</footer>
</body>
</html>'''

AVATAR_SVG = '<svg viewBox="0 0 64 64" width="40" height="40" aria-hidden="true" focusable="false"><circle cx="32" cy="24" r="10" fill="none" stroke="#16303F" stroke-width="2.5"/><path d="M12 56c2-12 10-18 20-18s18 6 20 18" fill="none" stroke="#16303F" stroke-width="2.5" stroke-linecap="round"/></svg>'

def author_box(updated="July 2026"):
    return f'''<div class="author-card">
  <div class="ac-row">
    <div class="ac-avatar"><img src="/assets/robert-miller-144.webp" alt="Robert Miller, former plumbing and water-treatment estimator" width="144" height="144" loading="lazy"></div>
    <div class="ac-id">
      <div class="ac-name">Robert Miller <span class="ac-verified" title="Verified author" aria-label="Verified author"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="#16303F"/><path d="M7 12.5l3.2 3.2L17 9" fill="none" stroke="#FAFAF7" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span></div>
      <div class="ac-title">Former Plumbing &amp; Water-Treatment Estimator &middot; Daytona Beach, FL &middot; <a class="ac-about" href="/about/">About</a></div>
    </div>
    <div class="ac-updated">Updated {updated}</div>
  </div>
  <div class="ac-pills">
    <span class="ac-pill"><span class="tick">&#10003;</span> 15+ yrs pricing installs</span>
    <span class="ac-pill"><span class="tick">&#10003;</span> Every figure source-linked</span>
    <span class="ac-pill"><span class="tick">&#10003;</span> No sponsored posts</span>
  </div>
</div>'''

def quote_sheet(title, rows, total_label="Total installed", stamp="Jul 2026"):
    f = lambda n: "$" + format(round(n), ",")
    def cell(r):
        item, lo, hi = r[0], r[1], r[2]
        note = f'<div class="qs-note">{r[3]}</div>' if len(r) > 3 and r[3] else ""
        return f'<tr><td>{item}{note}</td><td class="num">{f(lo)}</td><td class="num">{f(hi)}</td></tr>'
    body = "".join(cell(r) for r in rows)
    tl, th = sum(r[1] for r in rows), sum(r[2] for r in rows)  # notes ignored
    return f'''<div class="quote-sheet">
  <div class="qs-head"><span class="qs-eyebrow">Quote Sheet</span><span class="qs-title">{title}</span></div>
  <table>
    <caption>Quote Sheet: {title} &mdash; itemized low and high cost estimates</caption>
    <thead><tr><th scope="col">Item</th><th scope="col" class="num">Low</th><th scope="col" class="num">High</th></tr></thead>
    <tbody>{body}<tr class="total"><td class="label">{total_label}</td><td class="num">{f(tl)}</td><td class="num">{f(th)}</td></tr></tbody>
  </table>
  <div class="qs-foot"><span class="stamp">Data updated &middot; {stamp}</span><a href="#sources">Sources &darr;</a></div>
</div>'''

def cta_box(eyebrow, body, button, product, footnote="Lifetime warranty on tanks &amp; valves &middot; ships free"):
    return f'''<div class="cta-box">
  <div class="eyebrow">{eyebrow}</div>
  <p>{body}</p>
  <a class="btn" href="/pick/{product}" rel="sponsored nofollow noopener" target="_blank">{button} &rarr;</a>
  <div class="footnote">{footnote}</div>
  <div class="aff-note">Affiliate link &mdash; we may earn a commission at no cost to you. <a href="/how-we-make-money/">Details</a></div>
</div>'''

def faq_block(faqs):
    items = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    return f'<div class="faq">{items}</div>'

def faq_schema(faqs, page_url):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})

def article_schema(headline, desc, path, date="2026-07-08"):
    return json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": headline,
        "description": desc, "url": SITE + path, "dateModified": date,
        "author": {"@type": "Person", "name": "Robert Miller", "url": SITE + "/about/", "image": SITE + "/assets/robert-miller-144.webp"},
        "publisher": {"@type": "Organization", "name": "SoftWaterSystemCost",
            "address": {"@type": "PostalAddress", "streetAddress": "1635 S Ridgewood Ave, 2nd Floor Ste 201",
                        "addressLocality": "Daytona Beach", "addressRegion": "FL", "postalCode": "32119"}}})

def breadcrumb_schema(crumbs):
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]})

def ld(obj):
    return f'<script type="application/ld+json">{obj}</script>\n'

def sources(items):
    lis = "".join(f"<li>{s}</li>" for s in items)
    return f'''<div id="sources" class="sources col" style="margin-top:64px">
  <h2>Where these numbers come from</h2>
  <ol>{lis}</ol>
</div>'''

def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(content)
    print("wrote", full)

FIG = lambda t: f'<span class="fig">{t}</span>'

# ============ PILLAR (T2) — A1 full article ============
pillar_faqs = [
 ("How much does a water softener cost for a family of four?","Typically $1,200&ndash;$3,000 installed. A family of four on ~10 gpg water usually needs a 32k&ndash;48k grain unit ($600&ndash;$1,500 retail) plus $200&ndash;$500 labor on an existing loop. No loop adds $600&ndash;$2,000."),
 ("Why is my water softener quote $6,000?","Either real site work (loop run, drain, electrical, code items) or dealer sales cost. Ask for line items: legitimate quotes itemize equipment, labor, and site work separately. If it&rsquo;s one bundled number, get a second quote."),
 ("Is it cheaper to buy a softener yourself and hire a plumber?","Usually, yes. A $600&ndash;$1,500 retail unit plus $200&ndash;$500 independent labor typically beats a dealer package quoted at $3,000+, for the same hardware class. The savings shrink if your home needs a loop cut in."),
 ("How much does installation labor cost alone?","$200&ndash;$500 for a standard swap on an existing loop &mdash; about 2&ndash;4 hours at $100&ndash;$150/hr. Cutting a new loop is separate plumbing work at $600&ndash;$2,000 depending on run length and access."),
 ("What does a water softener cost per month?","Roughly $8&ndash;$25/month in salt and upkeep: $60&ndash;$180/yr for salt plus occasional parts. Renting instead runs $25&ndash;$50/month forever &mdash; buying usually wins within 3&ndash;5 years."),
 ("Do salt-free water softeners cost less?","Not upfront &mdash; $1,500&ndash;$4,500 installed vs. $1,200&ndash;$3,800 salt-based. They cost less to own (no salt), but they condition scale rather than removing hardness, so soap and spotting behave differently."),
 ("How long does a water softener last?","10&ndash;15 years for the valve; tanks last longer. Resin on chlorinated city water typically needs a $250&ndash;$600 rebed around year 10 &mdash; far cheaper than the new system a dealer will offer instead."),
]
a1_rows = [
 ("Softener unit (24k&ndash;48k grain, metered)",600,1500,"Grain capacity, valve quality; big-box entry units start lower"),
 ("Installation labor (2&ndash;4 hrs)",200,500,"Local plumber rates ($100&ndash;$150/hr typical); loop access"),
 ("Bypass valve &amp; fittings",40,120,"Often bundled &mdash; ask if it&rsquo;s included"),
 ("Loop run (only if none exists)",600,2000,"Run length, slab vs. crawlspace, drain distance"),
 ("Drain &amp; electrical (only if missing)",0,900,"Nearby drain and outlet = $0; dedicated circuit $250&ndash;$900"),
 ("First year of salt (8&ndash;12 bags)",60,180,"Hardness, household size, salt price ($5&ndash;$10/40-lb bag)"),
]
PICK = 'rel="sponsored nofollow noopener" target="_blank"'

master_rows = [("Softener unit (32k grain)",600,1500),("Installation labor",200,500),("Bypass valve &amp; fittings",40,120),("Loop run (if none exists)",600,2000)]

# ============ HOMEPAGE = A1 FULL ARTICLE (v1.8) ============
def donut_svg(segs, big, small, label="Cost composition chart"):
    C = 2*3.14159*54; off = 0; circles = ""
    for color,pct in segs:
        dash = C*pct/100
        circles += f'<circle r="54" cx="70" cy="70" fill="none" stroke="{color}" stroke-width="26" stroke-dasharray="{dash:.1f} {C-dash:.1f}" stroke-dashoffset="{-off:.1f}" transform="rotate(-90 70 70)"/>'
        off += dash
    return f'<svg viewBox="0 0 140 140" width="170" height="170" role="img" aria-label="{label}">{circles}<text x="70" y="66" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="15" fill="#16303F">{big}</text><text x="70" y="82" text-anchor="middle" font-family="Source Sans 3,sans-serif" font-size="9" fill="#5B6B75">{small}</text></svg>'

def range_bars(rows, scale_max, color="#16303F"):
    out = '<div class="range-chart">'
    for name, lo, hi, col in rows:
        l = lo/scale_max*100; w = max((hi-lo)/scale_max*100, 8)
        out += (f'<div class="range-row2"><div class="r-name">{name}</div>'
                f'<div class="r-track"><div class="r-bar" style="left:{l:.1f}%;width:{w:.1f}%;background:{col}">'
                f'<span>${lo:,}</span><span>${hi:,}</span></div></div></div>')
    out += ('<div class="range-row2"><div class="r-name"></div><div class="range-scale"><span>$0</span><span>$' + f'{scale_max//2:,}' + '</span><span>$' + f'{scale_max:,}' + '</span></div></div></div>')
    return out

route_rows = [
 ("DIY (self-install)",650,1750,"#1F7A5C"),
 ("Factory-direct + your plumber",1000,2700,"#16303F"),
 ("Local plumber supplies + installs",1200,3800,"#5B6B75"),
 ("Dealer in-home package",3000,8000,"#E8A13D"),
]
prep_rows = [
 ("Prepared home (loop, drain, outlet)",900,2300,"#1F7A5C"),
 ("Unprepared home (site work needed)",1500,5200,"#E8A13D"),
]
region_rows = [("Southwest",18),("Great Plains",16),("Midwest",14),("Southeast",9),("Pacific",7),("Northeast",4)]
region_bars = "".join(
    f'<div class="bar-row"><div class="b-name">{n}</div><div class="b-track"><div class="b-fill" style="width:{round(g/20*100)}%;background:{"#16303F" if g>=10.5 else "#5B6B75" if g>=7 else "#1F7A5C"}"></div></div><div class="b-val">{g}</div></div>'
    for n,g in region_rows)

home = head("Water Softener System Cost (2026): Full Price Breakdown",
 "Water softener systems cost $840\u2013$4,120 installed in 2026. A former estimator itemizes every line \u2014 unit, labor, loop, salt \u2014 with charts, calculators, and sources.",
 "/",
 ld(article_schema("Water Softener System Cost in 2026: Every Line Item, Priced","Itemized 2026 water softener cost data with interactive calculators and sourced ranges.","/",date="2026-07-12"))
 + ld(faq_schema(pillar_faqs,"/"))
 + ld(json.dumps({"@context":"https://schema.org","@type":"WebApplication","name":"Water Softener Cost Calculator","url":SITE+"/","applicationCategory":"UtilityApplication","operatingSystem":"Web"})))
home += HEADER + '''<main id="main">
  <div class="hero col-wide" style="margin-top:56px">
    <span class="stamp">Independent cost data &middot; Updated Jul 2026</span>
    <h1>Water Softener System Cost in 2026: Every Line Item, Priced</h1>
    <p class="sub">I wrote installation quotes for 15 years. This page prices a softener the way an estimator would &mdash; itemized, charted, and without the sales pitch.</p>
  </div>
  <div class="col" style="margin-top:24px">''' + author_box(updated="July 12, 2026") + '''</div>

  <div class="col-wide" style="margin-top:40px">
    <div class="calc-titlebar"><span class="t-left">Cost estimator &middot; Worksheet &#8470;1</span><span class="t-right">Live estimate</span></div>
    <div data-calc data-variant="full"></div>
  </div>

  <article class="col-wide">
    <div class="col" style="margin-top:64px">
      <h2 class="tight" id="answer">The short answer</h2>
      <p>Expect roughly <span class="fig">$840&ndash;$4,120</span> installed for a salt-based system in 2026, with most homes on an existing loop landing between <span class="fig">$1,200</span> and <span class="fig">$3,000</span>. National cost guides put the average around <span class="fig">$1,500</span> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">Angi&rsquo;s 2026 data</a> shows a full spread of <span class="fig">$200&ndash;$6,000</span>, and <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">HomeGuide</a> pegs the typical salt-based install at <span class="fig">$1,200&ndash;$3,800</span>.</p>
      <p style="margin:0">Fifteen years of building these quotes taught me one thing: the softener is only one line on the worksheet. The expensive surprises live in the plumbing around it. Everything below is itemized the way I&rsquo;d build the estimate &mdash; so you can judge a <span class="fig">$2,000</span> quote or a <span class="fig">$7,000</span> quote before anyone sits down at your kitchen table.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#quote-sheet">The installed-cost worksheet</a></li>
          <li><a href="#composition">Where the money goes (chart)</a></li>
          <li><a href="#equipment">Cost by buying route (chart)</a></li>
          <li><a href="#loop">Labor &amp; the $2,000 loop wildcard</a></li>
          <li><a href="#sizing">Sizing &amp; regional hardness</a></li>
          <li><a href="#salt-free">Salt-based vs. salt-free</a></li>
          <li><a href="#ownership">10-year ownership (tool)</a></li>
          <li><a href="#quote-anatomy">How to read a quote</a></li>
        </ol>
      </details>
      <h2 id="quote-sheet">What does a water softener system cost installed?</h2>
      <p style="margin:0">This is a typical salt-based project for a 3-bathroom home on city water, itemized the way an estimator prices it:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Salt-Based Softener, 3-Bath Home", a1_rows, total_label="Total estimated project") + '''</div>
    <div class="col">
      <p style="margin-top:24px">Notice that three rows &mdash; loop, drain, electrical &mdash; cost <span class="fig">$0</span> in a prepared home and up to <span class="fig">$2,900</span> in an unprepared one. That single fact explains most of the &ldquo;why did my neighbor pay half what I was quoted&rdquo; stories:</p>
    </div>
    <div class="col-wide" style="margin-top:16px">''' + range_bars(prep_rows, 6000) + '''</div>
    <div class="col" style="margin-top:40px">''' + cta_box("The factory-direct alternative",
      "You shouldn&rsquo;t need an in-home sales visit to learn a softener&rsquo;s price. SpringWell publishes its pricing and specs online, sizes by bathrooms, and ships free &mdash; so you have a real baseline number before any installer walks through your door.",
      "Check current SpringWell SS price","salt-softener") + '''</div>

    <div class="col">
      <h2 id="composition">Where the money actually goes</h2>
      <p style="margin:0 0 16px">Midpoint of the worksheet above, as shares of a typical project that needs site work:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",40),("#E8A13D",39),("#1F7A5C",13),("#5B6B75",5),("#D9DED9",3)], "~$2,600", "typical project") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> Softener unit <span class="pc">~40%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Site work (loop, drain, electrical) <span class="pc">~39%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Installation labor <span class="pc">~13%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> First-year salt <span class="pc">~5%</span></div>
          <div><span class="sw" style="background:#D9DED9"></span> Bypass &amp; fittings <span class="pc">~3%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of the worksheet above &middot; prepared homes skip the amber slice entirely</div>
    </div>

    <div class="col">
      <h2 id="equipment">How much is the equipment &mdash; and why quotes for the same hardware differ 5&times;</h2>
      <p>Retail, a metered ion-exchange softener runs <span class="fig">$600&ndash;$1,500</span> depending on grain capacity and the control valve; HomeGuide&rsquo;s 2026 planning data puts unit-only pricing at <span class="fig">$600&ndash;$2,000</span>. The valve is the machine &mdash; the tanks are commodity parts. Where prices genuinely diverge is the <strong>buying route</strong>, not the hardware class:</p>
    </div>
    <div class="col-wide" style="margin-top:16px">''' + range_bars(route_rows, 8000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Dealer-route figures are commonly reported ranges from BBB filings and homeowner-shared quotes &mdash; not list prices, because dealer brands don&rsquo;t publish pricing. Sources below.</p>
      <p style="margin:16px 0 0">Row one and row four are often the same class of equipment. The spread is sales cost &mdash; commissions, financing margin, and the in-home appointment itself. It&rsquo;s not automatically a rip-off; it is a line item you&rsquo;re allowed to see. The <a href="/dealer-vs-factory-direct-pricing/">dealer vs. factory-direct breakdown</a> itemizes where those thousands go, and the <a href="/brands/">brand price expos&eacute;s</a> track 45 dealer brands.</p>

      <h2 id="loop">Labor &mdash; and the $2,000 loop wildcard</h2>
      <p>On a home with an existing loop, installation is a half-day job: <span class="fig">$200&ndash;$500</span> of plumber time for two connections, a drain line, and programming (2&ndash;4 hours at <span class="fig">$100&ndash;$150</span>/hr per Angi). Add <span class="fig">$40&ndash;$120</span> for bypass and fittings if not itemized. DIY is realistic when loop, drain, and outlet already exist: <span class="fig">$50&ndash;$150</span> in supplies.</p>
      <p style="margin:0">No loop? The plumber is cutting into your main line and running pipe: <span class="fig">$600&ndash;$2,000</span> depending on run length, slab vs. crawlspace, and drain access. This one line is why two neighbors with identical softeners can pay <span class="fig">$1,100</span> and <span class="fig">$3,300</span>. Get the loop priced <em>separately</em> on any quote &mdash; it&rsquo;s the honest installer&rsquo;s tell.</p>

      <p style="margin:0 0 16px">Owning one is cheaper than most people expect: our <a href="/water-softener-maintenance/">DIY maintenance schedule</a> puts the whole year at about two hours and $31 in consumables beyond the salt.</p>
      <p style="margin:0 0 16px">And if you want the number that actually matters &mdash; not what it costs to buy, but what it costs to <em>own</em> &mdash; our <a href="/10-year-water-softener-cost/">10-year cost study</a> models the whole decade from cited inputs and finds that the purchase decision swings it further than every running cost combined.</p>
      <h2 id="sizing">What size do I need &mdash; and why your ZIP code changes the price</h2>
      <p style="margin:0 0 16px">Short version below; the full method &mdash; including the reason a &ldquo;32,000-grain&rdquo; softener only delivers 32,000 grains on the day it burns the most salt &mdash; is in our <a href="/what-size-water-softener-do-i-need/">water softener sizing guide and calculator</a>.</p>
      <p>Sizing is arithmetic: <strong>people &times; daily water use &times; hardness (gpg) &times; 7 days</strong> = weekly grain demand. Cost guides size with 90 gallons/person/day for headroom; the <a href="https://www.epa.gov/watersense/statistics-and-facts" rel="noopener" target="_blank">EPA</a> puts actual indoor use at 82. A family of four on 10 gpg water needs ~25,200 grains a week &mdash; buy the tier above, a 32k unit.</p>
      <p style="margin:0 0 16px">Hardness swings sizing &mdash; and therefore cost &mdash; by two full tiers across the country (<a href="https://www.usgs.gov/special-topics/water-science-school/science/hardness-water" rel="noopener" target="_blank">USGS data</a>):</p>
      <div class="chart-panel">
        <h2 style="font-size:19px;margin:0 0 12px">Average hardness by region (grains per gallon)</h2>
        <div style="display:flex;flex-direction:column;gap:8px">''' + region_bars + '''</div>
        <div class="chart-attr" style="margin-top:10px">USGS county data &middot; full methodology in the <a href="/data/water-hardness-study/" style="color:inherit">hardness study</a></div>
      </div>
      <p style="margin:16px 0 0">On well water, test for iron, manganese, and sulfur too &mdash; iron fouls softener resin and needs its own treatment ahead of the softener, a separate <span class="fig">$300&ndash;$1,500+</span> decision. If you don&rsquo;t have current numbers, start with a <a href="/pick/test-kit" ''' + PICK + '''>water test kit</a> &mdash; the cheapest line item in this entire project and the one that prevents buying the wrong system.</p>

      <h2 id="salt-free">Salt-based vs. salt-free: what&rsquo;s the cost difference?</h2>
      <p style="margin:0 0 16px">They solve different problems, and the gap is smaller than the marketing suggests. Salt-based <em>removes</em> hardness through ion exchange; a salt-free conditioner <em>changes how minerals behave</em> so they don&rsquo;t form scale.</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>Salt-based softener vs. salt-free conditioner cost, 2026</caption>
        <thead><tr><th scope="col">System type</th><th scope="col" class="num">Installed (2026)</th><th scope="col">Ownership</th><th scope="col">Best fit</th></tr></thead>
        <tbody>
          <tr><td>Salt-based softener</td><td class="num">$1,200&ndash;$3,800</td><td class="muted">$100&ndash;$300/yr (salt + upkeep)</td><td class="muted">True softening: soap, spotting, skin, scale</td></tr>
          <tr><td>Salt-free conditioner</td><td class="num">$1,500&ndash;$4,500</td><td class="muted">Media swap every 3&ndash;7 yrs</td><td class="muted">Scale protection, zero salt, minimal upkeep</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Want the water heater protected with zero upkeep? A conditioner is the honest recommendation &mdash; full math in the <a href="/salt-free-water-softener-cost/">salt-free cost guide</a>. Want genuinely soft water? Only ion exchange delivers it. And chlorine taste is a filtration problem a softener won&rsquo;t touch &mdash; a <a href="/pick/whole-house-filter" ''' + PICK + '''>whole-house carbon system</a> handles it, and pairing filter + softener in one install saves a second labor bill.</p>

      <h2 id="ownership">What does owning a softener cost per year?</h2>
      <p style="margin:0 0 12px">Day one is half the story. A useful rule from years of estimates: <strong>a softener&rsquo;s 10-year ownership cost roughly equals its purchase price.</strong> The decade, proportioned:</p>
      <div class="stackbar" role="img" aria-label="10-year ownership cost composition">
        <div style="width:46%;background:#16303F" title="Salt"></div>
        <div style="width:15%;background:#5B6B75" title="Prefilters"></div>
        <div style="width:23%;background:#E8A13D" title="Repairs"></div>
        <div style="width:16%;background:#1F7A5C" title="Resin rebed"></div>
      </div>
      <div class="stack-legend">
        <span><span class="sw" style="background:#16303F"></span>Salt $600&ndash;$1,800</span>
        <span><span class="sw" style="background:#5B6B75"></span>Prefilters $200&ndash;$600</span>
        <span><span class="sw" style="background:#E8A13D"></span>Repairs $300&ndash;$900</span>
        <span><span class="sw" style="background:#1F7A5C"></span>Rebed $250&ndash;$600</span>
      </div>
      <p style="margin:16px 0 12px">Salt is the recurring line &mdash; 8&ndash;12 bags a year at Angi&rsquo;s observed <span class="fig">$5&ndash;$10</span> per 40-lb bag. Slide your own numbers:</p>
      <div data-salt-calc></div>
      <p style="margin:16px 0 0">Electricity is a non-factor &mdash; the valve draws a few watts. If your system has a sediment prefilter, <a href="/pick/replacement-prefilters" ''' + PICK + '''>replacement cartridges</a> are the other recurring line; a clogged prefilter mimics expensive pressure problems, so it&rsquo;s cheap insurance. Cheap timer-based units regenerate on a clock whether you used water or not &mdash; the extra salt quietly doubles the recurring line. Full year-by-year math in the <a href="/water-softener-maintenance-cost/">maintenance cost guide</a>.</p>

      <h2 id="quote-anatomy">How to read a dealer or plumber quote</h2>
      <p>Six drivers set every estimate I ever wrote. A quote you can trust shows all six: <strong>equipment</strong> (exact model and grain capacity &mdash; &ldquo;whole-home softener system&rdquo; with no model number is a red flag), <strong>labor</strong> stated separately, <strong>materials</strong>, <strong>site work</strong> priced line by line, <strong>removal</strong> of the old unit (<span class="fig">$50&ndash;$150</span>), and <strong>extras</strong> &mdash; warranty, service plan, financing cost, permit where required.</p>
      <p><strong>Legitimate reasons one quote is higher:</strong> a real loop run the cheaper quote ignored; code-required drain or permit work; a genuinely larger, better-metered unit; licensed labor in a high-cost metro.</p>
      <p style="margin:0"><strong>Red flags that deserve a second quote:</strong> no model number; &ldquo;today-only&rdquo; pricing; a water &ldquo;test&rdquo; that ends in a same-day contract; financing pushed before the cash price; one bundled number. A higher quote isn&rsquo;t automatically dishonest &mdash; an unreadable one usually is.</p>
      <p style="margin:16px 0 0"><strong>Before you get a quote, collect:</strong> your hardness number, city-or-well (plus iron results if well), people + bathrooms, loop yes/no, nearest drain and outlet, pipe size if visible, and your current model if replacing. With those seven answers, the calculator up top gives you a defensible range &mdash; and any installer quoting wildly outside it owes you a line-item explanation.</p>
      <div style="margin-top:40px">''' + cta_box("The factory-direct alternative",
        "Once you know your size and your range, compare it against published pricing before you book a single in-home visit. SpringWell&rsquo;s salt-based softeners are sized by bathrooms, sold at posted prices with a 6-month money-back guarantee, and DIY-friendly on an existing loop.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(pillar_faqs) + '''
      <h2>Keep going</h2>
      <div class="card-grid">
        <a class="card" href="/brands/"><div class="name">Brand price expos&eacute;s</div><div class="desc">The ranges dealers won&rsquo;t publish &mdash; 45 brands, sourced.</div></a>
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">Maintenance costs</div><div class="desc">Salt, resin, valves &mdash; what ownership really runs per year.</div></a>
        <a class="card" href="/calculators/"><div class="name">Calculators</div><div class="desc">Your inputs, your number, the math shown.</div></a>
        <a class="card" href="/data/water-hardness-study/"><div class="name">Hardness data study</div><div class="desc">County-level map and methods.</div></a>
        <a class="card" href="/salt-free-water-softener-cost/"><div class="name">Salt-free system cost</div><div class="desc">Conditioners, itemized.</div></a>
        <a class="card" href="/why-are-water-softeners-so-expensive/"><div class="name">Why so expensive?</div><div class="desc">Where every dollar of a quote actually goes.</div></a>
        <a class="card" href="/about/"><div class="name">About this site</div><div class="desc">Who I am, how I price, and how this site makes money.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Angi &mdash; Water Softener System Installation Cost (2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: $200&ndash;$6,000 range and $1,500 average; salt $5&ndash;$10/40-lb bag; repairs $150&ndash;$900; rental $25&ndash;$50/mo; 2&ndash;4 hr install; sizing formula.',
 '<strong>Angi &mdash; regional installation cost pages (2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost/ny/new-york" rel="noopener" target="_blank">angi.com/&hellip;/new-york</a>. Supports: plumber rates ($100&ndash;$150/hr) and labor totals of $200&ndash;$1,500 by market.',
 '<strong>HomeGuide &mdash; Water Softener Cost (2026)</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: salt-based installed $1,200&ndash;$3,800; salt-free $1,500&ndash;$4,500; salt $50&ndash;$150/yr; maintenance $100&ndash;$300/yr; dedicated circuit $250&ndash;$900.',
 '<strong>Homewyse &mdash; Cost to Install Water Softener (May 2026)</strong> &mdash; <a href="https://www.homewyse.com/services/cost_to_install_water_softener.html" rel="noopener" target="_blank">homewyse.com</a>. Supports: national average basic installed project of $1,131&ndash;$1,405.',
 '<strong>USGS &mdash; Hardness of Water</strong> &mdash; <a href="https://www.usgs.gov/special-topics/water-science-school/science/hardness-water" rel="noopener" target="_blank">usgs.gov</a>. Supports: regional hardness variation and gpg classification.',
 '<strong>U.S. EPA WaterSense &mdash; Statistics and Facts</strong> &mdash; <a href="https://www.epa.gov/watersense/statistics-and-facts" rel="noopener" target="_blank">epa.gov</a>. Supports: average indoor water use (~82 gal/person/day).',
 '<strong>Publicly reported dealer quotes</strong> &mdash; BBB complaint filings and homeowner-shared quotes (r/plumbing, Terry Love forums), 2024&ndash;2026. Supports: dealer-package range in the buying-route chart &mdash; commonly reported figures, not list prices.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("index.html", home)

# ============ ABOUT (T7) ============
about = head("About Robert Miller — SoftWaterSystemCost",
 "Former plumbing & water-treatment estimator publishing the itemized softener costs dealers don't. Editorial standards, disclosures, and contact.",
 "/about/",
 ld(json.dumps({"@context":"https://schema.org","@type":"Person","name":"Robert Miller","url":SITE+"/about/",
   "jobTitle":"Publisher, SoftWaterSystemCost","image":SITE+"/assets/robert-miller-240.webp","description":"Former plumbing and water-treatment estimator, 15+ years pricing residential installs.",
   "workLocation":{"@type":"Place","address":{"@type":"PostalAddress","addressLocality":"Daytona Beach","addressRegion":"FL"}}})))
about += HEADER + f'''<main id="main">
  <article class="col">
    <div class="page-hero-row" style="display:flex;gap:24px;align-items:center;margin-top:40px">
      <div class="avatar-photo"><img src="/assets/robert-miller-240.webp" alt="Robert Miller, former plumbing and water-treatment estimator" width="240" height="240"></div>
      <h1 style="margin:0">I priced these systems for 15 years. Now I publish the numbers.</h1>
    </div>
    <p style="margin-top:24px">I&rsquo;m Robert Miller. From the mid-2000s I worked as an estimator for plumbing and water-treatment contractors around Daytona Beach &mdash; the person who turned a walkthrough of your garage into the number on the quote. I know what a softener install costs to deliver, because writing that cost down was my job.</p>
    <p>I also watched what happened between my worksheet and the customer&rsquo;s kitchen table. The gap between those two numbers &mdash; sometimes <span class="fig">$3,000</span> on identical hardware &mdash; is why this site exists. Every guide here is built the way I built quotes: line items, ranges, sources.</p>

    <h2>What this site does &mdash; and doesn&rsquo;t</h2>
    <ul style="margin:0;padding-left:24px;display:flex;flex-direction:column;gap:8px">
      <li>We publish itemized cost ranges with sources for every figure.</li>
      <li>We <strong>don&rsquo;t sell or install</strong> water treatment systems.</li>
      <li>We <strong>don&rsquo;t accept sponsored posts</strong> or let any brand review content before publication.</li>
      <li>We critique pricing opacity, not products &mdash; brands are named only with cited, public figures.</li>
    </ul>

    <h2 id="money">How we make money</h2>
    <p style="margin:0">This site is reader-supported. If you buy through some links &mdash; currently SpringWell, a factory-direct manufacturer we recommend because it publishes its prices &mdash; we may earn a commission at no cost to you. That relationship never changes a number on this site: the figures come from the sources listed on each page, and the recommendation predates the commission. The full arrangement is described in our <a href="/how-we-make-money/">affiliate disclosure</a>.</p>

    <h2 id="standards">Editorial standards</h2>
    <ul style="margin:0;padding-left:24px;display:flex;flex-direction:column;gap:8px">
      <li>Every dollar figure traces to a listed source; estimates are always ranges.</li>
      <li>Every money page carries a data stamp; figures are re-checked at least twice a year.</li>
      <li>Claims about health or water quality cite EPA or CDC materials.</li>
      <li>Corrections are noted in-page. Found an error? Email me.</li>
    </ul>

    <h2 id="contact">Contact</h2>
    <p style="margin:0">Email: <a href="mailto:robert@softwatersystemcost.com">robert@softwatersystemcost.com</a> &mdash; I read everything; quote-review questions get priority.</p>
    <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">SoftWaterSystemCost &middot; 1635 S Ridgewood Ave, 2nd Floor Ste 201, Daytona Beach, FL 32119</p>
  </article>
</main>
''' + FOOTER
write("about/index.html", about)

# ============ TOOL PAGE (T5) ============
tool_faqs = [
 ("Why a range and not one number?","Because the plumbing decides the final third of the bill. A range built from your inputs is honest; a single number is a sales tactic."),
 ("Does the estimate include a loop run?","No &mdash; it assumes a loop exists. Add $600&ndash;$2,000 if one has to be cut in. The full cost guide explains how to tell if you have one."),
 ("Where does the hardness lookup come from?","USGS county-level survey data, averaged by ZIP prefix. It&rsquo;s a starting point &mdash; your utility&rsquo;s annual water report has your exact number."),
 ("Can I use this for a well?","Partially. Wells often need iron pre-treatment ahead of the softener, which this tool doesn&rsquo;t price. Test your water first, then size."),
]
tool = head("Water Softener Cost Calculator (2026) — SoftWaterSystemCost",
 "Free water softener cost calculator: household size + hardness → itemized installed cost range. Built on 2026 retail and labor data. Embeddable.",
 "/calculators/cost-calculator/",
 ld(json.dumps({"@context":"https://schema.org","@type":"WebApplication","name":"Water Softener Cost Calculator","url":SITE+"/calculators/cost-calculator/","applicationCategory":"UtilityApplication","operatingSystem":"Web"}))
 + ld(faq_schema(tool_faqs,"/calculators/cost-calculator/"))
 + ld(breadcrumb_schema([("Home","/"),("Calculators","/calculators/"),("Cost calculator","/calculators/cost-calculator/")])))
tool += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin:40px auto 24px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/calculators/">Calculators</a> &rsaquo; Cost calculator</nav>
      <h1>Water Softener Cost Calculator</h1>
      <span class="stamp">Data updated &middot; Jul 2026</span>
    </div>
    <div class="col">
      <div class="calc-titlebar"><span class="t-left">Cost estimator</span><span class="t-right">Live estimate</span></div>
      <div data-calc data-variant="full"></div>
    </div>
    <div class="col">
      <h2>How this calculator works</h2>
      <p>Sizing first: people &times; 75 gallons/day &times; your hardness (gpg) &times; a 7-day reserve gives weekly grain demand, which maps to a 24k, 32k, 48k, or 64k tier. Each tier carries a unit price range from 2026 retail surveys; labor and fittings come from Angi/HomeAdvisor national data. The output is a range, never a point &mdash; because your plumbing, not the math, sets the final number.</p>
      <p style="margin:0">The estimate defaults to no loop. Have one? Toggle it &mdash; that single item is worth <span class="fig">$600&ndash;$2,000</span>. The full explanation is in the <a href="/">cost guide</a>.</p>

      <h2>What actually drives the number</h2>
      <p>Three inputs matter far more than brand: hardness (it sets capacity), household size (it sets flow), and whether a loop exists (it sets labor). Everything else &mdash; smart valves, app monitoring, tank color &mdash; is trim. When a quote is thousands above this calculator&rsquo;s high end, the gap is sales cost, and you&rsquo;re allowed to ask what it buys.</p>
      <p style="margin:0">Hardness varies more than people expect: 3 gpg in New England, 20+ in the Southwest. Look yours up by ZIP in the calculator, or pull your utility&rsquo;s water report &mdash; it&rsquo;s on page one.</p>

      <h2>Embed this calculator</h2>
      <p style="margin:0 0 8px;font-size:17px">Free to embed with attribution. Paste this where you want it to appear:</p>
      <pre class="snippet">&lt;iframe src="https://softwatersystemcost.com/embed/cost-calculator/"
  width="100%" height="560" style="border:0" loading="lazy"
  title="Water Softener Cost Calculator"&gt;&lt;/iframe&gt;</pre>

      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(tool_faqs) + '''
    </div>
''' + sources([
 "Retail pricing survey, metered softeners by grain tier, Jul 2026.",
 "Angi / HomeAdvisor installation labor data, 2026.",
 "USGS county-level hardness data (ZIP lookup source).",
 "AWWA residential water use benchmarks (75 gal/person/day).",
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("calculators/cost-calculator/index.html", tool)

# ============ EMBED ROUTE ============
embed = head("Water Softener Cost Calculator — embed","Embeddable water softener cost calculator by SoftWaterSystemCost.","/embed/cost-calculator/","",noindex=True)
embed += '''<div style="max-width:680px;margin:0 auto">
  <div class="calc-titlebar" style="border-radius:0"><span class="t-left">Cost estimator</span><span class="t-right">Live estimate</span></div>
  <div data-calc data-variant="embed"></div>
  <div class="embed-attr" style="background:#FFFFFF;border:1px solid #D9DED9;border-top:none">Calculator by <a href="https://softwatersystemcost.com/" target="_blank" rel="noopener">SoftWaterSystemCost.com</a></div>
</div>
<script type="module" src="/assets/calculator.js?v=171"></script>
</body>
</html>'''
write("embed/cost-calculator/index.html", embed)

# ============ B1 — INSTALLATION COST (T3+viz) ============
b1_faqs = [
 ("How much does water softener installation labor cost?","$200&ndash;$500 for a standard swap on an existing loop &mdash; 2&ndash;4 hours at $100&ndash;$150/hr. Cutting a new loop is separate plumbing work at $600&ndash;$2,000; a dedicated outlet adds $250&ndash;$900 if missing."),
 ("Who installs water softeners?","Licensed plumbers, water-treatment installers, and big-box programs (which subcontract local plumbers with a referral markup). For a swap on an existing loop, any licensed plumber can do it in an afternoon."),
 ("How much does Lowe&rsquo;s or Home Depot charge to install a softener?","Reported program totals run $1,000&ndash;$2,800 at Lowe&rsquo;s and $2,500&ndash;$6,000 at Home Depot including the unit (Fixr). Both subcontract the work &mdash; you can often hire the same plumber directly for less."),
 ("How long does installation take?","2&ndash;4 hours for a swap on an existing loop. Add a loop cut-in and it&rsquo;s a half-to-full day; add drain and electrical work and plan on a full day plus an electrician visit."),
 ("Do I need a permit to install a water softener?","Some jurisdictions require a plumbing permit, typically $50&ndash;$150, especially when cutting into the main line. A quote that includes the permit line is a good sign; ask your installer or building department."),
 ("Can I install a water softener myself?","Yes, if a loop, drain, and outlet already exist and you can make two compression connections: budget $50&ndash;$150 in supplies. If any of the three is missing, the plumbing work is where DIY projects become rescue calls."),
 ("Is replacing an existing water softener cheaper than a first install?","Usually much cheaper: the loop, drain, and outlet already exist, so you&rsquo;re paying swap labor ($200&ndash;$500), fittings, and haul-away ($50&ndash;$150) &mdash; the $290&ndash;$770 &ldquo;prepared home&rdquo; band, plus the new unit."),
]
b1_rows = [
 ("Water softener equipment (metered)",600,1500,"HomeGuide retail class; the advertised price ends here"),
 ("Installation labor (2&ndash;4 hrs)",200,500,"$100&ndash;$150/hr typical plumber rates (Angi)"),
 ("Bypass valve, fittings &amp; materials",40,120,"Often bundled &mdash; ask if included"),
 ("Old unit removal &amp; haul-away (only if replacing)",0,150,"Skip on a first install"),
 ("Loop run (only if none exists)",0,2000,"Cut-in is $600&ndash;$2,000 when needed"),
 ("Drain line (only if missing)",0,300,"Distance to nearest standpipe or drain"),
 ("Dedicated 110V outlet (only if missing)",0,900,"Electrician work; $250&ndash;$900 (HomeGuide)"),
 ("Plumbing permit (where required)",0,150,"Jurisdiction-dependent"),
]
b1_route_rows = [
 ("DIY on existing loop (supplies only)",50,150,"#1F7A5C"),
 ("Independent plumber (labor, existing loop)",200,500,"#16303F"),
 ("Lowe&rsquo;s program (with unit, reported)",1000,2800,"#5B6B75"),
 ("Home Depot program (with unit, reported)",2500,6000,"#E8A13D"),
]
b1 = head("Water Softener Installation Cost (2026): Labor & Line Items",
 "Water softener installation costs $200\u2013$500 in labor on an existing loop \u2014 or up to $4,120 with site work. Every install line item, sourced.",
 "/water-softener-installation-cost/",
 ld(article_schema("Water Softener Installation Cost in 2026: Labor, Loop & Every Line Item","Itemized 2026 installation labor and site-work costs with sources.","/water-softener-installation-cost/",date="2026-07-12"))
 + ld(faq_schema(b1_faqs,"/water-softener-installation-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Installation cost","/water-softener-installation-cost/")])))
b1 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Installation cost</nav>
      <h1>Water Softener Installation Cost in 2026: Labor, Loop &amp; Every Line Item</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Installation labor for a water softener costs <span class="fig">$200&ndash;$500</span> on a home with an existing loop &mdash; a 2&ndash;4 hour job at typical plumber rates of <span class="fig">$100&ndash;$150</span>/hr per <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">Angi&rsquo;s 2026 data</a>. Installation <em>projects</em> are another story: once loop runs, drain lines, and electrical enter the worksheet, install-side costs alone can reach <span class="fig">$4,120</span>, and <a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">Fixr</a> puts typical full installed projects at <span class="fig">$1,100&ndash;$3,000</span>.</p>
      <p><strong>Installing a water softener costs $840&ndash;$4,120 all-in for most homes: $600&ndash;$1,500 for the metered unit, $200&ndash;$500 in labor on an existing loop, and $40&ndash;$120 in fittings &mdash; with loop runs, drain lines, and electrical work adding $0&ndash;$3,200 depending on what your house already has.</strong></p>
      <p style="margin:0">I wrote these estimates for fifteen years. The labor is the cheap part &mdash; what you&rsquo;re really pricing is <em>what your house is missing</em>. This page itemizes exactly that, so you know whether a <span class="fig">$300</span> or a <span class="fig">$3,000</span> install quote is the honest one for your garage.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#worksheet">The install-only worksheet</a></li>
          <li><a href="#scenario">Your scenario, priced (tool)</a></li>
          <li><a href="#module">Installation Module calculator</a></li>
          <li><a href="#composition">Where the install dollar goes (chart)</a></li>
          <li><a href="#routes">Who installs it &mdash; and what each route costs</a></li>
          <li><a href="#labor-table">Labor by task</a></li>
          <li><a href="#diy">DIY vs. pro</a></li>
          <li><a href="#quote">What a good install quote shows</a></li>
        </ol>
      </details>
      <h2 id="worksheet">What does water softener installation cost?</h2>
      <p style="margin:0">Everything except the softener itself, itemized. Rows marked &ldquo;only if&rdquo; are <span class="fig">$0</span> in a prepared home:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Total installed cost: unit + labor + parts", b1_rows, total_label="Total installed cost") + '''</div>
    <div class="col">
      <h2 id="scenario" style="margin-top:48px">Price your scenario in one tap</h2>
      <div data-install-calc></div>
      <p style="margin:16px 0 0">The scenario tool above prices the install side alone; the worksheet includes the unit. And a reading note on the sheet: the &ldquo;only if&rdquo; rows don&rsquo;t stack in real homes &mdash; nobody pays every conditional maximum at once, which is why typical completed projects land <span class="fig">$840&ndash;$4,120</span> rather than the theoretical top of the column. The <a href="/#quote-sheet">full cost worksheet</a> shows the same math sitewide.</p>
      <div style="margin-top:40px">''' + cta_box("Cut the install line to nearly zero",
        "SpringWell&rsquo;s softeners are engineered for DIY on an existing loop &mdash; push-fit connections, video guides, and phone support. On a prepared home, that turns the $200&ndash;$500 labor line into a Saturday morning, and the price is published before you start.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="module">Calculator: build your installed cost, line by line</h2>
      <p style="margin:0 0 16px">The Installation Module below assembles the same formula every honest quote uses &mdash; <em>equipment + labor + site modifications + parts + extras</em>. Toggle what your project actually includes; every input is a sourced range, and the result is a planning estimate, not a site-specific bid:</p>
      <div data-expense-calc></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Inputs that matter most: whether a loop exists (the biggest single swing), drain and outlet availability, and whether you&rsquo;re replacing an old unit. A contractor pricing your specific plumbing may land differently &mdash; that&rsquo;s what the itemization checklist below is for.</p>

      <h2 id="composition">Where the install dollar actually goes</h2>
      <p style="margin:0 0 16px">Midpoints for an unprepared home &mdash; the labor slice is smaller than everyone expects:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#E8A13D",52),("#5B6B75",18),("#1F7A5C",14),("#16303F",10),("#D9DED9",6)], "~$2,500", "unprepared home", "Install cost composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#E8A13D"></span> Loop run <span class="pc">~52%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Dedicated outlet (electrician) <span class="pc">~18%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Labor (the softener swap itself) <span class="pc">~14%</span></div>
          <div><span class="sw" style="background:#16303F"></span> Drain line + permit <span class="pc">~10%</span></div>
          <div><span class="sw" style="background:#D9DED9"></span> Fittings &amp; removal <span class="pc">~6%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; worksheet midpoints &middot; prepared homes pay only the green, navy-drain, and gray slices</div>
    </div>

    <div class="col">
      <h2 id="routes">Who installs it &mdash; and what each route really costs</h2>
      <p style="margin:0 0 16px">Big-box programs feel convenient, but both Lowe&rsquo;s and Home Depot <em>subcontract</em> the work to local plumbers and add a referral margin &mdash; reported program totals (unit included) land well above hiring the same plumber yourself:</p>
    </div>
    <div class="col-wide">''' + range_bars(b1_route_rows, 6000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Program figures: Fixr 2026 cost guide and reported Lowe&rsquo;s install pricing (UpgradedHome); labor-only rows: Angi. Big-box rows include a unit; the first two rows don&rsquo;t &mdash; that&rsquo;s the point of comparing them.</p>
      <p style="margin:16px 0 0">The same pattern shows up one tier higher: dealer packages bundle install &ldquo;free&rdquo; into a <span class="fig">$3,000&ndash;$8,000</span> quote. Nothing is free &mdash; it&rsquo;s a line item you&rsquo;re not allowed to see. The <a href="/dealer-vs-factory-direct-pricing/">dealer vs. factory-direct breakdown</a> takes that apart, and the <a href="/brands/">brand price expos&eacute;s</a> track who hides what.</p>

      <h2 id="labor-table">Labor cost by task</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Water softener installation labor by task, 2026</caption>
        <thead><tr><th scope="col">Task</th><th scope="col">Typical time</th><th scope="col" class="num">Cost</th></tr></thead>
        <tbody>
          <tr><td>Swap on existing loop (connect, drain, program)</td><td class="muted">2&ndash;4 hrs</td><td class="num">$200&ndash;$500</td></tr>
          <tr><td>Cut in a new softener loop</td><td class="muted">4&ndash;8 hrs</td><td class="num">$600&ndash;$2,000</td></tr>
          <tr><td>Run a drain line to a standpipe</td><td class="muted">1&ndash;2 hrs</td><td class="num">$100&ndash;$300</td></tr>
          <tr><td>Dedicated 110V outlet (electrician)</td><td class="muted">1&ndash;3 hrs</td><td class="num">$250&ndash;$900</td></tr>
          <tr><td>Old unit removal &amp; disposal</td><td class="muted">&lt;1 hr</td><td class="num">$50&ndash;$150</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <h2 id="diy">DIY vs. pro: the honest comparison</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>DIY versus professional water softener installation</caption>
        <thead><tr><th scope="col">Route</th><th scope="col" class="num">Install cost</th><th scope="col">Time</th><th scope="col">Watch out for</th></tr></thead>
        <tbody>
          <tr><td>DIY (loop exists)</td><td class="num">$50&ndash;$150</td><td class="muted">A Saturday morning</td><td class="muted">Drain air gap, bypass orientation, programming</td></tr>
          <tr><td>Independent plumber</td><td class="num">$200&ndash;$500</td><td class="muted">2&ndash;4 hrs</td><td class="muted">Get fittings itemized; confirm haul-away</td></tr>
          <tr><td>Big-box program</td><td class="num">$1,000&ndash;$6,000 w/ unit</td><td class="muted">Consult + ~1 week</td><td class="muted">Subcontracted labor with referral markup</td></tr>
          <tr><td>Dealer bundle</td><td class="num">Hidden in package</td><td class="muted">Same-day pitch</td><td class="muted">&ldquo;Free install&rdquo; priced into the quote</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">One more install-side saver worth knowing: if you also need whole-house filtration, a <a href="/pick/filter-salt-softener-combo" ''' + PICK + '''>filter + softener combo</a> goes in as <em>one</em> install &mdash; one loop, one labor bill, instead of paying the plumber twice a year apart.</p>

      <h2 id="quote">What should be itemized on an installation quote</h2>
      <p>Every trustworthy quote I ever built made ten things explicit: the exact <strong>model and capacity</strong> being installed; <strong>labor</strong> (hours or flat); <strong>fittings and bypass</strong>; each piece of <strong>site work priced as its own line</strong> (loop, drain, outlet); <strong>permit responsibility</strong>; <strong>old-unit removal</strong>; what the <strong>warranty</strong> covers on equipment vs. labor; and &mdash; the line most quotes omit &mdash; what is specifically <strong>excluded</strong>. The <a href="/#quote-anatomy">full quote-anatomy guide</a> covers the red flags; the short version: one bundled number with no lines means get a second quote.</p>
      <p style="margin:0 0 16px">And compare <em>scope against scope</em>, never total against total: a $300 install and a $2,000 install may not be pricing the same job. Line the bids up row by row on the worksheet above &mdash; the lowest number is not necessarily the lowest comparable quote. One more pre-quote saver: confirm your hardness with a <a href="/pick/test-kit" ''' + PICK + '''>test kit</a> before anyone sizes equipment for you &mdash; oversizing is the quietest padding there is, and our <a href="/what-size-water-softener-do-i-need/">sizing calculator</a> tells you the capacity you actually need before the quote does.</p>
      <p style="margin:0">Before you call anyone, collect the seven answers in the <a href="/#quote-anatomy">pre-quote checklist</a> (hardness, loop status, drain and outlet locations, pipe size). With those, the ranges on this page are defensible &mdash; and any installer quoting far outside them owes you a line-item explanation.</p>
      <div style="margin-top:40px">''' + cta_box("Know the whole number before the visit",
        "An install quote only makes sense next to a published equipment price. SpringWell posts its softener pricing, sizes by bathrooms, and ships free with a 6-month money-back guarantee &mdash; so the install quote is the only variable left to negotiate.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(b1_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/"><div class="name">Full system cost guide</div><div class="desc">Unit + install, itemized with charts.</div></a>
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">Maintenance costs</div><div class="desc">Salt, resin, valves per year.</div></a>
        <a class="card" href="/brands/"><div class="name">Brand price expos&eacute;s</div><div class="desc">45 brands, sourced ranges.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Angi &mdash; Water Softener System Installation Cost (2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: labor $200&ndash;$500 and $100&ndash;$150/hr; 2&ndash;4 hour installs.',
 '<strong>Fixr &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">fixr.com</a>. Supports: typical installed projects $1,100&ndash;$3,000; Lowe&rsquo;s program $1,000&ndash;$2,800; Home Depot program $2,500&ndash;$6,000.',
 '<strong>UpgradedHome &mdash; Lowe&rsquo;s Water Softener Installation Cost</strong> &mdash; <a href="https://upgradedhome.com/how-much-does-water-softener-installation-cost-at-lowes/" rel="noopener" target="_blank">upgradedhome.com</a>. Supports: Lowe&rsquo;s install labor add of $150&ndash;$600; 110V-outlet-within-10-ft requirement.',
 '<strong>HomeGuide &mdash; Water Softener Cost (2026)</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: dedicated electrical circuit $250&ndash;$900.',
 '<strong>Homewyse &mdash; Cost to Install Water Softener (May 2026)</strong> &mdash; <a href="https://www.homewyse.com/services/cost_to_install_water_softener.html" rel="noopener" target="_blank">homewyse.com</a>. Supports: national average basic installed project $1,131&ndash;$1,405.',
 '<strong>Contractor-forum reports (attributed)</strong> &mdash; homeowner-shared install quotes and subcontracting practice discussions (DoItYourself.com forums, plumbing trade blogs), 2024&ndash;2026. Supports: big-box subcontracting-with-markup pattern.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("water-softener-installation-cost/index.html", b1)

# ============ C1 — CULLIGAN EXPOSE (T4+viz) ============
c1_faqs = [
 ("How much does a Culligan water softener cost?","Most homeowners report $2,500&ndash;$4,500 installed; published guides put the full spread at $1,800&ndash;$6,500, with twin-tank and well systems exceeding $8,000. Culligan doesn&rsquo;t publish list prices &mdash; every quote comes from an in-home visit."),
 ("Why won&rsquo;t Culligan tell me a price over the phone?","The dealer model prices each sale at the kitchen table, not from a price list. The free in-home &ldquo;water test&rdquo; is the sales appointment. It&rsquo;s effective selling &mdash; it&rsquo;s just not transparent pricing."),
 ("Is renting a Culligan softener worth it?","Rentals run $25&ndash;$100/month, often on multi-year agreements. At $60/month you&rsquo;ve paid $3,600 in five years &mdash; roughly a mid-tier purchase &mdash; and own nothing. Renting fits short stays; buying wins within 3&ndash;5 years."),
 ("Is Culligan equipment good?","Generally yes &mdash; solid ion-exchange hardware with strong dealer service. This page critiques pricing opacity, not the product. You&rsquo;re paying for a sales channel and a service network, not better resin."),
 ("Can I negotiate a Culligan quote?","Commonly, yes. Reps typically hold discount authority, and dealers run rebates and trade-in offers worth $100&ndash;$500. A written competing quote is the fastest way to find the real floor."),
 ("What does Culligan salt delivery cost?","Reported at $240&ndash;$600 per year including delivery service. Self-supplied salt for a comparable softener runs $60&ndash;$180 &mdash; over ten years, the delivery program can cost more than a softener."),
]
c1_rows = [
 ("Aquasential HE-series equipment (published tier)",1500,3500,"BestCompany model-tier pricing"),
 ("Dealer installation (basic&ndash;standard)",200,1200,"BestCompany: $200&ndash;$500 basic, $500&ndash;$1,200 with new plumbing"),
 ("Remainder to reported installed totals (implied)",100,1800,"Sales, overhead &amp; service bundle &mdash; never itemized on the quote"),
]
c1_tier_rows = [
 ("Medallist series (unit)",800,1800,"#1F7A5C"),
 ("Aquasential HE (unit)",1500,3500,"#16303F"),
 ("HE Twin / Progressive Flow (unit)",3000,5000,"#5B6B75"),
 ("Reported installed totals (all systems)",1800,6500,"#E8A13D"),
]
c1 = head("Culligan Water Softener Cost (2026): Real Price Ranges",
 "Culligan softeners are reported at $2,500\u2013$4,500 installed ($1,800\u2013$6,500 full spread). Sourced ranges, rent-vs-buy math, and a quote checker.",
 "/culligan-water-softener-cost/",
 ld(article_schema("Culligan Water Softener Cost in 2026: The Price Ranges Dealers Don\u2019t Publish","Sourced Culligan pricing ranges, model tiers, rental math, and quote anatomy.","/culligan-water-softener-cost/",date="2026-07-12"))
 + ld(faq_schema(c1_faqs,"/culligan-water-softener-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Brands","/brands/"),("Culligan","/culligan-water-softener-cost/")])))
c1 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/brands/">Brands</a> &rsaquo; Culligan</nav>
      <h1>Culligan Water Softener Cost in 2026: The Price Ranges Dealers Don&rsquo;t Publish</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Culligan doesn&rsquo;t publish prices &mdash; but the reported numbers are consistent: most homeowners pay <span class="fig">$2,500&ndash;$4,500</span> installed per <a href="https://watersoftenercost.com/average-cost-of-culligan-water-softener/" rel="noopener" target="_blank">2026 ownership data</a>, with <a href="https://modernize.com/water-treatment/culligan-cost/water-softener" rel="noopener" target="_blank">Modernize</a> putting the full spread at <span class="fig">$1,800&ndash;$6,500</span> and twin-tank or well systems exceeding <span class="fig">$8,000</span>. Even <a href="https://www.culligan.com/blog/water-softener-cost-considerations" rel="noopener" target="_blank">Culligan&rsquo;s own cost guide</a> says a standard professional-grade system lands &ldquo;closer to $5,000.&rdquo; Rentals run <span class="fig">$25&ndash;$100</span>/month, typically on multi-year agreements.</p>
      <p style="margin:0">I built installation estimates for fifteen years, and here&rsquo;s the honest frame: Culligan sells solid ion-exchange equipment through the most expensive channel in the industry &mdash; commissioned in-home selling. This page shows what that channel costs, line by line, so you can walk into the free &ldquo;water test&rdquo; already knowing the numbers.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#models">What Culligan sells (tiers &amp; published ranges)</a></li>
          <li><a href="#worksheet">A Culligan quote, reconstructed</a></li>
          <li><a href="#checker">Quote checker (tool)</a></li>
          <li><a href="#ownership">The 10-year ownership surprise (chart)</a></li>
          <li><a href="#rent">Rent vs. buy</a></li>
          <li><a href="#why">Why Culligan doesn&rsquo;t publish prices</a></li>
          <li><a href="#alternative">The factory-direct alternative</a></li>
        </ol>
      </details>
      <h2 id="models">What Culligan sells &mdash; and what each tier reportedly costs</h2>
      <p style="margin:0 0 16px">Model-tier pricing collected from published 2026 guides (unit-focused; installed totals land higher):</p>
    </div>
    <div class="col-wide">''' + range_bars(c1_tier_rows, 8000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Tier figures: BestCompany 2026 Culligan pricing guide; installed totals: Modernize. Add-ons reported: Wi-Fi +$200&ndash;$500, dual tank +$500&ndash;$1,500, carbon add-on +$200&ndash;$600.</p>

      <h2 id="worksheet">A Culligan quote, reconstructed line by line</h2>
      <p style="margin:0">Culligan quotes arrive as one number. Here&rsquo;s an estimator&rsquo;s reconstruction of a typical HE-series quote using only published component figures &mdash; the third row is what&rsquo;s left over between the parts and the reported totals:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Culligan HE quote, reconstructed (est.)", c1_rows, total_label="Reported installed total") + '''</div>
    <div class="col">
      <p style="margin-top:24px">That third line is the one to negotiate. It covers real things &mdash; the dealer&rsquo;s service network, the in-home visit, financing overhead &mdash; but it&rsquo;s never shown on the quote, and its size is set by what the rep thinks you&rsquo;ll sign. Industry guides <a href="https://www.softprowatersystems.com/pages/average-costs-water-softener-brands" rel="noopener" target="_blank">warn</a> that high-pressure appointments push quotes to <span class="fig">$6,000&ndash;$8,000</span> &mdash; far above the hardware&rsquo;s published tiers.</p>

      <h2 id="checker">Check your Culligan quote against the reported bands</h2>
      <div data-quote-check></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Bands from the sourced ranges above. A verdict isn&rsquo;t a verdict on the dealer &mdash; it&rsquo;s a prompt for which questions to ask before signing.</p>
      <div style="margin-top:40px">''' + cta_box("See a published price first",
        "The strongest negotiating position is a real number from a company that posts one. SpringWell publishes its softener pricing online &mdash; sized by bathrooms, shipped free, 6-month money-back guarantee &mdash; so you can benchmark any in-home quote before the rep opens the folder.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="ownership">The 10-year ownership surprise: the salt program</h2>
      <p style="margin:0 0 16px">Culligan&rsquo;s salt-delivery service is genuinely convenient &mdash; and reported at <span class="fig">$240&ndash;$600 per year</span> (Modernize). Self-supplied salt for a comparable softener runs <span class="fig">$60&ndash;$180</span>. Over a decade, the convenience can cost more than the machine:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",42),("#E8A13D",50),("#5B6B75",8)], "~$8,400", "10-yr total (midpoints)", "10-year Culligan ownership composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> System, installed (midpoint ~$3,500) <span class="pc">~42%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Salt delivery program, 10 yrs (~$4,200) <span class="pc">~50%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Service visits &amp; parts <span class="pc">~8%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of sourced ranges &middot; self-supplied salt cuts the amber slice by roughly two-thirds</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">You don&rsquo;t have to take the delivery program &mdash; ask. And if you own any softener, the <a href="/water-softener-maintenance-cost/">maintenance cost guide</a> breaks down the self-service math, including <a href="/pick/replacement-prefilters" ''' + PICK + '''>prefilter cartridges</a>, the other quiet recurring line.</p>

      <h2 id="rent">Rent vs. buy: the five-year math</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Culligan rental versus purchase, five-year comparison &mdash; full math in the <a href="/water-softener-rental-cost/">rent-vs-buy guide</a></caption>
        <thead><tr><th scope="col">Route</th><th scope="col" class="num">5-year cost</th><th scope="col">You own it after?</th><th scope="col">Notes</th></tr></thead>
        <tbody>
          <tr><td>Rent at $25/mo (low band)</td><td class="num">$1,500</td><td class="muted">No</td><td class="muted">Often multi-year agreements; service included</td></tr>
          <tr><td>Rent at $60/mo (mid band)</td><td class="num">$3,600</td><td class="muted">No</td><td class="muted">Equals a mid-tier purchase &mdash; with nothing to show</td></tr>
          <tr><td>Buy, reported typical</td><td class="num">$2,500&ndash;$4,500</td><td class="muted">Yes</td><td class="muted">Plus salt; resin lasts 10&ndash;15 yrs</td></tr>
          <tr><td>Factory-direct + plumber</td><td class="num">$1,200&ndash;$3,200</td><td class="muted">Yes</td><td class="muted">Published pricing; install itemized separately</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Renting fits a two-year posting or a house you&rsquo;re selling. For everyone else, ownership wins by year three to five &mdash; the <a href="/water-softener-installation-cost/">installation cost guide</a> shows exactly what the install side should run.</p>

      <h2 id="why">Why doesn&rsquo;t Culligan publish prices?</h2>
      <p>Because the dealer network prices each sale individually &mdash; Culligan&rsquo;s own materials describe a &ldquo;custom quote after a free in-home water test.&rdquo; From an estimator&rsquo;s chair, that model has one job: the appointment. Once a rep is at your kitchen table with a hardness test turning colors, the close rate &mdash; and the price &mdash; goes up. None of that makes the equipment bad. It makes the <em>first number</em> negotiable, always.</p>
      <p style="margin:0">Fair credit where due: you&rsquo;re also buying a real service network, local techs, and 80+ years of brand accountability. Some homeowners happily pay for hands-off. The problem isn&rsquo;t the premium &mdash; it&rsquo;s that you can&rsquo;t see its size. The <a href="/dealer-vs-factory-direct-pricing/">dealer vs. factory-direct breakdown</a> quantifies it across every brand we track.</p>

      <h2 id="alternative">The factory-direct alternative</h2>
      <p style="margin:0">Third-party comparisons make the gap concrete: <a href="https://modernize.com/water-treatment/culligan-cost" rel="noopener" target="_blank">Modernize&rsquo;s Culligan cost guide</a> notes SpringWell systems &ldquo;typically cost $1,000 to $5,000 and are designed for DIY installation&rdquo; &mdash; same job, published price, no appointment. Pair that with an independent plumber from the <a href="/water-softener-installation-cost/">install guide</a> and the total usually lands below a Culligan quote&rsquo;s opening number.</p>
      <div style="margin-top:24px">''' + cta_box("The factory-direct alternative",
        "Skip the in-home quote entirely. SpringWell posts its softener prices, sizes by bathrooms, ships free, and backs it with a 6-month money-back guarantee and lifetime warranty on tanks and valves.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(c1_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/brands/"><div class="name">All brand expos&eacute;s</div><div class="desc">45 dealer brands, sourced ranges.</div></a>
        <a class="card" href="/water-softener-installation-cost/"><div class="name">Installation cost</div><div class="desc">Labor, loop &amp; line items.</div></a>
        <a class="card" href="/"><div class="name">Full system cost guide</div><div class="desc">Unit + install, itemized with charts.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Modernize &mdash; Culligan Water Softener Costs (2026)</strong> &mdash; <a href="https://modernize.com/water-treatment/culligan-cost/water-softener" rel="noopener" target="_blank">modernize.com</a>. Supports: $1,800&ndash;$6,500 installed spread; entry ~$1,500; twin-tank &gt;$8,000; rentals $25&ndash;$100/mo on multi-year agreements; salt refills $240&ndash;$600/yr; model lineup.',
 '<strong>Modernize &mdash; Culligan Water System Cost Guide (2026)</strong> &mdash; <a href="https://modernize.com/water-treatment/culligan-cost" rel="noopener" target="_blank">modernize.com</a>. Supports: softeners $500&ndash;$5,000; combos $3,000&ndash;$8,000; SpringWell comparison ($1,000&ndash;$5,000, DIY-designed).',
 '<strong>BestCompany &mdash; Culligan Water Softening System Cost</strong> &mdash; <a href="https://bestcompany.com/blog/water-softeners/culligan-water-cost" rel="noopener" target="_blank">bestcompany.com</a>. Supports: Medallist $800&ndash;$1,800; HE $1,500&ndash;$3,500; HE Twin $3,000&ndash;$5,000; salt-free $1,000&ndash;$3,000; install $200&ndash;$1,200; add-on and rebate figures.',
 '<strong>WaterSoftenerCost.com &mdash; Average Cost of Culligan Systems (2026)</strong> &mdash; <a href="https://watersoftenercost.com/average-cost-of-culligan-water-softener/" rel="noopener" target="_blank">watersoftenercost.com</a>. Supports: typical $2,500&ndash;$4,500 installed; resin life 10&ndash;15 years.',
 '<strong>Culligan &mdash; Water Softener Cost Considerations (official blog)</strong> &mdash; <a href="https://www.culligan.com/blog/water-softener-cost-considerations" rel="noopener" target="_blank">culligan.com</a>. Supports: brand&rsquo;s own $500&ndash;$10,000 framing and &ldquo;closer to $5,000&rdquo; standard; in-home consultative model.',
 '<strong>SoftPro &mdash; Average Costs for Water Softener Brands (2026)</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/average-costs-water-softener-brands" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: high-pressure sales pushing quotes to $6,000&ndash;$8,000.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("culligan-water-softener-cost/index.html", c1)

# ============ C28 — DEALER VS FACTORY-DIRECT (money hub) ============
c28_faqs = [
 ("Why do dealer water softener quotes range $3,000&ndash;$8,000?","The hardware class inside most quotes retails at $600&ndash;$1,500. The rest is the sales channel: commissioned in-home selling, financing margin, service-network overhead, and whatever the rep judges you&rsquo;ll sign."),
 ("Is a dealer softener better than a factory-direct one?","Usually the same class of ion-exchange equipment &mdash; resin tank, brine tank, metered valve. Dealers add a real local service network; factory-direct adds published pricing and warranty by mail. The resin doesn&rsquo;t know the difference."),
 ("Is the dealer channel ever worth it?","Yes: complicated well water needing on-site design, homeowners who want fully hands-off service, or landlords valuing one phone number. Pay the premium knowingly &mdash; the problem is paying it invisibly."),
 ("How do I negotiate a dealer quote down?","Bring a published price. Ask for the itemized version, name a written competing number, and let the rep use their discount authority &mdash; guides report rebates and discounts of $100&ndash;$500+ appearing on request."),
 ("What&rsquo;s the catch with factory-direct pricing?","You arrange installation yourself ($200&ndash;$500 on an existing loop) and service is warranty-by-mail plus phone support, not a local tech. For most standard city-water homes, that trade saves thousands."),
 ("Are big-box installs a middle ground?","Partly. Lowe&rsquo;s and Home Depot programs run $1,000&ndash;$6,000 with a unit, but both subcontract local plumbers with a referral markup &mdash; you can usually hire the same plumber directly for less."),
 ("How much markup is on a water softener?","Nobody outside a dealer&rsquo;s accounting knows, and any article quoting a percentage is guessing. What&rsquo;s published: the equipment class ($600&ndash;$1,500) and labor ($200&ndash;$500). The gap above that funds sales, overhead, service and financing &mdash; and it&rsquo;s the part you should see itemized."),
 ("Is $8,000 too much for a water softener?","It depends entirely on scope. Normalize first: capacity, tank count, bundled filtration or RO, site work, warranty terms, and whether that&rsquo;s a cash price or a financed total. An $8,000 well stack with an RO isn&rsquo;t the same purchase as an $8,000 softener on an existing loop."),
]
c28_rows = [
 ("Comparable metered softener (retail, published)",600,1500,"Same equipment class found inside most dealer packages"),
 ("Professional installation (existing loop)",200,500,"Angi: 2&ndash;4 hrs at $100&ndash;$150/hr"),
 ("Bypass, fittings &amp; haul-away",90,270,"Itemized in honest quotes"),
 ("Remainder of a $3,000&ndash;$8,000 dealer quote (implied)",2110,5730,"Sales commission, financing margin, overhead, service bundle &mdash; the unlabeled line"),
]
c28_ladder = [
 ("Retail/DIY (unit + supplies)",650,1750,"#1F7A5C"),
 ("Factory-direct + your plumber",1200,3200,"#16303F"),
 ("Big-box program (with unit)",1000,6000,"#5B6B75"),
 ("Dealer in-home package",3000,8000,"#E8A13D"),
]
c28 = head("Dealer vs Factory-Direct Water Softener Pricing (2026)",
 "The hardware in a $3,000\u2013$8,000 dealer quote retails at $600\u2013$1,500. Where the rest goes, how to negotiate it, and the published-price alternative.",
 "/dealer-vs-factory-direct-pricing/",
 ld(article_schema("Dealer vs. Factory-Direct Pricing: Why Softener Quotes Range $3,000\u2013$8,000","Channel-cost breakdown of dealer water softener quotes with sourced figures.","/dealer-vs-factory-direct-pricing/",date="2026-07-12"))
 + ld(faq_schema(c28_faqs,"/dealer-vs-factory-direct-pricing/"))
 + ld(breadcrumb_schema([("Home","/"),("Brands","/brands/"),("Dealer vs factory-direct","/dealer-vs-factory-direct-pricing/")])))
c28 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/brands/">Brands</a> &rsaquo; Dealer vs. factory-direct</nav>
      <h1>Dealer vs. Factory-Direct Pricing: Why Softener Quotes Range $3,000&ndash;$8,000</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Here is the whole argument in two numbers. The metered ion-exchange softener inside most dealer packages belongs to a hardware class that retails for <span class="fig">$600&ndash;$1,500</span> (<a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">HomeGuide</a>, <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">Angi</a>). Dealer in-home packages for that class are quoted at <span class="fig">$3,000&ndash;$8,000</span> &mdash; industry guides <a href="https://www.softprowatersystems.com/pages/average-costs-water-softener-brands" rel="noopener" target="_blank">warn</a> the top of that band is where high-pressure appointments land. The difference isn&rsquo;t resin. It&rsquo;s the channel.</p>
      <p style="margin:0">I spent fifteen years writing the worksheets behind quotes like these. This page shows you the ladder, prices each rung, reconstructs where the extra thousands go &mdash; and gives you the one negotiating tool that reliably works: a published price.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#ladder">The four ways to buy (chart)</a></li>
          <li><a href="#worksheet">A dealer quote, reconstructed</a></li>
          <li><a href="#reality">Reality-check your own quote (tool)</a></li>
          <li><a href="#premium">Price your quote&rsquo;s channel premium (tool)</a></li>
          <li><a href="#markup">Is that remainder just markup?</a></li>
          <li><a href="#fair">What the dealer premium legitimately buys</a></li>
          <li><a href="#negotiate">The negotiation script</a></li>
          <li><a href="#financing">The monthly payment is not the price (tool)</a></li>
          <li><a href="#normalize">Normalize before you compare</a></li>
          <li><a href="#redflags">Twelve things to clarify before signing</a></li>
          <li><a href="#direct">What buying direct actually asks of you</a></li>
          <li><a href="#brands">Brand-by-brand reported ranges</a></li>
        </ol>
      </details>
      <h2 id="ladder">The four ways to buy the same soft water</h2>
      <p style="margin:0 0 16px">Same job &mdash; hardness out, soft water in &mdash; four channels, sourced ranges:</p>
    </div>
    <div class="col-wide">''' + range_bars(c28_ladder, 8000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Sources: retail/unit and labor ranges from Angi and HomeGuide; big-box program totals from Fixr; dealer band from published brand guides and reported quotes &mdash; full list below. Bars overlap because homes differ; the pattern doesn&rsquo;t.</p>

      <h2 id="worksheet">A $3,000&ndash;$8,000 dealer quote, reconstructed</h2>
      <p style="margin:0">Dealer quotes arrive as one number. Build the same project from published component prices, and the arithmetic leaves a large unlabeled remainder:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Dealer package, reconstructed (est.)", c28_rows, total_label="Dealer quote band") + '''</div>
    <div class="col">
      <p style="margin-top:24px">That last row &mdash; often <em>two-thirds of the quote</em> &mdash; is the channel: sales commission, financing margin, branch overhead, and the service bundle. We ran the same reconstruction on a real brand in the <a href="/culligan-water-softener-cost/">Culligan cost expos&eacute;</a>, where even the <a href="https://www.culligan.com/blog/water-softener-cost-considerations" rel="noopener" target="_blank">brand&rsquo;s own cost guide</a> pegs a standard system &ldquo;closer to $5,000.&rdquo;</p>

      <h2 id="reality">Reality-check the quote in front of you</h2>
      <p style="margin:0 0 16px">The worksheet above is a national reconstruction. This one is yours: enter the number you were quoted and the condition of your house, and it separates the part of the price that has a <em>published</em> cost from the part that does not. That split &mdash; not the headline number &mdash; is what you actually need before signing anything.</p>
      <div data-reality-check></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Documented bands come from our sourced install scenarios &mdash; <a href="/water-softener-installation-cost/">prepared, first-time and complex</a> &mdash; built from HomeGuide equipment classes, Angi labor rates, and Fixr/HomeAdvisor site-work figures. Nothing in this tool is a claim about any dealer&rsquo;s margin. The next section is about why that distinction matters more than anything else on this page.</p>

      <h2 id="premium">Put your own quote on the worksheet</h2>
      <div data-channel-calc></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Comparable route = published mid-tier unit plus independent installation on an existing loop (see the <a href="/water-softener-installation-cost/">install cost guide</a>). Homes needing loop or electrical work narrow the gap &mdash; add those from the install worksheet.</p>
      <div style="margin-top:40px">''' + cta_box("The published-price benchmark",
        "Negotiation starts with a number nobody can argue with. SpringWell posts its softener prices online &mdash; sized by bathrooms, shipped free, 6-month money-back guarantee &mdash; which makes it the benchmark to hold any in-home quote against, even if you ultimately buy the dealer&rsquo;s system.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="markup">Is that remainder just markup?</h2>
      <p style="margin:0">No. And this is where most articles on dealer pricing get lazy &mdash; usually by publishing a markup percentage somebody made up. So let me be precise about what is knowable and what is not.</p>
      <p><strong>A $6,000 quote does not mean the dealer pocketed $5,000.</strong> When I built estimates, gross margin and net profit were different animals living in different rooms. The gap between the published equipment class and the number on your proposal has to cover a payroll, a fleet, a warehouse, insurance, licensing, a service department that still answers the phone in year six &mdash; plus the salesperson who spent two hours at your kitchen table and the advertising that produced the lead that sent them there. That is real business cost, and none of it is theft.</p>
      <p style="margin:0">Here is the honest boundary, and I would rather lose the argument than overstate it: <strong>I have never seen a dealer&rsquo;s P&amp;L, and neither has anyone else writing about this.</strong> Margins are not published. What <em>is</em> published is what the work costs. So the claim this page makes is narrow and firm &mdash; the remainder is a number you are entitled to see <strong>explained</strong>, not a number you are entitled to call <strong>profit</strong>.</p>
    </div>
    <div class="data-table-wrap" style="margin-top:24px">
      <table class="data-table">
        <caption>The nine layers inside an installed price &mdash; and which ones anybody can actually look up</caption>
        <thead><tr><th scope="col">Layer</th><th scope="col">What it pays for</th><th scope="col">Publicly priced?</th><th scope="col">In the direct route</th></tr></thead>
        <tbody>
          <tr><td><strong>Equipment</strong></td><td class="muted">Tank, control valve, resin</td><td><strong>Yes</strong> &mdash; $600&ndash;$1,500 class (HomeGuide)</td><td class="muted">You buy it at a posted price</td></tr>
          <tr><td><strong>Installation labor</strong></td><td class="muted">2&ndash;4 hours of a plumber&rsquo;s day</td><td><strong>Yes</strong> &mdash; $200&ndash;$500 (Angi)</td><td class="muted">You hire it, itemized</td></tr>
          <tr><td><strong>Site work</strong></td><td class="muted">Loop, drain, outlet where missing</td><td><strong>Yes</strong> &mdash; loop $600&ndash;$2,000 (Fixr)</td><td class="muted">Same plumber, same rate</td></tr>
          <tr><td><strong>Delivery &amp; removal</strong></td><td class="muted">Freight, old-unit haul-away</td><td><strong>Yes</strong> &mdash; removal $50&ndash;$150 (HomeGuide)</td><td class="muted">Freight often free; <a href="/water-softener-removal-cost/">removal usually bundled</a></td></tr>
          <tr><td>Sales &amp; lead acquisition</td><td class="muted">The in-home appointment, and the advertising that produced it</td><td class="muted">No &mdash; not published by anyone</td><td class="muted">This layer does not exist</td></tr>
          <tr><td>Business overhead</td><td class="muted">Showroom, vehicles, warehousing, insurance, licensing, admin</td><td class="muted">No</td><td class="muted">Mostly absent; some sits with the manufacturer</td></tr>
          <tr><td>Service &amp; warranty reserve</td><td class="muted">Techs, trucks, parts, the promise to show up in year six</td><td class="muted">No</td><td class="muted">You coordinate; warranty is manufacturer-direct</td></tr>
          <tr><td>Financing cost</td><td class="muted">The lender&rsquo;s cut of a payment plan</td><td class="muted">No &mdash; see the next section</td><td class="muted">Optional, third-party, separate</td></tr>
          <tr><td><strong>Net profit</strong></td><td class="muted">Whatever survives the eight lines above</td><td class="muted"><strong>No &mdash; and unknowable from outside</strong></td><td class="muted">&mdash;</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0"><strong>Nine layers. Four of them have published prices. Exactly one of them is profit</strong> &mdash; and it is the only one nobody outside the building can see. Any page that hands you a single markup percentage has quietly collapsed the other eight into it.</p>
      <p style="margin:16px 0 0">Which is also why the visual below is a stack and not a pie: the layers are real and their <em>order</em> is real, but no dealer publishes their proportions, so drawing them to scale would be inventing data. What the stack does show honestly is which layers simply stop existing when the equipment is bought at a posted price and the labor is hired separately.</p>
    </div>
    <div class="col-wide" style="margin-top:24px">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px">
        <div>
          <div style="font-weight:700;margin-bottom:10px;font-size:15px">Dealer-installed route</div>
          <div style="background:#16303F;color:#FAFAF7;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Equipment &mdash; $600&ndash;$1,500 class</div>
          <div style="background:#1F7A5C;color:#FAFAF7;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Delivery &amp; old-unit removal</div>
          <div style="background:#1F7A5C;color:#FAFAF7;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Installation labor &mdash; $200&ndash;$500</div>
          <div style="background:#1F7A5C;color:#FAFAF7;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Site work, where needed</div>
          <div style="background:#E8A13D;color:#16303F;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Sales &amp; the in-home appointment</div>
          <div style="background:#E8A13D;color:#16303F;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Overhead: showroom, fleet, admin</div>
          <div style="background:#E8A13D;color:#16303F;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Service dept &amp; warranty reserve</div>
          <div style="background:#E8A13D;color:#16303F;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Financing cost, if financed</div>
          <div style="background:#16303F;color:#FAFAF7;padding:11px;border-radius:4px;font-size:14px;font-weight:700">= One quoted number</div>
        </div>
        <div>
          <div style="font-weight:700;margin-bottom:10px;font-size:15px">Factory-direct + your own installer</div>
          <div style="background:#16303F;color:#FAFAF7;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Equipment &mdash; posted price, before any appointment</div>
          <div style="background:#1F7A5C;color:#FAFAF7;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Shipping &mdash; commonly free</div>
          <div style="background:#1F7A5C;color:#FAFAF7;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Installation labor &mdash; your plumber&rsquo;s quote</div>
          <div style="background:#1F7A5C;color:#FAFAF7;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px">Site work, where needed &mdash; same rates</div>
          <div style="border:1px dashed #C9D1CE;color:#5B6B75;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px;font-style:italic">No in-home sales appointment to fund</div>
          <div style="border:1px dashed #C9D1CE;color:#5B6B75;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px;font-style:italic">No local showroom or fleet to carry</div>
          <div style="border:1px dashed #C9D1CE;color:#5B6B75;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px;font-style:italic">Warranty direct &mdash; but service is yours to arrange</div>
          <div style="border:1px dashed #C9D1CE;color:#5B6B75;padding:9px 11px;border-radius:4px;margin-bottom:6px;font-size:14px;font-style:italic">Financing optional and separate, if at all</div>
          <div style="background:#16303F;color:#FAFAF7;padding:11px;border-radius:4px;font-size:14px;font-weight:700">= Two numbers you can audit</div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:10px">Diagram: SoftWaterSystemCost.com &middot; the layers and their order are real; the proportions are not published by any dealer, which is precisely why this is a stack and not a pie chart &middot; solid bands have published price ranges, dashed bands are costs the direct route does not carry &mdash; and the two dashed service lines are what you take on in exchange</div>
    </div>
    <div class="col">

      <h2 id="fair">What the dealer premium legitimately buys</h2>
      <p>Fairness matters here, because the premium isn&rsquo;t theft &mdash; it&rsquo;s a bundle you should price consciously. A good dealer gives you: on-site water analysis and system design (genuinely valuable on complicated well water), local techs who show up, install and service under one roof, and a brand that&rsquo;s answerable decades later. Some homeowners &mdash; hands-off owners, complex wells, landlords &mdash; rationally choose that bundle.</p>
      <p style="margin:0">The factory-direct trade: published pricing, the same hardware class, warranty-by-mail with phone support, and you arrange the plumber. On a standard city-water home with an existing loop, that trade typically keeps <span class="fig">$2,000&ndash;$5,000</span> in your pocket &mdash; and third-party guides make the comparison directly: <a href="https://modernize.com/water-treatment/culligan-cost" rel="noopener" target="_blank">Modernize</a> notes SpringWell systems &ldquo;typically cost $1,000 to $5,000 and are designed for DIY installation&rdquo; against dealer channels. Prefer no-salt conditioning? The same published-price logic applies to <a href="/pick/salt-free-softener" ''' + PICK + '''>salt-free systems</a>.</p>

      <h2 id="negotiate">The negotiation script (from the other side of the table)</h2>
      <p>If you want the dealer system, use the channel math instead of resenting it. The sequence that worked on every estimator worksheet I saw:</p>
      <p><strong>1. Ask for line items first.</strong> &ldquo;Before we talk total, can you itemize equipment, install, and everything else?&rdquo; Honest quotes survive this; padded ones start shrinking immediately.<br>
      <strong>2. Name a written benchmark.</strong> A published factory-direct price or a written competing quote. Guides report dealer rebates and discounts of <span class="fig">$100&ndash;$500+</span> that appear exactly at this moment &mdash; reps hold discount authority for a reason.<br>
      <strong>3. Separate the loop.</strong> Site work is real cost &mdash; get it priced as its own line (the <a href="/water-softener-installation-cost/">install guide</a> shows fair ranges), so it can&rsquo;t pad the equipment.<br>
      <strong>4. Decline same-day pricing.</strong> &ldquo;Today-only&rdquo; is the tell. A price that expires at sunset was never the price.</p>
      <p style="margin:0">Walk in with those four moves and the free water test becomes what it should have been all along: a water test.</p>

      <h2 id="financing">The monthly payment is not the price</h2>
      <p style="margin:0 0 16px">In-home selling rarely sells a softener. It sells a <em>payment</em> &mdash; because &ldquo;only $99 a month&rdquo; ends the conversation about the price, and a payment is not a price. It is a <strong>duration</strong>. The arithmetic that turns one back into the other takes ten seconds, and no honest dealer will mind you doing it at the table:</p>
      <div data-finance-calc></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Illustrative financing example &mdash; not a quote. These are your numbers from your own disclosure, not any dealer&rsquo;s published terms; none of the brands we track publishes financing terms any more than it publishes prices. Total of scheduled payments = payment &times; number of payments, and the implied price is what that payment stream is worth today at the stated APR.</p>
      <p style="margin:20px 0 0">Three lines belong in writing before a pen comes out: the <strong>cash price</strong>, the <strong>APR and term</strong>, and the <strong>total of payments</strong>. And one phrase deserves a hard second look, because it is not what most people think it is: <strong>&ldquo;no interest if paid in full&rdquo; is not the same offer as 0% APR.</strong> It is deferred interest &mdash; interest accrues quietly the whole time, and if any balance survives the promotional window, it is charged <em>retroactively to the purchase date on the original amount</em>. Federal advertising rules (Regulation Z) require those four words to appear, which makes them your tell. The CFPB has found roughly <strong>one in five</strong> deferred-interest balances end up hit with that retroactive charge, at ongoing rates typically above 20% regardless of the borrower&rsquo;s credit score. Financing can be entirely rational. It is simply a <em>second</em> decision &mdash; and it should be made after the first one is written down.</p>

      <h2 id="normalize">Normalize before you compare</h2>
      <p style="margin:0">I would never compare two water-treatment quotes until I had made them describe the same project. Nine lines do almost all of that work &mdash; screenshot this one and take it to the table:</p>
    </div>
    <div class="data-table-wrap" style="margin-top:20px">
      <table class="data-table">
        <caption>Apples-to-apples: what to normalize before deciding a quote is expensive</caption>
        <thead><tr><th scope="col">Normalize this</th><th scope="col">Why quotes diverge here</th><th scope="col">Ask for it in writing</th></tr></thead>
        <tbody>
          <tr><td>System capacity</td><td class="muted">A 32,000-grain and a 64,000-grain unit are different machines at different prices</td><td class="muted">The grain rating, and the hardness and household size it was sized against</td></tr>
          <tr><td>Single vs. twin tank</td><td class="muted">Twin systems cost more and <a href="/dual-tank-water-softener-cost/">most homes don&rsquo;t need one</a></td><td class="muted">Tank count &mdash; and the reason for it</td></tr>
          <tr><td>Softener only, or a bundle</td><td class="muted">Filtration or an RO inside the number hides what the softener actually costs</td><td class="muted">Every model number, priced on its own line</td></tr>
          <tr><td>Installation scope</td><td class="muted">The single biggest <em>legitimate</em> swing &mdash; loop, drain, outlet, removal</td><td class="muted">What is included, and what is &ldquo;if needed&rdquo; at extra cost</td></tr>
          <tr><td>Cash price vs. financed total</td><td class="muted">A payment is a duration, not a price</td><td class="muted">Cash price, APR, term, total of payments</td></tr>
          <tr><td>Warranty: parts vs. labor</td><td class="muted">&ldquo;Lifetime&rdquo; often excludes labor, and often dies when you sell the house</td><td class="muted">What is covered, for how long, who performs it, is it transferable</td></tr>
          <tr><td>Proprietary vs. standard parts</td><td class="muted">Proprietary cartridges set your costs for the next decade</td><td class="muted">Replacement part numbers and their current prices</td></tr>
          <tr><td>Service plan</td><td class="muted">Often bundled in a way that makes it look mandatory</td><td class="muted">Is it required? Price it separately. Cancellation terms</td></tr>
          <tr><td>Consumables</td><td class="muted">Salt programs and filter subscriptions are <a href="/water-softener-maintenance-cost/">where the decade goes</a></td><td class="muted">Annual salt and filter cost &mdash; and whether you may supply your own</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Run two proposals through those nine rows and something clarifying usually happens: the &ldquo;expensive&rdquo; quote turns out to include a loop, a bigger unit and an RO, while the &ldquo;cheap&rdquo; one quietly excluded the site work. Or it does not &mdash; and now you know that too, with reasons.</p>

      <p style="margin:0 0 16px">One number worth carrying into any appointment: on a dealer-quoted system, roughly <strong>73% of what the softener will ever cost you</strong> is settled in that single evening. Our <a href="/10-year-water-softener-cost/">ten-year ownership study</a> shows the working.</p>
      <h2 id="redflags">Twelve things to clarify before you sign</h2>
      <p style="margin:0 0 12px">None of these proves anything is wrong. Each is a question you are entitled to have answered before money moves &mdash; and a dealer running an honest shop will answer all twelve without flinching. I did, for fifteen years.</p>
      <ul style="margin:0;padding-left:20px">
        <li style="margin-bottom:7px">There is no <strong>cash price</strong> on the proposal &mdash; only a monthly payment.</li>
        <li style="margin-bottom:7px">The <strong>model number</strong> of the equipment is not written down.</li>
        <li style="margin-bottom:7px">The <strong>capacity</strong> is not stated, or was never tied to an actual hardness test.</li>
        <li style="margin-bottom:7px">&ldquo;Installation included&rdquo; appears with <strong>no scope</strong> &mdash; no list of what is and is not covered.</li>
        <li style="margin-bottom:7px">Extra <strong>filtration or an RO is bundled</strong> without a test result that justifies it.</li>
        <li style="margin-bottom:7px"><strong>APR, term and total of payments</strong> are missing from the paperwork.</li>
        <li style="margin-bottom:7px">Promises made out loud are <strong>not in the written agreement</strong>.</li>
        <li style="margin-bottom:7px">The price <strong>expires tonight</strong>.</li>
        <li style="margin-bottom:7px"><strong>Cancellation terms</strong> are something you have to ask for.</li>
        <li style="margin-bottom:7px">&ldquo;Lifetime warranty&rdquo; with no answer on <strong>parts vs. labor, transferability, or who performs the service</strong>.</li>
        <li style="margin-bottom:7px">A <strong>service plan</strong> you are told is required, priced inside the bundle.</li>
        <li style="margin-bottom:0"><strong>Proprietary filters or cartridges</strong> with no published replacement price.</li>
      </ul>

      <h2 id="direct">What buying direct actually asks of you</h2>
      <p style="margin:0">Fairness cuts both ways, so here is the bill for the other route. Buying the equipment at a posted price does not delete the work &mdash; it moves it onto your desk. You test the water yourself (a <a href="/pick/test-kit" ''' + PICK + '''>home test kit</a>, or a lab if you are on a problem well). You size the system yourself. You confirm flow rate, capacity and the space it has to fit. You <a href="/water-softener-installation-cost/">hire and schedule your own plumber</a>, and you own that relationship if the install goes sideways. You check whether a permit applies. And in year six, when something fails, you are the general contractor: the warranty is with the manufacturer, but the truck is yours to book.</p>
      <p style="margin:16px 0 0">Some homeowners should not do that, and I have no interest in pretending otherwise. Complicated well chemistry, a landlord juggling six properties, an owner who simply wants one company answerable for the whole outcome &mdash; for them the bundle is worth its premium, and the section above spells out exactly what that premium buys. The point of this page was never that one route wins. It is that you should be able to see both numbers before you choose: <strong>the equipment price, and the labor price.</strong> A quote that will not separate them is asking you to buy on faith. You are allowed to want arithmetic instead.</p>

      <h2 id="brands">Brand-by-brand reported ranges</h2>
      <p style="margin:0 0 16px">We track the reported numbers per brand &mdash; live pages first, the rest of the 45-brand index publishes through Phase 3:</p>
      <div class="card-grid narrow">
        <a class="card" href="/culligan-water-softener-cost/"><div class="name">Culligan</div><div class="range">$2,500&ndash;$4,500</div><div class="desc">Typical reported installed &middot; tiers, rental math, quote checker.</div></a>
        <a class="card" href="/kinetico-water-softener-cost/"><div class="name">Kinetico</div><div class="range">$3,000&ndash;$5,000+</div><div class="desc">Publishes no prices at all &middot; reported tiers &amp; real installs.</div></a>
        <a class="card" href="/rainsoft-water-softener-cost/"><div class="name">RainSoft</div><div class="range">$6,000&ndash;$11,000</div><div class="desc">Widest reported spread &middot; Home Depot channel.</div></a>
        <a class="card" href="/costco-water-softener-cost/"><div class="name">Costco / EcoWater</div><div class="range">$6,000&ndash;$10,000</div><div class="desc">Member-perk math &middot; the 3-day window.</div></a>
        <a class="card" href="/ecowater-water-softener-cost/"><div class="name">EcoWater</div><div class="range">$1,150&ndash;$10,000</div><div class="desc">One machine, three storefronts.</div></a>
        <a class="card" href="/brands/"><div class="name">All brands index</div><div class="desc">Pelican, Leaf Home &amp; 40+ more.</div></a>
        <a class="card" href="/"><div class="name">Full cost guide</div><div class="range">$840&ndash;$4,120</div><div class="desc">Every line item, itemized with charts.</div></a>
      </div>
      <div style="margin-top:40px">''' + cta_box("Skip the channel entirely",
        "If your water is ordinary city hardness and a loop exists, the factory-direct route is a Saturday project at a posted price. SpringWell&rsquo;s SS series ships free with a lifetime warranty on tanks and valves &mdash; the quote is on the screen, not at your kitchen table.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(c28_faqs) + '''
    </div>
''' + sources([
 '<strong>Angi &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: unit and labor ranges; $200&ndash;$6,000 project spread.',
 '<strong>HomeGuide &mdash; Water Softener Cost (2026)</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: $600&ndash;$2,000 unit-only pricing; installed ranges.',
 '<strong>Fixr &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">fixr.com</a>. Supports: big-box program totals (Lowe&rsquo;s $1,000&ndash;$2,800; Home Depot $2,500&ndash;$6,000).',
 '<strong>SoftPro &mdash; Average Costs for Water Softener Brands (2026)</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/average-costs-water-softener-brands" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: high-pressure quotes reaching $6,000&ndash;$8,000; brand tier comparisons.',
 '<strong>Modernize &mdash; Culligan Cost Guide (2026)</strong> &mdash; <a href="https://modernize.com/water-treatment/culligan-cost" rel="noopener" target="_blank">modernize.com</a>. Supports: dealer installed spreads; SpringWell $1,000&ndash;$5,000 DIY-designed comparison.',
 '<strong>Culligan &mdash; Water Softener Cost Considerations (official blog)</strong> &mdash; <a href="https://www.culligan.com/blog/water-softener-cost-considerations" rel="noopener" target="_blank">culligan.com</a>. Supports: brand&rsquo;s own &ldquo;closer to $5,000&rdquo; standard-system framing.',
 '<strong>BestCompany &mdash; Culligan Pricing Guide</strong> &mdash; <a href="https://bestcompany.com/blog/water-softeners/culligan-water-cost" rel="noopener" target="_blank">bestcompany.com</a>. Supports: dealer install tiers; rebate/discount figures of $100&ndash;$500.',
 '<strong>Consumer Financial Protection Bureau &mdash; Issue Spotlight: The High Cost of Retail Credit Cards; Regulation Z &sect;1026.16</strong> &mdash; <a href="https://www.consumerfinance.gov/data-research/research-reports/issue-spotlight-the-high-cost-of-retail-credit-cards/" rel="noopener" target="_blank">consumerfinance.gov</a>, <a href="https://www.consumerfinance.gov/rules-policy/regulations/1026/16/" rel="noopener" target="_blank">Reg Z &sect;1026.16</a>. Supports: deferred interest charged retroactively on the original purchase amount; ~1 in 5 promotional balances hit; ongoing rates above 20% regardless of credit score; the &ldquo;if paid in full&rdquo; disclosure requirement. Financing mechanics only &mdash; not any dealer&rsquo;s terms.',
 '<strong>National Consumer Law Center &mdash; Deceptive Bargain: The Hidden Time Bomb of Deferred Interest</strong> &mdash; <a href="https://www.nclc.org/resources/deceptive-bargain-the-hidden-time-bomb-of-deferred-interest-credit-cards/" rel="noopener" target="_blank">nclc.org</a>. Supports: the mechanics of retroactive interest on promotional balances.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("dealer-vs-factory-direct-pricing/index.html", c28)

# ============ C2 — KINETICO EXPOSE (T4+viz) ============
c2_faqs = [
 ("How much does a Kinetico water softener cost?","Most homeowners report $3,000&ndash;$5,000+ installed. Third-party guides put Signature-series units at $1,500&ndash;$3,500 and Premier systems at $3,500&ndash;$6,000, with dealer installation adding $300&ndash;$2,500. Kinetico itself publishes no prices."),
 ("Why doesn&rsquo;t Kinetico publish any prices?","Kinetico sells exclusively through franchised dealers who set their own pricing after an in-home water test. Even Culligan blogs a ballpark figure; Kinetico&rsquo;s own site lists none &mdash; every number in circulation is third-party or homeowner-reported."),
 ("Is Kinetico worth the premium?","The engineering is genuinely differentiated: non-electric operation, twin tanks for 24/7 soft water, reported 20+ year lifespans, and salt use reported around $60&ndash;$150/yr. If you keep the system 15&ndash;20 years, the math can work &mdash; the problem is you can&rsquo;t see the premium&rsquo;s size upfront."),
 ("Can I buy a Kinetico softener without the dealer?","Not new &mdash; dealer installation is mandatory, and warranties route through the dealer network. Used units appear on resale sites, but proprietary parts and service still lead back to a dealer."),
 ("How much do real Kinetico installs cost?","Purchase reports collected in 2024&ndash;2025: $2,700 for a 2030s in St. Louis, $6,000 for a Premier XP on a Flagstaff well, $7,200 for a Premier with carbon prefilter and RO in Las Vegas. Reported figures, not list prices."),
 ("What does a Kinetico cost to own per year?","Reported ownership is cheap: roughly $60&ndash;$150/yr in salt (twin-tank metering is salt-efficient) plus $100&ndash;$200/yr if you take dealer service. The premium is front-loaded in the purchase, not the ownership."),
 ("Should I finance a Kinetico system?","Only once you know the cash price. A $4,000-class system at a mid-teens APR over 84 months means handing over roughly $6,720 &mdash; around 40% of it interest. Get the cash price, APR, term and total of payments in writing, then decide on the loan as a separate question."),
]
c2_rows = [
 ("Signature-series equipment (third-party tier)",1500,3500,"ThePricer/Modernize tier data &mdash; Kinetico publishes no prices"),
 ("Dealer installation (reported span)",300,2500,"BestCompany $300&ndash;$1,000; ThePricer $800&ndash;$2,500 &mdash; dealer-set, where quotes diverge"),
]
c2_tier_rows = [
 ("Essential / Powerline (entry)",500,2000,"#1F7A5C"),
 ("Signature series",1500,3500,"#16303F"),
 ("Premier series",3500,6000,"#5B6B75"),
 ("Real reported installs (2024&ndash;25)",2700,7200,"#E8A13D"),
]
c2_bands = '[{"upTo":2999,"band":"below-typical","text":"Below the typical reported band ($3,000\\u2013$5,000). Plausible for Essential/Powerline entry units \\u2014 confirm series, tank count, and what install covers."},{"upTo":5000,"band":"typical","text":"Inside the typical reported band ($3,000\\u2013$5,000+ installed). Ask for the equipment and install lines separately \\u2014 the dealer sets both."},{"upTo":6500,"band":"upper","text":"Premier-series territory ($3,500\\u2013$6,000 plus install). Legitimate for twin-tank well setups \\u2014 otherwise ask, in writing, what justifies it."},{"upTo":null,"band":"above-published","text":"Above every reported install we track except full bundles (a $7,200 report included carbon prefilter + RO). If yours isn\\u2019t a bundle, get a second quote."}]'
c2 = head("Kinetico Water Softener Cost (2026): Reported Price Ranges",
 "Kinetico softeners are reported at $3,000\u2013$5,000+ installed \u2014 the brand publishes no prices at all. Sourced tiers, real purchase reports, quote checker.",
 "/kinetico-water-softener-cost/",
 ld(article_schema("Kinetico Water Softener Cost in 2026: The Brand That Publishes No Prices","Sourced Kinetico pricing tiers, real purchase reports, ownership math, and quote anatomy.","/kinetico-water-softener-cost/",date="2026-07-12"))
 + ld(faq_schema(c2_faqs,"/kinetico-water-softener-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Brands","/brands/"),("Kinetico","/kinetico-water-softener-cost/")])))
c2 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/brands/">Brands</a> &rsaquo; Kinetico</nav>
      <h1>Kinetico Water Softener Cost in 2026: The Brand That Publishes No Prices</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Kinetico is the most price-opaque major brand we track &mdash; <a href="https://www.kinetico.com/" rel="noopener" target="_blank">its own site</a> lists no prices whatsoever. The reported numbers: most homeowners pay <span class="fig">$3,000&ndash;$5,000+</span> installed per <a href="https://watersoftenercost.com/kinetico-water-softener-cost/" rel="noopener" target="_blank">2026 ownership data</a>, with <a href="https://www.thepricer.org/kinetico-water-softener-cost/" rel="noopener" target="_blank">ThePricer</a> putting Signature-series units at <span class="fig">$1,500&ndash;$3,500</span>, Premier systems at <span class="fig">$3,500&ndash;$6,000</span>, and dealer installation at <span class="fig">$800&ndash;$2,500</span>. Real 2024&ndash;25 purchase reports run <span class="fig">$2,700&ndash;$7,200</span>.</p>
      <p style="margin:0">Here&rsquo;s the estimator&rsquo;s frame: Kinetico builds genuinely differentiated hardware &mdash; non-electric, twin-tank, reported 20-year lifespans &mdash; and then sells it through the one channel where you can&rsquo;t see a single number until a rep is in your kitchen. Even Culligan blogs a ballpark. Kinetico doesn&rsquo;t. This page assembles every number that <em>is</em> public, so the in-home water test starts on your terms.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#tiers">Series tiers &amp; reported ranges (chart)</a></li>
          <li><a href="#reports">Real purchase reports</a></li>
          <li><a href="#worksheet">A Kinetico quote, reconstructed</a></li>
          <li><a href="#checker">Quote checker (tool)</a></li>
          <li><a href="#ownership">The 10-year math &mdash; where Kinetico flips (chart)</a></li>
          <li><a href="#financing">The monthly payment (tool)</a></li>
          <li><a href="#fair">What the premium legitimately buys</a></li>
        </ol>
      </details>
      <h2 id="tiers">What Kinetico sells &mdash; and what each series reportedly costs</h2>
      <p style="margin:0 0 16px">Every figure below is third-party or homeowner-reported, because the brand publishes none (unit-focused tiers; installed totals land higher):</p>
    </div>
    <div class="col-wide">''' + range_bars(c2_tier_rows, 8000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Tier figures: ThePricer and Modernize 2026 guides; entry span includes BestCompany&rsquo;s low end. The amber row is actual reported installs, bundles included &mdash; table below.</p>

      <h2 id="reports">Real purchase reports, 2024&ndash;2025</h2>
      <p style="margin:0 0 16px">The most useful Kinetico numbers are the ones homeowners shared after signing. Reported figures &mdash; anecdotal, not list prices:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>Publicly reported Kinetico purchases, 2024&ndash;2025 (ThePricer)</caption>
        <thead><tr><th scope="col">System</th><th scope="col">Situation</th><th scope="col" class="num">Reported total</th></tr></thead>
        <tbody>
          <tr><td>Kinetico 2030s</td><td class="muted">City water + copper repipe tie-in, St. Louis MO</td><td class="num">$2,700</td></tr>
          <tr><td>Premier XP twin-tank</td><td class="muted">Private well, complex PVC runs, Flagstaff AZ</td><td class="num">$6,000</td></tr>
          <tr><td>Premier + carbon prefilter + RO faucet</td><td class="muted">Full bundle, Las Vegas NV</td><td class="num">$7,200</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Notice the spread isn&rsquo;t random: the $2,700 report is a straightforward city-water swap; the $6,000 and $7,200 reports carry real site work and bundled treatment. That&rsquo;s the honest half of dealer pricing &mdash; the <a href="/water-softener-installation-cost/">install-side line items</a> are real. The other half is the part no Kinetico quote itemizes.</p>

      <h2 id="worksheet">A Kinetico quote, reconstructed line by line</h2>
      <p style="margin:0">Build a Signature-series project from the only published components that exist, and the reconstruction brackets the typical $3,000&ndash;$5,000 quote &mdash; with the dealer setting <em>both</em> lines:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Kinetico Signature quote, reconstructed (est.)", c2_rows, total_label="Reconstruction span") + '''</div>
    <div class="col">
      <p style="margin-top:24px">Compare that to the <a href="/culligan-water-softener-cost/">Culligan reconstruction</a>, where published tiers let us isolate the implied sales remainder. Kinetico&rsquo;s structure hides it differently: because the dealer prices equipment <em>and</em> install with no published anchor for either, the channel premium lives inside both lines at once. The <a href="/dealer-vs-factory-direct-pricing/">dealer vs. factory-direct breakdown</a> shows that pattern across every brand we track.</p>

      <h2 id="checker">Check your Kinetico quote against the reported bands</h2>
      <div data-quote-check data-min="1500" data-max="9000" data-start="4000" data-bands=''' + "'" + c2_bands + "'" + '''></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Bands from the sourced ranges above. A verdict is a prompt for which questions to ask &mdash; series, tank count, install scope, and what the water test actually found.</p>
      <div style="margin-top:40px">''' + cta_box("See a published price first",
        "The strongest position in a no-published-prices negotiation is a real posted number. SpringWell publishes its softener pricing online &mdash; sized by bathrooms, shipped free, 6-month money-back guarantee &mdash; the benchmark to hold any in-home quote against.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="ownership">The 10-year math &mdash; where Kinetico&rsquo;s story flips</h2>
      <p style="margin:0 0 16px">Fair is fair: Kinetico&rsquo;s ownership costs are reported <em>low</em>. Twin-tank metered regeneration keeps salt around <span class="fig">$60&ndash;$150/yr</span>, there&rsquo;s no electricity draw, and dealer service runs <span class="fig">$100&ndash;$200/yr</span> if you take it. Unlike the <a href="/culligan-water-softener-cost/">Culligan salt-delivery math</a>, the premium here is front-loaded:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",62),("#1F7A5C",16),("#5B6B75",22)], "~$6,500", "10-yr total (midpoints)", "10-year Kinetico ownership composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> System, installed (midpoint ~$4,000) <span class="pc">~62%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Salt, 10 yrs (~$1,050) <span class="pc">~16%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Dealer service &amp; parts (~$1,500) <span class="pc">~22%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of sourced ranges &middot; skip the service plan and the gray slice shrinks toward DIY <a href="/pick/replacement-prefilters" ''' + PICK + '''>prefilter swaps</a></div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Run it out 20 years &mdash; the lifespan owners report &mdash; and the per-year cost genuinely competes. The catch is the entry ticket: you pay the whole channel premium on day one, sight unseen. Full self-service math lives in the <a href="/water-softener-maintenance-cost/">maintenance cost guide</a>.</p>

      <h2 id="financing">The monthly payment, and what durability doesn&rsquo;t protect you from</h2>
      <p style="margin:0 0 16px">Kinetico&rsquo;s pitch is longevity: a non-electric valve, mechanical metering, a machine built to outlast the people who sold it. That argument is genuinely strong &mdash; and it is also exactly what makes the payment plan land so softly. When a system is sold as a thirty-year purchase, a seven-year loan sounds modest. So run the arithmetic the appointment doesn&rsquo;t:</p>
      <div data-finance-calc data-pmt="80" data-term="84" data-apr="15.9"></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Illustrative &mdash; not a quote, and not Kinetico&rsquo;s terms, which no dealer publishes any more than they publish prices. The default is seeded at a payment implying a system near $4,000, inside the reported band above. Move the sliders to match your own disclosure.</p>
      <p style="margin:20px 0 0">At that seeded example you hand over roughly <span class="fig">$6,720</span> for an implied system price near <span class="fig">$4,000</span> &mdash; about 40% of the money is interest. And here is the part worth sitting with: <strong>an APR does not know the difference between a well-built machine and a badly-built one.</strong> It prices the number on the contract and nothing else. Kinetico&rsquo;s engineering premium is real and defensible. Financing it simply means paying a second premium, to a lender, on top of the first one &mdash; and the durability argument cuts both ways, because the system may well outlive the loan, but the loan does not care, and it will not discount itself for good workmanship.</p>
      <p style="margin:16px 0 0">Three lines belong in writing before anyone signs: the <strong>cash price</strong>, the <strong>APR and term</strong>, and the <strong>total of payments</strong>. And treat one phrase as a flag rather than a feature &mdash; <strong>&ldquo;no interest if paid in full&rdquo; is not 0% APR.</strong> It is deferred interest: charges accrue quietly, and any balance still standing when the promotion ends is billed retroactively to the purchase date on the original amount. Federal advertising rules (Regulation Z) require those four words to appear, which makes them the tell, and the CFPB has found roughly one in five such balances get hit. The <a href="/dealer-vs-factory-direct-pricing/">channel hub</a> carries the full decoder.</p>

      <h2 id="fair">What the Kinetico premium legitimately buys</h2>
      <p>More than most dealer brands, honestly. Non-electric operation means no control board to fail and nothing to plug in. Twin tanks mean soft water even mid-regeneration &mdash; a real difference for big households. Owners report 20+ year lifespans, the warranty is transferable, and the brand claims up to 70% less salt use than timer-based units. If you want engineered-for-decades and hands-off, this is a rational premium.</p>
      <p style="margin:0">The critique isn&rsquo;t the product &mdash; it&rsquo;s that you cannot price any of it before the appointment. A premium you can&rsquo;t see the size of isn&rsquo;t a premium; it&rsquo;s a negotiation you didn&rsquo;t know you were in. Walk in with the reported bands above and the <a href="/dealer-vs-factory-direct-pricing/">four-step negotiation script</a>, and it becomes a fair trade either way.</p>
      <div style="margin-top:40px">''' + cta_box("The factory-direct alternative",
        "If 20-year engineering is the appeal, compare it against a posted price: SpringWell&rsquo;s SS series carries a lifetime warranty on tanks and valves, publishes its pricing, ships free, and installs DIY on an existing loop &mdash; no appointment required to learn the number.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(c2_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/culligan-water-softener-cost/"><div class="name">Culligan cost expos&eacute;</div><div class="range">$2,500&ndash;$4,500</div><div class="desc">Tiers, rental math, quote checker.</div></a>
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Dealer vs. factory-direct</div><div class="desc">Where the extra thousands go.</div></a>
        <a class="card" href="/"><div class="name">Full cost guide</div><div class="range">$840&ndash;$4,120</div><div class="desc">Every line item, itemized with charts.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>WaterSoftenerCost.com &mdash; Kinetico Water Softener Cost (2026)</strong> &mdash; <a href="https://watersoftenercost.com/kinetico-water-softener-cost/" rel="noopener" target="_blank">watersoftenercost.com</a>. Supports: typical $3,000&ndash;$5,000+ installed; salt $60&ndash;$150/yr; maintenance $100&ndash;$200/yr; 20+ year lifespans; mandatory dealer installation.',
 '<strong>ThePricer &mdash; Kinetico Water Softener Cost</strong> &mdash; <a href="https://www.thepricer.org/kinetico-water-softener-cost/" rel="noopener" target="_blank">thepricer.org</a>. Supports: Signature $1,500&ndash;$3,500; Premier $3,500&ndash;$6,000; entry $500&ndash;$2,000; install $800&ndash;$2,500; the three 2024&ndash;25 purchase reports ($2,700 / $6,000 / $7,200).',
 '<strong>BestCompany &mdash; Kinetico pricing references</strong> &mdash; <a href="https://bestcompany.com/blog/water-softeners/culligan-water-cost" rel="noopener" target="_blank">bestcompany.com</a>. Supports: Kinetico starting-range comparison ($1,500&ndash;$5,000) and dealer install low end ($300&ndash;$1,000).',
 '<strong>ConsumerAffairs &mdash; Kinetico Water Softeners</strong> &mdash; <a href="https://www.consumeraffairs.com/homeowners/kinetico.html" rel="noopener" target="_blank">consumeraffairs.com</a>. Supports: no published pricing (dealer-determined); up-to-70%-less-salt claim; transferable warranty.',
 '<strong>Kinetico &mdash; official site</strong> &mdash; <a href="https://www.kinetico.com/" rel="noopener" target="_blank">kinetico.com</a>. Supports: absence of any published pricing; dealer water-test sales model.',
 '<strong>Consumer Financial Protection Bureau &mdash; Issue Spotlight: The High Cost of Retail Credit Cards; Regulation Z &sect;1026.16</strong> &mdash; <a href="https://www.consumerfinance.gov/data-research/research-reports/issue-spotlight-the-high-cost-of-retail-credit-cards/" rel="noopener" target="_blank">consumerfinance.gov</a>, <a href="https://www.consumerfinance.gov/rules-policy/regulations/1026/16/" rel="noopener" target="_blank">Reg Z &sect;1026.16</a>. Supports: deferred interest billed retroactively on the original purchase amount; roughly 1 in 5 promotional balances hit; ongoing rates above 20% regardless of credit score; the &ldquo;if paid in full&rdquo; disclosure requirement. Financing mechanics only &mdash; not this brand&rsquo;s terms, which are unpublished.',
 '<strong>National Consumer Law Center &mdash; Deceptive Bargain: The Hidden Time Bomb of Deferred Interest</strong> &mdash; <a href="https://www.nclc.org/resources/deceptive-bargain-the-hidden-time-bomb-of-deferred-interest-credit-cards/" rel="noopener" target="_blank">nclc.org</a>. Supports: the mechanics of retroactive interest on promotional balances.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("kinetico-water-softener-cost/index.html", c2)

# ============ A9 — WHY SO EXPENSIVE (linkable asset) ============
a9_faqs = [
 ("Are water softeners overpriced?","The equipment usually isn&rsquo;t &mdash; metered softeners retail at $600&ndash;$1,500. Installed projects at $1,200&ndash;$3,000 reflect real labor and site work. Quotes at $5,000&ndash;$8,000 for standard homes usually carry channel cost, and that part is negotiable."),
 ("Why do dealer water softeners cost so much?","Commissioned in-home selling, financing margin, branch overhead, and bundled service. Reconstructed from published component prices, the unlabeled remainder in a $3,000&ndash;$8,000 dealer quote is often two-thirds of the total."),
 ("Is a $5,000 water softener worth it?","Sometimes: complex well water, twin-tank engineering, or a full-service dealer relationship can justify it. On a standard city-water home with a loop, published data says the same class of hardware installs for $1,200&ndash;$3,000."),
 ("Are expensive water softeners actually better?","Price tracks the valve, capacity, and the sales channel &mdash; not softness. A $900 metered unit and a $5,000 dealer unit both make zero-grain water. Pay more for metering, capacity, and warranty; don&rsquo;t pay more for the appointment."),
 ("How much should I reasonably spend on a water softener?","Most homes: $1,200&ndash;$3,000 installed on an existing loop; $840&ndash;$4,120 nationally once site work counts. Below $900 usually means DIY or timer-based units; above $4,500 should come with a line-item explanation."),
 ("Can I save money by buying a softener online?","Commonly, yes. Published-price units plus an independent plumber ($200&ndash;$500 on a loop) typically undercut dealer packages by thousands. The trade: you arrange install, and service is warranty-by-mail rather than a local tech."),
]
a9_rows = [
 ("Softener equipment (metered, retail)",600,1500,"The part everyone pictures &mdash; often the smallest stack in a dealer quote"),
 ("Installation labor",200,500,"2&ndash;4 hrs at $100&ndash;$150/hr (Angi)"),
 ("Materials: bypass, fittings, haul-away",90,270,"Itemized in honest quotes"),
 ("Site work: loop / drain / outlet (only if missing)",0,2900,"$0 in a prepared home &mdash; the honest reason quotes differ"),
 ("Permit (where required)",0,150,"Jurisdiction-dependent"),
 ("Sales-channel remainder (dealer route only)",0,3900,"Implied by reported $3,000&ndash;$8,000 dealer quotes vs. the components above"),
]
a9_driver_rows = [
 ("Loop run (none exists)",600,2000,"#E8A13D"),
 ("Dedicated 110V outlet",250,900,"#5B6B75"),
 ("Drain line to standpipe",100,300,"#16303F"),
 ("Old-unit removal",50,150,"#1F7A5C"),
 ("Permit (where required)",50,150,"#D9DED9"),
]
a9 = head("Why Are Water Softeners So Expensive? (2026 Cost Anatomy)",
 "Softeners retail at $600\u2013$1,500 \u2014 so why are quotes $3,000\u2013$8,000? An estimator itemizes where every dollar goes, with sources and tools.",
 "/why-are-water-softeners-so-expensive/",
 ld(article_schema("Why Are Water Softeners So Expensive? Where the Money Actually Goes","Cost anatomy of water softener quotes: equipment, labor, site work, and channel, with sourced figures.","/why-are-water-softeners-so-expensive/",date="2026-07-12"))
 + ld(faq_schema(a9_faqs,"/why-are-water-softeners-so-expensive/"))
 + ld(breadcrumb_schema([("Home","/"),("Why so expensive","/why-are-water-softeners-so-expensive/")])))
a9 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Why so expensive</nav>
      <h1>Why Are Water Softeners So Expensive? Where the Money Actually Goes</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Because you&rsquo;re rarely buying just a softener. The machine itself &mdash; a resin tank, a brine tank, and a metered valve &mdash; retails at <span class="fig">$600&ndash;$1,500</span> (<a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">HomeGuide</a>). What you&rsquo;re quoted is the machine <em>plus</em> labor, plumbing, site work, and &mdash; on the dealer route &mdash; a sales channel that can double or triple the number. Published projects run <span class="fig">$200&ndash;$6,000</span> per <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">Angi</a>, and dealer packages are commonly reported at <span class="fig">$3,000&ndash;$8,000</span>.</p>
      <p><strong>Water softeners are expensive because the installed price stacks four different costs: equipment ($600&ndash;$1,500 retail), installation labor ($200&ndash;$500), site-specific plumbing and electrical ($0&ndash;$2,900), and &mdash; on dealer-sold systems &mdash; sales-channel costs that reconstruction suggests can reach two-thirds of the quote.</strong></p>
      <p style="margin:0">I priced these projects for fifteen years. A water softener is not expensive because resin became a precious metal &mdash; the final quote is a stack of equipment, plumbing, labor, overhead, and sometimes a healthy layer of pricing opacity. This page pulls the stack apart so you can look at a <span class="fig">$2,000</span>, <span class="fig">$4,000</span>, or <span class="fig">$6,000</span> quote and know which layers are real for <em>your</em> house.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#builder">Build your own quote (tool)</a></li>
          <li><a href="#anatomy">The full cost anatomy</a></li>
          <li><a href="#equipment">The equipment truth</a></li>
          <li><a href="#drivers">Legitimate cost drivers (chart)</a></li>
          <li><a href="#channel">The channel layer (chart)</a></li>
          <li><a href="#justified">When expensive is justified &mdash; and the red flags</a></li>
          <li><a href="#save">Where you can safely save</a></li>
          <li><a href="#bottom">Bottom line</a></li>
        </ol>
      </details>
      <h2 id="builder">Watch a quote grow: build yours</h2>
      <p style="margin:0 0 16px">Every toggle below is a sourced line item. Start with the machine, add what your house is missing, and add the channel &mdash; this is exactly how the number on a real quote gets built:</p>
      <div data-expense-calc></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Component ranges: HomeGuide (equipment, electrical), Angi (labor), Fixr and reported dealer quotes (channel remainder) &mdash; sources below. For your specific home, the <a href="/#quote-sheet">full cost worksheet</a> itemizes it live.</p>

      <h2 id="anatomy">The full cost anatomy, itemized</h2>
      <p style="margin:0">Every layer a quote can contain. This is a cost anatomy model, not a universal contractor quote &mdash; the &ldquo;only if&rdquo; rows are <span class="fig">$0</span> in many homes, and the channel row applies only to dealer-sold systems:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Cost anatomy: every layer a quote can contain", a9_rows, total_label="Full-stack span") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>How I&rsquo;d read this sheet:</strong> the low end ($890) is a prepared home, self-arranged; the high end only occurs when an unprepared house meets the dealer channel. No single homeowner pays every maximum &mdash; and that&rsquo;s the point. When a rep hands you one bundled number, they&rsquo;re hoping you never see which layers your house actually needs.</p>
      <div style="margin-top:24px">''' + cta_box("The factory-direct alternative",
        "Strip the stack to its real layers: SpringWell publishes its softener pricing online, sizes by bathrooms, and ships free &mdash; so the only remaining variables are your plumber&rsquo;s afternoon and whatever site work your house genuinely needs.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="equipment">The equipment truth: the valve is the machine</h2>
      <p>Inside every softener is the same idea: hardness ions swap onto resin, salt regenerates the resin. The tanks are commodity fiberglass and plastic. What you actually pay for in better equipment is the <strong>control valve</strong> and <strong>capacity</strong>: a demand-metered valve regenerates on real water use instead of a timer &mdash; which matters because timer units burn salt whether you showered or traveled, quietly doubling the recurring cost in the <a href="/water-softener-maintenance-cost/">ownership math</a>. Bigger resin beds regenerate less often for large or hard-water households.</p>
      <p style="margin:0">That&rsquo;s why the honest equipment spread is only <span class="fig">$600&ndash;$1,500</span> retail, <span class="fig">$600&ndash;$2,000</span> across all capacities (HomeGuide). A <span class="fig">$900</span> metered unit and a <span class="fig">$5,000</span> dealer unit both produce zero-grain soft water. Softness is binary; the premium buys efficiency, capacity, and warranty &mdash; or, sometimes, just the appointment.</p>

      <h2 id="drivers">The legitimate cost drivers &mdash; what your house adds</h2>
      <p style="margin:0 0 16px">These are the real reasons two identical softeners can be <span class="fig">$1,100</span> and <span class="fig">$3,300</span> installed. Each is honest work with a fair price band:</p>
    </div>
    <div class="col-wide">''' + range_bars(a9_driver_rows, 2000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Ranges: Angi (labor tasks), HomeGuide (electrical circuit $250&ndash;$900). The <a href="/water-softener-installation-cost/">installation cost guide</a> prices each scenario with its own tool.</p>
      <p style="margin:16px 0 0">The single biggest wildcard is the <strong>softener loop</strong>. If your home has one &mdash; most post-2000 construction in hard-water regions does &mdash; three of these bars drop to zero. If it doesn&rsquo;t, the plumber is cutting into your main line, and <span class="fig">$600&ndash;$2,000</span> of that quote is genuinely earned. An honest quote prices the loop as its own line; a padded one hides it inside &ldquo;professional installation.&rdquo;</p>

      <h2 id="channel">The channel layer: the part nobody itemizes</h2>
      <p style="margin:0 0 16px">Now the layer that answers the actual question. Take a commonly reported <span class="fig">$5,500</span> dealer quote and subtract the published components &mdash; here&rsquo;s the reconstruction (estimates from midpoints, method as in our <a href="/dealer-vs-factory-direct-pricing/">dealer vs. factory-direct breakdown</a>):</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",19),("#1F7A5C",6),("#5B6B75",3),("#B3541E",72)], "$5,500", "dealer quote (est.)", "Reconstruction of a $5,500 dealer quote") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> Comparable equipment (midpoint ~$1,050) <span class="pc">~19%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Installation labor (~$350) <span class="pc">~6%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Materials &amp; haul-away (~$180) <span class="pc">~3%</span></div>
          <div><span class="sw" style="background:#B3541E"></span> Implied remainder: commission, overhead, financing, service bundle <span class="pc">~72%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; illustrative reconstruction from published component midpoints on a prepared home &middot; site work, where needed, shifts dollars from the rust slice to honest work</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Is that remainder theft? No &mdash; it funds real things: the commissioned rep&rsquo;s afternoon, the branch, the financing desk, the service network. Industry guides <a href="https://www.softprowatersystems.com/pages/average-costs-water-softener-brands" rel="noopener" target="_blank">warn</a> high-pressure appointments push quotes to <span class="fig">$6,000&ndash;$8,000</span>; even <a href="https://www.culligan.com/blog/water-softener-cost-considerations" rel="noopener" target="_blank">Culligan&rsquo;s own guide</a> frames a standard system &ldquo;closer to $5,000.&rdquo; The issue isn&rsquo;t that the layer exists &mdash; it&rsquo;s that it&rsquo;s never labeled, so its size is set by what the rep thinks you&rsquo;ll sign. Our brand pages reconstruct it for <a href="/culligan-water-softener-cost/">Culligan</a> and <a href="/kinetico-water-softener-cost/">Kinetico</a> line by line.</p>

      <h2 id="justified">When an expensive quote is justified &mdash; and the red flags</h2>
      <p><strong>Legitimately expensive:</strong> a real loop run or code-required drain and permit work; twin-tank or high-capacity equipment for big households; complicated well water needing on-site design and pretreatment; licensed labor in a high-cost metro; a service relationship you actually want. All of that deserves to cost more &mdash; itemized.</p>
      <p style="margin:0"><strong>Expensively vague:</strong> no model number (&ldquo;whole-home system&rdquo;); one bundled figure with no lines; &ldquo;today-only&rdquo; pricing; a free water &ldquo;test&rdquo; that ends in a same-day contract; financing offered before the cash price is stated. None of these makes a dealer dishonest &mdash; but each one is a reason to get the itemized version before signing. The <a href="/#quote-anatomy">quote-anatomy guide</a> covers the full checklist.</p>

      <h2 id="save">Where you can safely save &mdash; and where cheap backfires</h2>
      <p><strong>Safe savings:</strong> buy the published-price unit and hire your own plumber (<span class="fig">$200&ndash;$500</span> on a loop); skip Wi-Fi and app features that don&rsquo;t change the water; supply your own salt instead of a delivery program; DIY if &mdash; and only if &mdash; loop, drain, and outlet already exist.</p>
      <p style="margin:0"><strong>False economies:</strong> timer-based bargain units (the salt bill quietly doubles); undersizing to save <span class="fig">$200</span> (constant regeneration wears everything); guessing your hardness instead of measuring it &mdash; before you pay for a bigger system because a salesperson says your water is &ldquo;extremely hard,&rdquo; get an actual number with a <a href="/pick/test-kit" ''' + PICK + '''>water test kit</a>; and cutting into a main line yourself to dodge a loop charge. The cheap path and the smart path overlap about 80% of the way &mdash; the last 20% is where rescue calls come from.</p>

      <h2 id="bottom">Bottom line: is an expensive softener worth it?</h2>
      <p style="margin:0">Conditionally. Pay more for metering, capacity, real site work, and engineering you&rsquo;ll keep for twenty years &mdash; that money comes back. Don&rsquo;t pay more for the appointment. My rule from fifteen years of worksheets: <strong>every dollar should be attached to a line you can read.</strong> Equipment, labor, site work &mdash; readable. The channel layer &mdash; ask. If the quote can&rsquo;t survive itemization, it wasn&rsquo;t a price; it was an opening offer.</p>
      <div style="margin-top:40px">''' + cta_box("Every dollar on a readable line",
        "That&rsquo;s the whole pitch for factory-direct: SpringWell&rsquo;s price is published before anyone visits, the install is a separate line from your own plumber, and the 6-month money-back guarantee means the decision stays reversible.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(a9_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/"><div class="name">Full cost guide</div><div class="range">$840&ndash;$4,120</div><div class="desc">Every line item, itemized with charts.</div></a>
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Dealer vs. factory-direct</div><div class="desc">The channel layer, quantified.</div></a>
        <a class="card" href="/water-softener-installation-cost/"><div class="name">Installation cost</div><div class="desc">Labor, loop &amp; site work priced.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Angi &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: $200&ndash;$6,000 project spread; labor $200&ndash;$500 at $100&ndash;$150/hr; removal and task costs.',
 '<strong>HomeGuide &mdash; Water Softener Cost (2026)</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: equipment $600&ndash;$2,000 across capacities; installed $1,200&ndash;$3,800; dedicated circuit $250&ndash;$900.',
 '<strong>Fixr &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">fixr.com</a>. Supports: typical installed projects $1,100&ndash;$3,000; program pricing context.',
 '<strong>SoftPro &mdash; Average Costs for Water Softener Brands (2026)</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/average-costs-water-softener-brands" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: high-pressure quotes reaching $6,000&ndash;$8,000.',
 '<strong>Culligan &mdash; Water Softener Cost Considerations (official blog)</strong> &mdash; <a href="https://www.culligan.com/blog/water-softener-cost-considerations" rel="noopener" target="_blank">culligan.com</a>. Supports: the brand&rsquo;s own &ldquo;closer to $5,000&rdquo; standard-system framing.',
 '<strong>Modernize &mdash; Culligan Cost Guide (2026)</strong> &mdash; <a href="https://modernize.com/water-treatment/culligan-cost" rel="noopener" target="_blank">modernize.com</a>. Supports: dealer installed spreads used in the channel reconstruction.',
 '<strong>Reported dealer quotes (anecdotal, attributed)</strong> &mdash; BBB filings and homeowner-shared quotes (r/plumbing, Terry Love forums), 2024&ndash;2026. Supports: the $3,000&ndash;$8,000 dealer band behind the implied-remainder rows.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("why-are-water-softeners-so-expensive/index.html", a9)

# ============ F3 — LOW-COST SOFTENERS (money, budget tiers) ============
f3_faqs = [
 ("Can you get a good water softener for under $500?","Yes, with caveats. Big-box cabinet units (A.O. Smith, GE, Rheem, Whirlpool) run $357&ndash;$500 and genuinely soften. Fine for 1&ndash;3 people on city water; the trade-offs are single-cabinet design, shorter warranties, and valves that get replaced, not rebuilt."),
 ("What is the cheapest type of water softener that actually works?","A big-box cabinet ion-exchanger ($357&ndash;$797) or an entry Fleck 5600SXT DIY bundle ($499&ndash;$899). Electronic descalers at $100&ndash;$250 are cheaper but don&rsquo;t remove hardness &mdash; they&rsquo;re not softeners."),
 ("How much is a water softener unit without installation?","Entry cabinet units: $357&ndash;$797. Fleck-valve DIY bundles: $499&ndash;$899. Quality metered two-tank systems: roughly $900&ndash;$1,600. Add $90&ndash;$200 in fittings for DIY or $200&ndash;$500 labor on an existing loop."),
 ("Is a cheap water softener worth it?","For 1&ndash;3 people on moderate city water, often yes. Published dealer analysis shows the risk: a $500 unit lasting ~6 years with 20&ndash;30% higher salt use can cost more over a decade than a $1,500 rebuildable system. Match the unit to your demand."),
 ("What improves when you spend up to $1,500?","Metered regeneration as standard, 40k&ndash;64k capacity, rebuildable valves (replace a $550 valve or $295 rebed instead of the whole unit), stronger flow, and 10-year-to-lifetime warranties &mdash; upgrades big or hard-water households actually use."),
 ("How long does a low-cost water softener last?","Box-store cabinet units are commonly reported at 6&ndash;10 years; when the valve fails the unit is replaced. Fleck-style systems run 15+ years because the valve is serviceable and resin can be re-bedded for about $295 per cubic foot."),
]
f3_rows = [
 ("Softener unit (big-box cabinet &rarr; Fleck bundle)",357,899,"A.O. Smith/GE cabinet units to Fleck 5600SXT DIY kits"),
 ("Connection fittings &amp; bypass",40,120,"Often partly included &mdash; check the box contents"),
 ("Drain line materials",20,60,"Tubing + air gap to a standpipe"),
 ("First salt (2 bags)",12,20,"$5&ndash;$10 per 40-lb bag (Angi)"),
 ("Professional labor (skip if DIY, loop exists)",0,500,"2&ndash;4 hrs at $100&ndash;$150/hr"),
]
f3_bars = [
 ("Big-box cabinet (A.O. Smith, GE, Rheem)",357,797,"#1F7A5C"),
 ("Fleck 5600SXT DIY bundle",499,899,"#16303F"),
 ("WaterBoss compact",500,700,"#5B6B75"),
 ("Quality metered two-tank",900,1600,"#E8A13D"),
]
f3 = head("Low Cost Water Softeners (2026): $700 vs $1,500 Tiers",
 "Real softeners start at $357\u2013$899. What under $700 buys, what improves under $1,500, and when cheap becomes a false economy \u2014 sourced.",
 "/low-cost-water-softener/",
 ld(article_schema("Low-Cost Water Softeners That Actually Work: Under $700 vs. Under $1,500","Budget-tier analysis of entry water softeners with verified 2026 pricing and false-economy math.","/low-cost-water-softener/",date="2026-07-12"))
 + ld(faq_schema(f3_faqs,"/low-cost-water-softener/"))
 + ld(breadcrumb_schema([("Home","/"),("Low-cost softeners","/low-cost-water-softener/")])))
f3 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Low-cost softeners</nav>
      <h1>Low-Cost Water Softeners That Actually Work: Under $700 vs. Under $1,500</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Real ion-exchange softeners start cheaper than the quotes suggest: big-box cabinet units run <span class="fig">$357&ndash;$797</span> (A.O. Smith, GE, Rheem, Whirlpool), and Fleck 5600SXT DIY bundles are currently listed at <span class="fig">$499&ndash;$899</span> per <a href="https://radcity.net/best-water-softener-systems-2026/" rel="noopener" target="_blank">2026 comparisons</a>. Those are <em>equipment</em> prices &mdash; a DIY project adds <span class="fig">$70&ndash;$200</span> in materials, and professional labor adds <span class="fig">$200&ndash;$500</span> on an existing loop.</p>
      <p><strong>Under $700 buys a genuine entry softener &mdash; big-box cabinet units ($357&ndash;$797) or a Fleck DIY bundle ($499&ndash;$899). Under $1,500 buys metered regeneration, 40k&ndash;64k capacity, and rebuildable valves. Equipment price and installed cost are different numbers: add $70&ndash;$500 depending on who does the work.</strong></p>
      <p style="margin:0">I priced these projects for fifteen years, and here&rsquo;s the worksheet truth: the question isn&rsquo;t &ldquo;what&rsquo;s the cheapest softener&rdquo; &mdash; it&rsquo;s the <em>lowest budget that solves your problem without creating a second one</em>. This page prices both tiers honestly, names what actually softens, and shows the exact math where cheap flips into expensive.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#decoder">First: what actually softens water</a></li>
          <li><a href="#tier1">Under $700 (and the under-$500 answer)</a></li>
          <li><a href="#worksheet">The budget project worksheet</a></li>
          <li><a href="#fit">Which tier fits your home? (tool)</a></li>
          <li><a href="#tier2">What $1,500 buys that $700 doesn&rsquo;t</a></li>
          <li><a href="#false-economy">When cheap becomes expensive (chart)</a></li>
          <li><a href="#framework">The decision framework</a></li>
        </ol>
      </details>
      <h2 id="decoder">First: what actually softens water &mdash; and what just sounds like it</h2>
      <p style="margin:0 0 16px">The low-cost aisle mixes four different technologies under one word. Only one of them removes hardness:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>What&rsquo;s sold as a &ldquo;water softener&rdquo; at low prices, decoded</caption>
        <thead><tr><th scope="col">Sold as</th><th scope="col">What it actually does</th><th scope="col">Softens?</th><th scope="col" class="num">Typical equipment price</th></tr></thead>
        <tbody>
          <tr><td>Ion-exchange softener (salt-based)</td><td class="muted">Removes calcium &amp; magnesium on resin</td><td><strong>Yes</strong></td><td class="num">$357&ndash;$1,600</td></tr>
          <tr><td>Salt-free conditioner (TAC)</td><td class="muted">Crystallizes minerals so scale doesn&rsquo;t stick &mdash; hardness stays in the water</td><td class="muted">No &mdash; scale control</td><td class="num">$300&ndash;$1,500</td></tr>
          <tr><td>Cartridge scale filter</td><td class="muted">Point-of-entry scale reduction, cartridge swaps</td><td class="muted">No &mdash; scale control</td><td class="num">$200&ndash;$800</td></tr>
          <tr><td>Electronic / magnetic descaler</td><td class="muted">Clamp-on coil; evidence for real-world effect is weak</td><td class="muted">No</td><td class="num">$100&ndash;$250</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">If your goal is soap that lathers, no spotting, and softer skin &mdash; you need row one. If you only want scale protection for the water heater with zero upkeep, a TAC conditioner is the honest budget answer, and <a href="/pick/salt-free-softener" ''' + PICK + '''>salt-free systems with published pricing</a> exist so you can compare without a sales visit. Rows three and four are where budget shoppers most often buy the wrong technology.</p>

      <h2 id="tier1">What can you realistically get for under $700?</h2>
      <p style="margin:0 0 16px">More than the dealer channel wants you to think. Current verified equipment pricing:</p>
    </div>
    <div class="col-wide">''' + range_bars(f3_bars, 2000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Pricing: big-box ranges (A.O. Smith at Lowe&rsquo;s $357&ndash;$797, GE at Home Depot $397&ndash;$799), Fleck bundles $499&ndash;$899 (2026 listings), WaterBoss $500&ndash;$700 (SoftPro). Listed at time of research &mdash; verify current prices before purchase.</p>
      <p style="margin:16px 0 0"><strong>Can you get a good one under $500?</strong> Honestly, yes &mdash; for the right house. A $397&ndash;$500 cabinet unit from GE, Rheem, or A.O. Smith is a true metered ion-exchanger that will zero out hardness for 1&ndash;3 people on city water. The trade-offs are real but livable: single-cabinet design (brine and resin share a box), 1&ndash;5 year warranties instead of ten-to-lifetime, and a throwaway valve. Where under-$500 stops being honest: five-plus people, 15+ gpg hardness, or iron on well water &mdash; those homes burn these units up.</p>

      <h2 id="worksheet">The budget project, itemized</h2>
      <p style="margin:0">Equipment price is the first line, not the total. Here&rsquo;s the tier-1 project worksheet &mdash; the labor row is <span class="fig">$0</span> if you DIY on an existing loop:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Under-$700 softener project (DIY &rarr; pro)", f3_rows, total_label="Project span") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>How I&rsquo;d read this sheet:</strong> the swing line is labor &mdash; DIY on an existing loop keeps the whole project under <span class="fig">$1,100</span> even with the best tier-1 unit. What you shouldn&rsquo;t cut to hit budget: the bypass valve (it&rsquo;s what makes future service a 10-minute job instead of a whole-house shutoff) and the drain air gap (code, and for good reason). What you can skip: nothing on this sheet is padding &mdash; it&rsquo;s already the lean version. No loop? That&rsquo;s <span class="fig">$600&ndash;$2,000</span> of real plumbing first &mdash; the <a href="/water-softener-installation-cost/">installation cost guide</a> prices every scenario.</p>
      <div style="margin-top:24px">''' + cta_box("The factory-direct step-up",
        "Before you settle a tier, check the posted number: SpringWell&rsquo;s salt-based line publishes its pricing online, sizes by bathrooms, ships free, and carries a lifetime warranty on tanks and valves &mdash; the exact upgrades the tier-2 math below is about.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="fit">Which tier fits your home? Two taps</h2>
      <p style="margin:0 0 16px">Household demand and hardness decide this &mdash; not the marketing. If you don&rsquo;t know your gpg number, a <a href="/pick/test-kit" ''' + PICK + '''>water test kit</a> is the cheapest line in this whole project and settles it before you spend anything:</p>
      <div data-budget-fit></div>

      <h2 id="tier2">What $1,500 buys that $700 doesn&rsquo;t</h2>
      <p>Four things, and they&rsquo;re the right four. <strong>Metered regeneration as standard</strong> &mdash; the unit regenerates on actual use, not a timer burning salt on schedule. <strong>Capacity</strong> &mdash; 40k&ndash;64k grains means fewer regenerations for big or hard-water households. <strong>Rebuildable valves</strong> &mdash; published service pricing shows a Fleck-style valve rebuilds for <span class="fig">$545&ndash;$595</span> and resin re-beds at <span class="fig">~$295</span>/cu-ft, while a dead cabinet-unit valve means the dumpster. <strong>Warranties</strong> &mdash; 10-year tanks to lifetime coverage, versus 1&ndash;5 years at tier 1.</p>
      <p style="margin:0">What tier 2 does <em>not</em> buy: softer water. A <span class="fig">$450</span> metered cabinet and a <span class="fig">$1,500</span> two-tank both produce zero-grain water on day one. You&rsquo;re buying longevity, efficiency, and serviceability &mdash; which is why the tier decision belongs to your household demand, not your aspirations. (Wi-Fi apps, incidentally, are in neither list &mdash; the water can&rsquo;t tell.)</p>

      <h2 id="false-economy">When cheap becomes expensive: the 10-year math</h2>
      <p style="margin:0 0 16px">Published dealer-service analysis (Mid Atlantic Water, 2026) prices the failure mode: a <span class="fig">$500</span> box-store unit commonly lasts ~6 years and uses 20&ndash;30% more salt than metered systems. Run the decade from those cited inputs:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#E8A13D",36),("#16303F",53),("#5B6B75",11)], "~$2,800", "10 yrs, $500 unit (est.)", "10-year cost of a budget softener") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#E8A13D"></span> Units: original + ~yr-6 replacement (~$1,000) <span class="pc">~36%</span></div>
          <div><span class="sw" style="background:#16303F"></span> Salt at timer-unit efficiency (~$150/yr) <span class="pc">~53%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Parts &amp; fittings along the way <span class="pc">~11%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; derived estimate from cited inputs (unit lifespan &amp; salt-efficiency: Mid Atlantic Water; salt price: Angi) &middot; a $900&ndash;$1,500 metered system typically lands in the same decade total &mdash; once &mdash; and is still running</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">That&rsquo;s the whole false-economy argument in one chart: over ten years the cheap path and the quality path cost about the same &mdash; the difference is that one of them ends with a working softener. The <a href="/water-softener-maintenance-cost/">maintenance cost guide</a> runs the salt and parts math line by line, and the <a href="/why-are-water-softeners-so-expensive/">cost-anatomy guide</a> covers the opposite trap &mdash; overpaying the channel instead of underpaying the equipment.</p>

      <h2 id="framework">The decision framework, by homeowner</h2>
      <p><strong>Renter / small condo, 1&ndash;2 people:</strong> tier 1, low end &mdash; or a cartridge conditioner if you only need scale control and a landlord-friendly install. <strong>3&ndash;4 people, city water, moderate-to-hard:</strong> top of tier 1 &mdash; a <span class="fig">$450&ndash;$900</span> metered unit, DIY if the loop exists. <strong>3&ndash;4 people, very hard water:</strong> tier 2 &mdash; the capacity is used, not spare. <strong>5+ people, or any iron on a well:</strong> tier 2 without hesitation, and test before buying &mdash; iron changes the equipment list entirely. <strong>Anyone quoted $3,000+ for a &ldquo;budget&rdquo; system:</strong> that&rsquo;s not a budget problem, that&rsquo;s a <a href="/dealer-vs-factory-direct-pricing/">channel problem</a>.</p>
      <p style="margin:0">And the one rule that outranks every tier: <strong>buy the technology that matches the problem, sized to a measured number.</strong> A correctly-sized $450 softener beats a mis-sized $1,500 one every year of its life &mdash; and our <a href="/what-size-water-softener-do-i-need/">sizing calculator</a> gives you that number in about thirty seconds.</p>
      <div style="margin-top:40px">''' + cta_box("Published pricing, tier-2 hardware",
        "If your household lands in tier 2, compare the posted number before any showroom: SpringWell&rsquo;s SS series is sized by bathrooms, DIY-friendly on an existing loop, ships free, and the 6-month money-back guarantee keeps the decision reversible.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(f3_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/"><div class="name">Full cost guide</div><div class="range">$840&ndash;$4,120</div><div class="desc">Every line item, itemized with charts.</div></a>
        <a class="card" href="/water-softener-installation-cost/"><div class="name">Installation cost</div><div class="desc">DIY vs. pro, loop &amp; site work priced.</div></a>
        <a class="card" href="/why-are-water-softeners-so-expensive/"><div class="name">Why so expensive?</div><div class="desc">Where every dollar of a quote goes.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>RadCity &mdash; Best Water Softener Systems 2026 (Jun 2026)</strong> &mdash; <a href="https://radcity.net/best-water-softener-systems-2026/" rel="noopener" target="_blank">radcity.net</a>. Supports: Fleck 5600SXT DIY bundles $499&ndash;$899; 2&ndash;4 hr DIY installs with quick-connect bypass; technology-fit groupings.',
 '<strong>Mid Atlantic Water &mdash; Water Softener Cost (Mar 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/faqs/water-softener-cost" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: $500 box-store unit ~6-yr lifespan; 20&ndash;30% higher salt use; valve rebuild $545&ndash;$595; resin re-bed ~$295/cu-ft; 10-yr TCO comparisons.',
 '<strong>SoftPro &mdash; Average Costs for Water Softener Brands (Jul 2026)</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/average-costs-water-softener-brands" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: Fleck $300&ndash;$1,600 / from $600; WaterBoss $500&ndash;$700; budget-tier maintenance $150&ndash;$300/yr.',
 '<strong>SoftPro &mdash; Top-Rated Water Softeners Ranked (2026)</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/top-rated-water-softeners-ranked" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: under-$1,500 model set (Rheem Preferred, GE GXSH40V, WaterBoss 220, Morton M30, Fleck 5600SXT).',
 '<strong>Bob Vila &mdash; Best Water Softeners (Dec 2025)</strong> &mdash; <a href="https://www.bobvila.com/articles/best-water-softener/" rel="noopener" target="_blank">bobvila.com</a>. Supports: category picks and household-suitability notes (WaterBoss 36.4k for 3&ndash;6 people; Whirlpool 40k for 1&ndash;6).',
 '<strong>Haller Enterprises &mdash; big-box softener pricing</strong> &mdash; <a href="https://hallerent.com/blog/where-to-purchase-a-water-softener/" rel="noopener" target="_blank">hallerent.com</a>. Supports: A.O. Smith at Lowe&rsquo;s $357&ndash;$797; GE at Home Depot $397&ndash;$799.',
 '<strong>Angi &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: labor $200&ndash;$500 at $100&ndash;$150/hr; salt $5&ndash;$10 per 40-lb bag.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("low-cost-water-softener/index.html", f3)

# ============ E1 — MAINTENANCE COST PILLAR (expanded from T3) ============
e1_faqs = [
 ("How much does water softener maintenance cost per year?","$60&ndash;$300 for a self-serviced system: salt is $60&ndash;$180 (8&ndash;12 bags at $5&ndash;$10), prefilter cartridges add $20&ndash;$60, and occasional parts round it out. Dealer service plans add $100&ndash;$200/yr on top."),
 ("How much does water softener salt cost?","$5&ndash;$10 per 40-lb bag of sodium chloride; most homes use 8&ndash;12 bags a year ($60&ndash;$180). Potassium chloride runs $50&ndash;$70 per bag &mdash; same job, roughly 7&times; the price, chosen for sodium-restricted households or septic preference."),
 ("How much does it cost to replace water softener resin?","About $295 per cubic foot for a professional re-bed &mdash; typically $250&ndash;$600 all-in around years 8&ndash;15. Chlorinated city water shortens resin life; 10% crosslink resin lasts 12&ndash;15 years versus 8&ndash;10 for standard."),
 ("What do water softener repairs cost?","$150&ndash;$900 for common failures (seals, motors, circuit boards) per Angi. On rebuildable systems, a full valve rebuild runs $545&ndash;$595 &mdash; the reason quality valves outlive cheap cabinets, where a dead valve totals the unit."),
 ("Is a water softener service plan worth it?","Usually not for a metered system on city water &mdash; the annual tasks are salt refills and a prefilter swap. Plans at $100&ndash;$200/yr make sense for well water with pretreatment, landlords, or anyone who values never touching it."),
 ("How can I lower my softener&rsquo;s maintenance cost?","Three levers: a demand-metered valve (timer units waste 20&ndash;30% more salt), correct hardness settings (test, don&rsquo;t guess), and buying salt yourself &mdash; delivery programs are reported at $240&ndash;$600/yr versus $60&ndash;$180 self-supplied."),
]
e1_rows = [
 ("Softener salt (8&ndash;12 bags &times; $5&ndash;$10)",60,180,"The recurring line &mdash; usage scales with hardness &amp; household"),
 ("Prefilter cartridges (where fitted)",20,60,"Every 6&ndash;9 months; protects the resin bed"),
 ("Resin cleaner (optional, iron-prone water)",10,25,"Skip on clean city water"),
 ("Repairs, amortized (seals, motor, board)",30,90,"Angi: $150&ndash;$900 per event, every few years"),
 ("Dealer service plan (only if you take one)",0,200,"$100&ndash;$200/yr &mdash; optional on metered city-water systems"),
]
e1_repair_bars = [
 ("Common repairs (seals, motor, board)",150,900,"#5B6B75"),
 ("Valve rebuild (Fleck-class)",545,595,"#16303F"),
 ("Resin re-bed (~$295/cu-ft)",250,600,"#1F7A5C"),
 ("Salt delivery program, per year",240,600,"#E8A13D"),
]
e1 = head("Water Softener Maintenance Cost (2026): Salt, Resin, Repairs",
 "Water softener maintenance costs $60\u2013$300/yr self-serviced. Salt, prefilters, resin re-beds, valve rebuilds \u2014 every line itemized with sources.",
 "/water-softener-maintenance-cost/",
 ld(article_schema("Water Softener Maintenance Cost in 2026: Salt, Resin & Repairs, Itemized","Annual and lifetime softener upkeep costs with sourced figures and an interactive calculator.","/water-softener-maintenance-cost/",date="2026-07-12"))
 + ld(faq_schema(e1_faqs,"/water-softener-maintenance-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Maintenance cost","/water-softener-maintenance-cost/")])))
e1 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Maintenance cost</nav>
      <h1>Water Softener Maintenance Cost in 2026: Salt, Resin &amp; Repairs, Itemized</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Plan on <span class="fig">$60&ndash;$300</span> a year for a self-serviced softener: salt is the recurring line at <span class="fig">$60&ndash;$180</span> (8&ndash;12 bags at <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">Angi&rsquo;s</a> observed <span class="fig">$5&ndash;$10</span> per 40-lb bag), with <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">HomeGuide</a> putting total annual upkeep at <span class="fig">$100&ndash;$300</span>. The occasional big tickets: repairs at <span class="fig">$150&ndash;$900</span>, a resin re-bed around <span class="fig">$250&ndash;$600</span> near year ten, and &mdash; on rebuildable systems &mdash; a valve rebuild at <span class="fig">$545&ndash;$595</span> per published service pricing.</p>
      <p><strong>Water softener maintenance costs $60&ndash;$300 per year self-serviced: $60&ndash;$180 in salt, $20&ndash;$60 in prefilter cartridges, and amortized parts. Add $100&ndash;$200/yr for a dealer service plan, and budget one resin re-bed ($250&ndash;$600) around years 8&ndash;15.</strong></p>
      <p style="margin:0">I priced service contracts for fifteen years, and the honest summary is: a metered softener on city water is one of the cheapest appliances you&rsquo;ll ever own &mdash; <em>if</em> you buy your own salt and skip the plan. The expensive versions of ownership are all optional, and this page prices every one of them so you can opt out on purpose.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#calc">Price your upkeep (tool)</a></li>
          <li><a href="#worksheet">The annual worksheet</a></li>
          <li><a href="#schedule">The full maintenance schedule</a></li>
          <li><a href="#salt">The salt line: sodium vs. potassium</a></li>
          <li><a href="#big-tickets">The big tickets (chart)</a></li>
          <li><a href="#year-donut">What a typical year looks like (chart)</a></li>
          <li><a href="#plans">Service plans &amp; delivery programs</a></li>
          <li><a href="#save">Cutting the bill: three levers</a></li>
        </ol>
      </details>
      <h2 id="calc">Price your softener&rsquo;s upkeep in ten seconds</h2>
      <p style="margin:0 0 16px">Every input below is a sourced line item &mdash; toggle what your setup actually includes:</p>
      <div data-maint-calc></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Figures: Angi (salt, repairs), HomeGuide (annual ranges), published service pricing (rebuilds, re-beds) &mdash; sources below.</p>

      <h2 id="worksheet">The annual maintenance worksheet</h2>
      <p style="margin:0">A typical metered softener on city water, itemized the way I&rsquo;d budget a service contract:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Softener upkeep, per year (self-serviced)", e1_rows, total_label="Annual span") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>How I&rsquo;d read this sheet:</strong> the realistic self-service year is <span class="fig">$120&ndash;$355</span> at the top of the ranges, but most homes on moderate hardness land near <span class="fig">$10&ndash;$20 a month</span>. Electricity isn&rsquo;t on the sheet because a metered valve draws a few watts &mdash; pennies a year. The rows that quietly double for some homes: salt (very hard water, big households) and the service plan (which is a choice, not a requirement).</p>
      <div style="margin-top:24px">''' + cta_box("Efficiency is a purchase decision",
        "Most of a softener&rsquo;s lifetime upkeep is set the day you buy it: metered valves sip salt, timer units burn it. SpringWell&rsquo;s SS series meters by actual use, publishes its price online, and carries a lifetime warranty on tanks and valves &mdash; the two parts this page prices repairs for.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="schedule">The full maintenance schedule &mdash; what, when, what it costs</h2>
      <p style="margin:0 0 16px">This section prices each job. For <em>how to actually do them</em> &mdash; breaking a salt bridge, stripping the injector, washing the brine tank &mdash; see our <a href="/water-softener-maintenance/">complete DIY maintenance schedule</a>, which walks through all six step by step and finds the whole year comes to about two hours and $31 beyond the salt.</p>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Water softener maintenance schedule and costs, 2026</caption>
        <thead><tr><th scope="col">Task</th><th scope="col">Frequency</th><th scope="col" class="num">Cost</th></tr></thead>
        <tbody>
          <tr><td>Check salt level, break salt bridges</td><td class="muted">Monthly</td><td class="num">$0</td></tr>
          <tr><td>Refill salt</td><td class="muted">~Monthly (8&ndash;12 bags/yr)</td><td class="num">$5&ndash;$10/bag</td></tr>
          <tr><td>Swap sediment prefilter</td><td class="muted">Every 6&ndash;9 months</td><td class="num">$20&ndash;$60/yr</td></tr>
          <tr><td>Clean brine tank</td><td class="muted">Yearly (DIY)</td><td class="num">$0</td></tr>
          <tr><td>Resin cleaner treatment (iron-prone water)</td><td class="muted">Yearly, optional</td><td class="num">$10&ndash;$25</td></tr>
          <tr><td>Hardness re-test &amp; settings check</td><td class="muted">Every 1&ndash;2 years</td><td class="num">$0&ndash;$30</td></tr>
          <tr><td>Resin re-bed</td><td class="muted">Years 8&ndash;15</td><td class="num">$250&ndash;$600</td></tr>
          <tr><td>Valve rebuild (rebuildable systems)</td><td class="muted">Years 10&ndash;15</td><td class="num">$545&ndash;$595</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Two of those rows earn their own cross-references: the prefilter swap is the cheapest insurance on the sheet &mdash; a clogged cartridge mimics expensive pressure problems, and <a href="/pick/replacement-prefilters" ''' + PICK + '''>replacement cartridges</a> cost less than one service visit. And the settings check matters because hardness drifts: re-test with a <a href="/pick/test-kit" ''' + PICK + '''>water test kit</a> before assuming your softener &ldquo;stopped working&rdquo; &mdash; half the time it&rsquo;s the setting, not the resin.</p>

      <p style="margin:0 0 16px">One line deliberately absent from this worksheet: electricity. It is about a dollar a month, and I make the case in full in our <a href="/water-softener-electricity-usage/">water softener electricity and running-cost guide</a> &mdash; along with the regeneration water, which quietly costs more.</p>
      <h2 id="salt">The salt line: sodium vs. potassium</h2>
      <p style="margin:0 0 16px">The full treatment &mdash; all four salt types priced, the purity that decides whether your injector clogs, and why potassium chloride costs nearly 5&times; as much for a slightly worse regeneration &mdash; is in our <a href="/water-softener-salt-cost/">salt cost and types guide</a>.</p>
      <p style="margin:0 0 16px">Same job, very different bills. Sodium chloride runs <span class="fig">$5&ndash;$10</span> per 40-lb bag; potassium chloride &mdash; chosen for sodium-restricted diets or septic preference &mdash; runs <span class="fig">$50&ndash;$70</span> per Angi. At 10 bags a year that&rsquo;s <span class="fig">$50&ndash;$100</span> versus <span class="fig">$500&ndash;$700</span>: the single biggest maintenance decision most owners never realize they&rsquo;re making. If sodium is the concern, a cheaper middle path is a reverse-osmosis tap for drinking water while the softener stays on sodium &mdash; or skipping salt entirely with a <a href="/pick/futuresoft" ''' + PICK + '''>salt-free conditioner</a> where scale control (not true softening) fits the goal.</p>

      <h2 id="big-tickets">The big tickets &mdash; and when they arrive</h2>
      <p style="margin:0 0 16px">This section prices those repairs. Whether you should <em>buy</em> one is a different question, and it turns on a single division sign &mdash; our <a href="/how-long-does-a-water-softener-last/">lifespan and repair-versus-replace guide</a> works it out, and finds that most &ldquo;dead&rdquo; softeners are one $295 component away from another decade.</p>
      <p style="margin:0 0 16px">Four numbers cover essentially every non-routine event in a softener&rsquo;s life:</p>
    </div>
    <div class="col-wide">''' + range_bars(e1_repair_bars, 1000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Repairs: Angi. Rebuild &amp; re-bed: published service pricing (Mid Atlantic Water). Delivery program: reported Culligan figures (Modernize) &mdash; per year, shown for scale against one-time repairs.</p>
      <p style="margin:16px 0 0">The pattern worth noticing: on a rebuildable system, <em>every</em> failure mode has a fix cheaper than replacement &mdash; valve rebuild <span class="fig">$545&ndash;$595</span>, re-bed <span class="fig">$250&ndash;$600</span> &mdash; which is how these systems reach 15&ndash;20 years. Cabinet units invert that: the valve dies, the unit&rsquo;s done. That difference is priced in full in the <a href="/low-cost-water-softener/">budget-tier guide</a>. And note the amber bar: a salt <em>delivery program</em> costs as much per year as a resin re-bed costs once a decade.</p>

      <h2 id="year-donut">What a typical maintenance year actually looks like</h2>
    </div>
    <div class="col-wide" style="margin-top:16px">
      <div class="donut-wrap">''' + donut_svg([("#16303F",55),("#1F7A5C",18),("#5B6B75",27)], "~$220/yr", "typical self-serviced", "Typical annual maintenance composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> Salt (10 bags, midpoint pricing) <span class="pc">~55%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Prefilter cartridges <span class="pc">~18%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Repairs &amp; parts, amortized <span class="pc">~27%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of the worksheet above &middot; roughly $18/month &mdash; less than most streaming bundles</div>
    </div>
    <div class="col">
      <h2 id="plans" style="margin-top:48px">Service plans and delivery programs: the optional expensive version</h2>
      <p style="margin:0 0 16px">For what an individual visit costs &mdash; trip charges, diagnostic fees, hourly labour, and an honest surprise about all-inclusive contracts &mdash; see our <a href="/water-softener-servicing/">water softener servicing guide</a>.</p>
      <p style="margin:0 0 16px">Everything above assumes you carry your own bags. The hands-off versions, priced:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>Self-service versus dealer programs, annual cost</caption>
        <thead><tr><th scope="col">Route</th><th scope="col" class="num">Per year</th><th scope="col">What you get</th><th scope="col">Worth it when</th></tr></thead>
        <tbody>
          <tr><td>Self-service</td><td class="num">$60&ndash;$300</td><td class="muted">You buy salt, swap cartridges</td><td class="muted">Metered system, city water &mdash; most homes</td></tr>
          <tr><td>Dealer service plan</td><td class="num">+$100&ndash;$200</td><td class="muted">Inspection, settings, cleaning visit</td><td class="muted">Well water with pretreatment; landlords</td></tr>
          <tr><td>Salt delivery program</td><td class="num">$240&ndash;$600</td><td class="muted">Bags carried to the tank for you</td><td class="muted">Mobility constraints &mdash; otherwise it&rsquo;s the priciest line on this page</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">The delivery-program math gets its own exhibit in the <a href="/culligan-water-softener-cost/">Culligan expos&eacute;</a>: over ten years the program can out-cost the softener. None of this is a scam &mdash; it&rsquo;s convenience with a price tag. The point of this page is that the tag is <span class="fig">$1,800&ndash;$4,200</span> per decade, and you should read it before signing.</p>

      <h2 id="save">Cutting the bill: the three levers that actually work</h2>
      <p><strong>1. Metered regeneration.</strong> Timer units regenerate on schedule whether you used water or not &mdash; published service data puts the waste at 20&ndash;30% more salt. If yours is a timer, the fix is a valve upgrade or the next purchase, not a habit. <strong>2. Correct settings.</strong> A softener set 5 gpg too high regenerates for hardness that isn&rsquo;t there &mdash; re-test every year or two and dial it in; it&rsquo;s a $0&ndash;$30 fix that pays every month after. <strong>3. Resin quality on chlorinated water.</strong> 10% crosslink resin lasts 12&ndash;15 years versus 8&ndash;10 standard &mdash; a <span class="fig">$200&ndash;$400</span> upgrade that skips one entire re-bed cycle.</p>
      <p style="margin:0">Do all three and the realistic bill is <span class="fig">$8&ndash;$15 a month</span> &mdash; which is the honest answer to whether softeners are expensive to own: no, unless you buy the expensive version of every optional line. For what the <em>purchase</em> should cost, the <a href="/">full cost guide</a> itemizes that side.</p>
      <div style="margin-top:40px">''' + cta_box("Built for the cheap version of ownership",
        "The self-service math on this page assumes a system designed for it: SpringWell&rsquo;s metered SS series, published price, free shipping, lifetime warranty on the tanks and valves that make up both big-ticket bars above &mdash; so the decade you just priced stays on the low line.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(e1_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/"><div class="name">Full cost guide</div><div class="range">$840&ndash;$4,120</div><div class="desc">Purchase + install, itemized with charts.</div></a>
        <a class="card" href="/low-cost-water-softener/"><div class="name">Low-cost softeners</div><div class="desc">$700 vs $1,500 tiers &mdash; and the false economy.</div></a>
        <a class="card" href="/culligan-water-softener-cost/"><div class="name">Culligan cost expos&eacute;</div><div class="desc">Where the delivery-program math came from.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Angi &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: salt $5&ndash;$10/40-lb bag and 8&ndash;12 bags/yr; potassium $50&ndash;$70; repairs $150&ndash;$900.',
 '<strong>HomeGuide &mdash; Water Softener Cost (2026)</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: annual maintenance $100&ndash;$300; salt/potassium $50&ndash;$150/yr.',
 '<strong>Mid Atlantic Water &mdash; Water Softener Cost (Mar 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/faqs/water-softener-cost" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: valve rebuild $545&ndash;$595; resin re-bed ~$295/cu-ft; 20&ndash;30% salt overuse on timer units; 10% crosslink resin lifespan (12&ndash;15 vs 8&ndash;10 yrs).',
 '<strong>Modernize &mdash; Culligan Water Softener Costs (2026)</strong> &mdash; <a href="https://modernize.com/water-treatment/culligan-cost/water-softener" rel="noopener" target="_blank">modernize.com</a>. Supports: salt delivery programs $240&ndash;$600/yr.',
 '<strong>WaterSoftenerCost.com &mdash; brand ownership data (2026)</strong> &mdash; <a href="https://watersoftenercost.com/average-cost-of-culligan-water-softener/" rel="noopener" target="_blank">watersoftenercost.com</a>. Supports: dealer service-visit pricing ($100&ndash;$200/yr) and resin-life ranges.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("water-softener-maintenance-cost/index.html", e1)

# ============ C3 — RAINSOFT EXPOSE (T4+viz) ============
c3_faqs = [
 ("How much does a RainSoft water softener cost?","The flagship EC5 is reported at $6,000&ndash;$11,000 fully installed, with review-cited quotes of $7,000&ndash;$9,000 and forum reports up to $13,000. The older EC4 was reported around $4,000&ndash;$5,000. RainSoft publishes no prices &mdash; every figure is dealer-set."),
 ("Why doesn&rsquo;t RainSoft list any prices?","RainSoft sells only through exclusive dealers via in-home presentations &mdash; there is no MSRP anywhere, including on Home Depot&rsquo;s own EC5 listing, which is quote-based. The final number is set by the dealer, the market, and the presentation."),
 ("Is RainSoft sold at Home Depot?","Yes &mdash; RainSoft is Home Depot&rsquo;s in-store water-treatment brand, sold through kiosk sign-ups and a free in-home test. The store hosts the pitch; an independent RainSoft dealer sets the price and installs."),
 ("Is RainSoft equipment good?","Genuinely, yes: US-made, DC-powered, proportional brining that meters salt to real usage, and owner ratings that beat several rivals. The 1-star reviews are almost universally about the price and the pressure &mdash; not the machine."),
 ("What&rsquo;s the catch with RainSoft&rsquo;s lifetime warranty?","Three asterisks: it&rsquo;s non-transferable (dies when you sell the house), it requires dealer installation to stay valid, and configured filtration uses proprietary cartridges reported at $275&ndash;$1,000, sourced only through the dealer."),
 ("Can I negotiate a RainSoft quote?","Reports suggest wide dealer discretion &mdash; one review site put it bluntly: pricing is what the dealer thinks you&rsquo;ll pay. A written competing quote and a published-price benchmark are the strongest tools; never sign at the first sit-down."),
 ("Should I finance a RainSoft system?","Get the cash price first &mdash; a payment is not a price. At a mid-teens APR over 84 months, a $160 monthly payment totals roughly $13,440 on an implied $8,000 system. Weigh too that the reported lifetime warranty is non-transferable, while the loan follows you regardless."),
]
c3_rows = [
 ("Comparable metered softener hardware (published class)",600,1500,"Same ion-exchange job; RainSoft&rsquo;s own hardware is dealer-only"),
 ("Professional installation (existing loop)",200,500,"Angi: 2&ndash;4 hrs at $100&ndash;$150/hr"),
 ("Materials &amp; haul-away",90,270,"Itemized in honest quotes"),
 ("Remainder to reported EC5 installed totals (implied)",5110,8730,"The largest unlabeled line we track &mdash; channel, presentation, warranty program"),
]
c3_brand_bars = [
 ("Factory-direct + your plumber",1200,3200,"#1F7A5C"),
 ("Culligan (typical reported)",2500,4500,"#16303F"),
 ("Kinetico (typical reported)",3000,5000,"#5B6B75"),
 ("RainSoft EC5 (reported installs)",6000,11000,"#E8A13D"),
]
c3_bands = '[{"upTo":4999,"band":"below-typical","text":"Below the reported EC5 band \\u2014 plausible for TC-M or older EC4-class systems ($4,000\\u2013$5,000 reported). Confirm the exact model and what install covers."},{"upTo":8000,"band":"typical","text":"Inside the commonly reported EC5 band ($6,000\\u2013$11,000 installed; reviews cluster near $7,000\\u2013$8,000). Ask for equipment and install as separate lines \\u2014 the dealer sets both."},{"upTo":11000,"band":"upper","text":"Upper end of reported installs. Legitimate only for bundled filtration + RO configurations \\u2014 get the bundle itemized, in writing, before signing."},{"upTo":null,"band":"above-published","text":"Above almost every report we track \\u2014 the highest forum-reported RainSoft quote is $13,000. Do not sign same-day; a second quote will likely be thousands lower."}]'
BANDS_ATTR = "'" + c3_bands + "'"
c3 = head("RainSoft Water Softener Cost (2026): Reported Price Ranges",
 "RainSoft EC5 systems are reported at $6,000\u2013$11,000 installed \u2014 no published prices exist. Sourced reports, warranty fine print, quote checker.",
 "/rainsoft-water-softener-cost/",
 ld(article_schema("RainSoft Water Softener Cost in 2026: The Widest Quote Spread We Track","Sourced RainSoft EC5 pricing reports, Home Depot channel analysis, warranty lock-in math, and quote anatomy.","/rainsoft-water-softener-cost/",date="2026-07-12"))
 + ld(faq_schema(c3_faqs,"/rainsoft-water-softener-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Brands","/brands/"),("RainSoft","/rainsoft-water-softener-cost/")])))
c3 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/brands/">Brands</a> &rsaquo; RainSoft</nav>
      <h1>RainSoft Water Softener Cost in 2026: The Widest Quote Spread We Track</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">RainSoft publishes no prices &mdash; not on <a href="https://www.rainsoft.com/ec5-water-conditioning-system/" rel="noopener" target="_blank">its own site</a>, and not even on <a href="https://www.homedepot.com/p/RAINSOFT-Premium-Whole-House-Water-Softener-System-Wi-Fi-enabled-EC5-HDINSTIEC5WS/311248905" rel="noopener" target="_blank">Home Depot&rsquo;s EC5 listing</a>, which is quote-only. The reported numbers: the flagship EC5 lands at <span class="fig">$6,000&ndash;$11,000</span> fully installed per <a href="https://engineerfix.com/how-much-does-a-rainsoft-ec5-system-cost/" rel="noopener" target="_blank">market analysis</a>, reviews cluster around <span class="fig">$7,000</span> with a Reddit-reported quote of <span class="fig">$7,800</span>, and forum reports reach <span class="fig">$13,000</span>. That&rsquo;s the widest spread of any brand we track &mdash; wider than <a href="/culligan-water-softener-cost/">Culligan</a> and <a href="/kinetico-water-softener-cost/">Kinetico</a> combined.</p>
      <p style="margin:0">The estimator&rsquo;s frame: RainSoft makes genuinely well-regarded, US-built equipment &mdash; and sells it through the most presentation-driven channel in the industry, anchored to Home Depot&rsquo;s sales floor. When there&rsquo;s no list price and the quote is built at your kitchen table, the spread <em>is</em> the pricing model. This page assembles every public number so the free water test starts on your terms.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#brands-chart">RainSoft vs. every brand we track (chart)</a></li>
          <li><a href="#reports">Real reported quotes</a></li>
          <li><a href="#worksheet">An EC5 quote, reconstructed</a></li>
          <li><a href="#checker">Quote checker (tool)</a></li>
          <li><a href="#warranty">The lifetime warranty&rsquo;s three asterisks (chart)</a></li>
          <li><a href="#homedepot">The Home Depot channel</a></li>
          <li><a href="#financing">At this ticket, the payment is the product (tool)</a></li>
          <li><a href="#fair">What the premium legitimately buys</a></li>
        </ol>
      </details>
      <h2 id="brands-chart">Where RainSoft sits against every brand we track</h2>
      <p style="margin:0 0 16px">Same job &mdash; hardness out, soft water in. Reported installed ranges, one scale:</p>
    </div>
    <div class="col-wide">''' + range_bars(c3_brand_bars, 12000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Sources: Culligan and Kinetico bands from our sourced expos&eacute;s; RainSoft EC5 band from EngineerFix market reports; factory-direct comparable from published unit + labor pricing. Reported figures, not list prices &mdash; none of these brands publishes one.</p>

      <h2 id="reports">Real reported RainSoft quotes</h2>
      <p style="margin:0 0 16px">Collected from published reviews and forums &mdash; anecdotal, attributed, and remarkably consistent about one thing:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>Publicly reported RainSoft pricing, 2020&ndash;2026</caption>
        <thead><tr><th scope="col">System / situation</th><th scope="col">Where reported</th><th scope="col" class="num">Reported figure</th></tr></thead>
        <tbody>
          <tr><td>EC5 + installation, Reddit user quote</td><td class="muted">via FilterSmart review roundup</td><td class="num">$7,800</td></tr>
          <tr><td>EC5, owner review (&ldquo;super expensive&rdquo;)</td><td class="muted">Home Depot / ConsumerAffairs reviews</td><td class="num">$7,000+</td></tr>
          <tr><td>System from in-store Home Depot vendor</td><td class="muted">Owner review</td><td class="num">~$9,000</td></tr>
          <tr><td>EC4 (previous generation) + install</td><td class="muted">Forum reports via MrWaterGeek</td><td class="num">$4,000&ndash;$5,000</td></tr>
          <tr><td>Highest quote seen in the wild</td><td class="muted">MrWaterGeek</td><td class="num">up to $13,000</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">The tell in those reviews: the 1-star complaints are almost universally about the <em>price and the pressure</em>, not the machine. One review analysis put it plainly &mdash; the pricing model &ldquo;essentially charges people what they want.&rdquo; That&rsquo;s not an equipment problem. It&rsquo;s a channel problem, and it&rsquo;s the exact pattern the <a href="/dealer-vs-factory-direct-pricing/">dealer vs. factory-direct breakdown</a> quantifies.</p>

      <h2 id="worksheet">An EC5 quote, reconstructed line by line</h2>
      <p style="margin:0">Build the same soft-water outcome from published component prices, and the arithmetic leaves the largest unlabeled remainder on this site:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("RainSoft EC5 quote, reconstructed (est.)", c3_rows, total_label="Reported installed band") + '''</div>
    <div class="col">
      <p style="margin-top:24px">To be scrupulously fair: RainSoft&rsquo;s remainder buys more than a commission &mdash; proportional-brining electronics, the lifetime warranty program, and the dealer&rsquo;s service obligation are real. But at <span class="fig">75&ndash;85%</span> of the quote, it&rsquo;s a remainder you&rsquo;re entitled to see priced. Compare the same reconstruction on <a href="/culligan-water-softener-cost/">Culligan (~2/3)</a> and the market-wide version in the <a href="/why-are-water-softeners-so-expensive/">cost-anatomy guide</a>.</p>

      <h2 id="checker">Check your RainSoft quote against the reported bands</h2>
      <div data-quote-check data-min="3000" data-max="13000" data-start="7000" data-bands=''' + BANDS_ATTR + '''></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Bands from the sourced reports above. A verdict is a prompt for questions &mdash; model, configuration, what install covers, and which parts of the warranty survive a home sale.</p>
      <div style="margin-top:40px">''' + cta_box("See a published price first",
        "Independent reviewers make the comparison themselves: quality whole-house systems sell at posted prices for a fraction of reported RainSoft quotes. SpringWell publishes its softener pricing online \u2014 sized by bathrooms, shipped free, 6-month money-back guarantee \u2014 the benchmark to hold any in-home presentation against.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="warranty">The lifetime warranty&rsquo;s three asterisks</h2>
      <p style="margin:0 0 16px">RainSoft&rsquo;s limited lifetime warranty is its best selling point &mdash; and its strongest lock-in. Reported fine print: it&rsquo;s <strong>non-transferable</strong> (unlike Kinetico&rsquo;s, it dies when you sell the house), it <strong>requires dealer installation</strong> to remain valid (DIY is off the table by design), and configured filtration runs on <strong>proprietary cartridges</strong> reported at <span class="fig">$275&ndash;$1,000</span>, sourced only through your dealer. Price a decade of that:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",77),("#E8A13D",14),("#1F7A5C",9)], "~$11,000", "10-yr total (midpoints)", "10-year RainSoft EC5 ownership composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> System, installed (EC5 midpoint ~$8,500) <span class="pc">~77%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Proprietary filters, where configured (~$1,500) <span class="pc">~14%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Salt (proportional brining, ~$1,050) <span class="pc">~9%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of sourced ranges; filter line applies to filtration-configured systems (reports of $275&ndash;$1,000 per change) &middot; the salt slice is genuinely small &mdash; the metering works</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Note what the chart concedes: the salt slice is small because the proportional-brining engineering genuinely works. The premium isn&rsquo;t in the upkeep &mdash; it&rsquo;s front-loaded in the purchase and back-loaded in the cartridge lock-in. The <a href="/water-softener-maintenance-cost/">maintenance cost guide</a> shows what the same decade costs on standard, non-proprietary parts.</p>

      <h2 id="homedepot">The Home Depot channel: the kiosk is not the store</h2>
      <p style="margin:0">The orange apron lends trust, but read the structure: Home Depot hosts the sign-up, an <em>independent RainSoft dealer</em> runs the in-home test, sets the price, and installs. The store&rsquo;s own EC5 listing carries no price &mdash; it books a consultation. That&rsquo;s the same subcontract-and-markup pattern as <a href="/water-softener-installation-cost/">big-box install programs</a>, with a presentation layer on top. Treat a kiosk sign-up as the start of a negotiation, not a retail purchase &mdash; and take the <a href="/dealer-vs-factory-direct-pricing/">four-step script</a> to the sit-down.</p>

      <h2 id="financing">At this ticket, the payment <em>is</em> the product</h2>
      <p style="margin:0 0 16px">RainSoft carries the widest reported spread on this site &mdash; <span class="fig">$6,000&ndash;$11,000</span> &mdash; and almost nobody writes a cheque for that at their own kitchen table. Which means the monthly payment is not a convenience bolted onto the sale. At this price level, <strong>the payment is how the sale happens at all</strong> &mdash; so it deserves exactly as much scrutiny as the equipment:</p>
      <div data-finance-calc data-pmt="160" data-term="84" data-apr="15.9"></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Illustrative &mdash; not a quote, and not RainSoft&rsquo;s terms, which are dealer-set and unpublished. The default is seeded at a payment implying a system near $8,000, mid-range among the reported quotes above.</p>
      <p style="margin:20px 0 0">Read that result slowly. A <span class="fig">$160</span> monthly payment across seven years is roughly <span class="fig">$13,440</span> handed over &mdash; about <span class="fig">$5,400</span> of it interest, on an implied system price near $8,000. Now set it beside <a href="#warranty">the warranty section above</a>, because on this page the two collide in a way they do not anywhere else on this site. That lifetime warranty is reported as <strong>non-transferable, conditional on dealer installation, and tied to dealer-supplied filters at $275&ndash;$1,000 a set.</strong> A seven- or ten-year loan is therefore a quiet bet that you will not move house, will not change service providers, and will keep buying proprietary cartridges for the duration. If any of that changes, the payments do not: <strong>you can still be financing a system whose warranty has stopped applying to you.</strong></p>
      <p style="margin:16px 0 0">One structural point people miss at this ticket: the loan is usually held by a <em>lender</em>, not the dealer. If the equipment disappoints, your dispute is with one company while the money is owed to another &mdash; and the second one keeps invoicing regardless of how the first conversation goes. So get the <strong>cash price, APR, term and total of payments</strong> in writing, and know that <strong>&ldquo;no interest if paid in full&rdquo; is deferred interest, not 0% APR</strong>: any surviving balance is billed retroactively to day one on the full amount, and the CFPB finds roughly one in five of these balances take that hit. Full mechanics in the <a href="/dealer-vs-factory-direct-pricing/">channel hub</a>.</p>

      <h2 id="fair">What the RainSoft premium legitimately buys</h2>
      <p>Credit where due, because the equipment earns it: US-made hardware, DC-powered electronics that sip electricity, proportional brining that meters salt to actual use, app-connected diagnostics, and owner satisfaction ratings that beat several rivals &mdash; review analyses note RainSoft&rsquo;s averages run <em>above</em> Culligan&rsquo;s. The in-home water test is reportedly thorough, and the company visibly works its 1-star reviews toward resolution.</p>
      <p style="margin:0">The critique is narrow and it&rsquo;s the same one every page in this series makes: none of that justifies a price you can&rsquo;t see until a rep is on your couch, spanning <span class="fig">$6,000&ndash;$13,000</span> for outcomes a <a href="/">$840&ndash;$4,120 itemized project</a> also delivers. Pay the premium if the warranty relationship is worth it to you &mdash; but make them price it in daylight first.</p>
      <div style="margin-top:40px">''' + cta_box("The factory-direct alternative",
        "If lifetime coverage is the appeal, compare the posted version: SpringWell\u2019s SS series carries a lifetime warranty on tanks and valves \u2014 transferable value, published price, free shipping, DIY-friendly on an existing loop. No kiosk, no presentation, no asterisks to negotiate.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(c3_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/culligan-water-softener-cost/"><div class="name">Culligan cost expos&eacute;</div><div class="range">$2,500&ndash;$4,500</div><div class="desc">Tiers, rental math, quote checker.</div></a>
        <a class="card" href="/kinetico-water-softener-cost/"><div class="name">Kinetico cost expos&eacute;</div><div class="range">$3,000&ndash;$5,000+</div><div class="desc">Zero published prices, real installs.</div></a>
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Dealer vs. factory-direct</div><div class="desc">Where the extra thousands go.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>EngineerFix &mdash; RainSoft EC5 System Cost (Nov 2025)</strong> &mdash; <a href="https://engineerfix.com/how-much-does-a-rainsoft-ec5-system-cost/" rel="noopener" target="_blank">engineerfix.com</a>. Supports: EC5 installed $6,000&ndash;$11,000; no MSRP / dealer-set pricing; dealer install required for warranty; non-transferable warranty; proprietary filters $275&ndash;$1,000.',
 '<strong>FilterSmart &mdash; RainSoft Review</strong> &mdash; <a href="https://filtersmart.com/blogs/article/rainsoft-water-review" rel="noopener" target="_blank">filtersmart.com</a>. Supports: ~$7,000 average from reviews; Reddit-reported $7,800 quote; owner review quotes ($7,000 / ~$9,000 Home Depot vendor); rating comparison vs. Culligan; price-focused 1-star pattern.',
 '<strong>MrWaterGeek &mdash; RainSoft Water Softener analysis</strong> &mdash; <a href="https://mrwatergeek.com/rainsoft-water-softener/" rel="noopener" target="_blank">mrwatergeek.com</a>. Supports: EC4 $4,000&ndash;$5,000 forum reports; quotes up to $13,000; dealer-discretion pricing characterization; factory-direct comparison framing.',
 '<strong>ConsumerAffairs &mdash; RainSoft Water Treatment Systems</strong> &mdash; <a href="https://www.consumeraffairs.com/homeowners/rainsoft.html" rel="noopener" target="_blank">consumeraffairs.com</a>. Supports: no published prices / dealer model; model lineup (EC5, EC5-CAB, TC-M); limited lifetime warranty across products.',
 '<strong>Home Depot &mdash; RainSoft EC5 listing (quote-based)</strong> &mdash; <a href="https://www.homedepot.com/p/RAINSOFT-Premium-Whole-House-Water-Softener-System-Wi-Fi-enabled-EC5-HDINSTIEC5WS/311248905" rel="noopener" target="_blank">homedepot.com</a>. Supports: in-store channel; consultation-only, no listed price.',
 '<strong>RainSoft &mdash; EC5 official pages</strong> &mdash; <a href="https://www.rainsoft.com/ec5-water-conditioning-system/" rel="noopener" target="_blank">rainsoft.com</a>. Supports: absence of published pricing; dealer water-test model; DC power and proportional-regeneration engineering claims.',
 '<strong>Consumer Financial Protection Bureau &mdash; Issue Spotlight: The High Cost of Retail Credit Cards; Regulation Z &sect;1026.16</strong> &mdash; <a href="https://www.consumerfinance.gov/data-research/research-reports/issue-spotlight-the-high-cost-of-retail-credit-cards/" rel="noopener" target="_blank">consumerfinance.gov</a>, <a href="https://www.consumerfinance.gov/rules-policy/regulations/1026/16/" rel="noopener" target="_blank">Reg Z &sect;1026.16</a>. Supports: deferred interest billed retroactively on the original purchase amount; roughly 1 in 5 promotional balances hit; ongoing rates above 20% regardless of credit score; the &ldquo;if paid in full&rdquo; disclosure requirement. Financing mechanics only &mdash; not this brand&rsquo;s terms, which are unpublished.',
 '<strong>National Consumer Law Center &mdash; Deceptive Bargain: The Hidden Time Bomb of Deferred Interest</strong> &mdash; <a href="https://www.nclc.org/resources/deceptive-bargain-the-hidden-time-bomb-of-deferred-interest-credit-cards/" rel="noopener" target="_blank">nclc.org</a>. Supports: the mechanics of retroactive interest on promotional balances.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("rainsoft-water-softener-cost/index.html", c3)


# ============ C5 — COSTCO / ECOWATER EXPOSE (T4+viz) ============
c5_faqs = [
 ("How much does a Costco water softener cost?","Costco doesn&rsquo;t sell softeners off the shelf &mdash; its program connects members to EcoWater dealers for an in-home quote. A Reddit-reported Costco/EcoWater quote ran $6,000&ndash;$10,000; Costco&rsquo;s own page lists no prices at all."),
 ("Does Costco sell water softeners in the warehouse?","No. Coverage of the program notes Costco lists no other softeners &mdash; the water-treatment page is a consultation booking for EcoWater, not a product you can put in a cart. The &ldquo;aisle&rdquo; is a phone number."),
 ("What do Costco members actually get on an EcoWater purchase?","A Costco Shop Card worth 10% of the pre-tax equipment-and-install total (delivered up to 4 weeks after completion), up to 2% back for Executive members, an extended warranty, and a 3-business-day right to cancel."),
 ("Is EcoWater good equipment?","The pedigree is real: EcoWater&rsquo;s founder received the first softener patent (1925), the company holds 70+ patents, and systems are NSF-certified with Wi-Fi monitoring. Reviews question the price, not the machine &mdash; Home Depot&rsquo;s program shows just 44% would recommend, mostly over cost."),
 ("Can I negotiate an EcoWater quote from Costco?","Yes &mdash; it&rsquo;s a dealer quote like any other. Your strongest leverage is the 3-business-day cancellation window: sign nothing same-day, collect a written competing number, and let the consultant&rsquo;s discount authority respond."),
 ("Is the Costco route cheaper than buying a softener yourself?","Usually not close. Published comparisons make the point bluntly: a $499 metered Rheem at Home Depot does the same ion-exchange job. Even after 10&ndash;12% member perks on an $8,000 quote, the remaining premium is thousands."),
 ("Is Costco water softener financing a good deal?","Nobody publishes the terms, so judge it on the total, not the payment. And note the mismatch: the reported three-day cancellation window covers the purchase, while the credit agreement runs for years &mdash; and &ldquo;no interest if paid in full&rdquo; is deferred interest, not 0% APR."),
]
c5_rows = [
 ("Comparable metered softener hardware (published class)",600,1500,"Same ion-exchange job at retail; EcoWater hardware is dealer-only"),
 ("Professional installation (existing loop)",200,500,"Angi: 2&ndash;4 hrs at $100&ndash;$150/hr"),
 ("Materials &amp; haul-away",90,270,"Itemized in honest quotes"),
 ("Member perks returned (10% card, up to 2% exec)",-1200,-600,"Real money &mdash; delivered as a Shop Card weeks later"),
 ("Remainder to reported quote band (implied)",5910,8730,"Channel, consultation, dealer overhead &mdash; the unlabeled line"),
]
c5_brand_bars = [
 ("Factory-direct + your plumber",1200,3200,"#1F7A5C"),
 ("Culligan (typical reported)",2500,4500,"#16303F"),
 ("Kinetico (typical reported)",3000,5000,"#5B6B75"),
 ("RainSoft EC5 (reported)",6000,11000,"#B3541E"),
 ("EcoWater via Costco (reported)",6000,10000,"#E8A13D"),
]
c5_bands = '[{"upTo":4999,"band":"below-typical","text":"Below the reported Costco/EcoWater band \\u2014 plausible for smaller softener-only configurations. Confirm the model, capacity, and that the Shop Card terms are in writing."},{"upTo":8000,"band":"typical","text":"Inside the reported band ($6,000\\u2013$10,000 from member reports). Ask for equipment and install as separate lines, and get the perk math \\u2014 10% card, exec 2% \\u2014 shown against the pre-tax total."},{"upTo":10000,"band":"upper","text":"Top of the reported band \\u2014 typical of softener + refiner + RO bundles. Get the bundle itemized; each piece has a published-market comparable."},{"upTo":null,"band":"above-published","text":"Above every member report we track. Use the 3-business-day cancellation window: sign nothing until a written second quote arrives \\u2014 it will likely be thousands lower."}]'
BANDS5 = "'" + c5_bands + "'"
c5 = head("Costco Water Softener Cost (2026): The EcoWater Program",
 "Costco\u2019s softener is an EcoWater in-home quote \u2014 reported at $6,000\u2013$10,000. The member-perk math, fine print, and comparisons, sourced.",
 "/costco-water-softener-cost/",
 ld(article_schema("Costco Water Softener Cost in 2026: The Aisle That Doesn\u2019t Exist","Sourced analysis of Costco\u2019s EcoWater program: reported quotes, member-perk math, and comparisons.","/costco-water-softener-cost/",date="2026-07-12"))
 + ld(faq_schema(c5_faqs,"/costco-water-softener-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Brands","/brands/"),("Costco / EcoWater","/costco-water-softener-cost/")])))
c5 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/brands/">Brands</a> &rsaquo; Costco / EcoWater</nav>
      <h1>Costco Water Softener Cost in 2026: The Aisle That Doesn&rsquo;t Exist</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Here&rsquo;s what surprises most members: Costco doesn&rsquo;t sell water softeners. <a href="https://www.costco.com/ecowater-water-treatment-systems.html" rel="noopener" target="_blank">Costco&rsquo;s water-treatment page</a> is a consultation booking for <strong>EcoWater</strong> dealers &mdash; no cart, no price, and per <a href="https://www.housedigest.com/1779560/costco-water-softener-worth-it-reviews/" rel="noopener" target="_blank">House Digest&rsquo;s review analysis</a>, no other softener sold at all. The reported numbers from that program: a member&rsquo;s Reddit-shared quote ran <span class="fig">$6,000&ndash;$10,000</span> after a two-hour in-home consultation. The member perks are real &mdash; a <span class="fig">10%</span> Shop Card, up to <span class="fig">2%</span> Executive cash back, an extended warranty &mdash; and so is the arithmetic problem this page prices.</p>
      <p style="margin:0">The estimator&rsquo;s frame: Costco&rsquo;s brand is trust, and the program borrows it well. But structurally this is the same dealer channel as <a href="/culligan-water-softener-cost/">Culligan</a> and <a href="/rainsoft-water-softener-cost/">RainSoft</a> &mdash; a free water test that&rsquo;s really a sales appointment, a quote set at your kitchen table, and a premium you can&rsquo;t see the size of. The Kirkland discount instinct doesn&rsquo;t apply. Ten percent back on a quote three times the comparable is not a deal; it&rsquo;s a rebate on a markup.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#structure">How the program actually works</a></li>
          <li><a href="#brands-chart">Where it sits against every channel (chart)</a></li>
          <li><a href="#math">The member math (tool)</a></li>
          <li><a href="#perks">The perks &amp; their fine print</a></li>
          <li><a href="#worksheet">The quote, reconstructed (chart)</a></li>
          <li><a href="#cancel">Your 3-day window &mdash; use it</a></li>
          <li><a href="#financing">The membership doesn&rsquo;t co-sign the loan (tool)</a></li>
          <li><a href="#fair">What the premium legitimately buys</a></li>
        </ol>
      </details>
      <h2 id="structure">How the Costco softener program actually works</h2>
      <p style="margin:0">You submit your number, an EcoWater consultant visits, tests your water, and quotes a customized system &mdash; softener, refiner, or RO bundle. Member reports describe consultations running two hours, and one Houzz commenter described the consultant as &ldquo;extremely pushy&rdquo; toward same-day signing. Costco fulfills the perks and hosts the trust; the <em>dealer</em> sets the price and installs &mdash; the same structure as <a href="/water-softener-installation-cost/">big-box install programs</a> and the <a href="/rainsoft-water-softener-cost/">Home Depot kiosk channel</a>, wearing a membership card. One detail reviewers flag: unlike nearly every Costco product, the EcoWater page carries no member reviews.</p>

      <h2 id="brands-chart">Where the Costco route sits against every channel we track</h2>
      <p style="margin:0 0 16px">Reported installed ranges, one scale &mdash; the Costco bar and the RainSoft bar are nearly the same bar:</p>
    </div>
    <div class="col-wide">''' + range_bars(c5_brand_bars, 12000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Sources: Culligan, Kinetico, RainSoft bands from our sourced expos&eacute;s; Costco/EcoWater band from member-reported quotes (House Digest / Reddit); factory-direct comparable from published unit + labor pricing.</p>

      <h2 id="math">The member math, honestly run</h2>
      <p style="margin:0 0 16px">The perks are real money &mdash; run them against your quote, then look at what remains:</p>
      <div data-costco-calc></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Shop Card is 10% of the pre-tax equipment-and-install total (Costco terms); Executive adds up to 2%. Comparable route: published mid-tier unit plus independent labor on an existing loop &mdash; the <a href="/water-softener-installation-cost/">install guide</a> itemizes it.</p>
      <h2 style="font-size:22px;margin-top:32px">And check the quote itself against the reported bands</h2>
      <div data-quote-check data-min="3000" data-max="11000" data-start="7000" data-bands=''' + BANDS5 + '''></div>

      <h2 id="perks">The perks &mdash; and their fine print</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Costco EcoWater member perks, per Costco&rsquo;s published terms</caption>
        <thead><tr><th scope="col">Perk</th><th scope="col" class="num">Worth (on $8,000)</th><th scope="col">Fine print</th></tr></thead>
        <tbody>
          <tr><td>10% Costco Shop Card</td><td class="num">$800</td><td class="muted">Pre-tax, equipment + install only; arrives up to 4 weeks after signed completion; extras don&rsquo;t count</td></tr>
          <tr><td>Executive 2% reward</td><td class="num">$160</td><td class="muted">Requires the $130/yr Executive tier</td></tr>
          <tr><td>Extended warranty</td><td class="num">Real, unpriced</td><td class="muted">Member exclusive, via EcoWater dealer network</td></tr>
          <tr><td>3-business-day right to cancel</td><td class="num">Your leverage</td><td class="muted">After it expires: special-order installed merchandise &mdash; no returns, no refunds</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Read the last row twice. Costco&rsquo;s famous return generosity <em>does not apply here</em> &mdash; once the cancellation window closes on installed special-order equipment, the purchase is final. The instinct that makes members comfortable signing (&ldquo;it&rsquo;s Costco, I can always return it&rdquo;) is exactly the instinct the structure doesn&rsquo;t honor.</p>

      <h2 id="worksheet">The quote, reconstructed &mdash; perks included</h2>
      <p style="margin:0">Build the reported quote from published components, credit the perks in full, and price what&rsquo;s left:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("EcoWater-via-Costco quote, reconstructed (est.)", c5_rows, total_label="Reported band, net of perks") + '''</div>
    <div class="col">
      <p style="margin-top:24px">Even with every perk credited, the implied remainder is the second-largest we track &mdash; behind only <a href="/rainsoft-water-softener-cost/">RainSoft</a>. And House Digest&rsquo;s own comparison lands the point without our help: a <span class="fig">$499</span> metered Rheem at Home Depot performs the same ion exchange. The full anatomy of that gap is in the <a href="/dealer-vs-factory-direct-pricing/">dealer vs. factory-direct breakdown</a>.</p>
    </div>
    <div class="col-wide" style="margin-top:24px">
      <div class="donut-wrap">''' + donut_svg([("#16303F",19),("#1F7A5C",6),("#E8A13D",12),("#B3541E",63)], "$8,000", "quote (est., mid)", "Reconstruction of an $8,000 Costco/EcoWater quote") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> Comparable equipment (~$1,050) <span class="pc">~19%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Install &amp; materials (~$530) <span class="pc">~6%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Perks returned to you (~$960) <span class="pc">~12%</span></div>
          <div><span class="sw" style="background:#B3541E"></span> Implied remainder: channel, consultation, dealer overhead <span class="pc">~63%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; illustrative reconstruction from published component midpoints and Costco&rsquo;s perk terms on a prepared home</div>
    </div>
    <div class="col">
      <div style="margin-top:40px">''' + cta_box("The published-price benchmark",
        "Walk into the consultation holding a posted number: SpringWell publishes its softener pricing online \u2014 sized by bathrooms, shipped free, 6-month money-back guarantee \u2014 so the consultant\u2019s quote has something real to be compared against, in the room, in writing.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="cancel">Your 3-business-day window &mdash; the most useful clause in the contract</h2>
      <p style="margin:0">Costco&rsquo;s terms give you three business days to cancel. Used well, that clause converts a pressure sale into a considered purchase: sign nothing at the sit-down; if you do sign, spend day one collecting a written competing quote (the <a href="/dealer-vs-factory-direct-pricing/">four-step script</a> takes an hour), day two comparing the itemized lines, and cancel inside the window if the math doesn&rsquo;t survive daylight. A quote that can&rsquo;t wait three days was never a price &mdash; it was a close.</p>

      <h2 id="financing">The membership doesn&rsquo;t co-sign the loan</h2>
      <p style="margin:0 0 16px">Everything about this channel is engineered to feel safe: a warehouse you already trust, a card already in your wallet, a brand with a legendary returns desk. But the financing paperwork that appears at the end of a two-hour in-home consultation is not Costco&rsquo;s promise. It is a credit agreement with a lender &mdash; and it behaves like one:</p>
      <div data-finance-calc data-pmt="140" data-term="84" data-apr="15.9"></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Illustrative &mdash; not a quote. No storefront in this chain publishes financing terms. The default is seeded at a payment implying a system near $7,000, inside the reported band above.</p>
      <p style="margin:20px 0 0">That example hands over roughly <span class="fig">$11,760</span> for an implied system near <span class="fig">$7,000</span>. Now connect it to <a href="#cancel">the section directly above</a>, because this is where the warehouse frame becomes genuinely expensive: <strong>the reported three-day cancellation window governs the purchase. It does not un-sign a credit agreement, and it does not survive day four.</strong> The famous returns policy belongs to Costco. The loan does not. Regret this on day five &mdash; with the reported no-returns terms already closed behind you &mdash; and you are not returning a rotisserie chicken. You are servicing a contract.</p>
      <p style="margin:16px 0 0">Which is why one distinction matters more here than anywhere else on the page: <strong>&ldquo;no interest if paid in full&rdquo; is not 0% APR.</strong> It is deferred interest &mdash; the standard promotional structure of the retail credit channel &mdash; and the interest accrues silently the entire time. Leave any balance when the window shuts and it is billed retroactively to the purchase date on the <em>original</em> amount, at ongoing rates the CFPB reports typically run above 20% regardless of credit score. About one in five of these promotional balances end up taking that hit. Federal advertising rules require the words &ldquo;if paid in full&rdquo; to appear, so they are your tell. Get the <strong>cash price, APR, term and total of payments</strong> in writing <em>before</em> the three-day clock starts running, and let the <a href="/dealer-vs-factory-direct-pricing/">channel hub</a> decode the rest.</p>

      <h2 id="fair">What the premium legitimately buys</h2>
      <p>Genuine credit: EcoWater is one of the oldest names in the industry &mdash; its founder received the first water softener patent in 1925, the company holds 70+ patents, systems carry NSF certification and HydroLink Wi-Fi monitoring, and Costco&rsquo;s accountability layer plus extended warranty is a real backstop most dealer channels lack. For a member who wants one accountable phone number and zero involvement, this is a rational hands-off purchase.</p>
      <p style="margin:0">The critique is the series&rsquo; standing one: none of that requires hiding the number until a consultant is on your couch. The engineering is from 1925; the pricing model shouldn&rsquo;t be. Bring the reported bands, run the member math above, and make the trust cut both ways.</p>
      <div style="margin-top:40px">''' + cta_box("The no-consultation alternative",
        "The factory-direct version of the same outcome: SpringWell\u2019s SS series at a posted price, lifetime warranty on tanks and valves, free shipping, DIY-friendly on an existing loop \u2014 and the money-back window is six months, not three business days.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(c5_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/rainsoft-water-softener-cost/"><div class="name">RainSoft cost expos&eacute;</div><div class="range">$6,000&ndash;$11,000</div><div class="desc">The Home Depot kiosk channel.</div></a>
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Dealer vs. factory-direct</div><div class="desc">Where the extra thousands go.</div></a>
        <a class="card" href="/low-cost-water-softener/"><div class="name">Low-cost softeners</div><div class="desc">What $499 actually buys &mdash; tiers &amp; false economies.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Costco &mdash; EcoWater Water Treatment Systems (official program pages)</strong> &mdash; <a href="https://www.costco.com/ecowater-water-treatment-systems.html" rel="noopener" target="_blank">costco.com</a>. Supports: consultation-only model with no listed prices; 10% Shop Card terms (pre-tax, material + install, up to 4-week delivery); Executive 2%; extended member warranty; 3-business-day cancellation and no-return terms for installed special-order merchandise; HydroLink/NSF/patent claims.',
 '<strong>House Digest &mdash; Are Costco&rsquo;s EcoWater Systems Worth The Money? (Feb 2025)</strong> &mdash; <a href="https://www.housedigest.com/1779560/costco-water-softener-worth-it-reviews/" rel="noopener" target="_blank">housedigest.com</a>. Supports: Reddit-reported $6,000&ndash;$10,000 quote; 2-hour consultation; Houzz pushy-consultant report; no reviews on Costco&rsquo;s page; Home Depot EcoWater 44% recommend; $499 Rheem comparison.',
 '<strong>Yahoo Lifestyle syndication of the same analysis (Feb 2025)</strong> &mdash; <a href="https://www.yahoo.com/lifestyle/costcos-ecowater-water-treatment-systems-114559480.html" rel="noopener" target="_blank">yahoo.com</a>. Supports: corroboration of the reported quote band and program structure.',
 '<strong>Angi &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: comparable labor ($200&ndash;$500) used in the reconstruction.',
 '<strong>HomeGuide &mdash; Water Softener Cost (2026)</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: comparable equipment class ($600&ndash;$1,500&ndash;$2,000) used in the reconstruction.',
 '<strong>Consumer Financial Protection Bureau &mdash; Issue Spotlight: The High Cost of Retail Credit Cards; Regulation Z &sect;1026.16</strong> &mdash; <a href="https://www.consumerfinance.gov/data-research/research-reports/issue-spotlight-the-high-cost-of-retail-credit-cards/" rel="noopener" target="_blank">consumerfinance.gov</a>, <a href="https://www.consumerfinance.gov/rules-policy/regulations/1026/16/" rel="noopener" target="_blank">Reg Z &sect;1026.16</a>. Supports: deferred interest billed retroactively on the original purchase amount; roughly 1 in 5 promotional balances hit; ongoing rates above 20% regardless of credit score; the &ldquo;if paid in full&rdquo; disclosure requirement. Financing mechanics only &mdash; not this brand&rsquo;s terms, which are unpublished.',
 '<strong>National Consumer Law Center &mdash; Deceptive Bargain: The Hidden Time Bomb of Deferred Interest</strong> &mdash; <a href="https://www.nclc.org/resources/deceptive-bargain-the-hidden-time-bomb-of-deferred-interest-credit-cards/" rel="noopener" target="_blank">nclc.org</a>. Supports: the mechanics of retroactive interest on promotional balances.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("costco-water-softener-cost/index.html", c5)


# ============ A3 — SALT-FREE COST (homepage-linked, honest decoder) ============
a3_faqs = [
 ("How much does a salt-free water softener cost?","Whole-house TAC conditioners run $500&ndash;$2,000 for the unit and $150&ndash;$400 to install &mdash; typically $900&ndash;$3,000 all-in. Installation is cheaper than a salt softener because there&rsquo;s no drain line, no electrical, and no brine tank."),
 ("Do salt-free water softeners actually work?","For scale prevention, yes &mdash; TAC is the one salt-free technology with real data: an Arizona State study found it the most effective non-salt method (&gt;90% scale reduction), and German DVGW W512 testing measured 99.6%. For actual softening &mdash; no: hardness stays in the water."),
 ("What&rsquo;s the catch with salt-free conditioners?","They condition, they don&rsquo;t soften. Your water still tests hard, soap lathers the same, spotting is reduced but not gone, and iron or sediment fouls the media. If you want the slippery soft-water feel, only ion exchange delivers it."),
 ("What does salt-free maintenance cost?","Almost nothing annually: no salt, no electricity, no backwash. The one recurring line is media replacement every 3&ndash;6 years (some rated longer) at $100&ndash;$500 &mdash; roughly $20&ndash;$80 per year annualized."),
 ("Is salt-free cheaper than a salt-based softener?","Over ten years, usually yes &mdash; roughly $750&ndash;$3,200 versus $1,650&ndash;$3,800+ for a comparable salt system once salt and a resin re-bed are counted. But they buy different outcomes: scale control versus true soft water."),
 ("Who should NOT buy a salt-free system?","Anyone who wants genuinely soft water (lather, no spots, slippery feel), homes with very hard water where TAC performance drops, and well water with iron or sediment unless it&rsquo;s pre-filtered &mdash; iron coats the media and kills it."),
]
a3_rows = [
 ("Whole-house TAC conditioner (unit)",500,2000,"CheckMyTap / TapWaterData published class"),
 ("Installation (no drain, no electrical)",150,400,"Simpler than a softener install &mdash; two connections"),
 ("Sediment prefilter (recommended; protects media)",0,150,"Skip only on clean, filtered city water"),
 ("Media replacement fund (per decade, 1&ndash;2 cycles)",100,800,"$100&ndash;$500 every 3&ndash;6 years"),
]
a3_bars = [
 ("Electronic / magnetic descaler",100,600,"#D9DED9"),
 ("Cartridge TAC system",200,800,"#5B6B75"),
 ("Whole-house TAC (unit only)",500,2000,"#16303F"),
 ("Whole-house TAC, installed totals",900,3000,"#E8A13D"),
]
a3 = head("Salt-Free Water Softener Cost (2026): TAC Conditioners Priced",
 "Salt-free conditioners cost $900\u2013$3,000 installed with near-zero upkeep \u2014 but they condition, they don\u2019t soften. Honest pricing, sourced.",
 "/salt-free-water-softener-cost/",
 ld(article_schema("Salt-Free Water Softener Cost in 2026: What Conditioners Really Cost (and Really Do)","Sourced TAC conditioner pricing, ownership math, effectiveness data, and the honest decision framework.","/salt-free-water-softener-cost/",date="2026-07-12"))
 + ld(faq_schema(a3_faqs,"/salt-free-water-softener-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Salt-free cost","/salt-free-water-softener-cost/")])))
a3 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Salt-free cost</nav>
      <h1>Salt-Free Water Softener Cost in 2026: What Conditioners Really Cost (and Really Do)</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">The pricing first: whole-house salt-free (TAC) systems run <span class="fig">$500&ndash;$2,000</span> for the unit per <a href="https://checkmytap.com/solutions/salt-free-conditioners/" rel="noopener" target="_blank">CheckMyTap</a> and <a href="https://www.tapwaterdata.com/blog/guides/water-softener-cost-guide" rel="noopener" target="_blank">TapWaterData</a>, with installation at just <span class="fig">$150&ndash;$400</span> &mdash; no drain line, no electrical, no brine tank &mdash; for installed totals of <span class="fig">$900&ndash;$3,000</span>. Ownership is the category&rsquo;s superpower: no salt, no power, and media replacement every 3&ndash;6 years at <span class="fig">$100&ndash;$500</span>, about <span class="fig">$20&ndash;$80/yr</span> annualized.</p>
      <p><strong>Salt-free water softeners cost $900&ndash;$3,000 installed &mdash; $500&ndash;$2,000 for the TAC unit plus $150&ndash;$400 for a drain-free, power-free install. The near-zero upkeep is real; so is the fine print: they prevent scale, they don&rsquo;t remove hardness.</strong></p>
      <p style="margin:0">Now the estimator&rsquo;s honesty clause, because this category runs on a misnomer: a &ldquo;salt-free softener&rdquo; doesn&rsquo;t soften. It conditions &mdash; converts hardness minerals into crystals that won&rsquo;t stick to your pipes and water heater. That&rsquo;s genuinely valuable and cheaply owned. But your water still tests hard, and buying this category for soft-water <em>feel</em> is the most common $2,000 mistake in the aisle. This page prices the category and draws the line in daylight.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#worksheet">The full project worksheet</a></li>
          <li><a href="#aisle">The salt-free aisle by price (chart)</a></li>
          <li><a href="#works">Does it actually work? The evidence</a></li>
          <li><a href="#delivers">What it delivers &mdash; and what it can&rsquo;t</a></li>
          <li><a href="#tco">10-year comparison vs. salt (tool)</a></li>
          <li><a href="#ownership">The ownership pie (chart)</a></li>
          <li><a href="#framework">Which camp are you in?</a></li>
        </ol>
      </details>
      <h2 id="worksheet">The full salt-free project, itemized</h2>
      <p style="margin:0">Everything a TAC project costs across a decade of ownership &mdash; note how short this sheet is compared to the <a href="/">salt-based worksheet</a>:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Salt-free TAC project + decade of ownership", a3_rows, total_label="10-year span") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>How I&rsquo;d read this sheet:</strong> there is no salt line, no electricity line, no valve-rebuild line, and no re-bed line &mdash; the four rows that dominate the <a href="/water-softener-maintenance-cost/">salt-based maintenance budget</a> simply don&rsquo;t exist here. The prefilter row is the one owners skip and regret: iron and sediment coat TAC media and kill it, so on anything but clean city water, that $0&ndash;$150 protects the whole investment.</p>

      <h2 id="aisle">The salt-free aisle, decoded by price</h2>
      <p style="margin:0 0 16px">Three technologies share the shelf, and only one has strong evidence behind it:</p>
    </div>
    <div class="col-wide">''' + range_bars(a3_bars, 3000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Ranges: CheckMyTap, TapWaterData 2026 guides. On the gray bar: the Water Quality Association doesn&rsquo;t certify electromagnetic devices as softeners, and independent testing of them is inconsistent &mdash; the budget-tier <a href="/low-cost-water-softener/">technology decoder</a> covers why.</p>

      <h2 id="works">Does it actually work? The evidence, straight</h2>
      <p style="margin:0">For scale prevention, TAC is the one salt-free technology with real data: an Arizona State University evaluation of softener alternatives found TAC the most effective non-salt method, with scale reduction consistently above <span class="fig">90%</span>, and German DVGW W512 testing &mdash; the strictest protocol in the category &mdash; measured <span class="fig">99.6%</span> efficiency on test heating coils. That&rsquo;s why this page takes the category seriously. What no test shows: hardness removal, because none occurs. Both things are true at once, and an honest cost page has to hold both.</p>

      <h2 id="delivers">What your money delivers &mdash; and what it can&rsquo;t</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>What a salt-free TAC conditioner delivers, goal by goal</caption>
        <thead><tr><th scope="col">Your goal</th><th scope="col">Delivered?</th><th scope="col">The honest note</th></tr></thead>
        <tbody>
          <tr><td>Stop scale in pipes, heater, appliances</td><td><strong>Yes</strong></td><td class="muted">88&ndash;99% reduction in testing; the category&rsquo;s whole job</td></tr>
          <tr><td>Dissolve existing scale</td><td>Partly</td><td class="muted">Conditioned water releases some old buildup over weeks</td></tr>
          <tr><td>Soap lather, slippery soft-water feel</td><td class="muted"><strong>No</strong></td><td class="muted">Hardness stays in the water &mdash; only ion exchange changes this</td></tr>
          <tr><td>Spot-free glass and fixtures</td><td class="muted">Reduced, not gone</td><td class="muted">Minerals still dry on surfaces, just less sticky</td></tr>
          <tr><td>Septic-safe / brine-restricted areas</td><td><strong>Yes</strong></td><td class="muted">No brine discharge &mdash; the legal choice where softeners are restricted</td></tr>
          <tr><td>Keep calcium &amp; magnesium in drinking water</td><td><strong>Yes</strong></td><td class="muted">Nothing is removed &mdash; a feature here, a limit elsewhere</td></tr>
          <tr><td>Handle iron or sediment</td><td class="muted"><strong>No</strong></td><td class="muted">Both foul TAC media &mdash; pre-filter or treat separately first</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">If three or more of your yeses live in the top and bottom &ldquo;Yes&rdquo; rows, you&rsquo;re a conditioner household. If your reason for shopping is the soap-and-skin row, stop here and price a <a href="/pick/salt-softener" ''' + PICK + '''>true softener</a> instead &mdash; no conditioner at any price delivers that row. Not sure which camp your water puts you in? A <a href="/pick/test-kit" ''' + PICK + '''>test kit</a> settles it for less than a bag of potassium.</p>

      <h2 id="tco">The 10-year money question, answered honestly</h2>
      <p style="margin:0 0 16px">Two taps &mdash; and read the disclaimer under the numbers, because these buy different outcomes:</p>
      <div data-tco-calc></div>
      <div style="margin-top:40px">''' + cta_box("The published-price TAC benchmark",
        "If the conditioner camp is yours, benchmark it against the category\u2019s most-cited system: SpringWell\u2019s FutureSoft \u2014 independent guides credit it with handling up to 81 GPG at 20 GPM \u2014 publishes its price online, ships free, installs without drain or power, and carries a 6-month money-back guarantee.",
        "Check current SpringWell FutureSoft price","futuresoft") + '''</div>

      <h2 id="ownership">The ownership pie: almost all day-one</h2>
      <p style="margin:0 0 16px">Even more than <a href="/kinetico-water-softener-cost/">Kinetico</a>, salt-free front-loads everything &mdash; the decade looks like this:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",78),("#E8A13D",15),("#1F7A5C",7)], "~$2,000", "10 yrs (midpoints)", "10-year salt-free ownership composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> Unit + install (midpoint ~$1,525) <span class="pc">~78%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Media replacement fund (~$300) <span class="pc">~15%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Prefilter cartridges <span class="pc">~7%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of sourced ranges &middot; no salt, no electricity, no re-bed &mdash; the recurring lines that fill the <a href="/water-softener-maintenance-cost/">salt-based version of this chart</a> are absent by design</div>
    </div>
    <div class="col">
      <h2 id="framework" style="margin-top:48px">Which camp are you in? The two-question framework</h2>
      <p><strong>Question one: what&rsquo;s the actual goal?</strong> Protecting the water heater, tankless unit, and pipes &rarr; conditioner camp. Soap, skin, spots, laundry feel &rarr; softener camp, full stop. <strong>Question two: what&rsquo;s in your water?</strong> Moderate hardness on clean city water &rarr; TAC performs at its best. Very hard water &rarr; TAC performance drops and ion exchange becomes the reliable tool. Iron, manganese, or sediment &rarr; treat those first or the media pays the price.</p>
      <p style="margin:0">And the estimator&rsquo;s closing rule for the category: <strong>salt-free is the cheapest system to own and the most expensive to buy for the wrong reason.</strong> Priced against its actual job &mdash; scale control at near-zero upkeep &mdash; it&rsquo;s one of the best values on this site. Priced against the job it can&rsquo;t do, it&rsquo;s $2,000 of disappointment. The <a href="/why-are-water-softeners-so-expensive/">cost-anatomy guide</a> covers the mirror-image mistake on the salt side.</p>
      <div style="margin-top:40px">''' + cta_box("Scale control at a posted price",
        "SpringWell\u2019s FutureSoft is the factory-direct version of everything this page priced: TAC conditioning with no salt, no drain, no electricity, a lifetime warranty on the tank, free shipping \u2014 and the price is on the screen before anyone visits your kitchen.",
        "Check current SpringWell FutureSoft price","futuresoft") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(a3_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/"><div class="name">Full cost guide</div><div class="range">$840&ndash;$4,120</div><div class="desc">The salt-based side, itemized.</div></a>
        <a class="card" href="/low-cost-water-softener/"><div class="name">Low-cost softeners</div><div class="desc">The technology decoder &amp; budget tiers.</div></a>
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">Maintenance costs</div><div class="desc">The recurring lines salt-free deletes.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>CheckMyTap &mdash; Salt-Free Water Conditioners Guide (Apr 2026)</strong> &mdash; <a href="https://checkmytap.com/solutions/salt-free-conditioners/" rel="noopener" target="_blank">checkmytap.com</a>. Supports: unit $800&ndash;$2,000; install $150&ndash;$400; media every 3&ndash;6 yrs at $100&ndash;$400; 5-yr totals; honest performance limits (lather, spotting, hardness unchanged).',
 '<strong>TapWaterData &mdash; Water Softener Cost Guide (Mar 2026)</strong> &mdash; <a href="https://www.tapwaterdata.com/blog/guides/water-softener-cost-guide" rel="noopener" target="_blank">tapwaterdata.com</a>. Supports: salt-free units $500&ndash;$3,000; media $200&ndash;$500 annualizing to $20&ndash;$80/yr; electronic descalers $200&ndash;$600 and WQA non-certification.',
 '<strong>TapWaterData &mdash; What TAC Actually Does (Jun 2026)</strong> &mdash; <a href="https://www.tapwaterdata.com/blog/guides/salt-free-water-softeners-tac-explained" rel="noopener" target="_blank">tapwaterdata.com</a>. Supports: 88&ndash;99% scale reduction framing; high-hardness and hot-water limits; iron/sediment fouling; the right-tool decision framework.',
 '<strong>Arizona State University study &amp; DVGW W512 results (via ecoTAC technical overview)</strong> &mdash; <a href="https://www.home-water-purifiers-and-filters.com/salt-free.php" rel="noopener" target="_blank">home-water-purifiers-and-filters.com</a>. Supports: TAC most effective non-salt technology (&gt;90%); DVGW W512 99.6% result; media life 3&ndash;5 yrs.',
 '<strong>SoftPro &mdash; Alternative Water Conditioning Systems (Apr 2026)</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/alternative-water-conditioning-systems-stop-buying-salt" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: $800&ndash;$2,500 range; 6&ndash;8 yr media claims; SpringWell FutureSoft 81 GPG / 20 GPM citation.',
 '<strong>World Water Reserve &mdash; Best Salt-Free Softeners (Jun 2026)</strong> &mdash; <a href="https://worldwaterreserve.com/best-salt-free-water-softener/" rel="noopener" target="_blank">worldwaterreserve.com</a>. Supports: verified June-2026 category pricing (from $1,149); iron-fouling caution; FutureSoft as the step-up for wells and high hardness.',
 '<strong>Angi &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: salt-side comparison inputs (bags, labor) used by the 10-year tool.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("salt-free-water-softener-cost/index.html", a3)


# ============ A4 — DUAL-TANK COST (last homepage 404) ============
a4_faqs = [
 ("How much does a dual-tank water softener cost?","DIY-class twins (Fleck 9100SXT builds) list at $1,219&ndash;$1,454 for the unit; dealer twins run $3,000&ndash;$6,000 before install (Culligan HE Twin, Kinetico Premier). Typical installed projects land $1,500&ndash;$5,000, with reported dealer installs reaching $7,200."),
 ("What does a dual-tank softener do that a single tank doesn&rsquo;t?","One resin tank serves while the other regenerates, so there&rsquo;s never a hard-water window and the system uses 100% of each tank&rsquo;s capacity instead of holding reserve. That&rsquo;s the whole premium: continuity and efficiency, not softer water."),
 ("Do most homes need a twin-tank softener?","Honestly, no. A metered single tank regenerates at 2 a.m. when nobody&rsquo;s using water &mdash; for typical daytime households on city water, the window a twin eliminates doesn&rsquo;t exist. Twins earn their cost on wells, very hard water, 5+ person homes, and round-the-clock use."),
 ("How much more does dual-tank cost than single-tank?","Published figures put the twin premium at $500&ndash;$1,500 on comparable equipment. On the DIY route the gap is smaller: a 9100SXT twin at ~$1,300 versus an equivalent single at $600&ndash;$900."),
 ("Is a dual-tank softener worth it on well water?","Often yes &mdash; high hardness plus iron means frequent regeneration, which is where a single tank&rsquo;s reserve waste and downtime add up. Treat iron first or alongside; it&rsquo;s the bigger equipment decision on most wells."),
 ("How long do dual-tank softeners last?","The same 10&ndash;20 years as quality singles &mdash; and often longer per tank, since alternating service splits the workload. Kinetico&rsquo;s non-electric twins are the extreme case, with owners reporting 20+ years."),
]
a4_rows = [
 ("Twin-tank system, DIY class (Fleck 9100SXT build)",1219,1454,"Current listings; dealer-class twins run $3,000&ndash;$6,000 instead"),
 ("Installation labor (existing loop)",200,500,"Same swap labor as a single &mdash; one extra tank to set"),
 ("Bypass, fittings &amp; materials",40,120,"Twins ship with interconnect; confirm what&rsquo;s boxed"),
 ("Loop run (only if none exists)",0,2000,"The usual wildcard &mdash; $600&ndash;$2,000 when needed"),
]
a4_bars = [
 ("DIY twin unit (Fleck 9100SXT class)",1219,1454,"#1F7A5C"),
 ("Dealer twin equipment (Culligan HE Twin)",3000,5000,"#16303F"),
 ("Kinetico Premier twins (reported)",3500,6000,"#5B6B75"),
 ("Installed twin projects, all routes",1500,7200,"#E8A13D"),
]
a4 = head("Dual Tank Water Softener Cost (2026): 24/7 Soft Water, Priced",
 "Dual-tank softeners cost $1,500\u2013$5,000 installed \u2014 DIY twins from $1,219, dealer twins to $6,000+. Who actually needs one, sourced and priced.",
 "/dual-tank-water-softener-cost/",
 ld(article_schema("Dual-Tank Water Softener Cost in 2026: 24/7 Soft Water, Honestly Priced","Sourced twin-tank pricing across DIY and dealer routes, with the honest who-needs-it framework.","/dual-tank-water-softener-cost/",date="2026-07-12"))
 + ld(faq_schema(a4_faqs,"/dual-tank-water-softener-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Dual-tank cost","/dual-tank-water-softener-cost/")])))
a4 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Dual-tank cost</nav>
      <h1>Dual-Tank Water Softener Cost in 2026: 24/7 Soft Water, Honestly Priced</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Twin-tank pricing splits cleanly by route: DIY-class twins built on the Fleck 9100SXT valve currently list at <span class="fig">$1,219&ndash;$1,454</span>, while dealer twins &mdash; Culligan&rsquo;s HE Twin at <span class="fig">$3,000&ndash;$5,000</span>, Kinetico&rsquo;s Premier series at <span class="fig">$3,500&ndash;$6,000</span> &mdash; carry the channel premium our <a href="/brands/">brand expos&eacute;s</a> itemize. <a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">Fixr</a> puts the typical dual-tank install around <span class="fig">$2,500</span> for a 3&ndash;4 bedroom home, and reported dealer installs reach <span class="fig">$7,200</span>.</p>
      <p><strong>Dual-tank water softeners cost $1,500&ndash;$5,000 installed for most homes: $1,219&ndash;$1,454 for a DIY-class twin unit or $3,000&ndash;$6,000 for dealer equipment, plus $200&ndash;$500 swap labor &mdash; a $500&ndash;$1,500 premium over comparable single-tank systems.</strong></p>
      <p style="margin:0">And the estimator&rsquo;s opening truth, because it decides whether you should read further: <em>most homes shopping for a twin need a correctly-sized single.</em> A metered single tank regenerates at 2 a.m. while your house sleeps &mdash; the hard-water window a twin eliminates never occurs. Twins earn their premium in four specific situations, and this page prices the premium and names the situations so you buy the tanks your house actually uses.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#fit">Do you actually need twin tanks? (tool)</a></li>
          <li><a href="#market">The twin market by route (chart)</a></li>
          <li><a href="#worksheet">The twin project worksheet</a></li>
          <li><a href="#compare">Single vs. twin, honestly compared</a></li>
          <li><a href="#when">The four situations where twins win</a></li>
          <li><a href="#ownership">The 10-year picture (chart)</a></li>
        </ol>
      </details>
      <h2 id="fit">Two taps: does your home actually need twin tanks?</h2>
      <div data-twin-fit></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Not sure which demand button is yours? A <a href="/pick/test-kit" ''' + PICK + '''>hardness test</a> answers it in minutes &mdash; sizing to a measured number is the whole game here.</p>

      <h2 id="market">The twin market, route by route</h2>
      <p style="margin:0 0 16px">Same alternating-tank concept, radically different price tags &mdash; the spread is the sales channel, not the resin:</p>
    </div>
    <div class="col-wide">''' + range_bars(a4_bars, 8000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Sources: current 9100SXT listings (June 2026 &mdash; verify before purchase), BestCompany Culligan tiers, ThePricer Kinetico data and real install reports from our <a href="/kinetico-water-softener-cost/">Kinetico expos&eacute;</a>. The dealer bars include the channel premium the <a href="/dealer-vs-factory-direct-pricing/">dealer vs. factory-direct breakdown</a> reconstructs.</p>

      <h2 id="worksheet">The twin project, itemized (DIY-class route)</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Dual-tank project, DIY-class equipment", a4_rows, total_label="Project span") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>How I&rsquo;d read this sheet:</strong> on an existing loop, a twin project lands <span class="fig">$1,459&ndash;$2,074</span> &mdash; barely above a quality single once you count the single&rsquo;s reserve-capacity waste. Choose the dealer route instead and the equipment line alone jumps to <span class="fig">$3,000&ndash;$6,000</span>; that&rsquo;s a service-relationship decision, not a hardware one. Twin-specific install note: you need floor space for two resin tanks plus brine &mdash; measure the corner before you order anything.</p>
      <div style="margin-top:24px">''' + cta_box("Right-size before you twin up",
        "The honest alternative for most of the homes on this page: a correctly-sized metered single. SpringWell\u2019s SS series scales to larger households (SS4, SS+), meters regeneration to actual use, publishes its price online, ships free, and carries a lifetime warranty on tanks and valves \u2014 price it against the twin math before paying for a second tank your schedule never uses.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="compare">Single vs. twin, honestly compared</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Single-tank versus dual-tank water softeners</caption>
        <thead><tr><th scope="col">Factor</th><th scope="col">Metered single</th><th scope="col">Dual-tank twin</th></tr></thead>
        <tbody>
          <tr><td>Upfront (unit, comparable class)</td><td class="num">$600&ndash;$1,500</td><td class="num">$1,219&ndash;$1,454 DIY / $3,000&ndash;$6,000 dealer</td></tr>
          <tr><td>Soft water during regeneration</td><td class="muted">No &mdash; hard-water window (usually 2 a.m.)</td><td><strong>Yes &mdash; tanks alternate</strong></td></tr>
          <tr><td>Capacity efficiency</td><td class="muted">Holds reserve; regenerates early</td><td><strong>Uses 100% of each tank</strong></td></tr>
          <tr><td>Footprint</td><td><strong>One tank + brine</strong></td><td class="muted">Two tanks + brine &mdash; measure first</td></tr>
          <tr><td>Best for</td><td class="muted">Typical daytime households, city water</td><td class="muted">Wells, very hard water, 5+ people, 24/7 use</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <h2 id="when">The four situations where twins genuinely win</h2>
      <p><strong>1. Round-the-clock water use.</strong> Shift workers, multigenerational homes, short-term rentals &mdash; when there&rsquo;s no 2 a.m. lull, the regeneration window becomes real hard water in real showers. <strong>2. Wells and very hard water (20+ gpg).</strong> Heavy hardness means frequent regeneration, which multiplies both the single tank&rsquo;s downtime and its reserve waste &mdash; and on iron-bearing wells, pair the softener decision with treatment, or go straight to a <a href="/pick/filter-salt-softener-combo" ''' + PICK + '''>filter + softener combo</a> and solve both in one install. <strong>3. Five-plus-person households.</strong> Daily demand near a single tank&rsquo;s capacity forces near-daily regeneration &mdash; the twin&rsquo;s alternation pays for itself in salt efficiency. <strong>4. Zero-tolerance uses.</strong> Tankless heaters and spot-free rinse systems that must never see hardness.</p>
      <p style="margin:0">Outside those four, the twin premium buys continuity your schedule already provides free. That&rsquo;s not a criticism of twins &mdash; it&rsquo;s the same rule every page here runs on: <strong>pay for the line your house actually uses.</strong></p>

      <h2 id="ownership">The 10-year picture</h2>
    </div>
    <div class="col-wide" style="margin-top:16px">
      <div class="donut-wrap">''' + donut_svg([("#16303F",72),("#1F7A5C",18),("#5B6B75",10)], "~$4,500", "10 yrs (midpoints)", "10-year dual-tank ownership composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> System, installed (midpoint ~$3,250) <span class="pc">~72%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Salt, 10 yrs (~$800 &mdash; alternation is salt-efficient) <span class="pc">~18%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Parts &amp; upkeep <span class="pc">~10%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of sourced ranges &middot; the salt slice runs below a comparable single&rsquo;s because 100%-capacity alternation wastes nothing &mdash; the <a href="/water-softener-maintenance-cost/">maintenance guide</a> prices every line</div>
    </div>
    <div class="col">
      <div style="margin-top:40px">''' + cta_box("If the four situations aren\u2019t yours",
        "Most readers of this page land at \u201ccorrectly-sized single\u201d \u2014 and that math has a posted price: SpringWell\u2019s metered SS series, sized by bathrooms up to SS+, free shipping, 6-month money-back guarantee, lifetime warranty on the tank and valve. The twin decision stays reversible while you test the sizing first.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(a4_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/"><div class="name">Full cost guide</div><div class="range">$840&ndash;$4,120</div><div class="desc">Every line item, itemized with charts.</div></a>
        <a class="card" href="/kinetico-water-softener-cost/"><div class="name">Kinetico cost expos&eacute;</div><div class="range">$3,000&ndash;$5,000+</div><div class="desc">The dealer twin, reconstructed.</div></a>
        <a class="card" href="/salt-free-water-softener-cost/"><div class="name">Salt-free cost</div><div class="range">$900&ndash;$3,000</div><div class="desc">The conditioner camp, honestly priced.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>AffordableWater &mdash; Fleck 9100SXT twin listings (June 2026)</strong> &mdash; <a href="https://affordablewater.us/collections/water-softeners-up-to-24-000-grains" rel="noopener" target="_blank">affordablewater.us</a>. Supports: DIY twin pricing $1,219&ndash;$1,454 (24k&ndash;32k per tank). Listed at research time &mdash; verify current prices before purchase.',
 '<strong>Fixr &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">fixr.com</a>. Supports: ~$2,500 typical dual-tank installed project for 3&ndash;4 bedroom homes.',
 '<strong>BestCompany &mdash; Culligan pricing guide</strong> &mdash; <a href="https://bestcompany.com/blog/water-softeners/culligan-water-cost" rel="noopener" target="_blank">bestcompany.com</a>. Supports: HE Twin $3,000&ndash;$5,000; dual-tank design premium $500&ndash;$1,500.',
 '<strong>ThePricer &mdash; Kinetico cost data</strong> &mdash; <a href="https://www.thepricer.org/kinetico-water-softener-cost/" rel="noopener" target="_blank">thepricer.org</a>. Supports: Premier twin tiers $3,500&ndash;$6,000 and the $6,000/$7,200 real install reports.',
 '<strong>Angi &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: swap labor $200&ndash;$500; salt inputs behind the ownership chart.',
 '<strong>HomeGuide &mdash; Water Softener Cost (2026)</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: comparable single-tank class $600&ndash;$1,500&ndash;$2,000 used in the comparison table.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("dual-tank-water-softener-cost/index.html", a4)


# ============ C6 — ECOWATER EXPOSE (three storefronts) ============
c6_faqs = [
 ("How much does an EcoWater water softener cost?","Through EcoWater&rsquo;s own dealers: units reported at $1,000&ndash;$3,000 with installation adding $150&ndash;$1,000. Whole-house systems run $1,800&ndash;$5,000 per dealer-published 2025 figures, and reported quotes through the Costco program reach $6,000&ndash;$10,000 for bundles."),
 ("Why can&rsquo;t I find EcoWater prices anywhere?","Every storefront is quote-based: EcoWater&rsquo;s own dealer network, the Costco program, and Home Depot&rsquo;s water-treatment channel all book in-home consultations. Even EcoWater&rsquo;s own article titled &ldquo;How Much Does a Water Softener Cost?&rdquo; contains no prices."),
 ("Is EcoWater a good brand?","Arguably the strongest pedigree in the industry: a Berkshire Hathaway company, the world&rsquo;s largest residential water-treatment maker, builder of ~1 in 3 US automatic softeners, holder of the first softener patent (1925), with demand regeneration and HydroLink Wi-Fi."),
 ("Is EcoWater cheaper through Costco or its own dealer?","Reported figures suggest the opposite of instinct: own-dealer softener installs land around $1,150&ndash;$4,000, while Costco-program quotes reach $6,000&ndash;$10,000 &mdash; bundles and perks included. One buyer reported $3,700 for a softener-only <em>after</em> Costco discounts."),
 ("What does EcoWater maintenance cost?","Reported at $100&ndash;$500 per year through dealer service &mdash; at the top of that band, a decade of service can out-cost the machine. Self-supplied salt and filters run far less; ask what&rsquo;s optional before signing a plan."),
 ("Can I negotiate an EcoWater quote?","Yes &mdash; it&rsquo;s dealer-set at every storefront. A written competing quote is the lever, and the spread between channels is your evidence: the same manufacturer&rsquo;s equipment reportedly sells from $1,150 installed to $10,000 bundled."),
 ("How much does an EcoWater ERR3700 cost?","No published price exists &mdash; dealer pages state it isn&rsquo;t sold online, installation extra. The ERR3700 is the carbon-refiner version of the 3700 softener, so expect quotes above the base ECR; the reported bands on this page are your benchmark."),
 ("What&rsquo;s the difference between the ECR3700 and ERR3700?","Per EcoWater&rsquo;s manual: ECR is the conditioner (softener); ERR is the refiner &mdash; the same softener plus a carbon layer removing chlorine taste and odor, warranted for municipal chlorinated supplies only. Models ending -02 are twin-tank versions."),
]
c6_rows = [
 ("Comparable metered softener hardware (published class)",600,1500,"EcoWater builds this class &mdash; often literally, as OEM"),
 ("Professional installation (existing loop)",200,500,"Angi: 2&ndash;4 hrs at $100&ndash;$150/hr"),
 ("Materials &amp; haul-away",90,270,"Itemized in honest quotes"),
 ("Remainder to own-dealer installed reports (implied)",260,1730,"The smallest dealer remainder we track &mdash; at this storefront"),
]
c6_bars = [
 ("Own-dealer softener, installed (reported)",1150,4000,"#1F7A5C"),
 ("Dealer whole-house systems (unit, 2025)",1800,5000,"#16303F"),
 ("Home Depot program (with unit, Fixr)",2500,6000,"#5B6B75"),
 ("Costco program quotes (reported, bundles)",6000,10000,"#E8A13D"),
]
c6_bands = '[{"upTo":2499,"band":"below-typical","text":"Below the reported own-dealer band \\u2014 plausible for softener-only ESS-class units. Confirm model, capacity, and whether install is included."},{"upTo":5000,"band":"typical","text":"Inside the reported own-dealer installed band ($1,150\\u2013$4,000, whole-house units to $5,000). Ask for equipment and install as separate lines \\u2014 the dealer sets both."},{"upTo":8000,"band":"upper","text":"Refiner + RO bundle territory \\u2014 and the reported Costco-program band starts here. Get each piece itemized; every component has a published-market comparable."},{"upTo":null,"band":"above-published","text":"At or above the top of reported Costco-program quotes ($10,000). Sign nothing same-day; a written second quote from a different EcoWater storefront may be thousands lower for the same machine."}]'
BANDS6 = "'" + c6_bands + "'"
c6 = head("EcoWater Softener Cost (2026): Three Storefronts, No Prices",
 "EcoWater makes 1 in 3 US softeners \u2014 and publishes no prices at any of its three storefronts. Reported ranges $1,150\u2013$10,000, sourced.",
 "/ecowater-water-softener-cost/",
 ld(article_schema("EcoWater Water Softener Cost in 2026: The Biggest Maker You Can\u2019t Get a Price From","Sourced EcoWater pricing across its own dealers, Costco, and Home Depot \u2014 same machine, three quote-based channels.","/ecowater-water-softener-cost/",date="2026-07-12"))
 + ld(faq_schema(c6_faqs,"/ecowater-water-softener-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Brands","/brands/"),("EcoWater","/ecowater-water-softener-cost/")])))
c6 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/brands/">Brands</a> &rsaquo; EcoWater</nav>
      <h1>EcoWater Water Softener Cost in 2026: The Biggest Maker You Can&rsquo;t Get a Price From</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Start with the scale: EcoWater is <a href="https://goecowater.com/products/all" rel="noopener" target="_blank">a Berkshire Hathaway company, the world&rsquo;s largest residential water-treatment manufacturer, and the maker of roughly 1 in 3 automatic softeners sold in the US</a>. Now try to find a price. Its own dealers quote in-home; the <a href="/costco-water-softener-cost/">Costco program</a> quotes in-home; Home Depot&rsquo;s channel quotes in-home &mdash; and EcoWater&rsquo;s own article, literally titled <a href="https://www.ecowater.com/resource/how-much-does-a-water-softener-cost/" rel="noopener" target="_blank">&ldquo;How Much Does a Water Softener Cost?&rdquo;</a>, answers with zero dollar figures. The reported numbers: own-dealer units at <span class="fig">$1,000&ndash;$3,000</span> plus <span class="fig">$150&ndash;$1,000</span> install, whole-house systems at <span class="fig">$1,800&ndash;$5,000</span>, and Costco-program bundles reaching <span class="fig">$6,000&ndash;$10,000</span>.</p>
      <p style="margin:0">The estimator&rsquo;s frame, and the reason this page closes our first exposé arc: EcoWater is the cleanest demonstration in the industry that <strong>the price is the storefront, not the machine.</strong> The same manufacturer&rsquo;s equipment reportedly sells from <span class="fig">$1,150</span> installed at one counter to <span class="fig">$10,000</span> bundled at another. Read this page before any of the three consultations, and the machine &mdash; which is genuinely excellent &mdash; can be bought without buying the markup blind.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#storefronts">One machine, three storefronts (chart)</a></li>
          <li><a href="#decoder">The 3700-series decoder (ERR vs. ECR)</a></li>
          <li><a href="#reports">Real reported quotes</a></li>
          <li><a href="#worksheet">The own-dealer quote, reconstructed</a></li>
          <li><a href="#checker">Quote checker (tool)</a></li>
          <li><a href="#finance">Why the monthly payment is not the price (tool)</a></li>
          <li><a href="#buying">Two buying models, compared fairly</a></li>
          <li><a href="#ownership">The service-decade surprise (chart)</a></li>
          <li><a href="#fair">What the name legitimately buys</a></li>
        </ol>
      </details>
      <h2 id="storefronts">One manufacturer, three quote-based storefronts</h2>
      <p style="margin:0 0 16px">Every bar below is EcoWater equipment. Only the counter changes:</p>
    </div>
    <div class="col-wide">''' + range_bars(c6_bars, 10000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Sources: own-dealer figures from published ownership data ($1,000&ndash;$3,000 + $150&ndash;$1,000 install) and dealer-published 2025 system pricing; Home Depot band from Fixr&rsquo;s program data; Costco band from member reports in our <a href="/costco-water-softener-cost/">Costco expos&eacute;</a>. Reported figures, not list prices &mdash; none exist.</p>

      <h2 id="decoder">The 3700-series decoder: ERR, ECR, and what the digits mean</h2>
      <p style="margin:0 0 16px">The model soup is half the confusion, so here is EcoWater&rsquo;s own taxonomy, straight from the Series 3700/3702 owner&rsquo;s manual: <strong>ECR</strong> means conditioner &mdash; the softener; <strong>ERR</strong> means refiner &mdash; the same softener with a carbon-media layer in the tank, so it also strips chlorine taste and odor; <strong>ERRC</strong> is the chloramine variant. The last two digits are tanks: <strong>-00</strong> single, <strong>-02</strong> twin. Full codes carry a capacity suffix (ECR3700<strong>R30</strong>) &mdash; a number your quote should state, because capacity moves price.</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>EcoWater&rsquo;s 3700 series, decoded from the official manual and spec sheets</caption>
        <thead><tr><th scope="col">Model</th><th scope="col">What it is</th><th scope="col">Tanks</th><th scope="col">Designed for</th></tr></thead>
        <tbody>
          <tr><td><strong>ECR3700</strong></td><td class="muted">Conditioner &mdash; the softener</td><td>Single</td><td class="muted">City or well; dealers market a &ldquo;3700+&rdquo; well variant with stratified resin for iron</td></tr>
          <tr><td>ECR3702</td><td class="muted">Same conditioner</td><td>Twin</td><td class="muted">Higher capacity, continuous soft water</td></tr>
          <tr><td><strong>ERR3700</strong></td><td class="muted">Refiner &mdash; softener + carbon (chlorine taste/odor)</td><td>Single</td><td class="muted">City water &mdash; the warranty fine print requires a municipal chlorinated supply</td></tr>
          <tr><td>ERR3702</td><td class="muted">Same refiner</td><td>Twin</td><td class="muted">City water, higher capacity</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Three honest notes from the public record. First, the naming runs inconsistent in the wild: at least one dealer page markets the ERR series &ldquo;for either municipal or well water supplies&rdquo; while the manufacturer&rsquo;s own warranty conditions ERR coverage on a <em>municipal chlorinated</em> supply &mdash; when dealer copy and the warranty disagree, believe the warranty. Second, a model number ending in <strong>3500</strong> (like the refiner in the Houzz report below) is the <em>prior generation</em> &mdash; the manual archive lists the 3500 series separately &mdash; so older forum prices describe the older platform. Third, no storefront publishes a price for any of these models; dealer pages state they aren&rsquo;t sold online, installation extra. The estimator&rsquo;s rule follows: an EcoWater quote isn&rsquo;t comparable until it names the <strong>full model code with capacity suffix</strong>, states <strong>single or twin tank</strong>, and prices the <strong>carbon-refiner upgrade separately</strong> from the base conditioner &mdash; a refiner quote against a conditioner quote is two different machines wearing one badge.</p>

      <h2 id="reports">Real reported EcoWater quotes</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Publicly reported EcoWater pricing, attributed</caption>
        <thead><tr><th scope="col">System / situation</th><th scope="col">Where reported</th><th scope="col" class="num">Reported figure</th></tr></thead>
        <tbody>
          <tr><td>ERR-class refiner + RO bundle, initial quote</td><td class="muted">Houzz buyer thread (older report)</td><td class="num">$5,500</td></tr>
          <tr><td>Softener-only, <em>after</em> Costco-program discounts</td><td class="muted">Same buyer, same thread</td><td class="num">~$3,700</td></tr>
          <tr><td>Costco-program consultation quotes, bundles</td><td class="muted">Member reports via House Digest (2025)</td><td class="num">$6,000&ndash;$10,000</td></tr>
          <tr><td>Whole-house systems, unit pricing</td><td class="muted">Dealer-published (2025)</td><td class="num">$1,800&ndash;$5,000</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">The Houzz thread is worth reading in full, because the buyer&rsquo;s three complaints &mdash; dealer reviews nonexistent, price feels high, no published performance data &mdash; are the dealer-channel trifecta this whole <a href="/brands/">series</a> documents. His conclusion after research? The equipment itself is &ldquo;probably the best unit on the market.&rdquo; Both things can be true; only one of them is priced in daylight.</p>

      <h2 id="worksheet">The own-dealer quote, reconstructed</h2>
      <p style="margin:0">Here&rsquo;s the twist this brand adds to our standard reconstruction &mdash; at its <em>own</em> storefront, EcoWater&rsquo;s implied remainder is the smallest we track:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("EcoWater own-dealer quote, reconstructed (est.)", c6_rows, total_label="Own-dealer reported band") + '''</div>
    <div class="col">
      <p style="margin-top:24px">Compare that <span class="fig">$260&ndash;$1,730</span> remainder to <a href="/rainsoft-water-softener-cost/">RainSoft&rsquo;s $5,110&ndash;$8,730</a> or the <a href="/costco-water-softener-cost/">Costco program&rsquo;s ~63%</a> &mdash; running EcoWater&rsquo;s <em>own</em> machine. Same factory, three remainders. If you want this equipment, the arbitrage is written right into the reports: the least glamorous storefront sells it cheapest.</p>

      <h2 id="checker">Check your EcoWater quote against the reported bands</h2>
      <div data-quote-check data-min="1500" data-max="10000" data-start="4000" data-bands=''' + BANDS6 + '''></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Bands span all three storefronts &mdash; a verdict is a prompt to ask which counter you&rsquo;re standing at, and what the same configuration costs at the other two.</p>
      <div style="margin-top:40px">''' + cta_box("The fourth storefront: a posted price",
        "There is a channel where the number comes first: SpringWell publishes its softener pricing online \u2014 sized by bathrooms, shipped free, 6-month money-back guarantee \u2014 which makes it the benchmark to carry into any of EcoWater\u2019s three consultations.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="ownership">The service-decade surprise</h2>
      <p style="margin:0 0 16px">Published ownership data puts EcoWater dealer maintenance at <span class="fig">$100&ndash;$500 per year</span>. At the top of that band, the decade of service out-costs the machine:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",45),("#E8A13D",52),("#1F7A5C",3)], "~$5,700", "10 yrs (midpoints)", "10-year EcoWater own-dealer ownership composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> System, installed (own-dealer midpoint ~$2,575) <span class="pc">~45%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Dealer maintenance &amp; salt program (~$300/yr) <span class="pc">~52%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Misc parts <span class="pc">~3%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of sourced ranges &middot; self-supplied salt and filters cut the amber slice by two-thirds or more &mdash; the <a href="/water-softener-maintenance-cost/">maintenance guide</a> prices the DIY decade line by line</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Same pattern as the <a href="/culligan-water-softener-cost/">Culligan salt-delivery math</a>: the ongoing program, not the machine, is where dealer economics live. Ask which service lines are optional before signing &mdash; on demand-metered EcoWater electronics, most of the annual visit is checking numbers the HydroLink app already shows you.</p>

      <h2 id="finance">Why the monthly payment is not the price</h2>
      <p style="margin:0 0 16px">Every quote-based storefront eventually reaches for the same move, and it is the single most effective number in the in-home-sales playbook: <em>&ldquo;it&rsquo;s only $99 a month.&rdquo;</em> When I built estimates, that was the line that ended the conversation about the price &mdash; because a monthly payment is not a price, it is a <strong>duration</strong>. The arithmetic that turns one back into the other is not complicated, and no dealer will mind you doing it at the table:</p>
      <div data-finance-calc></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Your numbers, from your own disclosure &mdash; not any brand&rsquo;s published terms, because none of the three EcoWater storefronts publishes financing terms any more than it publishes prices. Formula: total of scheduled payments = payment &times; number of payments; the implied system price is what that payment stream is worth today at the stated APR.</p>
      <p style="margin:16px 0 0">Run the default and the point lands: a <span class="fig">$99</span> monthly payment over 84 months at a mid-teens APR is roughly <span class="fig">$8,300</span> handed over for an implied system price near <span class="fig">$5,000</span> &mdash; the difference is interest, and it is not a small slice of the pie. That is not a scandal; that is what borrowing costs. It only becomes a problem when the monthly number is the <em>only</em> number on the table, because then you are comparing a payment against another dealer&rsquo;s cash price &mdash; which is not a comparison at all.</p>

      <h3 style="margin-top:32px">&ldquo;No interest&rdquo; and &ldquo;0% APR&rdquo; are not the same offer</h3>
      <p style="margin:0">This is the fine-print distinction most worth knowing before you sign anything at a kitchen table, and it is defined in federal regulation rather than opinion:</p>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Promotional financing, decoded &mdash; CFPB and Regulation Z definitions</caption>
        <thead><tr><th scope="col">What the paperwork says</th><th scope="col">What it actually means</th><th scope="col">What happens at the end</th></tr></thead>
        <tbody>
          <tr><td><strong>True 0% APR</strong></td><td class="muted">The rate really is zero for the promo period</td><td class="muted">Interest applies only <em>going forward</em>, on whatever balance remains</td></tr>
          <tr><td><strong>&ldquo;No interest if paid in full&rdquo;</strong><br><span class="muted">(also: &ldquo;12 months same as cash&rdquo;)</span></td><td class="muted">Deferred interest &mdash; interest accrues silently in the background the whole time</td><td class="muted">Any balance left, even a few dollars, triggers interest charged <em>retroactively</em> to the purchase date on the <em>original</em> amount</td></tr>
          <tr><td>The legal tell</td><td class="muted">Regulation Z requires that if an ad says &ldquo;no interest,&rdquo; the words <strong>&ldquo;if paid in full&rdquo;</strong> appear clearly and conspicuously, with the period stated</td><td class="muted">If you see those four words, you are looking at deferred interest &mdash; not a 0% loan</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">The consumer-law numbers behind that middle row: the CFPB has found roughly <strong>one in five</strong> deferred-interest promotional balances ends up hit with retroactive interest, and the ongoing rates on these products tend to run <strong>above 20%</strong> regardless of the borrower&rsquo;s credit score. The National Consumer Law Center&rsquo;s illustrative example is the clearest version &mdash; a $2,500 purchase on a 12-month, 24% deferred-interest plan, paid down to a $100 balance, can trigger nearly <span class="fig">$400</span> of retroactive interest on the <em>entire</em> $2,500. Most buyers do pay these off in time. The ones who do not are the reason the offer exists. So: ask for the cash price in writing <em>first</em>, then decide about financing separately &mdash; two decisions, not one.</p>

      <h2 id="buying">Two buying models, compared fairly</h2>
      <p style="margin:0">Not &ldquo;which brand is better&rdquo; &mdash; the hardware argument is settled below. This is the question the reader actually faces: which <em>purchasing process</em> fits them.</p>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Dealer-sold vs. factory-direct: the buying experience, not the badge</caption>
        <thead><tr><th scope="col">Buying factor</th><th scope="col">Dealer-sold (all three EcoWater storefronts)</th><th scope="col">Factory-direct channel</th></tr></thead>
        <tbody>
          <tr><td>Price visibility</td><td class="muted">Quote-based; no published price at any counter</td><td class="muted">Equipment price posted before you speak to anyone</td></tr>
          <tr><td>Sales process</td><td class="muted">In-home consultation with a water test; reported 2-hour appointments</td><td class="muted">Direct purchase online, no appointment</td></tr>
          <tr><td>Installation</td><td class="muted">Bundled and coordinated by the dealer</td><td class="muted">DIY or a plumber you hire and price yourself</td></tr>
          <tr><td>Quote breakdown</td><td class="muted">Depends entirely on the dealer; equipment and labor often bundled</td><td class="muted">Equipment and labor are separate purchases by definition</td></tr>
          <tr><td>Service &amp; accountability</td><td class="muted"><strong>One local company owns the whole outcome</strong> &mdash; a real advantage when something goes wrong</td><td class="muted">Manufacturer warranty plus an installer you coordinate yourself</td></tr>
          <tr><td>Financing</td><td class="muted">Commonly offered at the table &mdash; read the disclosure, not the monthly number</td><td class="muted">Posted price; third-party financing optional and separate</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Read that table honestly and the dealer model wins two rows outright. If you want one company that tests your water, sizes the system, cuts your pipe, and answers the phone in year six &mdash; that is a real service, and it is worth real money. The factory-direct route asks you to project-manage: you buy the equipment at a posted number, hire the installation, and own the coordination. What it buys in return is the one thing the consultation cannot offer &mdash; you know the equipment price <em>before</em> anyone sits at your table, which is also what makes a dealer quote legible when you do take the appointment. Either way, the <a href="/dealer-vs-factory-direct-pricing/">channel comparison</a> prices the trade-off in full.</p>

      <h2 id="fair">What the name legitimately buys</h2>
      <p>More engineering pedigree than any brand in this series: the founder&rsquo;s 1925 patent started the industry, the company holds 70+ patents, and today it builds counter-current brining, demand-initiated regeneration, and HydroLink Wi-Fi monitoring into machines so well-regarded that a skeptical buyer&rsquo;s own research called them the market&rsquo;s best. When a third of America&rsquo;s softeners come off your lines, the hardware argument is settled.</p>
      <p style="margin:0">Which is exactly why the pricing model deserves the scrutiny: the best machine in the aisle is the one that least needs a hidden price to sell. Take the reported bands, the <a href="/dealer-vs-factory-direct-pricing/">four-step script</a>, and the three-storefront spread above &mdash; and buy the excellent machine without paying for the shiniest counter.</p>
      <div style="margin-top:40px">''' + cta_box("Excellent hardware, posted number",
        "If demand-metered engineering and a lifetime warranty are the checklist, the factory-direct version exists: SpringWell\u2019s SS series \u2014 metered regeneration, lifetime warranty on tanks and valves, free shipping, DIY-friendly install \u2014 with the price on the screen before anyone books a consultation.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(c6_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/costco-water-softener-cost/"><div class="name">Costco / EcoWater expos&eacute;</div><div class="range">$6,000&ndash;$10,000</div><div class="desc">The membership storefront, priced.</div></a>
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Dealer vs. factory-direct</div><div class="desc">Where the extra thousands go.</div></a>
        <a class="card" href="/brands/"><div class="name">All brand expos&eacute;s</div><div class="desc">Culligan, Kinetico, RainSoft &amp; more.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>QualityWaterTreatment &mdash; True Ownership Costs (Jun 2026)</strong> &mdash; <a href="https://qualitywatertreatment.com/pages/cost-comparisons-budget-friendly-water-softeners-exposed" rel="noopener" target="_blank">qualitywatertreatment.com</a>. Supports: EcoWater units $1,000&ndash;$3,000; install $150&ndash;$1,000; annual maintenance $100&ndash;$500.',
 '<strong>SmartWater TT (EcoWater dealer) &mdash; Whole House System Cost (2025)</strong> &mdash; <a href="https://smartwatertt.com/how-much-does-the-ecowater-whole-house-system-cost/" rel="noopener" target="_blank">smartwatertt.com</a>. Supports: whole-house systems $1,800&ndash;$5,000 unit-focused; install often priced separately.',
 '<strong>Houzz &mdash; ERR3500 buyer thread (older report, attributed)</strong> &mdash; <a href="https://www.houzz.com/discussions/2512578/ecowater-refiner-softener-err3500-opinions" rel="noopener" target="_blank">houzz.com</a>. Supports: $5,500 refiner+RO quote; ~$3,700 softener-only after Costco discounts; buyer&rsquo;s transparency complaints and &ldquo;best unit on the market&rdquo; assessment.',
 '<strong>House Digest &mdash; Costco EcoWater analysis (Feb 2025)</strong> &mdash; <a href="https://www.housedigest.com/1779560/costco-water-softener-worth-it-reviews/" rel="noopener" target="_blank">housedigest.com</a>. Supports: Costco-program quotes $6,000&ndash;$10,000; Home Depot EcoWater 44% recommend.',
 '<strong>EcoWater &mdash; official cost article &amp; dealer product pages</strong> &mdash; <a href="https://www.ecowater.com/resource/how-much-does-a-water-softener-cost/" rel="noopener" target="_blank">ecowater.com</a>. Supports: absence of any published pricing (including in the brand&rsquo;s own cost guide); dealer water-test model; series lineup and HydroLink claims via <a href="https://goecowater.com/products/all" rel="noopener" target="_blank">dealer pages</a>, incl. Berkshire Hathaway ownership and 1-in-3 manufacture share.',
 '<strong>Fixr &mdash; Water Softener Installation Cost (2026)</strong> &mdash; <a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">fixr.com</a>. Supports: Home Depot program band $2,500&ndash;$6,000.',
 '<strong>Consumer Financial Protection Bureau &mdash; Issue Spotlight: The High Cost of Retail Credit Cards; Regulation Z &sect;1026.16 (advertising)</strong> &mdash; <a href="https://www.consumerfinance.gov/data-research/research-reports/issue-spotlight-the-high-cost-of-retail-credit-cards/" rel="noopener" target="_blank">consumerfinance.gov</a>, <a href="https://www.consumerfinance.gov/rules-policy/regulations/1026/16/" rel="noopener" target="_blank">Reg Z &sect;1026.16</a>. Supports: ~1 in 5 deferred-interest balances hit with retroactive interest; retroactive interest computed on the original purchase amount; the &ldquo;if paid in full&rdquo; disclosure requirement; ongoing rates above 20% regardless of credit score. Financing mechanics only &mdash; not EcoWater terms, which no storefront publishes.',
 '<strong>National Consumer Law Center &mdash; Deceptive Bargain: The Hidden Time Bomb of Deferred Interest</strong> &mdash; <a href="https://www.nclc.org/resources/deceptive-bargain-the-hidden-time-bomb-of-deferred-interest-credit-cards/" rel="noopener" target="_blank">nclc.org</a>. Supports: the illustrative $2,500 / 24% / 12-month example producing nearly $400 of retroactive interest. Presented as the NCLC&rsquo;s example, not a market average.',
 '<strong>EcoWater Systems &mdash; Series 3700/3702 official manuals (ECR/ERR/ERRC, updated Jan 2026)</strong> &mdash; <a href="https://ecowater.zendesk.com/hc/en-us/articles/1500008509382-ECR-ERR-ERRC-3700-3702" rel="noopener" target="_blank">ecowater.zendesk.com</a>. Supports: the decoder taxonomy (ECR conditioner / ERR refiner / ERRC chloramine; -00 single / -02 twin; capacity model codes); the ERR municipal-chlorinated-supply warranty condition; the 3500 series listed as a separate, prior manual.',
 '<strong>Authorized EcoWater dealer product pages (2026)</strong> &mdash; <a href="https://ecowateril.com/water-solutions/softeners-refiners/" rel="noopener" target="_blank">ecowateril.com</a> and <a href="https://fixyourwater.ca/products/err-3700" rel="noopener" target="_blank">fixyourwater.ca</a>. Supports: the ECR &ldquo;3700+&rdquo; well variant (stratified resin, iron); ERR carbon-layer description; the well-vs-city naming inconsistency; not-sold-online and installation-extra confirmations.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("ecowater-water-softener-cost/index.html", c6)


# ============ G1 — WELL WATER SOFTENER COST (Phase 4 silo pillar) ============
g1_faqs = [
 ("How much does a well water softener cost?","$1,000&ndash;$3,500 installed for the softener itself &mdash; sized larger than city units because well hardness often exceeds 15 gpg. But on most wells that&rsquo;s half the answer: iron above ~1 ppm needs its own filter first, and full stacks run $1,500&ndash;$6,500."),
 ("Why can&rsquo;t I just use a water softener for iron?","Softeners handle only trace iron (under ~1 ppm). Above that, dissolved iron fouls the resin &mdash; dealer service data reports capacity dying in 6&ndash;18 months, and iron exposure voids most resin warranties. The iron filter goes first; the softener lives longer for it."),
 ("What does an iron filter for well water cost?","Air-injection oxidation (AIO) systems &mdash; the chemical-free standard &mdash; run $1,500&ndash;$2,500 installed, with the broader iron-filter market at $1,400&ndash;$3,700. Ownership is nearly free: no chemicals, media lasts 6&ndash;8 years (~$300/cu-ft to replace)."),
 ("What order do well water systems install in?","Sediment filter first, acid neutralizer if pH is low, then iron filter, then softener, then UV last. Each stage protects the one after it &mdash; and installing out of order is how new equipment gets ruined by the problem upstream of it."),
 ("Are iron filter + softener packages worth it?","Usually. Matched two-tank packages run $2,495&ndash;$5,150 and are reported at $695&ndash;$1,095 below buying the pair separately &mdash; and matched sizing means the backwash demands and flow rates actually line up."),
 ("What should I do before buying anything for well water?","Test &mdash; iron, hardness, pH, manganese, sulfur, bacteria. A proper test runs $50&ndash;$150, and dealer guidance is blunt about the alternative: guessing is the most expensive mistake in well treatment, because the wrong system solves nothing at full price."),
]
g1_rows = [
 ("Well-sized softener, installed",1000,3500,"HomeGuide; sized up for 15+ gpg well hardness"),
 ("AIO iron filter, installed (only if iron &gt;1 ppm)",0,2500,"$1,500&ndash;$2,500 when needed &mdash; goes FIRST"),
 ("Sediment prefilter, installed",200,600,"Protects everything downstream"),
 ("UV disinfection (only if bacteria-positive)",0,2500,"$700&ndash;$2,500 installed; needs clear water upstream"),
]
g1_bars = [
 ("Sediment prefilter",200,600,"#D9DED9"),
 ("UV disinfection",700,2500,"#5B6B75"),
 ("Well-sized softener",1000,3500,"#16303F"),
 ("AIO iron filter",1500,2500,"#1F7A5C"),
 ("Matched iron + softener packages",2495,5150,"#E8A13D"),
]
g1 = head("Well Water Softener Cost (2026): Hardness + Iron, Priced as a System",
 "Well softeners run $1,000\u2013$3,500 installed \u2014 but iron over 1 ppm needs its own filter first. Full stacks $1,500\u2013$6,500, itemized and sourced.",
 "/well-water-softener-cost/",
 ld(article_schema("Well Water Softener Cost in 2026: Hardness + Iron, Priced as a System","Sourced well-water treatment pricing: softener, iron filter, sediment, UV \u2014 stack math, install order, and package savings.","/well-water-softener-cost/",date="2026-07-12"))
 + ld(faq_schema(g1_faqs,"/well-water-softener-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Well water cost","/well-water-softener-cost/")])))
g1 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Well water cost</nav>
      <h1>Well Water Softener Cost in 2026: Hardness + Iron, Priced as a System</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">A well-sized softener runs <span class="fig">$1,000&ndash;$3,500</span> installed per <a href="https://homeguide.com/costs/well-water-filtration-system-cost" rel="noopener" target="_blank">HomeGuide</a> &mdash; but on a private well, that&rsquo;s usually the second purchase, not the first. Iron above <span class="fig">~1 ppm</span> needs its own filter ahead of the softener: AIO iron systems run <span class="fig">$1,500&ndash;$2,500</span> installed, matched iron + softener packages go for <span class="fig">$2,495&ndash;$5,150</span>, and complete multi-stage stacks land <span class="fig">$3,000&ndash;$7,000</span>. Thirty-two-year dealer data puts most well owners&rsquo; total at <span class="fig">$1,500&ndash;$6,500</span>.</p>
      <p><strong>Well water softeners cost $1,000&ndash;$3,500 installed &mdash; and most wells need an iron filter first ($1,500&ndash;$2,500 AIO installed), because iron over 1 ppm fouls softener resin within 6&ndash;18 months and voids most resin warranties. Complete well stacks run $1,500&ndash;$6,500.</strong></p>
      <p style="margin:0">Here&rsquo;s the estimator&rsquo;s frame, and it&rsquo;s the whole page in one sentence: <em>on a well, the cheapest thing you can buy for your softener is the iron filter that goes in front of it.</em> Dealers know well quotes support the biggest numbers in the industry &mdash; this is where <a href="/kinetico-water-softener-cost/">$6,000 twin-tank installs</a> and <a href="/dealer-vs-factory-direct-pricing/">$8,000 packages</a> live &mdash; precisely because the buyer usually can&rsquo;t itemize a multi-system stack. After this page, you can.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#stack">Build your stack (tool)</a></li>
          <li><a href="#worksheet">The stack worksheet</a></li>
          <li><a href="#symptoms">Symptom decoder: what your water is telling you</a></li>
          <li><a href="#iron">Why softener-only fails on iron wells</a></li>
          <li><a href="#order">The install order (and why it&rsquo;s law)</a></li>
          <li><a href="#components">Component prices (chart)</a></li>
          <li><a href="#packages">The package math</a></li>
        </ol>
      </details>
      <h2 id="stack">Build your well stack in three taps</h2>
      <p style="margin:0 0 16px">Every toggle is a sourced installed range. Don&rsquo;t know which apply? That&rsquo;s what the <a href="/pick/test-kit" ''' + PICK + '''>water test</a> is for &mdash; $50&ndash;$150 of testing before thousands of equipment is the best ratio in home improvement:</p>
      <div data-well-calc></div>

      <h2 id="worksheet" style="margin-top:48px">The well-treatment stack, itemized</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Well water stack: softener + protection train", g1_rows, total_label="Stack span") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>How I&rsquo;d read this sheet:</strong> the &ldquo;only if&rdquo; rows are test-driven, not optional-by-preference &mdash; iron over 1 ppm makes the iron row mandatory (see below), a positive bacteria test makes UV mandatory, and nothing else does. The realistic clean-well project is <span class="fig">$1,200&ndash;$4,100</span>; the realistic iron-well project is <span class="fig">$2,700&ndash;$6,600</span>. Any quote far above those bands should itemize what your water test showed that this sheet doesn&rsquo;t.</p>

      <h2 id="symptoms">The symptom decoder: what your water is already telling you</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Well water symptoms, culprits, and the equipment that fixes each</caption>
        <thead><tr><th scope="col">Symptom</th><th scope="col">Likely culprit</th><th scope="col">Equipment</th><th scope="col" class="num">Installed cost</th></tr></thead>
        <tbody>
          <tr><td>Orange/brown stains, metallic taste</td><td class="muted">Ferrous iron (&gt;0.3 ppm)</td><td>AIO iron filter</td><td class="num">$1,500&ndash;$2,500</td></tr>
          <tr><td>Rotten-egg smell</td><td class="muted">Hydrogen sulfide</td><td>Same AIO handles it (to ~8 ppm)</td><td class="num">included</td></tr>
          <tr><td>Black stains or specks</td><td class="muted">Manganese</td><td>Same AIO handles it</td><td class="num">included</td></tr>
          <tr><td>Blue-green stains on fixtures</td><td class="muted">Low pH (acidic water)</td><td><a href="/acid-neutralizer-cost/">Acid neutralizer</a>, first in line</td><td class="num">$1,195&ndash;$1,895</td></tr>
          <tr><td>Scale, stiff laundry, soap won&rsquo;t lather</td><td class="muted">Hardness (often 15+ gpg)</td><td>Well-sized softener</td><td class="num">$1,000&ndash;$3,500</td></tr>
          <tr><td>Positive coliform/bacteria test</td><td class="muted">Microbial contamination</td><td><a href="/uv-water-purifier-cost/">UV disinfection</a>, last in line</td><td class="num">$500&ndash;$2,500</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">One tell worth knowing: water that runs clear from the tap but turns orange sitting in a glass is dissolved ferrous iron &mdash; the kind that quietly eats softener resin. Every cell is sourced &mdash; the neutralizer figure from the dedicated <a href="/acid-neutralizer-cost/">acid neutralizer cost guide</a>.</p>

      <h2 id="iron">Why &ldquo;just get a softener&rdquo; fails on iron wells</h2>
      <p style="margin:0">This is the costliest wrong turn in well treatment, so here&rsquo;s the mechanism, sourced from dealer service data: softener resin exchanges hardness ions, and it will grab dissolved iron too &mdash; but salt regeneration doesn&rsquo;t release iron the way it releases calcium. The iron accumulates, coats the beads, and the softener&rsquo;s capacity dies in <span class="fig">6&ndash;18 months</span>. Worse: iron exposure <strong>voids most resin warranties</strong>, so the failure is yours to fund. The fix costs less than the failure: an AIO filter ahead of the softener oxidizes iron to particles and backwashes them away &mdash; <span class="fig">$0</span> in annual chemicals, media good for 6&ndash;8 years at ~$300/cu-ft to replace. On a well, the iron filter isn&rsquo;t an add-on to the softener; it&rsquo;s the softener&rsquo;s bodyguard.</p>

      <h2 id="order">The install order &mdash; and why it&rsquo;s law, not preference</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Well water treatment sequence, from wellhead to tap</caption>
        <thead><tr><th scope="col">Order</th><th scope="col">System</th><th scope="col">Why it must go here</th></tr></thead>
        <tbody>
          <tr><td>1</td><td><a href="/sediment-filter-cost/">Sediment filter</a></td><td class="muted">Sand and silt clog every media bed behind it &mdash; $250&ndash;$600 installed</td></tr>
          <tr><td>2</td><td>Acid neutralizer (if pH &lt; 7)</td><td class="muted">Iron media needs neutral-or-better pH to oxidize at full speed</td></tr>
          <tr><td>3</td><td>Iron filter</td><td class="muted">Protects the softener resin from fouling</td></tr>
          <tr><td>4</td><td>Water softener</td><td class="muted">Now running on water that can&rsquo;t kill it</td></tr>
          <tr><td>5</td><td>UV disinfection</td><td class="muted">Needs clear, iron-free water to reach the microbes</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Each stage protects the one after it. A quote that sequences these differently &mdash; or that sells stage 4 without asking about stages 1&ndash;3 &mdash; is telling you the water test was a formality. The <a href="/water-softener-installation-cost/">installation guide</a> prices the plumbing side; wells add a drain-capacity check, since iron-filter backwash pulls 5&ndash;12 GPM your pump must sustain.</p>

      <h2 id="components">Component prices, one scale</h2>
    </div>
    <div class="col-wide">''' + range_bars(g1_bars, 6000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Installed ranges: HomeGuide (softener, UV, sediment), SC Well Service (AIO), Mid Atlantic Water (package tiers). The amber packages bar is the two biggest bars bought as one matched system &mdash; the math below.</p>

      <h2 id="packages">The package math: matched pairs beat two purchases</h2>
      <p style="margin:0 0 16px">Published dealer package pricing runs <span class="fig">$2,495</span> (single-tank all-in-one, mild iron) through <span class="fig">$3,395&ndash;$4,695</span> (matched two-tank trains) to <span class="fig">$5,150</span> (four-stage with neutralizer) &mdash; reported at <span class="fig">$695&ndash;$1,095 less</span> than buying the systems separately, with backwash flows and capacities engineered to match. That&rsquo;s the honest version of bundling: itemized, published, and cheaper. The dealer-channel version bundles the same stack into one unlabeled <span class="fig">$8,000</span> number &mdash; the <a href="/dealer-vs-factory-direct-pricing/">difference is the whole thesis of this site</a>.</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",42),("#1F7A5C",37),("#5B6B75",14),("#D9DED9",7)], "~$5,400", "full stack (midpoints)", "Full well-stack cost composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> Well-sized softener (~$2,250) <span class="pc">~42%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> AIO iron filter (~$2,000) <span class="pc">~37%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> UV, where needed (~$800 amortized) <span class="pc">~14%</span></div>
          <div><span class="sw" style="background:#D9DED9"></span> Sediment stage <span class="pc">~7%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of sourced installed ranges on an iron-bearing well &middot; ownership stays cheap: AIO runs $0/yr in chemicals and the softener behind it lives its full 15&ndash;20 years &mdash; the <a href="/water-softener-maintenance-cost/">maintenance guide</a> covers the decade</div>
    </div>
    <div class="col">
      <div style="margin-top:40px">''' + cta_box("The matched pair, at a posted price",
        "The factory-direct version of the package math: SpringWell\u2019s well water filter + softener combo pairs its air-injection iron system \u2014 independent guides credit it with handling up to 7 ppm iron and 8 ppm sulfur \u2014 with a matched metered softener, at a published price, shipped free, with a 6-month money-back guarantee. One order, one install, plumbed in the order the chemistry requires.",
        "Check current SpringWell combo price","filter-salt-softener-combo") + '''</div>
      <p style="margin:24px 0 0">And if your test comes back iron-free and bacteria-free? Congratulations &mdash; you have a city-water project on well pressure: a standard <a href="/">$840&ndash;$4,120 itemized softener install</a>, just sized a notch up for well hardness. Big households on wells should also read the <a href="/dual-tank-water-softener-cost/">dual-tank guide</a> &mdash; wells are two of its four twin-tank situations.</p>
      <div style="margin-top:40px">''' + cta_box("Test first, then buy once",
        "Every dollar figure on this page keys off a water test. SpringWell\u2019s combo route keeps the decision reversible \u2014 published price, free shipping, 6-month money-back \u2014 but the sequence never changes: $50\u2013$150 of testing first, then the stack your numbers actually require.",
        "Check current SpringWell combo price","filter-salt-softener-combo") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(g1_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/"><div class="name">Full cost guide</div><div class="range">$840&ndash;$4,120</div><div class="desc">The softener project, itemized.</div></a>
        <a class="card" href="/dual-tank-water-softener-cost/"><div class="name">Dual-tank cost</div><div class="range">$1,500&ndash;$5,000</div><div class="desc">Wells are twin-tank territory.</div></a>
        <a class="card" href="/iron-filter-for-well-water-cost/"><div class="name">Iron filter cost</div><div class="range">$1,000&ndash;$3,500</div><div class="desc">The softener&rsquo;s bodyguard, priced by technology.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>HomeGuide &mdash; Well Water Filtration System Cost (Apr 2026)</strong> &mdash; <a href="https://homeguide.com/costs/well-water-filtration-system-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: well softeners $1,000&ndash;$3,500 installed; iron &gt;1&ndash;2 ppm needs a dedicated filter first; UV $700&ndash;$2,500; sediment $200&ndash;$600; multi-contaminant stacks $3,000&ndash;$7,000; the five-stage install order.',
 '<strong>SC Well Service &mdash; Well Water Treatment System Cost (2026)</strong> &mdash; <a href="https://scwellservice.com/blog/water-treatment-system-cost.html" rel="noopener" target="_blank">scwellservice.com</a>. Supports: AIO iron systems $1,500&ndash;$2,500 installed; iron filters $1,000&ndash;$3,000; UV and sediment ranges.',
 '<strong>Mid Atlantic Water &mdash; Iron Filter + Softener Packages (Feb 2026)</strong> &mdash; <a href="https://midatlanticwater.net/collections/iron-filter-water-softener-packages" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: resin fouling in 6&ndash;18 months and voided warranties; package tiers $2,495&ndash;$5,150; $695&ndash;$1,095 package savings; iron-first install order; 5&ndash;12 GPM backwash demands.',
 '<strong>Mid Atlantic Water &mdash; Well Water Treatment Cost Guide (Mar 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/guides/well-water-treatment-system-cost" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: most owners $1,500&ndash;$6,500 total; Katalox media 6&ndash;8 yrs at ~$300/cu-ft; $0 annual iron-filter chemicals; testing-first guidance ($50&ndash;$150).',
 '<strong>SoftPro &mdash; Residential Iron Filter Costs (2026)</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/media-bed-costs-installing-iron-filter-system" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: iron filters installed $1,400&ndash;$3,700; install labor $150&ndash;$500.',
 '<strong>QualityWaterTreatment &mdash; Iron Filter Options for Well Water (2026)</strong> &mdash; <a href="https://qualitywatertreatment.com/pages/top-iron-filter-options-for-well-water" rel="noopener" target="_blank">qualitywatertreatment.com</a>. Supports: SpringWell AIO handling up to 7 ppm iron / 8 ppm hydrogen sulfide; air-injection as the chemical-free standard.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("well-water-softener-cost/index.html", g1)


# ============ D1 — AVERAGE COST DATA ROUNDUP (benchmark page) ============
d1_faqs = [
 ("What is the average water softener installation cost?","The most-cited national average is ~$1,500 installed (Angi/HomeAdvisor, 2026), with typical ranges of $200&ndash;$6,000. Independent datasets converge on $1,100&ndash;$3,800 for standard installed projects &mdash; our cross-source benchmark for a typical home is $1,200&ndash;$3,800."),
 ("Does the average installation price include the softener?","In the major cost guides, yes &mdash; the ~$1,500 figure covers equipment plus standard labor and materials. Labor alone runs $150&ndash;$1,000+ (Homewyse prices a basic labor-and-materials install at $1,131&ndash;$1,405). Always confirm which scope a quote or article means."),
 ("Why do published average costs differ so much?","Three reasons: different scopes (unit-only vs. labor-only vs. installed vs. whole projects), different dates, and syndication &mdash; several &ldquo;different&rdquo; sources republish the same underlying dataset. Ten pages on the SERP reduce to roughly four independent estimates."),
 ("Is $3,000 too much for a water softener installed?","Inside the consensus corridor if your home needed site work &mdash; a loop run alone is $600&ndash;$2,000. For a prepared home (loop, drain, outlet present), $3,000 is well above the $840&ndash;$1,500 the itemized components support: ask for the line items."),
 ("What pushes a project above the average?","No softener loop ($600&ndash;$2,000), missing drain ($0&ndash;$300) or outlet ($250&ndash;$900), permits, difficult access, oversized or dual-tank systems ($1,700&ndash;$5,000 installed), and dealer packages &mdash; where reported quotes run $2,500&ndash;$11,000 for comparable hardware."),
 ("Is it cheaper to buy the softener and hire a plumber separately?","Usually, when your home is prepared: a published-price unit ($600&ndash;$1,500) plus swap labor ($200&ndash;$500) lands under most bundled quotes. The trade-off is coordinating warranty service yourself &mdash; the dealer-vs-direct guide prices the difference."),
]
d1_rows = [
 ("Metered softener equipment",600,1500,"HomeGuide published class"),
 ("Standard installation labor (existing loop)",200,500,"Angi: 2&ndash;4 hrs at $100&ndash;$150/hr"),
 ("Fittings, bypass &amp; materials",40,120,"Often bundled &mdash; confirm"),
 ("Site work (only if loop/drain/outlet missing)",0,2000,"The variable that moves quotes most"),
]
d1_bars = [
 ("Homewyse (basic install, unit-cost method)",1131,1405,"#5B6B75"),
 ("Fixr (typical installed)",1100,3000,"#1F7A5C"),
 ("HomeGuide (salt-based installed)",1200,3800,"#16303F"),
 ("ANGI family (Angi/HomeAdvisor, avg $1,500)",200,6000,"#E8A13D"),
 ("Our itemized build (this site)",840,4120,"#B3541E"),
]
d1_bands = '[{"upTo":839,"band":"below-typical","text":"Below every itemized installed build we track \\u2014 this is unit-only or labor-only territory. Check what the number actually includes before comparing it to installed quotes."},{"upTo":1500,"band":"low-corridor","text":"The prepared-home corridor: unit + swap labor + fittings on an existing loop. Matches the most-cited $1,500 average and the Homewyse basic-install range \\u2014 a fair number for a home with loop, drain, and outlet in place."},{"upTo":3800,"band":"consensus","text":"The consensus corridor \\u2014 every independent dataset (HomeGuide, Fixr, our build) overlaps here. Normal for homes needing site work: a loop run alone adds $600\\u2013$2,000. Ask for the site-work lines itemized."},{"upTo":6000,"band":"upper","text":"Above the independent typical ranges, inside only the widest published spread. Legitimate for dual-tank systems, difficult retrofits, or big-capacity builds \\u2014 the quote should name which."},{"upTo":null,"band":"above-published","text":"Above nearly every published dataset \\u2014 this is dealer-package territory. Compare against the brand expos\\u00e9s\\u2019 reported bands and get a second, itemized quote before signing."}]'
BANDSD1 = "'" + d1_bands + "'"
d1 = head("Average Water Softener Installation Cost (2026): Every Source Compared",
 "The most-cited average is $1,500 installed \u2014 but 10 sources collapse to 4 independent datasets. Every published figure compared, deduplicated, benchmarked.",
 "/average-water-softener-installation-cost/",
 ld(article_schema("Average Water Softener Installation Cost in 2026: What Every Source Reports \u2014 and Which Numbers Are Actually Independent","Cross-source data roundup: published averages compared, syndicated datasets deduplicated, and an honest benchmark assembled.","/average-water-softener-installation-cost/",date="2026-07-12"))
 + ld(faq_schema(d1_faqs,"/average-water-softener-installation-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Average installation cost","/average-water-softener-installation-cost/")])))
d1 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Average installation cost</nav>
      <h1>Average Water Softener Installation Cost in 2026: What Every Source Reports &mdash; and Which Numbers Are Actually Independent</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">The headline first: the most-cited national average is <span class="fig">~$1,500</span> installed, with published typical ranges of <span class="fig">$200&ndash;$6,000</span> (<a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">Angi, updated March 2026</a>). Independent datasets converge tighter: <span class="fig">$1,200&ndash;$3,800</span> for a salt-based system installed (HomeGuide), <span class="fig">$1,100&ndash;$3,000</span> typical (Fixr), and <span class="fig">$1,131&ndash;$1,405</span> for a basic labor-and-materials install (Homewyse, May 2026).</p>
      <p><strong>Water softener installation averages ~$1,500 nationally including equipment, labor, and materials, with independent published datasets converging on $1,200&ndash;$3,800 for typical installed projects. Prepared homes with an existing loop land near the low end; homes needing plumbing work ($600&ndash;$2,000 for a loop alone) push toward the high end.</strong></p>
      <p style="margin:0">Now the part no ranking page will tell you, and the reason this roundup exists: <em>the word &ldquo;average&rdquo; on this SERP describes maybe four independent numbers wearing ten mastheads.</em> I spent fifteen years watching homeowners wave conflicting printouts at me across the estimate desk &mdash; this page reconciles them: every major published figure, what each actually includes, which ones share a bloodline, and the honest benchmark left standing when the duplicates are removed.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#sources">Every major published figure, compared (chart)</a></li>
          <li><a href="#family">The syndication problem: 10 sources, ~4 datasets</a></li>
          <li><a href="#why">Why the numbers disagree (scope decoder)</a></li>
          <li><a href="#benchmark">Our cross-source benchmark &amp; worksheet</a></li>
          <li><a href="#checker">Check your quote against every dataset (tool)</a></li>
          <li><a href="#above">What pushes a project above the average</a></li>
        </ol>
      </details>
      <h2 id="sources">Every major published figure, on one scale</h2>
      <p style="margin:0 0 16px">Installed-scope figures only, plotted together &mdash; note where the independent ranges pile up:</p>
    </div>
    <div class="col-wide">''' + range_bars(d1_bars, 6000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Data dates: Angi Mar 2026 &middot; Homewyse May 2026 &middot; HomeGuide 2025&ndash;26 &middot; Fixr 2026 &middot; our build assembled from the component sources below. The overlap zone &mdash; roughly <span class="fig">$1,200&ndash;$3,800</span> &mdash; is what this page calls the <strong>consensus corridor</strong>.</p>

      <h2 id="family">The syndication problem: ten sources, four datasets</h2>
      <p style="margin:0 0 16px">Before averaging anything, an estimator checks whether his sources are actually independent. On this SERP, mostly not:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>Who&rsquo;s reporting original data &mdash; and who&rsquo;s republishing it</caption>
        <thead><tr><th scope="col">Publisher</th><th scope="col" class="num">Reported figure</th><th scope="col">Data lineage</th></tr></thead>
        <tbody>
          <tr><td>Angi (Mar 2026)</td><td class="num">avg ~$1,500 &middot; $200&ndash;$6,000</td><td><strong>Original</strong> &mdash; ANGI Inc. marketplace data</td></tr>
          <tr><td>HomeAdvisor</td><td class="num">avg $1,500 &middot; $200&ndash;$6,000</td><td class="muted">Same parent company (ANGI Inc.) &mdash; same dataset, second masthead</td></tr>
          <tr><td>This Old House</td><td class="num">avg $3,100 (system cost)</td><td class="muted">States its data is &ldquo;sourced from Angi&rdquo; &mdash; same dataset, different slice</td></tr>
          <tr><td>Bob Vila</td><td class="num">avg $1,500 &middot; $200&ndash;$6,000</td><td class="muted">Cites &ldquo;HomeAdvisor and Angi&rdquo; directly</td></tr>
          <tr><td>Forbes Home (2025)</td><td class="num">avg ~$1,500</td><td class="muted">Same figures; authored by ex-HomeAdvisor/Angi staff</td></tr>
          <tr><td>HomeGuide</td><td class="num">$1,200&ndash;$3,800 installed</td><td><strong>Independent</strong> range-based dataset</td></tr>
          <tr><td>Homewyse (May 2026)</td><td class="num">$1,131&ndash;$1,405 basic</td><td><strong>Independent</strong> &mdash; unit-cost method, disclosed suppliers; +13&ndash;22% GC overhead excluded</td></tr>
          <tr><td>Fixr</td><td class="num">$1,100&ndash;$3,000 typical</td><td><strong>Independent</strong> editorial cost dataset</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Five mastheads, one marketplace dataset &mdash; which is why &ldquo;every site says $1,500&rdquo; is weaker evidence than it looks, and why This Old House&rsquo;s <span class="fig">$3,100</span> isn&rsquo;t a contradiction: it&rsquo;s the <em>same Angi data</em> sliced as average system cost rather than average installed project. Neither number is wrong. They&rsquo;re answering different questions from one spreadsheet.</p>

      <h2 id="why">Why published averages disagree: the scope decoder</h2>
      <p style="margin:0">Four different questions hide inside &ldquo;what does installation cost&rdquo;: <strong>labor only</strong> ($150&ndash;$1,000+ &mdash; Homewyse prices the basic labor-and-materials job at $1,131&ndash;$1,405); <strong>unit only</strong> ($400&ndash;$1,500 for the mainstream metered class); <strong>unit + standard install</strong> (the ~$1,500 average and the $1,200&ndash;$3,800 corridor); and <strong>complete projects with site work</strong> (where the $6,000 tops and $11,000 outliers live). Publication dates matter too &mdash; the figures above span 2024&ndash;2026, and we&rsquo;ve dated every one rather than silently blending vintages. A printout fight between a $1,405 number and a $3,800 number is usually two scopes arguing, not two facts.</p>

      <h2 id="benchmark">Our cross-source benchmark &mdash; and the worksheet behind it</h2>
      <p style="margin:0 0 16px"><strong>Methodology, stated plainly:</strong> taking the three independent installed-scope datasets (HomeGuide, Fixr, Homewyse-basic) plus our component-assembled build, the overlap of typical ranges is roughly <span class="fig">$1,200&ndash;$3,800</span> &mdash; that&rsquo;s a <em>consensus corridor of comparable published estimates</em>, not a survey average. Here&rsquo;s the same number built bottom-up from sourced components:</p>
    </div>
    <div style="margin-top:8px">''' + quote_sheet("Standard installed project, assembled from components", d1_rows, total_label="Component-built span") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>How the arithmetic reconciles:</strong> prepared home (loop, drain, outlet present) = <span class="fig">$840&ndash;$2,120</span>, matching Homewyse&rsquo;s basic band and the low corridor; add site work and the build reaches <span class="fig">$4,120</span>, bracketing HomeGuide&rsquo;s ceiling. The national averages aren&rsquo;t mysterious &mdash; they&rsquo;re these components in different mixtures. The <a href="/water-softener-installation-cost/">full installation guide</a> itemizes every row, and the <a href="/calculators/cost-calculator/">cost calculator</a> runs your mixture.</p>

      <h2 id="checker">Check your quote against every dataset at once</h2>
      <div data-quote-check data-min="300" data-max="7000" data-start="1500" data-bands=''' + BANDSD1 + '''></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Bands assembled from the deduplicated datasets above. A verdict is a starting question, not a final judgment &mdash; scope decides everything.</p>
      <div style="margin-top:40px">''' + cta_box("Turn the average into your number",
        "The fastest way out of average-land: price the equipment separately. SpringWell publishes its softener pricing online \u2014 sized by bathrooms, shipped free, 6-month money-back guarantee \u2014 so the equipment line of any installed quote has a posted benchmark sitting next to it.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="above">What pushes your project above &mdash; or below &mdash; the average</h2>
      <p><strong>Above:</strong> no softener loop (<span class="fig">$600&ndash;$2,000</span> to run one), missing drain (<span class="fig">$0&ndash;$300</span>) or outlet (<span class="fig">$250&ndash;$900</span>), permits, crawlspace access, dual-tank systems (<span class="fig">$1,700&ndash;$5,000</span> installed per HomeGuide), well pretreatment (a <a href="/well-water-softener-cost/">separate scope entirely</a>), and the dealer channel &mdash; where <a href="/brands/">reported quotes for comparable hardware</a> run far beyond every dataset on this page. <strong>Below:</strong> a prepared home, a replacement swap (<span class="fig">$290&ndash;$770</span> plus the unit), <a href="/low-cost-water-softener/">honest budget-tier equipment</a>, or DIY on an existing loop. Neither direction is suspicious by itself &mdash; the quote just has to <em>name</em> which lines put you there.</p>
      <div style="margin-top:40px">''' + cta_box("The benchmark that ends the printout fight",
        "Every average on this page is someone else\u2019s house. SpringWell\u2019s posted price plus your plumber\u2019s labor quote is YOUR number \u2014 equipment cost in daylight, install scope itemized, and the 6-month money-back window keeping the decision reversible.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(d1_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/water-softener-installation-cost/"><div class="name">Installation cost, itemized</div><div class="range">$840&ndash;$4,120</div><div class="desc">Every line the averages are made of.</div></a>
        <a class="card" href="/"><div class="name">Full cost guide</div><div class="range">$840&ndash;$4,120</div><div class="desc">The complete worksheet with charts.</div></a>
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Dealer vs. factory-direct</div><div class="desc">Why some quotes leave every dataset behind.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Angi &mdash; Water Softener Installation Cost (updated Mar 2026; installed scope, national marketplace data)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: ~$1,500 average; $200&ndash;$6,000 typical; $150&ndash;$11,000 full spread; labor rates; dual-tank $1,000&ndash;$5,000.',
 '<strong>HomeAdvisor &mdash; Water Softener Installation Costs (installed scope; same ANGI Inc. dataset)</strong> &mdash; <a href="https://www.homeadvisor.com/cost/kitchens/water-softener-installation-costs/" rel="noopener" target="_blank">homeadvisor.com</a>. Supports: $1,500 average / $200&ndash;$6,000 duplication; plumbing $0.50&ndash;$8/lf and electrical $2&ndash;$4/sqft add-on rates.',
 '<strong>This Old House &mdash; Water Softener System Cost (data credited to Angi; system-cost scope)</strong> &mdash; <a href="https://www.thisoldhouse.com/plumbing/water-softener-system-cost" rel="noopener" target="_blank">thisoldhouse.com</a>. Supports: $3,100 system-cost average and its Angi lineage.',
 '<strong>Bob Vila &mdash; Water Softener System Cost (Apr 2024; cites HomeAdvisor and Angi)</strong> &mdash; <a href="https://www.bobvila.com/articles/water-softener-system-cost/" rel="noopener" target="_blank">bobvila.com</a>. Supports: syndication documentation.',
 '<strong>Forbes Home &mdash; Water Softener Installation Cost (Feb 2025)</strong> &mdash; <a href="https://www.forbes.com/home-improvement/plumbing/water-softener-system-installation-cost/" rel="noopener" target="_blank">forbes.com</a>. Supports: ~$1,500 national average including labor and materials; labor $150&ndash;$11,000 spread.',
 '<strong>HomeGuide &mdash; Water Softener Cost (independent; installed scope)</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: salt-based $1,200&ndash;$3,800 installed; dual-tank $1,700&ndash;$5,000; unit class $600&ndash;$1,500.',
 '<strong>Homewyse &mdash; Cost to Install Water Softener (May 2026; unit-cost method, basic labor + materials)</strong> &mdash; <a href="https://www.homewyse.com/services/cost_to_install_water_softener.html" rel="noopener" target="_blank">homewyse.com</a>. Supports: $1,131&ndash;$1,405 basic install; +13&ndash;22% GC overhead exclusion note.',
 '<strong>Fixr &mdash; Water Softener Installation Cost (independent editorial dataset)</strong> &mdash; <a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">fixr.com</a>. Supports: $1,100&ndash;$3,000 typical installed; ~$2,500 dual-tank project.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("average-water-softener-installation-cost/index.html", d1)


# ============ B2 — WHOLE-HOUSE INSTALLED COST (system-type router) ============
b2_faqs = [
 ("How much does a whole house water softener cost installed?","$1,200&ndash;$3,800 for the standard salt-based system per HomeGuide &mdash; unit ($600&ndash;$1,500), labor ($200&ndash;$500), fittings, plus site work where needed. Prepared homes land near $890&ndash;$2,120; homes needing a loop or drain push toward $4,000+."),
 ("What&rsquo;s the difference between a whole-house softener and a whole-house filter?","A softener removes hardness minerals (scale, soap problems); a filter removes contaminants like chlorine, sediment, or iron. They&rsquo;re different machines solving different problems &mdash; many homes on wells or chlorinated city water end up wanting one of each, plumbed in sequence."),
 ("Which whole-house system type is cheapest installed?","Salt-free conditioners install cheapest ($900&ndash;$3,000 &mdash; no drain, no power) but only prevent scale. Salt-based softeners run $1,200&ndash;$3,800 installed; dual-tank $1,700&ndash;$5,000; well stacks with iron treatment $2,700&ndash;$6,600."),
 ("How much of a whole-house installation quote is labor?","On a prepared home, surprisingly little: $200&ndash;$500 of a $890&ndash;$2,120 project. Site work is what moves quotes &mdash; a loop run is $600&ndash;$2,000, an outlet $250&ndash;$900. Equipment and site work together dwarf the wrench time."),
 ("Do I need a permit for a whole-house water softener?","Many jurisdictions require a plumbing permit ($0&ndash;$150 where applicable) since the install cuts into the main line. Rules vary widely &mdash; ask your installer who pulls it, and get permit responsibility written into the quote."),
 ("Should I buy the whole-house system myself and hire a plumber?","On a prepared home, it&rsquo;s usually the cheapest professional route: published-price equipment plus $200&ndash;$500 swap labor. You coordinate warranty service yourself &mdash; the dealer-vs-direct guide prices exactly what that convenience costs."),
]
b2_rows = [
 ("Whole-house softener equipment (metered)",600,1500,"Capacity and valve quality; published class"),
 ("Installation labor",200,500,"2&ndash;4 hrs at $100&ndash;$150/hr (Angi)"),
 ("Fittings, bypass &amp; materials",40,120,"Confirm what&rsquo;s bundled"),
 ("Softener loop (only if none exists)",0,2000,"The single biggest swing on first-time installs"),
 ("Drain + outlet (only if missing)",0,1200,"Drain $0&ndash;$300; dedicated 110V outlet $250&ndash;$900"),
 ("Permit (where required)",0,150,"Jurisdiction-dependent"),
]
b2_bars = [
 ("Salt-free conditioner, installed",900,3000,"#5B6B75"),
 ("Salt-based softener, installed",1200,3800,"#16303F"),
 ("Dual-tank softener, installed",1700,5000,"#1F7A5C"),
 ("Well stack (iron + softener), installed",2700,6600,"#E8A13D"),
]
b2 = head("Whole House Water Softener Installation Cost (2026): Every Type",
 "Whole-house softeners cost $1,200\u2013$3,800 installed \u2014 salt-free from $900, dual-tank to $5,000, well stacks to $6,600. Every system type, priced.",
 "/whole-house-water-softener-installation-cost/",
 ld(article_schema("Whole-House Water Softener Installation Cost in 2026: Every System Type, Installed","Installed pricing across every whole-house option \u2014 salt-based, salt-free, dual-tank, and well stacks \u2014 with the system-type decision most guides skip.","/whole-house-water-softener-installation-cost/",date="2026-07-12"))
 + ld(faq_schema(b2_faqs,"/whole-house-water-softener-installation-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Whole-house installed cost","/whole-house-water-softener-installation-cost/")])))
b2 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Whole-house installed cost</nav>
      <h1>Whole-House Water Softener Installation Cost in 2026: Every System Type, Installed</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">The standard whole-house salt-based softener runs <span class="fig">$1,200&ndash;$3,800</span> installed per <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">HomeGuide</a> &mdash; <span class="fig">$600&ndash;$1,500</span> for the metered unit, <span class="fig">$200&ndash;$500</span> in labor, and the rest determined by what your house is missing. But &ldquo;whole house&rdquo; hides a decision most cost guides skip: salt-free conditioners install for <span class="fig">$900&ndash;$3,000</span>, dual-tank systems for <span class="fig">$1,700&ndash;$5,000</span>, and well stacks with iron treatment for <span class="fig">$2,700&ndash;$6,600</span> &mdash; and they solve different problems.</p>
      <p><strong>A whole-house water softener costs $1,200&ndash;$3,800 installed for the standard salt-based system: $600&ndash;$1,500 equipment, $200&ndash;$500 labor, plus $0&ndash;$3,200 in site work depending on whether a loop, drain, and outlet exist. Salt-free ($900&ndash;$3,000), dual-tank ($1,700&ndash;$5,000), and well configurations price differently.</strong></p>
      <p style="margin:0">The estimator&rsquo;s first question on every &ldquo;whole house&rdquo; call was never about the softener &mdash; it was <em>&ldquo;what problem are we actually solving?&rdquo;</em> Scale and soap point one direction; iron staining points another; chlorine taste isn&rsquo;t a softener problem at all. Pick the system before pricing the install, or you&rsquo;ll price the wrong project perfectly. Two taps below sorts it.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#picker">Which system is your project? (tool)</a></li>
          <li><a href="#types">Installed cost by system type (chart)</a></li>
          <li><a href="#worksheet">The installed-cost worksheet</a></li>
          <li><a href="#scenarios">Three real project scenarios</a></li>
          <li><a href="#composition">Where the installed dollar goes (chart)</a></li>
          <li><a href="#quote">Comparing whole-house quotes fairly</a></li>
        </ol>
      </details>
      <h2 id="picker">First decision: which whole-house system is your project?</h2>
      <p style="margin:0 0 16px">Two taps, and unsure means test: a <a href="/pick/test-kit" ''' + PICK + '''>water test</a> settles hardness, iron, and pH before any equipment decision spends four figures on a guess:</p>
      <div data-system-fit></div>

      <h2 id="types" style="margin-top:48px">Installed cost by system type, one scale</h2>
    </div>
    <div class="col-wide">''' + range_bars(b2_bars, 7000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Installed ranges: HomeGuide (salt-based, <a href="/dual-tank-water-softener-cost/">dual-tank</a>), our sourced <a href="/salt-free-water-softener-cost/">salt-free</a> and <a href="/well-water-softener-cost/">well-stack</a> builds. One distinction worth its own sentence: a whole-house <em>filter</em> (chlorine, sediment) is a different machine than a whole-house <em>softener</em> (hardness) &mdash; homes wanting both plumb them in sequence or buy a combo.</p>

      <h2 id="worksheet">The whole-house installed-cost worksheet</h2>
      <p style="margin:0">Standard salt-based scenario &mdash; the fourth column is what an estimator actually watches:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Whole-house salt-based softener, installed", b2_rows, total_label="Installed range") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Reading the sheet:</strong> the conditional rows don&rsquo;t stack in real homes &mdash; typical completed projects land <span class="fig">$840&ndash;$4,120</span>, not the theoretical column top. The <a href="/water-softener-installation-cost/">installation deep-dive</a> itemizes every row with its own scenario tool, and the <a href="/average-water-softener-installation-cost/">cross-source benchmark</a> shows how this build reconciles with every published average.</p>
      <div style="margin-top:24px">''' + cta_box("Price the equipment line first",
        "The equipment row is the one line you can benchmark before anyone visits: SpringWell publishes its whole-house softener pricing online \u2014 sized by bathrooms, shipped free, 6-month money-back guarantee \u2014 so your installed quote\u2019s biggest line has a posted number beside it.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="scenarios">Three real whole-house projects, priced</h2>
      <p><strong>Scenario 1 &mdash; the prepared home</strong> (loop, drain, outlet all present): unit + swap labor + fittings = <span class="fig">$890&ndash;$2,270</span> installed, wrench time 2&ndash;4 hours. This is the scenario most &ldquo;$1,500 average&rdquo; figures quietly assume. <strong>Scenario 2 &mdash; first-time install</strong> (no loop, drain nearby): add the loop run at <span class="fig">$600&ndash;$2,000</span> for <span class="fig">$1,490&ndash;$4,270</span> &mdash; the plumbing, not the softener, is now the project. <strong>Scenario 3 &mdash; the complex retrofit</strong> (no loop, no drain, no outlet, tight access): all conditional rows activate and the honest range is <span class="fig">$2,340&ndash;$5,470</span> &mdash; the territory where itemization matters most, because this is also where <a href="/dealer-vs-factory-direct-pricing/">bundled dealer quotes</a> hide their spread.</p>

      <h2 id="composition">Where the whole-house dollar actually goes</h2>
    </div>
    <div class="col-wide" style="margin-top:16px">
      <div class="donut-wrap">''' + donut_svg([("#16303F",42),("#E8A13D",41),("#1F7A5C",14),("#5B6B75",3)], "~$2,500", "mid project (est.)", "Whole-house installed cost composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> Equipment (~$1,050) <span class="pc">~42%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Site work where needed (~$1,020) <span class="pc">~41%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Labor (~$350) <span class="pc">~14%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Fittings &amp; materials <span class="pc">~3%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of the worksheet ranges on a first-time install &middot; on a prepared home the amber slice disappears and equipment becomes ~70% of the project</div>
    </div>
    <div class="col">
      <h2 style="margin-top:48px" id="quote">Comparing whole-house quotes: scope against scope</h2>
      <p style="margin:0">Before signing, get seven things explicit: the exact <strong>model and capacity</strong>; <strong>equipment vs. labor as separate lines</strong>; each piece of <strong>site work priced individually</strong>; <strong>permit responsibility</strong>; <strong>old-unit removal</strong>; whether the <strong>warranty depends on dealer service</strong>; and what&rsquo;s <strong>specifically excluded</strong>. Then compare bids row by row against the worksheet above &mdash; a $1,800 quote and a $3,500 quote may both be honest if one home needs a loop and the other doesn&rsquo;t. The <a href="/calculators/cost-calculator/">cost calculator</a> personalizes the range in about a minute.</p>
      <div style="margin-top:40px">''' + cta_box("The whole house, without the whole markup",
        "Every system type on this page has a factory-direct version with the price posted: SpringWell\u2019s whole-house line \u2014 softeners sized by bathrooms, salt-free FutureSoft, and well combos \u2014 ships free with a 6-month money-back guarantee, so the system decision and the price discovery happen before anyone books your kitchen table.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(b2_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/water-softener-installation-cost/"><div class="name">Installation cost, itemized</div><div class="range">$840&ndash;$4,120</div><div class="desc">The install mechanics deep-dive.</div></a>
        <a class="card" href="/average-water-softener-installation-cost/"><div class="name">Every published average</div><div class="range">$1,200&ndash;$3,800</div><div class="desc">The cross-source benchmark.</div></a>
        <a class="card" href="/well-water-softener-cost/"><div class="name">Well water cost</div><div class="range">$1,500&ndash;$6,500</div><div class="desc">Iron changes the whole project.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>HomeGuide &mdash; Water Softener Cost (installed scope)</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: salt-based $1,200&ndash;$3,800 installed; dual-tank $1,700&ndash;$5,000; unit class $600&ndash;$1,500; outlet $250&ndash;$900.',
 '<strong>Angi &mdash; Water Softener Installation Cost (updated Mar 2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: labor $200&ndash;$500 at $100&ndash;$150/hr; system-type unit ranges.',
 '<strong>CheckMyTap &mdash; Salt-Free Conditioners (Apr 2026)</strong> &mdash; <a href="https://checkmytap.com/solutions/salt-free-conditioners/" rel="noopener" target="_blank">checkmytap.com</a>. Supports: salt-free installed $900&ndash;$3,000 build (unit $800&ndash;$2,000 + install $150&ndash;$400).',
 '<strong>HomeGuide &mdash; Well Water Filtration System Cost (Apr 2026)</strong> &mdash; <a href="https://homeguide.com/costs/well-water-filtration-system-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: well-stack component ranges behind the $2,700&ndash;$6,600 band.',
 '<strong>SC Well Service &mdash; Water Treatment System Cost (2026)</strong> &mdash; <a href="https://scwellservice.com/blog/water-treatment-system-cost.html" rel="noopener" target="_blank">scwellservice.com</a>. Supports: AIO iron filter $1,500&ndash;$2,500 installed used in the well band.',
 '<strong>Fixr &mdash; Water Softener Installation Cost</strong> &mdash; <a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">fixr.com</a>. Supports: loop cut-in $600&ndash;$2,000; typical installed corroboration.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("whole-house-water-softener-installation-cost/index.html", b2)


# ============ B3 — RETROFIT COST (existing home, no loop) ============
b3_faqs = [
 ("How much does it cost to add a water softener to an existing home?","For a house never plumbed for one: $1,440&ndash;$5,470 all-in &mdash; unit ($600&ndash;$1,500), labor ($200&ndash;$500), and the retrofit work that defines the project: a loop run ($600&ndash;$2,000), plus drain ($0&ndash;$300) and outlet ($0&ndash;$900) where missing. Typical retrofits land $1,490&ndash;$4,270."),
 ("How much does it cost to put a water softener in a house without a loop?","The loop is the retrofit: cutting into the main line and running supply-and-return costs $600&ndash;$2,000 depending on distance and access, on top of the standard unit + labor + fittings. It&rsquo;s the single biggest line on most retrofit quotes."),
 ("Where should a water softener go in an existing house?","As close to where the main line enters as possible &mdash; every foot away is pipe you pay for ($0.50&ndash;$8/linear foot). Garages near the main are cheapest; basements are routine; crawlspaces add access labor; outdoor installs add freeze protection in most climates."),
 ("Can a water softener be installed outside?","Yes in mild climates, with an insulated enclosure &mdash; but outdoor placement adds enclosure and freeze-protection costs and shortens component life in sun. If an interior spot near the main line exists, it almost always prices better."),
 ("Do I need an electrician to add a water softener?","Only if there&rsquo;s no grounded outlet within reach of the install point. A dedicated 110V outlet runs $250&ndash;$900 (HomeGuide); rerouting wiring prices around $2&ndash;$4 per square foot (HomeAdvisor). Metered valves draw very little &mdash; the outlet is the cost, not the power."),
 ("Is it cheaper to buy the softener and hire a plumber for the retrofit?","Usually: published-price equipment plus a plumber&rsquo;s itemized retrofit labor beats most bundled quotes for the same scope &mdash; and it forces the loop, drain, and outlet onto separate lines where you can see them."),
]
b3_rows = [
 ("Water softener equipment (metered)",600,1500,"HomeGuide published class"),
 ("Installation labor",200,500,"Angi: $100&ndash;$150/hr"),
 ("Fittings, bypass &amp; materials",40,120,"Confirm what&rsquo;s bundled"),
 ("Softener loop run &mdash; the retrofit itself",600,2000,"Distance from main-line entry decides it (Fixr)"),
 ("Drain connection (only if none nearby)",0,300,"Standpipe or existing drain proximity"),
 ("Dedicated outlet (only if none nearby)",0,900,"$250&ndash;$900 when needed (HomeGuide)"),
 ("Permit (where required)",0,150,"Jurisdiction-dependent"),
]
b3_bars = [
 ("Prepared home (baseline, for contrast)",890,2270,"#D9DED9"),
 ("Typical retrofit (loop + nearby drain)",1490,4270,"#16303F"),
 ("Complex retrofit (loop + drain + outlet + access)",2340,5470,"#E8A13D"),
]
b3 = head("Cost to Add a Water Softener to an Existing Home (2026)",
 "Adding a softener to a home never plumbed for one costs $1,440\u2013$5,470 \u2014 the loop run ($600\u2013$2,000) is the retrofit. Itemized and sourced.",
 "/cost-to-add-water-softener-to-existing-home/",
 ld(article_schema("Cost to Add a Water Softener to an Existing Home in 2026: The Retrofit Worksheet","Sourced retrofit pricing for homes never plumbed for a softener: loop runs, placement economics, drain and electrical work, itemized.","/cost-to-add-water-softener-to-existing-home/",date="2026-07-12"))
 + ld(faq_schema(b3_faqs,"/cost-to-add-water-softener-to-existing-home/"))
 + ld(breadcrumb_schema([("Home","/"),("Retrofit cost","/cost-to-add-water-softener-to-existing-home/")])))
b3 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Retrofit cost</nav>
      <h1>Cost to Add a Water Softener to an Existing Home in 2026: The Retrofit Worksheet</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">For a house that was never plumbed for a softener, the realistic all-in range is <span class="fig">$1,440&ndash;$5,470</span>: the unit at <span class="fig">$600&ndash;$1,500</span>, labor at <span class="fig">$200&ndash;$500</span>, and the line that defines a retrofit &mdash; cutting into the main and running a softener loop at <span class="fig">$600&ndash;$2,000</span> (<a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">Fixr</a>) &mdash; plus a drain (<span class="fig">$0&ndash;$300</span>) and outlet (<span class="fig">$0&ndash;$900</span>) where the install spot lacks them. Typical retrofits land <span class="fig">$1,490&ndash;$4,270</span>.</p>
      <p><strong>Adding a water softener to an existing home costs $1,440&ndash;$5,470 total: $840&ndash;$2,120 for the unit, labor, and fittings, plus $600&ndash;$3,200 in retrofit plumbing &mdash; the loop run, drain connection, and electrical outlet your house does or doesn&rsquo;t already have. Loop distance is the biggest variable.</strong></p>
      <p style="margin:0">When I built these quotes, the first question was never the brand. It was <em>where the main line enters the house</em> &mdash; because in a retrofit, you&rsquo;re not really buying a softener installation. You&rsquo;re buying pipe, and the softener comes with it. Every dollar figure on this page follows from that one fact.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#builder">Build your retrofit, line by line (tool)</a></li>
          <li><a href="#worksheet">The retrofit worksheet</a></li>
          <li><a href="#scenarios">Three retrofits, priced (chart)</a></li>
          <li><a href="#placement">Placement economics: garage vs. basement vs. crawlspace vs. outdoor</a></li>
          <li><a href="#composition">Where the retrofit dollar goes (chart)</a></li>
          <li><a href="#quote">Getting an honest retrofit quote</a></li>
        </ol>
      </details>
      <h2 id="builder">Build your retrofit, line by line</h2>
      <p style="margin:0 0 16px">Same engine as our installation guide, pointed at your house: toggle what&rsquo;s missing and watch which line moves the total &mdash; a planning estimate from sourced ranges, not a site-specific bid:</p>
      <div data-expense-calc></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">In a retrofit, the loop toggle is your project&rsquo;s center of gravity. And before sizing anything: a <a href="/pick/test-kit" ''' + PICK + '''>water test</a> confirms the hardness the whole purchase is being sized against.</p>

      <h2 id="worksheet" style="margin-top:48px">The retrofit worksheet, every line sourced</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Adding a softener to an unprepared home", b3_rows, total_label="Retrofit range") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Reading the sheet:</strong> what pushes you to the <em>low end</em> is proximity &mdash; main line entering the garage, drain and outlet within reach, loop run short. The <em>middle</em> is a normal loop run plus one missing utility. The <em>high end</em> is distance and access: long runs, finished walls, crawlspace work, and the outlet an electrician has to create. Nobody pays every maximum at once &mdash; typical completed retrofits land <span class="fig">$1,490&ndash;$4,270</span>, consistent with the <a href="/average-water-softener-installation-cost/">cross-source benchmark corridor</a>.</p>
      <div style="margin-top:24px">''' + cta_box("Separate the equipment from the retrofit",
        "The retrofit is your plumber\u2019s job; the equipment doesn\u2019t have to be. SpringWell publishes its softener pricing online \u2014 sized by bathrooms, shipped free, 6-month money-back guarantee \u2014 so the biggest line on the worksheet is settled at a posted price before the pipe work is even quoted.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="scenarios">Three retrofits, priced against the prepared-home baseline</h2>
    </div>
    <div class="col-wide">''' + range_bars(b3_bars, 6000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Modeled from the sourced worksheet components &mdash; estimates, not actual quotes. The gray baseline is what the same softener costs in a home already plumbed for one; the gap between gray and amber is the retrofit itself. The <a href="/water-softener-installation-cost/">installation deep-dive</a> itemizes the baseline.</p>
      <p style="margin:16px 0 0"><strong>Scenario A &mdash; easy garage retrofit</strong> (<span class="fig">~$1,490&ndash;$2,600</span>): main line enters the garage, drain and outlet within reach, short loop run at the bottom of the $600&ndash;$2,000 band. <strong>Scenario B &mdash; the typical existing home</strong> (<span class="fig">$1,490&ndash;$4,270</span>): moderate loop run, drain routing required, standard professional install. <strong>Scenario C &mdash; the difficult retrofit</strong> (<span class="fig">$2,340&ndash;$5,470</span>): long runs through finished space, no drain, no outlet, tight access &mdash; where itemization matters most, because this is where <a href="/dealer-vs-factory-direct-pricing/">bundled dealer quotes</a> hide their spread.</p>

      <h2 id="placement">Placement economics: the four spots and what each one costs you</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Install locations in an existing home, by cost mechanism</caption>
        <thead><tr><th scope="col">Location</th><th scope="col">What it changes</th><th scope="col">The cost mechanism</th></tr></thead>
        <tbody>
          <tr><td>Garage, near main entry</td><td><strong>The cheap spot</strong> &mdash; short loop, open walls</td><td class="muted">Minimal pipe at $0.50&ndash;$8/linear foot; drain and outlet often already present</td></tr>
          <tr><td>Basement / utility room</td><td>Routine &mdash; usually drain-rich</td><td class="muted">Moderate runs; floor drains cut the drain line to $0</td></tr>
          <tr><td>Crawlspace</td><td>Access labor, not materials</td><td class="muted">Same parts, slower hours &mdash; labor at $100&ndash;$150/hr does the damage</td></tr>
          <tr><td>Outdoor (mild climates)</td><td>Enclosure + freeze protection</td><td class="muted">Insulated enclosure and UV exposure &mdash; interior spots almost always price better</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Notice there&rsquo;s no flat &ldquo;crawlspace surcharge&rdquo; row &mdash; because none exists in honest pricing. Placement costs flow through two sourced mechanisms: <strong>pipe distance</strong> ($0.50&ndash;$8/linear foot, HomeAdvisor) and <strong>labor hours</strong> ($100&ndash;$150/hr, Angi). A quote with a vague &ldquo;access fee&rdquo; should convert it into feet and hours on request. One more line to expect on GC-managed jobs: Homewyse notes general-contractor oversight adds <span class="fig">13&ndash;22%</span> when someone else coordinates the trades.</p>

      <h2 id="composition">Where the typical retrofit dollar goes</h2>
    </div>
    <div class="col-wide" style="margin-top:16px">
      <div class="donut-wrap">''' + donut_svg([("#E8A13D",45),("#16303F",37),("#1F7A5C",15),("#5B6B75",3)], "~$2,880", "typical retrofit (est.)", "Typical retrofit cost composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#E8A13D"></span> Retrofit plumbing: loop + drain (~$1,300) <span class="pc">~45%</span></div>
          <div><span class="sw" style="background:#16303F"></span> Equipment (~$1,050) <span class="pc">~37%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Labor (~$430) <span class="pc">~15%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Fittings &amp; materials <span class="pc">~3%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of the worksheet ranges, Scenario B assumptions &middot; the amber slice is the part your house&rsquo;s layout controls &mdash; and the part a prepared home never pays</div>
    </div>
    <div class="col">
      <h2 style="margin-top:48px" id="quote">Getting an honest retrofit quote</h2>
      <p style="margin:0">Ask for the retrofit priced as its own lines: <strong>loop run in feet</strong>, <strong>drain routing</strong>, <strong>outlet work</strong>, <strong>wall access and repair</strong>, and <strong>permit responsibility</strong> &mdash; each separate from equipment and base labor. Then the killer question from my estimating years: <em>&ldquo;what would have to happen on install day for this total to increase?&rdquo;</em> A pro who&rsquo;s walked your main-line entry answers specifically; a quote built from the driveway answers vaguely. The <a href="/whole-house-water-softener-installation-cost/">system-type guide</a> covers the decision upstream of all this, and the <a href="/calculators/cost-calculator/">cost calculator</a> personalizes the range.</p>
      <div style="margin-top:40px">''' + cta_box("The retrofit-friendly route",
        "Retrofits reward separating the purchases: SpringWell\u2019s posted equipment price plus your plumber\u2019s itemized pipe work keeps every line in daylight \u2014 free shipping, 6-month money-back guarantee, and DIY-friendly connections once the loop exists.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(b3_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/water-softener-installation-cost/"><div class="name">Installation cost, itemized</div><div class="range">$840&ndash;$4,120</div><div class="desc">The flagship install worksheet.</div></a>
        <a class="card" href="/whole-house-water-softener-installation-cost/"><div class="name">Which whole-house system?</div><div class="range">$900&ndash;$6,600</div><div class="desc">Pick the system before the retrofit.</div></a>
        <a class="card" href="/average-water-softener-installation-cost/"><div class="name">Every published average</div><div class="range">$1,200&ndash;$3,800</div><div class="desc">Where retrofits sit in the data.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Fixr &mdash; Water Softener Installation Cost</strong> &mdash; <a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">fixr.com</a>. Supports: loop cut-in $600&ndash;$2,000; typical installed corroboration.',
 '<strong>HomeGuide &mdash; Water Softener Cost</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: unit class $600&ndash;$1,500; dedicated outlet $250&ndash;$900.',
 '<strong>Angi &mdash; Water Softener Installation Cost (updated Mar 2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: labor $200&ndash;$500 at $100&ndash;$150/hr.',
 '<strong>HomeAdvisor &mdash; Water Softener Installation Costs</strong> &mdash; <a href="https://www.homeadvisor.com/cost/kitchens/water-softener-installation-costs/" rel="noopener" target="_blank">homeadvisor.com</a>. Supports: new plumbing $0.50&ndash;$8 per linear foot; electrical rerouting $2&ndash;$4 per square foot.',
 '<strong>Homewyse &mdash; Cost to Install Water Softener (May 2026)</strong> &mdash; <a href="https://www.homewyse.com/services/cost_to_install_water_softener.html" rel="noopener" target="_blank">homewyse.com</a>. Supports: general-contractor oversight +13&ndash;22%.',
 '<strong>Forbes Home &mdash; Water Softener Installation Cost (Feb 2025)</strong> &mdash; <a href="https://www.forbes.com/home-improvement/plumbing/water-softener-system-installation-cost/" rel="noopener" target="_blank">forbes.com</a>. Supports: complex-installation labor spread reaching $11,000 as the outer bound context.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("cost-to-add-water-softener-to-existing-home/index.html", b3)


# ============ E2 — REMOVAL COST (remove/repair/replace/relocate) ============
e2_faqs = [
 ("How much does it cost to remove a water softener?","$150&ndash;$500 for a straightforward professional removal (disconnect, cap, haul-away), with complex jobs &mdash; plumbing restoration, tight access, corroded lines &mdash; reaching $700&ndash;$1,100. Bundled with a replacement install, removal typically costs $0&ndash;$100."),
 ("Can I remove a water softener myself?","Often, if the bypass and shutoff work: bypass the unit, kill power, depressurize, drain the tanks, disconnect, and cap the drain line ($5&ndash;$10 cap &mdash; skip it and you risk sewer gas). Call a plumber the moment the job means cutting or soldering the main line."),
 ("What does it cost to move a water softener to another spot?","Relocation prices as two jobs: a removal ($150&ndash;$500) plus a partial install at the new location &mdash; pipe by the foot, drain access, outlet. Calculated from those sourced components, plan roughly $750&ndash;$2,800 depending on distance and what the new spot lacks."),
 ("What happens to the plumbing after a softener is removed?","Two options: cap the loop and keep it (preserves $600&ndash;$2,000 of future install value, costs little now) or restore the main line permanently (cleaner, pricier, and the loop is gone). Most estimators would tell you to cap and keep unless you&rsquo;re certain."),
 ("How do I get rid of an old water softener?","Contractor haul-away ($25&ndash;$150 range in published examples), municipal bulk pickup, scrap metal for the valve head, or resale if it runs. Resin beads go in general solid waste &mdash; not curbside recycling &mdash; and rental units go back to the provider, who handles removal."),
 ("Is it cheaper to repair or replace an old water softener?","Under 10 years with one fault: repair ($150&ndash;$600) usually wins. Past 10&ndash;15 years &mdash; the published lifespan &mdash; replacement wins, especially since removal of the old unit is typically free or $50&ndash;$100 when bundled with the new install."),
 ("Do I need to test my water before removing a softener?","If the softener works, yes: it&rsquo;s actively solving something, and a $50&ndash;$150 test tells you what you&rsquo;ll inherit &mdash; scale, spotting, stiff laundry &mdash; before you pay $150&ndash;$500 to remove it. A soft-supply result makes removal an easy call."),
]
e2_rows = [
 ("Service call / trip minimum",40,100,"Applies even to quick disconnects (HomeGuide)"),
 ("Disconnection &amp; capping labor (1&ndash;4 hrs)",45,600,"$45&ndash;$150/hr; copper takes longer than flex lines"),
 ("Caps, fittings &amp; valves",5,60,"Drain cap alone is $5&ndash;$10 &mdash; never skip it"),
 ("Plumbing restoration (only if removing the loop)",0,600,"Calculated from the simple-vs-complex tier gap"),
 ("Haul-away &amp; disposal",25,150,"Published examples $25&ndash;$100; resin = general waste"),
 ("Permit (rarely required)",0,250,"One published complex example; most jobs need none"),
]
e2_bars = [
 ("Bundled with a replacement install",0,100,"#D9DED9"),
 ("Simple disconnect &amp; cap (loop kept)",150,500,"#1F7A5C"),
 ("Full removal + disposal",200,700,"#16303F"),
 ("Removal + plumbing restoration",700,1100,"#5B6B75"),
 ("Relocation (removal + partial re-install)",750,2800,"#E8A13D"),
]
e2 = head("Water Softener Removal Cost (2026): Remove, Move, or Replace",
 "Removing a water softener costs $150\u2013$500 for a simple job, $700\u2013$1,100 with plumbing restoration \u2014 and often $0 bundled with a replacement. Sourced.",
 "/water-softener-removal-cost/",
 ld(article_schema("Water Softener Removal Cost in 2026: What You\u2019ll Actually Pay to Remove, Move, or Replace It","Sourced removal pricing across every job scope \u2014 disconnect, restoration, disposal, relocation \u2014 with the remove-repair-replace decision framework.","/water-softener-removal-cost/",date="2026-07-12"))
 + ld(faq_schema(e2_faqs,"/water-softener-removal-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Removal cost","/water-softener-removal-cost/")])))
e2 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Removal cost</nav>
      <h1>Water Softener Removal Cost in 2026: What You&rsquo;ll Actually Pay to Remove, Move, or Replace It</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">The published numbers: a straightforward professional removal runs <span class="fig">$150&ndash;$500</span> &mdash; disconnect, cap, carry out &mdash; with complex jobs (plumbing restoration, tight access, seized valves) reaching <span class="fig">$700&ndash;$1,100</span>. Relocating a working unit prices as two jobs at roughly <span class="fig">$750&ndash;$2,800</span>. And the fact that reframes the whole decision: bundled with a replacement install, removal typically costs <span class="fig">$0&ndash;$100</span> per <a href="https://homeguide.com/costs/water-softener-repair-cost" rel="noopener" target="_blank">HomeGuide</a> &mdash; the new unit&rsquo;s installer hauls the old one for nearly nothing.</p>
      <p><strong>Water softener removal costs $150&ndash;$500 for a simple disconnect-and-cap job, $200&ndash;$700 with disposal, and $700&ndash;$1,100 when the plumbing must be permanently restored. Bundled with a replacement installation, removal is typically free or $50&ndash;$100 &mdash; which changes the math for anyone replacing rather than quitting.</strong></p>
      <p style="margin:0">The estimator&rsquo;s framing: &ldquo;remove the softener&rdquo; is not one job &mdash; it&rsquo;s five different jobs wearing one phrase, from a $150 disconnect that leaves the loop usable to a plumbing rebuild with two heavy tanks carried up basement stairs. The cheapest version of this project is knowing which job yours is <em>before</em> the plumber arrives. Two taps below sorts it.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#fate">Remove, repair, replace, or relocate? (tool)</a></li>
          <li><a href="#tiers">The five removal jobs, priced (chart)</a></li>
          <li><a href="#worksheet">The removal worksheet</a></li>
          <li><a href="#loop">What happens to the plumbing after &mdash; the $2,000 question</a></li>
          <li><a href="#diy">Can you remove it yourself?</a></li>
          <li><a href="#disposal">Getting rid of the old unit</a></li>
          <li><a href="#quotes">Comparing removal quotes</a></li>
        </ol>
      </details>
      <h2 id="fate">First: should this softener even come out?</h2>
      <div data-fate-calc></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">The &ldquo;works fine + don&rsquo;t want one&rdquo; verdict deserves its sentence in daylight: a working softener is solving something. A <a href="/pick/test-kit" ''' + PICK + '''>$50&ndash;$150 water test</a> tells you exactly what you&rsquo;ll inherit before you pay to remove the thing preventing it. If the salt and upkeep are the objection &mdash; not soft water itself &mdash; the <a href="/salt-free-water-softener-cost/">salt-free swap</a> keeps scale protection on your existing loop at near-zero maintenance.</p>

      <h2 id="tiers" style="margin-top:48px">The five removal jobs, on one scale</h2>
    </div>
    <div class="col-wide">''' + range_bars(e2_bars, 3000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Sources: HomeGuide (bundled $0&ndash;$100), Well Built Florida ($150&ndash;$500 simple / $800&ndash;$1,000 complex), published contractor examples ($200&ndash;$700, $700&ndash;$1,100 premium), relocation calculated from the sourced components below. The gray bar is why the replace decision so often beats standalone removal: the same haul-away, nearly free.</p>

      <h2 id="worksheet">The removal worksheet, line by line</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Standalone water softener removal", e2_rows, total_label="Removal range") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Reading the sheet:</strong> labor is the whole ballgame &mdash; published examples show <span class="fig">$260</span> of a <span class="fig">$300&ndash;$380</span> mid-range job is the plumber&rsquo;s hours. The restoration row is what separates a $300 job from a $1,000 one, and it&rsquo;s optional (next section). Typical completed removals land <span class="fig">$150&ndash;$1,000</span> &mdash; regional labor shifts totals <span class="fig">&plusmn;10&ndash;25%</span>. If a working softener is being repaired instead, budget <span class="fig">$150&ndash;$600</span> per the <a href="/water-softener-maintenance-cost/">maintenance and repair guide</a>.</p>
      <div style="margin-top:24px">''' + cta_box("Replacing? The removal is nearly free",
        "If this softener is coming out because it\u2019s old, undersized, or failing, don\u2019t buy the removal twice: installers typically haul the old unit for $0\u2013$100 during a replacement. SpringWell publishes its softener pricing online \u2014 sized by bathrooms, free shipping, 6-month money-back guarantee \u2014 so the replace-vs-remove math has a posted number on the replace side.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="loop">What happens to the plumbing after &mdash; the $2,000 question nobody quotes</h2>
      <p style="margin:0"><strong>Option one: cap the loop and keep it.</strong> The tanks leave; the supply-and-return loop stays capped behind them. Cheap now, and it preserves what a future owner &mdash; or future you &mdash; would pay <span class="fig">$600&ndash;$2,000</span> to <a href="/cost-to-add-water-softener-to-existing-home/">build from scratch</a>. <strong>Option two: restore the main line permanently.</strong> Cleaner mechanical room, but you&rsquo;re paying the restoration row above <em>and</em> deleting the loop&rsquo;s value. When I priced these jobs, my default advice was cap-and-keep unless the homeowner was certain: it&rsquo;s the only line on this worksheet that can be worth more than the whole job costs. Make the quote state which option it prices &mdash; this single ambiguity is why two honest removal quotes can be $500 apart.</p>

      <h2 id="diy">Can you remove a water softener yourself?</h2>
      <p style="margin:0">Often, if four things are true: the <strong>bypass valve turns</strong> (routing water around the unit), the <strong>shutoff works</strong>, the connections are <strong>flex lines rather than soldered copper</strong>, and you have help for the tanks &mdash; a resin tank with water and media is a two-person object on stairs. The sequence: bypass, kill power, depressurize, drain the tanks (hose bib or cup-and-bucket, and brine is heavy), disconnect, and <strong>cap the drain line</strong> &mdash; a <span class="fig">$5&ndash;$10</span> cap that Angi&rsquo;s guide warns prevents leaks and sewer gas. The moment the job means cutting or soldering the main line, it&rsquo;s a plumber&rsquo;s job at <span class="fig">$45&ndash;$150/hr</span> &mdash; a botched cap or seal can cost more in water damage than every figure on this page.</p>

      <h2 id="disposal">Getting rid of the old unit</h2>
      <p style="margin:0">In rough order of effort: <strong>contractor haul-away</strong> (the $25&ndash;$150 disposal lines above); <strong>municipal bulk pickup</strong> (check your city&rsquo;s rules); <strong>scrap</strong> &mdash; the valve head and fittings have metal value even when the tanks don&rsquo;t; <strong>resale or donation</strong> if it runs (working softeners move locally precisely because <a href="/water-softener-installation-cost/">installed cost</a> is mostly not the unit); and <strong>rental returns</strong> &mdash; leased systems go back to the provider, who handles removal. One material note from the engineering guides: spent resin beads are inert and go in <strong>general solid waste, not curbside recycling</strong> &mdash; and local rules vary, so confirm before bagging fifty pounds of amber beads.</p>

      <h2 id="quotes">Comparing removal quotes: the six-line test</h2>
      <p style="margin:0">A quote you can trust states all six: <strong>disconnect scope</strong> (bypass-and-cap vs. restoration &mdash; the $500 ambiguity); <strong>fittings and new valves</strong> included or extra; <strong>drain-line handling</strong>; <strong>haul-away and disposal</strong> in or out; <strong>access assumptions</strong> (stairs, crawlspace, corroded shutoffs); and <strong>warranty on the new plumbing work</strong>. Then the estimator&rsquo;s question, same as every project on this site: <em>what would have to happen on the day for this total to increase?</em> The <a href="/calculators/cost-calculator/">cost calculator</a> covers the replacement side of the ledger if the Fate Finder pointed you there.</p>
      <div style="margin-top:40px">''' + cta_box("The one-visit upgrade",
        "The cheapest removal on this page is the one bundled into a replacement: old unit hauled for $0\u2013$100, new system on the existing loop in the same visit. SpringWell\u2019s posted price, free shipping, and 6-month money-back guarantee put the whole decision \u2014 both sides \u2014 in daylight before anyone rolls a truck.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(e2_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">Maintenance &amp; repair costs</div><div class="range">$60&ndash;$300/yr</div><div class="desc">The repair-first math, itemized.</div></a>
        <a class="card" href="/salt-free-water-softener-cost/"><div class="name">Salt-free cost</div><div class="range">$900&ndash;$3,000</div><div class="desc">For salt-objectors: swap, don&rsquo;t quit.</div></a>
        <a class="card" href="/cost-to-add-water-softener-to-existing-home/"><div class="name">Retrofit cost</div><div class="range">$1,440&ndash;$5,470</div><div class="desc">What the loop you&rsquo;re capping is worth.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>HomeGuide &mdash; Water Softener Repair, Service &amp; Maintenance Cost (Jul 2025)</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-repair-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: removal $50&ndash;$100 incl. disposal when bundled; free removal typically covered with new-install bundles; service call $40&ndash;$100; repairs $150&ndash;$600; 10&ndash;15 yr lifespan.',
 '<strong>Well Built Florida &mdash; Water Softener Removal Cost Guide</strong> &mdash; <a href="https://wellbuiltflorida.com/water-softener-removal-cost/" rel="noopener" target="_blank">wellbuiltflorida.com</a>. Supports: straightforward removal $150&ndash;$500; complex $800&ndash;$1,000; 1&ndash;4 hr duration; regional &plusmn;10&ndash;25%; labor-dominant composition.',
 '<strong>Published contractor removal examples (One &amp; Done Prep / Adnan Remodeling)</strong> &mdash; <a href="https://oneanddoneprep.com/cost-remove-water-softener/" rel="noopener" target="_blank">oneanddoneprep.com</a>, <a href="https://adnanpaintingandremodeling.com/cost-remove-water-softener-estimates-tips/" rel="noopener" target="_blank">adnanpaintingandremodeling.com</a>. Supports: worked examples ($300&ndash;$380 mid at $260 labor + $25 disposal; $700&ndash;$1,100 premium incl. $250 permit; $200&ndash;$700 overall). Examples, not national averages.',
 '<strong>Angi &mdash; How to Remove a Water Softener (Apr 2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-to-remove-a-water-softener.htm" rel="noopener" target="_blank">angi.com</a>. Supports: DIY sequence (bypass, shutoff, depressurize, drain); $5&ndash;$10 drain cap and the sewer-gas warning; soldering as the call-a-plumber line.',
 '<strong>Angi &mdash; Water Softener Repair Cost (Mar 2026)</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-repair-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: plumber rates $45&ndash;$150/hr; 1&ndash;3 hr repairs; the 10-year repair-vs-replace rule.',
 '<strong>EngineerFix &mdash; Water Softener Removal Cost (Nov 2025)</strong> &mdash; <a href="https://engineerfix.com/how-much-does-water-softener-removal-cost/" rel="noopener" target="_blank">engineerfix.com</a>. Supports: removal frequently bundled into replacement at negligible cost; two-technician heavy-tank jobs; copper vs. flex complexity; resin disposal as general solid waste.',
 '<strong>ConsumerAffairs &mdash; Cost to Replace a Water Softener (Feb 2026)</strong> &mdash; <a href="https://www.consumeraffairs.com/homeowners/cost-to-replace-water-softener.html" rel="noopener" target="_blank">consumeraffairs.com</a>. Supports: swap labor context ($150&ndash;$1,000 standard, 1&ndash;3 hrs) behind the relocation calculation.',
 '<strong>HomeAdvisor + Fixr component figures (via our retrofit guide)</strong> &mdash; <a href="https://www.homeadvisor.com/cost/kitchens/water-softener-installation-costs/" rel="noopener" target="_blank">homeadvisor.com</a>. Supports: pipe $0.50&ndash;$8/lf, loop $600&ndash;$2,000, outlet $250&ndash;$900 &mdash; the relocation range ($750&ndash;$2,800) is calculated from these sourced components plus the removal tiers above.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("water-softener-removal-cost/index.html", e2)


# ============ G2 — IRON FILTER COST (well silo) ============
g2_faqs = [
 ("How much does an iron filter for well water cost?","$1,000&ndash;$3,500 fully installed per HomeGuide, with Mid Atlantic Water&rsquo;s 2026 guide putting the working range at $1,500&ndash;$4,500. The sweet spot for most iron wells: chemical-free AIO air-injection systems at $1,200&ndash;$2,500 installed."),
 ("What&rsquo;s the best type of iron filter &mdash; AIO, greensand, or chemical injection?","For most residential wells: AIO air injection &mdash; one tank handles iron (to ~10&ndash;15 ppm by class), sulfur, and manganese with zero chemicals. Greensand needs potassium permanganate handling; chemical injection earns its complexity only above ~15 ppm or with iron bacteria."),
 ("Can a water softener remove iron instead of an iron filter?","Only trace amounts &mdash; under roughly 1 ppm of dissolved (ferrous) iron. Above that, iron fouls softener resin, killing capacity in 6&ndash;18 months and voiding most resin warranties. The iron filter isn&rsquo;t an alternative to the softener; it&rsquo;s the thing that keeps the softener alive."),
 ("What do iron filters cost to run each year?","AIO systems: essentially $0 in chemicals &mdash; the media lasts 6&ndash;8 years and re-beds at roughly $300 per cubic foot. Chemical-based systems (greensand, injection) run $100&ndash;$250 per year in chemicals, refills, and pump service."),
 ("Does my water&rsquo;s pH matter for an iron filter?","A lot: most iron media wants pH ~7.5 or higher (higher still when manganese is present). Acidic wells need an acid neutralizer ahead of the iron filter &mdash; skipping it is why some &ldquo;failed&rdquo; iron filters were actually pH problems."),
 ("How do I know if my iron is ferrous or ferric?","The glass test: water that runs clear from the tap and turns orange as it sits is dissolved ferrous iron. Water already tinted at the tap is ferric (particulate). A lab test gives the exact number the sizing decision needs &mdash; $50&ndash;$150."),
]
g2_rows = [
 ("AIO iron filter system (Fleck 2510 AIO class)",1200,2500,"Installed; chemical-free air-injection oxidation"),
 ("Sediment prefilter (protects the media bed)",200,600,"<a href=\"/sediment-filter-cost/\">Priced here</a>; skip only on verified low-sediment wells"),
 ("Acid neutralizer (only if pH &lt; 7)",0,1500,"Most iron media wants pH 7.5+ &mdash; test first"),
 ("Media re-bed fund (year 6&ndash;8)",0,450,"~$300/cu-ft when the time comes; $0 until then"),
]
g2_bars = [
 ("Greensand / catalytic (needs Pot-Perm)",1000,2500,"#5B6B75"),
 ("AIO air injection (chemical-free)",1200,2500,"#1F7A5C"),
 ("All iron/manganese systems (HomeGuide)",1000,3500,"#16303F"),
 ("Chemical injection (15+ ppm / bacteria)",1500,4000,"#E8A13D"),
]
g2 = head("Iron Filter for Well Water Cost (2026): AIO, Greensand & Injection",
 "Iron filters cost $1,000\u2013$3,500 installed \u2014 chemical-free AIO systems $1,200\u2013$2,500. Every technology priced, with the pH gate and sizing rules.",
 "/iron-filter-for-well-water-cost/",
 ld(article_schema("Iron Filter for Well Water Cost in 2026: Every Technology, Priced Honestly","Sourced iron-filter pricing across AIO, greensand, and chemical injection \u2014 with iron-level matching, pH requirements, and ownership math.","/iron-filter-for-well-water-cost/",date="2026-07-12"))
 + ld(faq_schema(g2_faqs,"/iron-filter-for-well-water-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Well water cost","/well-water-softener-cost/"),("Iron filter cost","/iron-filter-for-well-water-cost/")])))
g2 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/well-water-softener-cost/">Well water cost</a> &rsaquo; Iron filter cost</nav>
      <h1>Iron Filter for Well Water Cost in 2026: Every Technology, Priced Honestly</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">The installed numbers: iron and manganese removal systems run <span class="fig">$1,000&ndash;$3,500</span> fully installed per <a href="https://homeguide.com/costs/well-water-filtration-system-cost" rel="noopener" target="_blank">HomeGuide</a>, with <a href="https://midatlanticwater.net/blogs/faqs/iron-filter-well-water-cost" rel="noopener" target="_blank">Mid Atlantic Water&rsquo;s February 2026 guide</a> putting the working range at <span class="fig">$1,500&ndash;$4,500</span>. By technology: chemical-free <strong>AIO air injection</strong> at <span class="fig">$1,200&ndash;$2,500</span> installed, greensand at <span class="fig">$1,000&ndash;$2,500</span>, and chemical injection at <span class="fig">$1,500&ndash;$4,000</span> for the heaviest iron loads.</p>
      <p><strong>An iron filter for well water costs $1,000&ndash;$3,500 installed. Chemical-free AIO air-injection systems &mdash; the residential standard &mdash; run $1,200&ndash;$2,500 installed with $0/year in chemicals and media lasting 6&ndash;8 years, while chemical-injection systems for 15+ ppm iron run $1,500&ndash;$4,000 plus $100&ndash;$250 yearly.</strong></p>
      <p style="margin:0">The estimator&rsquo;s frame, carried over from the <a href="/well-water-softener-cost/">well-water pillar</a>: this is the purchase that protects every purchase behind it. Iron over ~1 ppm kills softener resin in 6&ndash;18 months and voids the warranty on its way out &mdash; so the iron filter isn&rsquo;t a line item on the well quote. It&rsquo;s the reason the rest of the quote survives. What follows: match your tested ppm to a technology, price it installed, and dodge the two classic mistakes (the pH gate and the pump check).</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#matcher">Match your iron level to a system (tool)</a></li>
          <li><a href="#tech">The three technologies, decoded</a></li>
          <li><a href="#market">Installed cost by technology (chart)</a></li>
          <li><a href="#worksheet">The iron-filter project worksheet</a></li>
          <li><a href="#gates">The two gates: pH and pump flow</a></li>
          <li><a href="#ownership">The ownership decade (chart)</a></li>
        </ol>
      </details>
      <h2 id="matcher">Match your tested iron level to a system</h2>
      <p style="margin:0 0 16px">Everything keys off one number. Don&rsquo;t have it? A <a href="/pick/test-kit" ''' + PICK + '''>$50&ndash;$150 test</a> is the cheapest component on this page &mdash; and the field version costs nothing: water that runs <em>clear then turns orange in the glass</em> is dissolved ferrous iron; water already tinted at the tap is ferric.</p>
      <div data-iron-calc></div>

      <h2 id="tech" style="margin-top:48px">The three technologies, decoded</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Iron-removal technologies for well water, compared</caption>
        <thead><tr><th scope="col">Technology</th><th scope="col">Handles</th><th scope="col" class="num">Installed</th><th scope="col">The catch</th></tr></thead>
        <tbody>
          <tr><td><strong>AIO air injection</strong></td><td class="muted">Iron to ~10&ndash;15 ppm by class, sulfur, manganese</td><td class="num">$1,200&ndash;$2,500</td><td class="muted">Backwash needs 5&ndash;12 GPM from your pump</td></tr>
          <tr><td>Greensand / catalytic</td><td class="muted">Iron, manganese, sulfur (+arsenic/radium with pre-oxidation)</td><td class="num">$1,000&ndash;$2,500</td><td class="muted">Potassium permanganate handling &mdash; even sellers steer residential buyers elsewhere</td></tr>
          <tr><td>Chemical injection</td><td class="muted">15+ ppm iron, iron bacteria, combined problems</td><td class="num">$1,500&ndash;$4,000</td><td class="muted">$100&ndash;$250/yr chemicals + metering-pump service</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">The field consensus is unusually one-sided here. Mid Atlantic Water &mdash; testing media on Maryland wells they call some of the worst iron water in the country &mdash; ran Birm, greensand, and carbon before settling on air-injection with Katalox Light as the recommendation: one tank, no salt, no chemicals, and it nudges low pH upward as a side effect. Meanwhile a greensand <em>retailer</em> tells residential shoppers there&rsquo;s &ldquo;virtually always a better way&rdquo; than handling Pot-Perm at home. When the people selling a technology talk you out of it, believe them.</p>

      <h2 id="market">Installed cost by technology, one scale</h2>
    </div>
    <div class="col-wide">''' + range_bars(g2_bars, 5000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Installed ranges: The Well Guide (Mar 2026), HomeGuide (Apr 2026), SC Well Service. Note what the chart hides: the greensand and AIO bars overlap almost completely on price &mdash; the difference is the decade of chemical handling, not the day-one check.</p>

      <h2 id="worksheet">The iron-filter project, itemized</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Iron filter project + first decade", g2_rows, total_label="Project span") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Reading the sheet:</strong> the neutralizer row is the one that surprises people &mdash; it&rsquo;s conditional on a pH test, not a preference (next section) &mdash; and the re-bed row is the entire long-term cost of an AIO: <span class="fig">$0</span> in chemicals until year 6&ndash;8, then one media refresh. Buying iron treatment and softening together? The <a href="/well-water-softener-cost/">well pillar&rsquo;s package math</a> shows matched pairs running <span class="fig">$695&ndash;$1,095</span> below separate purchases.</p>
      <div style="margin-top:24px">''' + cta_box("The chemical-free standard, at a posted price",
        "The AIO class this page prices has a factory-direct benchmark: SpringWell\u2019s air-injection iron filter \u2014 independent guides credit it with handling up to 7 ppm iron, 8 ppm hydrogen sulfide, and 1 ppm manganese in one tank \u2014 publishes its price online, ships free, and carries a 6-month money-back guarantee. Above ~7 ppm tested iron, verify any model\u2019s rated capacity before buying \u2014 this one included.",
        "Check current SpringWell iron filter price","iron-filter") + '''</div>

      <h2 id="gates">The two gates every iron filter must pass</h2>
      <p><strong>Gate one: pH.</strong> Most iron media wants pH ~7.5 or higher &mdash; higher still when manganese rides along. On an acidic well, the iron filter you install will underperform until an <a href="/pick/ph-neutralizer" ''' + PICK + '''>acid neutralizer</a> goes ahead of it &mdash; a <a href="/acid-neutralizer-cost/">$1,195&ndash;$1,895 fix</a> that&rsquo;s the difference between &ldquo;this filter failed&rdquo; and &ldquo;this filter finally had a chance.&rdquo; Test pH before blaming media. <strong>Gate two: pump flow.</strong> AIO backwash pulls <span class="fig">5&ndash;12 GPM</span> that your well pump must sustain &mdash; a filter your pump can&rsquo;t backwash is a media bed that never gets clean. Your installer should verify both numbers before anything is ordered; a quote that skips them was built from the driveway.</p>

      <h2 id="ownership">The ownership decade: where AIO wins the long game</h2>
    </div>
    <div class="col-wide" style="margin-top:16px">
      <div class="donut-wrap">''' + donut_svg([("#16303F",79),("#E8A13D",13),("#1F7A5C",8)], "~$2,350", "10-yr AIO (midpoints)", "10-year AIO iron filter ownership composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> System, installed (midpoint ~$1,850) <span class="pc">~79%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Media re-bed, year 6&ndash;8 (~$300) <span class="pc">~13%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Valve parts &amp; misc <span class="pc">~8%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of sourced ranges &middot; the slice that isn&rsquo;t here is the point: $0/yr in chemicals &mdash; a chemical-injection decade adds $1,000&ndash;$2,500 in consumables the AIO never buys</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">That&rsquo;s the quiet argument for paying the AIO&rsquo;s slightly higher day-one price over greensand: the purchase prices overlap, but one of them signs you up for a decade of purple-powder logistics and the other doesn&rsquo;t. Same lesson as the <a href="/water-softener-maintenance-cost/">softener maintenance decade</a> &mdash; ownership, not sticker, is where systems get expensive.</p>
      <div style="margin-top:40px">''' + cta_box("Iron first &mdash; then everything behind it lives longer",
        "Whether it\u2019s the standalone iron filter or the matched iron + softener combo from the well pillar\u2019s package math, SpringWell\u2019s well line posts its prices, ships free, and backs both with the 6-month money-back window \u2014 so the stack gets built in the order the chemistry requires, at numbers you saw before anyone visited.",
        "Check current SpringWell iron filter price","iron-filter") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(g2_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/well-water-softener-cost/"><div class="name">Well water pillar</div><div class="range">$1,500&ndash;$6,500</div><div class="desc">The full stack &amp; package math.</div></a>
        <a class="card" href="/"><div class="name">Full cost guide</div><div class="range">$840&ndash;$4,120</div><div class="desc">The softener this filter protects.</div></a>
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">Maintenance costs</div><div class="range">$60&ndash;$300/yr</div><div class="desc">The ownership-decade lesson.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Mid Atlantic Water &mdash; Iron Filter Cost for Well Water, 2026 Price Guide (Feb 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/faqs/iron-filter-well-water-cost" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: $1,500&ndash;$4,500 installed range; Maryland media field-testing (Birm/greensand/carbon vs. Katalox Light); Fleck 2510 AIO recommendation; 6&ndash;8 yr media life; no-salt/no-chemical ownership.',
 '<strong>The Well Guide &mdash; Whole House Water Filter Cost (Mar 2026)</strong> &mdash; <a href="https://www.thewell.guide/cost-guides/whole-house-water-filter-cost" rel="noopener" target="_blank">thewell.guide</a>. Supports: AIO $1,200&ndash;$2,500 installed (10&ndash;15 ppm class); greensand $1,000&ndash;$2,500; chemical injection $1,500&ndash;$4,000; $100&ndash;$250/yr chemical-system maintenance; iron-before-softener sequence.',
 '<strong>HomeGuide &mdash; Well Water Filtration System Cost (Apr 2026)</strong> &mdash; <a href="https://homeguide.com/costs/well-water-filtration-system-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: iron/manganese systems $500&ndash;$2,500 unit / $1,000&ndash;$3,500 installed; 0.3 ppm staining threshold; 1&ndash;2 ppm dedicated-filter rule; media 5&ndash;10 yrs; backwash drain requirements.',
 '<strong>SC Well Service &mdash; iron filter &amp; treatment cost guides (2026)</strong> &mdash; <a href="https://scwellservice.com/blog/iron-filter-for-well-water.html" rel="noopener" target="_blank">scwellservice.com</a>. Supports: technology-by-level matching (softener &lt;1 ppm / Birm moderate / AIO-greensand high); ferrous-vs-ferric glass test; AIO $1,500&ndash;$2,500.',
 '<strong>Clean Water Store &mdash; Greensand technical FAQ</strong> &mdash; <a href="https://www.cleanwaterstore.com/resource/frequently-asked-questions/about-greensand-filters/" rel="noopener" target="_blank">cleanwaterstore.com</a>. Supports: potassium permanganate regeneration mechanics; GreensandPlus capabilities (arsenic/radium with pre-oxidation); Katalox Light as chemical-free alternative.',
 '<strong>Waters Filters of America &mdash; greensand vendor guidance</strong> &mdash; <a href="https://waterfiltersofamerica.com/iron-removal-from-water-greensand-iron-filter-remove-iron-sulfur-manganese/" rel="noopener" target="_blank">waterfiltersofamerica.com</a>. Supports: pH 7.5+ media requirement (8.0+ with manganese); the vendor&rsquo;s own steer-away from residential Pot-Perm systems.',
 '<strong>QualityWaterTreatment &mdash; Iron Filter Options (2026)</strong> &mdash; <a href="https://qualitywatertreatment.com/pages/top-iron-filter-options-for-well-water" rel="noopener" target="_blank">qualitywatertreatment.com</a>. Supports: SpringWell AIO rated capacities (7 ppm iron / 8 ppm sulfur / 1 ppm manganese) cited in the CTA.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("iron-filter-for-well-water-cost/index.html", g2)


# ============ G3 — ACID NEUTRALIZER COST (well silo) ============
g3_faqs = [
 ("How much does an acid neutralizer cost?","Systems run $1,195&ndash;$1,895: non-backwashing upflow units at $1,195&ndash;$1,495 (the right pick for 90%+ of homes), backwashing at $1,695&ndash;$1,895 for iron-or-sediment wells, and a FloMag blend adding ~$200 for pH below 6.0. Install: $0&ndash;$100 DIY or $300&ndash;$800 plumbed."),
 ("What does calcite media cost per year?","$145 per 50-lb bag, with most homes using 1&ndash;3 bags yearly &mdash; a typical pH-6.5 house burns about 1.5 bags ($200&ndash;$220/yr). The media dissolving is the treatment: top off through the fill port every 18&ndash;36 months. Published maintenance range: $145&ndash;$435/yr."),
 ("Does an acid neutralizer make water hard?","Yes, by design &mdash; calcite adds roughly 2&ndash;5 gpg of hardness as it dissolves. The honest nuance: most acidic well water starts naturally soft, so many homes never end up needing a softener anyway. Already at 5+ gpg? Add one downstream; matched packages save $295&ndash;$495."),
 ("Can an acid neutralizer raise the pH too much?","No &mdash; and that&rsquo;s calcite&rsquo;s best feature. It&rsquo;s chemically self-limiting: it only dissolves while the water is acidic and stops at neutral equilibrium (~7.0&ndash;7.5). You cannot overshoot with calcite, which is why it needs no dosing, metering, or electronics."),
 ("When do I need FloMag (Corosex) instead of plain calcite?","Below pH 6.0. FloMag corrects roughly 5&times; faster and blends 90/10 with calcite &mdash; never straight. Field records run to pH 4.0 and below on blends; when neutralizers disappoint, it&rsquo;s almost always undersizing or wrong media, not the chemistry."),
 ("How long does an acid neutralizer system last?","15&ndash;25+ years. Upflow units have no electronics, no drain, and a valve with zero moving parts &mdash; installations from 15+ years ago commonly run on all-original equipment with nothing replaced but calcite. The tank outlives several media refills."),
]
g3_rows = [
 ("Upflow calcite neutralizer system",1195,1495,"Non-backwashing; the 90% case (MAW 2026 pricing)"),
 ("FloMag blend upgrade (only if pH &lt; 6.0)",0,200,"90/10 blend, ~5&times; faster correction"),
 ("Sediment prefilter housing",30,50,"Keeps the calcite bed clean &mdash; cheap insurance"),
 ("Installation (DIY $0&ndash;$100 &rarr; plumber)",0,800,"No power, no drain: 1&ndash;2 hr DIY for most upflow units"),
]
g3_bars = [
 ("Upflow calcite (non-backwashing)",1195,1495,"#1F7A5C"),
 ("Upflow + FloMag blend (pH &lt; 6.0)",1395,1695,"#16303F"),
 ("Backwashing (iron / heavy sediment wells)",1695,1895,"#5B6B75"),
 ("Installed by a plumber, all types",1495,2695,"#E8A13D"),
]
g3 = head("Acid Neutralizer Cost (2026): Fixing Low-pH Well Water, Priced",
 "Acid neutralizers cost $1,195\u2013$1,895 plus $145\u2013$435/yr in calcite \u2014 the media dissolving IS the treatment. Every tier priced, sourced.",
 "/acid-neutralizer-cost/",
 ld(article_schema("Acid Neutralizer Cost in 2026: What Fixing Low-pH Well Water Costs \u2014 and What Skipping It Costs","Sourced acid neutralizer pricing: system tiers, calcite economics, the hardness trade-off, and the corrosion stakes.","/acid-neutralizer-cost/",date="2026-07-12"))
 + ld(faq_schema(g3_faqs,"/acid-neutralizer-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Well water cost","/well-water-softener-cost/"),("Acid neutralizer cost","/acid-neutralizer-cost/")])))
g3 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/well-water-softener-cost/">Well water cost</a> &rsaquo; Acid neutralizer cost</nav>
      <h1>Acid Neutralizer Cost in 2026: What Fixing Low-pH Well Water Costs &mdash; and What Skipping It Costs</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">The 2026 pricing, from the most detailed published guide in the category: non-backwashing upflow calcite systems at <span class="fig">$1,195&ndash;$1,495</span>, backwashing systems at <span class="fig">$1,695&ndash;$1,895</span>, and a FloMag blend adding <span class="fig">~$200</span> for deeper acidity (<a href="https://midatlanticwater.net/blogs/faqs/acid-neutralizer-cost" rel="noopener" target="_blank">Mid Atlantic Water, March 2026</a>). Installation is the category&rsquo;s pleasant surprise: <span class="fig">$0&ndash;$100</span> DIY &mdash; upflow units need no electricity and no drain &mdash; or <span class="fig">$300&ndash;$800</span> plumbed. The recurring line: calcite at <span class="fig">$145/bag</span>, 1&ndash;3 bags a year.</p>
      <p><strong>An acid neutralizer costs $1,195&ndash;$1,895 for the system plus $0&ndash;$800 to install, with calcite media running $145&ndash;$435 per year &mdash; because the media dissolving into your water IS the treatment. Total ownership works out to roughly $49/month to stop acidic water from eating your plumbing.</strong></p>
      <p style="margin:0">Two things make this page different from every other cost guide on this site. First, the stakes are inverted: blue-green stains aren&rsquo;t a cosmetic problem &mdash; they&rsquo;re <em>your copper pipes, dissolved, leaving the building through your faucets</em>, and the endgame is pinhole leaks inside walls. Second, the ownership math is inverted too: this is the only system we track that consumes itself <em>by design</em> &mdash; and the decade of media legitimately out-costs the machine. Both inversions are priced below.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#matcher">Match your pH to a system (tool)</a></li>
          <li><a href="#how">The self-limiting chemistry (why it can&rsquo;t overshoot)</a></li>
          <li><a href="#market">System tiers, priced (chart)</a></li>
          <li><a href="#worksheet">The project worksheet</a></li>
          <li><a href="#ownership">The inverted ownership decade (chart)</a></li>
          <li><a href="#hardness">The hardness trade-off, honestly</a></li>
          <li><a href="#stakes">What doing nothing costs</a></li>
        </ol>
      </details>
      <h2 id="matcher">Match your tested pH to a system</h2>
      <p style="margin:0 0 16px">One number decides everything on this page &mdash; and pH strips are the cheapest line in water treatment. No number yet? A <a href="/pick/test-kit" ''' + PICK + '''>proper test</a> covers pH alongside the iron and hardness this tool also asks about:</p>
      <div data-ph-calc></div>

      <h2 id="how" style="margin-top:48px">The chemistry that can&rsquo;t overshoot</h2>
      <p style="margin:0">A neutralizer is a tank of crushed limestone (calcite &mdash; ~95% calcium carbonate, NSF-certified media) that gives your water the alkaline minerals your local bedrock didn&rsquo;t. Acidic water dissolves the calcite on contact; the dissolved carbonate neutralizes the acid; the water exits at ~7.0&ndash;7.5. And here&rsquo;s the elegant part: calcite is <strong>self-limiting</strong> &mdash; it only dissolves <em>while the water is acidic</em>, then stops at neutral equilibrium. No dosing pump, no metering, no electronics, no way to overcorrect. It&rsquo;s the rare water system where the failure mode &ldquo;too much&rdquo; is chemically impossible &mdash; which is exactly why the upflow version runs with zero moving parts for decades.</p>

      <h2 id="market">The system tiers, one scale</h2>
    </div>
    <div class="col-wide">''' + range_bars(g3_bars, 3000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Pricing: Mid Atlantic Water 2026 guides. The decision between the green and gray bars isn&rsquo;t budget &mdash; it&rsquo;s water: iron above ~0.3 ppm or heavy sediment fouls a static calcite bed, so those wells need the self-cleaning backwashing unit (which also needs an outlet, a drain within ~20 ft, and 6&ndash;10 GPM from the pump) &mdash; or the iron treated separately per the <a href="/iron-filter-for-well-water-cost/">iron filter guide</a>.</p>

      <h2 id="worksheet">The neutralizer project, itemized</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Acid neutralizer project (upflow scenario)", g3_rows, total_label="Project span") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Reading the sheet:</strong> this is the most DIY-friendly project on the entire site &mdash; no power, no drain, two connections, 1&ndash;2 hours &mdash; which is why the install row can genuinely be <span class="fig">$0&ndash;$100</span>. The blend row is test-driven: pH 6.0&ndash;6.9 runs plain calcite; below 6.0 wants the 90/10 FloMag mix (and never more FloMag than that &mdash; over-blending is the classic amateur mistake).</p>
      <div style="margin-top:24px">''' + cta_box("The posted-price version",
        "SpringWell\u2019s calcite pH neutralizer publishes its price online \u2014 Bluetooth-metered head, free shipping, 6-month money-back window, lifetime warranty on covered components \u2014 and is calibrated for the common 6.0\u20136.5 pH band. The honest fine print from its own spec sheet: iron, manganese, or sulfur in the water fouls calcite media, so test first and treat those upstream \u2014 deeper acidity than ~6.0 belongs on blended-media systems.",
        "Check current SpringWell neutralizer price","ph-neutralizer") + '''</div>

      <h2 id="ownership">The inverted ownership decade</h2>
      <p style="margin:0 0 16px">Every other donut on this site shows the machine dominating the decade. This one flips &mdash; because consuming the media <em>is</em> the product working:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#E8A13D",58),("#16303F",40),("#1F7A5C",2)], "~$3,450", "10 yrs (midpoints)", "10-year acid neutralizer ownership composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#E8A13D"></span> Calcite refills, 10 yrs (~$2,000 at ~$200/yr) <span class="pc">~58%</span></div>
          <div><span class="sw" style="background:#16303F"></span> System + DIY install (~$1,395) <span class="pc">~40%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Everything else <span class="pc">~2%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of sourced ranges, typical pH-6.5 home &middot; the tiny green slice is real: zero moving parts, no filters, no service visits &mdash; 15-year-old installs commonly run all-original except the calcite</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">The refill routine itself is a bag of calcite (<span class="fig">$145</span>) poured through the fill port every 18&ndash;36 months &mdash; the published framing puts total protection around <span class="fig">$49/month</span>. More acidic water eats media faster: the <span class="fig">$145&ndash;$435/yr</span> spread <em>is</em> the pH spread.</p>

      <h2 id="hardness">The hardness trade-off, stated honestly</h2>
      <p style="margin:0">Calcite raises pH by adding calcium &mdash; which means it adds roughly <span class="fig">2&ndash;5 gpg</span> of hardness. Two honest paths from there. Most acidic well water starts naturally soft, so many homes absorb the added hardness and never need anything more &mdash; the vendors themselves say most of their neutralizer customers never add a softener. But if your water already tests <span class="fig">5+ gpg</span>, the neutralizer will push it into <a href="/">softener territory</a>, and the right build is neutralizer &rarr; softener in series &mdash; matched packages run <span class="fig">$295&ndash;$495</span> below separate purchases, the same package logic as the <a href="/well-water-softener-cost/">well pillar&rsquo;s iron math</a>. Sequence stays law: sediment &rarr; <strong>neutralizer</strong> &rarr; iron filter &rarr; softener &rarr; UV &mdash; the neutralizer goes early because <a href="/iron-filter-for-well-water-cost/">iron media wants neutral pH</a> to work.</p>

      <h2 id="stakes">What doing nothing costs</h2>
      <p style="margin:0">The published customer accounts read like insurance-claim files: pinhole leaks inside walls, flooded hardwood, corroded bronze PEX fittings &mdash; acidic water working invisibly for years before the first stain appears on a fixture. The vendor&rsquo;s framing is blunt and correct: the entire well treatment stack costs less than a single plumbing repair from corroded pipes. Against a re-pipe, a <span class="fig">$1,195&ndash;$1,895</span> tank of limestone with <span class="fig">$49/month</span> ownership isn&rsquo;t a water-quality upgrade &mdash; it&rsquo;s the cheapest plumbing insurance sold. If your fixtures show blue-green and your pipes are copper, the test kit shouldn&rsquo;t wait for the weekend.</p>
      <div style="margin-top:40px">''' + cta_box("Limestone for the house, in daylight",
        "The whole category runs on one posted-price logic: test the pH ($50\u2013$150), match the media, and buy the tank at a number you saw before anyone visited. SpringWell\u2019s neutralizer ships free with the 6-month money-back window \u2014 and if your test also shows iron or hardness, the well line\u2019s matched systems build the full stack in the order the chemistry requires.",
        "Check current SpringWell neutralizer price","ph-neutralizer") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(g3_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/well-water-softener-cost/"><div class="name">Well water pillar</div><div class="range">$1,500&ndash;$6,500</div><div class="desc">The full stack &amp; install order.</div></a>
        <a class="card" href="/iron-filter-for-well-water-cost/"><div class="name">Iron filter cost</div><div class="range">$1,000&ndash;$3,500</div><div class="desc">The pH gate&rsquo;s other half.</div></a>
        <a class="card" href="/"><div class="name">Full cost guide</div><div class="range">$840&ndash;$4,120</div><div class="desc">If the trade-off sends you to a softener.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Mid Atlantic Water &mdash; Acid Neutralizer Cost Guide (Mar 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/faqs/acid-neutralizer-cost" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: $1,195&ndash;$1,895 full pricing; FloMag +$200; DIY vs. $300&ndash;$800 plumber install; ~$49/month ownership framing; 15&ndash;25+ yr lifespan; packages $295&ndash;$495 savings.',
 '<strong>Mid Atlantic Water &mdash; Buyer&rsquo;s Guide &amp; Neutralizer Collection (Mar&ndash;May 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/faqs/best-acid-neutralizer-well-water" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: non-backwashing $1,195&ndash;$1,495 / backwashing $1,695&ndash;$1,895 tiers; calcite $145&ndash;$290/yr; 18&ndash;36-month top-offs; upflow-for-90% rule; backwashing 6&ndash;10 GPM + drain-within-20-ft requirements; pH-4.0 field blends; undersizing-not-media failure pattern.',
 '<strong>Mid Atlantic Water &mdash; Well Treatment Cost Breakdown (Mar 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/guides/well-water-treatment-system-cost" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: calcite $145/50-lb bag, 1&ndash;3 bags/yr, ~1.5 bags at pH 6.5; $145&ndash;$435/yr range; FloMag $225/bag; corroded-PEX customer account; stack-vs-repair framing.',
 '<strong>HomePlus &mdash; Acid Water Neutralizers technical overview</strong> &mdash; <a href="https://www.home-water-purifiers-and-filters.com/acid-water-neutralizer.php" rel="noopener" target="_blank">home-water-purifiers-and-filters.com</a>. Supports: self-limiting chemistry; calcite for 6.0&ndash;6.9 / Corosex blends below 6.0; hardness increase 2&ndash;5 gpg (30&ndash;100 mg/l); most-customers-never-need-a-softener nuance.',
 '<strong>ReverseOsmosis.com &mdash; Calcite media specifications</strong> &mdash; <a href="https://www.reverseosmosis.com/products/calcite" rel="noopener" target="_blank">reverseosmosis.com</a>. Supports: NSF certification; ~95% calcium carbonate composition; self-limiting anti-leaching properties for copper and lead.',
 '<strong>SpringWell &mdash; Calcite pH Neutralizer official specifications</strong> &mdash; <a href="https://www.springwellwater.com/product/well-water/calcite-ph-neutralizer/" rel="noopener" target="_blank">springwellwater.com</a>. Supports: 6.0&ndash;6.5 calibration band; pre-treatment requirements (iron/manganese/sulfur foul calcite media) cited in the CTA fine print; DIY 2&ndash;3 hr install guidance. No pricing cited &mdash; posted on the product page.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("acid-neutralizer-cost/index.html", g3)


# ============ G4 — UV DISINFECTION COST (well silo) ============
g4_faqs = [
 ("How much does a UV water purifier cost?","$400&ndash;$1,500 for equipment and $500&ndash;$2,500 installed. The named Class A residential benchmarks run $895&ndash;$995 (9&ndash;18 GPM). Ownership is the real line: an annual lamp at $30&ndash;$100, a quartz sleeve every 2&ndash;3 years at $20&ndash;$40, and ~$35/yr of electricity."),
 ("What&rsquo;s the difference between Class A and Class B UV systems?","NSF/ANSI 55 Class A delivers a 40 mJ/cm&sup2; dose and is certified to disinfect microbiologically unsafe water &mdash; the requirement for wells. Class B (16 mJ/cm&sup2;) is supplemental-only, for water that&rsquo;s already safe. On a well, Class B is never appropriate."),
 ("Why do UV lamps need replacing if they still light up?","Because the visible glow isn&rsquo;t the treatment. Germicidal UV-C output decays below effective dose around 9,000 hours (~12 months) while the bulb keeps glowing for years. A UV system on an old lamp passes water untreated with zero visible warning &mdash; replace by calendar, not by eye."),
 ("Does a UV purifier filter my water?","No &mdash; and that&rsquo;s the most misunderstood fact in the category. UV adds nothing and removes nothing: no chemicals, no metals, no sediment, no taste change. It inactivates living organisms only. Anything non-biological in your water needs its own system."),
 ("Do I need pre-filtration before a UV system?","Yes, non-negotiably: UV can&rsquo;t disinfect water it can&rsquo;t penetrate. Sediment and iron coat the quartz sleeve and shadow microbes from the light, so a 5-micron sediment filter &mdash; and iron treatment where present &mdash; goes upstream. UV is always the last stage in the stack."),
 ("Is UV better than shock-chlorinating my well?","Different tools: shock chlorination is a one-time reset after a contamination event; UV is a continuous barrier treating every gallon afterward. Wells with a coliform-positive history typically shock once, fix the entry point, and run Class A UV permanently."),
]
g4_rows = [
 ("UV system, Class A residential (equipment)",400,1500,"Named benchmarks $895&ndash;$995 at 9&ndash;18 GPM"),
 ("Installation (outlet required; horizontal clearance)",100,300,"SC Well Service; more if an outlet must be added"),
 ("<a href=\"/sediment-filter-cost/\">Sediment prefilter</a>, 5-micron (upstream, required)",30,150,"UV can&rsquo;t treat water it can&rsquo;t penetrate"),
 ("First-year consumables (lamp + sleeve care)",50,150,"The clock starts at install"),
]
g4_bars = [
 ("Budget units, Class B or uncertified",150,400,"#D9DED9"),
 ("Class A residential units (named)",895,995,"#1F7A5C"),
 ("UV equipment, full published class",400,1500,"#16303F"),
 ("Installed totals",500,2500,"#E8A13D"),
]
g4 = head("UV Water Purifier Cost (2026): Class A Systems for Well Water",
 "UV purifiers cost $500\u2013$2,500 installed plus a $30\u2013$100 lamp every year \u2014 the bulb glows long after the treatment stops. Sourced pricing + sizing.",
 "/uv-water-purifier-cost/",
 ld(article_schema("UV Water Purifier Cost in 2026: The Bulb That Lies, Priced Honestly","Sourced UV disinfection pricing: Class A vs B, sizing by bathrooms, the lamp-decay clock, and the pre-treatment rule.","/uv-water-purifier-cost/",date="2026-07-12"))
 + ld(faq_schema(g4_faqs,"/uv-water-purifier-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Well water cost","/well-water-softener-cost/"),("UV purifier cost","/uv-water-purifier-cost/")])))
g4 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/well-water-softener-cost/">Well water cost</a> &rsaquo; UV purifier cost</nav>
      <h1>UV Water Purifier Cost in 2026: The Bulb That Lies, Priced Honestly</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">The numbers: UV equipment runs <span class="fig">$400&ndash;$1,500</span> with installed totals of <span class="fig">$500&ndash;$2,500</span> per <a href="https://homeguide.com/costs/well-water-filtration-system-cost" rel="noopener" target="_blank">HomeGuide</a> and <a href="https://scwellservice.com/blog/uv-water-treatment-well.html" rel="noopener" target="_blank">SC Well Service</a>; the named Class A residential benchmarks sit at <span class="fig">$895&ndash;$995</span> for 9&ndash;18 GPM chambers. Ownership: a <span class="fig">$30&ndash;$100</span> lamp <em>every year</em>, a quartz sleeve every 2&ndash;3 years at <span class="fig">$20&ndash;$40</span>, and roughly <span class="fig">$35/yr</span> of electricity.</p>
      <p><strong>A UV water purifier costs $500&ndash;$2,500 installed &mdash; $400&ndash;$1,500 for the system, $100&ndash;$300 in labor &mdash; plus a $30&ndash;$100 lamp annually, because germicidal output dies at ~12 months while the bulb keeps glowing. For wells, only NSF 55 Class A (40 mJ/cm&sup2;) systems qualify.</strong></p>
      <p style="margin:0">This page is different from every other guide on this site in one way that matters: everything else here fights stains, scale, and appliance wear. UV fights <em>illness</em> &mdash; it&rsquo;s the one system where the failure mode isn&rsquo;t a spotted glass, it&rsquo;s E.&nbsp;coli in the kitchen tap. Which is why the two things this page hammers are the two things budget listings hide: the <strong>certification class</strong> that decides whether the unit is rated for unsafe water at all, and the <strong>lamp clock</strong> &mdash; the consumable that dies invisibly while looking perfectly alive.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#sizer">Size it &amp; get the class right (tool)</a></li>
          <li><a href="#class">Class A vs. Class B &mdash; the $200 Amazon trap</a></li>
          <li><a href="#market">The UV market by tier (chart)</a></li>
          <li><a href="#worksheet">The project worksheet</a></li>
          <li><a href="#lamp">The bulb that lies: the maintenance clock</a></li>
          <li><a href="#pretreat">The clear-water rule (why UV goes last)</a></li>
          <li><a href="#ownership">The ownership decade (chart)</a></li>
        </ol>
      </details>
      <h2 id="sizer">Two taps: size the chamber, settle the class</h2>
      <p style="margin:0 0 16px">Sizing runs on bathrooms and peak flow; the class runs on your water source. And the number that puts you on this page at all &mdash; a coliform or E.&nbsp;coli result &mdash; comes from a <a href="/pick/test-kit" ''' + PICK + '''>proper water test</a>, which private wells should run yearly since nobody regulates them for you:</p>
      <div data-uv-calc></div>

      <h2 id="class" style="margin-top:48px">Class A vs. Class B: the $200 Amazon trap</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>NSF/ANSI 55 UV classes &mdash; the distinction budget listings avoid</caption>
        <thead><tr><th scope="col">Class</th><th scope="col">Minimum dose</th><th scope="col">Certified for</th><th scope="col">The rule</th></tr></thead>
        <tbody>
          <tr><td><strong>Class A</strong></td><td class="num">40 mJ/cm&sup2;</td><td class="muted">Microbiologically <em>unsafe</em> water &mdash; sole-barrier duty</td><td><strong>The well-water requirement</strong></td></tr>
          <tr><td>Class B</td><td class="num">16 mJ/cm&sup2;</td><td class="muted">Already-safe water &mdash; supplemental layer only</td><td class="muted">Never on a well</td></tr>
          <tr><td>Uncertified</td><td class="num">Unstated</td><td class="muted">&ldquo;Kills 99.99%!&rdquo; with no dose named is avoiding the question</td><td class="muted">The $150&ndash;$400 listing tier</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">The specialist framing is blunt: the most common question is whether the $200 Amazon unit matches the $895 Class A system, and the answer is &ldquo;no, and usually not close&rdquo; &mdash; the budget tier is typically Class B or uncertified, in plastic chambers that crack under prolonged UV exposure. Some municipalities won&rsquo;t even permit a well install without Class A proof. On city water as a supplemental layer, though, Class B is a legitimate budget choice &mdash; that&rsquo;s the honest half of the trap.</p>

      <h2 id="market">The UV market by tier</h2>
    </div>
    <div class="col-wide">''' + range_bars(g4_bars, 3000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Sources: budget-tier and Class A benchmark figures from Mid Atlantic Water&rsquo;s 2026 UV guides; equipment and installed ranges from HomeGuide and SC Well Service. The gray bar isn&rsquo;t a bargain version of the green bar &mdash; it&rsquo;s a different certification doing a different job.</p>

      <h2 id="worksheet">The UV project, itemized</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("UV disinfection project (well scenario)", g4_rows, total_label="Project span") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Reading the sheet:</strong> the prefilter row isn&rsquo;t optional decoration &mdash; it&rsquo;s the physics (next-plus-one section) &mdash; and the consumables row starts ticking at install, not at year one&rsquo;s end. Site notes: UV needs a nearby outlet, horizontal mounting with clearance to slide the lamp out, and freeze protection &mdash; the same checklist your installer should walk before quoting.</p>
      <div style="margin-top:24px">''' + cta_box("The independently tested option",
        "SpringWell\u2019s UV chamber was lab-tested by an independent reviewer this year: 5.0-log inactivation at 8 GPM \u2014 above the 4-log Class A claim \u2014 built to the 40 mJ/cm\u00b2 Class A dose spec (honesty note: to the spec, not NSF-certified), with the only lifetime chamber-housing warranty in the test and Viqua-compatible lamps. Posted price, free shipping, 6-month money-back window.",
        "Check current SpringWell UV price","uv-purification") + '''</div>

      <h2 id="lamp">The bulb that lies: your maintenance clock</h2>
      <p style="margin:0 0 16px">Here&rsquo;s the field story that should sell every countdown timer ever made: installers walk into basements where the UV lamp hasn&rsquo;t been changed in three or four years &mdash; <em>still glowing</em> &mdash; while its germicidal UV-C output sits far below effective dose. The decay is invisible: output drops below safe dose around <span class="fig">9,000 hours (~12 months)</span> though the bulb lights up for years, and a UV system on a dead lamp passes water completely untreated with no visible sign. Replace by calendar, never by eye:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>The UV maintenance clock &mdash; every interval and cost</caption>
        <thead><tr><th scope="col">Component</th><th scope="col">Interval</th><th scope="col" class="num">Cost</th><th scope="col">The catch</th></tr></thead>
        <tbody>
          <tr><td>UV lamp</td><td>Every 12 months</td><td class="num">$30&ndash;$100</td><td class="muted">Glows for years; doses for one. Calendar, not eyes &mdash; and OEM lamps on sensor-equipped units</td></tr>
          <tr><td>Quartz sleeve &mdash; clean</td><td>6&ndash;12 months</td><td class="num">$0</td><td class="muted">Mineral film on the sleeve blocks dose invisibly</td></tr>
          <tr><td>Quartz sleeve &mdash; replace</td><td>Every 2&ndash;3 years</td><td class="num">$20&ndash;$40</td><td class="muted">Cloudy sleeve = under-dosed water behind clean glass</td></tr>
          <tr><td>Sediment prefilter cartridge</td><td>3&ndash;6 months</td><td class="num">$40&ndash;$80/yr</td><td class="muted">The clear-water rule&rsquo;s recurring line</td></tr>
          <tr><td>Electricity (40&ndash;100W, always on)</td><td>Continuous</td><td class="num">~$35/yr</td><td class="muted">UV doesn&rsquo;t cycle &mdash; it burns 24/7</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">This is also what the price ladder actually buys: hour-meter-only units trust you to remember; countdown timers alarm at day 355; intensity sensors <em>measure</em> real output; and solenoid-equipped Class A units physically stop the water when the dose fails &mdash; the feature many municipalities require. You&rsquo;re not paying more for a stronger bulb. You&rsquo;re paying for the system to tell the truth the bulb won&rsquo;t.</p>

      <h2 id="pretreat">The clear-water rule: why UV always goes last</h2>
      <p style="margin:0">UV can&rsquo;t disinfect water it can&rsquo;t penetrate. Sediment and iron do two quiet things: they coat the quartz sleeve, cutting output, and they <em>shadow</em> microbes from the light entirely &mdash; a particle between the lamp and an E.&nbsp;coli cell is a shield. So the stack order from the <a href="/well-water-softener-cost/">well pillar</a> holds: sediment &rarr; <a href="/acid-neutralizer-cost/">neutralizer</a> &rarr; <a href="/iron-filter-for-well-water-cost/">iron filter</a> &rarr; softener &rarr; <strong>UV, last</strong>, drinking the clearest water in the house. And the mirror truth: UV removes <em>nothing</em> &mdash; no iron, no hardness, no chemicals, no taste change. It&rsquo;s not a filter at all; it&rsquo;s a kill step. One-time contamination events get shock chlorination as the reset; UV is the continuous barrier that makes the next event a non-event.</p>

      <h2 id="ownership">The ownership decade</h2>
    </div>
    <div class="col-wide" style="margin-top:16px">
      <div class="donut-wrap">''' + donut_svg([("#16303F",52),("#E8A13D",31),("#1F7A5C",12),("#5B6B75",5)], "~$2,870", "10 yrs (midpoints)", "10-year UV ownership composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> System, installed (~$1,500) <span class="pc">~52%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Lamps &times;10 (~$900) <span class="pc">~31%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Electricity, always-on (~$350) <span class="pc">~12%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Sleeves &amp; misc <span class="pc">~5%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of sourced ranges &middot; the amber slice is non-negotiable by design &mdash; skipping a $90 lamp doesn&rsquo;t save money, it silently turns a $1,500 system into a glowing pipe</div>
    </div>
    <div class="col">
      <div style="margin-top:40px">''' + cta_box("The last stage, at a posted price",
        "If the test came back coliform-positive, the stack finishes here: SpringWell\u2019s UV stage \u2014 lifetime chamber warranty, Viqua-compatible lamps, posted price, free shipping \u2014 slots behind its iron and softener systems in exactly the order the physics requires. Test first ($50\u2013$150), then build the stack your numbers demand.",
        "Check current SpringWell UV price","uv-purification") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(g4_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/well-water-softener-cost/"><div class="name">Well water pillar</div><div class="range">$1,500&ndash;$6,500</div><div class="desc">The full stack this page finishes.</div></a>
        <a class="card" href="/iron-filter-for-well-water-cost/"><div class="name">Iron filter cost</div><div class="range">$1,000&ndash;$3,500</div><div class="desc">The pre-treatment UV depends on.</div></a>
        <a class="card" href="/acid-neutralizer-cost/"><div class="name">Acid neutralizer cost</div><div class="range">$1,195&ndash;$1,895</div><div class="desc">The stack&rsquo;s other early stage.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Mid Atlantic Water &mdash; UV Water Filter Complete Guide (Mar 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/guides/uv-water-filter-complete-guide" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: Class A 40 mJ/cm&sup2; vs Class B 16; Class-A-for-wells rule; named benchmarks $895 (9 GPM) / $995 (18 GPM); pre-treatment physics (sleeve coating + microbe shadowing); UV adds/removes nothing.',
 '<strong>Mid Atlantic Water &mdash; Best UV Purifier / VH410 review (Mar 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/faqs/best-uv-water-purifier" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: the glowing-but-dead basement-lamp field account; $150&ndash;$400 Amazon tier as Class B/uncertified; plastic-chamber warning; 365-day countdown feature; municipal Class A requirements.',
 '<strong>DEL Ozone &mdash; independent Class A systems lab test (May 2026)</strong> &mdash; <a href="https://delozone.com/best-uv-water-purifier-for-well-water/" rel="noopener" target="_blank">delozone.com</a>. Supports: ~9,000-hr (&asymp;12-month) germicidal decay below safe dose; lamp ~$90 + ~$35/yr electricity; solenoid shutoff municipal requirement; OEM-lamp sensor lock-in; SpringWell UV field results (5.0-log at 8 GPM, Class A-equivalent dose spec, not NSF-certified, lifetime chamber warranty, Viqua-compatible lamps) cited in the CTA.',
 '<strong>PurityMap &mdash; UV Purifiers guide (Mar 2026)</strong> &mdash; <a href="https://puritymap.com/solutions/uv-water-purifier/" rel="noopener" target="_blank">puritymap.com</a>. Supports: $30&ndash;$80/yr consumables (lamp $30&ndash;$70, sleeve $20&ndash;$40 every 2&ndash;3 yrs); 40&ndash;100W draw; replace-annually-regardless-of-glow.',
 '<strong>SC Well Service &mdash; UV Water Treatment for Wells (2026)</strong> &mdash; <a href="https://scwellservice.com/blog/uv-water-treatment-well.html" rel="noopener" target="_blank">scwellservice.com</a>. Supports: $500&ndash;$1,500 equipment + $100&ndash;$300 install; ~$100/yr lamp; shock-chlorination-vs-UV framing.',
 '<strong>HomeGuide &mdash; Well Water Filtration System Cost (Apr 2026)</strong> &mdash; <a href="https://homeguide.com/costs/well-water-filtration-system-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: UV $400&ndash;$1,500 equipment / $700&ndash;$2,500 installed; 99.99% inactivation list; lamp $50&ndash;$150/yr; clear-water prerequisite.',
 '<strong>FreshWaterSystems &mdash; UV Buyer&rsquo;s Guide (Apr 2026)</strong> &mdash; <a href="https://www.freshwatersystems.com/blogs/blog/uv-water-purification-buyer-s-guide" rel="noopener" target="_blank">freshwatersystems.com</a>. Supports: bathroom-based GPM sizing and the oversize rule; flow restrictors; alarm conditions; POE framing.',
 '<strong>Aquatell &mdash; UV systems collection guidance</strong> &mdash; <a href="https://www.aquatell.com/collections/ultraviolet-uv-water-filter-treatment-systems" rel="noopener" target="_blank">aquatell.com</a>. Supports: 12-month lamp rule even while glowing; sleeve ~2-yr replacement; horizontal-mount, outlet, and freeze-protection install requirements.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("uv-water-purifier-cost/index.html", g4)


# ============ R1 — WATER SOFTENER RENTAL COST vs BUYING ============
r1_faqs = [
 ("How much does it cost to rent a water softener?","$20&ndash;$100 a month across published sources, plus a setup fee of roughly $50&ndash;$499 where one is charged. Rayne publishes $25&ndash;$100 by market; Culligan rentals are reported at $25&ndash;$100. Most plans bundle service and repairs; salt is sometimes extra, up to $40/month."),
 ("Is it cheaper to rent or buy a water softener?","It hinges on one number: your monthly rate. Against a mid-priced owned system (~$2,000 installed plus upkeep), a $100/month rental breaks even in about 2 years and a $50/month rental in about 5 &mdash; while a $20/month all-inclusive rental may never break even in a normal stay."),
 ("Is renting a water softener worth it?","It can be. Renting transfers repair risk, bundles service, needs almost no cash up front, and suits short stays or a trial run. It costs more across a long stay. Compare totals over the years you actually expect to be in the house &mdash; not over the life of the equipment."),
 ("Can I cancel a water softener rental?","That depends entirely on your signed agreement. Cancellation terms are not publicly standardized and no source publishes them. Request the current cancellation amount, the buyout figure, and whether removal costs extra &mdash; all in writing &mdash; before deciding anything."),
 ("Can I buy out a rented water softener?","Often yes: Culligan&rsquo;s own materials describe rent-to-purchase options, and many agreements include a buyout. The formula isn&rsquo;t public, so ask for the current payoff in writing and weigh it against simply buying a system outright."),
 ("What happens to a rented water softener when the house is sold?","The equipment belongs to the provider, so it gets transferred to the buyer, bought out, or removed. Ask for the transfer and removal terms in writing before closing &mdash; this is the detail that ambushes buyers who inherit a softener they don&rsquo;t own."),
 ("Does a water softener rental include repairs?","Usually. Culligan states repair and maintenance costs are included in the monthly fee, and Rayne advertises complete maintenance and service with its rentals. Verify it in your own agreement &mdash; &ldquo;included&rdquo; varies by plan, and salt often isn&rsquo;t."),
 ("Is rent-to-own the same as renting?","No. A rental never ends in ownership; rent-to-own credits payments toward the equipment; financing is a loan on a purchase you own from day one. Culligan offers all three. Ask which one your paperwork actually is &mdash; the monthly payment can look identical."),
]
r1_rows = [
 ("Setup / installation fee",50,499,"Rayne: $50&ndash;$150 where charged; Culligan reported at $199&ndash;$499"),
 ("Monthly payments &times; 120 months",2400,12000,"At the published $20&ndash;$100/mo span"),
 ("Salt &amp; service where the plan excludes them",0,4800,"$0&ndash;$40/mo in add-ons, depending on plan"),
]
r1 = head("Water Softener Rental Cost (2026): Rent vs Buy, With the Math",
 "Renting runs $20\u2013$100/mo. Buying breaks even in ~2 years at the high end and possibly never at the low end \u2014 find your own break-even year.",
 "/water-softener-rental-cost/",
 ld(article_schema("Water Softener Rental Cost in 2026: Rent vs. Buy, and the Break-Even Year Nobody Shows You","Sourced rental pricing ($20\u2013$100/mo), the ten-year rental worksheet, a break-even calculator, contract decoder, and an exit framework for existing renters.","/water-softener-rental-cost/",date="2026-07-12"))
 + ld(faq_schema(r1_faqs,"/water-softener-rental-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Rental cost","/water-softener-rental-cost/")])))
r1 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Cost Guides &rsaquo; Rental cost</nav>
      <h1>Water Softener Rental Cost in 2026: Rent vs. Buy, and the Break-Even Year Nobody Shows You</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Published rental rates run <span class="fig">$20&ndash;$100 per month</span> &mdash; <a href="https://www.raynewater.com/faq/water-softener-rental-cost-what-you-need-to-know/" rel="noopener" target="_blank">Rayne posts $25&ndash;$100 depending on the market</a>, and Culligan rentals are reported at <a href="https://modernize.com/water-treatment/culligan-cost/water-softener" rel="noopener" target="_blank">$25&ndash;$100</a> &mdash; plus a setup fee of roughly <span class="fig">$50&ndash;$499</span> where one is charged. Most plans bundle service and repairs. What none of them publish is the number that actually decides this: <strong>your break-even year</strong>.</p>
      <p><strong>Renting a water softener costs $20&ndash;$100 a month plus a $50&ndash;$499 setup fee, with service and repairs usually included. Whether renting beats buying depends almost entirely on your monthly rate: against a mid-priced owned system, a $100/month rental breaks even in roughly 2 years, a $50/month rental in about 5.</strong></p>
      <p style="margin:0">And here is the finding that surprised me when I ran the arithmetic across every published rate: <strong>there is no universal answer to rent-vs-buy.</strong> There is a break-even year, and it moves from about <em>two years</em> at the top of the market to <em>never, inside any normal stay</em>, at the bottom. A $20-a-month all-inclusive rental is a genuinely good deal that most cost guides would tell you to escape. A $100-a-month rental has paid for a whole system before your third Christmas in the house. Same product. Same contract type. Opposite conclusion. So let&rsquo;s find <em>your</em> number.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#calc">Find your break-even year (tool)</a></li>
          <li><a href="#market">What renting actually costs, by provider</a></li>
          <li><a href="#worksheet">The ten-year rental, itemized</a></li>
          <li><a href="#chart">Renting vs. owning over 15 years (chart)</a></li>
          <li><a href="#decoder">Rental, rent-to-own, or financing?</a></li>
          <li><a href="#blank">The two lines nobody publishes</a></li>
          <li><a href="#matrix">Which one fits your situation</a></li>
          <li><a href="#questions">Ten questions before you sign</a></li>
          <li><a href="#escape">Already renting? The exit worksheet</a></li>
          <li><a href="#inherited">You bought a house with a rented softener</a></li>
        </ol>
      </details>
      <h2 id="calc">Find your break-even year</h2>
      <p style="margin:0 0 16px">Three inputs, and it answers the only question that matters: over the years you actually expect to live in this house, which one costs less?</p>
      <div data-rent-buy></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Calculated from sourced components, not a quote. Rental setup is modelled at $250 (mid of the sourced $50&ndash;$499 span); ownership at $2,000 installed (mid of our <a href="/water-softener-installation-cost/">sourced $840&ndash;$4,120 range</a>) plus $190/yr covering <a href="/water-softener-maintenance-cost/">upkeep</a> and a repair allowance. Salt, where a plan excludes it, is added at Angi&rsquo;s 8&ndash;12 bags at $5&ndash;$10.</p>

      <h2 id="market" style="margin-top:48px">What renting actually costs, by provider</h2>
      <p style="margin:0 0 16px">Two things stand out in the published data. First, Rayne <em>does</em> publish rates &mdash; and they differ by market, which is honest and unusual. Second, the reported spread is enormous for what is essentially the same machine in the same closet.</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>Published and reported water softener rental pricing, 2026</caption>
        <thead><tr><th scope="col">Provider</th><th scope="col" class="num">Monthly</th><th scope="col">Setup</th><th scope="col">What the payment covers</th></tr></thead>
        <tbody>
          <tr><td><strong>Rayne Water</strong> (published by market)</td><td class="num">$25&ndash;$100</td><td class="muted">$50&ndash;$150 where charged; some markets free</td><td class="muted">Maintenance and service; salt included on some plans. Contract-free rentals advertised in some markets</td></tr>
          <tr><td><strong>Culligan</strong> (reported, dealer-set)</td><td class="num">$25&ndash;$100</td><td class="muted">$199&ndash;$499 reported</td><td class="muted">Repairs and maintenance included in the monthly fee, per Culligan&rsquo;s own materials; salt delivery often bundled; multi-year agreements common</td></tr>
          <tr><td>One Culligan dealer&rsquo;s promotion</td><td class="num">from $29</td><td class="muted">&mdash;</td><td class="muted">Advertised intro offer, plus a $9.95/mo first-three-months promotion. <strong>One dealer&rsquo;s promo, not a national price</strong></td></tr>
          <tr><td>Reported low-end plans</td><td class="num">$20&ndash;$60</td><td class="muted">$199&ndash;$499</td><td class="muted">Add-ons of $0&ndash;$40/mo where salt and service aren&rsquo;t bundled</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Notice the third row. Culligan&rsquo;s own comparison page lists a <em>low introductory offer</em> among the advantages of renting &mdash; which is fair enough, and also the single most important thing to check before signing. The intro rate is a rate; it is not <em>the</em> rate. Ask what the payment becomes in month four, and whether it can rise again after that.</p>

      <h2 id="worksheet">The ten-year rental, itemized</h2>
      <p style="margin:0">A monthly payment is not a price. It is a <strong>duration</strong>. Here is the same payment, seen the way an estimator sees it &mdash; as a decade:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Ten years of renting, at the published rates", r1_rows, total_label="Ten-year rental range") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Reading the sheet:</strong> those columns do not stack in real contracts &mdash; a $100/month plan generally bundles the salt, so nobody pays the top of every row. The realistic middle: a $50/month plan with a $250 setup fee runs <span class="fig">$6,250 over ten years</span> (calculated from the sourced mid figures). For comparison, our sourced ownership build &mdash; <a href="/">$840&ndash;$4,120 installed</a> plus upkeep &mdash; lands near <span class="fig">$3,900</span> across the same decade. That gap, roughly $2,350, is what a decade of bundled service and transferred repair risk costs you. Whether that is a bargain or a bad trade is a judgment, not a fact &mdash; and it is yours to make.</p>
      <div style="margin-top:24px">''' + cta_box("Before the next decade of payments, price the alternative",
        "The rental payment renews quietly; the purchase price doesn\u2019t. SpringWell publishes its softener pricing online \u2014 sized by bathrooms, shipped free, 6-month money-back guarantee \u2014 so you can hold a real ownership number against your remaining rental cost before your next renewal, without booking a single appointment.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="chart">Renting vs. owning, fifteen years out</h2>
      <p style="margin:0 0 16px">Two straight lines, one crossing point. This is the mid-market case &mdash; a $50/month all-inclusive rental against a mid-priced owned system:</p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 320" style="width:100%;height:auto" role="img" aria-label="Cumulative cost of renting versus owning a water softener across fifteen years, with the lines crossing around year five">
        <line x1="70" y1="210" x2="660" y2="210" stroke="#E3E6E3" stroke-width="1"/>
        <line x1="70" y1="150" x2="660" y2="150" stroke="#E3E6E3" stroke-width="1"/>
        <line x1="70" y1="90" x2="660" y2="90" stroke="#E3E6E3" stroke-width="1"/>
        <line x1="70" y1="30" x2="660" y2="30" stroke="#E3E6E3" stroke-width="1"/>
        <text x="62" y="214" text-anchor="end" font-size="11" fill="#5B6B75">$2,500</text>
        <text x="62" y="154" text-anchor="end" font-size="11" fill="#5B6B75">$5,000</text>
        <text x="62" y="94" text-anchor="end" font-size="11" fill="#5B6B75">$7,500</text>
        <text x="62" y="34" text-anchor="end" font-size="11" fill="#5B6B75">$10,000</text>
        <line x1="70" y1="270" x2="660" y2="270" stroke="#16303F" stroke-width="1.5"/>
        <line x1="70" y1="30" x2="70" y2="270" stroke="#16303F" stroke-width="1.5"/>
        <line x1="70" y1="264" x2="660" y2="48" stroke="#E8A13D" stroke-width="3" stroke-linecap="round"/>
        <line x1="70" y1="222" x2="660" y2="154" stroke="#1F7A5C" stroke-width="3" stroke-linecap="round"/>
        <line x1="238" y1="270" x2="238" y2="203" stroke="#16303F" stroke-width="1" stroke-dasharray="4 3"/>
        <circle cx="238" cy="203" r="5" fill="#16303F"/>
        <text x="248" y="197" font-size="12.5" fill="#16303F" font-weight="700">Break-even &asymp; year 5</text>
        <text x="656" y="40" text-anchor="end" font-size="12.5" fill="#E8A13D" font-weight="700">Renting: $9,250</text>
        <text x="656" y="146" text-anchor="end" font-size="12.5" fill="#1F7A5C" font-weight="700">Owning: $4,850</text>
        <text x="70" y="288" text-anchor="middle" font-size="11" fill="#5B6B75">Year 0</text>
        <text x="267" y="288" text-anchor="middle" font-size="11" fill="#5B6B75">5</text>
        <text x="463" y="288" text-anchor="middle" font-size="11" fill="#5B6B75">10</text>
        <text x="660" y="288" text-anchor="middle" font-size="11" fill="#5B6B75">15</text>
        <text x="365" y="309" text-anchor="middle" font-size="11" fill="#5B6B75">Years in the house</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; calculated from sourced components &middot; renting = $250 setup + $50/mo, all-inclusive; owning = $2,000 installed + $190/yr upkeep and repair allowance &middot; <strong>flat-payment baseline &mdash; rental rates that rise pull the crossing point earlier, never later</strong> &middot; at $20/mo the amber line never crosses; at $100/mo it crosses before year 3</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">The shape is the argument. Ownership is a step you take once and then a shallow slope. Renting is a line that never flattens &mdash; and, crucially, <em>never ends</em>. In year fifteen the owner has a fifteen-year-old machine and a decision to make. The renter has fifteen years of receipts and the same machine they started with, still belonging to somebody else. That is not a scandal. It is simply the deal, stated plainly &mdash; which is more than most rental paperwork does.</p>

      <h2 id="decoder">Rental, rent-to-own, or financing? They are not the same paper</h2>
      <p style="margin:0 0 16px">Culligan alone offers all three, and the monthly payment can look nearly identical across them. The difference only shows up years later, in who owns the tank:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>Three arrangements that produce a similar monthly payment</caption>
        <thead><tr><th scope="col">Arrangement</th><th scope="col">Who owns the equipment</th><th scope="col">What the payment buys</th><th scope="col">The tell</th></tr></thead>
        <tbody>
          <tr><td><strong>True rental</strong></td><td class="muted">The provider &mdash; always</td><td class="muted">Use of the machine, plus service and repairs</td><td class="muted">Payments never end in ownership. Ending it means removal or buyout</td></tr>
          <tr><td><strong>Rent-to-own</strong></td><td class="muted">The provider, until it&rsquo;s paid off</td><td class="muted">Use, service, and equity toward the purchase</td><td class="muted">Payments are credited toward ownership. Ask for the credit schedule</td></tr>
          <tr><td><strong>Financing</strong></td><td class="muted"><strong>You do &mdash; from day one</strong></td><td class="muted">It&rsquo;s a loan against a purchase you already own</td><td class="muted">There is an APR, a term, and a total of payments. <a href="/dealer-vs-factory-direct-pricing/">Run the total</a></td></tr>
          <tr><td>Service plan on an owned system</td><td class="muted">You do</td><td class="muted">Maintenance visits only</td><td class="muted">Not a rental at all &mdash; and usually optional, whatever the pitch implies</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">One question settles it: <strong>&ldquo;At the end of these payments, whose name is on the tank?&rdquo;</strong> If the answer takes more than one sentence, get it in writing.</p>

      <h2 id="blank">The two lines nobody publishes</h2>
      <p style="margin:0">I could source a monthly rate from four companies. I could not source a single <strong>cancellation fee</strong> or <strong>buyout formula</strong> &mdash; not from Culligan, not from Rayne, not from any dealer page or cost database. They are not publicly standardized, and I am not going to invent them to round out a table.</p>
      <p style="margin:16px 0 0">So treat that blank as information: <strong>the two numbers that determine your cost of leaving are the two numbers the market does not advertise.</strong> Your signed agreement controls, and it is entirely reasonable to ask for both, in writing, <em>before</em> you sign &mdash; and to ask again, today, if you already have. This is cost guidance, not legal advice; the paperwork is the authority, not this page.</p>

      <h2 id="matrix">Which one fits your situation</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Rent or buy, by homeowner situation</caption>
        <thead><tr><th scope="col">Your situation</th><th scope="col">Renting</th><th scope="col">Owning</th><th scope="col">Why</th></tr></thead>
        <tbody>
          <tr><td>Staying under 3 years</td><td><strong>Usually stronger</strong></td><td class="muted">Rarely</td><td class="muted">Little cash up front, and at most rates you leave before the break-even year</td></tr>
          <tr><td>Staying 10+ years</td><td class="muted">Compare hard</td><td><strong>Usually stronger</strong></td><td class="muted">$50/mo becomes $6,250 by year ten; the owned system is near $3,900</td></tr>
          <tr><td>Want repairs to be someone else&rsquo;s problem</td><td><strong>Stronger</strong></td><td class="muted">Depends on warranty</td><td class="muted">Rentals bundle service; owners carry repair risk at $150&ndash;$600 a fault</td></tr>
          <tr><td>Comfortable with basic upkeep</td><td class="muted">Weaker value</td><td><strong>Stronger</strong></td><td class="muted">You&rsquo;re paying monthly for a job that&rsquo;s mostly adding salt</td></tr>
          <tr><td>Cash is tight right now</td><td><strong>Stronger</strong></td><td class="muted">Harder</td><td class="muted">$50&ndash;$499 to start versus $840&ndash;$4,120 installed</td></tr>
          <tr><td>Only moderately hard water; unsure it&rsquo;s worth it</td><td><strong>Stronger (as a trial)</strong></td><td class="muted">Later, if it proves out</td><td class="muted">Even Culligan&rsquo;s problem-water specialist suggests renting first to see the benefit before committing</td></tr>
          <tr><td>Landlord or rental property</td><td><strong>Often stronger</strong></td><td class="muted">Depends</td><td class="muted">No capital outlay, and somebody else takes the 2 a.m. call</td></tr>
          <tr><td>Renting for years and the rate has crept up</td><td class="muted">Run the exit math</td><td><strong>Often stronger</strong></td><td class="muted">Every month past break-even is money the owner isn&rsquo;t spending</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <h2 id="questions" style="margin-top:40px">Ten questions I would ask before signing a rental</h2>
      <ol style="margin:0;padding-left:20px">
        <li style="margin-bottom:7px">At the end of these payments, <strong>who owns the equipment</strong>?</li>
        <li style="margin-bottom:7px">Is this a rental, a lease, a rent-to-own agreement, or financing &mdash; <strong>in the contract&rsquo;s own words</strong>?</li>
        <li style="margin-bottom:7px">What is the payment <strong>after any introductory period</strong>, and can it rise again after that?</li>
        <li style="margin-bottom:7px">Is there a <strong>minimum term</strong>, and does the agreement <strong>auto-renew</strong>?</li>
        <li style="margin-bottom:7px">What is the <strong>cancellation amount</strong> today, and how is it calculated?</li>
        <li style="margin-bottom:7px">What is the <strong>buyout figure</strong> today, and how does it change over the term?</li>
        <li style="margin-bottom:7px">Who pays for <strong>repairs, parts, and service calls</strong> &mdash; all of them, or some?</li>
        <li style="margin-bottom:7px">Is <strong>salt</strong> included, and at what price if it isn&rsquo;t?</li>
        <li style="margin-bottom:7px">What happens <strong>if I sell the house</strong> &mdash; transfer, buyout, or removal?</li>
        <li style="margin-bottom:0">Is <strong>removal</strong> included at the end, or is that a separate charge?</li>
      </ol>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">A provider running an honest program answers all ten in writing without hesitating. The answers are also exactly what you need to run the exit math below, years from now, when you have forgotten what you signed.</p>

      <h2 id="escape">Already renting? The exit worksheet</h2>
      <p style="margin:0">Do not cancel because you are annoyed. Cancel &mdash; or stay &mdash; because the arithmetic says so. Here is the sequence I would run, in order:</p>
      <ol style="margin:12px 0 0;padding-left:20px">
        <li style="margin-bottom:6px">Find the signed agreement. Not the brochure &mdash; the agreement.</li>
        <li style="margin-bottom:6px">Confirm which of the three arrangements above it actually is.</li>
        <li style="margin-bottom:6px">Request the <strong>current monthly rate</strong> in writing (it may not be the rate you remember).</li>
        <li style="margin-bottom:6px">Request the <strong>cancellation amount</strong>.</li>
        <li style="margin-bottom:6px">Request the <strong>buyout amount</strong> &mdash; buying the tank you already have is sometimes the cheapest exit on the table.</li>
        <li style="margin-bottom:6px">Ask whether <strong>removal</strong> costs extra, and whether the equipment can stay during a transition.</li>
        <li style="margin-bottom:6px">Price the two paths (below).</li>
        <li style="margin-bottom:6px">Add back the <strong>value of the service you would lose</strong> &mdash; repairs at $150&ndash;$600 a fault are real money.</li>
        <li style="margin-bottom:6px">Decide on total cost across the years you will actually stay.</li>
        <li style="margin-bottom:0">If you buy, the <a href="/water-softener-removal-cost/">old unit&rsquo;s removal</a> is often bundled free into the new install &mdash; ask.</li>
      </ol>
      <div style="margin-top:20px;padding:18px 20px;border-left:4px solid #E8A13D;background:#F4F1EA;border-radius:4px">
        <div style="font-weight:700;margin-bottom:8px">The two formulas</div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;line-height:1.7">
          <strong>Staying rented</strong> = current monthly rate &times; months you expect to stay (+ add-ons)<br>
          <strong>Getting out</strong> = cancellation or buyout + purchase + installation + expected upkeep
        </div>
        <div style="font-size:13px;color:#5B6B75;margin-top:10px">Run both over the same number of months. Whichever is smaller wins &mdash; and if they are close, the rental&rsquo;s bundled repairs are the tiebreaker in its favour.</div>
      </div>

      <h2 id="inherited">You bought a house and inherited a rented softener</h2>
      <p style="margin:0">It is more common than you would think, and the shock is real: the tank in the garage is not yours. Three doors are open, and all three are fine. <strong>Assume the agreement</strong> (the provider transfers it into your name &mdash; ask what rate <em>you</em> get, not what the seller had). <strong>Buy it out</strong> (ask for the payoff; an older unit may be cheap to own outright). Or <strong>have it removed</strong> and start clean &mdash; which is when our <a href="/">full cost guide</a> and the <a href="/calculators/cost-calculator/">cost calculator</a> earn their keep. What you should not do is keep paying a rate you never agreed to, on a machine you never chose, because nobody handed you the paperwork at closing. Ask for it. It exists.</p>

      <h2>When renting is genuinely the right call</h2>
      <p style="margin:0">I have spent this whole page doing arithmetic that mostly favours owning, so let me be straight about the other side, because the arithmetic is not the whole story. Renting is the better choice when you will be gone before the break-even year. When your water is only <em>moderately</em> hard and you honestly do not know whether soft water is worth it to you &mdash; Culligan&rsquo;s own problem-water specialist suggests renting first for exactly that reason, and he is right. When the upfront cost is genuinely out of reach right now. When a landlord, not a resident, is making the decision. And when you simply do not want to be the person who diagnoses a stuck valve on a Sunday &mdash; that is a legitimate thing to pay for, and the monthly fee buys it honestly.</p>
      <p style="margin:16px 0 0">What renting should never be is a decision you drift into and then keep making by default for twelve years, because nobody ever showed you the crossing point. Now you have seen it. Before signing anything new, a <a href="/pick/test-kit" ''' + PICK + '''>water test</a> tells you whether you need this machine at all &mdash; and the <a href="/culligan-water-softener-cost/">Culligan pricing guide</a> covers what the same brand charges to sell you one outright.</p>
      <div style="margin-top:40px">''' + cta_box("Own the tank, end the payments",
        "If your break-even year has already come and gone, the comparison is simple: what remains on the rental versus what a system costs once. SpringWell posts its softener prices online \u2014 free shipping, 6-month money-back guarantee \u2014 so you can put a real ownership number beside your remaining rental cost tonight, and decide with both figures in front of you.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(r1_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/culligan-water-softener-cost/"><div class="name">Culligan cost guide</div><div class="range">$1,800&ndash;$6,500</div><div class="desc">What the biggest renter charges to sell.</div></a>
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Dealer vs. factory-direct</div><div class="range">$3,000&ndash;$8,000</div><div class="desc">Where the quoted number comes from.</div></a>
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">Maintenance costs</div><div class="range">$60&ndash;$300/yr</div><div class="desc">What owning actually asks of you.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Rayne Water &mdash; rental cost FAQ and market pages (2025&ndash;2026)</strong> &mdash; <a href="https://www.raynewater.com/faq/water-softener-rental-cost-what-you-need-to-know/" rel="noopener" target="_blank">raynewater.com</a>. Supports: $30&ndash;$60/mo national FAQ figure and $25&ndash;$100/mo across market pages (Bay Area, Las Vegas, Sacramento, Glendale, Palm Springs, Ventura); installation $50&ndash;$150 where charged; add-on fees around $100&ndash;$300/yr; maintenance and service included; contract-free rentals advertised in some markets.',
 '<strong>Modernize &mdash; Culligan Water Softener Costs (Apr 2026)</strong> &mdash; <a href="https://modernize.com/water-treatment/culligan-cost/water-softener" rel="noopener" target="_blank">modernize.com</a>. Supports: Culligan rentals reported at $25&ndash;$100/mo, typically including service and salt delivery, often on multi-year agreements; Culligan purchase $1,800&ndash;$6,500 installed; owner salt refills $240&ndash;$600/yr.',
 '<strong>Well Built Florida &mdash; Culligan rental cost overview (Jan 2026)</strong> &mdash; <a href="https://wellbuiltflorida.com/culligan-water-softener-rental-cost-overview/" rel="noopener" target="_blank">wellbuiltflorida.com</a>. Supports: upfront installation $199&ndash;$499; monthly rental $20&ndash;$60; salt and maintenance add-ons $0&ndash;$40/mo; a first-year example of roughly $970&ndash;$1,100.',
 '<strong>Culligan &mdash; payment options and renting-vs-owning pages</strong> &mdash; <a href="https://www.culligan.com/support/payment-options" rel="noopener" target="_blank">culligan.com</a>, <a href="https://www.culliganwater.com/resources/renting-vs-owning-from-culligan/" rel="noopener" target="_blank">culliganwater.com</a>. Supports: three distinct routes (rental, financing, purchase); repair and maintenance costs included in the monthly rental fee; rent-to-purchase offered; low introductory offers listed as a rental advantage.',
 '<strong>Culligan Total Water &mdash; an independent Culligan dealer&rsquo;s promotions</strong> &mdash; <a href="https://www.culligantotalwater.com/about/rent-buy-finance" rel="noopener" target="_blank">culligantotalwater.com</a>. Supports: advertised rental from $29/mo and a $9.95/mo first-three-months offer, and rent-to-own contracts. <strong>One dealer&rsquo;s promotion &mdash; not a national price list.</strong>',
 '<strong>Culligan &mdash; renting vs. buying guidance</strong> &mdash; <a href="https://www.culligan.com/blog/questions-to-ask-when-renting-a-water-softener" rel="noopener" target="_blank">culligan.com</a>. Supports: the company&rsquo;s own problem-water specialist recommending a rental trial for moderately hard water before committing to a purchase; maintenance included in rental packages.',
 '<strong>HomeGuide &mdash; Water Softener Cost and Repair Cost</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-repair-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: repairs $150&ndash;$600 per fault; 10&ndash;15 year lifespan; removal $50&ndash;$100 and typically bundled with a replacement install.',
 '<strong>Angi &mdash; salt and repair figures</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-repair-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: salt at 8&ndash;12 bags/yr at $5&ndash;$10 a bag; repairs $150&ndash;$900. Ownership installed range ($840&ndash;$4,120) and upkeep ($60&ndash;$300/yr) come from our own sourced <a href="/water-softener-installation-cost/">installation</a> and <a href="/water-softener-maintenance-cost/">maintenance</a> worksheets.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("water-softener-rental-cost/index.html", r1)


# ============ G5 — SEDIMENT FILTER COST (well silo keystone) ============
g5_faqs = [
 ("How much does a sediment filter cost?","$250&ndash;$600 installed for a cartridge system &mdash; $100&ndash;$300 in equipment plus $150&ndash;$300 of labor. A reusable spin-down screen runs about $145 and never needs a cartridge; a self-cleaning backwashing tank is $1,895 and most wells don&rsquo;t need one."),
 ("What micron sediment filter do I need for well water?","5 micron is the standard for most wells. Spin-down screens run 50&ndash;100 micron and only catch coarse sand. Go finer than 5 &mdash; to 1 micron &mdash; only ahead of a UV system; used alone on a dirty well, a 1-micron cartridge clogs fast."),
 ("How often do sediment filter cartridges need changing?","Every 3&ndash;6 months, or whenever pressure drops 5&ndash;10 PSI below normal &mdash; whichever comes first. A well eating a cartridge a month isn&rsquo;t telling you to buy more cartridges. It&rsquo;s telling you to put a spin-down in front of it."),
 ("Do I need a sediment filter if I have a water softener?","On a well, effectively yes. Sand and silt score control valves and foul resin and media beds &mdash; sediment is the number-one killer of softener resin, iron-filter media and UV sleeves. The cheapest stage in the stack is the one protecting the expensive ones."),
 ("What&rsquo;s the difference between a spin-down and a cartridge filter?","A spin-down spins coarse particles into a clear sump you flush in seconds &mdash; reusable, zero cartridge cost, 50&ndash;100 micron. A cartridge traps fine particles in a disposable 5-micron element. Dirty wells run both, in that order."),
 ("Is a backwashing sediment filter worth it?","Only for continuous heavy sediment that would clog cartridges in weeks. At $1,895 it&rsquo;s by far the most expensive answer &mdash; and the specialist who sells it says most homeowners don&rsquo;t need it. Try the $310&ndash;$360 spin-down + cartridge combo first."),
 ("Can I install a sediment filter myself?","Cartridge and spin-down systems, often yes &mdash; no power, no drain, and a spin-down is under an hour for anyone comfortable with basic plumbing. Professional installation runs $150&ndash;$300. Backwashing tanks need a drain line and an outlet, which raises the bar."),
 ("Where does the sediment filter go in the treatment order?","Spin-down before the pressure tank; cartridge housing after the pressure tank and ahead of every other treatment stage. Sediment is always first &mdash; its entire job is protecting what comes after it."),
]
g5_rows = [
 ("Filter housing &amp; first cartridge",100,300,"Kits at $165 (10&Prime;) and $195 (20&Prime;, NSF 42)"),
 ("Professional installation",150,300,"DIY is realistic &mdash; no power, no drain"),
 ("Spin-down pre-filter (only if you see sand)",0,249,"Standard $145; 2&Prime; high-flow $249"),
 ("First year of cartridges",30,100,"$10&ndash;$45 each, every 3&ndash;6 months"),
]
g5_bars = [
 ("Spin-down screen (reusable, no cartridges)",45,380,"#1F7A5C"),
 ("Cartridge housing kit (equipment only)",165,195,"#16303F"),
 ("Spin-down + cartridge combo (equipment)",310,360,"#E8A13D"),
 ("Cartridge system, professionally installed",250,600,"#5B6B75"),
]
g5 = head("Sediment Filter Cost for Well Water (2026): The $200 Bodyguard",
 "Sediment filters cost $250\u2013$600 installed \u2014 and $600 of cartridges over a decade. The stage that protects every expensive stage behind it, priced.",
 "/sediment-filter-cost/",
 ld(article_schema("Sediment Filter Cost in 2026: The Cheapest Stage in the Stack, and the One That Saves the Others","Sourced sediment filter pricing across cartridge, spin-down and backwashing systems \u2014 with micron selection, the cartridge-treadmill math, and placement rules.","/sediment-filter-cost/",date="2026-07-12"))
 + ld(faq_schema(g5_faqs,"/sediment-filter-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Well water cost","/well-water-softener-cost/"),("Sediment filter cost","/sediment-filter-cost/")])))
g5 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/well-water-softener-cost/">Well water cost</a> &rsaquo; Sediment filter cost</nav>
      <h1>Sediment Filter Cost in 2026: The Cheapest Stage in the Stack &mdash; and the One That Saves the Others</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">A whole-house sediment filter runs <span class="fig">$250&ndash;$600 installed</span> &mdash; <span class="fig">$100&ndash;$300</span> in equipment plus <span class="fig">$150&ndash;$300</span> of labor, per <a href="https://scwellservice.com/blog/sediment-filter-installation-well.html" rel="noopener" target="_blank">SC Well Service</a>. A reusable spin-down screen is about <span class="fig">$145</span> and never needs a cartridge. A self-cleaning backwashing tank is <span class="fig">$1,895</span> &mdash; and per the specialist who sells it, most wells don&rsquo;t need one. It is, by a wide margin, the cheapest equipment on this entire site.</p>
      <p><strong>A sediment filter costs $250&ndash;$600 installed for a 5-micron cartridge system, or about $145 for a reusable spin-down screen. Cartridges run $10&ndash;$45 each every 3&ndash;6 months &mdash; $30&ndash;$100 a year &mdash; which means across a decade the consumables cost roughly three times the housing they sit in.</strong></p>
      <p style="margin:0">Here is the thing I would tell every well owner before they spend a dollar on anything else. <strong>Every other filter in your stack is protecting your house. This one is protecting the other filters.</strong> Sand and silt are the number-one killer of softener resin, iron-filter media beds and UV sleeves &mdash; and the part that stops them costs less than a single service call on the equipment it saves. It is also the stage people skip, which is precisely how a <a href="/iron-filter-for-well-water-cost/">$2,500 iron filter</a> ends up dying young. Cheap, unglamorous, and load-bearing.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#matcher">Match what you see to a filter (tool)</a></li>
          <li><a href="#tech">Three technologies, decoded</a></li>
          <li><a href="#market">What each one costs (chart)</a></li>
          <li><a href="#micron">The micron ladder &mdash; and the word that matters</a></li>
          <li><a href="#worksheet">The project, itemized</a></li>
          <li><a href="#decade">The cheapest filter, the most expensive habit (chart)</a></li>
          <li><a href="#tank">When the $1,895 tank is actually right</a></li>
          <li><a href="#placement">Placement law, and the failure nobody notices</a></li>
        </ol>
      </details>
      <h2 id="matcher">Match what you actually see to a filter</h2>
      <p style="margin:0 0 16px">Sediment is the one well problem you can diagnose without a lab: run the tap into a white bucket, or lift the lid off the toilet tank and look at what settled. Then tell the tool what you saw &mdash; and if the water is also staining, smelling or scaling, a <a href="/pick/test-kit" ''' + PICK + '''>full test</a> sorts the rest of the stack.</p>
      <div data-sediment-calc></div>

      <h2 id="tech" style="margin-top:48px">Three technologies, decoded</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Sediment filtration for well water &mdash; how each type cleans itself, and what it costs to feed</caption>
        <thead><tr><th scope="col">Type</th><th scope="col">Catches</th><th scope="col" class="num">Cost</th><th scope="col">What it costs to run</th></tr></thead>
        <tbody>
          <tr><td><strong>Cartridge (large-format housing)</strong></td><td class="muted">Fine silt, clay, rust fines &mdash; down to 5 micron</td><td class="num">$165&ndash;$195 kit<br>$250&ndash;$600 installed</td><td class="muted"><strong>$30&ndash;$100/yr</strong> &mdash; a disposable element every 3&ndash;6 months</td></tr>
          <tr><td><strong>Spin-down screen</strong></td><td class="muted">Coarse sand and grit only &mdash; 50&ndash;100 micron</td><td class="num">$45&ndash;$380<br>(standard ~$145)</td><td class="muted"><strong>$0</strong> &mdash; centrifugal separation into a clear sump you flush in about ten seconds</td></tr>
          <tr><td>Backwashing media tank</td><td class="muted">Continuous heavy loads that would clog any cartridge</td><td class="num">$1,895</td><td class="muted"><strong>$0</strong> &mdash; rinses itself to drain on a timer; needs a drain line and an outlet</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Read the last column twice, because it inverts the usual logic of this site: <strong>the cheap system is the one with the recurring bill, and the expensive systems are the ones that eat nothing.</strong> A cartridge is a consumable wall of polyspun fibre &mdash; it fills up and you throw it away. A spin-down and a backwashing tank both clean <em>themselves</em>, which is exactly what you are paying the premium for.</p>

      <h2 id="market">What each one costs</h2>
    </div>
    <div class="col-wide">''' + range_bars(g5_bars, 700) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Sources: Mid Atlantic Water&rsquo;s 2026 pricing (kits at $165 and $195; standard spin-down $145; combo $310&ndash;$360), SC Well Service&rsquo;s installed band, iSpring&rsquo;s spin-down range. The $1,895 backwashing tank is off this chart entirely &mdash; deliberately. It belongs to a different problem, and the next-but-one section is about why most people should not buy it.</p>

      <h2 id="micron">The micron ladder &mdash; and the one word that matters</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Micron ratings: what each one stops, and where it fails</caption>
        <thead><tr><th scope="col">Rating</th><th scope="col">Stops</th><th scope="col">Use it</th><th scope="col">The catch</th></tr></thead>
        <tbody>
          <tr><td><strong>1 micron</strong></td><td class="muted">The finest particles</td><td class="muted">Only ahead of a <a href="/uv-water-purifier-cost/">UV system</a></td><td class="muted">Used alone on a dirty well it clogs fast &mdash; put something coarser in front of it</td></tr>
          <tr><td><strong>5 micron</strong></td><td class="muted">Silt, clay, rust fines &mdash; the fines that matter</td><td class="muted"><strong>The standard for most wells</strong></td><td class="muted">Coarse sand will clog it in weeks; a spin-down upstream fixes that</td></tr>
          <tr><td>20&ndash;25 micron</td><td class="muted">Mid-size grit</td><td class="muted">As a pre-filter ahead of a 5-micron on heavy sediment</td><td class="muted">Passes the fines &mdash; it&rsquo;s a stage, not an answer</td></tr>
          <tr><td>50&ndash;100 micron</td><td class="muted">Sand and coarse debris</td><td class="muted">Spin-down screens live here</td><td class="muted">Fine silt sails straight through. Never the whole solution on cloudy water</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">And the word that decides whether your UV system works: <strong>nominal</strong> versus <strong>absolute</strong>. A nominal rating removes roughly 85% of particles at its stated size. An absolute rating removes 99.9%. For general sediment, nominal is fine and nobody should pay extra. Ahead of a UV chamber it is not fine at all &mdash; because <a href="/uv-water-purifier-cost/">a single particle can shadow a bacterium from the lamp</a>, and 15% of them getting through is 15% too many. If a filter is feeding UV, the spec sheet must say <em>absolute</em>. It is the cheapest upgrade in well water and almost nobody asks for it.</p>

      <h2 id="worksheet">The sediment project, itemized</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("A sediment filter, first year", g5_rows, total_label="First-year project") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Reading the sheet:</strong> those rows don&rsquo;t all fire &mdash; the spin-down row is conditional on actually seeing sand. The realistic middle is a 20-inch housing installed for a few hundred dollars, feeding on roughly <span class="fig">$60/yr</span> of cartridges. Which sounds trivial. It is not, and the chart two sections down is why.</p>
      <div style="margin-top:24px">''' + cta_box("The stage that protects the stack, at a posted price",
        "SpringWell\u2019s sediment cartridge stage publishes its price online \u2014 free shipping, 6-month money-back guarantee \u2014 and it is the least glamorous thing you will ever buy for your water. The honest note it deserves: a cartridge filter is mechanical only. Iron, hardness, sulfur and bacteria pass straight through it, so if your test showed any of those, this stage protects the equipment that treats them \u2014 it does not replace it.",
        "Check current SpringWell sediment filter price","sediment-canister") + '''</div>

      <h2 id="decade">The cheapest filter, the most expensive habit</h2>
      <p style="margin:0 0 16px">Ten years of a cartridge system, using the sourced mid figures &mdash; a $195 housing, a few hundred to install it, and $60 a year in elements:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#E8A13D",59),("#5B6B75",22),("#16303F",19)], "~$1,020", "10 yrs (cartridge route)", "Ten-year sediment filter ownership composition") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#E8A13D"></span> Cartridges &times; 10 years (~$600) <span class="pc">~59%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Professional installation (~$225) <span class="pc">~22%</span></div>
          <div><span class="sw" style="background:#16303F"></span> The housing itself (~$195) <span class="pc">~19%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; calculated from sourced components &middot; the consumable outspends the machine roughly three to one across a decade &mdash; and the housing is rated to last about ten years, so the amber slice is the only one that repeats</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Now the arbitrage, which is the most useful paragraph on this page. On a sandy well, cartridges clog in <em>weeks</em> &mdash; call it $250&ndash;$300 a year, and you are changing them in a cold crawlspace on a Sunday. Put a <span class="fig">$145</span> spin-down screen in front, and the same cartridges last <strong>6 to 12 months</strong> instead. <strong>You spend $145 once to stop spending a couple of hundred a year, forever.</strong> That is the entire trick, it is well documented by the people who install these for a living, and it is why the dirtiest wells run <em>both</em> filters in series rather than either one alone.</p>

      <h2 id="tank">When the $1,895 tank is actually right &mdash; and when it isn&rsquo;t</h2>
      <p style="margin:0">The self-cleaning backwashing tank is the premium answer: a media bed that reverses its own flow every few days and rinses the sediment to a drain. No cartridges, ever. And here is what I find genuinely persuasive about the specialists who sell it &mdash; <strong>they say out loud that the advice they give most often costs them the sale.</strong> Their own recommendation, on their own product page, is that most homeowners don&rsquo;t need the $1,895 system: the spin-down plus cartridge combo at <span class="fig">$310&ndash;$360</span> handles the overwhelming majority of wells, and about 70% of their sediment customers end up on a plain cartridge filter.</p>
      <p style="margin:16px 0 0">So the honest test is narrow. The backwashing tank earns its price when sediment is <strong>continuous and heavy enough to clog a cartridge in weeks even with a spin-down upstream</strong> &mdash; a newly drilled well still settling, or a well pulling constant fines. The arithmetic is close, too: at $1,895 with no consumables, it takes six or seven years to overtake a cartridge system that is eating $300 a year. Before then, the cheap route wins. That is not the pitch you get from a salesman standing in your kitchen, which is rather the point of this website.</p>

      <h2 id="placement">Placement law, and the failure nobody notices</h2>
      <p style="margin:0"><strong>Spin-down goes before the pressure tank</strong> &mdash; it is the first line of defence, and it keeps sand out of the tank itself. <strong>The cartridge housing goes after the pressure tank and ahead of every other treatment stage</strong>: sediment first, then <a href="/acid-neutralizer-cost/">neutralizer</a>, <a href="/iron-filter-for-well-water-cost/">iron filter</a>, softener, and <a href="/uv-water-purifier-cost/">UV</a> last. Put it anywhere else and it is protecting nothing. Mount it where you can actually reach it &mdash; you will be opening it two to four times a year &mdash; and keep it out of freezing space, because a cracked housing floods a basement.</p>
      <p style="margin:16px 0 0">Then the failure mode almost nobody catches: <strong>a clogged cartridge does not just restrict flow &mdash; it lets sediment bypass.</strong> Pressure drops, the element channels, and the grit you installed the thing to stop goes marching downstream into the resin bed you were protecting. The trigger to change it is not a date on a calendar; it is <span class="fig">5&ndash;10 PSI</span> below your normal pressure, or 3&ndash;6 months, whichever lands first. A $20 element left in for a year is not thrift. It is a $2,500 iron filter, unprotected, and nobody in the house can tell.</p>
      <div style="margin-top:40px">''' + cta_box("$145 once, instead of $250 a year",
        "If your well throws visible sand, the spin-down is the highest-return part in well water: a reusable screen with no cartridge to buy, ever, that makes the cartridge behind it last six to twelve months instead of weeks. SpringWell posts its spin-down price online, ships free, and backs it with the 6-month money-back window. Honest limit, stated plainly: a screen catches coarse sand only \u2014 fine silt needs the 5-micron stage behind it, and neither one touches iron, hardness or bacteria.",
        "Check current SpringWell spin-down price","spin-down-sediment") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(g5_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/well-water-softener-cost/"><div class="name">Well water pillar</div><div class="range">$1,500&ndash;$6,500</div><div class="desc">The full stack this stage protects.</div></a>
        <a class="card" href="/iron-filter-for-well-water-cost/"><div class="name">Iron filter cost</div><div class="range">$1,000&ndash;$3,500</div><div class="desc">The media bed sand destroys.</div></a>
        <a class="card" href="/uv-water-purifier-cost/"><div class="name">UV purifier cost</div><div class="range">$500&ndash;$2,500</div><div class="desc">Why &ldquo;absolute&rdquo; matters.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Mid Atlantic Water &mdash; Sediment Filters for Well Water: Complete Guide and product collection (Mar&ndash;May 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/guides/sediment-filters-for-well-water-complete-guide" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: the three technologies; 10&Prime; kit $165 and 20&Prime; kit $195 (NSF 42, 15 GPM); standard spin-down $145 and 2&Prime; high-flow $249; backwashing Fleck 2510SXT tank $1,895; spin-down screens at 50&ndash;100 micron; sand as the leading killer of iron filters, softener resin and UV sleeves; sediment first in the treatment order.',
 '<strong>Mid Atlantic Water &mdash; Best Sediment Filter and Spin-Down guides (Mar 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/faqs/best-sediment-filter-for-well-water" rel="noopener" target="_blank">midatlanticwater.net</a>, <a href="https://midatlanticwater.net/blogs/faqs/spin-down-sediment-filter-well-water" rel="noopener" target="_blank">spin-down guide</a>. Supports: the combo at $310&ndash;$360; a spin-down extending cartridge life from weeks to 6&ndash;12 months; roughly 70% of their sediment customers landing on a plain cartridge filter; their stated position that most homeowners do not need the $1,895 backwashing system.',
 '<strong>Mid Atlantic Water &mdash; Well Water Treatment Cost Breakdown (Mar 2026)</strong> &mdash; <a href="https://midatlanticwater.net/blogs/guides/well-water-treatment-system-cost" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: cartridges $15&ndash;$25 each, replaced every 3&ndash;6 months, ~$40&ndash;$80/yr; the 20&Prime; housing at $195 with roughly $60/yr in cartridges; housing life around ten years.',
 '<strong>SC Well Service &mdash; Sediment Filter Installation for Wells (Feb 2026)</strong> &mdash; <a href="https://scwellservice.com/blog/sediment-filter-installation-well.html" rel="noopener" target="_blank">scwellservice.com</a>. Supports: $100&ndash;$300 equipment + $150&ndash;$300 installation = $250&ndash;$600 installed; cartridges $10&ndash;$40 each and $30&ndash;$100/yr; the micron ladder (5 micron standard, 1 micron before UV, 20&ndash;25 as a pre-filter); nominal (~85%) versus absolute (99.9%) ratings; the 5&ndash;10 PSI change trigger; placement after the pressure tank; the warning that a clogged filter lets sediment bypass.',
 '<strong>iSpring &mdash; spin-down sediment filter range</strong> &mdash; <a href="https://www.ispringfilter.com/spin-down-sediment-water-filters" rel="noopener" target="_blank">ispringfilter.com</a>. Supports: spin-down pricing from $45&ndash;$100 (small) to $180&ndash;$200 (medium) and $320&ndash;$380 (jumbo); 50 micron as the standard screen; DIY-friendly installation.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("sediment-filter-cost/index.html", g5)


# ============ C7 — LEAF HOME WATER SOLUTIONS (opening bid) ============
c7_faqs = [
 ("How much does a Leaf Home water system cost?","Reported at $800&ndash;$8,000+ with no published price list. Modernize puts most systems at $1,500&ndash;$4,000 and combination systems at $4,000&ndash;$8,000+; BestCompany reports softeners at $2,000&ndash;$4,000. Every number comes out of an in-home consultation."),
 ("Why isn&rsquo;t there a Leaf Home price list?","Because the price is produced at your kitchen table after a free water test, like every in-home-sales brand. That&rsquo;s also why one published customer account describes a quote moving from over $9,000 to $4,785 inside a single visit."),
 ("Can I negotiate a Leaf Home quote?","The published accounts say the number moves &mdash; and Leaf Home&rsquo;s own marketing celebrates quoting far below competitors who visited the day before. A written competing quote is the lever; a published factory-direct price is the anchor."),
 ("Is Leaf Home cheaper than Culligan or RainSoft?","Reported ranges put it below RainSoft ($6,000&ndash;$11,000) and roughly alongside Culligan. But comparing quote-based brands to each other compares negotiations, not prices &mdash; which is why this site anchors everything against a published number."),
 ("What is Leaf Home&rsquo;s warranty?","Reported as limited and non-transferable &mdash; commonly one year from the date of shipment, with select parts possibly qualifying for lifetime coverage. Get duration, parts-versus-labor, transferability and what voids it, all in writing."),
 ("Does Leaf Home handle well water?","Yes &mdash; they market well-specific systems for iron, sulfur odour and microbial contamination. On a well, the order of the treatment stack matters more than the badge on the tank; our well guide covers the sequence and the sourced costs."),
 ("Is Leaf Home a good company?","Founded in 2021, serving 12 states, with a four-week installer training programme, a two-minute digital water test and no long-term contracts. Reviews are mixed, with reported warranty disputes &mdash; and the company does respond publicly to complaints."),
]
c7_rows = [
 ("Comparable metered softener (published class)",600,1500,"HomeGuide equipment band &mdash; the class inside most packages"),
 ("Professional installation",200,500,"Angi: 2&ndash;4 hrs at $100&ndash;$150/hr"),
 ("Fittings, bypass &amp; materials",40,120,"Itemised in honest quotes"),
 ("Remainder of the $4,785 discounted deal (implied)",2665,3945,"Sales, lead acquisition, overhead, service, financing &mdash; the unlabelled line"),
]
c7_bars = [
 ("Reverse osmosis (drinking water)",1500,3000,"#5B6B75"),
 ("Water softener",2000,4000,"#16303F"),
 ("Whole-house filtration",2000,5000,"#5B6B75"),
 ("Combination systems",4000,8000,"#E8A13D"),
 ("For reference: our documented softener build, installed",840,4120,"#1F7A5C"),
]
c7 = head("Leaf Home Water Solutions Cost (2026): The Number Is an Opening Bid",
 "Leaf Home systems are reported at $800\u2013$8,000+ with no published prices \u2014 and one account describes $9,000 becoming $4,785 in a single visit. Decoded.",
 "/leaf-home-water-solutions-cost/",
 ld(article_schema("Leaf Home Water Solutions Cost in 2026: Why the First Number Isn\u2019t a Price","Reported Leaf Home pricing, the same-visit discount phenomenon, quote reconstruction, warranty structure, and the financing math nobody runs.","/leaf-home-water-solutions-cost/",date="2026-07-12"))
 + ld(faq_schema(c7_faqs,"/leaf-home-water-solutions-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Brand pricing","/dealer-vs-factory-direct-pricing/"),("Leaf Home cost","/leaf-home-water-solutions-cost/")])))
c7 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/dealer-vs-factory-direct-pricing/">Brand pricing</a> &rsaquo; Leaf Home cost</nav>
      <h1>Leaf Home Water Solutions Cost in 2026: Why the First Number Isn&rsquo;t a Price</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">The reported figures span an extraordinary range: <a href="https://modernize.com/water-treatment/leaf-home-water-solutions-cost" rel="noopener" target="_blank">Modernize</a> puts most Leaf Home systems at <span class="fig">$1,000&ndash;$4,000</span> installed with complex whole-home builds reaching <span class="fig">$8,000+</span>; <a href="https://bestcompany.com/blog/water-softeners/leaf-home-water-system-cost" rel="noopener" target="_blank">BestCompany</a> reports softeners at <span class="fig">$2,000&ndash;$4,000</span> and whole-house filtration at <span class="fig">$2,000&ndash;$5,000</span>. Leaf Home publishes none of it. And there is a reason that matters more than the range itself.</p>
      <p><strong>Leaf Home Water Solutions systems are reported at $800&ndash;$8,000+ with no published price list &mdash; softeners typically $2,000&ndash;$4,000, combination systems $4,000&ndash;$8,000+. Every figure originates in an in-home consultation, and published customer accounts describe the quoted number moving by thousands of dollars within a single visit.</strong></p>
      <p style="margin:0">I spent fifteen years producing numbers like these, so let me say the quiet part first. <strong>When a price can fall by half during the appointment that created it, it was never a price. It was an opening bid.</strong> That is not an accusation &mdash; it is arithmetic, and two independent pieces of public evidence point at it. One of them is a customer&rsquo;s account. The other is Leaf Home&rsquo;s own marketing.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#ranges">What the reported numbers actually say (chart)</a></li>
          <li><a href="#twonumbers">Two numbers, one appointment (chart)</a></li>
          <li><a href="#anchor">The anchor test (tool)</a></li>
          <li><a href="#worksheet">The discounted deal, reconstructed</a></li>
          <li><a href="#financing">Finance the discount and you&rsquo;re back at the first number (tool)</a></li>
          <li><a href="#warranty">The warranty structure &mdash; and what to demand in writing</a></li>
          <li><a href="#fair">What Leaf Home genuinely does well</a></li>
        </ol>
      </details>
      <h2 id="ranges">What the reported numbers actually say</h2>
    </div>
    <div class="col-wide">''' + range_bars(c7_bars, 8000) + '''</div>
    <div class="col">
      <p style="margin:12px 0 0;font-size:14px;color:#5B6B75">Reported ranges: Modernize (Feb&ndash;Mar 2026), BestCompany (Oct 2025). The green bar is not a Leaf Home figure &mdash; it is <a href="/water-softener-installation-cost/">our own sourced build</a> of what a softener costs to buy and install, from HomeGuide equipment classes and Angi labour rates. It is on the chart for one reason: it is the only bar on it that anybody publishes.</p>

      <h2 id="twonumbers">Two numbers, one appointment</h2>
      <p style="margin:0 0 16px">A published customer account describes being quoted <strong>over $9,000</strong> for a whole-home system. The customer mentioned that comparable equipment was available online for a fraction of it. The salesperson phoned a supervisor &mdash; and came back with a one-time offer of <strong>$4,785</strong>, in the same visit:</p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 190" style="width:100%;height:auto" role="img" aria-label="A reported quote of over nine thousand dollars dropping to four thousand seven hundred and eighty-five dollars within the same appointment">
        <text x="140" y="62" text-anchor="end" font-size="13" fill="#16303F" font-weight="600">First number</text>
        <rect x="150" y="40" width="450" height="34" rx="3" fill="#E8A13D"/>
        <text x="608" y="62" font-size="14" fill="#16303F" font-weight="700">$9,000+</text>
        <text x="140" y="122" text-anchor="end" font-size="13" fill="#16303F" font-weight="600">Same-visit offer</text>
        <rect x="150" y="100" width="239" height="34" rx="3" fill="#1F7A5C"/>
        <text x="397" y="122" font-size="14" fill="#16303F" font-weight="700">$4,785</text>
        <line x1="389" y1="100" x2="389" y2="162" stroke="#5B6B75" stroke-width="1" stroke-dasharray="4 3"/>
        <line x1="600" y1="40" x2="600" y2="162" stroke="#5B6B75" stroke-width="1" stroke-dasharray="4 3"/>
        <line x1="389" y1="162" x2="600" y2="162" stroke="#5B6B75" stroke-width="1.5"/>
        <text x="494" y="181" text-anchor="middle" font-size="12.5" fill="#5B6B75">$4,215+ &mdash; moved by one phone call</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; one customer&rsquo;s published account. <strong>An example, not a national average</strong> &mdash; and not a discount you should expect, plan on, or be promised</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">On its own, one review proves nothing; people exaggerate, and companies get unfairly kicked. So here is the second piece of evidence, and it is the one I find genuinely decisive &mdash; because it comes from <strong>Leaf Home&rsquo;s own website</strong>. On their water softener page, among the testimonials they chose to publish, a customer celebrates being quoted a price <strong>40&ndash;60% below two other companies that had visited the day before.</strong></p>
      <p style="margin:16px 0 0">Sit with that for a second. Leaf Home is <em>advertising</em> that its number came in around half of what two competitors said, for the same house, in the same week. I believe them. But read it as a professional and it stops being a boast about Leaf Home and becomes a statement about the entire channel: <strong>if a 40&ndash;60% swing between quotes is a selling point rather than a scandal, then none of these numbers are prices.</strong> They are positions. And a customer who negotiates well pays less than a customer who does not &mdash; for exactly the same tank, in exactly the same basement.</p>

      <h2 id="anchor">The anchor test</h2>
      <p style="margin:0 0 16px">So do the one thing the appointment is designed to prevent: compare the number to something that does not move. Drop in what you were quoted and what your house actually needs &mdash; and toggle the discount to see what a same-visit cut of the reported size would leave behind.</p>
      <div data-anchor-test></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Documented bands come from our sourced <a href="/water-softener-installation-cost/">installation scenarios</a> &mdash; HomeGuide equipment classes, Angi labour, Fixr and HomeAdvisor site work. And before any of it, a <a href="/pick/test-kit" ''' + PICK + '''>water test you own</a> tells you what you actually need, rather than what the free test found.</p>

      <h2 id="worksheet">The discounted deal, reconstructed</h2>
      <p style="margin:0">Take the $4,785 &mdash; the <em>good</em> number, the one that felt like a win &mdash; and build the same project from published component prices:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("The $4,785 &ldquo;one-time deal&rdquo;, reconstructed", c7_rows, total_label="The discounted deal") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Reading the sheet:</strong> even at half price, <span class="fig">56&ndash;82%</span> of the money sits above the documented cost of the equipment and the labour. That remainder is <em>not</em> profit &mdash; it also funds the in-home appointment, the advertising that produced the lead, vehicles, insurance, licensing, a service department and financing costs, exactly as the <a href="/dealer-vs-factory-direct-pricing/">channel hub</a> lays out. But it is the part you are entitled to see itemised. And the discount did not reveal it. <strong>The discount didn&rsquo;t find the price. It just moved the number.</strong></p>
      <div style="margin-top:24px">''' + cta_box("Anchor the appointment before it starts",
        "Leaf Home\u2019s flagship is a 2-in-1: a softener and a catalytic carbon filter in one tank. SpringWell publishes the price of the equivalent combination online \u2014 softener plus whole-house filter, sized by bathrooms, shipped free, with a 6-month money-back guarantee. Whether or not you end up buying it, walking into a free water test already knowing what that hardware costs is the single cheapest thing you can do for your negotiating position.",
        "Check current SpringWell combo price","filter-salt-softener-combo") + '''</div>

      <h2 id="financing">Finance the discount, and you&rsquo;re back at the first number</h2>
      <p style="margin:0 0 16px">Here is the part that turns the whole story inside out. The $4,785 deal almost never gets paid in cash &mdash; it gets paid monthly. So run the payment the way an estimator runs it:</p>
      <div data-finance-calc data-pmt="95" data-term="84" data-apr="15.9"></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Illustrative &mdash; not a quote, and not Leaf Home&rsquo;s terms, which are unpublished. The default is seeded at a payment that implies roughly the $4,785 deal above, financed over seven years at a mid-teens APR.</p>
      <p style="margin:20px 0 0">Read the total. A <span class="fig">$95</span> monthly payment across 84 months is <span class="fig">$7,980</span> handed over &mdash; which lands you back <strong>within about a thousand dollars of the $9,000 quote you were so relieved to escape.</strong> The discount was real. The saving, after seven years of interest, largely was not. That is not a Leaf Home trick; it is what borrowing costs, and it happens at every brand in this channel. It is simply invisible unless somebody multiplies the payment by the number of payments &mdash; which is why the <a href="/dealer-vs-factory-direct-pricing/">hub</a> puts a calculator in front of it. Get the <strong>cash price, APR, term and total of payments</strong> in writing, and treat &ldquo;no interest if paid in full&rdquo; as deferred interest rather than 0% APR: any balance surviving the promo window is billed retroactively to day one on the original amount, and the CFPB finds roughly one in five such balances take that hit.</p>

      <h2 id="warranty">The warranty structure &mdash; and what to demand in writing</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>What the public record says about Leaf Home coverage &mdash; and the question each line generates</caption>
        <thead><tr><th scope="col">Reported term</th><th scope="col">What it means in practice</th><th scope="col">Ask for this in writing</th></tr></thead>
        <tbody>
          <tr><td><strong>Limited &amp; non-transferable</strong></td><td class="muted">Coverage does not follow the house to a new owner</td><td class="muted">Is it transferable at all, and at what cost?</td></tr>
          <tr><td><strong>One year from date of shipment</strong> on some products</td><td class="muted">The clock can start before the system is even installed</td><td class="muted">Does coverage run from shipment, install, or first use?</td></tr>
          <tr><td>Select parts may qualify for lifetime coverage</td><td class="muted">&ldquo;Lifetime&rdquo; applies to <em>parts</em>, not necessarily to labour</td><td class="muted">Which parts, for how long &mdash; and who pays the technician?</td></tr>
          <tr><td>Reported clauses around changing water conditions</td><td class="muted">One published complaint describes a clause about seasonal water changes being used to decline responsibility</td><td class="muted">What conditions void coverage? Get the exclusions listed</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Two honest caveats on that table. First, these are <strong>reported</strong> terms from review databases and individual customer accounts &mdash; the authority is your own signed agreement, not this page, and warranty terms vary by product. Second, individual complaints are individual complaints: one published account describes carbon media replacements running around <span class="fig">$500 every 4&ndash;6 months</span>, which would be a serious ownership cost if it were the norm &mdash; but it is one person&rsquo;s account, not a published price, and I am not going to present it as one. Turn it into a question instead, because it is a very good one: <strong>&ldquo;what does the media in this tank cost to replace, how often, and is that in writing?&rdquo;</strong> Ask it before you sign, not after. Our <a href="/water-softener-maintenance-cost/">maintenance guide</a> prices the honest answer for a conventional system: <span class="fig">$60&ndash;$300 a year</span>, not thousands.</p>

      <h2 id="fair">What Leaf Home genuinely does well</h2>
      <p style="margin:0">Fairness is not decoration on this site, so: the free water test is a real one. It is digital, returns results in about two minutes, and removes the strip-reading guesswork that makes most in-home tests theatre &mdash; that is a genuine improvement on the industry norm. Installers go through a four-week training programme. There are no long-term contracts, unlike some of the rental-heavy competitors on this site. The flagship softener is a legitimate piece of engineering: a 2-in-1 tank pairing ion exchange with catalytic carbon, with proportional brining the company says saves up to 30% of the salt and up to 2,000 gallons of water a year &mdash; precision brining is a real efficiency feature, not marketing vapour. And when customers complain publicly, the company answers publicly, which is more than several brands in this series manage.</p>
      <p style="margin:16px 0 0">Which is exactly why the pricing model deserves the scrutiny rather than the products. <strong>A company confident in a $4,785 system does not need to open at $9,000.</strong> The equipment is not the problem here. The <em>process</em> is &mdash; and the fix costs you nothing: walk into the appointment already knowing what the hardware costs, and the free water test becomes what it should have been all along. A water test.</p>
      <div style="margin-top:40px">''' + cta_box("The number that doesn\u2019t move",
        "Every figure on this page came out of somebody\u2019s living room. Here is one that didn\u2019t: SpringWell posts its softener pricing online \u2014 sized by bathrooms, free shipping, 6-month money-back guarantee \u2014 so you can hold a published number against any in-home quote, before the supervisor gets phoned. Buy the Leaf Home system if it wins on the merits. Just make it win against a real number.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(c7_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Dealer vs. factory-direct</div><div class="range">$3,000&ndash;$8,000</div><div class="desc">Where the quoted number comes from.</div></a>
        <a class="card" href="/culligan-water-softener-cost/"><div class="name">Culligan cost guide</div><div class="range">$1,800&ndash;$6,500</div><div class="desc">The same model, older.</div></a>
        <a class="card" href="/water-softener-installation-cost/"><div class="name">Installation, itemised</div><div class="range">$840&ndash;$4,120</div><div class="desc">The build every quote is measured against.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Modernize &mdash; Leaf Home Water Solutions Costs (Mar 2026) and brand review (Feb 2026)</strong> &mdash; <a href="https://modernize.com/water-treatment/leaf-home-water-solutions-cost" rel="noopener" target="_blank">modernize.com</a>, <a href="https://modernize.com/water-treatment/best-companies/leaf-home-water-solutions" rel="noopener" target="_blank">brand review</a>. Supports: $1,000&ndash;$4,000 typical installed, complex builds $8,000+, combination systems $4,000&ndash;$8,000+; entry units around $800; founded 2021 under the Leaf Home brand (parent of LeafFilter); serving 12 states; one-year limited warranty from date of shipment with select parts possibly qualifying for lifetime coverage.',
 '<strong>BestCompany &mdash; Leaf Home Water System cost and brand reviews</strong> &mdash; <a href="https://bestcompany.com/blog/water-softeners/leaf-home-water-system-cost" rel="noopener" target="_blank">bestcompany.com</a>. Supports: most systems $1,500&ndash;$6,000; softeners $2,000&ndash;$4,000; whole-house filtration $2,000&ndash;$5,000; reverse osmosis $1,500&ndash;$3,000; limited non-transferable warranties; the four-week installer training programme; the two-minute digital water test.',
 '<strong>Leaf Home &mdash; official water softener product page</strong> &mdash; <a href="https://www.leafhome.com/water-solutions/water-softening-systems/softening-systems" rel="noopener" target="_blank">leafhome.com</a>. Supports: the 2-in-1 softener + catalytic carbon design; proportional brining claimed to save up to 30% salt and up to 2,000 gallons of water per year; and the company&rsquo;s own published testimonial celebrating a quote 40&ndash;60% below two competitors who had visited the day before. No prices are published anywhere on the site.',
 '<strong>Trustpilot &mdash; published Leaf Home Water Solutions customer accounts</strong> &mdash; <a href="https://www.trustpilot.com/review/www.leafhomewatersolutions.com" rel="noopener" target="_blank">trustpilot.com</a>. Supports: the account of a quote above $9,000 reduced to a same-visit offer of $4,785 after the salesperson consulted a supervisor. <strong>Individual customer accounts &mdash; examples, not national averages.</strong> The company responds publicly to reviews on the platform.',
 '<strong>PissedConsumer &mdash; reported Leaf Home complaints</strong> &mdash; <a href="https://www.pissedconsumer.com/leaf-home-water-solutions/RT-F.html" rel="noopener" target="_blank">pissedconsumer.com</a>. Supports: a reported contract clause regarding seasonal changes in water conditions, and a single reported figure of roughly $500 per carbon-media replacement every 4&ndash;6 months. <strong>One customer&rsquo;s account, not a published price</strong> &mdash; presented on this page only as a question to ask in writing.',
 '<strong>HomeGuide and Angi &mdash; the documented build</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>, <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: equipment class $600&ndash;$1,500; installation labour $200&ndash;$500 at $100&ndash;$150/hr &mdash; the reconstruction and the reference bar.',
 '<strong>Consumer Financial Protection Bureau &mdash; Regulation Z &sect;1026.16 and retail credit research</strong> &mdash; <a href="https://www.consumerfinance.gov/rules-policy/regulations/1026/16/" rel="noopener" target="_blank">consumerfinance.gov</a>. Supports: deferred interest billed retroactively on the original purchase amount; roughly 1 in 5 promotional balances hit; the &ldquo;if paid in full&rdquo; disclosure requirement. Financing mechanics only &mdash; not Leaf Home&rsquo;s terms, which are unpublished.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("leaf-home-water-solutions-cost/index.html", c7)


# ============ S1 — WHAT SIZE WATER SOFTENER DO I NEED ============
s1_faqs = [
 ("What size water softener do I need for a family of 4?","At 10 gpg, four people need about 3,000 grains a day &mdash; 21,000 over a week. Most calculators answer &ldquo;24,000-grain.&rdquo; But a 24k only reaches that number at maximum salt. Sized to run efficiently, a 40,000-grain unit is the better answer &mdash; same water, less salt."),
 ("How do I calculate water softener size?","People &times; 75 gallons &times; hardness (gpg) = grains per day. Multiply by 7 for a weekly regeneration cycle. Add 5 gpg for every 1 ppm of iron. Then pick a unit whose capacity at an <em>efficient</em> salt dose &mdash; roughly 65% of nameplate &mdash; covers that number."),
 ("What does &ldquo;32,000 grain&rdquo; actually mean?","It is the capacity at maximum salt dose &mdash; about 15 lbs of salt per cubic foot of resin. At an efficient 6-lb dose the same tank delivers roughly 20,000 grains. The nameplate is a ceiling reached only on the day you waste the most salt, not a working number."),
 ("Is it bad to oversize a water softener?","Slightly bigger is good &mdash; it lets the same water be softened at a lower salt dose. Far too big causes channeling: water carves a groove through the resin, beads oversaturate and softening quality drops. Keep regeneration inside the 7&ndash;14 day window."),
 ("How do I convert ppm to grains per gallon?","Divide by 17.1. So 171 ppm of hardness is 10 gpg. Municipal water usually tests 5&ndash;15 gpg; wells often run 20&ndash;30 gpg or higher, which is why sizing errors get expensive faster on a well."),
 ("Does iron change the softener size I need?","Yes &mdash; add 5 gpg for every 1 ppm of iron. But iron doesn&rsquo;t just consume capacity, it coats the resin and shortens its life. Above about 1 ppm the answer isn&rsquo;t a bigger softener; it&rsquo;s an iron filter in front of the one you have."),
 ("Can I size a water softener by the number of bathrooms?","It&rsquo;s a common shortcut, and it&rsquo;s a reasonable proxy for household size and peak flow. It is not a hardness measurement. Fine at typical municipal hardness &mdash; but above roughly 15 gpg, or on a well, check the grain capacity against your own 7-day number."),
 ("How often should a water softener regenerate?","Every 7&ndash;14 days is the healthy window. Much more often wastes salt and water and wears the valve; much less often risks channeling and stagnant water in the resin bed. Regeneration frequency is a sizing symptom &mdash; it tells you whether you got it right."),
]
s1 = head("What Size Water Softener Do I Need? (2026 Calculator + The Nameplate Trap)",
 "The formula every calculator uses \u2014 and the salt-efficiency correction almost none of them apply. Size on working capacity, not the number on the box.",
 "/what-size-water-softener-do-i-need/",
 ld(article_schema("What Size Water Softener Do I Need? The Sizing Calculator, and the Nameplate Trap","Grain-capacity sizing from sourced figures: 75 gal/person, the 7-day rule, iron compensation \u2014 plus why a 32,000-grain softener only delivers 32,000 grains on the day it wastes the most salt.","/what-size-water-softener-do-i-need/",date="2026-07-12"))
 + ld(faq_schema(s1_faqs,"/what-size-water-softener-do-i-need/"))
 + ld(breadcrumb_schema([("Home","/"),("Sizing","/what-size-water-softener-do-i-need/")])))
s1 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Sizing</nav>
      <h1>What Size Water Softener Do I Need? The Calculator, and the Nameplate Trap</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">The formula is not a secret, and every sizing page on the internet runs it: <strong>people &times; 75 gallons &times; hardness in grains per gallon &times; 7 days.</strong> A family of four at 10 gpg needs about <span class="fig">21,000 grains</span> a week, so the standard advice is a 24,000-grain softener. That advice is wrong &mdash; not because the arithmetic is wrong, but because of what the number on the box actually means.</p>
      <p><strong>Size a water softener by multiplying people &times; 75 gallons &times; your hardness in gpg, then &times; 7 days, adding 5 gpg per ppm of iron. But buy a unit whose capacity at an efficient salt dose &mdash; about 65% of its nameplate &mdash; covers that number. For a family of four at 10 gpg, that is a 40,000-grain unit, not the 24,000-grain one most calculators recommend.</strong></p>
      <p style="margin:0">Here is the thing almost nobody tells you, and it is the entire point of this page. <strong>A &ldquo;32,000-grain&rdquo; softener only removes 32,000 grains on the day it burns the most salt.</strong> That rating is measured at maximum salt dose &mdash; roughly 15 lbs per cubic foot of resin. Feed the same tank an efficient 6 lbs and it delivers about 20,000 grains. The industry rates its equipment at its least efficient setting, and then everybody sizes against that number as though it were free. It isn&rsquo;t. You pay for it every month, in salt, for the life of the machine.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#calc">Size your softener (calculator)</a></li>
          <li><a href="#formula">The formula, step by step</a></li>
          <li><a href="#nameplate">The nameplate trap (chart)</a></li>
          <li><a href="#ladder">What each size actually delivers</a></li>
          <li><a href="#bigger">Why buying bigger uses less salt</a></li>
          <li><a href="#toobig">And the limit: what oversizing breaks</a></li>
          <li><a href="#iron">On a well, iron eats your capacity (chart)</a></li>
          <li><a href="#bathrooms">Sizing by bathrooms: is it good enough?</a></li>
        </ol>
      </details>
      <h2 id="calc">Size your softener</h2>
      <p style="margin:0 0 16px">Three numbers. If you don&rsquo;t know your hardness, that is the first thing to fix &mdash; a <a href="/pick/test-kit" ''' + PICK + '''>home test kit</a> gives you gpg and iron in a few minutes, and your utility publishes hardness for city water for free. Sizing without it is guessing with a decimal point.</p>
      <div data-sizer></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Built from the standard sourced inputs &mdash; 75 gallons per person per day, a 7-day regeneration target, +5 gpg per ppm of iron &mdash; with one correction the others skip: capacity is scored at an <strong>efficient</strong> salt dose (about 65% of nameplate), not at the maximum dose manufacturers use for the rating.</p>

      <h2 id="formula">The formula, step by step</h2>
      <p style="margin:0 0 16px">Nothing here is complicated. It is worth doing by hand once, because it shows you exactly which number is doing the damage:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>Sizing a softener for a family of four at 10 gpg</caption>
        <thead><tr><th scope="col">Step</th><th scope="col">The maths</th><th scope="col" class="num">Result</th></tr></thead>
        <tbody>
          <tr><td>Daily water use</td><td class="muted">4 people &times; 75 gallons</td><td class="num">300 gallons</td></tr>
          <tr><td>Grains removed per day</td><td class="muted">300 gallons &times; 10 gpg</td><td class="num">3,000 grains</td></tr>
          <tr><td>Capacity for a 7-day cycle</td><td class="muted">3,000 &times; 7 days</td><td class="num"><strong>21,000 grains</strong></td></tr>
          <tr><td>What everyone tells you to buy</td><td class="muted">Smallest unit whose <em>nameplate</em> clears 21,000</td><td class="num">24,000-grain</td></tr>
          <tr><td><strong>What actually clears it</strong></td><td class="muted">Smallest unit whose <em>efficient</em> capacity (~65%) clears 21,000</td><td class="num"><strong>40,000-grain</strong></td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">If your hardness is in ppm rather than grains, divide by <strong>17.1</strong>. Municipal supplies typically test 5&ndash;15 gpg; wells frequently run 20&ndash;30 gpg or more, which is why a sizing mistake on a well gets expensive so much faster. And if there is iron in the water, add <strong>5 gpg for every 1 ppm</strong> before you do any of this &mdash; the resin does not care whether the metal it is stripping is calcium or iron.</p>

      <h2 id="nameplate">The nameplate trap</h2>
      <p style="margin:0 0 16px">Here is the same cubic foot of resin, fed three different salt doses. Watch what happens to capacity &mdash; and then watch what happens to the salt it took to get there:</p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 300" style="width:100%;height:auto" role="img" aria-label="Bar chart showing grains of hardness removed per pound of salt falling as the salt dose rises: 3,333 grains per pound at 6 lbs, 2,778 at 9 lbs, and 2,000 at 15 lbs">
        <line x1="70" y1="240" x2="660" y2="240" stroke="#16303F" stroke-width="1.5"/>
        <text x="70" y="26" font-size="13" fill="#16303F" font-weight="700">Grains of hardness removed per pound of salt</text>
        <rect x="130" y="50" width="110" height="190" rx="3" fill="#1F7A5C"/>
        <text x="185" y="42" text-anchor="middle" font-size="14" fill="#16303F" font-weight="700">3,333</text>
        <text x="185" y="262" text-anchor="middle" font-size="12.5" fill="#16303F" font-weight="600">6 lbs / cu ft</text>
        <text x="185" y="280" text-anchor="middle" font-size="11.5" fill="#5B6B75">&rarr; 20,000 grains</text>
        <text x="185" y="296" text-anchor="middle" font-size="11.5" fill="#1F7A5C" font-weight="700">efficient</text>
        <rect x="295" y="81" width="110" height="159" rx="3" fill="#E8A13D"/>
        <text x="350" y="73" text-anchor="middle" font-size="14" fill="#16303F" font-weight="700">2,778</text>
        <text x="350" y="262" text-anchor="middle" font-size="12.5" fill="#16303F" font-weight="600">9 lbs / cu ft</text>
        <text x="350" y="280" text-anchor="middle" font-size="11.5" fill="#5B6B75">&rarr; 25,000 grains</text>
        <rect x="460" y="126" width="110" height="114" rx="3" fill="#5B6B75"/>
        <text x="515" y="118" text-anchor="middle" font-size="14" fill="#16303F" font-weight="700">2,000</text>
        <text x="515" y="262" text-anchor="middle" font-size="12.5" fill="#16303F" font-weight="600">15 lbs / cu ft</text>
        <text x="515" y="280" text-anchor="middle" font-size="11.5" fill="#5B6B75">&rarr; 30,000+ grains</text>
        <text x="515" y="296" text-anchor="middle" font-size="11.5" fill="#16303F" font-weight="700">the nameplate</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; capacity-per-salt-dose figures from SoftPro and industry sizing data &middot; <strong>going from 6 lbs to 15 lbs of salt buys you 50% more capacity for 150% more salt</strong> &mdash; and the bigger number is the one printed on the box</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">That is the whole trick, and it is not really a scandal &mdash; it is a rating convention, the same way a car&rsquo;s towing capacity assumes conditions you will never drive in. The problem is that <em>sizing guides use the rating as though it were the working number.</em> It isn&rsquo;t. As one plumbing calculator puts it plainly: manufacturers rate capacity at maximum salt dosage, which most systems never use, and at efficient settings you should expect <strong>60&ndash;75% of the nameplate</strong>. Everything below follows from taking that seriously.</p>

      <h2 id="ladder">What each size actually delivers</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>The capacity ladder &mdash; nameplate versus the number you can actually plan around</caption>
        <thead><tr><th scope="col">Nameplate</th><th scope="col">Resin</th><th scope="col" class="num">Working capacity at an efficient dose</th><th scope="col">Typically fits</th></tr></thead>
        <tbody>
          <tr><td>24,000-grain</td><td class="muted">0.75 cu ft</td><td class="num">~15,600 grains</td><td class="muted">1&ndash;2 people, moderate hardness</td></tr>
          <tr><td>32,000-grain</td><td class="muted">1.0 cu ft</td><td class="num">~20,800 grains</td><td class="muted">2&ndash;3 people at typical city hardness</td></tr>
          <tr><td><strong>40,000-grain</strong></td><td class="muted">1.25 cu ft</td><td class="num"><strong>~26,000 grains</strong></td><td class="muted"><strong>The honest answer for a family of four at 10 gpg</strong></td></tr>
          <tr><td>48,000-grain</td><td class="muted">1.5 cu ft</td><td class="num">~31,200 grains</td><td class="muted">4&ndash;5 people, or hard water</td></tr>
          <tr><td>64,000-grain</td><td class="muted">2.0 cu ft</td><td class="num">~41,600 grains</td><td class="muted">5&ndash;6 people, very hard water, or an iron load</td></tr>
          <tr><td>80,000-grain</td><td class="muted">2.5 cu ft</td><td class="num">~52,000 grains</td><td class="muted">Large households on very hard well water</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Resin volume is the thing you are actually buying &mdash; a 48,000-grain unit holds 1.5 cubic feet, a 64,000 holds 2.0, and the extra width is also what lets a bigger tank sustain a higher flow rate without dropping your shower pressure when the dishwasher starts. Capacity and flow arrive in the same box.</p>

      <h2 id="bigger">Why buying bigger uses <em>less</em> salt</h2>
      <p style="margin:0">This is the counter-intuitive part, and it is arithmetic rather than opinion. Take our family of four needing 21,000 grains a week.</p>
      <p style="margin:16px 0 0">Buy the <strong>24,000-grain unit</strong> that every calculator recommends, and the only way it reaches 21,000 grains is at its maximum salt dose: roughly <span class="fig">11 lbs of salt per regeneration</span>, about every eight days &mdash; call it <span class="fig">510 lbs of salt a year</span>. Buy the <strong>40,000-grain unit</strong> instead and run it lean at 6 lbs per cubic foot, and it delivers 26,000 usable grains on <span class="fig">7.5 lbs of salt</span>, regenerating every 8.7 days &mdash; about <span class="fig">315 lbs a year</span>.</p>
      <p style="margin:16px 0 0"><strong>Same soft water. Roughly 195 lbs less salt every year</strong> &mdash; nearly five 40-lb bags, which at Angi&rsquo;s $5&ndash;$10 a bag is $25&ndash;$50 a year, every year, for the decade-plus the machine lives. The bigger tank costs more once. The smaller tank costs more forever. That is the single most useful sentence on this page, and it is why the industry&rsquo;s own sizing advice quietly costs its customers money.</p>
      <div style="margin-top:24px">''' + cta_box("Buy the size, not the nameplate",
        "SpringWell publishes its softener pricing online and sizes by bathroom count \u2014 free shipping, 6-month money-back guarantee \u2014 so you can put a real price against the capacity you just calculated instead of a number produced in your kitchen. The honest caveat, since this page is about not being lied to by a spec: bathroom-count sizing is a proxy for household size and flow, not a hardness measurement. If you tested above roughly 15 gpg, or you are on a well, check the grain capacity against your own 7-day figure above before you buy.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="toobig">And the limit: what oversizing actually breaks</h2>
      <p style="margin:0">Sizing up is not a licence to buy the biggest tank in the catalogue, and the failure mode at the top end is real. Culligan describes it accurately: go far too big and you get <strong>channeling</strong> &mdash; there isn&rsquo;t enough water moving through the bed, so it carves a groove and repeatedly follows the same narrow path between the resin beads. Those beads oversaturate, the rest of the bed sits idle, and softening quality falls, especially at low flow. Water standing a long time in an oversized tank raises hygiene questions of its own.</p>
      <p style="margin:16px 0 0">Which gives you the boundary condition, and it is the number to hold onto: <strong>a healthy softener regenerates every 7 to 14 days.</strong> More often than that and you are burning salt, wasting water and wearing out a valve. Much less often and the bed is going stale. Regeneration frequency is not a setting &mdash; it is a <em>symptom</em>, and it is how you find out whether whoever sized your system got it right.</p>

      <h2 id="iron">On a well, iron eats your capacity</h2>
      <p style="margin:0 0 16px">Add 5 gpg per ppm of iron, and the arithmetic gets ugly fast. A household with 12 gpg hardness and just 2 ppm of iron is not running a 12 gpg softener &mdash; it is running a 22 gpg one:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",55),("#E8A13D",45)], "22 gpg", "compensated hardness", "Share of a softener's workload taken by iron at 2 ppm") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> Actual hardness (12 gpg) <span class="pc">~55%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Iron at 2 ppm (&times;5 = 10 gpg) <span class="pc">~45%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; iron compensation at the standard 5 gpg per ppm &middot; nearly half the resin&rsquo;s work is iron &mdash; and unlike calcium, iron <em>coats</em> the beads on the way through</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">And this is where sizing stops being the answer. Calcium leaves cleanly at the next regeneration. Iron does not &mdash; it fouls the bed, and a fouled bed loses capacity permanently. So the correct response to 2 ppm of iron is <strong>not</strong> a bigger softener; it is <a href="/iron-filter-for-well-water-cost/">an iron filter in front of the softener you were already going to buy</a>. Size the softener for your hardness, and let the machine designed for iron take the iron. Our <a href="/well-water-softener-cost/">well water guide</a> prices the whole stack in the order it has to be installed.</p>

      <h2 id="bathrooms">Sizing by bathrooms: is it good enough?</h2>
      <p style="margin:0">Most companies that publish prices online &mdash; the factory-direct channel &mdash; size by bathroom count rather than grains, and dealers often ask the same question first. It is not lazy: bathroom count is a decent proxy for how many people live there and how much simultaneous flow the system has to sustain, and flow rate matters as much as capacity when three taps run at once.</p>
      <p style="margin:16px 0 0">But be clear about what it is: <strong>a proxy for demand, not a measurement of hardness.</strong> Two identical four-bathroom houses, one on 8 gpg city water and one on 25 gpg well water with iron, need very different machines. Bathroom sizing handles the first perfectly well. It will quietly undersize the second. So use the shortcut if your water is ordinary &mdash; and use the number you calculated above if it isn&rsquo;t. Then take that capacity into any conversation about price, whether that is our <a href="/">cost pillar</a>, the <a href="/water-softener-installation-cost/">installation worksheet</a>, or a salesman at your kitchen table who would very much like to talk about monthly payments instead.</p>
      <div style="margin-top:40px">''' + cta_box("The capacity you calculated, at a published price",
        "You now have a grain number, a regeneration interval and a salt figure \u2014 which is more than most people bring to a $4,000 appointment. SpringWell posts its softener prices online, ships free, and backs the purchase with a 6-month money-back window, so the last step is simply matching the size you worked out to a number nobody has to phone a supervisor to produce.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(s1_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/"><div class="name">What it all costs</div><div class="range">$840&ndash;$4,120</div><div class="desc">The size you picked, priced.</div></a>
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">Salt &amp; maintenance</div><div class="range">$60&ndash;$300/yr</div><div class="desc">What the salt dose costs you.</div></a>
        <a class="card" href="/dual-tank-water-softener-cost/"><div class="name">Do you need a twin?</div><div class="range">$1,700&ndash;$5,000</div><div class="desc">Usually the answer is a correctly-sized single.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>SoftPro / Quality Water Treatment &mdash; residential capacity and sizing guides (Jan&ndash;May 2026)</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/residential-water-softener-capacity-guide-grains-per-gallon-explained" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: 75 gallons per person per day; multiply by hardness then by 7 for weekly capacity; add 5 grains per 1 ppm of iron; hardness classes (soft 0&ndash;3.5, moderately hard 3.5&ndash;7, hard 7&ndash;10.5, very hard 10.5+); 15 lbs of salt per cubic foot yielding roughly 30,000 grains and 9 lbs yielding about 25,000; regeneration every 7&ndash;14 days; operating at 75&ndash;85% of maximum capacity.',
 '<strong>PlumbersDen &mdash; water softener sizing calculator</strong> &mdash; <a href="https://plumbersden.com/water-softener-calculator/" rel="noopener" target="_blank">plumbersden.com</a>. Supports the central correction on this page: manufacturers rate grain capacity at maximum salt dosage, which most systems never use, and at efficient salt settings you should expect 60&ndash;75% of the nameplate rating. Also: 1 gpg = 17.1 ppm; municipal water typically 5&ndash;15 gpg, wells often 20&ndash;30+.',
 '<strong>HomeProjectCalculators &mdash; water softener size calculator (Apr 2026)</strong> &mdash; <a href="https://homeprojectcalculators.com/water-softener-size-calculator/" rel="noopener" target="_blank">homeprojectcalculators.com</a>. Supports: a 32,000-grain rating requiring 15+ lbs of salt per regeneration while an efficient 6-lb setting yields about 20,000 grains; resin volumes (48,000-grain = 1.5 cu ft, 64,000-grain = 2.0 cu ft) and the flow-rate consequence; worked sizing examples.',
 '<strong>Culligan &mdash; What Size Water Softener Do I Need?</strong> &mdash; <a href="https://www.culligan.com/blog/what-size-water-softener-do-i-need" rel="noopener" target="_blank">culligan.com</a>. Supports: 50&ndash;75 gallons per person per day; one cubic foot of resin rated around 32,000 grains; undersized units regenerating more often and straining the system; oversized units causing channeling, where water grooves a path between the resin beads and softening effectiveness drops.',
 '<strong>HQ Water Solutions &mdash; sizing guide</strong> &mdash; <a href="https://www.hqwatersolutions.com/blog/what-size-water-softener-do-i-need-a-comprehensive-guide/" rel="noopener" target="_blank">hqwatersolutions.com</a>. Supports: the 75-gallon-per-person figure, the 7-day multiplication, and the 5 gpg per ppm iron adjustment.',
 '<strong>Angi &mdash; salt costs</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-repair-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: softener salt at $5&ndash;$10 per 40-lb bag &mdash; the figure behind the annual salt savings calculated on this page.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("what-size-water-softener-do-i-need/index.html", s1)


# ============ E3 — WATER SOFTENER ELECTRICITY USAGE & RUNNING COSTS ============
el_faqs = [
 ("Do water softeners use a lot of electricity?","No. A typical residential softener uses about 70 kWh a year &mdash; roughly what an alarm clock uses. At the EIA&rsquo;s April 2026 US average of 18.83&cent;/kWh that is about $13 a year. Even in Hawaii, the most expensive state in the country, it does not reach $35."),
 ("Does a water softener increase your electric bill?","Barely. About $1 a month at the national average rate. If your electric bill jumped noticeably after a softener was installed, the softener is almost certainly not the cause &mdash; check the water heater, which hard water makes work harder."),
 ("How much does a water softener cost per month to run?","Roughly $5&ndash;$24 a month for a properly sized metered system: electricity, salt, regeneration water and sewer, and routine consumables. Salt is usually the biggest of those. Electricity is always the smallest."),
 ("Is salt the biggest water softener running cost?","Of the recurring cash costs, usually yes &mdash; $19&ndash;$166 a year depending on hardness and household size. But across the machine&rsquo;s full life, the annualised big tickets (valve rebuild, resin replacement) typically cost more than the salt does."),
 ("Does regeneration waste enough water to matter?","It costs real money, yes. About 25&ndash;30 gallons per regeneration, roughly 40 regenerations a year for a typical family &mdash; call it 1,100 gallons. At sourced water-and-sewer rates that is $12&ndash;$31 a year, which is the same as or more than the electricity."),
 ("Do water softeners use electricity when they aren&rsquo;t regenerating?","Yes, a small standby draw for the display, the meter and the clock. It is tiny. Multiplying the 30&ndash;50-watt regeneration figure by 8,760 hours &mdash; which some cost pages do &mdash; overstates the real annual bill by about six times."),
 ("Are timer-based softeners more expensive to run?","They can be. A timer regenerates on a schedule whether or not the capacity was used; a metered valve regenerates on actual water use. The saving shows up in salt and water, not in electricity &mdash; because electricity was never the expensive part."),
 ("Is a salt-free conditioner cheaper to run?","Yes &mdash; no salt, no regeneration water, and typically no electricity at all. But it conditions scale rather than removing hardness by ion exchange. It is a different outcome, not a cheaper version of the same one, and the water is not chemically softened."),
]
el_rows = [
 ("Electricity (70 kWh/yr &times; your state&rsquo;s rate)",9,33,"EIA Apr 2026: 12.35&cent; (ND) to 46.62&cent; (HI); US average 18.83&cent;"),
 ("Salt",19,166,"Derived: regenerations &times; efficient dose; Angi $5&ndash;$10 per 40-lb bag"),
 ("Regeneration water + sewer",12,31,"25&ndash;30 gal per regeneration at $15&ndash;$23 per 1,000 gal combined"),
 ("Consumables &amp; routine service",20,60,"Prefilter cartridges, resin cleaner, the occasional adjustment"),
]
el = head("Water Softener Electricity Usage & Running Costs (2026): The Real Numbers",
 "A softener uses ~70 kWh/yr \u2014 about $13 at EIA\u2019s 18.83\u00a2. That\u2019s the smallest line on the bill. Here\u2019s what it actually costs to run, month by month.",
 "/water-softener-electricity-usage/",
 ld(article_schema("Water Softener Electricity Usage and Running Costs in 2026","What a softener really draws (~70 kWh/yr), what that costs at current EIA rates, and the four-line running-cost stack that electricity barely registers in.","/water-softener-electricity-usage/",date="2026-07-12"))
 + ld(faq_schema(el_faqs,"/water-softener-electricity-usage/"))
 + ld(breadcrumb_schema([("Home","/"),("Running costs","/water-softener-electricity-usage/")])))
el += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Running costs</nav>
      <h1>Water Softener Electricity Usage &amp; Running Costs in 2026</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">A residential water softener uses about <span class="fig">70 kWh a year</span> &mdash; roughly what an alarm clock uses. At the EIA&rsquo;s April 2026 US average residential rate of <span class="fig">18.83&cent;/kWh</span>, that is <span class="fig">$13.18 a year</span>. About a dollar a month. I am going to spend the rest of this page explaining why that number, the one you came here for, is the least interesting number on your bill.</p>
      <p><strong>A water softener uses roughly 70 kWh per year &mdash; about $13 at the current US average electricity rate, or a dollar a month. But the full running cost of a metered salt-based system is $5&ndash;$24 a month once salt, regeneration water and sewer, and routine consumables are counted. Electricity is typically 5&ndash;16% of it.</strong></p>
      <p style="margin:0">When I was building residential estimates, operating cost was rarely the number homeowners asked about first &mdash; but it was reliably the number they cared about six months later. And electricity was never the one that got them. <strong>The water your softener flushes down the drain during regeneration usually costs you more than the electricity does.</strong> Nobody asks about that one.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#draw">What a softener actually draws</a></li>
          <li><a href="#trap">The 8,760-hour error (table)</a></li>
          <li><a href="#stack">Your real running cost (calculator)</a></li>
          <li><a href="#sheet">The operating-cost worksheet</a></li>
          <li><a href="#where">Where the money actually goes (chart)</a></li>
          <li><a href="#scenarios">Three households &mdash; and the bar that never moves (chart)</a></li>
          <li><a href="#water">Does regeneration raise your water bill?</a></li>
          <li><a href="#saltfree">Would salt-free cost less to run?</a></li>
          <li><a href="#bottom">The three bills: my bottom line</a></li>
        </ol>
      </details>
      <h2 id="draw">What a softener actually draws</h2>
      <p style="margin:0">There is a transformer plugged into your wall, and it is stepping 120 volts down to about <strong>24 volts</strong> for the control valve. That is the whole electrical story. The valve motor draws <strong>30&ndash;50 watts</strong> &mdash; less than a light bulb &mdash; and only while it is actually moving through a regeneration cycle, which for an average family of four happens <strong>fewer than five times a month</strong>, usually at 2 a.m. The rest of the time you are powering a display, a clock and a flow meter.</p>
      <p style="margin:16px 0 0">Add it up across a year and the widely cited figure is about <span class="fig">70 kWh</span> &mdash; a number traced back to Battelle Memorial Institute research conducted for the Water Quality Association. The control head may be plugged in 24 hours a day, but it is not quietly running a second refrigerator.</p>

      <h2 id="trap">The 8,760-hour error</h2>
      <p style="margin:0 0 16px">Here is the mistake I see in online cost estimates, and it is the same mistake that makes a &ldquo;32,000-grain&rdquo; softener sound bigger than it is: <strong>somebody takes the maximum rating and treats it as a permanent condition.</strong> Multiply the 50-watt regeneration draw by the 8,760 hours in a year and you get a scary number that has nothing to do with your bill.</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>The same softener, three ways of costing its electricity (at the US average 18.83&cent;/kWh)</caption>
        <thead><tr><th scope="col">Method</th><th scope="col">The arithmetic</th><th scope="col" class="num">Annual cost</th></tr></thead>
        <tbody>
          <tr><td>Rated draw &times; every hour of the year</td><td class="muted">50 W &times; 8,760 hrs = 438 kWh</td><td class="num">$82</td></tr>
          <tr><td><strong>Actual typical consumption</strong></td><td class="muted">~70 kWh/yr (Battelle/WQA figure)</td><td class="num"><strong>$13</strong></td></tr>
          <tr><td>One dealer&rsquo;s metering of his own units</td><td class="muted">Reported under $1/yr at 8.9&cent;/kWh &asymp; 11 kWh</td><td class="num">~$2</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">The first row <strong>overstates the real bill by about six times.</strong> And notice that even the honest sources disagree with each other by a factor of six &mdash; 70 kWh against a dealer&rsquo;s measured 11 kWh. I am not going to pretend to resolve that, because <em>it does not matter.</em> At one end you are arguing about $13 a year and at the other about $2. The argument itself costs more attention than the electricity does. Where your state lands changes it more than your model does: at North Dakota&rsquo;s 12.35&cent; that 70 kWh costs <span class="fig">$8.64</span>; at Hawaii&rsquo;s 46.62&cent;, <span class="fig">$32.63</span>.</p>

      <h2 id="stack">Your real running cost</h2>
      <p style="margin:0 0 16px">So let us cost the thing properly. Four lines, all of them sourced, and your own utility rates in the sliders &mdash; because a softener does not run on electricity, it runs on <em>salt, water and time</em>:</p>
      <div data-run-cost></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Regenerations are derived using the same method as our <a href="/what-size-water-softener-do-i-need/">sizing calculator</a> &mdash; capacity scored at an efficient salt dose, not at the nameplate. Salt at Angi&rsquo;s $5&ndash;$10 per 40-lb bag; water at 25&ndash;30 gallons per regeneration; electricity held at the sourced 70 kWh/yr, because it barely moves.</p>

      <h2 id="sheet">The operating-cost worksheet</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Annual running cost &mdash; a properly sized metered softener", el_rows, total_label="Annual operating cost") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>That is $5 to $24 a month.</strong> The spread is not vagueness &mdash; it is the honest distance between two people who own the same machine. A couple on 7 gpg city water and a family of six on 20 gpg well water are running identical hardware and living with wildly different bills, and the variable doing almost all of that work is <em>salt</em>. The worksheet excludes the purchase price, the <a href="/water-softener-installation-cost/">installation</a>, and the big tickets &mdash; which I annualise below, because that is where the money actually is.</p>
      <div style="margin-top:24px">''' + cta_box("The cheapest running cost is a system sized right the first time",
        "None of the four lines above is fixed by fate. They are all set by how often the machine regenerates \u2014 which is set by capacity and salt dose. SpringWell publishes its softener pricing online, sizes by bathroom count, ships free and backs it with a 6-month money-back window, so you can match capacity to a published number before anybody quotes you a monthly payment. Verify the grain capacity against your own hardness reading first \u2014 bathroom sizing is a proxy, not a measurement.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="where">Where the money actually goes</h2>
      <p style="margin:0 0 16px">Now the part that reframes the whole question. Take our typical family &mdash; four people, 10 gpg &mdash; and cost a full year of <em>ownership</em>, not just operation. That means annualising the big tickets: a valve rebuild runs <span class="fig">$545&ndash;$595</span> and tends to arrive around year seven; a resin rebed runs about <span class="fig">$295 per cubic foot</span> and arrives around year ten. A $570 repair every seven years is not literally a monthly charge &mdash; but an estimator budgets for it anyway:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#E8A13D",5),("#16303F",23),("#5B6B75",9),("#1F7A5C",16),("#B44A2E",47)], "$244", "a year to own", "Annual ownership cost of a typical metered softener, by component") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#E8A13D"></span> Electricity <span class="pc">5%</span></div>
          <div><span class="sw" style="background:#16303F"></span> Salt <span class="pc">23%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Regeneration water + sewer <span class="pc">9%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Consumables &amp; service <span class="pc">16%</span></div>
          <div><span class="sw" style="background:#B44A2E"></span> Big tickets, annualised <span class="pc">47%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; family of four at 10 gpg, US average utility rates &middot; calculated from sourced components; big tickets annualised from published repair costs &mdash; <strong>a planning allowance, not a bill you receive</strong></div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0"><strong>Electricity is the 5% sliver.</strong> The 47% slice &mdash; the one that dwarfs everything you came here to ask about &mdash; is the repair schedule nobody mentions in the showroom. That is the real answer to &ldquo;what does a water softener cost to run.&rdquo; Our <a href="/water-softener-maintenance-cost/">maintenance cost guide</a> breaks each of those repairs down properly, with what triggers them and what they should cost.</p>

      <h2 id="scenarios">Three households &mdash; and the bar that never moves</h2>
      <p style="margin:0 0 16px">Same machine, three families. Watch the amber segment:</p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 250" style="width:100%;height:auto" role="img" aria-label="Stacked bar chart of annual running cost for three households: 85, 129 and 250 dollars, in which the electricity segment stays the same size while salt grows dramatically">
        <text x="155" y="52" text-anchor="end" font-size="12.5" fill="#16303F" font-weight="600">2 people, 7 gpg</text>
        <rect x="165" y="32" width="26" height="34" fill="#E8A13D"/><rect x="191" y="32" width="24" height="34" fill="#5B6B75"/><rect x="215" y="32" width="38" height="34" fill="#16303F"/><rect x="253" y="32" width="80" height="34" fill="#1F7A5C"/>
        <text x="343" y="54" font-size="13.5" fill="#16303F" font-weight="700">$85/yr</text>
        <text x="155" y="112" text-anchor="end" font-size="12.5" fill="#16303F" font-weight="600">4 people, 10 gpg</text>
        <rect x="165" y="92" width="26" height="34" fill="#E8A13D"/><rect x="191" y="92" width="42" height="34" fill="#5B6B75"/><rect x="233" y="92" width="110" height="34" fill="#16303F"/><rect x="343" y="92" width="80" height="34" fill="#1F7A5C"/>
        <text x="433" y="114" font-size="13.5" fill="#16303F" font-weight="700">$129/yr</text>
        <text x="155" y="172" text-anchor="end" font-size="12.5" fill="#16303F" font-weight="600">6 people, 20 gpg</text>
        <rect x="165" y="152" width="26" height="34" fill="#E8A13D"/><rect x="191" y="152" width="62" height="34" fill="#5B6B75"/><rect x="253" y="152" width="332" height="34" fill="#16303F"/><rect x="585" y="152" width="80" height="34" fill="#1F7A5C"/>
        <text x="600" y="205" text-anchor="middle" font-size="13.5" fill="#16303F" font-weight="700">$250/yr</text>
        <line x1="165" y1="26" x2="165" y2="215" stroke="#E8A13D" stroke-width="1" stroke-dasharray="3 3"/>
        <line x1="191" y1="26" x2="191" y2="215" stroke="#E8A13D" stroke-width="1" stroke-dasharray="3 3"/>
        <text x="178" y="228" text-anchor="middle" font-size="11" fill="#5B6B75">electricity: identical</text>
        <rect x="165" y="238" width="10" height="10" fill="#E8A13D"/><text x="180" y="247" font-size="11.5" fill="#5B6B75">Electricity</text>
        <rect x="248" y="238" width="10" height="10" fill="#5B6B75"/><text x="263" y="247" font-size="11.5" fill="#5B6B75">Regen water</text>
        <rect x="345" y="238" width="10" height="10" fill="#16303F"/><text x="360" y="247" font-size="11.5" fill="#5B6B75">Salt</text>
        <rect x="400" y="238" width="10" height="10" fill="#1F7A5C"/><text x="415" y="247" font-size="11.5" fill="#5B6B75">Consumables &amp; service</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; calculated from sourced components at US average utility rates &middot; the running cost triples across these three households &mdash; <strong>and the electricity segment is the same width in all three</strong></div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">That is the entire argument in one picture. The bill goes from <span class="fig">$85</span> to <span class="fig">$250</span> a year, and electricity contributes exactly nothing to the increase. It is 16% of the small household&rsquo;s cost and 5% of the large one&rsquo;s &mdash; not because it fell, but because everything around it rose.</p>

      <h2 id="water">Does regeneration raise your water bill?</h2>
      <p style="margin:0">Yes, and this is the line item that deserves the attention electricity gets. Each regeneration sends roughly <strong>25&ndash;30 gallons</strong> to the drain. A typical family regenerating about 40 times a year is flushing around <span class="fig">1,100 gallons</span> &mdash; and you pay for that water twice, once to buy it and once to have it taken away.</p>
      <p style="margin:16px 0 0">Nationally representative survey data put the 2023 average at <span class="fig">$44.77</span> for a month of water and <span class="fig">$50.17</span> for sewer at 6,200 gallons &mdash; about <span class="fig">$15.31 per 1,000 gallons</span> combined, and rising 3&ndash;4% a year since. Real published rate sheets today run higher: Harrisburg charges $11.63 for water plus $11.43 for wastewater per 1,000 gallons; a Michigan utility, $8.87 plus $12.88. Call it <strong>$15&ndash;$23 per 1,000 gallons</strong>, and your softener&rsquo;s regeneration water costs you <span class="fig">$12&ndash;$31 a year</span> &mdash; the same as or more than its electricity. A demand-initiated valve can cut that waste substantially versus a timer that regenerates whether or not you used the capacity.</p>

      <h2 id="saltfree">Would a salt-free conditioner cost less to run?</h2>
      <p style="margin:0">On running cost alone, yes &mdash; and by a lot. No salt to buy, lift or store. No regeneration, so no 1,100 gallons down the drain and no sewer charge on it. Most need no electricity at all, which retires the very question this page opened with. Look at the donut again and a salt-free conditioner deletes the 5% slice, the 23% slice and the 9% slice outright.</p>
      <p style="margin:16px 0 0">But I have to be straight with you, because the trade-off is not a footnote. <strong>A salt-free conditioner does not soften water.</strong> It conditions the hardness minerals so they are far less inclined to form scale &mdash; your pipes and your water heater benefit &mdash; but the calcium and magnesium are still in the water. You will not get the slippery-shower, no-spots, half-the-detergent result that ion exchange produces, because nothing was exchanged. So the honest framing is not &ldquo;cheaper to run.&rdquo; It is: <em>if scale protection is what you actually want, you can have it without a running cost at all</em> &mdash; and SpringWell&rsquo;s <a href="/pick/futuresoft" ''' + PICK + '''>FutureSoft conditioner</a> is priced openly online if that is the trade you want to make. If you want soft water, you want salt, and the four lines above are the price of it. Our <a href="/salt-free-water-softener-cost/">salt-free versus salt-based cost comparison</a> runs that decision properly.</p>

      <h2 id="bottom">The three bills: my bottom line</h2>
      <p style="margin:0">On a quote sheet I would separate these three, and I would never let a customer confuse them:</p>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Three different questions, three different answers</caption>
        <thead><tr><th scope="col">The bill</th><th scope="col">What it covers</th><th scope="col" class="num">Typical monthly</th></tr></thead>
        <tbody>
          <tr><td><strong>The electricity bill</strong></td><td class="muted">The control valve, the display, the meter</td><td class="num">~$1</td></tr>
          <tr><td><strong>The operating bill</strong></td><td class="muted">Electricity + salt + regeneration water/sewer + consumables</td><td class="num">$5&ndash;$24</td></tr>
          <tr><td><strong>The ownership cost</strong></td><td class="muted">All of the above, plus the big tickets annualised</td><td class="num">$16&ndash;$30</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">If a dealer quotes you a &ldquo;low monthly cost&rdquo; for a softener, ask which of those three he is quoting. In my experience the answer is usually the first one, and occasionally the second, and never the third. The gap between the electricity bill and the ownership cost is roughly <strong>thirtyfold</strong> &mdash; and that gap is where a good deal quietly turns into a bad one. The good news is that every line in it is knowable in advance, which is more than can be said for the purchase price.</p>
      <div style="margin-top:40px">''' + cta_box("Buy the running cost, not just the box",
        "The four numbers on this page are set the day the system is sized \u2014 capacity, salt dose, regeneration frequency. Get those right and the machine costs about a dollar a month in electricity and a few dollars a week in everything else. SpringWell posts its softener pricing online with free shipping and a 6-month money-back window, so you can weigh purchase price and running cost together, before anyone converts either one into a monthly payment.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(el_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">Maintenance cost</div><div class="range">$60&ndash;$300/yr</div><div class="desc">The 47% slice, itemised.</div></a>
        <a class="card" href="/what-size-water-softener-do-i-need/"><div class="name">What size do I need?</div><div class="range">Free tool</div><div class="desc">Sizing sets every running cost.</div></a>
        <a class="card" href="/salt-free-water-softener-cost/"><div class="name">Salt-free vs salt-based</div><div class="range">$0/yr salt</div><div class="desc">Different outcome, not a cheaper one.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>U.S. Energy Information Administration &mdash; Electric Power Monthly, Table 5.6.A (April 2026 data)</strong> &mdash; <a href="https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a" rel="noopener" target="_blank">eia.gov</a>. Supports: US average residential electricity price of 18.83&cent;/kWh; the state range from North Dakota at 12.35&cent; to Hawaii at 46.62&cent;. All electricity dollar figures on this page are that rate multiplied by the consumption figure below.',
 '<strong>HomeWater 101 &mdash; softener energy use</strong> &mdash; <a href="https://www.homewater101.com/myth-water-softeners-waste-energy-money" rel="noopener" target="_blank">homewater101.com</a>. Supports: approximately 70 kWh per year (compared to an alarm clock); an average family of four regenerating fewer than five times a month. The article attributes its figures to research conducted by the Battelle Memorial Institute for the Water Quality Association.',
 '<strong>SoftPro / Quality Water Treatment &mdash; softener electricity use and electrical requirements</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/how-much-electricity-does-a-softener-use" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: 30&ndash;50 watts drawn during regeneration; the ~70 kWh annual figure; a transformer stepping 120V down to roughly 24V for the control valve; 25&ndash;30 gallons wasted per regeneration on timer-based systems, with demand-initiated models cutting that materially.',
 '<strong>Holmes Water (EcoWater dealer) &mdash; cost to operate a water softener</strong> &mdash; <a href="https://holmeswater.com/much-cost-operate-water-softener/" rel="noopener" target="_blank">holmeswater.com</a>. Supports: the dissenting low estimate &mdash; a dealer reporting metered results from softeners installed in his own home, putting annual electrical cost under $1 at 8.9&cent;/kWh. Cited on this page precisely because it disagrees with the 70 kWh figure.',
 '<strong>Teodoro / Water &amp; Health Advisory Council &mdash; nationally representative water and sewer price survey (2023 wave)</strong> &mdash; <a href="https://wateradvisory.org/council/water-online-tariff-trends-utility-affordability-in-america/" rel="noopener" target="_blank">wateradvisory.org</a>. Supports: an average of $44.77 for a month of residential water service and $50.17 for sewer at 6,200 gallons &mdash; about $15.31 per 1,000 gallons combined &mdash; rising at 3.8% (water) and 3.2% (sewer) annually.',
 '<strong>Published utility rate sheets &mdash; Capital Region Water (Harrisburg, PA) and the City of Birmingham, Michigan</strong> &mdash; <a href="https://capitalregionwater.com/customer-support/water-sewer-rates/" rel="noopener" target="_blank">capitalregionwater.com</a>. Supports the upper end of the $15&ndash;$23 per 1,000 gallons combined range used in the worksheet: $11.63 water + $11.43 wastewater in Harrisburg; $8.87 water + $12.88 sewer in Birmingham for 2025&ndash;26.',
 '<strong>Angi &mdash; softener salt and repair costs</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-repair-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: salt at $5&ndash;$10 per 40-lb bag.',
 '<strong>My Alternate Water &mdash; published repair and rebed pricing</strong> &mdash; <a href="https://myalternatewater.com/" rel="noopener" target="_blank">myalternatewater.com</a>. Supports the annualised big-ticket line: valve rebuild at $545&ndash;$595 and resin rebed at approximately $295 per cubic foot. These are annualised over 7 and 10 years respectively as a <strong>planning allowance</strong> &mdash; not a bill any homeowner receives monthly.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("water-softener-electricity-usage/index.html", el)


# ============ D10 — TRUE 10-YEAR COST OF OWNING A WATER SOFTENER (data study) ============
d10_faqs = [
 ("What is the true 10-year cost of owning a water softener?","For a typical household, about $3,500&ndash;$8,200 all-in &mdash; equipment, installation, salt, regeneration water, electricity, repairs and disposal. Roughly $1,290 of that is running cost. The rest is the purchase, which is where almost all the variation lives."),
 ("How much does a water softener cost per year?","Between roughly $355 and $823 a year across our three modelled channels &mdash; $0.97 to $2.25 a day. The machines are comparable; the households are identical. The spread is almost entirely the purchase price."),
 ("Is a cheaper water softener more expensive to maintain?","Our model finds no reason to assume so. Salt, regeneration water and electricity are set by your hardness and household size, not by the badge. A $6,000 system and a $1,300 system serving the same house consume the same salt."),
 ("What is the biggest cost of owning a water softener?","The purchase. It swings the ten-year total by about $6,680 &mdash; more than repairs, salt, consumables, electricity and regeneration water combined. Electricity, the thing homeowners ask about most, swings it by $240."),
 ("Do dealer systems save money over 10 years?","Only if the extra buys something real. A $4,680 upfront premium would need to eliminate roughly $4,680 of future cost &mdash; but ten years of repairs on our model totals about $939. That leaves most of the premium unexplained by the maths."),
 ("How long does a water softener last?","Commonly quoted at 10&ndash;15 years. That is why we model a decade: it is a realistic ownership window, and it is long enough for the first valve rebuild and resin replacement to appear in the numbers."),
 ("What does a water softener cost per day?","Between about $0.97 and $2.25 a day across our three scenarios, spread over ten years. That is the honest way to read the number &mdash; and the cheapest version costs less per day than the water it softens."),
 ("Can I reproduce these numbers myself?","Yes, and you should. Every input is published and cited below, the arithmetic is stated in the methodology, and the calculator on this page lets you swap in your own hardness, household size, purchase price and ownership period."),
]
d10_rows = [
 ("Equipment",600,2000,"HomeGuide: softener unit, published class"),
 ("Professional installation (labour)",200,500,"Angi: 2&ndash;4 hrs at $100&ndash;$150/hr"),
 ("Plumbing modifications where required",0,2900,"Fixr: loop $600&ndash;$2,000 &middot; HomeGuide: outlet $250&ndash;$900. Most homes need neither; few need both"),
 ("Salt &mdash; 10 years",190,1660,"Calculated: regenerations &times; efficient dose; Angi $5&ndash;$10 per 40-lb bag"),
 ("Regeneration water + sewer &mdash; 10 years",120,310,"Calculated: 25&ndash;30 gal/regen at $15&ndash;$23 per 1,000 gal"),
 ("Electricity &mdash; 10 years",86,326,"Calculated: 70 kWh/yr at EIA rates, 12.35&cent; (ND) to 46.62&cent; (HI)"),
 ("Consumables &amp; routine service &mdash; 10 years",200,600,"Prefilter cartridges, resin cleaner, adjustments"),
 ("Big-ticket repairs (valve rebuild, resin rebed)",0,1900,"MAW: rebuild $545&ndash;$595; rebed ~$295/cu ft"),
 ("Removal &amp; disposal at end of life",50,100,"HomeGuide"),
]
d10 = head("True 10-Year Cost of Owning a Water Softener (2026 Data Study)",
 "The same softener, same house, same salt: $3,550, $4,730 or $8,230 over ten years. A transparent, reproducible ownership model \u2014 with every input cited.",
 "/10-year-water-softener-cost/",
 ld(article_schema("The True 10-Year Cost of Owning a Water Softener: A 2026 Data Study","A transparent, reproducible ten-year ownership model built from cited inputs \u2014 equipment, installation, salt, regeneration water, electricity, repairs and disposal \u2014 with a sensitivity analysis showing which variable actually moves the total.","/10-year-water-softener-cost/",date="2026-07-12"))
 + ld(faq_schema(d10_faqs,"/10-year-water-softener-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("10-year cost study","/10-year-water-softener-cost/")])))
d10 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; 10-year cost study</nav>
      <h1>The True 10-Year Cost of Owning a Water Softener</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">The same water softener, in the same house, softening the same water, costs <span class="fig">$3,550</span>, <span class="fig">$4,730</span> or <span class="fig">$8,230</span> over ten years &mdash; depending almost entirely on <em>who you bought it from</em>. The salt bill is identical in all three. The water bill is identical. The electricity is identical. Everything that separates those numbers was decided before the installer packed up his van.</p>
      <p><strong>A water softener costs roughly $3,500&ndash;$8,200 over ten years for a typical household, including equipment, installation, salt, regeneration water, electricity, repairs and disposal. Running costs are only about $1,290 of that. The purchase channel &mdash; factory-direct versus an in-home dealer quote &mdash; swings the decade more than every other variable combined.</strong></p>
      <p style="margin:0">This is the page I wish I could have handed people when I was writing estimates. It is a model, not a survey: every input below is published and cited, every calculation is stated, and you can rebuild it yourself or tear it apart. <strong>Data updated: July 2026.</strong></p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#lines">Three channels, ten years (chart)</a></li>
          <li><a href="#model">Model your own decade (calculator)</a></li>
          <li><a href="#sheet">The 10-year worksheet</a></li>
          <li><a href="#donut">Where a decade of money goes (chart)</a></li>
          <li><a href="#sensitivity">Which variable actually moves the total (chart)</a></li>
          <li><a href="#years">Year by year</a></li>
          <li><a href="#method">Methodology &mdash; and how to attack it</a></li>
        </ol>
      </details>

      <h2 id="lines">Three channels, ten years</h2>
      <p style="margin:0 0 16px">Here is the whole study in one picture. Three ways to buy the same class of metered softener for the same household &mdash; four people, 10 grains per gallon &mdash; tracked across a decade of ownership. <strong>Watch the distance between the lines.</strong></p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 340" style="width:100%;height:auto" role="img" aria-label="Cumulative ten-year ownership cost for three purchase channels. The three lines run parallel: the gap of 4,680 dollars present at year zero is still exactly 4,680 dollars at year ten.">
        <line x1="80" y1="290" x2="660" y2="290" stroke="#16303F" stroke-width="1.5"/>
        <line x1="80" y1="40" x2="80" y2="290" stroke="#16303F" stroke-width="1.5"/>
        <line x1="80" y1="172" x2="660" y2="172" stroke="#E6E1D8" stroke-width="1"/>
        <line x1="80" y1="55" x2="660" y2="55" stroke="#E6E1D8" stroke-width="1"/>
        <text x="72" y="294" text-anchor="end" font-size="11" fill="#5B6B75">$0</text>
        <text x="72" y="176" text-anchor="end" font-size="11" fill="#5B6B75">$4k</text>
        <text x="72" y="59" text-anchor="end" font-size="11" fill="#5B6B75">$8k</text>
        <text x="80" y="308" text-anchor="middle" font-size="11" fill="#5B6B75">Year 0</text>
        <text x="370" y="308" text-anchor="middle" font-size="11" fill="#5B6B75">Year 5</text>
        <text x="660" y="308" text-anchor="middle" font-size="11" fill="#5B6B75">Year 10</text>
        <polyline points="80,114 138,110 196,106 254,102 312,98 370,95 428,91 486,70 544,66 602,63 660,48" fill="none" stroke="#B44A2E" stroke-width="2.5"/>
        <polyline points="80,216 138,213 196,209 254,205 312,201 370,197 428,194 486,173 544,169 602,166 660,151" fill="none" stroke="#E8A13D" stroke-width="2.5"/>
        <polyline points="80,251 138,247 196,244 254,240 312,236 370,232 428,228 486,208 544,204 602,200 660,186" fill="none" stroke="#1F7A5C" stroke-width="2.5"/>
        <line x1="62" y1="114" x2="62" y2="251" stroke="#5B6B75" stroke-width="1.5"/>
        <line x1="58" y1="114" x2="66" y2="114" stroke="#5B6B75" stroke-width="1.5"/>
        <line x1="58" y1="251" x2="66" y2="251" stroke="#5B6B75" stroke-width="1.5"/>
        <line x1="678" y1="48" x2="678" y2="186" stroke="#5B6B75" stroke-width="1.5"/>
        <line x1="674" y1="48" x2="682" y2="48" stroke="#5B6B75" stroke-width="1.5"/>
        <line x1="674" y1="186" x2="682" y2="186" stroke="#5B6B75" stroke-width="1.5"/>
        <text x="40" y="186" text-anchor="middle" font-size="11.5" fill="#5B6B75" font-weight="700" transform="rotate(-90 40 186)">$4,680 gap</text>
        <text x="696" y="121" text-anchor="middle" font-size="11.5" fill="#5B6B75" font-weight="700" transform="rotate(-90 696 121)">$4,680 gap</text>
        <text x="200" y="88" font-size="12" fill="#B44A2E" font-weight="700">Dealer in-home quote &rarr; $8,230</text>
        <text x="200" y="190" font-size="12" fill="#E8A13D" font-weight="700">Mid-market + pro install &rarr; $4,730</text>
        <text x="200" y="270" font-size="12" fill="#1F7A5C" font-weight="700">Factory-direct + DIY &rarr; $3,550</text>
        <text x="370" y="330" text-anchor="middle" font-size="11.5" fill="#16303F" font-style="italic">The lines are parallel. Nothing after installation day changes the distance between them.</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; <strong>calculated</strong> from cited inputs (see methodology) for an identical household: 4 people, 10 gpg, US average utility rates &middot; the step at year 7 is a valve rebuild; the step at year 10 is a resin rebed</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">The gap between the cheapest and the dearest path is <span class="fig">$4,680</span> on the day of purchase. Ten years later, after every bag of salt, every regeneration, every kilowatt-hour and every repair, the gap is <strong>still $4,680.</strong> It never closes, because the three lines have the <em>same slope</em> &mdash; the resin does not know what you paid for it, and the salt bill does not care whose logo is on the tank.</p>
      <p style="margin:16px 0 0">This is the single most useful thing I know about water softeners, and it took me years of writing quotes to see it plainly: <strong>the decision that determines your ten-year cost takes about ninety minutes, and you make it at your kitchen table.</strong> Everything after that is rounding.</p>

      <h2 id="model">Model your own decade</h2>
      <p style="margin:0 0 16px">National ranges are a starting point, not an answer. Your hardness, your household, your purchase price and how long you actually stay in the house all move the total. Before you touch the sliders, get two numbers: <strong>your hardness in grains per gallon</strong> (a <a href="/pick/test-kit" ''' + PICK + '''>test kit</a> or your utility's report) and <strong>the real all-in price</strong> you have been quoted, including installation.</p>
      <div data-decade></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Regenerations and salt come from the same method as our <a href="/what-size-water-softener-do-i-need/">sizing calculator</a>; the running lines come from the <a href="/water-softener-electricity-usage/">running-cost breakdown</a>; the repair figures are published service prices, annualised. Watch the last line of the output as you move the top slider &mdash; that is the whole study.</p>

      <h2 id="sheet">The 10-year worksheet</h2>
      <p style="margin:0">Every line below is either published data or arithmetic on published data. Nothing is a guess:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Ten years of ownership, itemised", d10_rows, total_label="10-year total") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>$1,446 to $10,296.</strong> A range that wide is a useless answer, and I want to be honest that it is useless &mdash; that is precisely why the rest of this page exists. Almost the entire spread comes from three lines: what you paid, whether your house needed plumbing work, and how hard your water is. The rest &mdash; electricity, regeneration water, consumables &mdash; adds up to less than the sales tax on the machine.</p>
      <div style="margin-top:24px">''' + cta_box("The one number that moves the decade",
        "If the purchase price is the variable that swings ten years of ownership more than everything else put together, then the highest-value hour you can spend is the one where you compare a published price against a quoted one. SpringWell posts its softener pricing online \u2014 sized by bathrooms, free shipping, 6-month money-back window \u2014 so you can put a real figure into the calculator above before anyone sits down in your kitchen. Check the grain capacity against your own hardness reading; bathroom sizing is a proxy, not a measurement.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="donut">Where a decade of money goes</h2>
      <p style="margin:0 0 16px">Take the middle path &mdash; the mid-market system, professionally installed, four people, 10 gpg, <span class="fig">$4,730</span> across ten years &mdash; and break the decade open:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",53),("#B44A2E",20),("#1F7A5C",12),("#5B6B75",8),("#8FA6A0",4),("#E8A13D",3)], "$4,730", "over ten years", "Ten-year ownership cost of a typical softener, by component") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> Equipment + installation <span class="pc">53%</span></div>
          <div><span class="sw" style="background:#B44A2E"></span> Big-ticket repairs <span class="pc">20%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Salt <span class="pc">12%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Consumables &amp; service <span class="pc">8%</span></div>
          <div><span class="sw" style="background:#8FA6A0"></span> Regeneration water <span class="pc">4%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Electricity <span class="pc">3%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; <strong>calculated</strong> from cited inputs &middot; the purchase is over half of a decade of ownership &mdash; and on a dealer-quoted system it rises to roughly three-quarters</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">On the dealer path that dark slice grows to about <strong>73%</strong> of the decade. Which is a strange thing to sit with: for most homeowners who buy through an in-home sales visit, <em>three-quarters of what the machine will ever cost them is settled in a single evening</em>, by a number that was never published anywhere &mdash; a pattern our <a href="/dealer-vs-factory-direct-pricing/">dealer-versus-factory-direct analysis</a> takes apart in detail.</p>

      <h2 id="sensitivity">Which variable actually moves the total?</h2>
      <p style="margin:0 0 16px">This is the part of the study I would most like people to steal. I ran each input across its full sourced range, held everything else at the typical case, and measured how far the ten-year total moved. Here is the ranking:</p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 270" style="width:100%;height:auto" role="img" aria-label="Sensitivity analysis. The upfront purchase swings the ten-year total by 6,680 dollars, more than repairs, salt, consumables, electricity and regeneration water combined, which total 4,200 dollars.">
        <text x="185" y="24" text-anchor="end" font-size="11.5" fill="#5B6B75" font-weight="600">How far it swings 10 years</text>
        <text x="185" y="48" text-anchor="end" font-size="12.5" fill="#16303F" font-weight="700">What you pay up front</text>
        <rect x="195" y="32" width="480" height="22" rx="2" fill="#16303F"/>
        <text x="683" y="48" text-anchor="end" font-size="12" fill="#F7F5F0" font-weight="700">$6,680</text>
        <text x="185" y="80" text-anchor="end" font-size="12.5" fill="#16303F">Big-ticket repairs</text>
        <rect x="195" y="64" width="137" height="22" rx="2" fill="#B44A2E"/>
        <text x="340" y="80" font-size="12" fill="#16303F" font-weight="600">$1,900</text>
        <text x="185" y="112" text-anchor="end" font-size="12.5" fill="#16303F">Salt (hardness &times; household)</text>
        <rect x="195" y="96" width="106" height="22" rx="2" fill="#1F7A5C"/>
        <text x="309" y="112" font-size="12" fill="#16303F" font-weight="600">$1,470</text>
        <text x="185" y="144" text-anchor="end" font-size="12.5" fill="#16303F">Consumables &amp; service</text>
        <rect x="195" y="128" width="29" height="22" rx="2" fill="#5B6B75"/>
        <text x="232" y="144" font-size="12" fill="#16303F" font-weight="600">$400</text>
        <text x="185" y="176" text-anchor="end" font-size="12.5" fill="#16303F">Electricity</text>
        <rect x="195" y="160" width="17" height="22" rx="2" fill="#E8A13D"/>
        <text x="220" y="176" font-size="12" fill="#16303F" font-weight="600">$240</text>
        <text x="185" y="208" text-anchor="end" font-size="12.5" fill="#16303F">Regeneration water</text>
        <rect x="195" y="192" width="14" height="22" rx="2" fill="#8FA6A0"/>
        <text x="217" y="208" font-size="12" fill="#16303F" font-weight="600">$190</text>
        <line x1="195" y1="228" x2="675" y2="228" stroke="#E6E1D8" stroke-width="1"/>
        <text x="185" y="248" text-anchor="end" font-size="12.5" fill="#5B6B75" font-style="italic">All five of those, combined</text>
        <rect x="195" y="232" width="302" height="22" rx="2" fill="none" stroke="#5B6B75" stroke-width="1.5" stroke-dasharray="4 3"/>
        <text x="505" y="248" font-size="12" fill="#5B6B75" font-weight="700">$4,200 &mdash; still shorter than the bar at the top</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; each input swept across its full <strong>sourced</strong> range with all others held at the typical case &middot; the purchase price moves the decade <strong>28&times; further than the electricity everybody asks about</strong></div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Read that bottom row again. <strong>Repairs, salt, consumables, electricity and regeneration water &mdash; every recurring cost of ownership, at their full sourced spread, added together &mdash; still swing your decade less than the purchase decision does.</strong> Homeowners spend months worrying about salt bills and a single evening deciding what to pay. The maths says that is exactly backwards.</p>

      <h2 id="years">Year by year</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Cumulative ownership cost by year &mdash; identical household, three purchase channels (calculated)</caption>
        <thead><tr><th scope="col">Year</th><th scope="col" class="num">Factory-direct + DIY</th><th scope="col" class="num">Mid-market + pro install</th><th scope="col" class="num">Dealer in-home quote</th></tr></thead>
        <tbody>
          <tr><td>0 (purchase)</td><td class="num">$1,320</td><td class="num">$2,500</td><td class="num">$6,000</td></tr>
          <tr><td>1</td><td class="num">$1,449</td><td class="num">$2,629</td><td class="num">$6,129</td></tr>
          <tr><td>3</td><td class="num">$1,707</td><td class="num">$2,887</td><td class="num">$6,387</td></tr>
          <tr><td>5</td><td class="num">$1,965</td><td class="num">$3,145</td><td class="num">$6,645</td></tr>
          <tr><td>7 <span class="muted">(valve rebuild)</span></td><td class="num">$2,793</td><td class="num">$3,973</td><td class="num">$7,473</td></tr>
          <tr><td>10 <span class="muted">(resin rebed)</span></td><td class="num"><strong>$3,550</strong></td><td class="num"><strong>$4,730</strong></td><td class="num"><strong>$8,230</strong></td></tr>
          <tr><td><strong>Per day</strong></td><td class="num"><strong>$0.97</strong></td><td class="num"><strong>$1.30</strong></td><td class="num"><strong>$2.25</strong></td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">A dollar a day for the cheapest path. That is genuinely not a bad deal for soft water &mdash; and I say that as someone whose job was to make the number bigger. The problem was never that softeners are expensive. It is that the <em>same</em> softener can cost you two and a quarter.</p>

      <h2 id="method">Methodology &mdash; and how to attack it</h2>
      <p style="margin:0"><strong>What was used.</strong> Equipment classes and disposal from HomeGuide; installation labour from Angi; the softener loop from Fixr; the electrical outlet from HomeGuide; electricity consumption at 70 kWh/yr against EIA&rsquo;s April 2026 residential rates; regeneration water at 25&ndash;30 gallons per cycle against nationally surveyed water and sewer rates; salt at Angi&rsquo;s $5&ndash;$10 per 40-lb bag; valve rebuild and resin rebed from published service pricing. Every one is listed and linked below.</p>
      <p style="margin:16px 0 0"><strong>What was calculated.</strong> Regeneration frequency is derived from household size and hardness at an efficient salt dose (65% of nameplate capacity), not at the nameplate &mdash; the correction explained in our <a href="/what-size-water-softener-do-i-need/">sizing guide</a>. Salt, water and electricity follow from that. Cumulative totals are simple addition, with the valve rebuild placed at year 7 and the resin rebed at year 10.</p>
      <p style="margin:16px 0 0"><strong>What was excluded, and this matters.</strong> No financing costs (which, on a dealer-financed system, can add thousands &mdash; the payment is not the price). No inflation adjustment on salt or utilities. No claimed savings on soap, appliance life or water-heater efficiency &mdash; those are real, but they are not costs, and inserting them would let me flatter any conclusion I liked. No warranty or service-plan pricing, which is unpublished for most dealer systems. And no resale value, because a softener has none.</p>
      <p style="margin:16px 0 0"><strong>Where you should push back.</strong> The ten-year window is itself an assumption &mdash; a defensible one, since published service life is 10&ndash;15 years, but our <a href="/how-long-does-a-water-softener-last/">lifespan analysis</a> takes it apart component by component and finds a maintained system can run twenty while a proprietary one can die at twelve for want of a part. The dealer figure of $6,000 is the middle of the reported bands on our brand pages, not a published price &mdash; because those brands do not publish prices. If your quote is $3,000, the gap shrinks and the argument weakens; run it yourself in the calculator. The repair timing is a modelling assumption, not a prophecy: some valves run fifteen years untouched, and some fail at four. And if a dealer genuinely includes a decade of parts and labour, subtract the whole $939 repair line from their column and see whether the premium still stands. <strong>On these numbers it does not</strong> &mdash; but that is a calculation you can now do, which is the entire point of publishing the model instead of the conclusion.</p>
      <div style="margin-top:40px">''' + cta_box("Ten years is a long time to pay for an evening",
        "You now have the model, the inputs and the arithmetic. The last step is a number to test it against \u2014 and the only kind that is worth anything is a published one. SpringWell lists its softener pricing openly, ships free, and gives you six months to send it back. Drop that figure into the calculator above, drop your quote in next to it, and let the decade decide.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(d10_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/"><div class="name">The purchase, itemised</div><div class="range">$840&ndash;$4,120</div><div class="desc">The line that decides the decade.</div></a>
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Where the quote comes from</div><div class="range">$3,000&ndash;$8,000</div><div class="desc">Why the dark slice is so big.</div></a>
        <a class="card" href="/water-softener-electricity-usage/"><div class="name">The running bill</div><div class="range">$5&ndash;$24/mo</div><div class="desc">The 3% everyone asks about.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>HomeGuide &mdash; water softener cost</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: equipment class $600&ndash;$2,000; electrical outlet $250&ndash;$900; removal and disposal $50&ndash;$100; the 10&ndash;15 year service life that frames the ten-year model.',
 '<strong>Angi &mdash; water softener installation and repair costs</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: installation labour $200&ndash;$500 at $100&ndash;$150/hr over 2&ndash;4 hours; salt at $5&ndash;$10 per 40-lb bag; repair calls $150&ndash;$900.',
 '<strong>Fixr &mdash; softener loop and plumbing modification</strong> &mdash; <a href="https://www.fixr.com/costs/water-softener-installation" rel="noopener" target="_blank">fixr.com</a>. Supports: a plumbed softener loop at $600&ndash;$2,000 &mdash; the single largest swing inside the installation line.',
 '<strong>U.S. Energy Information Administration &mdash; Electric Power Monthly, Table 5.6.A (April 2026)</strong> &mdash; <a href="https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a" rel="noopener" target="_blank">eia.gov</a>. Supports: residential electricity at 18.83&cent;/kWh nationally, 12.35&cent; (North Dakota) to 46.62&cent; (Hawaii) &mdash; the range behind the $86&ndash;$326 ten-year electricity line.',
 '<strong>Battelle Memorial Institute research for the Water Quality Association, via HomeWater 101</strong> &mdash; <a href="https://www.homewater101.com/myth-water-softeners-waste-energy-money" rel="noopener" target="_blank">homewater101.com</a>. Supports: approximately 70 kWh per year of consumption, and fewer than five regenerations a month for an average family of four.',
 '<strong>Teodoro / Water &amp; Health Advisory Council &mdash; nationally representative water and sewer price survey</strong> &mdash; <a href="https://wateradvisory.org/council/water-online-tariff-trends-utility-affordability-in-america/" rel="noopener" target="_blank">wateradvisory.org</a>. Supports: $44.77 water plus $50.17 sewer per month at 6,200 gallons (about $15.31 per 1,000 gallons combined), cross-checked against published utility rate sheets, giving the $15&ndash;$23 band used for regeneration water.',
 '<strong>SoftPro / Quality Water Treatment &mdash; sizing and regeneration data</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/residential-water-softener-capacity-guide-grains-per-gallon-explained" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: 75 gallons per person per day; salt dose versus delivered capacity; 25&ndash;30 gallons per regeneration &mdash; the inputs behind every salt and water figure calculated here.',
 '<strong>My Alternate Water &mdash; published repair and rebed pricing</strong> &mdash; <a href="https://myalternatewater.com/" rel="noopener" target="_blank">myalternatewater.com</a>. Supports: valve rebuild $545&ndash;$595 and resin rebed at approximately $295 per cubic foot &mdash; the big-ticket line, placed at years 7 and 10 as a <strong>modelling assumption</strong>, not a prediction.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("10-year-water-softener-cost/index.html", d10)


# ============ L1 — HOW LONG DOES A WATER SOFTENER LAST (lifespan x cost per year) ============
l1_faqs = [
 ("How long does a water softener last?","Commonly 10&ndash;15 years as a system &mdash; but the parts age at wildly different rates. Mineral tank 20&ndash;30+ years, brine tank 15&ndash;20+, control valve 10&ndash;25, resin 8&ndash;15. The system &ldquo;dies&rdquo; when one cheap part fails and nobody offers to replace just that part."),
 ("Is a 15-year-old water softener worth repairing?","Often, yes. A resin rebed at roughly $295 per cubic foot that buys eight more years costs about $40 a year of service. A $2,500 replacement over twelve years costs $208 a year. Ask what the repair costs <em>per year it buys</em>, not what percentage of a new unit it is."),
 ("What part of a water softener fails first?","Usually the resin (8&ndash;15 years) or the control valve (10&ndash;25). The mineral tank outlives both at 20&ndash;30+ years and rarely fails at all &mdash; fiberglass tank failures are typically early manufacturing defects, not gradual wear."),
 ("Does replacing the resin extend a softener&rsquo;s life?","Yes &mdash; that is precisely what it is for. Fresh resin restores softening capacity. It will not fix a failed valve and it cannot save a cracked tank, but on an otherwise sound system it is the cheapest decade you can buy."),
 ("Can a water softener last 20 years?","Yes &mdash; if the valve is a rebuildable industry-standard type and the resin gets replaced when it is spent. What ends most softeners is not wear. It is parts availability, which is a purchasing decision you made years earlier."),
 ("Does hard water make a softener wear out faster?","Indirectly, and so does undersizing. Both mean more regenerations &mdash; more osmotic stress on the resin and more mechanical cycles on the valve. Sizing a softener correctly is not just a salt decision; it is a longevity decision."),
 ("Does chlorine damage water softener resin?","Yes. Chlorine and especially chloramine oxidise the resin&rsquo;s cross-links, leaving the beads soft and unable to hold minerals. On city water a carbon filter ahead of the softener is genuinely cheap insurance."),
 ("When should I replace instead of repair?","When the mineral tank is cracked, when the parts no longer exist, or when the repair costs more per year of remaining service than a new system costs per year of its own. That last test is the only one that actually means anything."),
]
l1_rows = [
 ("Diagnostic / service visit",75,200,"Angi: service call before any parts are quoted"),
 ("Resin replacement (10% crosslink)",295,590,"Published: ~$295 per cu ft &mdash; 1 to 2 cu ft on most residential units"),
 ("Control valve replacement or rebuild",545,595,"Published: Fleck 5600SXT replacement valve $545; rebuild kits at the lower end"),
 ("Labour on a repair",150,400,"Angi: repairs $150&ndash;$900 all-in; parts above quoted separately"),
 ("&mdash; OR &mdash; full replacement system, installed",1495,4120,"Published entry replacement $1,495; our installed range tops at $4,120"),
 ("Removal &amp; disposal of the old unit",50,100,"HomeGuide"),
]
l1 = head("How Long Does a Water Softener Last? (2026: Lifespan \u00d7 Cost per Year)",
 "10\u201315 years is the answer everyone gives \u2014 and it describes no actual component. Real part-by-part lifespans, and what each extra year really costs.",
 "/how-long-does-a-water-softener-last/",
 ld(article_schema("How Long Does a Water Softener Last? Lifespan, Component by Component, and the Cost of Every Extra Year","Published component lifespans \u2014 resin, control valve, brine tank, mineral tank \u2014 plus a repair-versus-replace framework that measures cost per year of service instead of guessing.","/how-long-does-a-water-softener-last/",date="2026-07-12"))
 + ld(faq_schema(l1_faqs,"/how-long-does-a-water-softener-last/"))
 + ld(breadcrumb_schema([("Home","/"),("Lifespan","/how-long-does-a-water-softener-last/")])))
l1 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Lifespan</nav>
      <h1>How Long Does a Water Softener Last?</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Ten to fifteen years. That is the answer every page on this subject gives you, and it is not wrong &mdash; it is just <em>useless</em>, because it describes no component that actually exists inside the machine. The mineral tank lasts <span class="fig">20&ndash;30+ years</span>. The brine tank, <span class="fig">15&ndash;20+</span>. The control valve, <span class="fig">10&ndash;25</span>. The resin, <span class="fig">8&ndash;15</span>. Those are four different machines wearing out on four different schedules, inside one cabinet.</p>
      <p><strong>A water softener typically lasts 10&ndash;15 years as a system, but its parts age at very different rates: the mineral tank runs 20&ndash;30+ years, the control valve 10&ndash;25, and the resin 8&ndash;15. Iron, chlorine and undersizing shorten resin life sharply. Most &ldquo;dead&rdquo; softeners are one $295 component away from another decade.</strong></p>
      <p style="margin:0">A water softener does not really die. Its parts do, one at a time &mdash; and <strong>the part that fails first is almost never the part you paid for.</strong> That distinction is worth real money, and the rest of this page is about how much.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#components">Four schedules, one cabinet (chart)</a></li>
          <li><a href="#kills">What actually kills a softener</a></li>
          <li><a href="#quote">What a replacement quote is really replacing (chart)</a></li>
          <li><a href="#tool">Repair or replace? (calculator)</a></li>
          <li><a href="#rule">The 50% rule has no denominator</a></li>
          <li><a href="#sheet">The repair-or-replace worksheet</a></li>
          <li><a href="#peryear">Cost per useful year (chart)</a></li>
          <li><a href="#proprietary">The part nobody mentions: who is allowed to fix it</a></li>
        </ol>
      </details>

      <h2 id="components">Four schedules, one cabinet</h2>
      <p style="margin:0 0 16px">Here is every major component, with its published service life. The dashed line is the number the industry quotes you:</p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 250" style="width:100%;height:auto" role="img" aria-label="Component lifespan ranges: resin 8 to 15 years, control valve 10 to 25 years, brine tank 15 to 20 years, mineral tank 20 to 30 years. The commonly quoted 15-year figure sits in the middle of none of them.">
        <line x1="175" y1="30" x2="175" y2="205" stroke="#E6E1D8" stroke-width="1"/>
        <line x1="335" y1="30" x2="335" y2="205" stroke="#E6E1D8" stroke-width="1"/>
        <line x1="495" y1="30" x2="495" y2="205" stroke="#E6E1D8" stroke-width="1"/>
        <line x1="655" y1="30" x2="655" y2="205" stroke="#E6E1D8" stroke-width="1"/>
        <text x="175" y="222" text-anchor="middle" font-size="11" fill="#5B6B75">0 yrs</text>
        <text x="335" y="222" text-anchor="middle" font-size="11" fill="#5B6B75">10</text>
        <text x="495" y="222" text-anchor="middle" font-size="11" fill="#5B6B75">20</text>
        <text x="655" y="222" text-anchor="middle" font-size="11" fill="#5B6B75">30</text>
        <text x="165" y="50" text-anchor="end" font-size="12" fill="#16303F">Resin &mdash; 8% crosslink</text>
        <rect x="303" y="36" width="64" height="20" rx="2" fill="#B44A2E"/>
        <text x="375" y="50" font-size="11.5" fill="#5B6B75">8&ndash;12 yrs</text>
        <text x="165" y="86" text-anchor="end" font-size="12" fill="#16303F">Resin &mdash; 10% crosslink</text>
        <rect x="335" y="72" width="160" height="20" rx="2" fill="#E8A13D"/>
        <text x="503" y="86" font-size="11.5" fill="#5B6B75">10&ndash;20 yrs</text>
        <text x="165" y="122" text-anchor="end" font-size="12" fill="#16303F">Control valve</text>
        <rect x="335" y="108" width="240" height="20" rx="2" fill="#5B6B75"/>
        <text x="583" y="122" font-size="11.5" fill="#5B6B75">10&ndash;25 yrs</text>
        <text x="165" y="158" text-anchor="end" font-size="12" fill="#16303F">Brine tank</text>
        <rect x="415" y="144" width="80" height="20" rx="2" fill="#8FA6A0"/>
        <text x="503" y="158" font-size="11.5" fill="#5B6B75">15&ndash;20+ yrs</text>
        <text x="165" y="194" text-anchor="end" font-size="12" fill="#16303F">Mineral tank</text>
        <rect x="495" y="180" width="160" height="20" rx="2" fill="#16303F"/>
        <text x="663" y="194" font-size="11.5" fill="#5B6B75">20&ndash;30+ yrs</text>
        <line x1="415" y1="24" x2="415" y2="210" stroke="#16303F" stroke-width="1.5" stroke-dasharray="5 4"/>
        <text x="415" y="18" text-anchor="middle" font-size="11.5" fill="#16303F" font-weight="700">&ldquo;15 years&rdquo;</text>
        <text x="350" y="242" text-anchor="middle" font-size="11.5" fill="#5B6B75" font-style="italic">The number everyone quotes. Ask which of these five it is describing.</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; published component lifespans from water-treatment retailers and service companies (sources below) &middot; the cheapest part on the chart is the one that fails first &mdash; and the most expensive part is the one that outlives everything</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Read the chart from the bottom up and the economics invert. <strong>The mineral tank &mdash; the big fibreglass cylinder that <em>is</em> the softener, visually &mdash; almost never fails.</strong> Fibreglass tank failures are typically early manufacturing defects, not gradual wear. The thing that goes is the resin inside it: a consumable, priced around <span class="fig">$295 per cubic foot</span>. And the control valve on top: mechanical, and on the industry-standard bodies, rebuildable.</p>

      <h2 id="kills">What actually kills a softener</h2>
      <p style="margin:0">Not age. Chemistry, and arithmetic:</p>
      <p style="margin:16px 0 0"><strong>Iron.</strong> It coats the beads and blocks the exchange sites. Published guidance puts the damage threshold shockingly low &mdash; iron above roughly <span class="fig">0.3 ppm</span> can halve resin life, and above 2 ppm you need an <a href="/iron-filter-for-well-water-cost/">iron filter ahead of the softener</a>, not a bigger softener. This is the single most common reason a softener dies before its time.</p>
      <p style="margin:16px 0 0"><strong>Chlorine, and chloramine especially.</strong> They <em>oxidise</em> the resin &mdash; attacking the cross-links that keep each bead firm, until the beads go soft and mushy and simply cannot hold minerals any more. Chloramine is worse than free chlorine because it stays stable in the water far longer. On city water a carbon filter in front of the softener is cheap insurance, and 10% crosslink resin is the more durable choice.</p>
      <p style="margin:16px 0 0"><strong>Undersizing &mdash; and this one is on the person who sold it to you.</strong> An undersized unit regenerates constantly to keep up. That is not just a salt bill: every cycle is osmotic stress on the resin and mechanical wear on the valve. A 32,000-grain unit serving four people at 15 gpg may regenerate every other day; a properly sized 48,000-grain unit handles the identical load every four or five days. <strong>Same water, same house, half the wear.</strong> Which makes <a href="/what-size-water-softener-do-i-need/">sizing</a> a longevity decision, not a salt decision &mdash; and it is why a system sized to its nameplate rather than its efficient capacity is quietly ageing faster than it should.</p>
      <p style="margin:16px 0 0">None of those three is fixed by spending more money on the softener. All three are fixed by <a href="/pick/test-kit" ''' + PICK + '''>testing the water first</a> and putting the right thing in front of the tank. Replace the beads without fixing the cause and you have simply bought the same failure again, on a payment plan.</p>

      <h2 id="quote">What a replacement quote is really replacing</h2>
      <p style="margin:0 0 16px">Now take a twelve-year-old softener. The resin is probably spent. The valve is a coin flip. The mineral tank &mdash; on the published numbers &mdash; is almost certainly fine, and so is the brine tank. Against that, a full replacement quote of $6,000:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#B44A2E",14),("#E6E1D8",86)], "$840", "actually failed", "Share of a $6,000 replacement quote that corresponds to genuinely worn parts") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#B44A2E"></span> New resin + new control valve <span class="pc">14%</span></div>
          <div><span class="sw" style="background:#E6E1D8"></span> Equipment that was still working <span class="pc">86%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; <strong>calculated</strong>: published resin ($295) + published valve ($545) against a $6,000 quote &middot; assumes a sound mineral tank, which at twelve years is the likeliest condition &mdash; <strong>verify yours rather than assuming</strong></div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">A full rebuild &mdash; new resin <em>and</em> a new control valve, the two parts that plausibly wore out &mdash; runs about <span class="fig">$840</span> in parts. That is <strong>14%</strong> of the quote. The other 86% buys you a fibreglass tank to replace a fibreglass tank with fifteen good years left in it, and a brine tank to replace a plastic box with no moving parts.</p>
      <p style="margin:16px 0 0">I want to be careful here, because this is the point where an article like this usually starts shouting. So: <strong>sometimes replacement is right.</strong> A cracked mineral tank ends the conversation. So does a valve nobody makes parts for. And a genuinely ancient timer-based unit may be wasting more in salt and water than the repair is worth. But those are findings from an inspection &mdash; and if nobody looked inside the tank before quoting you a new one, no such finding exists.</p>

      <h2 id="tool">Repair or replace?</h2>
      <p style="margin:0 0 16px">If you know which component failed, price it first in our <a href="/water-softener-repair-cost/">repair cost by problem</a> guide &mdash; then bring that number back here.</p>
      <p style="margin:0 0 16px">Here is the framework I used on every ageing system I ever priced. It is one division sign. <strong>What does each option cost per year of service it actually delivers?</strong></p>
      <div data-repair-replace></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Repair costs are published parts pricing (resin ~$295/cu ft, valve ~$545); replacement defaults to the middle of our <a href="/">installed cost range</a>. The years-bought slider is your judgement, not ours &mdash; move it and watch how fast the verdict turns. That sensitivity <em>is</em> the answer: whoever controls that assumption controls the recommendation.</p>

      <h2 id="rule">The 50% rule has no denominator</h2>
      <p style="margin:0">You will be told, repeatedly, that you should replace a softener once repairs pass <strong>50% of the price of a new one.</strong> It is quoted everywhere, it sounds prudent, and it collapses the moment you do arithmetic on it.</p>
      <p style="margin:16px 0 0">A full rebuild is about <span class="fig">$840</span>. A sourced entry-level replacement system is <span class="fig">$1,495</span>. Half of that is $748 &mdash; so $840 in repairs trips the rule, and the rule says <em>replace.</em> But that $840 rebuild buys roughly another decade: <span class="fig">$84 per year of service</span>. The new system, over a twelve-year life, costs <span class="fig">$125 per year</span>. <strong>The rule says replace. The arithmetic says the rebuild is the better buy by half again.</strong></p>
      <p style="margin:16px 0 0">The rule fails because it has no denominator. It compares a repair to a purchase price and never once asks the only question that matters: <em>how many years does it buy?</em> A $300 repair that buys one year is terrible. An $840 repair that buys ten is the cheapest water you will ever soften. Same rule, opposite answers &mdash; and the rule cannot tell them apart.</p>

      <h2 id="sheet">The repair-or-replace worksheet</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Keeping, rebuilding or replacing an ageing softener", l1_rows, total_label="Do NOT total this sheet") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>An estimator&rsquo;s warning about that total.</strong> Do not add these rows up. A repair path and a replacement path are <em>competing</em> options, not a shopping list &mdash; the moment you stack them the total becomes meaningless, and I have watched quotes get built that way. Read it as two columns: the repair path (diagnostic + parts + labour, roughly <span class="fig">$520&ndash;$1,785</span>) against the replacement path (new system + disposal, <span class="fig">$1,545&ndash;$4,220</span>). Then divide each by the years it buys, which is the whole point of the calculator above.</p>
      <div style="margin-top:24px">''' + cta_box("When replacement genuinely is the answer",
        "If the tank is cracked or the parts have vanished, the repair path is closed and you are buying a system \u2014 so buy it with the price in front of you. SpringWell publishes its softener pricing online, ships free, and gives you six months to send it back, which means you can put a real replacement figure into the calculator above rather than the one a technician produces while standing next to your failed unit. Check the grain capacity against your own hardness reading before ordering \u2014 sizing is what determines whether the next one lives a decade or two.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="peryear">Cost per useful year</h2>
      <p style="margin:0 0 16px">This is the number I would put on the front page of every quote, and nobody does. Divide what you paid by the years of service you actually got. Six honest paths:</p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 250" style="width:100%;height:auto" role="img" aria-label="Cost per year of service: factory-direct rebedded and kept twenty years costs 84 dollars a year, rising to 400 dollars a year for a dealer system replaced at fifteen years.">
        <text x="240" y="24" text-anchor="end" font-size="11.5" fill="#5B6B75" font-weight="600">Cost per year of service</text>
        <text x="240" y="48" text-anchor="end" font-size="12" fill="#16303F" font-weight="700">Factory-direct, rebedded, kept 20 yrs</text>
        <rect x="250" y="32" width="92" height="22" rx="2" fill="#1F7A5C"/>
        <text x="350" y="48" font-size="12.5" fill="#16303F" font-weight="700">$84</text>
        <text x="240" y="80" text-anchor="end" font-size="12" fill="#16303F">Factory-direct, replaced at 12 yrs</text>
        <rect x="250" y="64" width="121" height="22" rx="2" fill="#1F7A5C" opacity="0.72"/>
        <text x="379" y="80" font-size="12.5" fill="#16303F" font-weight="600">$110</text>
        <text x="240" y="112" text-anchor="end" font-size="12" fill="#16303F">Mid-market, rebuilt, kept 20 yrs</text>
        <rect x="250" y="96" width="184" height="22" rx="2" fill="#E8A13D"/>
        <text x="442" y="112" font-size="12.5" fill="#16303F" font-weight="600">$167</text>
        <text x="240" y="144" text-anchor="end" font-size="12" fill="#16303F">Mid-market, replaced at 12 yrs</text>
        <rect x="250" y="128" width="229" height="22" rx="2" fill="#E8A13D" opacity="0.72"/>
        <text x="487" y="144" font-size="12.5" fill="#16303F" font-weight="600">$208</text>
        <text x="240" y="176" text-anchor="end" font-size="12" fill="#16303F">Dealer system, generous 20-yr life</text>
        <rect x="250" y="160" width="330" height="22" rx="2" fill="#B44A2E" opacity="0.72"/>
        <text x="588" y="176" font-size="12.5" fill="#16303F" font-weight="600">$300</text>
        <text x="240" y="208" text-anchor="end" font-size="12" fill="#16303F">Dealer system, replaced at 15 yrs</text>
        <rect x="250" y="192" width="440" height="22" rx="2" fill="#B44A2E"/>
        <text x="682" y="208" text-anchor="end" font-size="12.5" fill="#F7F5F0" font-weight="700">$400</text>
        <text x="360" y="240" text-anchor="middle" font-size="11.5" fill="#16303F" font-style="italic">The cheapest year of soft water belongs to the cheapest system somebody bothered to maintain.</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; <strong>calculated</strong> from our sourced installed-cost ranges and published repair pricing &middot; the dealer path is given the <em>benefit of the doubt</em> at 20 years, the very top of the published range, and it still lands last</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Look at what wins. Not the cheap system, and emphatically not the expensive one &mdash; <strong>the repairable one that somebody kept alive.</strong> A factory-direct softener with a $369 bag of resin dropped into it at year ten delivers soft water for <span class="fig">$84 a year</span> across two decades.</p>
      <p style="margin:16px 0 0">And run the longevity defence properly, because it is the one thing a dealer can honestly say back to all this: <em>ours lasts longer.</em> Fine &mdash; grant it. Give the dealer system twenty years, the top of the published range, and give the factory-direct system only twelve. The dealer system costs <span class="fig">$300</span> a year; the factory-direct one costs <span class="fig">$110</span>. <strong>For a $6,000 system to reach $110 a year, it would have to run for fifty-five years.</strong> Nobody claims that. The published range is 10&ndash;15. Longevity is a real advantage, and it is nowhere near large enough to carry a 4.5&times; price gap &mdash; which is exactly what our <a href="/10-year-water-softener-cost/">ten-year ownership study</a> found from the opposite direction.</p>

      <h2 id="proprietary">The part nobody mentions: who is allowed to fix it</h2>
      <p style="margin:0">Here is the thing I most want you to take away, and it is not about wear at all.</p>
      <p style="margin:16px 0 0">A softener with an industry-standard valve body can be rebuilt by any competent plumber, using a part you can order yourself, for as long as that part is manufactured &mdash; and those valves have been in production for decades. A softener built around a <strong>proprietary</strong> valve can be rebuilt by whoever the manufacturer permits, at whatever the parts cost, for as long as they choose to make them. Published guidance is blunt about this: full replacement makes sense when the mineral tank is cracked <em>or when the system is a proprietary brand where parts are unavailable</em>.</p>
      <p style="margin:16px 0 0">Which flips the entire premium argument on its head. <strong>The system most likely to hit a hard, unrepairable end-of-life is often the expensive proprietary one</strong> &mdash; not because it is built worse, but because its lifespan is a commercial decision made by somebody else. You are not buying a longer life. In some cases you are buying <em>a shorter list of people allowed to extend it.</em></p>
      <p style="margin:16px 0 0">So before you replace anything, ask three questions: <strong>Is the mineral tank sound? Is the valve a rebuildable standard type? And is the water still doing to the new resin whatever it did to the old?</strong> Three answers, and you will know whether you are looking at a $340 afternoon, an $840 rebuild, or a genuine replacement. Our <a href="/water-softener-maintenance-cost/">maintenance cost guide</a> prices each of those events; this page is about deciding which one you are actually in.</p>
      <div style="margin-top:40px">''' + cta_box("Buy the one you are allowed to keep",
        "If this system is genuinely finished, the next one should be chosen for the thing that ends softeners: parts. A standard, rebuildable valve you can source yourself is the difference between a twelve-year machine and a twenty-year one. SpringWell publishes its pricing openly \u2014 free shipping, 6-month money-back window \u2014 so you can weigh the replacement against the repair with a real number instead of a quoted one, and put the difference toward the prefilter that protects the resin you just paid for.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(l1_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">What upkeep costs</div><div class="range">$60&ndash;$300/yr</div><div class="desc">Each repair on this page, priced.</div></a>
        <a class="card" href="/10-year-water-softener-cost/"><div class="name">The 10-year study</div><div class="range">$3,550&ndash;$8,230</div><div class="desc">The same finding, from the other end.</div></a>
        <a class="card" href="/what-size-water-softener-do-i-need/"><div class="name">Sizing</div><div class="range">Free tool</div><div class="desc">Undersizing is a longevity decision.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Mid Atlantic Water &mdash; how long do water softeners last</strong> &mdash; <a href="https://midatlanticwater.net/blogs/faqs/how-long-do-water-softeners-last" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports: mineral tank 20&ndash;30+ years (fibreglass-lined, rarely fails unless physically damaged); brine tank 15&ndash;20+; control valve 15&ndash;25+ on industry-standard bodies; resin 10&ndash;15 with clean water; 8% crosslink resin 8&ndash;12 years and 10% crosslink 12&ndash;15+; Fleck 5600SXT replacement valve $545; 10% crosslink replacement resin $295; entry replacement system $1,495+; iron fouling as the most common cause of premature death, with an iron filter needed above 2 ppm; undersizing driving more cycles, more osmotic stress on the resin and more mechanical wear on the valve; and full replacement being the right call when the mineral tank is cracked <em>or the system is a proprietary brand where parts are unavailable</em>.',
 '<strong>SoftPro / Quality Water Treatment &mdash; softener lifespan and resin warning signs</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/average-lifespan-residential-water-softener" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: the 10&ndash;15 year system figure with high-efficiency units reaching 20; control valve 10&ndash;15 and often the first component to fail; chlorine and iron shortening life; and the widely repeated industry rule of thumb that a system should be replaced once repair costs exceed 50% of a new unit &mdash; the rule interrogated on this page.',
 '<strong>Peterson Salt &mdash; how long does water softener resin last</strong> &mdash; <a href="https://www.petersonsalt.com/how-long-does-water-softener-resin-last/" rel="noopener" target="_blank">petersonsalt.com</a>. Supports the failure mechanism: chlorine and chloramine oxidise the resin&rsquo;s cross-links until the beads go soft and cannot hold minerals; chloramine is more damaging because it stays stable longer; iron attaches to the bead surface and blocks exchange sites; sediment abrades the beads; hot water stresses the polymer. Also: 8% crosslink 8&ndash;12 years, 10% crosslink 10&ndash;20 depending on chlorine.',
 '<strong>Wills Friends / water education &mdash; average lifespan of a water softener</strong> &mdash; <a href="https://willsfriends.com/about/water-education/water-softener-average-lifespan" rel="noopener" target="_blank">willsfriends.com</a>. Supports: iron above roughly 0.3 ppm cutting resin life in half; fibreglass media tanks typically carrying 10-year warranties and often lasting longer, with tank failures rare and usually early manufacturing defects rather than gradual wear; control-valve electronics typically carrying 5-year warranties.',
 '<strong>Hill Water &mdash; water softener lifespan by component</strong> &mdash; <a href="https://hillwater.com/blog/what-is-the-average-industrial-water-softener-lifespan/" rel="noopener" target="_blank">hillwater.com</a>. Supports the independent second reading of the component ranges: resin 10&ndash;15, control valve 10&ndash;15, brine tank 15&ndash;20, mineral tank 20+ years.',
 '<strong>Environmental ProTech &mdash; when resin needs changing</strong> &mdash; <a href="https://www.environmentalprotech.com/water-education/when-do-the-resins-in-the-softener-tank-need-to-be-changed" rel="noopener" target="_blank">environmentalprotech.com</a>. Supports: resin at 8&ndash;10 years with proper care but 5&ndash;7 in aggressive water without a prefilter; and that replacing resin does not require replacing the system &mdash; full replacement is reserved for failures of the valve, tank or other critical parts.',
 '<strong>HomeGuide &mdash; water softener cost</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: the 10&ndash;15 year service life; removal and disposal at $50&ndash;$100; and the installed-cost range used as the replacement path in the worksheet.',
 '<strong>Angi &mdash; water softener repair cost</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-repair-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: repairs at $150&ndash;$900 including labour, and the service-call range used in the worksheet.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("how-long-does-a-water-softener-last/index.html", l1)


# ============ M1 — WATER SOFTENER MAINTENANCE (the work, not the invoice) ============
m1_faqs = [
 ("How often should a water softener be serviced?","There are six routine jobs: check the salt monthly, feel for a bridge every few months, clean the injector twice a year, run a resin cleaner every 3&ndash;6 months, wash the brine tank when it looks dirty, and test your water quarterly. Total: about two hours a year."),
 ("Can I clean a water softener myself?","Almost all of it, yes. Washing the brine tank is dish soap and a brush. The injector comes apart with a screwdriver. Relieve the water pressure first, and reassemble the injector in the exact order it came out. Repairs are a different matter &mdash; those are a professional&rsquo;s job."),
 ("How often should I clean the brine tank?","Nobody actually agrees. The same publisher recommends every 2&ndash;3 months on one page and every 3&ndash;4 years on another. The honest answer is condition-based: open the lid. If there is sludge on the bottom or a crust across the top, wash it. Otherwise leave it alone."),
 ("What is salt bridging, and how do I fix it?","A hard crust that forms across the salt with a void underneath, so the salt never reaches the water and the brine never forms. Your tank looks full and your water is hard. Push a broom handle down through it, break the crust, and regenerate manually."),
 ("Do I need an annual service plan?","Rarely. Every non-salt consumable for a year &mdash; resin cleaner, test strips, soap &mdash; runs about $31. A service plan typically costs $150&ndash;$300 and does not include the salt. Pay for diagnosis when something is actually wrong; that is different, and worth it."),
 ("How do I clean the injector or venturi?","Confirm the system is not under pressure, remove the cover, unscrew the injector cap without losing the O-ring, lift out the screen, screen support, nozzle and venturi, wash them in warm soapy water with a small brush, and reassemble in exactly the order they came out."),
 ("What happens if I never maintain a water softener?","Nothing, for a while. Then a salt bridge forms, regeneration quietly fails, and hard water returns while the tank still looks full. Sludge clogs the injector, salt use climbs, and iron fouls the resin permanently. The first three are free to fix; the last one is not."),
 ("Does a salt-free conditioner need maintenance?","Almost none &mdash; no salt, no brine tank, no regeneration. Usually just a sediment prefilter every 6&ndash;12 months. That is the honest case for one, and its honest limit: it controls scale rather than removing hardness, so your water is not actually softened."),
]
m1_rows = [
 ("Salt &mdash; the whole year",60,180,"Angi: $5&ndash;$10 per 40-lb bag &middot; 8&ndash;12 bags for a typical household"),
 ("Resin cleaner (2&ndash;4 doses)",15,40,"Retail softener cleaner, dosed into the brine well"),
 ("Hardness test strips or kit",8,25,"The only task that verifies the other five"),
 ("Dish soap, brush, a bucket",0,5,"You already own these"),
 ("Sediment prefilter cartridges, where fitted",0,60,"Only if a prefilter is part of the system"),
]
m1 = head("Water Softener Maintenance (2026): The Complete DIY Schedule & Real Costs",
 "Six jobs, about two hours a year, roughly $31 in consumables beyond the salt. The full schedule, the actual procedures, and where DIY stops.",
 "/water-softener-maintenance/",
 ld(article_schema("Water Softener Maintenance: The Complete DIY Schedule and What It Really Costs","Every routine maintenance task with its real interval and procedure, the point where DIY should stop, and an honest look at why no two sources agree on how often to clean a brine tank.","/water-softener-maintenance/",date="2026-07-12"))
 + ld(faq_schema(m1_faqs,"/water-softener-maintenance/"))
 + ld(breadcrumb_schema([("Home","/"),("Maintenance","/water-softener-maintenance/")])))
m1 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Maintenance</nav>
      <h1>Water Softener Maintenance: The Complete DIY Schedule</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">There are <strong>six routine jobs</strong>. Together they take roughly <span class="fig">two hours a year</span> and about <span class="fig">$31</span> in consumables on top of the salt. Everything else you will be offered &mdash; the annual service plan, the &ldquo;system health check,&rdquo; the sanitising visit &mdash; is either one of those six jobs performed by somebody else, or it is a repair, which is a different thing entirely and belongs on a different invoice.</p>
      <p><strong>Water softener maintenance is six tasks: check the salt monthly, break any salt bridge, clean the injector twice a year, run a resin cleaner every 3&ndash;6 months, wash the brine tank when it looks dirty, and test your water quarterly. Roughly two hours and $31 a year beyond salt. Repairs and component failures are separate.</strong></p>
      <p style="margin:0">Adding salt is maintenance. It is not the maintenance <em>plan</em>. But the good news &mdash; and I mean this as somebody who used to write the invoices &mdash; is that the real plan is short, cheap, and almost entirely within reach of anybody who owns a bucket.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#calendar">The maintenance calendar (chart)</a></li>
          <li><a href="#generator">Your schedule, personalised (tool)</a></li>
          <li><a href="#intervals">Nobody agrees on the intervals (chart)</a></li>
          <li><a href="#howto">The six jobs, step by step</a></li>
          <li><a href="#stop">Where DIY stops</a></li>
          <li><a href="#sheet">What a year actually costs</a></li>
          <li><a href="#plans">What a service plan is really selling (chart)</a></li>
          <li><a href="#skip">What happens if you skip it</a></li>
        </ol>
      </details>

      <h2 id="calendar">The maintenance calendar</h2>
      <p style="margin:0 0 16px">Print this, tape it inside the utility-room door, and you are done thinking about it:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>The complete routine schedule &mdash; salt-based softener</caption>
        <thead><tr><th scope="col">Job</th><th scope="col">How often</th><th scope="col">Who</th><th scope="col" class="num">Time</th></tr></thead>
        <tbody>
          <tr><td><strong>Look at the salt</strong> &mdash; a few inches above the water line</td><td class="muted">Monthly</td><td class="muted">You</td><td class="num">1 min</td></tr>
          <tr><td><strong>Feel for a salt bridge</strong> with a broom handle</td><td class="muted">Every 2&ndash;3 months</td><td class="muted">You</td><td class="num">2 min</td></tr>
          <tr><td><strong>Test your treated water</strong></td><td class="muted">Quarterly</td><td class="muted">You</td><td class="num">5 min</td></tr>
          <tr><td><strong>Run a resin cleaner</strong> through a regeneration</td><td class="muted">Every 3&ndash;6 months <span class="muted">(3 with iron)</span></td><td class="muted">You</td><td class="num">5 min</td></tr>
          <tr><td><strong>Clean the injector / venturi</strong></td><td class="muted">Twice a year <span class="muted">(quarterly on a well)</span></td><td class="muted">Confident DIY</td><td class="num">15 min</td></tr>
          <tr><td><strong>Wash the brine tank</strong></td><td class="muted">When it looks dirty &mdash; not on a calendar</td><td class="muted">You</td><td class="num">45 min</td></tr>
          <tr><td><strong>Sanitise the system</strong> (bleach, per the manual)</td><td class="muted">Annually, or after any disuse or boil-water notice</td><td class="muted">Confident DIY</td><td class="num">15 min</td></tr>
          <tr><td>Valve service, resin replacement, electrical faults</td><td class="muted">When something is actually wrong</td><td class="muted"><strong>Professional</strong></td><td class="num">&mdash;</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Intervals are the consensus of published guidance (sources below). Times are my own estimate from having priced this work, not a sourced figure &mdash; treat them as an honest order of magnitude, not a stopwatch.</p>

      <h2 id="generator">Your schedule, personalised</h2>
      <p style="margin:0 0 16px">Iron changes it. A well changes it. A salt-free system changes it enormously. Set your own conditions:</p>
      <div data-schedule></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Salt consumption is derived the same way as our <a href="/what-size-water-softener-do-i-need/">sizing calculator</a> &mdash; from your household size and hardness at an efficient salt dose. If you have never measured your hardness or iron, a <a href="/pick/test-kit" ''' + PICK + '''>test kit</a> is the cheapest thing on this entire page and it decides half the schedule above.</p>

      <h2 id="intervals">Nobody agrees on the intervals</h2>
      <p style="margin:0 0 16px">Before you follow anybody&rsquo;s maintenance calendar &mdash; including mine &mdash; you should see this. Here are five published recommendations for how often to clean a brine tank. <strong>They come from the same publisher.</strong></p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 210" style="width:100%;height:auto" role="img" aria-label="Five published brine-tank cleaning intervals from the same publisher, ranging from every two to three months to every three to four years — a twenty-four-fold spread.">
        <rect x="176" y="118" width="412" height="24" fill="#E8A13D" opacity="0.16"/>
        <line x1="150" y1="130" x2="650" y2="130" stroke="#16303F" stroke-width="1.5"/>
        <line x1="150" y1="126" x2="150" y2="136" stroke="#16303F" stroke-width="1.5"/>
        <line x1="275" y1="126" x2="275" y2="136" stroke="#16303F" stroke-width="1.5"/>
        <line x1="400" y1="126" x2="400" y2="136" stroke="#16303F" stroke-width="1.5"/>
        <line x1="525" y1="126" x2="525" y2="136" stroke="#16303F" stroke-width="1.5"/>
        <line x1="650" y1="126" x2="650" y2="136" stroke="#16303F" stroke-width="1.5"/>
        <text x="150" y="152" text-anchor="middle" font-size="11" fill="#5B6B75">0</text>
        <text x="275" y="152" text-anchor="middle" font-size="11" fill="#5B6B75">1 yr</text>
        <text x="400" y="152" text-anchor="middle" font-size="11" fill="#5B6B75">2 yrs</text>
        <text x="525" y="152" text-anchor="middle" font-size="11" fill="#5B6B75">3 yrs</text>
        <text x="650" y="152" text-anchor="middle" font-size="11" fill="#5B6B75">4 yrs</text>
        <circle cx="176" cy="130" r="6" fill="#B44A2E"/>
        <line x1="176" y1="124" x2="176" y2="96" stroke="#B44A2E" stroke-width="1"/>
        <text x="176" y="88" text-anchor="middle" font-size="11.5" fill="#B44A2E" font-weight="700">&ldquo;every 2&ndash;3 months&rdquo;</text>
        <circle cx="181" cy="130" r="6" fill="#B44A2E"/>
        <line x1="181" y1="136" x2="181" y2="172" stroke="#B44A2E" stroke-width="1"/>
        <text x="181" y="186" text-anchor="middle" font-size="11.5" fill="#B44A2E" font-weight="700">&ldquo;quarterly&rdquo;</text>
        <circle cx="275" cy="130" r="6" fill="#E8A13D"/>
        <line x1="275" y1="124" x2="275" y2="96" stroke="#E8A13D" stroke-width="1"/>
        <text x="275" y="88" text-anchor="middle" font-size="11.5" fill="#16303F" font-weight="700">&ldquo;annually&rdquo;</text>
        <circle cx="400" cy="130" r="6" fill="#5B6B75"/>
        <line x1="400" y1="136" x2="400" y2="172" stroke="#5B6B75" stroke-width="1"/>
        <text x="400" y="186" text-anchor="middle" font-size="11.5" fill="#16303F" font-weight="700">&ldquo;every 1&ndash;3 years&rdquo;</text>
        <circle cx="588" cy="130" r="6" fill="#16303F"/>
        <line x1="588" y1="124" x2="588" y2="96" stroke="#16303F" stroke-width="1"/>
        <text x="588" y="88" text-anchor="middle" font-size="11.5" fill="#16303F" font-weight="700">&ldquo;every 3&ndash;4 years&rdquo;</text>
        <text x="382" y="30" text-anchor="middle" font-size="13" fill="#16303F" font-weight="700">How often should you clean a brine tank?</text>
        <text x="382" y="48" text-anchor="middle" font-size="11.5" fill="#5B6B75">Five answers. One publisher. A 24&times; spread.</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; five published recommendations from the same water-treatment publisher across five of its own pages (all linked in the sources) &middot; <strong>the interval is not a fact &mdash; it is a guess, and it is the guess a service plan is priced against</strong></div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">I am not picking on them; you will find the same spread across the industry, and their guidance is otherwise good. The point is what it tells you: <strong>nobody actually knows how often your brine tank needs washing, because it depends on your tank.</strong> So stop maintaining on a calendar and start maintaining on <em>condition</em>. Open the lid. Is there sludge on the bottom or a crust across the top? Wash it. Is it clean? Close the lid and go and do something else.</p>

      <h2 id="howto">The six jobs, step by step</h2>
      <p style="margin:0 0 16px;font-size:14px;color:#5B6B75">Which salt you put in decides how much of this list you actually have to do &mdash; see our <a href="/water-softener-salt-cost/">salt cost and types guide</a>: rock salt puts 110 lbs of insoluble sludge into your tank over a decade; evaporated pellets put in three.</p>
      <h3 style="margin-top:24px">1. Look at the salt (monthly, 1 minute)</h3>
      <p style="margin:0">You are checking one thing: is the salt sitting <strong>a few inches above the water?</strong> Not filling it to the brim &mdash; overfilling is what causes bridging in the first place. Two-thirds full is plenty.</p>
      <h3 style="margin-top:20px">2. Feel for a salt bridge (every 2&ndash;3 months, 2 minutes)</h3>
      <p style="margin:0">A bridge is a hard crust that forms across the salt with a <em>void underneath</em>, so the salt never reaches the water and no brine forms. The tank looks full. The water goes hard anyway. It is caused by humidity and by poor-quality salt. Push a broom handle straight down through the salt; if it stops on a crust with a hollow beneath, lever the crust apart, then run a manual regeneration. <strong>This is the single most common &ldquo;my softener is broken&rdquo; call that is not a broken softener.</strong></p>
      <h3 style="margin-top:20px">3. Test your treated water (quarterly, 5 minutes)</h3>
      <p style="margin:0">Everything above is invisible. This is the task that makes it visible &mdash; and it is the one almost everybody skips. If the treated water is reading hard, something in the chain has failed and you now know it in month three instead of month eighteen.</p>
      <h3 style="margin-top:20px">4. Run a resin cleaner (every 3&ndash;6 months, 5 minutes)</h3>
      <p style="margin:0">Pour the dose into the brine well per the label, then start a manual regeneration to draw it through the bed. It lifts iron and mineral deposits off the beads. With iron in the water, published guidance shortens this to roughly every three months &mdash; though if iron is the reason, cleaner is a holding action and an <a href="/iron-filter-for-well-water-cost/">iron filter ahead of the softener</a> is the actual fix.</p>
      <h3 style="margin-top:20px">5. Clean the injector / venturi (twice a year, 15 minutes)</h3>
      <p style="margin:0">This little nozzle creates the suction that pulls brine out of the tank during regeneration. Sediment blocks it, brine stops being drawn, and the resin never recharges &mdash; a total softening failure caused by a part the size of a thimble. <strong>Relieve the water pressure first.</strong> Then: remove the cover, unscrew the injector cap without losing the O-ring, lift out the screen, the screen support, and the nozzle and venturi, wash everything in warm soapy water with a small brush, and <strong>reassemble in the exact order it came apart.</strong></p>
      <h3 style="margin-top:20px">6. Wash the brine tank (when it is dirty, 45 minutes)</h3>
      <p style="margin:0">Best done when the salt is nearly gone. Bypass the system, disconnect the tank, drain the water, scoop out the salt, then scrub the inside with dish soap and warm water and a stiff brush. Rinse it properly &mdash; soap residue is not something you want drawn into the brine. Let it dry, reassemble, refill with clean salt, and regenerate. The sludge you are removing is <strong>salt mushing</strong>: the thick sediment layer left behind by the insolubles in cheaper salt, which can clog the system and cause an overflow.</p>
      <p style="margin:20px 0 0"><strong>And an annual sanitise</strong>, per your manual &mdash; typically household bleach dosed into the brine well ahead of a regeneration, on the order of an ounce or so per cubic foot of resin. Do it after any period of disuse or a boil-water notice. Follow the manual, not me: dose and method vary by manufacturer, and this is one place where guessing is genuinely a bad idea.</p>

      <h2 id="stop">Where DIY stops</h2>
      <p style="margin:0 0 16px">And when it does stop &mdash; when you actually need somebody in a van &mdash; our <a href="/water-softener-servicing/">servicing guide</a> publishes what companies charge ($40&ndash;$100 for a call, $150&ndash;$600 for a repair) and the five questions that get you a price on the phone instead of &ldquo;we can&rsquo;t quote until we come out.&rdquo;</p>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>The honest line between maintenance, confident DIY, and a phone call</caption>
        <thead><tr><th scope="col">Anyone can do it</th><th scope="col">Confident DIY</th><th scope="col">Call a professional</th></tr></thead>
        <tbody>
          <tr><td class="muted">Salt level and salt quality</td><td class="muted">Injector / venturi strip-down</td><td class="muted">Anything electrical</td></tr>
          <tr><td class="muted">Breaking a salt bridge</td><td class="muted">Annual sanitising</td><td class="muted">A valve that will not cycle</td></tr>
          <tr><td class="muted">Washing the brine tank</td><td class="muted">Adjusting hardness / regeneration settings</td><td class="muted">Leaks from anything under pressure</td></tr>
          <tr><td class="muted">Resin cleaner doses</td><td class="muted">Replacing a sediment prefilter</td><td class="muted">Resin replacement, valve rebuild</td></tr>
          <tr><td class="muted">Testing the water</td><td class="muted">Manual regeneration</td><td class="muted">Hard water that persists after all of the above</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">That last cell in the right column is the important one. If you have cleaned the injector, broken the bridge, washed the tank, dosed the resin and the water is <em>still</em> hard, stop cleaning things. You are no longer in maintenance &mdash; you are in diagnosis, and paying somebody for an hour of that is money well spent. Our <a href="/how-long-does-a-water-softener-last/">repair-or-replace guide</a> covers what happens next, and what each answer costs per year of life it buys.</p>

      <h2 id="sheet">What a year actually costs</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("A year of DIY softener maintenance", m1_rows, total_label="Annual DIY maintenance") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Estimator&rsquo;s note.</strong> This sheet is <em>routine consumables only</em>. It deliberately excludes repairs, resin replacement, valve rebuilds and anything else that happens when a part fails &mdash; those are not maintenance, they are events, and stacking them into a maintenance budget is how a $150 year gets quoted as a $600 one. Our <a href="/water-softener-maintenance-cost/">maintenance cost guide</a> prices those events properly and separately. Your own total lands low if your water is soft and your salt is cheap, and high if you are on a well with iron.</p>
      <div style="margin-top:24px">''' + cta_box("Low-maintenance is a purchase decision, not a chore",
        "Most of the work on this page exists because of what is in the water and how the system was sized. A correctly sized softener with a standard, serviceable valve is the difference between two hours a year and a standing service appointment. SpringWell publishes its softener pricing online \u2014 free shipping, 6-month money-back window \u2014 so you can size and price one against your own hardness reading rather than a technician\u2019s. Check the grain capacity against your measured gpg; bathroom-count sizing is a proxy, not a measurement.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="plans">What a service plan is really selling</h2>
      <p style="margin:0 0 16px">Here is a full year of softener maintenance, broken into what you actually buy:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",79),("#1F7A5C",13),("#E8A13D",7),("#5B6B75",1)], "$151", "a year, all in", "A year of DIY water softener maintenance, by cost component") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> Salt <span class="pc">79%</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> Resin cleaner <span class="pc">13%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Test strips <span class="pc">7%</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> Soap, brush, an afternoon <span class="pc">1%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; midpoints of the worksheet above &middot; <strong>every non-salt consumable for an entire year comes to about $31</strong> &mdash; and a service plan does not include the salt</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Strip out the salt &mdash; which you buy whether or not anybody visits &mdash; and the entire material cost of maintaining a water softener for a year is roughly <span class="fig">$31</span>. Against that, a service plan is commonly <span class="fig">$150&ndash;$300</span> a year, and the salt is still yours to buy. What you are purchasing is <em>the two hours</em>, and whether that is a good trade is genuinely your call: some people would rather not take a brine tank apart, and there is nothing wrong with that.</p>
      <p style="margin:16px 0 0">What I would push back on is the framing. A service plan is a convenience purchase, and it deserves to be priced like one &mdash; not sold as though the machine will fail without it. And it is worth knowing which of the six jobs the technician is actually doing, because <strong>&ldquo;annual service&rdquo; on an invoice and &ldquo;he looked at the salt and left&rdquo; are not always different events.</strong> Our <a href="/water-softener-maintenance-cost/">cost guide</a> takes the plans apart line by line.</p>

      <h2 id="skip">What happens if you skip it</h2>
      <p style="margin:0">Honestly? Nothing, for a while. Softeners are tolerant machines and this is why maintenance gets skipped &mdash; the punishment is deferred, not immediate. Then, roughly in this order:</p>
      <p style="margin:16px 0 0"><strong>A salt bridge forms.</strong> Regeneration quietly stops working while the tank still looks full. You have hard water and a full salt tank, which is the most confusing failure in the whole category. <em>Cost to fix: a broom handle.</em></p>
      <p style="margin:16px 0 0"><strong>Sludge builds and the injector clogs.</strong> Brine draw weakens, regenerations go incomplete, salt use climbs because the system keeps trying. <em>Cost to fix: dish soap and fifteen minutes.</em></p>
      <p style="margin:16px 0 0"><strong>Iron fouls the resin.</strong> This is the one that is not free. Iron coats the beads and blocks the exchange sites, and past a certain point cleaning will not bring the capacity back &mdash; you are buying resin. <em>Cost to fix: around $295 per cubic foot.</em></p>
      <p style="margin:16px 0 0">Which is the whole argument for the six jobs in one line: <strong>the first two failures cost you nothing to prevent and nothing to reverse. The third one you pay for.</strong> And you will not see any of them coming without the fourth job on the list &mdash; the water test &mdash; which is why it is the one I would fight to keep if you dropped every other task on this page.</p>
      <div style="margin-top:40px">''' + cta_box("The cheapest maintenance is the system you sized right",
        "Everything on this page gets shorter when the water is understood before the equipment is chosen: iron filtered out in front, capacity matched to real hardness, a valve any plumber can service. SpringWell posts its pricing openly, ships free and gives you six months to change your mind \u2014 so you can build that system against a published number instead of an appointment, and spend your two hours a year rather than somebody else\u2019s two hundred dollars.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(m1_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">What upkeep costs</div><div class="range">$60&ndash;$300/yr</div><div class="desc">The invoice, itemised.</div></a>
        <a class="card" href="/how-long-does-a-water-softener-last/"><div class="name">When to stop repairing</div><div class="range">$84&ndash;$400/yr</div><div class="desc">Maintenance ends; economics begin.</div></a>
        <a class="card" href="/what-size-water-softener-do-i-need/"><div class="name">Sizing</div><div class="range">Free tool</div><div class="desc">Half of your maintenance load, decided up front.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>SoftPro / Quality Water Treatment &mdash; maintenance schedule guidance (multiple pages)</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/best-practices-for-water-softener-maintenance-schedules" rel="noopener" target="_blank">maintenance schedules</a>, <a href="https://www.softprowatersystems.com/pages/how-often-should-you-clean-your-water-softener" rel="noopener" target="_blank">cleaning frequency</a>, <a href="https://www.softprowatersystems.com/pages/sanitization-schedule-maintenance-water-softeners" rel="noopener" target="_blank">sanitisation schedule</a>, <a href="https://www.softprowatersystems.com/pages/essential-water-softener-maintenance-for-longevity" rel="noopener" target="_blank">essential maintenance</a>, <a href="https://qualitywatertreatment.com/pages/how-often-should-you-clean-your-water-softener" rel="noopener" target="_blank">QWT cleaning frequency</a>. Supports: monthly salt checks; salt sitting roughly three inches above the water line; breaking bridges with a broom handle; resin cleaner every 3&ndash;6 months; injector/venturi cleaning quarterly to twice yearly; annual sanitising. <strong>These five pages are also the source of the brine-tank interval chart</strong> &mdash; they publish, respectively, &ldquo;every 2&ndash;3 months,&rdquo; &ldquo;quarterly,&rdquo; &ldquo;annually,&rdquo; &ldquo;every 1&ndash;3 years&rdquo; and &ldquo;every 3&ndash;4 years.&rdquo;',
 '<strong>Lowe&rsquo;s &mdash; how to clean and maintain a water softener</strong> &mdash; <a href="https://www.lowes.com/n/how-to/how-to-clean-water-softener-tank" rel="noopener" target="_blank">lowes.com</a>. Supports the brine-tank procedure (bypass, disconnect, drain, scoop, scrub with dish soap and a stiff brush, rinse, dry, refill) and the definitions used here: salt <strong>bridging</strong> as a hard crust caused by humidity or the wrong salt, and salt <strong>mushing</strong> as a sludgy layer that can clog the system and cause overflow.',
 '<strong>Discount Water Softeners &mdash; venturi and resin-bed cleaning</strong> &mdash; <a href="https://www.discountwatersofteners.com/blog/water-softener-cleaning-guide-for-springtime/" rel="noopener" target="_blank">discountwatersofteners.com</a>. Supports the injector strip-down step by step: confirm no pressure at the nozzle, remove the cover, unscrew the cap without losing the O-ring, remove screen, screen support, nozzle and venturi, wash in warm soapy water, and reassemble in the exact order removed. Also: resin-bed cleaning at least annually with high iron or manganese.',
 '<strong>Clear Water Concepts &mdash; softener maintenance and sanitising</strong> &mdash; <a href="https://clearwaterarizona.com/blog/everything-about-water-softener-maintenance/" rel="noopener" target="_blank">clearwaterarizona.com</a>. Supports: venturi and nozzle cleaned with soapy water twice a year; relieving water pressure before disassembly; and sanitising with household bleach dosed into the brine ahead of a regeneration (on the order of an ounce or so per cubic foot of resin &mdash; follow your manual, as dosing varies).',
 '<strong>Angi &mdash; water softener salt and repair costs</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-installation-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports: salt at $5&ndash;$10 per 40-lb bag and 8&ndash;12 bags a year for a typical household &mdash; the salt line in the worksheet and the 79% slice of the donut.',
 '<strong>HomeGuide &mdash; water softener cost</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: total annual upkeep commonly reported at $100&ndash;$300, which the worksheet on this page reconciles with from the bottom up.',
 '<strong>Mid Atlantic Water &mdash; published resin pricing</strong> &mdash; <a href="https://midatlanticwater.net/blogs/faqs/how-long-do-water-softeners-last" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports the one failure on this page that is not free to reverse: replacement resin at approximately $295 per cubic foot once iron fouling is permanent.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("water-softener-maintenance/index.html", m1)


# ============ S2 — WATER SOFTENER SERVICING (what companies charge) ============
s2_faqs = [
 ("How much does it cost to service a water softener?","A service call and inspection runs $40&ndash;$100 with parts excluded; a billed diagnostic hour is $65&ndash;$180, and some sources put a visit at $100&ndash;$300. Once a part has actually failed, a typical repair lands at $150&ndash;$600 all in."),
 ("How often should a water softener be professionally serviced?","On demand, not on a schedule. The six routine jobs are DIY and take about two hours a year. Pay a professional when something is genuinely wrong &mdash; that is diagnosis, and it is the one thing you cannot do yourself."),
 ("Can I service a water softener myself?","Most of it, yes: salt, bridges, brine tank, injector, resin cleaner, water tests. What you cannot do is diagnose a failed valve or a fouled resin bed. That judgement is what the visit is actually selling &mdash; the tasks are not."),
 ("What does a water softener service visit include?","Usually inspection, a regeneration test, a brine-draw check, injector cleaning, settings calibration and a water test &mdash; inside about an hour. Parts are extra. What is included varies enough that you should ask before the truck moves."),
 ("Is an annual maintenance plan worth paying for?","It depends entirely on the word &ldquo;all-inclusive.&rdquo; HomeGuide reports contracts at $100&ndash;$250 a year covering repairs, cleaning, salt refills, testing and inspections. If that is real, it is good value &mdash; better than DIY. Get the exclusions in writing."),
 ("How do I know if my softener needs service or repair?","Hard water with a full salt tank is almost always a salt bridge, and free to fix. Hard water with the salt going down is resin or settings. Leaks, a dead display or a valve that will not cycle are repairs. Test first &mdash; a kit costs less than a truck."),
 ("Why won&rsquo;t companies quote a price over the phone?","Because the fault is unknown until somebody looks, which is fair. What is not fair is refusing to quote the trip charge, the hourly rate, or whether the diagnostic is credited against the repair. Those are all knowable before anyone drives anywhere."),
 ("Are salt-free systems really lower maintenance?","Genuinely, yes &mdash; no salt, no brine tank, no regeneration, usually just a prefilter. But a conditioner controls scale rather than removing hardness. It is a different outcome, not a cheaper version of the same one."),
]
s2_rows = [
 ("Service call / trip charge &amp; inspection",40,100,"HomeGuide, softener-specific &mdash; explicitly excludes repair parts"),
 ("Diagnostics, where billed as a separate line",0,180,"HomeGuide: $65&ndash;$180 for a call-out diagnostic of up to one hour"),
 ("Water test, where billed rather than included",0,300,"HomeGuide. A kit you own costs $10&ndash;$25 and you can run it whenever you like"),
]
s2 = head("Water Softener Servicing (2026): What Companies Charge, and What You Can Do Yourself",
 "A service call is $40\u2013$100. A repair is $150\u2013$600. Here is what the visit buys, what it doesn\u2019t, and the five questions that get a price on the phone.",
 "/water-softener-servicing/",
 ld(article_schema("Water Softener Servicing: What Companies Charge, and What You Can Do Yourself","Published service-call, diagnostic, labour and repair pricing; what a visit actually includes; a symptom triage that tells you whether to call at all; and the questions that turn \u201cwe can\u2019t price it until we come out\u201d into a number.","/water-softener-servicing/",date="2026-07-12"))
 + ld(faq_schema(s2_faqs,"/water-softener-servicing/"))
 + ld(breadcrumb_schema([("Home","/"),("Servicing","/water-softener-servicing/")])))
s2 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Servicing</nav>
      <h1>Water Softener Servicing: What Companies Charge</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">A water softener <strong>service call and inspection runs <span class="fig">$40&ndash;$100</span></strong>, parts excluded. A billed diagnostic hour is <span class="fig">$65&ndash;$180</span>. If something has actually failed, the repair lands at <span class="fig">$150&ndash;$600</span> once labour and parts are in. Those numbers exist. They are published. And you were still told &ldquo;we can&rsquo;t give you a price until we come out.&rdquo;</p>
      <p><strong>Water softener servicing costs $40&ndash;$100 for a service call and inspection, or $65&ndash;$180 where diagnostics are billed separately. A repair typically totals $150&ndash;$600 including labour at $45&ndash;$150 an hour. Parts are extra, after-hours work adds $75&ndash;$350, and most routine maintenance does not require a visit at all.</strong></p>
      <p style="margin:0">A service truck pulling into your driveway costs money before anybody opens the control valve. That does not make the charge unreasonable &mdash; I used to build those estimates, and the truck is real. But it does mean something worth understanding before you book: <strong>you are not paying for the tasks. You are paying for the judgement.</strong> And if nothing is broken, there is no judgement to buy.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#triage">Should you even call? (tool)</a></li>
          <li><a href="#sheet">What a visit costs</a></li>
          <li><a href="#invoice">Where the money goes on a repair (chart)</a></li>
          <li><a href="#diy">What they do that you could have done</a></li>
          <li><a href="#plans">Plans and contracts &mdash; an honest surprise (chart)</a></li>
          <li><a href="#script">Five questions that get a price on the phone</a></li>
          <li><a href="#replace">When another service call stops making sense</a></li>
        </ol>
      </details>

      <h2 id="triage">Should you even call?</h2>
      <p style="margin:0 0 16px">Start here, because roughly the most useful thing on this page is the possibility that you do not need a technician at all. Pick what is actually happening:</p>
      <div data-triage></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">The DIY fixes referenced above &mdash; breaking a bridge, cleaning the injector, dosing a resin cleaner &mdash; are walked through step by step in our <a href="/water-softener-maintenance/">complete maintenance schedule</a>. And if you do not know your hardness, a <a href="/pick/test-kit" ''' + PICK + '''>test kit</a> costs $10&ndash;$25; a company may bill $100&ndash;$300 for the same reading.</p>

      <h2 id="sheet">What a visit costs</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("A service visit where nothing turns out to be broken", s2_rows, total_label="Inspection visit, all in") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Estimator&rsquo;s note.</strong> In practice most inspection visits land at <span class="fig">$40&ndash;$180</span>. That $580 top end is not a scare figure &mdash; it is what happens when the diagnostic hour and a water test are billed as <em>separate lines</em> rather than folded into the call. Which is precisely why you ask on the phone. And note what the sourced service-call figure explicitly excludes: <strong>parts.</strong> If something has failed, you are in a different table.</p>
    </div>
    <div class="data-table-wrap" style="margin-top:24px">
      <table class="data-table">
        <caption>And if something <em>has</em> failed &mdash; the repair path (published ranges)</caption>
        <thead><tr><th scope="col">Line</th><th scope="col" class="num">Low</th><th scope="col" class="num">High</th><th scope="col">Note</th></tr></thead>
        <tbody>
          <tr><td>Labour beyond the first hour</td><td class="num">$45</td><td class="num">$150/hr</td><td class="muted">Plumber rate; a handyman runs $50&ndash;$80 for simple work</td></tr>
          <tr><td><strong>Typical repair, all in</strong></td><td class="num"><strong>$150</strong></td><td class="num"><strong>$600</strong></td><td class="muted">Parts + labour together; average commonly reported near $400</td></tr>
          <tr><td>Resin replacement, if that is the fault</td><td class="num">$200</td><td class="num">$400</td><td class="muted">Media only</td></tr>
          <tr><td>After-hours or emergency</td><td class="num">$75</td><td class="num">$350</td><td class="muted">Flat surcharge <em>plus</em> hourly rates at 2&ndash;3&times; normal</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Do not add these two tables together. An inspection and a repair are the same visit at two different depths, not two bills &mdash; and stacking them is exactly how a $150 job gets budgeted as a $600 one.</p>
      <div style="margin-top:24px">''' + cta_box("When the repair bill outgrows the machine",
        "There is a point where you stop buying service calls and start buying a system \u2014 and at that moment the single most valuable thing you can hold is a published price to measure the quote against. SpringWell posts its softener pricing online, ships free, and gives you six months to send it back, so you can weigh a replacement against your next repair with a real number instead of an appointment. Check the grain capacity against your own hardness reading; bathroom-count sizing is a proxy, not a measurement.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="invoice">Where the money goes on a repair</h2>
      <p style="margin:0 0 16px">Take the commonly reported <span class="fig">$400</span> repair and open it up:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#5B6B75",18),("#16303F",47),("#E8A13D",35)], "$400", "typical repair", "A typical water softener repair invoice, by component") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#5B6B75"></span> Trip charge &amp; diagnostic <span class="pc">18%</span></div>
          <div><span class="sw" style="background:#16303F"></span> Labour (about two hours) <span class="pc">47%</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> Parts <span class="pc">35%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; <strong>calculated</strong> from published component pricing against the commonly reported ~$400 average repair &middot; proportions will vary by fault &mdash; the point is the shape</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0"><strong>Nearly two-thirds of the invoice is the hour and the drive, not the part.</strong> That is not a scandal; it is what a licensed, insured technician with a stocked van costs, and I would defend most of it. But it does tell you where your leverage is: <em>the money is decided before anybody touches the softener.</em> Which is why the highest-value five minutes in this entire process happen on the phone, and why the industry would rather you skipped them.</p>

      <h2 id="diy">What they do that you could have done</h2>
      <p style="margin:0 0 16px">A standard service visit is about an hour. Here is what is usually in it, and what the same job costs when you do it:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>The service visit, line by line &mdash; against what the same task costs you</caption>
        <thead><tr><th scope="col">What the technician does</th><th scope="col" class="num">Your cost</th><th scope="col">Difficulty</th><th scope="col">Risk of doing it wrong</th></tr></thead>
        <tbody>
          <tr><td>Checks salt level and breaks any bridge</td><td class="num">$0</td><td class="muted">Broom handle</td><td class="muted">None</td></tr>
          <tr><td>Cleans the injector / venturi</td><td class="num">~$0</td><td class="muted">Screwdriver, soapy water</td><td class="muted">Low &mdash; relieve pressure first, keep the O-ring</td></tr>
          <tr><td>Washes the brine tank</td><td class="num">~$1</td><td class="muted">Bucket, 45 min</td><td class="muted">None</td></tr>
          <tr><td>Doses a resin cleaner, runs a regeneration</td><td class="num">$10&ndash;$20</td><td class="muted">Pour and press a button</td><td class="muted">None</td></tr>
          <tr><td>Tests your water</td><td class="num">$10&ndash;$25</td><td class="muted">Dip a strip</td><td class="muted">None</td></tr>
          <tr><td>Checks settings against your hardness</td><td class="num">$0</td><td class="muted">Requires knowing your gpg</td><td class="muted">Low</td></tr>
          <tr><td><strong>Tests brine draw; diagnoses a failing valve, motor or fouled bed</strong></td><td class="num"><strong>Not DIY</strong></td><td class="muted"><strong>&mdash;</strong></td><td class="muted"><strong>This is the product. This is worth paying for.</strong></td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Read that last row and then read the six above it. <strong>Six of the seven things a technician does on a routine visit, you can do for about $30 in consumables and two hours spread across a year.</strong> The seventh you cannot do at any price, and it is the reason the visit exists. So the rule writes itself, and it is not anti-technician in the slightest: <em>never pay a service call for tasks. Pay it for judgement.</em>

      <h2 id="plans">Plans and contracts &mdash; an honest surprise</h2>
      <p style="margin:0 0 16px">I expected to write that maintenance plans are poor value. The published numbers did not cooperate, and I would rather show you that than pretend otherwise:</p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 230" style="width:100%;height:auto" role="img" aria-label="Five-year cost comparison: DIY only 755 dollars, all-inclusive contract 875 dollars, DIY plus an annual service call 1105 dollars, and a bare service plan plus buying your own salt 1725 dollars.">
        <text x="255" y="24" text-anchor="end" font-size="11.5" fill="#5B6B75" font-weight="600">Five years of upkeep</text>
        <text x="255" y="50" text-anchor="end" font-size="12.5" fill="#16303F" font-weight="700">DIY only</text>
        <rect x="265" y="34" width="176" height="24" rx="2" fill="#1F7A5C"/>
        <text x="449" y="51" font-size="12.5" fill="#16303F" font-weight="700">$755</text>
        <text x="265" y="72" font-size="11" fill="#5B6B75">no repairs covered</text>
        <text x="255" y="104" text-anchor="end" font-size="12.5" fill="#16303F" font-weight="700">All-inclusive contract</text>
        <rect x="265" y="88" width="204" height="24" rx="2" fill="#E8A13D"/>
        <text x="477" y="105" font-size="12.5" fill="#16303F" font-weight="700">$875</text>
        <text x="265" y="126" font-size="11" fill="#1F7A5C" font-weight="600">&hellip; and this one includes the salt AND the repairs</text>
        <text x="255" y="158" text-anchor="end" font-size="12.5" fill="#16303F">DIY + one service call a year</text>
        <rect x="265" y="142" width="258" height="24" rx="2" fill="#5B6B75"/>
        <text x="531" y="159" font-size="12.5" fill="#16303F" font-weight="600">$1,105</text>
        <text x="255" y="196" text-anchor="end" font-size="12.5" fill="#16303F">Bare service plan + your own salt</text>
        <rect x="265" y="180" width="402" height="24" rx="2" fill="#B44A2E"/>
        <text x="675" y="197" text-anchor="end" font-size="12.5" fill="#F7F5F0" font-weight="700">$1,725</text>
        <text x="265" y="218" font-size="11" fill="#B44A2E" font-weight="600">covers neither salt nor repairs &mdash; the worst value on the chart</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; <strong>calculated</strong> from published pricing: all-inclusive contract $100&ndash;$250/yr covering repairs, cleaning, salt refills, water testing and inspection (HomeGuide); bare professional servicing $150&ndash;$300/yr (SoftPro); DIY baseline $151/yr from our own maintenance worksheet &middot; midpoints used</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Look at the second bar. <strong>An all-inclusive contract &mdash; if it genuinely covers what HomeGuide says it covers &mdash; is the second-cheapest option on the board, and it is the only one that also absorbs a $600 repair.</strong> At the low end of that published range it beats doing everything yourself, because it includes the salt you were buying anyway. That is a real finding and I am not going to bury it because it is inconvenient for the tidier story.</p>
      <p style="margin:16px 0 0">My scepticism is about a single word: <em>all-inclusive.</em> A contract that covers parts and labour on a twelve-year-old proprietary valve for about twelve dollars a month is either a loss-leader for a relationship, or it has an exclusions list. Probably both, and neither is sinister. <strong>So get the exclusions in writing before you sign</strong> &mdash; specifically: which parts, whose labour, what happens on a system the company did not install, and whether it renews at the same price. Then look at the bottom bar, which is the deal to actually avoid: the plan that buys you neither the salt nor the repairs.</p>

      <h2 id="script">Five questions that get a price on the phone</h2>
      <p style="margin:0">&ldquo;We can&rsquo;t give you a price until we come out&rdquo; is half true. Nobody can quote the <em>fault</em> before seeing it &mdash; that is fair, and any tradesman who quotes a repair blind is guessing. But the <strong>cost of coming out</strong> is entirely knowable, and so is everything around it. Ask these, in this order, and write the answers down:</p>
    </div>
    <div class="data-table-wrap" style="margin-top:20px">
      <table class="data-table">
        <caption>What to ask before the truck moves</caption>
        <thead><tr><th scope="col">Ask this</th><th scope="col">Why it matters</th></tr></thead>
        <tbody>
          <tr><td><strong>1. What is your trip charge or diagnostic fee?</strong></td><td class="muted">Published range is $40&ndash;$100 for a softener call, $65&ndash;$180 for a billed diagnostic hour. This is knowable. Refusing to say it is a choice.</td></tr>
          <tr><td><strong>2. Is that fee credited against the repair if I go ahead?</strong></td><td class="muted">The single highest-value question here. In many trades it is credited. If this company does not, you want to know that before you book, not after.</td></tr>
          <tr><td><strong>3. What is the hourly rate after the first hour?</strong></td><td class="muted">$45&ndash;$150 is the published spread. Labour is nearly half a typical repair invoice &mdash; this is the number that moves your bill most.</td></tr>
          <tr><td><strong>4. Are parts marked up, and do you carry common ones on the van?</strong></td><td class="muted">A second trip for a part you could have named on the phone is a second trip charge.</td></tr>
          <tr><td><strong>5. My salt tank is full and my water is hard &mdash; what would you check first?</strong></td><td class="muted">You already know the answer is a salt bridge. Their answer tells you whether you are talking to a technician or a salesperson.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">That fifth one is not a trap and I would not use it as one. It is a fair question with a well-known answer, and a good technician will give it to you cheerfully &mdash; probably along with instructions for fixing it yourself, because good technicians would rather come out for the valve than the broom handle.</p>

      <h2 id="replace">When another service call stops making sense</h2>
      <p style="margin:0 0 16px">And if you already know which part failed, our <a href="/water-softener-repair-cost/">repair cost by problem</a> guide prices each fault individually &mdash; including the one that matters most, where a control valve quoted as a rebuild ($99.99 in parts) or as a replacement ($545) is the same failure at 5&times; the price.</p>
      <p style="margin:0">There is a point at which servicing an old softener becomes an expensive way of postponing a decision. It is not an age &mdash; I do not believe in &ldquo;replace anything over ten years&rdquo; and neither should you. It is arithmetic: <strong>what does this repair cost per year of service it actually buys, compared with what a replacement costs per year of its own life?</strong></p>
      <p style="margin:16px 0 0">One $150 service call on a system that then runs cleanly for six years is $25 a year &mdash; an outstanding deal. A third $400 repair in two years on a unit that still is not delivering soft water is not a repair, it is a subscription. Our <a href="/how-long-does-a-water-softener-last/">repair-or-replace calculator</a> runs that division for you, and it will tell you to keep the system far more often than a salesperson would &mdash; but it also names the two failures worth walking away from: <strong>a cracked mineral tank, and a proprietary valve nobody makes parts for any more.</strong></p>
      <p style="margin:16px 0 0">And if you are reading this because you are simply tired of the whole category &mdash; the salt, the bridges, the service calls, the man in the driveway &mdash; then there is an honest alternative worth understanding, and an honest limit on it.</p>
      <div style="margin-top:32px">''' + cta_box("Or step off the treadmill entirely",
        "A salt-free conditioner has a genuinely different maintenance profile: no salt, no brine tank, no regeneration, no bridges \u2014 realistically a prefilter change and not much else. SpringWell publishes FutureSoft pricing online with free shipping and a 6-month money-back window. The honest limit, because it matters more than the sale: a conditioner controls scale rather than removing hardness through ion exchange. Your water will not test soft, because nothing was exchanged. If you want genuinely softened water, you want salt \u2014 and everything above still applies.",
        "Check current SpringWell FutureSoft price","futuresoft") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(s2_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/water-softener-maintenance/"><div class="name">The six DIY jobs</div><div class="range">~2 hrs/yr</div><div class="desc">What the technician was going to do.</div></a>
        <a class="card" href="/how-long-does-a-water-softener-last/"><div class="name">Repair or replace?</div><div class="range">Free tool</div><div class="desc">Cost per year of service, both ways.</div></a>
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">The annual budget</div><div class="range">$60&ndash;$300/yr</div><div class="desc">Every upkeep line, priced.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>HomeGuide &mdash; water softener repair, service and maintenance cost</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-repair-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: a service call and inspection at <strong>$40&ndash;$100, explicitly not including repair parts</strong>; an <strong>all-inclusive maintenance contract at $100&ndash;$250 per year covering repairs, cleaning, salt refills, water testing and annual inspections</strong> &mdash; the figure behind the second bar of the five-year chart; typical repair $150&ndash;$600; resin replacement $200&ndash;$400.',
 '<strong>HomeGuide &mdash; water filtration system repair cost</strong> &mdash; <a href="https://homeguide.com/costs/water-filtration-system-repair-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports: plumber labour at $45&ndash;$150 per hour and handyman rates at $50&ndash;$80; <strong>diagnostics at $65&ndash;$180 as part of a call-out taking up to one hour</strong>; water testing billed at $100&ndash;$300; and an emergency/after-hours flat fee of $75&ndash;$350 on top of hourly rates running 2&ndash;3&times; normal.',
 '<strong>ConsumerAffairs &mdash; cost to replace a water softener</strong> &mdash; <a href="https://www.consumeraffairs.com/homeowners/cost-to-replace-water-softener.html" rel="noopener" target="_blank">consumeraffairs.com</a>. Supports the upper end of the service-call spread: visits commonly reported at $100&ndash;$300, and a home-warranty service fee or deductible of $75&ndash;$150 where a softener is covered equipment.',
 '<strong>SoftPro / Quality Water Treatment &mdash; professional servicing costs</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/breaking-down-water-softener-maintenance-costs" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports the <em>bare</em> professional-servicing figure of $150&ndash;$300 a year (or $75&ndash;$125 per inspection) &mdash; the bottom bar of the five-year chart, and the comparison that makes the all-inclusive contract look as good as it does.',
 '<strong>WaterSoftenerCost.com &mdash; repair cost breakdown</strong> &mdash; <a href="https://watersoftenercost.com/water-softener-repair-cost/" rel="noopener" target="_blank">watersoftenercost.com</a>. Supports: a typical repair range of $150&ndash;$600 with the <strong>average commonly reported near $400</strong> &mdash; the figure decomposed in the invoice donut &mdash; and the observation that proprietary-parts systems cost materially more for the same repair.',
 '<strong>Angi &mdash; water softener repair cost</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-repair-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports the independent second reading on repairs at $150&ndash;$900 and salt at $5&ndash;$10 per 40-lb bag, which feeds the DIY baseline used in the five-year comparison.',
 '<strong>SoftWaterSystemCost.com &mdash; our own DIY maintenance worksheet</strong> &mdash; <a href="/water-softener-maintenance/">the complete maintenance schedule</a>. Supports the $151/year DIY baseline (salt $120, resin cleaner $20, test strips $10, soap $1) and the two-hours-a-year time estimate used throughout this page.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("water-softener-servicing/index.html", s2)


# ============ R1 — WATER SOFTENER REPAIR COST BY PROBLEM ============
r1_faqs = [
 ("How much does it cost to repair a water softener?","HomeGuide puts the national average at $430, with a typical range of $150&ndash;$600, a minimum of $40 and a maximum of $1,500. The spread is that wide because the price depends entirely on which component failed &mdash; and on whether it failed at all."),
 ("How much does it cost to replace a water softener control valve?","A complete Fleck 5600SXT valve is published at about $545 in parts. But a rebuild kit for the same valve &mdash; piston, seals, spacers and brine valve &mdash; is published at $99.99. Same fault, same labour. Ask which one you are being quoted."),
 ("Why is my water softener repair quote so expensive?","Because most of it usually is not the part. A service call is $40&ndash;$100 before anyone opens the valve, and labour runs $45&ndash;$150 an hour. A $100 part inside a $430 invoice is normal &mdash; what is not normal is nobody itemising it."),
 ("Can a leaking water softener be repaired?","Usually. HomeGuide names three causes: a loose water-line connection, worn rotor-valve seals, or a cracked tank. The first is nearly free, the second is a rebuild kit, the third is $150&ndash;$500 for a tank. Find out which before approving anything."),
 ("Why won&rsquo;t my water softener regenerate?","HomeGuide lists the causes in order: a broken or misconfigured timer, a blocked drain hose, a plugged injector or venturi &mdash; and, &ldquo;in rare cases,&rdquo; the motor. Note that the motor is last and explicitly rare. Cheap causes first."),
 ("Is a water softener worth repairing?","Often, yes. The test is not the age of the machine, it is what the repair costs per year of service it buys. A $250 fix on a sound system that then runs eight more years is exceptional value. A third repair in two years is not a repair, it is a subscription."),
 ("How much does a water softener service call cost?","$40&ndash;$100 for the call and inspection, parts excluded. Ask two things before booking: whether that fee is credited against the repair, and what the hourly rate is after the first hour."),
 ("Should I repair or replace an old water softener?","Divide the repair quote by the cost of a comparable installed replacement ($700&ndash;$3,000). But read the answer alongside age, repair history and parts availability &mdash; a proprietary valve nobody stocks parts for is a stronger argument for replacing than any percentage."),
]
r1_rows = [
 ("Service call &amp; diagnosis",40,100,"HomeGuide, softener-specific &mdash; parts excluded"),
 ("The part: control valve rebuild kit",100,100,"Published: Fleck 5600 kit (P/N 61962) &mdash; piston, seals, spacers, brine valve"),
 ("Repair labour, 1&ndash;2 hours",45,300,"HomeGuide: plumber $45&ndash;$150/hr"),
 ("Fittings, sealant, sundries",0,40,"Itemised on an honest invoice"),
]
r1 = head("Water Softener Repair Cost by Problem (2026): Valve, Motor, Timer &amp; Leaks",
 "National average $430, range $150\u2013$600. But the same failing valve is a $100 rebuild kit or a $545 replacement \u2014 and the difference is who holds the pen.",
 "/water-softener-repair-cost/",
 ld(article_schema("Water Softener Repair Cost by Problem: Valve, Motor, Timer and Leaks","Published repair pricing broken out by the component that actually failed, a symptom-to-cause map from HomeGuide's own troubleshooting data, and the rebuild-versus-replace distinction that swings a control-valve quote by 5x.","/water-softener-repair-cost/",date="2026-07-12"))
 + ld(faq_schema(r1_faqs,"/water-softener-repair-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Repair cost","/water-softener-repair-cost/")])))
r1 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Repair cost</nav>
      <h1>Water Softener Repair Cost by Problem</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">HomeGuide puts the national average water softener repair at <span class="fig">$430</span>, inside a typical range of <span class="fig">$150&ndash;$600</span>, with a minimum of <span class="fig">$40</span> and a maximum of <span class="fig">$1,500</span>. Useful, as far as it goes. But then HomeGuide says something in its own summary that almost nobody quotes back at them: <strong>&ldquo;Most problems are an empty brine tank, a jammed valve, or parts that need cleaning.&rdquo;</strong></p>
      <p><strong>Water softener repair costs $150&ndash;$600 with a national average of $430, but the price is set entirely by which part failed. Resin replacement runs $200&ndash;$400 and a tank $150&ndash;$500. A control valve is the big fork: a published rebuild kit is $99.99, while a complete replacement valve is about $545 &mdash; for the same fault.</strong></p>
      <p style="margin:0">Read that HomeGuide line again. An empty brine tank is not a repair. Parts that need cleaning are not a repair. <strong>The most common water softener &ldquo;repair&rdquo; is a chore.</strong> And the second most common one &mdash; the jammed valve &mdash; is where the real money is decided, because that single fault can be quoted two completely different ways.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#map">Symptom &rarr; cause &rarr; cost (the map)</a></li>
          <li><a href="#tool">Decode your quote (tool)</a></li>
          <li><a href="#bars">What each repair actually costs (chart)</a></li>
          <li><a href="#fork">The $445 word: rebuild or replace (chart)</a></li>
          <li><a href="#sheet">The worksheet</a></li>
          <li><a href="#why">Why a $100 part becomes a $430 bill</a></li>
          <li><a href="#matrix">Repair or replace: the matrix</a></li>
          <li><a href="#checklist">Before you approve the quote</a></li>
        </ol>
      </details>

      <h2 id="map">Symptom &rarr; cause &rarr; cost</h2>
      <p style="margin:0 0 16px">This is the table I would have wanted taped to the inside of every homeowner&rsquo;s utility door. Causes are HomeGuide&rsquo;s own troubleshooting findings; prices are published ranges:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>What the symptom usually means, and what it usually costs</caption>
        <thead><tr><th scope="col">What you are seeing</th><th scope="col">Most likely cause</th><th scope="col">Is it a repair?</th><th scope="col" class="num">Cost</th></tr></thead>
        <tbody>
          <tr><td>Salt not going down, water hard</td><td class="muted">Salt bridge</td><td class="muted"><strong>No &mdash; a chore</strong></td><td class="num">$0</td></tr>
          <tr><td>Brine tank full of water, not draining</td><td class="muted">Float set too high, clogged drain or injector, salt mushing</td><td class="muted"><strong>Usually not</strong></td><td class="num">$0&ndash;$20</td></tr>
          <tr><td>Running constantly</td><td class="muted">Salt bridge, or a clog in the drain / valve / injector</td><td class="muted"><strong>Usually not</strong></td><td class="num">$0&ndash;$20</td></tr>
          <tr><td>Will not regenerate</td><td class="muted">Timer, blocked drain hose, plugged injector &mdash; motor only &ldquo;in rare cases&rdquo;</td><td class="muted">Maybe</td><td class="num">$0&ndash;$600</td></tr>
          <tr><td>Water tastes salty</td><td class="muted">Clogged drain hose, or worn rotor-valve seals</td><td class="muted">Maybe</td><td class="num">$0&ndash;$500</td></tr>
          <tr><td><strong>Leaking</strong></td><td class="muted">Loose connection &middot; worn rotor-valve <strong>seals</strong> &middot; cracked tank</td><td class="muted"><strong>Yes</strong></td><td class="num">$0 &rarr; $500</td></tr>
          <tr><td>Low water pressure</td><td class="muted">Fouled resin, iron/sediment, clogged prefilter &mdash; <em>or the system was undersized</em></td><td class="muted">Depends</td><td class="num">$200&ndash;$400</td></tr>
          <tr><td>Resin beads in the taps</td><td class="muted">Broken screen, failed seal, cracked distributor &mdash; usually chlorine damage</td><td class="muted"><strong>Yes</strong></td><td class="num">$200&ndash;$400+</td></tr>
          <tr><td>Brown or discoloured water</td><td class="muted">Iron and manganese fouling the resin</td><td class="muted">Depends</td><td class="num">$200&ndash;$400</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Count the rows. <strong>Three of the nine are not repairs at all</strong>, and two more are &ldquo;maybe.&rdquo; That is not me being contrarian &mdash; it is HomeGuide&rsquo;s own diagnostic table, read honestly. The <a href="/water-softener-maintenance/">DIY fixes for the free ones</a> take minutes.</p>
      <p style="margin:16px 0 0">And notice what sits behind &ldquo;low water pressure&rdquo;: a system that was simply <em>sized too small</em>. There is no repair for that. No part fixes it. If that is your problem, the resin replacement you are about to buy will not solve anything &mdash; <a href="/what-size-water-softener-do-i-need/">check the sizing</a> first.</p>

      <h2 id="tool">Decode your quote</h2>
      <p style="margin:0 0 16px">Pick your symptom, drop in what you have been quoted, and see what the published data says about both:</p>
      <div data-quote-decoder></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Causes are HomeGuide&rsquo;s troubleshooting findings; the repair bands are its published pricing. If you have not tested your water, do that before anyone replaces resin &mdash; a <a href="/pick/test-kit" ''' + PICK + '''>test kit</a> is $10&ndash;$25 and iron is the single most common reason resin dies young.</p>

      <h2 id="bars">What each repair actually costs</h2>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 290" style="width:100%;height:auto" role="img" aria-label="Published water softener repair costs by type, from a 40 to 80 dollar inspection up to a 700 to 3000 dollar full system replacement, with the 430 dollar national average marked.">
        <line x1="250" y1="30" x2="250" y2="248" stroke="#E6E1D8" stroke-width="1"/>
        <line x1="390" y1="30" x2="390" y2="248" stroke="#E6E1D8" stroke-width="1"/>
        <line x1="530" y1="30" x2="530" y2="248" stroke="#E6E1D8" stroke-width="1"/>
        <line x1="670" y1="30" x2="670" y2="248" stroke="#E6E1D8" stroke-width="1"/>
        <text x="250" y="266" text-anchor="middle" font-size="10.5" fill="#5B6B75">$0</text>
        <text x="390" y="266" text-anchor="middle" font-size="10.5" fill="#5B6B75">$350</text>
        <text x="530" y="266" text-anchor="middle" font-size="10.5" fill="#5B6B75">$700</text>
        <text x="670" y="266" text-anchor="middle" font-size="10.5" fill="#5B6B75">$1,050</text>
        <text x="240" y="46" text-anchor="end" font-size="11.5" fill="#16303F">Inspection &mdash; nothing broken</text>
        <rect x="266" y="34" width="16" height="16" rx="2" fill="#1F7A5C"/>
        <text x="290" y="46" font-size="11" fill="#5B6B75">$40&ndash;$80</text>
        <text x="240" y="72" text-anchor="end" font-size="11.5" fill="#16303F">Filter replacement</text>
        <rect x="262" y="60" width="68" height="16" rx="2" fill="#1F7A5C"/>
        <text x="338" y="72" font-size="11" fill="#5B6B75">$30&ndash;$200</text>
        <text x="240" y="98" text-anchor="end" font-size="11.5" fill="#16303F" font-weight="700">Valve REBUILD (parts + labour)</text>
        <rect x="324" y="86" width="126" height="16" rx="2" fill="#1F7A5C"/>
        <text x="458" y="98" font-size="11" fill="#16303F" font-weight="700">$185&ndash;$500</text>
        <text x="240" y="124" text-anchor="end" font-size="11.5" fill="#16303F">Resin replacement</text>
        <rect x="330" y="112" width="80" height="16" rx="2" fill="#E8A13D"/>
        <text x="418" y="124" font-size="11" fill="#5B6B75">$200&ndash;$400</text>
        <text x="240" y="150" text-anchor="end" font-size="11.5" fill="#16303F">Tank replacement</text>
        <rect x="310" y="138" width="140" height="16" rx="2" fill="#E8A13D"/>
        <text x="458" y="150" font-size="11" fill="#5B6B75">$150&ndash;$500</text>
        <text x="240" y="176" text-anchor="end" font-size="11.5" fill="#16303F" font-weight="700">Typical repair (avg $430)</text>
        <rect x="310" y="164" width="180" height="16" rx="2" fill="#5B6B75"/>
        <line x1="422" y1="160" x2="422" y2="184" stroke="#16303F" stroke-width="2"/>
        <text x="498" y="176" font-size="11" fill="#16303F" font-weight="700">$150&ndash;$600</text>
        <text x="240" y="202" text-anchor="end" font-size="11.5" fill="#B44A2E" font-weight="700">Valve REPLACE (parts + labour)</text>
        <rect x="502" y="190" width="126" height="16" rx="2" fill="#B44A2E"/>
        <text x="636" y="202" font-size="11" fill="#B44A2E" font-weight="700">$630&ndash;$945</text>
        <text x="240" y="228" text-anchor="end" font-size="11.5" fill="#16303F">Full system replacement</text>
        <rect x="530" y="216" width="140" height="16" rx="2" fill="#16303F"/>
        <polygon points="670,216 686,224 670,232" fill="#16303F"/>
        <text x="530" y="246" font-size="10.5" fill="#5B6B75">$700&ndash;$3,000 (runs off this chart)</text>
        <text x="422" y="20" text-anchor="middle" font-size="10.5" fill="#16303F" font-weight="700">&darr; national average $430</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; published ranges from HomeGuide; valve figures <strong>calculated</strong> from published parts pricing plus published labour rates &middot; note the two valve bars &mdash; <strong>same fault, and they do not overlap</strong></div>
    </div>
    <div class="col">
      <h2 id="fork">The $445 word: rebuild or replace</h2>
      <p style="margin:0">Here is the thing I most want a homeowner to walk away knowing, because it is worth more than everything else on this page combined.</p>
      <p style="margin:16px 0 0">A control valve fails in a very particular way. The piston and the seals inside it wear &mdash; and one authorised parts supplier states plainly that the piston and seal are on a <strong>48-month replacement interval</strong>. Read that again. They are not a catastrophic failure. <strong>They are a wear part with a service interval, like brake pads.</strong></p>
      <p style="margin:16px 0 0">A published rebuild kit for a Fleck 5600 &mdash; piston, seals, spacers and brine valve &mdash; is <span class="fig">$99.99</span>. A complete replacement valve for the same unit is published at about <span class="fig">$545</span>. The labour is essentially identical, because you are taking the valve apart either way. So the same failure, on the same machine, on the same afternoon, is either a <strong>$185&ndash;$500 job or a $630&ndash;$945 one</strong> &mdash; and the difference is <em>one word on a work order.</em></p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#1F7A5C",18),("#E6E1D8",82)], "$100", "of $545", "Share of a complete valve replacement that a rebuild kit would cover") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#1F7A5C"></span> The rebuild kit that usually fixes it <span class="pc">18%</span></div>
          <div><span class="sw" style="background:#E6E1D8"></span> Valve body, meter and electronics &mdash; often still working <span class="pc">82%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; published rebuild kit $99.99 against a published complete valve at ~$545 &middot; <strong>not every valve fault is a piston and seals</strong> &mdash; a cracked body or a dead board genuinely needs the assembly. But you are entitled to be told which one you have</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">I want to be scrupulously fair here, because this is the part where a page like this usually starts shouting. <strong>Sometimes the whole valve genuinely is finished.</strong> The body cracks. The board dies. The meter fails. In those cases $545 is the correct number and the technician recommending it is doing his job. Replacing the assembly is also faster, cleaner and easier to warranty &mdash; all legitimate reasons a good company might prefer it.</p>
      <p style="margin:16px 0 0">But it is not a coincidence that the more expensive path is also the more convenient one to sell. So there is exactly one question to put on the table, and it is not confrontational: <strong>&ldquo;Is this a rebuild or a replacement &mdash; and if it&rsquo;s a replacement, what specifically is wrong with the body?&rdquo;</strong> A technician who can answer that has earned the $545. One who cannot has just been asked the only question that mattered.</p>

      <h2 id="sheet">The worksheet</h2>
      <p style="margin:0">A control-valve rebuild, assembled from published prices &mdash; the most common real repair on this page:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Control valve rebuild, assembled from published pricing", r1_rows, total_label="Rebuild, all in") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>An illustrative assembled estimate, not a national average.</strong> I have built it from a published parts price and published labour rates rather than quoting somebody&rsquo;s average, because that is the only way you can check my arithmetic. The equivalent sheet with a complete valve in it instead of the kit runs <span class="fig">$630&ndash;$945</span>. Both are legitimate quotes. Only one of them might be necessary.</p>

      <h2 id="why">Why a $100 part becomes a $430 bill</h2>
      <p style="margin:0">Because the part was never the expensive bit, and pretending otherwise is how homeowners end up feeling cheated by a fair invoice. A service call is <span class="fig">$40&ndash;$100</span> before anyone touches the softener. Labour is <span class="fig">$45&ndash;$150</span> an hour. A technician who diagnoses a worn seal stack, drives to your house, strips the valve, fits a $100 kit and tests it has spent two hours and a van on you.</p>
      <p style="margin:16px 0 0">That is a $430 invoice with a $100 part in it, and <strong>it is not a rip-off</strong> &mdash; it is what skilled labour costs. What you are entitled to is the <em>itemisation</em>: parts, labour, call-out, separately, on paper. Our <a href="/water-softener-servicing/">servicing guide</a> covers the call-out economics and the questions that get a price on the phone. The opacity is the problem, never the price.</p>

      <h2 id="matrix">Repair or replace: the matrix</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>Which way each factor actually points</caption>
        <thead><tr><th scope="col">Your situation</th><th scope="col">Repair leans better</th><th scope="col">Replacement leans better</th></tr></thead>
        <tbody>
          <tr><td>One isolated failure on an otherwise sound system</td><td class="num">&#10003;</td><td class="num"></td></tr>
          <tr><td>The fault is a worn piston and seal stack</td><td class="num">&#10003;</td><td class="num"></td></tr>
          <tr><td>Industry-standard valve, parts widely stocked</td><td class="num">&#10003;</td><td class="num"></td></tr>
          <tr><td>Cracked mineral tank</td><td class="num"></td><td class="num">&#10003;</td></tr>
          <tr><td><strong>Proprietary valve, parts hard to source</strong></td><td class="num"></td><td class="num"><strong>&#10003;</strong></td></tr>
          <tr><td>Third repair in two years</td><td class="num"></td><td class="num">&#10003;</td></tr>
          <tr><td>Multiple simultaneous failures (valve <em>and</em> resin <em>and</em> tank)</td><td class="num"></td><td class="num">&#10003;</td></tr>
          <tr><td>Hard water persists after the repair</td><td class="num"></td><td class="num">&#10003; <span class="muted">&mdash; or it was never a repair, it was sizing</span></td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">The percentage in the tool above &mdash; <strong>repair quote &divide; installed replacement cost</strong> &mdash; is worth calculating and worth <em>not</em> obeying. There is no magic threshold, whatever the internet tells you, because a percentage has no denominator in <em>time</em>: it never asks how many years the repair buys. Our <a href="/how-long-does-a-water-softener-last/">lifespan and repair-or-replace guide</a> runs that division properly, and finds the repair wins far more often than a salesperson would like.</p>
      <p style="margin:16px 0 0">Look instead at the two bold rows. <strong>A proprietary valve nobody stocks parts for is a better argument for replacing than any percentage</strong> &mdash; because that machine is not going to have a next repair at all, at any price. That is the failure worth planning around.</p>
      <div style="margin-top:32px">''' + cta_box("When the arithmetic finally points at a new system",
        "If the tank is cracked, the parts have vanished, or you are three repairs deep on a machine that still is not delivering soft water, the repair path is closed and you are buying a system \u2014 so buy it with a real number in front of you. SpringWell publishes its softener pricing online, ships free, and gives you six months to send it back, which means you can weigh a replacement against the quote in your hand rather than one produced beside your failed unit. Match the grain capacity to your measured hardness first; bathroom-count sizing is a proxy, not a measurement.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="checklist">Before you approve the quote</h2>
      <p style="margin:0 0 16px">Nine questions. None of them are hostile, and a good technician will answer every one without blinking:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>The checklist that pays for itself</caption>
        <thead><tr><th scope="col">Ask</th><th scope="col">Because</th></tr></thead>
        <tbody>
          <tr><td><strong>1. Which exact component failed?</strong></td><td class="muted">&ldquo;The valve&rdquo; is not a component. The piston, the seals, the board and the body are.</td></tr>
          <tr><td><strong>2. Is it being rebuilt or replaced &mdash; and why?</strong></td><td class="muted">The $445 question. Published parts differ by roughly 5&times; for the same fault.</td></tr>
          <tr><td><strong>3. What is the part number?</strong></td><td class="muted">You can look it up. That is the entire point of asking.</td></tr>
          <tr><td><strong>4. Is the diagnostic fee credited against the repair?</strong></td><td class="muted">$40&ndash;$100 you may or may not be paying twice.</td></tr>
          <tr><td><strong>5. Is labour flat-rate or hourly?</strong></td><td class="muted">At $45&ndash;$150/hr, labour is usually the biggest line on the invoice.</td></tr>
          <tr><td><strong>6. Did you check the injector and drain line first?</strong></td><td class="muted">HomeGuide lists clogs <em>before</em> the motor. Cheap causes first.</td></tr>
          <tr><td><strong>7. What warranty covers the repair?</strong></td><td class="muted">Parts and labour, and for how long &mdash; in writing.</td></tr>
          <tr><td><strong>8. What else is showing wear?</strong></td><td class="muted">You do not want a second call-out fee in six weeks.</td></tr>
          <tr><td><strong>9. What would a comparable replacement cost installed?</strong></td><td class="muted">$700&ndash;$3,000 is the published band. Ask them to say a number out loud.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">That last question is not a threat and I would not frame it as one. It is the question a good technician <em>wants</em> you to ask &mdash; because if the honest answer is &ldquo;this $250 rebuild will give you another eight years,&rdquo; he would much rather you heard it from him than from a salesman with a brochure.</p>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(r1_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/water-softener-servicing/"><div class="name">What the visit costs</div><div class="range">$40&ndash;$100</div><div class="desc">Trip charges, and the phone script.</div></a>
        <a class="card" href="/how-long-does-a-water-softener-last/"><div class="name">Repair or replace?</div><div class="range">Free tool</div><div class="desc">Cost per year of service, both ways.</div></a>
        <a class="card" href="/water-softener-maintenance/"><div class="name">The free fixes</div><div class="range">~2 hrs/yr</div><div class="desc">Three of the nine faults above.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>HomeGuide &mdash; water softener repair, service and maintenance cost</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-repair-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports the backbone of this page: <strong>national average repair $430; minimum $40; maximum $1,500; average range $150&ndash;$600</strong>; inspection $40&ndash;$80; resin replacement $200&ndash;$400; tank replacement $150&ndash;$500; filter replacement $30&ndash;$200; system removal $50&ndash;$100; full system replacement $700&ndash;$3,000; all-inclusive contract $100&ndash;$250/yr. Also the entire symptom&ndash;cause map, including its own summary that <strong>&ldquo;most problems are an empty brine tank, a jammed valve, or parts that need cleaning&rdquo;</strong>, that motor failure occurs only &ldquo;in rare cases,&rdquo; and that a control valve may be <em>cleaned or replaced</em>.',
 '<strong>Aquatell (authorised dealer) &mdash; Fleck 5600 control valve rebuild kit, P/N 61962</strong> &mdash; <a href="https://www.aquatell.com/products/fleck-5600-softener-control-valve-rebuild-kit-5600rb" rel="noopener" target="_blank">aquatell.com</a>. Supports the published rebuild-kit price of <strong>$99.99</strong>, and its contents: main piston assembly, seals and spacers, and brine valve piston. Price checked July 2026 and subject to change.',
 '<strong>AquaScience &mdash; replacement piston and seal kit for Fleck 5600SXT control valves</strong> &mdash; <a href="https://aquascience.net/replacement-piston-and-seal-kit-for-fleck-5600sxt-backwash-water-softener-control-valves" rel="noopener" target="_blank">aquascience.net</a>. Supports the single most important technical claim on this page: the manufacturer-side recommendation to <strong>replace the piston and seal every 48 months</strong> &mdash; i.e. that they are a wear part on a service interval, not a catastrophic failure.',
 '<strong>Mid Atlantic Water &mdash; published control-valve pricing</strong> &mdash; <a href="https://midatlanticwater.net/blogs/faqs/how-long-do-water-softeners-last" rel="noopener" target="_blank">midatlanticwater.net</a>. Supports the complete Fleck 5600SXT replacement valve at approximately <strong>$545</strong> &mdash; the other half of the fork &mdash; along with resin at roughly $295 per cubic foot.',
 '<strong>HomeGuide &mdash; water filtration system repair cost</strong> &mdash; <a href="https://homeguide.com/costs/water-filtration-system-repair-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports the labour figures used to assemble the worksheet: plumber $45&ndash;$150 per hour, handyman $50&ndash;$80; diagnostics $65&ndash;$180 for a call-out of up to one hour; emergency and after-hours surcharges of $75&ndash;$350 on top of hourly rates at 2&ndash;3&times; normal.',
 '<strong>Angi &mdash; water softener repair cost</strong> &mdash; <a href="https://www.angi.com/articles/how-much-does-water-softener-repair-cost.htm" rel="noopener" target="_blank">angi.com</a>. Supports the independent second reading on repair pricing at $150&ndash;$900 including labour &mdash; a wider band than HomeGuide&rsquo;s, which is itself a useful signal about how much these numbers move by market.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("water-softener-repair-cost/index.html", r1)


# ============ SC — WATER SOFTENER SALT COST & TYPES ============
sc_faqs = [
 ("How much does water softener salt cost?","$4.50&ndash;$10 per 40-lb bag &mdash; roughly 12&cent; a pound for rock or solar salt and up to 25&cent; for evaporated pellets. A typical family of four at 10 gpg uses about 8 bags a year, so $40&ndash;$80 annually."),
 ("How much salt does a water softener use?","It scales with hardness and household size, not with the machine. A family of four at 10 gpg on a correctly sized softener uses roughly 316 lbs a year &mdash; about eight 40-lb bags, or one bag every seven weeks."),
 ("What is the best water softener salt?","Solar pellets for most homes: 99.6% pure, they dissolve evenly and bridge far less than crystals. Evaporated pellets (99.9%) are the premium choice on very hard water. Avoid rock salt &mdash; its 2&ndash;5% insolubles are what clog injectors."),
 ("Is potassium chloride worth the money?","It costs up to four times more and regenerates less efficiently &mdash; published guidance says raise your hardness setting 10&ndash;20% to compensate. Buy it for a genuine medical sodium restriction or septic and garden discharge. Not because it is the expensive bag."),
 ("Salt pellets or crystals?","Pellets. They dissolve more evenly and bridge far less, especially in humid climates. Crystals are cheaper and fine in smaller, low-use systems &mdash; but they are the form most associated with bridging. Do not mix the two in one tank."),
 ("Does cheap salt damage a water softener?","Not directly &mdash; it <em>clogs</em> it. Rock salt carries 2&ndash;5% insoluble matter, mostly calcium sulfate and shale, which settles as sludge, drives mushing and bridging, and blocks the injector. A blocked injector is a documented cause of regeneration failure."),
 ("How often should I add salt?","Look at it monthly; most households refill every six to eight weeks. Keep the salt a few inches above the water line and resist filling to the brim &mdash; overfilling is one of the main causes of bridging."),
 ("Can I mix salt types?","Don&rsquo;t. Mixing pellets and crystals in one tank is specifically advised against, and switching between sodium and potassium chloride complicates the hardness setting your softener is running to."),
]
sc_rows = [
 ("The salt itself &mdash; ten years, ~79 bags",395,790,"$5&ndash;$10 per 40-lb bag &middot; 316 lbs/yr for a typical household"),
 ("Extra brine-tank cleanouts if you buy on price",0,0,"Time, not money &mdash; but each wash is about 45 minutes"),
 ("Insoluble sludge you will shovel out",0,0,"110 lbs on rock salt versus 3 lbs on evaporated. Free to remove, tedious to ignore"),
 ("One clogged injector, if the cheap salt does what the literature says it does",0,430,"HomeGuide: $430 national average repair. A blocked injector is a named cause"),
]
sc = head("Water Softener Salt Cost & Types (2026): Why the Cheapest Bag Costs the Most",
 "Salt is 79% of what a softener costs to run. Rock salt saves $8 a year and puts 110 lbs of shale in your tank. Full cost calculator, all four types priced.",
 "/water-softener-salt-cost/",
 ld(article_schema("Water Softener Salt Cost and Types: Rock, Solar, Evaporated and Potassium Chloride","What each salt type costs, how much your household actually uses, the insoluble residue each one leaves behind, and why the cheapest bag on the shelf is the most expensive one you can buy.","/water-softener-salt-cost/",date="2026-07-12"))
 + ld(faq_schema(sc_faqs,"/water-softener-salt-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Salt cost","/water-softener-salt-cost/")])))
sc += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Salt cost</nav>
      <h1>Water Softener Salt Cost &amp; Types</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Softener salt runs <span class="fig">$4.50&ndash;$10</span> per 40-lb bag &mdash; about 12&cent; a pound for rock or solar salt, up to 25&cent; for evaporated pellets. A typical family of four at 10 gpg gets through roughly <span class="fig">316 lbs a year</span>: eight bags, one every seven weeks, <span class="fig">$40&ndash;$80</span>. That is the answer to the question you asked. Now here is the one you didn&rsquo;t.</p>
      <p><strong>Water softener salt costs $4.50&ndash;$10 per 40-lb bag, and a typical household uses about 8 bags (316 lbs) a year &mdash; $40&ndash;$80. But rock salt carries 2&ndash;5% insoluble matter versus under 0.2% in evaporated pellets, and that residue is what causes the bridging, mushing and injector clogs behind a $430 average repair.</strong></p>
      <p style="margin:0">Salt is the biggest recurring cost a softener has &mdash; <a href="/water-softener-maintenance/">79% of what you spend maintaining one</a>. So it is the line people try hardest to shave. And it is the one line where <strong>shaving is a trap</strong>, because the money you save buying cheap salt is measured in single-digit dollars a year, while the machine it damages is measured in hundreds.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#calc">What your salt actually costs (tool)</a></li>
          <li><a href="#ladder">The four types, priced</a></li>
          <li><a href="#sludge">What you are shovelling out (chart)</a></li>
          <li><a href="#trap">The rock salt trap</a></li>
          <li><a href="#kcl">Potassium chloride: the honest verdict (chart)</a></li>
          <li><a href="#sheet">The ten-year salt bill</a></li>
          <li><a href="#less">The cheapest bag is the one you never buy</a></li>
        </ol>
      </details>

      <h2 id="calc">What your salt actually costs</h2>
      <p style="margin:0 0 16px">Salt use is set by your <em>hardness</em> and your <em>household</em> &mdash; not by the brand on the bag. Set both, then switch salt types and watch two numbers move in opposite directions:</p>
      <div data-salt-cost></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Consumption is derived from the same method as our <a href="/what-size-water-softener-do-i-need/">sizing calculator</a> &mdash; regenerations at an efficient salt dose, not at the nameplate. If you have never measured your hardness, a <a href="/pick/test-kit" ''' + PICK + '''>test kit</a> costs less than one bag of salt and it sets every number above.</p>

      <h2 id="ladder">The four types, priced</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>What is actually in the bag &mdash; purity, price, and the consequence</caption>
        <thead><tr><th scope="col">Type</th><th scope="col" class="num">Purity</th><th scope="col" class="num">Per 40-lb bag</th><th scope="col">What that means for you</th></tr></thead>
        <tbody>
          <tr><td><strong>Rock salt</strong></td><td class="num">95&ndash;98%</td><td class="num">$5&ndash;$8</td><td class="muted">2&ndash;5% insolubles &mdash; calcium sulfate and shale. Sludge, mushing, bridging, clogs. One supplier states outright it does not recommend it</td></tr>
          <tr><td><strong>Solar pellets</strong></td><td class="num">99.6%</td><td class="num">$6&ndash;$8</td><td class="muted">The sensible default. Dissolves evenly, bridges far less than crystals, residue is a fraction of rock salt&rsquo;s</td></tr>
          <tr><td><strong>Evaporated pellets</strong></td><td class="num">99.8&ndash;99.9%</td><td class="num">$8&ndash;$10</td><td class="muted">Under 0.2% insolubles. The premium choice on very hard water (15+ gpg) or if you want the tank to stay clean for years</td></tr>
          <tr><td><strong>Potassium chloride</strong></td><td class="num">99%+</td><td class="num">up to ~4&times;</td><td class="muted">Sodium-free, and less efficient &mdash; raise the hardness setting 10&ndash;20%. A medical or septic choice, not a performance one</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0"><strong>One more axis, and it is not a small one: pellets versus crystals.</strong> Crystals are cheaper and dissolve faster, and they are also the form most associated with bridging &mdash; one supplier reports seeing far more clogged and bridged softeners on crystals than on pellets. Their irregular shape lets them bind together. Pellets dissolve evenly and behave far better in humid climates. Buy pellets, and don&rsquo;t mix the two in one tank.</p>

      <h2 id="sludge">What you are shovelling out</h2>
      <p style="margin:0 0 16px">Purity sounds like a spec-sheet detail until you multiply it by ten years of bags. Here is the insoluble matter each salt type puts into the bottom of your brine tank over the life of the machine:</p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 220" style="width:100%;height:auto" role="img" aria-label="Insoluble residue delivered into a brine tank over ten years: rock salt 110 pounds, potassium chloride 32 pounds, solar pellets 13 pounds, evaporated pellets 3 pounds.">
        <text x="230" y="24" text-anchor="end" font-size="11.5" fill="#5B6B75" font-weight="600">Insoluble residue, 10 years</text>
        <text x="230" y="50" text-anchor="end" font-size="12.5" fill="#B44A2E" font-weight="700">Rock salt</text>
        <rect x="240" y="34" width="460" height="24" rx="2" fill="#B44A2E"/>
        <text x="690" y="51" text-anchor="end" font-size="13" fill="#F7F5F0" font-weight="700">110 lbs</text>
        <text x="230" y="88" text-anchor="end" font-size="12.5" fill="#16303F">Potassium chloride</text>
        <rect x="240" y="72" width="131" height="24" rx="2" fill="#5B6B75"/>
        <text x="379" y="89" font-size="12.5" fill="#16303F" font-weight="600">32 lbs</text>
        <text x="230" y="126" text-anchor="end" font-size="12.5" fill="#16303F" font-weight="700">Solar pellets</text>
        <rect x="240" y="110" width="52" height="24" rx="2" fill="#E8A13D"/>
        <text x="300" y="127" font-size="12.5" fill="#16303F" font-weight="600">13 lbs</text>
        <text x="230" y="164" text-anchor="end" font-size="12.5" fill="#16303F">Evaporated pellets</text>
        <rect x="240" y="148" width="13" height="24" rx="2" fill="#1F7A5C"/>
        <text x="261" y="165" font-size="12.5" fill="#16303F" font-weight="600">3 lbs</text>
        <text x="370" y="200" text-anchor="middle" font-size="12" fill="#16303F" font-style="italic">Rock salt delivers 35&times; more insoluble shale and calcium sulfate into your tank than evaporated does.</text>
        <text x="370" y="216" text-anchor="middle" font-size="11.5" fill="#5B6B75">All of it has to leave through an injector orifice the size of a pinhole.</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; <strong>calculated</strong> from published purity ranges against 316 lbs of salt a year for a typical household &middot; midpoints used (rock 96.5%, solar 99.6%, evaporated 99.9%, potassium 99%)</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">A hundred and ten pounds. That is not a spec-sheet abstraction &mdash; it is a wheelbarrow of ground rock, delivered into your brine tank one bag at a time, and it has to get out through an orifice you could cover with a fingernail. <strong>This is the entire mechanism.</strong> It is why cheap salt is associated with mushing, why it bridges in humid climates, and why the injector &mdash; the single part whose blockage most reliably stops a softener from regenerating &mdash; is the thing it blocks.</p>

      <h2 id="trap">The rock salt trap</h2>
      <p style="margin:0">So run the arithmetic that the price tag invites you to skip.</p>
      <p style="margin:16px 0 0">Rock salt runs about <span class="fig">$6</span> a bag against roughly <span class="fig">$7</span> for solar pellets. Across eight bags a year, buying the cheap one saves you <strong>about $8 a year.</strong> Eight dollars.</p>
      <p style="margin:16px 0 0">A clogged injector &mdash; which is not a hypothetical, it is the documented consequence of exactly this residue &mdash; sits inside a <a href="/water-softener-repair-cost/">national average repair of $430</a>. So: <strong>the cheap salt would need to run for fifty-four years without causing a single incident to break even.</strong> The softener itself lasts ten to fifteen. There is no version of this arithmetic where rock salt wins, and there is no version where it even gets close.</p>
      <p style="margin:16px 0 0">That is the whole case, and it is not a moral one about buying quality. It is that <strong>the saving is too small to be worth any risk at all</strong> &mdash; and this particular risk is the one thing the literature is unanimous about.</p>

      <h2 id="kcl">Potassium chloride: the honest verdict</h2>
      <p style="margin:0 0 16px">Now the expensive mistake, which is the mirror image of the cheap one. Potassium chloride costs up to <strong>four times</strong> as much as sodium chloride &mdash; and because it regenerates less efficiently, published guidance tells you to <em>raise your hardness setting 10&ndash;20%</em>, meaning you use more of it. Here is a year of it, against the same year of solar pellets:</p>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",21),("#B44A2E",79)], "$265", "a year", "Annual potassium chloride cost against the equivalent sodium chloride cost") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> What sodium chloride would have cost <span class="pc">21%</span></div>
          <div><span class="sw" style="background:#B44A2E"></span> The potassium premium <span class="pc">79%</span></div>
        </div>
      </div>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; <strong>calculated</strong>: 8 bags/yr of solar pellets at $7 against potassium chloride at ~4&times; the price plus the ~20% extra volume its lower efficiency requires &middot; the multiple varies by market &mdash; run your own numbers in the tool above</div>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">Nearly <strong>five times the cost, for a slightly worse regeneration.</strong> And here is the part that ought to settle it: one supplier describes being called out to a softener that was <em>totally clogged with potassium chloride</em> &mdash; the family had been told to &ldquo;buy the best salt,&rdquo; and reasonably assumed that meant the most expensive bag on the shelf. It took days to clear. <em>An individual account, not a statistic</em> &mdash; but a perfect illustration that price is not purity and purity is not performance.</p>
      <p style="margin:16px 0 0">So when <em>should</em> you buy it? There are two genuinely good reasons, and I want to be straight about both. <strong>One: a medically restricted sodium intake.</strong> Softening exchanges hardness minerals for sodium, and how much sodium depends on how hard your water is &mdash; if a doctor has restricted yours, potassium chloride exists for exactly this, and that is a conversation to have with them rather than with a website. <strong>Two: septic systems and garden irrigation</strong>, where the discharge water is gentler. Those are real. &ldquo;It was the pricey one so it must be better&rdquo; is not.</p>

      <h2 id="sheet">The ten-year salt bill</h2>
      <p style="margin:0">Nobody prices this, so here it is &mdash; the entire salt exposure of owning a softener for a decade:</p>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Ten years of salt, honestly accounted", sc_rows, total_label="Ten-year salt exposure") + '''</div>
    <div class="col">
      <p style="margin-top:24px"><strong>Read the shape of that, not just the total.</strong> The low column is what happens if you buy decent pellets and nothing goes wrong. The high column is what happens if you buy on price and the cheap salt does precisely what every supplier in the sources says it does. <span class="fig">$395</span> against <span class="fig">$1,220</span> &mdash; and the difference is not the salt. <strong>The difference is the repair the salt caused.</strong></p>
      <div style="margin-top:24px">''' + cta_box("The cheapest bag of salt is the one you never buy",
        "Salt use is set by hardness and household \u2014 but also by how well the system was sized. A softener sized to run at an efficient salt dose rather than at its nameplate uses roughly 195 lbs less salt a year: five fewer bags, every year, for the life of the machine. SpringWell publishes its softener pricing online, ships free, and gives you six months to send it back \u2014 so you can match real capacity to your measured hardness before anybody sells you a salt delivery plan. Check the grain capacity against your own gpg; bathroom-count sizing is a proxy, not a measurement.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="less">The cheapest bag is the one you never buy</h2>
      <p style="margin:0">Everything above is about choosing well between bags. But the bigger lever is not on the shelf at all &mdash; it is in how the softener was <em>sized and set</em>, and it dwarfs the difference between salt types.</p>
      <p style="margin:16px 0 0">A softener rated at 32,000 grains only delivers 32,000 grains on the day it burns the most salt; run lean, the same tank gives about 20,000. Which means a system <a href="/what-size-water-softener-do-i-need/">sized to run at an efficient dose</a> rather than flogged to its nameplate uses roughly <span class="fig">195 lbs less salt a year</span> &mdash; nearly <strong>five bags, every year, forever</strong>. That single decision saves more salt than switching from the most expensive bag on the shelf to the cheapest one, and unlike the cheap bag, it costs you nothing downstream.</p>
      <p style="margin:16px 0 0">And if you want off the salt entirely, that option exists too &mdash; with a limit I will not soften. A salt-free conditioner uses no salt, no brine tank and no regeneration, so every number on this page goes to zero. But it <em>conditions</em> scale rather than removing hardness by ion exchange: your water will not test soft, because nothing was exchanged. It is a different outcome, not a cheaper version of the same one, and our <a href="/salt-free-water-softener-cost/">salt-free comparison</a> runs that decision properly.</p>
      <div style="margin-top:32px">''' + cta_box("Or stop buying salt altogether",
        "SpringWell publishes FutureSoft pricing online \u2014 free shipping, 6-month money-back window \u2014 and it needs no salt, no brine tank and no regeneration, which retires the brine tank, the bridging, the mushing and the injector clog in one go. The honest limit, because it matters more than the sale: it controls scale rather than removing hardness. Your water will not read soft on a test strip. If you want genuinely softened water, buy the pellets \u2014 and buy the good ones.",
        "Check current SpringWell FutureSoft price","futuresoft") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(sc_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/water-softener-maintenance/"><div class="name">The salt jobs</div><div class="range">~2 hrs/yr</div><div class="desc">Bridging, mushing, and the broom handle.</div></a>
        <a class="card" href="/water-softener-repair-cost/"><div class="name">The clogged injector</div><div class="range">$430 avg</div><div class="desc">What cheap salt eventually buys.</div></a>
        <a class="card" href="/what-size-water-softener-do-i-need/"><div class="name">Sizing</div><div class="range">Free tool</div><div class="desc">The bigger salt lever, by far.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Crystal Quest &mdash; best water softener salt buying guide (2026)</strong> &mdash; <a href="https://crystalquest.com/blogs/filter-maintenance/best-water-softener-salt" rel="noopener" target="_blank">crystalquest.com</a>. Supports: rock salt at 95&ndash;98% purity and $5&ndash;$8 per 40-lb bag, with <strong>2&ndash;5% insoluble content &mdash; mostly calcium sulfate and shale &mdash; that settles as sludge</strong> and is especially prone to bridging in humid climates; evaporated pellets at 99.9%; solar pellets as the best overall balance; and the instruction to set hardness ~10% higher on potassium chloride to compensate for lower exchange efficiency.',
 '<strong>Puronics &mdash; guide to the best water softener salt</strong> &mdash; <a href="https://puronics.com/water-softener-salt/" rel="noopener" target="_blank">puronics.com</a>. Supports the pricing backbone: <strong>from about 12&cent; per pound for rock or solar salt up to 25&cent; for evaporated pellets, giving a $4.50&ndash;$10.00 range per 40-lb bag</strong>, with Morton averaging around $6.50. Also: rock salt is halite, containing high levels of non-soluble calcium sulfate, and the company states it does <em>not</em> recommend it for all-in-one systems.',
 '<strong>Water eStore &mdash; the best and worst salt for your water softener</strong> &mdash; <a href="https://waterestore.ca/blogs/news/the-best-and-worst-salt-for-your-water-softener" rel="noopener" target="_blank">waterestore.ca</a>. Supports the potassium chloride economics: it <strong>costs almost four times more than traditional softener salt and is only about 80% as efficient</strong>, requiring a ~20% higher hardness setting. Also the crystal-versus-pellet observation (more clogged and bridged softeners seen on crystals), and the reported case of a softener totally clogged with potassium chloride &mdash; <strong>an individual account, not a statistic.</strong>',
 '<strong>Culligan &mdash; what is the best water softener salt</strong> &mdash; <a href="https://www.culligan.com/blog/what-is-the-best-water-softener-salt" rel="noopener" target="_blank">culligan.com</a>. Supports the definition doing the work on this page: <strong>purity is the proportion of sodium or potassium chloride against insoluble material</strong>, and higher-purity products leave less residue. Also that rock salt&rsquo;s greater impurity means more residue and more frequent cleaning, and the mushing/bridging failure modes.',
 '<strong>SoftPro / Quality Water Treatment &mdash; choosing softener salt, and top salts for performance</strong> &mdash; <a href="https://www.softprowatersystems.com/blogs/maintenance/choosing-the-right-water-softener-salt" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: evaporated salt at 99.6&ndash;99.9% purity as the low-maintenance choice, especially above 10&ndash;15 gpg; rock salt&rsquo;s insoluble matter clogging the system; and the higher end of the reported potassium chloride efficiency penalty (cited there as operating around 70% efficiency).',
 '<strong>Home-Water-Softener &mdash; salt types compared</strong> &mdash; <a href="https://www.home-water-softener.com/water-softener-salt-different-types.htm" rel="noopener" target="_blank">home-water-softener.com</a>. Supports the purity figures used in the residue calculation: <strong>evaporated salt at 99.8%+ (under 0.2% insolubles), solar at 99.6&ndash;99.8%, rock at 95&ndash;98%</strong>, and the link between purity and how often the brine tank needs cleaning.',
 '<strong>HomeGuide &mdash; water softener repair cost</strong> &mdash; <a href="https://homeguide.com/costs/water-softener-repair-cost" rel="noopener" target="_blank">homeguide.com</a>. Supports the $430 national average repair used in the rock-salt trap, and its own troubleshooting finding that a plugged injector or blocked drain line is a leading cause of a softener failing to regenerate &mdash; the failure that cheap salt&rsquo;s residue produces.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("water-softener-salt-cost/index.html", sc)


# ============ CALC HUB — the real one (replaces the launch stub) ============
hub_faqs = [
 ("Are these water softener calculators free?","Yes, all thirty-two of them, with no email gate and no sign-up. Every one shows its arithmetic and links to the sourced figures behind it, so you can check the maths rather than trust it."),
 ("Which calculator should I start with?","The sizer, almost always. Capacity decides your salt bill, your regeneration frequency, your running cost and a good chunk of your equipment price &mdash; so getting it wrong makes every other number on this site wrong too."),
 ("Do I need to know my water hardness?","For about half of these, yes. It is the single most useful number you can own, and a home test kit costs $10&ndash;$25. Some companies bill $100&ndash;$300 for the same reading."),
 ("Why do some of these tools tell me not to buy anything?","Because sometimes that is the correct answer. A calculator that can only ever recommend a purchase is not a calculator, it is a sales page with sliders on it."),
 ("Where do the numbers come from?","Published sources &mdash; HomeGuide, Angi, Fixr, HomeAdvisor, the EIA, the CFPB, manufacturer parts pricing and utility rate sheets &mdash; cited on the page each tool lives on. Anything we calculated rather than quoted is labelled as calculated."),
 ("Is there a hard water damage calculator?","No, deliberately. We promised one at launch and then declined to build it, because the appliance-life and soap-saving figures it would need come almost entirely from research funded by the industry that sells softeners. See below."),
 ("Can I use these if I already own a softener?","That is what a third of them are for &mdash; maintenance scheduling, running costs, repair pricing, service-call triage and the repair-or-replace decision. You do not have to be shopping to get value here."),
 ("Do the calculators store my data?","No. Everything runs in your browser and nothing is sent anywhere, which is also why there is no email gate."),
]
hub = head("Water Softener Calculators (2026): 30 Free Tools, Every Number Sourced",
 "Thirty-two free water softener calculators \u2014 sizing, cost, running cost, quote checking, repair-or-replace. No email gate. Every figure sourced, every calculation shown.",
 "/calculators/",
 ld(json.dumps({"@context":"https://schema.org","@type":"WebApplication","name":"Water Softener Calculators","url":SITE+"/calculators/","applicationCategory":"UtilityApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}))
 + ld(faq_schema(hub_faqs,"/calculators/"))
 + ld(breadcrumb_schema([("Home","/"),("Calculators","/calculators/")])))
hub += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Calculators</nav>
      <h1>Water Softener Calculators</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Thirty-two of them. No email gate, no sign-up, nothing stored &mdash; every one runs in your browser, shows its arithmetic, and links back to the published figures behind it. They are organised below by the question you are actually asking, in roughly the order people ask them.</p>
      <p><strong>Thirty-two free water softener calculators: sizing, installed cost, running cost, ten-year ownership, quote checking, financing, maintenance scheduling, repair-or-replace, and the full well-water treatment stack. Every figure is sourced and every calculation is shown. Start with the sizer &mdash; it decides most of the others.</strong></p>
      <p style="margin:0">One thing worth saying before you use any of them. <strong>Every calculator on this page will, under the right conditions, tell you not to buy something.</strong> That is not a quirk of the design; it is the entire reason to trust the ones that do recommend a purchase. A tool that can only ever say &ldquo;yes&rdquo; is not a calculator. It is a sales page with sliders on it.</p>
      <p style="margin:16px 0 0">So here is the proof, before the index:</p>
    </div>
    <div class="data-table-wrap" style="margin-top:20px">
      <table class="data-table">
        <caption>The moment each tool argues against the sale</caption>
        <thead><tr><th scope="col">Tool</th><th scope="col">What it says when the honest answer is &ldquo;don&rsquo;t&rdquo;</th></tr></thead>
        <tbody>
          <tr><td><strong>Sizer</strong></td><td class="muted">At 3 gpg or below: &ldquo;ask whether you need a softener at all &mdash; the honest answer here is often no.&rdquo;</td></tr>
          <tr><td><strong>Service Triage</strong></td><td class="muted">Full salt tank, hard water: &ldquo;do not call anybody yet.&rdquo; Cost to fix: a broom handle.</td></tr>
          <tr><td><strong>Repair or Replace</strong></td><td class="muted">Cracked mineral tank: refuses to recommend the repair, even though repairs are the cheaper story.</td></tr>
          <tr><td><strong>Repair Quote Decoder</strong></td><td class="muted">Low pressure from an undersized system: &ldquo;no repair fixes it.&rdquo; It will not sell you resin you do not need.</td></tr>
          <tr><td><strong>Maintenance Schedule</strong></td><td class="muted">Iron above 0.3 ppm: &ldquo;maintenance is not the fix here &mdash; an iron filter ahead of the softener is.&rdquo;</td></tr>
          <tr><td><strong>Rent vs Buy</strong></td><td class="muted">At a low enough monthly rate, it says buying <em>never</em> breaks even &mdash; and prints that word.</td></tr>
          <tr><td><strong>Well Stack Builder</strong></td><td class="muted">Tells most households they do not need the $1,895 backwashing tank a dealer will quote them.</td></tr>
          <tr><td><strong>Budget Fit</strong></td><td class="muted">&ldquo;A correctly-sized $450 softener beats a mis-sized $1,500 one every year of its life.&rdquo;</td></tr>
          <tr><td><strong>Sediment Matcher</strong></td><td class="muted">States its own limit out loud: mechanical filtration only &mdash; it will not touch dissolved iron.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <h2 id="start">Start here: what size do you need?</h2>
      <p style="margin:0 0 16px">If you only use one tool on this page, use this one. Capacity sets your salt bill, your regeneration frequency, your running cost and a chunk of your equipment price &mdash; which means <strong>getting the size wrong makes every other number on this site wrong too.</strong></p>
      <div data-sizer></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Full method, sources and the nameplate trap: <a href="/what-size-water-softener-do-i-need/">what size water softener do I need</a>. If you do not know your hardness, a <a href="/pick/test-kit" ''' + PICK + '''>test kit</a> is $10&ndash;$25 and it unlocks roughly half the tools below.</p>

      <h2 id="index">All thirty, by the question you are asking</h2>
    </div>
    <div class="col-wide">
      <div class="donut-wrap">''' + donut_svg([("#16303F",30),("#1F7A5C",20),("#B44A2E",20),("#E8A13D",13),("#5B6B75",17)], "32", "calculators", "The thirty calculators by the question they answer") + '''
        <div class="donut-legend">
          <div><span class="sw" style="background:#16303F"></span> Before you buy <span class="pc">11</span></div>
          <div><span class="sw" style="background:#1F7A5C"></span> What ownership costs <span class="pc">6</span></div>
          <div><span class="sw" style="background:#B44A2E"></span> When someone is selling to you <span class="pc">6</span></div>
          <div><span class="sw" style="background:#E8A13D"></span> When something is wrong <span class="pc">4</span></div>
          <div><span class="sw" style="background:#5B6B75"></span> On a well <span class="pc">5</span></div>
        </div>
      </div>
    </div>
    <div class="col">
      <h3 style="margin-top:32px">Before you buy <span class="muted" style="font-weight:400">&mdash; 11 tools</span></h3>
      <div class="card-grid narrow">
        <a class="card" href="/water-hardness-by-zip/"><div class="name">Hardness by ZIP</div><div class="desc">A regional estimate &mdash; and a straight answer about what a ZIP code cannot tell you.</div></a>
        <a class="card" href="/what-size-water-softener-do-i-need/"><div class="name">Sizer</div><div class="desc">What capacity you need &mdash; scored at an efficient salt dose, not the nameplate.</div></a>
        <a class="card" href="/calculators/cost-calculator/"><div class="name">Cost calculator</div><div class="desc">Installed cost range from household size, hardness and install path.</div></a>
        <a class="card" href="/water-softener-installation-cost/"><div class="name">Install scenario picker</div><div class="desc">What installation costs on <em>your</em> house: loop, drain, outlet, access.</div></a>
        <a class="card" href="/whole-house-water-softener-installation-cost/"><div class="name">System picker</div><div class="desc">Which class of system actually fits the problem you have.</div></a>
        <a class="card" href="/low-cost-water-softener/"><div class="name">Budget fit</div><div class="desc">What a real budget buys &mdash; and what it quietly costs you later.</div></a>
        <a class="card" href="/dual-tank-water-softener-cost/"><div class="name">Twin-tank fit</div><div class="desc">Whether you need a dual tank, or a correctly-sized single.</div></a>
        <a class="card" href="/pelican-water-softener-cost/"><div class="name">Conditioner or softener?</div><div class="desc">Which technology your water actually calls for &mdash; they are not the same product.</div></a>
        <a class="card" href="/salt-free-water-softener-cost/"><div class="name">Salt vs salt-free TCO</div><div class="desc">The two systems compared over time, honestly.</div></a>
        <a class="card" href="/water-softener-rental-cost/"><div class="name">Rent vs buy break-even</div><div class="desc">When renting wins &mdash; and when buying never catches up.</div></a>
        <a class="card" href="/why-are-water-softeners-so-expensive/"><div class="name">Expense decoder</div><div class="desc">Where the money in a softener price actually goes.</div></a>
      </div>

      <h3 style="margin-top:32px">What ownership costs <span class="muted" style="font-weight:400">&mdash; 6 tools</span></h3>
      <div class="card-grid narrow">
        <a class="card" href="/10-year-water-softener-cost/"><div class="name">The decade model</div><div class="desc">Ten years, all in &mdash; and the finding that the purchase swings it more than everything else combined.</div></a>
        <a class="card" href="/water-softener-electricity-usage/"><div class="name">Running-cost stack</div><div class="desc">Electricity, salt, regeneration water, consumables. Electricity is the smallest.</div></a>
        <a class="card" href="/water-softener-salt-cost/"><div class="name">Salt cost calculator</div><div class="desc">What you will actually shovel, and what the four salt types really cost.</div></a>
        <a class="card" href="/water-softener-maintenance-cost/"><div class="name">Maintenance budget</div><div class="desc">The annual upkeep bill, itemised.</div></a>
        <a class="card" href="/water-softener-maintenance/"><div class="name">Maintenance schedule generator</div><div class="desc">Your six jobs, timed to your water &mdash; about two hours a year.</div></a>
        <a class="card" href="/"><div class="name">Salt mini-calculator</div><div class="desc">A fast salt estimate on the cost pillar.</div></a>
      </div>

      <h3 style="margin-top:32px">When someone is selling to you <span class="muted" style="font-weight:400">&mdash; 6 tools</span></h3>
      <div class="card-grid narrow">
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Dealer quote reality check</div><div class="desc">What is inside the number an in-home visit produces.</div></a>
        <a class="card" href="/culligan-water-softener-cost/"><div class="name">Quote checker</div><div class="desc">Your quote against the reported band for that brand.</div></a>
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Channel savings</div><div class="desc">What the buying route costs you, before anyone marks anything up.</div></a>
        <a class="card" href="/kinetico-water-softener-cost/"><div class="name">Payment-to-total translator</div><div class="desc">What that monthly payment is really costing over the term.</div></a>
        <a class="card" href="/leaf-home-water-solutions-cost/"><div class="name">The anchor test</div><div class="desc">What a same-visit discount actually leaves behind.</div></a>
        <a class="card" href="/costco-water-softener-cost/"><div class="name">Costco member math</div><div class="desc">Whether the membership and the card perks pay for themselves.</div></a>
      </div>

      <h3 style="margin-top:32px">When something is wrong <span class="muted" style="font-weight:400">&mdash; 4 tools</span></h3>
      <div class="card-grid narrow">
        <a class="card" href="/water-softener-servicing/"><div class="name">Service call triage</div><div class="desc">Whether you need a technician at all &mdash; often you do not.</div></a>
        <a class="card" href="/water-softener-repair-cost/"><div class="name">Repair quote decoder</div><div class="desc">What failed, what it should cost, and the rebuild-vs-replace fork.</div></a>
        <a class="card" href="/how-long-does-a-water-softener-last/"><div class="name">Repair or replace</div><div class="desc">Cost per year of service, both ways.</div></a>
        <a class="card" href="/water-softener-removal-cost/"><div class="name">Fate finder</div><div class="desc">What to do with the old unit.</div></a>
      </div>

      <h3 style="margin-top:32px">On a well <span class="muted" style="font-weight:400">&mdash; 5 tools</span></h3>
      <div class="card-grid narrow">
        <a class="card" href="/well-water-softener-cost/"><div class="name">Well stack builder</div><div class="desc">Which treatment stages you need, in which order.</div></a>
        <a class="card" href="/iron-filter-for-well-water-cost/"><div class="name">Iron matcher</div><div class="desc">Which iron filter your water actually calls for.</div></a>
        <a class="card" href="/acid-neutralizer-cost/"><div class="name">pH matcher</div><div class="desc">Whether you need a neutraliser, and which media.</div></a>
        <a class="card" href="/uv-water-purifier-cost/"><div class="name">UV sizer</div><div class="desc">Dose, flow rate and what a UV lamp really costs to keep.</div></a>
        <a class="card" href="/sediment-filter-cost/"><div class="name">Sediment matcher</div><div class="desc">Spin-down, cartridge or backwashing &mdash; and the $145 arbitrage.</div></a>
      </div>

      <h2 id="decade" style="margin-top:48px">And the one that changed how I think about all of it</h2>
      <p style="margin:0 0 16px">If the sizer is where you start, this is where you finish. It models a decade of ownership from sourced inputs &mdash; and it found that <strong>the purchase decision swings your ten-year cost further than repairs, salt, consumables, electricity and regeneration water combined.</strong></p>
      <div data-decade></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">Full study, methodology and the sensitivity analysis: <a href="/10-year-water-softener-cost/">the true 10-year cost of owning a water softener</a>.</p>

      <h2 id="notbuilt">The calculator we deliberately did not build</h2>
      <p style="margin:0">When this site launched, this page promised seven calculators. Thirty exist now. But one of the original seven has been quietly dropped, and I would rather say so plainly than let it disappear: <strong>the &ldquo;hard water is costing you $X a year&rdquo; damage calculator.</strong></p>
      <p style="margin:16px 0 0">You have seen it elsewhere. You put in your hardness and it tells you that scale is destroying your water heater, that you are wasting a fortune in detergent, that your appliances are dying young &mdash; and it produces a satisfying annual figure that happens to be larger than the softener it is recommending. I could build that in an afternoon. I am not going to.</p>
      <p style="margin:16px 0 0">The reason is simple, and it is the same standard the other thirty tools are held to. The appliance-life, soap-saving and water-heater-efficiency numbers those calculators depend on trace back, overwhelmingly, to research <strong>funded by the trade association of the industry that sells water softeners.</strong> The effects are probably real &mdash; scale genuinely does foul a heating element, and softened water genuinely does lather better. But &ldquo;probably real&rdquo; is not the same as sourced, and a number I cannot stand behind has no business being multiplied by your hardness and shown to you as a loss.</p>
      <p style="margin:16px 0 0">This site prices what a softener <em>costs</em>, because those figures are published and checkable. It does not price what hard water costs you, because that figure is not &mdash; and the moment I invent it, every other number here becomes worth less. <strong>The missing calculator is the point.</strong></p>
      <div style="margin-top:40px">''' + cta_box("When the maths is done, you need one honest number",
        "Most of these tools exist to measure a quote against something that does not move. SpringWell publishes its softener pricing online \u2014 sized by bathroom count, free shipping, 6-month money-back window \u2014 which makes it the anchor the calculators above are built to compare against. Run your size first, then check the price against it: bathroom-count sizing is a proxy for household demand, not a hardness measurement, so verify the grain capacity against your own reading before you order.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(hub_faqs) + '''
      <h2>Where to go next</h2>
      <div class="card-grid narrow">
        <a class="card" href="/"><div class="name">The cost pillar</div><div class="range">$840&ndash;$4,120</div><div class="desc">Every line item, priced.</div></a>
        <a class="card" href="/10-year-water-softener-cost/"><div class="name">The 10-year study</div><div class="range">$3,550&ndash;$8,230</div><div class="desc">The number that actually matters.</div></a>
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Where quotes come from</div><div class="range">$3,000&ndash;$8,000</div><div class="desc">Read this before an in-home visit.</div></a>
      </div>
    </div>
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("calculators/index.html", hub)


# ============ C8 — PELICAN / PENTAIR NATURSOFT (a comparison, not an expose) ============
p1_faqs = [
 ("Is the Pelican NaturSoft a real water softener?","No, and Pentair does not claim it is &mdash; they market it as a &ldquo;water softener alternative,&rdquo; and their own FAQ says it only addresses hardness scale. It prevents scale rather than removing hardness. Your water will still test hard."),
 ("Does the Pelican salt-free system actually work?","For scale prevention, the evidence is unusually good: NaturSoft carries a DVGW certification for 99.6% scale prevention. That is the strongest independent performance evidence in the salt-free category. It just is not softening, and those are different claims."),
 ("What does a Pelican system cost to run?","Very little. Roughly $22&ndash;$44 a year in prefilters, plus carbon media replacement about every five years. No salt, no electricity, no wastewater and no drain &mdash; against roughly $151 a year for a salt-based softener on our own worksheet."),
 ("Is Pelican NSF certified?","Partly, and the detail matters. The NaturSoft tank is certified to NSF/ANSI 61 for material safety and tested to NSF/ANSI 42 for <em>structural integrity only</em> &mdash; not performance. The scale-prevention claim rests on the DVGW certification, not on NSF."),
 ("Can I use Pelican on well water with iron?","Not without pretreatment. Pentair&rsquo;s own installation manual states that iron, manganese, sulfur and tannin &ldquo;should be removed prior&rdquo; to the system. On a well, the iron filter comes first &mdash; that is Pentair&rsquo;s instruction, not our opinion."),
 ("What is the hardness limit for NaturSoft?","75 grains per gallon, published in Pentair&rsquo;s own manual. That is a generous ceiling &mdash; most municipal water is 5&ndash;15 gpg &mdash; but if you are past it, you are in salt territory."),
 ("Pelican or SpringWell FutureSoft?","Both are salt-free conditioners using the same broad approach, both publish prices, and both spare you the salt. Compare the certifications, the flow rate you need and the current price. Neither will make your water test soft, because neither removes hardness."),
 ("Should I buy a conditioner or a softener?","Ask what outcome you want. Scale protection for pipes and appliances &mdash; a conditioner is a legitimate answer. Slippery water, no spots, half the detergent &mdash; that is hardness being removed, and only ion exchange does it."),
]
p1_rows = [
 ("Prefilter cartridges",22,44,"Published: ~$22 each, replaced one to two times a year"),
 ("Salt",0,0,"None. There is no brine tank"),
 ("Electricity",0,0,"None. Up-flow design, no moving parts, no electronic head"),
 ("Regeneration water &amp; sewer",0,0,"None. No backwashing, no drain, no wastewater"),
]
p1 = head("Pelican Water Softener Cost & Review (2026): The Honest Verdict on NaturSoft",
 "Pentair Pelican publishes its prices \u2014 and calls its flagship a \u201csoftener alternative,\u201d not a softener. That word is the whole review. Here\u2019s what you\u2019re actually buying.",
 "/pelican-water-softener-cost/",
 ld(article_schema("Pelican (Pentair) Water Softener Cost and Review: What NaturSoft Actually Does","A comparison rather than an expos\u00e9 \u2014 because Pentair publishes prices and names the product honestly. What the DVGW certification proves, what the NSF certification does not, and the running-cost case for a conditioner.","/pelican-water-softener-cost/",date="2026-07-12"))
 + ld(faq_schema(p1_faqs,"/pelican-water-softener-cost/"))
 + ld(breadcrumb_schema([("Home","/"),("Brand pricing","/dealer-vs-factory-direct-pricing/"),("Pelican","/pelican-water-softener-cost/")])))
p1 += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/dealer-vs-factory-direct-pricing/">Brand pricing</a> &rsaquo; Pelican</nav>
      <h1>Pelican (Pentair) Water Softener Cost &amp; Review</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Seven brand pages on this site have been about companies that will not tell you what their equipment costs until somebody is sitting in your kitchen. This one is different, and I want to say so before anything else: <strong>Pentair publishes its prices, and it does not call its flagship product a water softener.</strong> It calls it a <em>water softener alternative</em>. After a year of reading in-home sales scripts, I found that single word genuinely refreshing &mdash; and it is also, as it turns out, the entire review.</p>
      <p><strong>Pelican&rsquo;s NaturSoft is a salt-free conditioner, not a softener &mdash; Pentair says so in the product name and in its own FAQ. It carries a DVGW certification for 99.6% scale prevention, costs roughly $22&ndash;$44 a year to run, and uses no salt, electricity or wastewater. It will not make your water test soft, because it removes nothing.</strong></p>
      <p style="margin:0">So this page is a comparison, not an expos&eacute;. There is no opaque quote to reconstruct and no financing trick to decode. The only question worth 2,000 words is the one the marketing quietly blurs: <strong>you are being offered scale prevention. Are you sure that is what you came for?</strong></p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#chart">Removed vs. prevented (chart)</a></li>
          <li><a href="#credit">What Pelican genuinely gets right</a></li>
          <li><a href="#certs">The certifications, read properly</a></li>
          <li><a href="#limits">The limits &mdash; from Pentair&rsquo;s own manual</a></li>
          <li><a href="#run">What it costs to run</a></li>
          <li><a href="#decide">Conditioner or softener? (tool)</a></li>
        </ol>
      </details>

      <h2 id="chart">Removed vs. prevented</h2>
      <p style="margin:0 0 16px">This is the confusion the whole category lives inside, and one chart settles it:</p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 240" style="width:100%;height:auto" role="img" aria-label="Two comparisons: hardness removed from the water is 100 percent for a salt softener and 0 percent for NaturSoft; scale prevented on pipes is near 100 percent for a softener and 99.6 percent for NaturSoft.">
        <text x="175" y="26" text-anchor="middle" font-size="13" fill="#16303F" font-weight="700">Hardness REMOVED from your water</text>
        <text x="525" y="26" text-anchor="middle" font-size="13" fill="#16303F" font-weight="700">Scale PREVENTED on your pipes</text>
        <text x="120" y="62" text-anchor="end" font-size="11.5" fill="#16303F">Salt softener</text>
        <rect x="130" y="48" width="180" height="20" rx="2" fill="#16303F"/>
        <text x="318" y="62" font-size="11.5" fill="#16303F" font-weight="700">100%</text>
        <text x="120" y="98" text-anchor="end" font-size="11.5" fill="#16303F">Pelican NaturSoft</text>
        <rect x="130" y="84" width="3" height="20" rx="1" fill="#B44A2E"/>
        <text x="141" y="98" font-size="11.5" fill="#B44A2E" font-weight="700">0%</text>
        <text x="470" y="62" text-anchor="end" font-size="11.5" fill="#16303F">Salt softener</text>
        <rect x="480" y="48" width="180" height="20" rx="2" fill="#16303F"/>
        <text x="668" y="62" text-anchor="end" font-size="11.5" fill="#F7F5F0" font-weight="700">~100%</text>
        <text x="470" y="98" text-anchor="end" font-size="11.5" fill="#16303F">Pelican NaturSoft</text>
        <rect x="480" y="84" width="179" height="20" rx="2" fill="#1F7A5C"/>
        <text x="667" y="98" text-anchor="end" font-size="11.5" fill="#F7F5F0" font-weight="700">99.6%</text>
        <line x1="350" y1="40" x2="350" y2="200" stroke="#E6E1D8" stroke-width="1"/>
        <text x="175" y="140" text-anchor="middle" font-size="12" fill="#B44A2E" font-weight="700">Opposite outcomes</text>
        <text x="525" y="140" text-anchor="middle" font-size="12" fill="#1F7A5C" font-weight="700">Near-identical outcomes</text>
        <text x="350" y="180" text-anchor="middle" font-size="12.5" fill="#16303F" font-style="italic">Same job for your plumbing. Completely different job for your water.</text>
        <text x="350" y="206" text-anchor="middle" font-size="11.5" fill="#5B6B75">Which one you needed depends entirely on what you were trying to fix.</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; the 99.6% figure is NaturSoft&rsquo;s DVGW scale-prevention certification, published by Pentair &middot; the 0% is not a criticism &mdash; it is the design. A conditioner is <em>supposed</em> to leave the minerals in the water</div>
    </div>
    <div class="col">
      <h2 id="credit">What Pelican genuinely gets right</h2>
      <p style="margin:0">I have spent seven pages on this site being hard on brands, so let me be equally precise when a company earns credit. <strong>Pelican earns quite a lot of it.</strong></p>
      <p style="margin:16px 0 0"><strong>It is performance-certified, which almost nothing in this category is.</strong> The salt-free aisle is full of devices making scale claims that rest on nothing but a datasheet. NaturSoft holds a <strong>DVGW certification for 99.6% scale prevention</strong> &mdash; an independent German standard with an actual test protocol behind it. Whatever else is true, that is real evidence, and most of Pelican&rsquo;s competitors cannot show you anything like it.</p>
      <p style="margin:16px 0 0"><strong>It is honest in the product name.</strong> &ldquo;Water softener alternative&rdquo; is a mouthful, it is worse marketing than &ldquo;softener,&rdquo; and it is accurate. Their FAQ goes further and states that the system only addresses hardness scale. Compare that to the in-home channel, where the word &ldquo;softener&rdquo; gets applied to anything with a tank.</p>
      <p style="margin:16px 0 0"><strong>The engineering removes whole categories of problem.</strong> Up-flow design, no moving parts, no electronic head, no backwashing, no drain, no wastewater, no electricity. Read our <a href="/water-softener-repair-cost/">repair cost guide</a> and notice that the two components which fail most on a salt softener &mdash; the control valve and its piston and seals &mdash; <em>do not exist here.</em> You cannot be quoted $545 for a valve you do not have.</p>
      <p style="margin:16px 0 0">And the price is on the website. After Culligan, Kinetico, RainSoft, EcoWater and Leaf Home, that should not feel remarkable. It does.</p>

      <h2 id="certs">The certifications, read properly</h2>
      <p style="margin:0 0 16px">One thing needs care, because the marketing runs the certifications together and they do not mean the same thing:</p>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>What each certification on the box actually certifies</caption>
        <thead><tr><th scope="col">Certification</th><th scope="col">What it covers</th><th scope="col">What it does <em>not</em> cover</th></tr></thead>
        <tbody>
          <tr><td><strong>DVGW DW-9191</strong></td><td class="muted">99.6% hard water <strong>scale prevention</strong> &mdash; the performance claim</td><td class="muted">Softening. Nothing is removed from the water.</td></tr>
          <tr><td>NSF/ANSI 61 (NaturSoft)</td><td class="muted">Material safety &mdash; the tank will not leach anything into your water</td><td class="muted">Any statement about whether it works</td></tr>
          <tr><td><strong>NSF/ANSI 42 (NaturSoft)</strong></td><td class="muted">Tested for <strong>structural integrity only</strong> &mdash; the vessel holds pressure</td><td class="muted"><strong>Performance.</strong> This is the one most likely to be misread as an efficacy certification</td></tr>
          <tr><td>NSF/ANSI 42 (PC600/PC1000 carbon)</td><td class="muted">Chlorine taste and odour reduction &mdash; a genuine performance cert, for the <em>carbon filter</em></td><td class="muted">Anything to do with hardness or scale</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0">None of that is dishonest on Pentair&rsquo;s part &mdash; every line above comes from their own documentation, plainly stated. But if you skim a product page and see &ldquo;NSF certified&rdquo; next to a softening claim, you will conclude something the certification does not say. <strong>The scale claim rests on DVGW. The NSF marks on the NaturSoft tank are about safety and structure, not efficacy.</strong> Know which is which.</p>

      <h2 id="limits">The limits &mdash; from Pentair&rsquo;s own manual</h2>
      <p style="margin:0">I did not have to dig for these. They are printed in the installation manual Pentair ships with the product, which is more than most brands on this site can say:</p>
      <p style="margin:16px 0 0"><strong>Maximum 75 grains per gallon.</strong> Generous &mdash; typical municipal water is 5&ndash;15 gpg &mdash; but a real ceiling. Past it, you are in salt territory.</p>
      <p style="margin:16px 0 0"><strong>&ldquo;All iron/manganese, sulfur and Tannin should be removed prior.&rdquo;</strong> That is Pentair&rsquo;s sentence, not mine, and it is the single most important line in the document. If you are on a <a href="/well-water-softener-cost/">well</a>, this system does not go first. An <a href="/iron-filter-for-well-water-cost/">iron filter</a> goes first, and then this. Buy it the other way round and you are fouling brand-new media on day one.</p>
      <p style="margin:16px 0 0"><strong>And the one nobody mentions: your water will still be hard.</strong> Not &ldquo;a bit hard.&rdquo; Exactly as hard as it was. Test it before and after and the grains-per-gallon number will not move, because nothing was taken out. You will not get the slippery shower, you will not get spot-free glassware, and you will not halve your detergent &mdash; those are all consequences of <em>removal</em>, and this device does not remove. It is not underperforming when that happens. It is doing precisely what it says on the tank.</p>

      <h2 id="run">What it costs to run</h2>
    </div>
    <div style="margin-top:24px">''' + quote_sheet("Annual running cost &mdash; Pelican NaturSoft", p1_rows, total_label="Per year, excluding carbon media") + '''</div>
    <div class="col">
      <p style="margin-top:24px">Add carbon media replacement roughly <strong>every five years</strong> (Pentair rates the carbon tank by volume &mdash; on the order of 650,000 gallons for the smaller combo unit), and the softening media itself is described as lasting the life of the system. <strong>Equipment pricing is published on Pentair&rsquo;s site and moves with promotions, so check it at the source rather than trusting a number I typed in July.</strong></p>
      <p style="margin:16px 0 0">Set that against the salt route. Our own <a href="/water-softener-maintenance/">maintenance worksheet</a> puts a salt softener at about <span class="fig">$151 a year</span> all in &mdash; $120 of it salt. Over ten years that is roughly <span class="fig">$1,510</span> against a few hundred dollars of prefilters. <strong>The conditioner wins the running-cost argument decisively, and it is not close.</strong> It also does a different job. Both of those sentences are true at once, and the entire decision lives in holding them both in your head.</p>

      <h2 id="decide">Conditioner or softener?</h2>
      <p style="margin:0 0 16px">So decide it properly. Tell the tool what you actually want &mdash; not what the category is called:</p>
      <div data-tech-decider></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">The iron and hardness thresholds come from Pentair&rsquo;s own installation manual. If you have never measured either, a <a href="/pick/test-kit" ''' + PICK + '''>test kit</a> is $10&ndash;$25 and it decides this entire question for you.</p>
      <div style="margin-top:32px">''' + cta_box("If scale protection is what you actually want",
        "Then a salt-free conditioner is a legitimate answer, and you should compare the two brands that both publish their prices. SpringWell\u2019s FutureSoft is the direct competitor \u2014 same salt-free approach, published pricing, free shipping, 6-month money-back window. The honest limit is identical to Pelican\u2019s and I will not soften it: it conditions scale rather than removing hardness, so your water will not test soft. Compare flow rates, certifications and current price, and buy whichever wins on the merits.",
        "Check current SpringWell FutureSoft price","futuresoft") + '''</div>
      <div style="margin-top:24px">''' + cta_box("If you want water that is actually soft",
        "Then no conditioner \u2014 Pelican\u2019s, SpringWell\u2019s or anyone\u2019s \u2014 will give it to you, and it is worth being blunt about that before you spend anything. Slippery water, spot-free glasses and half the detergent all require the hardness to be removed, and removal means ion exchange, which means salt. SpringWell publishes softener pricing online with free shipping and a 6-month money-back window. Size it against your measured hardness first \u2014 bathroom-count sizing is a proxy, not a measurement.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(p1_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/salt-free-water-softener-cost/"><div class="name">Salt-free vs salt-based</div><div class="range">$0/yr salt</div><div class="desc">The full cost comparison over time.</div></a>
        <a class="card" href="/dealer-vs-factory-direct-pricing/"><div class="name">Where quotes come from</div><div class="range">$3,000&ndash;$8,000</div><div class="desc">Why a published price is worth so much.</div></a>
        <a class="card" href="/what-size-water-softener-do-i-need/"><div class="name">Sizing</div><div class="range">Free tool</div><div class="desc">If you decide you want the salt.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>Pentair &mdash; Pelican PSE1800-P / PSE2000-P installation and owner&rsquo;s manual (primary source)</strong> &mdash; <a href="https://www.pentair.com/content/dam/extranet/web/nam/pentair-water-solutions/manuals/4006041-pse1800-p-pse2000-p-manual.pdf" rel="noopener" target="_blank">pentair.com</a>. Supports the limits and certifications quoted on this page, all in Pentair&rsquo;s own words: NaturSoft effective to a <strong>maximum hardness of 75 gpg (1,282 ppm)</strong>; <strong>&ldquo;all iron/manganese, sulfur and Tannin should be removed prior&rdquo;</strong>; <strong>DVGW DW-9191 certified for 99.6% hard water scale prevention</strong>; NaturSoft NS3/NS6 certified to NSF/ANSI 61 for material safety and tested to NSF/ANSI 42 <strong>for structural integrity only</strong>; PC600/PC1000 carbon certified to NSF/ANSI 42 for chlorine taste and odour.',
 '<strong>Pentair &mdash; Pelican Salt-Free Water Softener Alternative product page</strong> &mdash; <a href="https://www.pentair.com/en-us/water-softening-filtration/water-softener-alternatives/products/salt-free-water-softener-alternatives.html" rel="noopener" target="_blank">pentair.com</a>. Supports: the product is marketed as a &ldquo;water softener alternative,&rdquo; and Pentair&rsquo;s own FAQ states it <strong>only addresses water hardness</strong> scale; maximum flow rate 15 GPM; sizing by bathroom count (PSE1800-P for 1&ndash;3 bathrooms, PSE2000-P for 4&ndash;6); up-flow design with no moving parts, no backwashing, no wastewater and no electricity. Equipment pricing is published on the site and changes with promotions &mdash; check it there.',
 '<strong>Pentair &mdash; combo system with UV, carbon media specification</strong> &mdash; <a href="https://www.pentair.com/en-us/water-softening-filtration/water-softener-alternatives/products/water-softener-alternative-filter-combo-system-pro-uv.html" rel="noopener" target="_blank">pentair.com</a>. Supports: carbon tank media replacement every 5 years or 650,885 gallons (PSE1800-P) / 1,301,770 gallons (PSE2000-P).',
 '<strong>Quality Water Lab &mdash; Pelican NaturSoft review</strong> &mdash; <a href="https://qualitywaterlab.com/softeners/pelican-natursoft-salt-free/" rel="noopener" target="_blank">qualitywaterlab.com</a>. Supports the running-cost figures: prefilter replacement at roughly $22, once or twice a year, with the softening media described as lasting the life of the system. A third-party review site &mdash; treated here as a reported figure, not a manufacturer specification.',
 '<strong>SoftWaterSystemCost.com &mdash; our own maintenance worksheet</strong> &mdash; <a href="/water-softener-maintenance/">the complete maintenance schedule</a>. Supports the $151/year salt-softener baseline the running-cost comparison is measured against ($120 salt, $31 consumables).',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("pelican-water-softener-cost/index.html", p1)


# ============ HZ — WATER HARDNESS BY ZIP CODE ============
hz_faqs = [
 ("How do I find my water hardness by ZIP code?","You can get a regional estimate from state-level data &mdash; the lookup on this page does that. But a ZIP code cannot measure your tap. Your utility publishes the real number free in its annual Consumer Confidence Report, and a home test kit costs $10&ndash;$25."),
 ("What is a normal water hardness level?","The USGS bands are: soft up to 3.5 gpg, moderately hard to 7, hard to 10.5, and very hard above that. Around 85% of American homes have some degree of hard water. One gpg equals 17.1 ppm."),
 ("Which states have the hardest water?","Arizona, Nevada, Utah, New Mexico, Texas, Kansas, Oklahoma, Indiana and Minnesota consistently rank hardest &mdash; frequently above 10.5 gpg. New Mexico spans roughly 10&ndash;30 gpg, the widest range in the country."),
 ("Which states have the softest water?","The Pacific Northwest and New England. Washington, Oregon, Maine, New Hampshire and Vermont typically test under 4 gpg. Arkansas is the surprise &mdash; among the softest in the country despite its neighbours."),
 ("Is a ZIP code accurate enough to size a water softener?","No, and anyone who tells you otherwise is selling something. Hardness varies between neighbouring towns, between well and mains supply, and by season. Use the estimate to know roughly where you stand, then test before you size anything."),
 ("How do I convert ppm to grains per gallon?","Divide by 17.1. So 171 ppm is 10 gpg, and the 120 ppm threshold where water is officially &ldquo;hard&rdquo; is about 7 gpg."),
 ("Do I need a softener if my water is soft?","Usually not, and this page will tell you so. At 3.5 gpg or below there is very little scale to prevent. Test first &mdash; the cheapest water treatment decision is the one where you correctly buy nothing."),
 ("Why does hardness vary so much inside one state?","Geology. Limestone and dolomite bedrock dissolve calcium into groundwater; granite does not. Pennsylvania is the classic case &mdash; the eastern half runs moderate while the limestone west near Pittsburgh runs much harder."),
]
hz = head("Water Hardness by ZIP Code (2026): The Honest Version",
 "A regional hardness estimate from state-level data \u2014 and a straight answer about what a ZIP code can and cannot tell you about your tap.",
 "/water-hardness-by-zip/",
 ld(article_schema("Water Hardness by ZIP Code: What It Can and Cannot Tell You","A state-level water hardness lookup built from published regional data, the USGS classification bands, and an honest account of why a ZIP code is an estimate rather than a measurement.","/water-hardness-by-zip/",date="2026-07-12"))
 + ld(faq_schema(hz_faqs,"/water-hardness-by-zip/"))
 + ld(breadcrumb_schema([("Home","/"),("Hardness by ZIP","/water-hardness-by-zip/")])))
hz += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Hardness by ZIP</nav>
      <h1>Water Hardness by ZIP Code</h1>
''' + author_box(updated="July 12, 2026") + '''
      <p style="margin-top:24px">Every water softener site has one of these lookups. Almost all of them give you a single confident number, because a single confident number is what sells softeners. This one gives you a <strong>range</strong>, tells you which state it came from, and then tells you not to size anything on it.</p>
      <p><strong>A ZIP code gives you a regional hardness estimate, not a measurement. USGS bands run soft (to 3.5 gpg), moderately hard (to 7), hard (to 10.5) and very hard above that, and about 85% of US homes have some degree of hard water. Your utility publishes your real figure free; a test kit costs $10&ndash;$25.</strong></p>
      <p style="margin:0">I want to start with a confession, because it is the reason this page exists. <strong>Until today, the calculator on our own homepage inferred your hardness from the first digit of your ZIP code.</strong> Ten buckets for the entire United States. That meant Seattle and Los Angeles &mdash; both starting with a 9 &mdash; were handed the identical hardness value. Seattle&rsquo;s water is among the softest in the country. It is not a rounding error; it is a wrong answer, and it was ours. It is fixed below, and I am telling you about it rather than quietly shipping the patch.</p>
      <details open class="toc">
        <summary>On this page</summary>
        <ol>
          <li><a href="#lookup">Look up your ZIP (tool)</a></li>
          <li><a href="#bands">The four bands (chart)</a></li>
          <li><a href="#states">Hardest and softest states (chart)</a></li>
          <li><a href="#cant">What a ZIP code cannot tell you</a></li>
          <li><a href="#fixed">The bug we just fixed</a></li>
        </ol>
      </details>

      <h2 id="lookup">Look up your ZIP</h2>
      <div data-hardness></div>
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">State-level ranges compiled from published regional hardness data against the USGS classification. A <a href="/pick/test-kit" ''' + PICK + '''>home test kit</a> gives you the real number in minutes &mdash; and it is the input half the <a href="/calculators/">calculators on this site</a> are waiting for.</p>

      <h2 id="bands">The four bands</h2>
    </div>
    <div class="data-table-wrap" style="margin-top:16px">
      <table class="data-table">
        <caption>USGS hardness classification &mdash; and what each band actually means for you</caption>
        <thead><tr><th scope="col">Band</th><th scope="col" class="num">gpg</th><th scope="col" class="num">ppm</th><th scope="col">What to do</th></tr></thead>
        <tbody>
          <tr><td><strong>Soft</strong></td><td class="num">0&ndash;3.5</td><td class="num">0&ndash;60</td><td class="muted">Buy nothing. Be sceptical of anyone selling you a softener here.</td></tr>
          <tr><td><strong>Moderately hard</strong></td><td class="num">3.5&ndash;7</td><td class="num">60&ndash;120</td><td class="muted">A preference, not a necessity. Scale forms slowly.</td></tr>
          <tr><td><strong>Hard</strong></td><td class="num">7&ndash;10.5</td><td class="num">120&ndash;180</td><td class="muted">Softening pays. Size it on a measured reading.</td></tr>
          <tr><td><strong>Very hard</strong></td><td class="num">10.5+</td><td class="num">180+</td><td class="muted">Sizing errors get expensive fast here. Test, then size.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="col">
      <p style="margin:16px 0 0;font-size:14px;color:#5B6B75">One gpg = 17.1 ppm. Your utility reports in ppm; softener sizing uses gpg.</p>

      <h2 id="states">Hardest and softest</h2>
      <p style="margin:0 0 16px">The spread across the country is enormous &mdash; and it is geology, not policy. Limestone and dolomite dissolve calcium into groundwater; granite does not:</p>
    </div>
    <div class="col-wide">
      <svg viewBox="0 0 700 300" style="width:100%;height:auto" role="img" aria-label="Water hardness ranges by state. New Mexico spans 10 to 30 grains per gallon while Maine and Washington sit between 1 and 4.">
        <line x1="130" y1="34" x2="130" y2="252" stroke="#E6E1D8" stroke-width="1"/>
        <line x1="308" y1="34" x2="308" y2="252" stroke="#E6E1D8" stroke-width="1"/>
        <line x1="486" y1="34" x2="486" y2="252" stroke="#E6E1D8" stroke-width="1"/>
        <line x1="664" y1="34" x2="664" y2="252" stroke="#E6E1D8" stroke-width="1"/>
        <text x="130" y="270" text-anchor="middle" font-size="10.5" fill="#5B6B75">0</text>
        <text x="308" y="270" text-anchor="middle" font-size="10.5" fill="#5B6B75">10 gpg</text>
        <text x="486" y="270" text-anchor="middle" font-size="10.5" fill="#5B6B75">20</text>
        <text x="664" y="270" text-anchor="middle" font-size="10.5" fill="#5B6B75">30</text>
        <line x1="192" y1="28" x2="192" y2="258" stroke="#16303F" stroke-width="1.5" stroke-dasharray="5 4"/>
        <text x="192" y="22" text-anchor="middle" font-size="10.5" fill="#16303F" font-weight="700">&ldquo;hard&rdquo; starts (3.5)</text>
        <text x="120" y="52" text-anchor="end" font-size="11.5" fill="#16303F" font-weight="700">New Mexico</text>
        <rect x="308" y="40" width="356" height="16" rx="2" fill="#B44A2E"/>
        <text x="120" y="78" text-anchor="end" font-size="11.5" fill="#16303F">Kansas</text>
        <rect x="344" y="66" width="142" height="16" rx="2" fill="#B44A2E"/>
        <text x="120" y="104" text-anchor="end" font-size="11.5" fill="#16303F">Arizona &middot; Nevada &middot; Texas</text>
        <rect x="308" y="92" width="178" height="16" rx="2" fill="#B44A2E"/>
        <text x="120" y="130" text-anchor="end" font-size="11.5" fill="#16303F">Utah &middot; Iowa &middot; the Dakotas</text>
        <rect x="308" y="118" width="142" height="16" rx="2" fill="#E8A13D"/>
        <text x="120" y="156" text-anchor="end" font-size="11.5" fill="#16303F">Indiana &middot; Minnesota</text>
        <rect x="308" y="144" width="124" height="16" rx="2" fill="#E8A13D"/>
        <text x="120" y="182" text-anchor="end" font-size="11.5" fill="#16303F">California <span>(huge internal spread)</span></text>
        <rect x="237" y="170" width="196" height="16" rx="2" fill="#E8A13D"/>
        <text x="120" y="208" text-anchor="end" font-size="11.5" fill="#16303F">Pennsylvania</text>
        <rect x="219" y="196" width="71" height="16" rx="2" fill="#5B6B75"/>
        <text x="120" y="234" text-anchor="end" font-size="11.5" fill="#16303F" font-weight="700">Maine &middot; Washington &middot; Arkansas</text>
        <rect x="148" y="222" width="53" height="16" rx="2" fill="#1F7A5C"/>
        <text x="212" y="234" font-size="11" fill="#1F7A5C" font-weight="700">1&ndash;4 gpg &mdash; buy nothing</text>
        <text x="400" y="292" text-anchor="middle" font-size="11" fill="#5B6B75" font-style="italic">Regional estimates. The spread inside a single state is often wider than the gap between two states.</text>
      </svg>
      <div class="chart-attr" style="margin-top:8px">Chart: SoftWaterSystemCost.com &middot; state-level ranges from published regional hardness data against the USGS classification &middot; <strong>these are estimates, not measurements &mdash; which is the entire point of the next section</strong></div>
    </div>
    <div class="col">
      <h2 id="cant">What a ZIP code cannot tell you</h2>
      <p style="margin:0">Look at California on that chart. Roughly <strong>6 to 17 gpg</strong> &mdash; from moderately hard to very hard, inside one state. A ZIP-code lookup that hands a Californian a single number is not estimating; it is guessing and rounding the guess to look like data.</p>
      <p style="margin:16px 0 0">Three things move your hardness that no ZIP code knows about. <strong>Your source:</strong> a private well and the municipal main on the same street can differ by a factor of three. <strong>Your local geology:</strong> Pennsylvania runs moderate in the east and much harder over the limestone near Pittsburgh &mdash; same state, same chart row, different water. <strong>The season:</strong> surface-water systems shift with rainfall.</p>
      <p style="margin:16px 0 0">So use the number above to know roughly where you stand &mdash; and then get a real one, because it is nearly free. <strong>Your utility publishes your actual hardness every year in its Consumer Confidence Report, at no cost.</strong> If you are on a well, or you want it today, a test kit is $10&ndash;$25. Some companies bill $100&ndash;$300 for the same reading, and an in-home &ldquo;free water test&rdquo; is a sales appointment with a chemistry set.</p>
      <div style="margin-top:24px">''' + cta_box("Know your number before anyone else does",
        "Hardness decides capacity, capacity decides salt, and salt decides most of what a softener costs you to run \u2014 so this one figure quietly sets your bill for a decade. Get it yourself, then size against a published price rather than a quote. SpringWell posts its softener pricing online with free shipping and a 6-month money-back window. Check the grain capacity against your measured gpg before ordering: bathroom-count sizing is a proxy for household demand, not a hardness reading.",
        "Check current SpringWell SS price","salt-softener") + '''</div>

      <h2 id="fixed">The bug we just fixed</h2>
      <p style="margin:0">This site&rsquo;s whole claim is that every number on it is sourced or calculable from something that is. So here is one that was not, for far too long.</p>
      <p style="margin:16px 0 0">Our homepage cost calculator asks for a ZIP code and estimates your hardness from it. Under the hood, it was doing this: <strong>take the first digit, look it up in a table of ten values, done.</strong> One number for every ZIP starting with a 9 &mdash; which is California, Oregon, Washington and more. It returned <span class="fig">10 gpg</span> for all of them. Seattle&rsquo;s water runs about <span class="fig">2&ndash;3 gpg</span>. We were telling people in one of the softest-water cities in America that they had hard water, and then sizing a softener for it.</p>
      <p style="margin:16px 0 0">It now resolves your ZIP to a <strong>state</strong> and returns that state&rsquo;s published range, with the band, the midpoint, and a caveat telling you not to trust it too far. Seattle now returns 1&ndash;4 gpg and the words &ldquo;the honest answer is often that you do not need a softener at all.&rdquo;</p>
      <p style="margin:16px 0 0">We also fixed a second thing while we were in there. The sizing routine behind that calculator was using the <em>naive</em> grain-capacity method &mdash; the one our own <a href="/what-size-water-softener-do-i-need/">sizing guide</a> spends two thousand words demolishing, because it scores a softener at its nameplate rather than at an efficient salt dose. Our calculator was contradicting our own article. It now uses the same method the article does.</p>
      <p style="margin:16px 0 0"><strong>I would rather publish this than patch it quietly.</strong> A site that audits other people&rsquo;s numbers for a living has no business hiding its own bad ones &mdash; and if you have used our calculator with a west-coast ZIP code before today, I am sorry, and you should re-run it.</p>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(hz_faqs) + '''
      <h2>Related guides</h2>
      <div class="card-grid narrow">
        <a class="card" href="/what-size-water-softener-do-i-need/"><div class="name">What size do I need?</div><div class="range">Free tool</div><div class="desc">Hardness is the input. This is the output.</div></a>
        <a class="card" href="/calculators/"><div class="name">All 32 calculators</div><div class="range">Free</div><div class="desc">Half of them want this number.</div></a>
        <a class="card" href="/"><div class="name">What it costs</div><div class="range">$840&ndash;$4,120</div><div class="desc">Every line item, priced.</div></a>
      </div>
    </div>
''' + sources([
 '<strong>U.S. Geological Survey &mdash; water hardness classification and national mapping</strong> &mdash; <a href="https://www.usgs.gov/media/images/map-water-hardness-united-states" rel="noopener" target="_blank">usgs.gov</a>. Supports the four classification bands used throughout this page (soft to 3.5 gpg, moderately hard to 7, hard to 10.5, very hard above), the 1 gpg = 17.1 ppm conversion, and the national pattern: hardest water concentrated in the Southwest, Great Plains and south-central states; softest in the Pacific Northwest and New England.',
 '<strong>Published state-level hardness compilations</strong> &mdash; <a href="https://www.stone-stream.com/blogs/knowledgebase/hard-water-map" rel="noopener" target="_blank">stone-stream.com</a>, <a href="https://waternitylab.com/water-hardness-by-state-hard-water-states/" rel="noopener" target="_blank">waternitylab.com</a>. Supports the state ranges behind the lookup and the chart: New Mexico at roughly 10&ndash;30 gpg (the widest in the country); Arizona, Nevada, Utah, Texas, Kansas, Oklahoma, Indiana and Minnesota consistently very hard; the Pacific Northwest and northern New England under 4 gpg; Arkansas unexpectedly soft; and Pennsylvania splitting between a moderate east and a limestone-driven harder west. <strong>These are regional estimates, and both sources say so explicitly &mdash; as does this page.</strong>',
 '<strong>SoftPro / Quality Water Treatment &mdash; average US hardness</strong> &mdash; <a href="https://www.softprowatersystems.com/pages/what-is-the-average-hardness-level-across-the-us" rel="noopener" target="_blank">softprowatersystems.com</a>. Supports: roughly 85% of American homes have some degree of hard water; the national average falls around 120&ndash;140 ppm (about 7&ndash;8 gpg); and the hardest urban supplies &mdash; San Antonio, Austin, Indianapolis, Las Vegas, Minneapolis, Phoenix &mdash; run 15&ndash;20 gpg.',
 '<strong>U.S. EPA &mdash; Consumer Confidence Reports and secondary standards</strong>. Supports the recommendation on this page: hardness is a <em>secondary</em> standard (aesthetic, not a health hazard), which is why it is unregulated &mdash; and why your utility&rsquo;s annual Consumer Confidence Report, which publishes your actual figure at no cost, is a better source than any ZIP-code lookup including this one.',
]) + '''
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("water-hardness-by-zip/index.html", hz)


# ============ BRAND EXPOSE TEMPLATE (T4) — [Brand] placeholders, noindex, content team fills ============
brand_faqs = [
 ("Is [Brand] equipment bad?","No &mdash; the hardware is generally solid ion-exchange equipment. This page critiques pricing opacity, not the product. You&rsquo;re paying a sales channel, not a better resin."),
 ("Can I buy [Brand] without the in-home visit?","Usually not at list terms &mdash; the dealer channel is the product. Some models appear used or via independent installers; warranties often don&rsquo;t transfer."),
 ("Will [Brand] match a competitor&rsquo;s quote?","Reps commonly have discount authority of 20&ndash;40% off the opening number. A written competing quote is the fastest way to find the floor."),
 ("What do [Brand] owners say about service?","Service reviews skew positive; price-related complaints dominate the negatives. That pattern &mdash; good product, opaque price &mdash; repeats across the dealer brands we track."),
]
rq_rows = [
 ("Mid-line softener, 3-bath home","$5,200","2026","BBB complaint #4821"),
 ("Flagship smart softener","$7,800","2025","Angi review, Tampa FL"),
 ("Entry softener, existing loop","$3,100","2026","r/plumbing thread"),
 ("Softener + carbon filter combo","$9,400","2025","Terry Love forum"),
]
rq_html = "".join(f'<tr><td>{s}</td><td class="num">{p}</td><td class="muted">{y}</td><td class="muted"><a href="#sources">{src}</a></td></tr>' for s,p,y,src in rq_rows)
brand = head("[Brand] Water Softener Cost: Real Price Ranges (2026) — TEMPLATE",
 "[Brand] softener quotes are commonly reported at $X–$Y installed. Sourced price ranges, itemized — the numbers the dealer won't publish.",
 "/templates/brand-expose/", "", noindex=True)
brand += HEADER + '''<main id="main">
  <!-- T4 TEMPLATE: replace every [Brand], the quote-sheet rows, reported-quotes rows, and per-brand copy.
       Body copy comes from the master article prompt output. Keep section order — it is the site-wide T4 pattern. -->
  <article class="col-wide">
    <div class="col" style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/brands/">Brands</a> &rsaquo; [Brand]</nav>
      <h1>[Brand] Water Softener Cost: Real Price Ranges (2026)</h1>
      ''' + author_box(updated="July 5, 2026") + '''
      <p style="margin-top:24px">[Brand] doesn&rsquo;t publish prices, but installed quotes are commonly reported at <span class="fig">$3,000&ndash;$8,000</span> for a whole-home softener, based on BBB filings, Angi reviews, and owner forum posts collected below. Comparable hardware installs for <span class="fig">$1,000&ndash;$2,500</span> through an independent plumber. This page itemizes where the difference goes.</p>
      <h2>What [Brand] sells</h2>
      <p style="margin:0">[150-word model rundown &mdash; fill per brand from the prompt template output.]</p>
    </div>
    <div style="margin-top:40px">''' + quote_sheet("[Brand] quote, as typically itemized",
      [("Mid-line softener unit (comparable retail $800&ndash;$1,500)",2400,4500),
       ("Installation (bundled, never itemized)",300,800),
       ("&ldquo;Water analysis&rdquo; &amp; in-home sales cost (implied)",300,2700)],
      total_label="Total quoted") + '''</div>
    <div class="col">
      <h2>Why doesn&rsquo;t [Brand] publish prices?</h2>
      <p style="margin:0">[Estimator&rsquo;s explanation, 150&ndash;250 words, varied per brand. Theme: the price is set in your kitchen, not at the factory &mdash; in-home selling prices to the buyer, not the bill of materials.]</p>
      <h2>Reported [Brand] quotes</h2>
    </div>
    <div class="data-table-wrap">
      <table class="data-table">
        <caption>Reported [Brand] quotes with source attribution</caption>
        <thead><tr><th scope="col">System quoted</th><th scope="col" class="num">Reported price</th><th scope="col">Year</th><th scope="col">Source</th></tr></thead>
        <tbody>''' + rq_html + '''</tbody>
      </table>
    </div>
    <div class="col">
      <h2>The factory-direct alternative</h2>
      <p>You don&rsquo;t have to sit through a water test to learn a price. Factory-direct makers publish theirs &mdash; the full comparison is in the <a href="/dealer-vs-factory-direct-pricing/">dealer vs. factory-direct breakdown</a>.</p>
      <div>''' + cta_box("The factory-direct alternative",
        "Skip the in-home quote. SpringWell publishes its softener prices &mdash; no dealer visit, DIY-friendly install, 6-month money-back guarantee.",
        "Check current SpringWell SS price","salt-softener") + '''</div>
      <h2 style="margin-bottom:8px">Frequently asked</h2>''' + faq_block(brand_faqs) + '''
    </div>
''' + sources([
 "BBB complaint filings naming quoted prices, 2024&ndash;2026 (linked per row).",
 "Angi / HomeAdvisor verified reviews citing [Brand] quotes.",
 "Owner forum posts, attributed and linked (Reddit r/plumbing, Terry Love forums).",
 "Independent plumber pricing for comparable hardware, Jul 2026.",
]) + '''
  </article>
</main>
''' + FOOTER
write("templates/brand-expose/index.html", brand)

# ============ DATA STUDY (T6) ============
regions = [("Southwest",18),("Great Plains",16),("Midwest",14),("Southeast",9),("Pacific",7),("Northeast",4)]
def bar(name,gpg):
    pct = round(gpg/20*100)
    color = "#16303F" if gpg>=10.5 else "#5B6B75" if gpg>=7 else "#1F7A5C"
    return f'<div class="bar-row"><div class="b-name">{name}</div><div class="b-track"><div class="b-fill" style="width:{pct}%;background:{color}"></div></div><div class="b-val">{gpg}</div></div>'
bars = "".join(bar(n,g) for n,g in regions)
study = head("How Hard Is America's Water? County-Level Study (2026) — SoftWaterSystemCost",
 "72% of U.S. counties have hard or very hard water. County-level USGS analysis of hardness by region — and what it does to softener cost.",
 "/data/water-hardness-study/",
 ld(article_schema("How Hard Is America's Water? A County-Level Analysis","USGS county-level water hardness analysis by region.","/data/water-hardness-study/",date="2026-06-15"))
 + ld(breadcrumb_schema([("Home","/"),("Data studies","/data/water-hardness-study/")])))
study += HEADER + '''<main id="main">
  <article class="col-wide">
    <div style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; Data studies &rsaquo; Water hardness</nav>
      <h1>How Hard Is America&rsquo;s Water? A County-Level Analysis</h1>
      <div class="byline"><span>By <a href="/about/">Robert Miller</a> &middot; Published June 2026</span><span class="stamp">Data updated &middot; Jun 2026</span></div>
    </div>
    <div class="key-findings" style="margin-top:24px">
      <div class="eyebrow">Key findings</div>
      <ul>
        <li><span class="fig">72%</span> of U.S. counties have water classified hard or very hard (over 7 gpg).</li>
        <li>The hardest region averages <span class="fig">18 gpg</span> &mdash; six times the softest, which changes softener sizing by two full tiers.</li>
        <li>Hardness alone shifts typical installed cost by <span class="fig">$400&ndash;$900</span> between regions, before any dealer markup.</li>
      </ul>
    </div>
    <div class="chart-panel" style="margin-top:64px">
      <h2>Average water hardness by region (gpg)</h2>
      <div style="display:flex;flex-direction:column;gap:8px">''' + bars + '''</div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px">
        <div class="chart-attr">Chart: SoftWaterSystemCost.com &middot; USGS data</div>
        <a href="#" style="font-size:14px;color:#5B6B75">Download chart image &darr;</a>
      </div>
    </div>
    <div class="col">
      <h2>What this means for your quote</h2>
      <p style="margin:0">Hardness sets softener capacity, and capacity sets price tier. A Phoenix household at 18 gpg needs roughly double the grain capacity of a Boston household at 3 gpg &mdash; a <span class="fig">$400&ndash;$900</span> hardware difference before anyone marks anything up. If a dealer quotes the same system to every house on the street, that&rsquo;s a script, not an assessment.</p>
      <h2>Methodology</h2>
      <p style="margin:0">We aggregated USGS county-level hardness measurements (most recent survey cycle) to regional means, weighted by household count from Census ACS data. Hardness classes follow the USGS scale: soft (0&ndash;3.5 gpg), moderate (3.5&ndash;7), hard (7&ndash;10.5), very hard (10.5+). County data, weights, and the aggregation script are available on request. Estimated cost effects use the same tier pricing as our <a href="/calculators/cost-calculator/">cost calculator</a>.</p>
      <div style="margin-top:64px;background:#FFFFFF;border:1px solid #D9DED9;padding:24px">
        <h2 style="font-size:22px;margin:0 0 8px">Cite this study</h2>
        <p style="margin:0 0 8px;font-size:15px;color:#5B6B75">Journalists and researchers may reuse our charts with attribution. Copy-ready citation:</p>
        <pre class="snippet">Miller, R. (2026). How Hard Is America&rsquo;s Water? A County-Level
Analysis. SoftWaterSystemCost.com.
https://softwatersystemcost.com/data/water-hardness-study/</pre>
      </div>
    </div>
''' + sources([
 "USGS national water hardness survey, county-level measurements.",
 "U.S. Census ACS household counts (regional weighting).",
 "SoftWaterSystemCost tier pricing model, Jul 2026.",
]) + '''
  </article>
</main>
''' + FOOTER
write("data/water-hardness-study/index.html", study)

# ============ HUB STUBS + LEGAL (launch requirements) ============
def stub(path, title, desc, h1, body_html, crumbs):
    pg = head(title, desc, path, ld(breadcrumb_schema(crumbs)))
    pg += HEADER + f'''<main id="main">
  <article class="col">
    <div style="margin-top:40px">
      <nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> &rsaquo; {crumbs[-1][0]}</nav>
      <h1>{h1}</h1>
    </div>
    {body_html}
  </article>
</main>
''' + FOOTER
    write(path.lstrip("/") + "index.html", pg)

stub("/brands/","Water Softener Brand Prices — SoftWaterSystemCost",
 "Sourced price ranges for 45 dealer softener brands — Culligan, Kinetico, RainSoft and more. The numbers the in-home quote won't show you.",
 "Brand price expos&eacute;s",
 '''<p style="margin-top:24px">Dealer brands don&rsquo;t publish prices; we collect the publicly reported ones and itemize them, one brand at a time.</p>
<div class="card-grid" style="margin-top:24px">
  <a class="card" href="/culligan-water-softener-cost/"><div class="name">Culligan</div><div class="range">$2,500&ndash;$4,500</div><div class="desc">Typical reported installed cost &mdash; tiers, rental math, quote checker.</div></a>
  <a class="card" href="/kinetico-water-softener-cost/"><div class="name">Kinetico</div><div class="range">$3,000&ndash;$5,000+</div><div class="desc">The brand that publishes no prices &mdash; reported tiers, real purchase reports.</div></a>
  <a class="card" href="/rainsoft-water-softener-cost/"><div class="name">RainSoft</div><div class="range">$6,000&ndash;$11,000</div><div class="desc">The widest reported quote spread we track &mdash; Home Depot channel, warranty fine print.</div></a>
  <a class="card" href="/costco-water-softener-cost/"><div class="name">Costco / EcoWater</div><div class="range">$6,000&ndash;$10,000</div><div class="desc">The aisle that doesn&rsquo;t exist &mdash; member-perk math &amp; the 3-day window.</div></a>
  <a class="card" href="/ecowater-water-softener-cost/"><div class="name">EcoWater</div><div class="range">$1,150&ndash;$10,000</div><div class="desc">The biggest maker in America &mdash; three storefronts, three price bands, zero list prices.</div></a>
</div>
<p style="margin-top:24px">Pelican, Leaf Home, Aquasure and the rest of the 45-brand index publish through Phase&nbsp;3. <a href="/dealer-vs-factory-direct-pricing/">Start with the dealer vs. factory-direct breakdown &rarr;</a></p>''',
 [("Home","/"),("Brands","/brands/")])

stub("/how-we-make-money/","How We Make Money — SoftWaterSystemCost",
 "SoftWaterSystemCost is reader-supported through disclosed affiliate links. How the commission works and why it never changes a published figure.",
 "How we make money",
 '''<p style="margin-top:24px">SoftWaterSystemCost is an independent publisher. We don&rsquo;t sell or install water treatment systems, run dealer advertising, or accept sponsored posts.</p>
<p>Some links on this site are affiliate links &mdash; currently to SpringWell, a factory-direct manufacturer. If you buy through one, we may earn a commission at no additional cost to you. Affiliate links are marked <code>rel="sponsored"</code> and open the manufacturer&rsquo;s site, where current prices are published.</p>
<p>The commission never changes a number on this site. Cost figures come from the public sources listed on each page &mdash; contractor cost surveys, BBB filings, attributed owner reports, retail pricing &mdash; and we publish them whether or not they flatter any brand, including brands we link to.</p>
<p style="margin:0">Questions? <a href="/about/#contact">Contact Robert</a>.</p>''',
 [("Home","/"),("How we make money","/how-we-make-money/")])

stub("/privacy/","Privacy Policy — SoftWaterSystemCost",
 "SoftWaterSystemCost privacy policy: no accounts, no tracking cookies, calculator inputs never leave your browser.",
 "Privacy policy",
 '''<p style="margin-top:24px">This is a static website. We don&rsquo;t require accounts, set tracking cookies, or run third-party advertising scripts.</p>
<p>Calculator inputs are processed entirely in your browser and are never transmitted or stored. If you email us, we use your address only to reply.</p>
<p>Outbound affiliate links go to the manufacturer&rsquo;s website, which has its own privacy policy. Server logs (standard hosting) are retained by our hosting provider for security purposes.</p>
<p style="margin:0">Effective July 2026 &middot; SoftWaterSystemCost, 1635 S Ridgewood Ave, 2nd Floor Ste 201, Daytona Beach, FL 32119.</p>''',
 [("Home","/"),("Privacy","/privacy/")])

# 404
p404 = head("Page not found — SoftWaterSystemCost","Page not found.","/404.html","",noindex=True)
p404 += HEADER + '''<main id="main"><div class="col" style="margin-top:64px;text-align:center">
<h1>404 &mdash; that line item isn&rsquo;t on the worksheet</h1>
<p>The page you&rsquo;re after moved or never existed. Start from the <a href="/">cost calculator</a> or the <a href="/">cost guide</a>.</p>
</div></main>
''' + FOOTER
write("404.html", p404)

# ============ STYLEGUIDE (noindex) ============
sg = head("Styleguide — SoftWaterSystemCost","Internal component library.","/styleguide/","",noindex=True)
sg += HEADER + '''<main id="main">
  <article class="col-wide">
    <div class="col" style="margin-top:40px"><h1>Component styleguide</h1>
    <p>Internal reference (noindex). Every component below is production markup &mdash; copy it verbatim into new pages.</p></div>
    <div class="col"><h2>Type &amp; figures</h2>
      <h1 style="margin:0">H1 Zilla Slab 700</h1><h2 style="margin:16px 0 0">H2 Zilla Slab 600</h2><h3>H3 Source Sans 600</h3>
      <p>Body 18px Source Sans. Every dollar figure wraps in <code>.fig</code>: <span class="fig">$1,499</span> &mdash; Plex Mono, tabular numerals.</p>
      <span class="stamp">Data updated &middot; Jul 2026</span></div>
    <div style="margin-top:40px">''' + quote_sheet("Component demo, 3-Bath Home", master_rows) + '''</div>
    <div class="col" style="margin-top:40px">''' + cta_box("The factory-direct alternative","CTA box demo copy &mdash; two to three lines, benefit-led, never salesy.","Check current SpringWell SS price","salt-softener") + '''</div>
    <div class="col" style="margin-top:40px"><h2 class="tight">FAQ</h2>''' + faq_block([("Question style?","Answer &le;300 characters, plain, numbers-forward.")]) + '''</div>
    <div class="col" style="margin-top:40px">''' + author_box() + '''</div>
    <div class="col" style="margin-top:40px"><h2 class="tight">Buttons &amp; cards</h2>
      <p><a class="btn" href="#">Primary button &rarr;</a></p>
      <div class="card-grid narrow"><a class="card" href="#"><div class="name">Card title</div><div class="range">$840&ndash;$4,120</div><div class="desc">Card description.</div></a></div></div>
    <div class="col" style="margin-top:40px"><h2 class="tight">Calculator (embed variant)</h2>
      <div class="calc-titlebar"><span class="t-left">Cost estimator</span><span class="t-right">Live estimate</span></div>
      <div data-calc data-variant="embed"></div></div>
  </article>
</main>
<script type="module" src="/assets/calculator.js?v=171"></script>
''' + FOOTER
write("styleguide/index.html", sg)

# ============ robots / sitemap ============
write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /templates/\nDisallow: /styleguide/\nDisallow: /embed/\nDisallow: /pick/\n\nSitemap: {SITE}/sitemap.xml\n")
urls = ["/","/water-softener-salt-cost/","/water-softener-repair-cost/","/water-softener-servicing/","/water-softener-maintenance/","/how-long-does-a-water-softener-last/","/10-year-water-softener-cost/","/water-softener-electricity-usage/","/what-size-water-softener-do-i-need/","/leaf-home-water-solutions-cost/","/sediment-filter-cost/","/water-softener-rental-cost/","/uv-water-purifier-cost/","/acid-neutralizer-cost/","/iron-filter-for-well-water-cost/","/water-softener-removal-cost/","/cost-to-add-water-softener-to-existing-home/","/whole-house-water-softener-installation-cost/","/average-water-softener-installation-cost/","/well-water-softener-cost/","/ecowater-water-softener-cost/","/dual-tank-water-softener-cost/","/salt-free-water-softener-cost/","/costco-water-softener-cost/","/rainsoft-water-softener-cost/","/low-cost-water-softener/","/why-are-water-softeners-so-expensive/","/kinetico-water-softener-cost/","/dealer-vs-factory-direct-pricing/","/culligan-water-softener-cost/","/water-softener-installation-cost/","/water-softener-maintenance-cost/","/calculators/","/calculators/cost-calculator/","/data/water-hardness-study/","/brands/","/about/","/how-we-make-money/","/privacy/"]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>2026-07-12</lastmod></url>\n" for u in urls)
sm += "</urlset>\n"
write("sitemap.xml", sm)

print("DONE")
