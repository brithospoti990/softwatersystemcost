#!/usr/bin/env python3
"""Regenerate the /pick/ redirects block in vercel.json from pick-links.json.
pick-links.json is the SINGLE SOURCE OF TRUTH for affiliate destinations.
Run after any change to pick-links.json, commit both files."""
import json
links = json.load(open('pick-links.json'))
v = json.load(open('vercel.json'))
keep = [r for r in v.get('redirects', []) if not r['source'].startswith('/pick/')]
pick = []
for slug, d in sorted(links.items()):
    # both forms: trailingSlash:true normalizes /pick/x -> /pick/x/, so the
    # slashed source is the one that actually matches after normalization
    pick.append({"source": f"/pick/{slug}", "destination": d["url"], "permanent": False})
    pick.append({"source": f"/pick/{slug}/", "destination": d["url"], "permanent": False})
v['redirects'] = keep + pick
json.dump(v, open('vercel.json', 'w'), indent=2)
print(f"vercel.json: {len(v['redirects'])} /pick/ redirects written")
