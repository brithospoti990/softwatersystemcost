// everflow-config.js — SINGLE SOURCE OF TRUTH for affiliate URLs (spec §8.4)
// Every outbound SpringWell link is built from here. Never hand-write an
// affiliate URL in a template. rel="sponsored nofollow noopener" target="_blank".

export const AFFID = 'REPLACE_AFFID';
const BASE = 'https://www.tkqlhce.example/click'; // placeholder Everflow tracking domain

/** oid map — one entry per product path */
export const OIDS = {
  ss1: 'oid-ss1-softener',        // SpringWell SS1 (1–3 bath)
  ss4: 'oid-ss4-softener',        // SpringWell SS4 (4–6 bath)
  futuresoft: 'oid-futuresoft',   // salt-free FutureSoft
  combo: 'oid-css-combo',         // whole-house combo
};

export function affiliateUrl(product) {
  const oid = OIDS[product] || OIDS.ss1;
  return BASE + '?affid=' + AFFID + '&oid=' + oid;
}

export const REL = 'sponsored nofollow noopener';
