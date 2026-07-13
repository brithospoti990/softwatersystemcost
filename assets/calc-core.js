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
/* ZIP3 -> state (standard USPS prefix allocations) */
const ZIP3_STATE = [[10,27,'MA'],[28,29,'RI'],[30,38,'NH'],[39,49,'ME'],[50,59,'VT'],[60,69,'CT'],[70,89,'NJ'],[100,149,'NY'],[150,196,'PA'],[197,199,'DE'],[200,205,'DC'],[206,219,'MD'],[220,246,'VA'],[247,268,'WV'],[270,289,'NC'],[290,299,'SC'],[300,319,'GA'],[320,349,'FL'],[350,369,'AL'],[370,385,'TN'],[386,397,'MS'],[398,399,'GA'],[400,427,'KY'],[430,459,'OH'],[460,479,'IN'],[480,499,'MI'],[500,528,'IA'],[530,549,'WI'],[550,567,'MN'],[570,577,'SD'],[580,588,'ND'],[590,599,'MT'],[600,629,'IL'],[630,658,'MO'],[660,679,'KS'],[680,693,'NE'],[700,714,'LA'],[716,729,'AR'],[730,749,'OK'],[750,799,'TX'],[800,816,'CO'],[820,831,'WY'],[832,838,'ID'],[840,847,'UT'],[850,865,'AZ'],[870,884,'NM'],[889,898,'NV'],[900,961,'CA'],[967,968,'HI'],[970,979,'OR'],[980,994,'WA'],[995,999,'AK']];

/* State hardness ranges in gpg. Regional estimates from published state-level
   hardness data (USGS classification bands). NOT a measurement of your tap. */
const STATE_GPG = {ME:[1,3],NH:[1,3],VT:[2,4],MA:[2,4],RI:[2,4],CT:[3,6],NY:[3,6],NJ:[4,7],PA:[5,9],DE:[4,7],MD:[4,8],DC:[5,8],VA:[4,8],WV:[4,8],NC:[2,5],SC:[2,5],GA:[2,5],FL:[7,13],AL:[3,7],MS:[4,8],TN:[4,8],KY:[6,11],OH:[6,11],MI:[7,12],IN:[10,17],IL:[8,14],WI:[8,15],MN:[10,17],IA:[10,18],MO:[8,14],ND:[10,18],SD:[10,18],NE:[10,18],KS:[12,20],OK:[10,17],TX:[10,20],LA:[4,9],AR:[1,4],CO:[7,14],WY:[8,15],MT:[6,12],ID:[6,12],UT:[10,18],AZ:[10,20],NV:[10,20],NM:[10,30],CA:[6,17],OR:[1,4],WA:[1,4],AK:[1,5],HI:[2,6]};

export function stateForZip(zip) {
  const z = String(zip || '').trim();
  if (!/^[0-9]{5}$/.test(z)) return null;
  const p = +z.slice(0, 3);
  for (const [lo, hi, st] of ZIP3_STATE) if (p >= lo && p <= hi) return st;
  return null;
}

/** Full detail: state, gpg range, midpoint, USGS band. Regional estimate only. */
export function hardnessDetailForZip(zip) {
  const st = stateForZip(zip);
  if (!st || !STATE_GPG[st]) return null;
  const [lo, hi] = STATE_GPG[st];
  const mid = Math.round(((lo + hi) / 2) * 10) / 10;
  const band = mid <= 3.5 ? 'soft' : mid <= 7 ? 'moderately hard' : mid <= 10.5 ? 'hard' : 'very hard';
  return { state: st, lo, hi, mid, band };
}
export function hardnessForZip(zip) {
  const d = hardnessDetailForZip(zip);
  return d ? d.mid : null;
}

/** Softener sizing: capacity scored at an EFFICIENT salt dose (65% of nameplate),
 *  not at the nameplate — see /what-size-water-softener-do-i-need/ */
export function grainTier(people, gpg) {
  const weekly = people * 75 * gpg * 7;
  const EFF = 0.65;
  for (const t of [24, 32, 40, 48, 64, 80]) if (t * 1000 * EFF >= weekly) return t;
  return 80;
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
    const unit = { 24: [500, 1100], 32: [600, 1500], 40: [700, 1700], 48: [800, 1900], 64: [1000, 2400], 80: [1200, 2900] }[tier];
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
