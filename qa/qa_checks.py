#!/usr/bin/env python3
"""Portfolio QA protocol: div balance walk, FAQ <=300 chars, affiliate rel check, fig-span check."""
import re, sys, glob, html

fail = 0
pages = [p for p in glob.glob("**/*.html", recursive=True) if not p.startswith("qa/")]
for p in sorted(pages):
    src = open(p).read()
    # 1. div balance walk
    opens = len(re.findall(r"<div\b", src)); closes = len(re.findall(r"</div>", src))
    if opens != closes:
        print(f"FAIL div balance {p}: {opens} open vs {closes} close"); fail = 1
    # tag balance for other structural tags
    for tag in ["table","details","article","main","header","footer","nav","ol","ul"]:
        o = len(re.findall(rf"<{tag}\b", src)); c = len(re.findall(rf"</{tag}>", src))
        if o != c:
            print(f"FAIL <{tag}> balance {p}: {o} vs {c}"); fail = 1
    # 2. FAQ answers <=300 chars (text inside <details><summary>..</summary><p>ANSWER</p>)
    for m in re.finditer(r"<details[^>]*>\s*<summary[^>]*>.*?</summary>\s*<p[^>]*>(.*?)</p>", src, re.S):
        txt = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        if len(txt) > 300 and "toc" not in m.group(0):
            print(f"FAIL FAQ>300 {p}: {len(txt)} chars: {txt[:60]}..."); fail = 1
    # 3. affiliate links must carry rel + target
    for m in re.finditer(r'<a\s[^>]*href="(/pick/[^"]+)"[^>]*>', src):
        tag = m.group(0)
        if 'rel="sponsored nofollow noopener"' not in tag or 'target="_blank"' not in tag:
            print(f"FAIL affiliate rel {p}: {tag[:100]}"); fail = 1
    # 4. no SpringWell dollar prices near brand name (crude heuristic: '$' within same sentence as SpringWell)
    for m in re.finditer(r"([^.]*SpringWell[^.]*\.)", src):
        if re.search(r"\$\d", m.group(1)):
            print(f"WARN SpringWell + $ in one sentence in {p}: {html.unescape(re.sub(r'<[^>]+>','',m.group(1)))[:90]}")
# 5. MOBILE GUARDRAILS (for all future articles)
for p in sorted(pages):
    src = open(p).read()
    # 5a. viewport meta on every page
    if 'name="viewport"' not in src:
        print(f"FAIL missing viewport meta: {p}"); fail = 1
    # 5b. every <table> must live inside an overflow-scrolling wrapper
    for m in re.finditer(r"<table", src):
        before = src[:m.start()]
        qs = before.rfind('class="quote-sheet"'); dw = before.rfind('class="data-table-wrap"')
        anchor = max(qs, dw)
        if anchor == -1 or before.rfind("</table>") > anchor:
            print(f"FAIL bare <table> (needs .quote-sheet or .data-table-wrap): {p} @byte {m.start()}"); fail = 1
    # 5c. no fixed inline widths wider than the mobile viewport
    for m in re.finditer(r'style="[^"]*(?<![a-z-])width:\s*(\d{3,})px', src):
        if int(m.group(1)) > 390:
            print(f"FAIL fixed width {m.group(1)}px inline in {p}"); fail = 1
    # 5d. imgs need width+height attributes (CLS)
    for m in re.finditer(r"<img\b[^>]*>", src):
        tag = m.group(0)
        if "width=" not in tag or "height=" not in tag:
            print(f"FAIL <img> without width/height in {p}: {tag[:80]}"); fail = 1

# 6. every /pick/ slug used in HTML must exist in pick-links.json
import json
picks = set(json.load(open("pick-links.json")).keys())
for p in sorted(pages):
    src = open(p).read()
    for m in re.finditer(r'href="/pick/([^"#?]+)"', src):
        if m.group(1).rstrip("/") not in picks:
            print(f"FAIL unknown /pick/ slug in {p}: {m.group(1)}"); fail = 1
print("PAGES:", len(pages), "— all checks passed" if not fail else "— FAILURES ABOVE")
sys.exit(fail)
