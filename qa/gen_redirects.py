#!/usr/bin/env python3
"""Regenerate the /pick/ redirects block in vercel.json from pick-links.json.
pick-links.json is the SINGLE SOURCE OF TRUTH for affiliate destinations.
Run after any change to pick-links.json, commit both files."""
import json
links = json.load(open('pick-links.json'))
v = json.load(open('vercel.json'))
v['redirects'] = [
    {"source": f"/pick/{slug}", "destination": d["url"], "permanent": False}
    for slug, d in sorted(links.items())
]
json.dump(v, open('vercel.json', 'w'), indent=2)
print(f"vercel.json: {len(v['redirects'])} /pick/ redirects written")
