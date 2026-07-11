// calc-core.js — shared calculator utilities (vanilla ES module, no deps)
// softwatersystemcost.com · spec §4.5 · production v1.0

export function reducedMotion() {
  return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/** "$1,240" — always whole dollars */
export function fmt(n) {
  return '$' + Math.round(n).toLocaleString('en-US');
}

/** "$1,240 – $2,180" */
export function fmtRange(low, high) {
  return fmt(low) + ' \u2013 ' + fmt(high);
}

/** 200ms count-up on the FINAL figure only (spec §2.4). Instant under
    prefers-reduced-motion. Returns a cancel function. */
export function countUp(fromLow, fromHigh, toLow, toHigh, render) {
  if (reducedMotion()) { render(fmtRange(toLow, toHigh)); return () => {}; }
  const t0 = performance.now(), DUR = 200;
  let raf;
  const tick = (t) => {
    const p = Math.min(1, (t - t0) / DUR);
    const e = 1 - Math.pow(1 - p, 2); // ease-out
    render(fmtRange(fromLow + (toLow - fromLow) * e, fromHigh + (toHigh - fromHigh) * e));
    if (p < 1) raf = requestAnimationFrame(tick);
  };
  raf = requestAnimationFrame(tick);
  return () => cancelAnimationFrame(raf);
}

/** ZIP → average grains-per-gallon hardness.
    Production: replace ZIP_GPG with the generated /assets/data/zip-hardness.json
    (USGS county data → ZIP3 prefix). Stub keys on first digit until then. */
const ZIP_GPG = { 0: 6, 1: 7, 2: 8, 3: 11, 4: 12, 5: 14, 6: 18, 7: 16, 8: 17, 9: 10 };
export function hardnessForZip(zip) {
  const z = String(zip || '').trim();
  if (!/^[0-9]{5}$/.test(z)) return null;
  return ZIP_GPG[+z[0]] ?? null;
}

/** Softener sizing: people × 75 gal/day × gpg × 7 days reserve → grain tier */
export function grainTier(people, gpg) {
  const weekly = people * 75 * gpg * 7;
  if (weekly <= 21000) return 24;
  if (weekly <= 28000) return 32;
  if (weekly <= 42000) return 48;
  return 64;
}

/** Cost model — returns { rows: [{item, low, high}], low, high }.
    opts: { people, gpg, type:'salt'|'saltfree', install:'pro'|'diy', hasLoop:bool }
    Figures: 2026 retail survey tiers + Angi/HomeAdvisor labor data (see /data sources). */
export function estimate(opts) {
  const rows = [];
  const { people, gpg, type, install, hasLoop } = opts;
  if (type === 'saltfree') {
    const size = people <= 3 ? [800, 1800] : [1200, 2800];
    rows.push({ item: 'Salt-free conditioner (' + (people <= 3 ? 'standard' : 'high-flow') + ')', low: size[0], high: size[1] });
  } else {
    const tier = grainTier(people, gpg);
    const unit = { 24: [500, 1100], 32: [600, 1500], 48: [800, 1900], 64: [1000, 2400] }[tier];
    rows.push({ item: 'Softener unit (' + tier + 'k grain)', low: unit[0], high: unit[1] });
  }
  if (install === 'pro') {
    rows.push({ item: 'Installation labor', low: 200, high: 500 });
    rows.push({ item: 'Bypass valve & fittings', low: 40, high: 120 });
  } else {
    rows.push({ item: 'Fittings & supplies (DIY)', low: 50, high: 150 });
  }
  if (!hasLoop) rows.push({ item: 'Loop run (if none exists)', low: 600, high: 2000 });
  if (type === 'salt') rows.push({ item: 'First year of salt', low: 60, high: 180 });
  const low = rows.reduce((s, r) => s + r.low, 0);
  const high = rows.reduce((s, r) => s + r.high, 0);
  return { rows, low, high };
}
