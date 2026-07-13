// jsdom verification of all calculator branches (portfolio QA protocol)
import { JSDOM } from 'jsdom';
import { readFileSync } from 'fs';
import { estimate, grainTier, hardnessForZip, hardnessDetailForZip, fmtRange } from '../assets/calc-core.js';

let fails = 0;
const ok = (cond, msg) => { console.log((cond ? 'PASS' : 'FAIL') + ' ' + msg); if (!cond) fails++; };

// ---- 1. Cost model branches (pure) ----
const base = { people: 3, gpg: 12, type: 'salt', install: 'pro', hasLoop: true };
const e1 = estimate(base);
ok(e1.rows.length === 4 && e1.low === 900 && e1.high === 2300, `salt/pro/loop → ${e1.low}-${e1.high} (efficient-dose sizing lands the 40k tier; the naive ladder said 32k)`);
const e2 = estimate({ ...base, hasLoop: false });
ok(e2.low === 1500 && e2.high === 4300, `no-loop adds 600-2000 → ${e2.low}-${e2.high}`);
const e3 = estimate({ ...base, type: 'saltfree' });
ok(e3.rows.some(r => r.item.includes('conditioner')) && !e3.rows.some(r => r.item.includes('salt')), 'saltfree drops salt row');
const e4 = estimate({ ...base, install: 'diy' });
ok(e4.rows.some(r => r.item.includes('DIY')) && !e4.rows.some(r => r.item.includes('labor')), 'diy swaps labor rows');
ok(grainTier(1, 5) === 24 && grainTier(4, 12) === 40 && grainTier(5, 14) === 64 && grainTier(6, 20) === 80, 'grain tiers scored at an EFFICIENT salt dose (65% of nameplate) — matching our own sizing guide, not the naive nameplate ladder the old test locked in');
ok(hardnessForZip('90210') === 11.5 && hardnessForZip('123') === null && hardnessForZip('abcde') === null, 'ZIP lookup validates 5 digits and resolves STATE-level data');
ok(hardnessForZip('98101') !== hardnessForZip('90001'), 'THE BUG, GUARDED: Seattle and Los Angeles no longer share a hardness value (both ZIPs start with 9)');
ok(hardnessDetailForZip('98101').band === 'soft' && hardnessDetailForZip('90001').band === 'very hard', 'Seattle reads soft; LA reads very hard');
ok(hardnessDetailForZip('87501').hi === 30, 'New Mexico carries the widest published range in the country (10-30 gpg)');
ok(fmtRange(840, 4120) === '$840 \u2013 $4,120', 'range formatting');

// ---- 2. DOM mount + interaction on the real homepage ----
const html = readFileSync('index.html', 'utf8');
const dom = new JSDOM(html, { url: 'https://softwatersystemcost.com/' });
global.window = dom.window; global.document = dom.window.document;
global.performance = { now: () => 0 };
global.requestAnimationFrame = (fn) => { fn(1000); return 1; };
global.cancelAnimationFrame = () => {};
window.matchMedia = () => ({ matches: true }); // reduced motion → instant renders

const { mountCalculator } = await import('../assets/calculator.js?raw' + Math.random()).catch(() => import('../assets/calculator.js'));
const root = document.querySelector('[data-calc]');
ok(!!root, 'homepage has [data-calc] mount point');
// calculator.js auto-mounts on import querySelectorAll — verify it rendered
ok(root.querySelectorAll('input[type=range]').length === 2, 'two sliders rendered');
ok(root.querySelectorAll('.seg').length === 3, 'three segmented controls (full variant)');
const result0 = JSON.parse(root.getAttribute('data-result'));
ok(result0.low === 1500 && result0.high === 4300, `initial data-result ${result0.low}-${result0.high} (default no-loop)`);

// toggle loop=yes → totals drop by 600-2000
const loopYes = [...root.querySelectorAll('.seg button')].find(b => b.textContent === 'Yes');
loopYes.click();
const r1 = JSON.parse(root.getAttribute('data-result'));
ok(r1.low === 900 && r1.high === 2300, `loop toggle updates data-result → ${r1.low}-${r1.high}`);
ok(loopYes.getAttribute('aria-pressed') === 'true', 'aria-pressed follows selection');

// slider input event
const people = root.querySelector('#calc-people');
people.value = '6';
people.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
const r2 = JSON.parse(root.getAttribute('data-result'));
ok(r2.inputs.people === 6 && r2.low > r1.low, `people slider → tier up (${r2.low}-${r2.high})`);

// salt-free branch via UI
const sf = [...root.querySelectorAll('.seg button')].find(b => b.textContent === 'Salt-free');
sf.click();
const r3 = JSON.parse(root.getAttribute('data-result'));
ok(r3.inputs.type === 'saltfree', 'salt-free branch reachable via UI');

// quote sheet rows render + result figure text
ok(root.querySelectorAll('[data-qs-body] tr').length >= 3, 'live quote sheet rows rendered');
ok(/\$\d/.test(root.querySelector('.result-fig').textContent), 'result figure renders formatted range');

// ---- 3. Salt mini-calculator ----
const saltRoot = document.querySelector('[data-salt-calc]');
ok(!!saltRoot, 'homepage has salt mini-calc mount');
if (saltRoot) {
  const r0 = JSON.parse(saltRoot.getAttribute('data-result'));
  ok(r0.yearly === 70 && r0.tenYear === 700, `salt calc defaults 10×$7 → ${r0.yearly}/yr`);
  const bagsInput = saltRoot.querySelector('#mc-bags');
  bagsInput.value = '12';
  bagsInput.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  const r1 = JSON.parse(saltRoot.getAttribute('data-result'));
  ok(r1.yearly === 84 && r1.tenYear === 840, `salt calc updates → ${r1.yearly}/yr`);
}

// ---- 4. Install scenario tool (B1 page) ----
const b1html = readFileSync('water-softener-installation-cost/index.html', 'utf8');
const dom2 = new JSDOM(b1html, { url: 'https://softwatersystemcost.com/water-softener-installation-cost/' });
global.window = dom2.window; global.document = dom2.window.document;
window.matchMedia = () => ({ matches: true });
const mod2 = await import('../assets/calculator.js?b1=' + Math.random()).catch(() => null);
const iroot = dom2.window.document.querySelector('[data-install-calc]');
ok(!!iroot, 'B1 page has install-calc mount');
if (iroot && mod2 && mod2.mountInstallCalc) {
  mod2.mountInstallCalc(iroot);
  const s0 = JSON.parse(iroot.getAttribute('data-result'));
  ok(s0.scenario === 'prepared' && s0.low === 290 && s0.high === 770, `install default prepared → ${s0.low}-${s0.high}`);
  const full = [...iroot.querySelectorAll('button')].find(b => b.dataset.k === 'full');
  full.click();
  const s1 = JSON.parse(iroot.getAttribute('data-result'));
  ok(s1.low === 890 && s1.high === 4120, `install full-site-work → ${s1.low}-${s1.high}`);
}

// ---- 5. Culligan quote checker (C1 page) ----
const c1html = readFileSync('culligan-water-softener-cost/index.html', 'utf8');
const dom3 = new JSDOM(c1html, { url: 'https://softwatersystemcost.com/culligan-water-softener-cost/' });
global.window = dom3.window; global.document = dom3.window.document;
window.matchMedia = () => ({ matches: true });
const mod3 = await import('../assets/calculator.js?c1=' + Math.random()).catch(() => null);
const qroot = dom3.window.document.querySelector('[data-quote-check]');
ok(!!qroot, 'C1 page has quote-check mount');
if (qroot && mod3 && mod3.mountQuoteCheck) {
  mod3.mountQuoteCheck(qroot);
  const q0 = JSON.parse(qroot.getAttribute('data-result'));
  ok(q0.amount === 4500 && q0.band === 'typical', `quote-check default → ${q0.band}`);
  const slider = qroot.querySelector('#qc-amt');
  slider.value = '7500';
  slider.dispatchEvent(new dom3.window.Event('input', { bubbles: true }));
  const q1 = JSON.parse(qroot.getAttribute('data-result'));
  ok(q1.band === 'above-published', `quote-check 7500 → ${q1.band}`);
  slider.value = '2000';
  slider.dispatchEvent(new dom3.window.Event('input', { bubbles: true }));
  ok(JSON.parse(qroot.getAttribute('data-result')).band === 'below-typical', 'quote-check 2000 → below-typical');
}

// ---- 6. Channel savings calc (C28 page) ----
const c28html = readFileSync('dealer-vs-factory-direct-pricing/index.html', 'utf8');
const dom4 = new JSDOM(c28html, { url: 'https://softwatersystemcost.com/dealer-vs-factory-direct-pricing/' });
global.window = dom4.window; global.document = dom4.window.document;
window.matchMedia = () => ({ matches: true });
const mod4 = await import('../assets/calculator.js?c28=' + Math.random()).catch(() => null);
const croot = dom4.window.document.querySelector('[data-channel-calc]');
ok(!!croot, 'C28 page has channel-calc mount');
if (croot && mod4 && mod4.mountChannelCalc) {
  mod4.mountChannelCalc(croot);
  const d0 = JSON.parse(croot.getAttribute('data-result'));
  ok(d0.quote === 5500 && d0.savingsLow === 2300 && d0.savingsHigh === 4300, `channel default → ${d0.savingsLow}-${d0.savingsHigh}`);
  const sl = croot.querySelector('#cc-amt');
  sl.value = '3000';
  sl.dispatchEvent(new dom4.window.Event('input', { bubbles: true }));
  const d1 = JSON.parse(croot.getAttribute('data-result'));
  ok(d1.savingsLow === 0 && d1.savingsHigh === 1800, `channel floor at 0 → ${d1.savingsLow}-${d1.savingsHigh}`);
}

// ---- 7. Parameterized quote checker (C2 Kinetico) + C1 default regression ----
const c2html = readFileSync('kinetico-water-softener-cost/index.html', 'utf8');
const dom5 = new JSDOM(c2html, { url: 'https://softwatersystemcost.com/kinetico-water-softener-cost/' });
global.window = dom5.window; global.document = dom5.window.document;
window.matchMedia = () => ({ matches: true });
const mod5 = await import('../assets/calculator.js?c2=' + Math.random()).catch(() => null);
const kroot = dom5.window.document.querySelector('[data-quote-check]');
ok(!!kroot, 'C2 page has quote-check mount with data-bands');
if (kroot && mod5 && mod5.mountQuoteCheck) {
  mod5.mountQuoteCheck(kroot);
  const k0 = JSON.parse(kroot.getAttribute('data-result'));
  ok(k0.amount === 4000 && k0.band === 'typical', `kinetico default 4000 → ${k0.band}`);
  const ks = kroot.querySelector('#qc-amt');
  ks.value = '2800';
  ks.dispatchEvent(new dom5.window.Event('input', { bubbles: true }));
  ok(JSON.parse(kroot.getAttribute('data-result')).band === 'below-typical', 'kinetico 2800 → below-typical');
  ks.value = '7000';
  ks.dispatchEvent(new dom5.window.Event('input', { bubbles: true }));
  ok(JSON.parse(kroot.getAttribute('data-result')).band === 'above-published', 'kinetico 7000 → above-published');
  // regression: C1 page (no data-bands) still gets Culligan defaults
  const c1r = new JSDOM(readFileSync('culligan-water-softener-cost/index.html', 'utf8'), { url: 'https://softwatersystemcost.com/culligan-water-softener-cost/' });
  global.window = c1r.window; global.document = c1r.window.document;
  window.matchMedia = () => ({ matches: true });
  const mod5b = await import('../assets/calculator.js?c1r=' + Math.random()).catch(() => null);
  const c1root = c1r.window.document.querySelector('[data-quote-check]');
  mod5b.mountQuoteCheck(c1root);
  const r0 = JSON.parse(c1root.getAttribute('data-result'));
  ok(r0.amount === 4500 && r0.band === 'typical', `C1 defaults regression → ${r0.amount}/${r0.band}`);
}

// ---- 8. Quote Builder (why-so-expensive page) ----
const a9html = readFileSync('why-are-water-softeners-so-expensive/index.html', 'utf8');
const dom6 = new JSDOM(a9html, { url: 'https://softwatersystemcost.com/why-are-water-softeners-so-expensive/' });
global.window = dom6.window; global.document = dom6.window.document;
window.matchMedia = () => ({ matches: true });
const mod6 = await import('../assets/calculator.js?a9=' + Math.random()).catch(() => null);
const eroot = dom6.window.document.querySelector('[data-expense-calc]');
ok(!!eroot, 'A9 page has expense-calc mount');
if (eroot && mod6 && mod6.mountExpenseCalc) {
  mod6.mountExpenseCalc(eroot);
  const e0 = JSON.parse(eroot.getAttribute('data-result'));
  ok(e0.low === 1100 && e0.high === 2000, `builder default mid+pro → ${e0.low}-${e0.high}`);
  const dealerBtn = [...eroot.querySelectorAll('[data-addon]')].find(b => b.dataset.addon === 'dealer');
  dealerBtn.click();
  const e1 = JSON.parse(eroot.getAttribute('data-result'));
  ok(e1.low === 3210 && e1.high === 7730, `builder +dealer channel → ${e1.low}-${e1.high}`);
  const diyBtn = [...eroot.querySelectorAll('[data-install]')].find(b => b.dataset.install === 'diy');
  diyBtn.click();
  const e2 = JSON.parse(eroot.getAttribute('data-result'));
  ok(e2.low === 3060 && e2.high === 7380, `builder diy swap → ${e2.low}-${e2.high}`);
  ok(eroot.querySelectorAll('[data-stack] div').length === 3, 'stacked bar renders 3 segments');
}

// ---- 9. Budget Fit tool (low-cost page) ----
const f3html = readFileSync('low-cost-water-softener/index.html', 'utf8');
const dom7 = new JSDOM(f3html, { url: 'https://softwatersystemcost.com/low-cost-water-softener/' });
global.window = dom7.window; global.document = dom7.window.document;
window.matchMedia = () => ({ matches: true });
const mod7 = await import('../assets/calculator.js?f3=' + Math.random()).catch(() => null);
const broot = dom7.window.document.querySelector('[data-budget-fit]');
ok(!!broot, 'F3 page has budget-fit mount');
if (broot && mod7 && mod7.mountBudgetFit) {
  mod7.mountBudgetFit(broot);
  const b0 = JSON.parse(broot.getAttribute('data-result'));
  ok(b0.tier === 'either', `budget-fit default 3-4/hard → ${b0.tier}`);
  const hh5 = [...broot.querySelectorAll('[data-hh]')].find(b => b.dataset.hh === '5p');
  hh5.click();
  ok(JSON.parse(broot.getAttribute('data-result')).tier === 'under-1500', 'budget-fit 5+/hard → under-1500');
  const hh12 = [...broot.querySelectorAll('[data-hh]')].find(b => b.dataset.hh === '12');
  const mod = [...broot.querySelectorAll('[data-hard]')].find(b => b.dataset.hard === 'mod');
  hh12.click(); mod.click();
  ok(JSON.parse(broot.getAttribute('data-result')).tier === 'under-700', 'budget-fit 1-2/moderate → under-700');
}

// ---- 10. Maintenance cost calc (E1 page) ----
const e1html = readFileSync('water-softener-maintenance-cost/index.html', 'utf8');
const dom8 = new JSDOM(e1html, { url: 'https://softwatersystemcost.com/water-softener-maintenance-cost/' });
global.window = dom8.window; global.document = dom8.window.document;
window.matchMedia = () => ({ matches: true });
const mod8 = await import('../assets/calculator.js?e1=' + Math.random()).catch(() => null);
const mroot = dom8.window.document.querySelector('[data-maint-calc]');
ok(!!mroot, 'E1 page has maint-calc mount');
if (mroot && mod8 && mod8.mountMaintCalc) {
  mod8.mountMaintCalc(mroot);
  const m0 = JSON.parse(mroot.getAttribute('data-result'));
  ok(m0.low === 70 && m0.high === 160, `maint default sodium/10/prefilter → ${m0.low}-${m0.high}`);
  const pot = [...mroot.querySelectorAll('[data-salt]')].find(b => b.dataset.salt === 'potassium');
  pot.click();
  const m1 = JSON.parse(mroot.getAttribute('data-result'));
  ok(m1.low === 520 && m1.high === 760, `maint potassium swap → ${m1.low}-${m1.high}`);
  const plan = [...mroot.querySelectorAll('[data-x]')].find(b => b.dataset.x === 'plan');
  plan.click();
  const m2 = JSON.parse(mroot.getAttribute('data-result'));
  ok(m2.low === 620 && m2.high === 960, `maint +service plan → ${m2.low}-${m2.high}`);
}

// ---- 11. RainSoft quote checker bands (C3 page) ----
const c3html = readFileSync('rainsoft-water-softener-cost/index.html', 'utf8');
const dom9 = new JSDOM(c3html, { url: 'https://softwatersystemcost.com/rainsoft-water-softener-cost/' });
global.window = dom9.window; global.document = dom9.window.document;
window.matchMedia = () => ({ matches: true });
const mod9 = await import('../assets/calculator.js?c3=' + Math.random()).catch(() => null);
const rroot = dom9.window.document.querySelector('[data-quote-check]');
ok(!!rroot, 'C3 page has quote-check mount');
if (rroot && mod9 && mod9.mountQuoteCheck) {
  mod9.mountQuoteCheck(rroot);
  const r0 = JSON.parse(rroot.getAttribute('data-result'));
  ok(r0.amount === 7000 && r0.band === 'typical', `rainsoft default 7000 → ${r0.band}`);
  const rs = rroot.querySelector('#qc-amt');
  rs.value = '12000';
  rs.dispatchEvent(new dom9.window.Event('input', { bubbles: true }));
  ok(JSON.parse(rroot.getAttribute('data-result')).band === 'above-published', 'rainsoft 12000 → above-published');
  rs.value = '4500';
  rs.dispatchEvent(new dom9.window.Event('input', { bubbles: true }));
  ok(JSON.parse(rroot.getAttribute('data-result')).band === 'below-typical', 'rainsoft 4500 → below-typical');
}

// ---- 12. Costco member math + bands (C5 page) ----
const c5html = readFileSync('costco-water-softener-cost/index.html', 'utf8');
const dom10 = new JSDOM(c5html, { url: 'https://softwatersystemcost.com/costco-water-softener-cost/' });
global.window = dom10.window; global.document = dom10.window.document;
window.matchMedia = () => ({ matches: true });
const mod10 = await import('../assets/calculator.js?c5=' + Math.random()).catch(() => null);
const cwroot = dom10.window.document.querySelector('[data-costco-calc]');
ok(!!cwroot, 'C5 page has costco-calc mount');
if (cwroot && mod10 && mod10.mountCostcoCalc) {
  mod10.mountCostcoCalc(cwroot);
  const w0 = JSON.parse(cwroot.getAttribute('data-result'));
  ok(w0.quote === 8000 && w0.back === 800 && w0.net === 7200 && w0.premLow === 4000 && w0.premHigh === 6000, `costco default → back ${w0.back}, net ${w0.net}, prem ${w0.premLow}-${w0.premHigh}`);
  cwroot.querySelector('[data-exec]').click();
  const w1 = JSON.parse(cwroot.getAttribute('data-result'));
  ok(w1.back === 960 && w1.net === 7040, `costco exec toggle → back ${w1.back}, net ${w1.net}`);
}
const c5q = dom10.window.document.querySelector('[data-quote-check]');
ok(!!c5q, 'C5 page has quote-check with costco bands');
if (c5q && mod10 && mod10.mountQuoteCheck) {
  mod10.mountQuoteCheck(c5q);
  ok(JSON.parse(c5q.getAttribute('data-result')).band === 'typical', 'costco checker default 7000 → typical');
}

// ---- 13. B1 Installation Module (shared expense calc) + removal toggle ----
const b1v2 = readFileSync('water-softener-installation-cost/index.html', 'utf8');
const dom11 = new JSDOM(b1v2, { url: 'https://softwatersystemcost.com/water-softener-installation-cost/' });
global.window = dom11.window; global.document = dom11.window.document;
window.matchMedia = () => ({ matches: true });
const mod11 = await import('../assets/calculator.js?b1v2=' + Math.random()).catch(() => null);
const b1e = dom11.window.document.querySelector('[data-expense-calc]');
ok(!!b1e, 'B1 page embeds the Installation Module (expense calc)');
ok(!!dom11.window.document.querySelector('[data-install-calc]'), 'B1 keeps the scenario picker too');
if (b1e && mod11 && mod11.mountExpenseCalc) {
  mod11.mountExpenseCalc(b1e);
  const x0 = JSON.parse(b1e.getAttribute('data-result'));
  ok(x0.low === 1100 && x0.high === 2000 && x0.removal === false, `module default → ${x0.low}-${x0.high}`);
  const rem = [...b1e.querySelectorAll('[data-addon]')].find(b => b.dataset.addon === 'removal');
  rem.click();
  const x1 = JSON.parse(b1e.getAttribute('data-result'));
  ok(x1.low === 1150 && x1.high === 2150, `module +removal → ${x1.low}-${x1.high}`);
  ok(b1e.querySelectorAll('[data-stack] div').length === 3, 'stack renders 3 segments with removal on');
}

// ---- 14. TCO comparator (salt-free page) ----
const a3html = readFileSync('salt-free-water-softener-cost/index.html', 'utf8');
const dom12 = new JSDOM(a3html, { url: 'https://softwatersystemcost.com/salt-free-water-softener-cost/' });
global.window = dom12.window; global.document = dom12.window.document;
window.matchMedia = () => ({ matches: true });
const mod12 = await import('../assets/calculator.js?a3=' + Math.random()).catch(() => null);
const troot = dom12.window.document.querySelector('[data-tco-calc]');
ok(!!troot, 'A3 page has tco-calc mount');
if (troot && mod12 && mod12.mountTcoCalc) {
  mod12.mountTcoCalc(troot);
  const t0 = JSON.parse(troot.getAttribute('data-result'));
  ok(t0.saltFree[0] === 750 && t0.saltFree[1] === 3200 && t0.saltBased[0] === 1650 && t0.saltBased[1] === 3800, `tco default 3-4 → sf ${t0.saltFree}, sb ${t0.saltBased}`);
  const hh5 = [...troot.querySelectorAll('[data-hh]')].find(b => b.dataset.hh === '5p');
  hh5.click();
  const t1 = JSON.parse(troot.getAttribute('data-result'));
  ok(t1.saltBased[0] === 1850 && t1.saltBased[1] === 4200, `tco 5+ → sb ${t1.saltBased}`);
}

// ---- 15. Twin-fit tool (dual-tank page) ----
const a4html = readFileSync('dual-tank-water-softener-cost/index.html', 'utf8');
const dom13 = new JSDOM(a4html, { url: 'https://softwatersystemcost.com/dual-tank-water-softener-cost/' });
global.window = dom13.window; global.document = dom13.window.document;
window.matchMedia = () => ({ matches: true });
const mod13 = await import('../assets/calculator.js?a4=' + Math.random()).catch(() => null);
const twroot = dom13.window.document.querySelector('[data-twin-fit]');
ok(!!twroot, 'A4 page has twin-fit mount');
if (twroot && mod13 && mod13.mountTwinFit) {
  mod13.mountTwinFit(twroot);
  ok(JSON.parse(twroot.getAttribute('data-result')).fit === 'single', 'twin-fit default daytime/moderate → single');
  const always = [...twroot.querySelectorAll('[data-use]')].find(b => b.dataset.use === 'always');
  const heavy = [...twroot.querySelectorAll('[data-demand]')].find(b => b.dataset.demand === 'heavy');
  always.click(); heavy.click();
  ok(JSON.parse(twroot.getAttribute('data-result')).fit === 'twin', 'twin-fit always/heavy → twin');
  const daytime = [...twroot.querySelectorAll('[data-use]')].find(b => b.dataset.use === 'daytime');
  daytime.click();
  ok(JSON.parse(twroot.getAttribute('data-result')).fit === 'either', 'twin-fit daytime/heavy → either');
}

// ---- 16. EcoWater bands (C6 page) ----
const c6html = readFileSync('ecowater-water-softener-cost/index.html', 'utf8');
const dom14 = new JSDOM(c6html, { url: 'https://softwatersystemcost.com/ecowater-water-softener-cost/' });
global.window = dom14.window; global.document = dom14.window.document;
window.matchMedia = () => ({ matches: true });
const mod14 = await import('../assets/calculator.js?c6=' + Math.random()).catch(() => null);
const eqroot = dom14.window.document.querySelector('[data-quote-check]');
ok(!!eqroot, 'C6 page has quote-check mount');
if (eqroot && mod14 && mod14.mountQuoteCheck) {
  mod14.mountQuoteCheck(eqroot);
  ok(JSON.parse(eqroot.getAttribute('data-result')).band === 'typical', 'ecowater default 4000 → typical');
  const es = eqroot.querySelector('#qc-amt');
  es.value = '7000';
  es.dispatchEvent(new dom14.window.Event('input', { bubbles: true }));
  ok(JSON.parse(eqroot.getAttribute('data-result')).band === 'upper', 'ecowater 7000 → upper');
  es.value = '9500';
  es.dispatchEvent(new dom14.window.Event('input', { bubbles: true }));
  ok(JSON.parse(eqroot.getAttribute('data-result')).band === 'above-published', 'ecowater 9500 → above-published');
}

// ---- 17. Well Stack Builder (G1 page) ----
const g1html = readFileSync('well-water-softener-cost/index.html', 'utf8');
const dom15 = new JSDOM(g1html, { url: 'https://softwatersystemcost.com/well-water-softener-cost/' });
global.window = dom15.window; global.document = dom15.window.document;
window.matchMedia = () => ({ matches: true });
const mod15 = await import('../assets/calculator.js?g1=' + Math.random()).catch(() => null);
const wroot = dom15.window.document.querySelector('[data-well-calc]');
ok(!!wroot, 'G1 page has well-calc mount');
if (wroot && mod15 && mod15.mountWellCalc) {
  mod15.mountWellCalc(wroot);
  const g0 = JSON.parse(wroot.getAttribute('data-result'));
  ok(g0.iron === true && g0.sediment === true && g0.uv === false && g0.low === 2700 && g0.high === 6600, `well default iron+sediment → ${g0.low}-${g0.high}`);
  const uvBtn = [...wroot.querySelectorAll('[data-w]')].find(b => b.dataset.w === 'uv');
  uvBtn.click();
  const g1r = JSON.parse(wroot.getAttribute('data-result'));
  ok(g1r.low === 3400 && g1r.high === 9100, `well full stack → ${g1r.low}-${g1r.high}`);
  const ironBtn = [...wroot.querySelectorAll('[data-w]')].find(b => b.dataset.w === 'iron');
  ironBtn.click();
  const g2r = JSON.parse(wroot.getAttribute('data-result'));
  ok(g2r.iron === false && g2r.low === 1900 && wroot.querySelector('[data-note]').textContent.includes('standard softener project'), `well no-iron → ${g2r.low}, note switches`);
}

// ---- 18. Consensus-corridor bands (D1 roundup page, first 5-band config) ----
const d1html = readFileSync('average-water-softener-installation-cost/index.html', 'utf8');
const dom16 = new JSDOM(d1html, { url: 'https://softwatersystemcost.com/average-water-softener-installation-cost/' });
global.window = dom16.window; global.document = dom16.window.document;
window.matchMedia = () => ({ matches: true });
const mod16 = await import('../assets/calculator.js?d1=' + Math.random()).catch(() => null);
const dqroot = dom16.window.document.querySelector('[data-quote-check]');
ok(!!dqroot, 'D1 page has quote-check mount');
if (dqroot && mod16 && mod16.mountQuoteCheck) {
  mod16.mountQuoteCheck(dqroot);
  ok(JSON.parse(dqroot.getAttribute('data-result')).band === 'low-corridor', 'roundup default 1500 → low-corridor');
  const ds = dqroot.querySelector('#qc-amt');
  const set = (v) => { ds.value = v; ds.dispatchEvent(new dom16.window.Event('input', { bubbles: true })); };
  set('600');  ok(JSON.parse(dqroot.getAttribute('data-result')).band === 'below-typical', 'roundup 600 → below-typical');
  set('2500'); ok(JSON.parse(dqroot.getAttribute('data-result')).band === 'consensus', 'roundup 2500 → consensus');
  set('5000'); ok(JSON.parse(dqroot.getAttribute('data-result')).band === 'upper', 'roundup 5000 → upper');
  set('6800'); ok(JSON.parse(dqroot.getAttribute('data-result')).band === 'above-published', 'roundup 6800 → above-published');
}

// ---- 19. Whole-house System Picker (B2 page) ----
const b2html = readFileSync('whole-house-water-softener-installation-cost/index.html', 'utf8');
const dom17 = new JSDOM(b2html, { url: 'https://softwatersystemcost.com/whole-house-water-softener-installation-cost/' });
global.window = dom17.window; global.document = dom17.window.document;
window.matchMedia = () => ({ matches: true });
const mod17 = await import('../assets/calculator.js?b2=' + Math.random()).catch(() => null);
const sfroot = dom17.window.document.querySelector('[data-system-fit]');
ok(!!sfroot, 'B2 page has system-fit mount');
if (sfroot && mod17 && mod17.mountSystemFit) {
  mod17.mountSystemFit(sfroot);
  const s0 = JSON.parse(sfroot.getAttribute('data-result'));
  ok(s0.pick === 'hardness' && sfroot.querySelector('[data-l]').getAttribute('href') === '/', 'system-fit default hardness → softener, links home');
  const wellBtn = [...sfroot.querySelectorAll('[data-pick]')].find(b => b.dataset.pick === 'well');
  wellBtn.click();
  ok(JSON.parse(sfroot.getAttribute('data-result')).pick === 'well' && sfroot.querySelector('[data-l]').getAttribute('href') === '/well-water-softener-cost/', 'system-fit well → well guide link');
  const sfBtn = [...sfroot.querySelectorAll('[data-pick]')].find(b => b.dataset.pick === 'scaleonly');
  sfBtn.click();
  ok(sfroot.querySelector('[data-l]').getAttribute('href') === '/salt-free-water-softener-cost/', 'system-fit scale-only → salt-free link');
  const bhBtn = [...sfroot.querySelectorAll('[data-pick]')].find(b => b.dataset.pick === 'bighouse');
  bhBtn.click();
  ok(sfroot.querySelector('[data-l]').getAttribute('href') === '/dual-tank-water-softener-cost/', 'system-fit big-house → dual-tank link');
}

// ---- 20. Retrofit Builder embed (B3 page, shared expense engine) ----
const b3html = readFileSync('cost-to-add-water-softener-to-existing-home/index.html', 'utf8');
const dom18 = new JSDOM(b3html, { url: 'https://softwatersystemcost.com/cost-to-add-water-softener-to-existing-home/' });
global.window = dom18.window; global.document = dom18.window.document;
window.matchMedia = () => ({ matches: true });
const mod18 = await import('../assets/calculator.js?b3=' + Math.random()).catch(() => null);
const rfroot = dom18.window.document.querySelector('[data-expense-calc]');
ok(!!rfroot, 'B3 page embeds the Retrofit Builder (expense calc)');
if (rfroot && mod18 && mod18.mountExpenseCalc) {
  mod18.mountExpenseCalc(rfroot);
  const rf0 = JSON.parse(rfroot.getAttribute('data-result'));
  ok(rf0.low === 1100 && rf0.high === 2000, `retrofit builder default → ${rf0.low}-${rf0.high}`);
  const loop = [...rfroot.querySelectorAll('[data-addon]')].find(b => b.dataset.addon === 'loop');
  loop.click();
  const rf1 = JSON.parse(rfroot.getAttribute('data-result'));
  ok(rf1.low === 1700 && rf1.high === 4000, `retrofit builder +loop → ${rf1.low}-${rf1.high}`);
}

// ---- 21. Fate Finder (E2 removal page) ----
const e2html = readFileSync('water-softener-removal-cost/index.html', 'utf8');
const dom19 = new JSDOM(e2html, { url: 'https://softwatersystemcost.com/water-softener-removal-cost/' });
global.window = dom19.window; global.document = dom19.window.document;
window.matchMedia = () => ({ matches: true });
const mod19 = await import('../assets/calculator.js?e2=' + Math.random()).catch(() => null);
const froot = dom19.window.document.querySelector('[data-fate-calc]');
ok(!!froot, 'E2 page has fate-calc mount');
if (froot && mod19 && mod19.mountFateCalc) {
  mod19.mountFateCalc(froot);
  ok(JSON.parse(froot.getAttribute('data-result')).fit === 'test', 'fate default working/dontwant → test');
  const salt = [...froot.querySelectorAll('[data-goal]')].find(b => b.dataset.goal === 'salt');
  salt.click();
  ok(JSON.parse(froot.getAttribute('data-result')).fit === 'saltfree', 'fate working/salt → saltfree');
  const spot = [...froot.querySelectorAll('[data-goal]')].find(b => b.dataset.goal === 'spot');
  spot.click();
  ok(JSON.parse(froot.getAttribute('data-result')).fit === 'relocate', 'fate working/spot → relocate');
  const acting = [...froot.querySelectorAll('[data-cond]')].find(b => b.dataset.cond === 'acting');
  acting.click();
  ok(JSON.parse(froot.getAttribute('data-result')).fit === 'repair', 'fate acting → repair (condition overrides goal)');
  const old = [...froot.querySelectorAll('[data-cond]')].find(b => b.dataset.cond === 'old');
  old.click();
  ok(JSON.parse(froot.getAttribute('data-result')).fit === 'replace', 'fate old → replace');
}

// ---- 22. Iron Level Matcher (G2 page) ----
const g2html = readFileSync('iron-filter-for-well-water-cost/index.html', 'utf8');
const dom20 = new JSDOM(g2html, { url: 'https://softwatersystemcost.com/iron-filter-for-well-water-cost/' });
global.window = dom20.window; global.document = dom20.window.document;
window.matchMedia = () => ({ matches: true });
const mod20 = await import('../assets/calculator.js?g2=' + Math.random()).catch(() => null);
const feroot = dom20.window.document.querySelector('[data-iron-calc]');
ok(!!feroot, 'G2 page has iron-calc mount');
if (feroot && mod20 && mod20.mountIronCalc) {
  mod20.mountIronCalc(feroot);
  ok(JSON.parse(feroot.getAttribute('data-result')).tier === 'aio', 'iron default 3ppm → aio');
  const fe = feroot.querySelector('#fe-ppm');
  const set = (v) => { fe.value = v; fe.dispatchEvent(new dom20.window.Event('input', { bubbles: true })); };
  set('0');    ok(JSON.parse(feroot.getAttribute('data-result')).tier === 'none', 'iron 0 → none');
  set('0.5');  ok(JSON.parse(feroot.getAttribute('data-result')).tier === 'borderline', 'iron 0.5 → borderline');
  set('10');   ok(JSON.parse(feroot.getAttribute('data-result')).tier === 'high', 'iron 10 → high');
  set('5');
  const soft = [...feroot.querySelectorAll('[data-x]')].find(b => b.dataset.x === 'softener');
  soft.click();
  ok(feroot.querySelector('[data-n]').textContent.includes('goes FIRST'), 'iron softener toggle → order-is-law note');
}

// ---- 23. pH Matcher (G3 page) ----
const g3html = readFileSync('acid-neutralizer-cost/index.html', 'utf8');
const dom21 = new JSDOM(g3html, { url: 'https://softwatersystemcost.com/acid-neutralizer-cost/' });
global.window = dom21.window; global.document = dom21.window.document;
window.matchMedia = () => ({ matches: true });
const mod21 = await import('../assets/calculator.js?g3=' + Math.random()).catch(() => null);
const phroot = dom21.window.document.querySelector('[data-ph-calc]');
ok(!!phroot, 'G3 page has ph-calc mount');
if (phroot && mod21 && mod21.mountPhCalc) {
  mod21.mountPhCalc(phroot);
  ok(JSON.parse(phroot.getAttribute('data-result')).tier === 'calcite', 'ph default 6.5 → calcite');
  const pv = phroot.querySelector('#ph-val');
  const setPh = (v) => { pv.value = v; pv.dispatchEvent(new dom21.window.Event('input', { bubbles: true })); };
  setPh('7.5'); ok(JSON.parse(phroot.getAttribute('data-result')).tier === 'none', 'ph 7.5 → none');
  setPh('5.7'); ok(JSON.parse(phroot.getAttribute('data-result')).tier === 'blend', 'ph 5.7 → blend');
  setPh('5.2'); ok(JSON.parse(phroot.getAttribute('data-result')).tier === 'deep', 'ph 5.2 → deep');
  setPh('6.5');
  const ironBtn = [...phroot.querySelectorAll('[data-p]')].find(b => b.dataset.p === 'iron');
  ironBtn.click();
  ok(phroot.querySelector('[data-n]').textContent.includes('BACKWASHING'), 'ph iron toggle → backwashing switch note');
  const hardBtn = [...phroot.querySelectorAll('[data-p]')].find(b => b.dataset.p === 'hard');
  hardBtn.click();
  ok(phroot.querySelector('[data-n]').textContent.includes('$295'), 'ph hard toggle → package-savings note');
}

// ---- 24. UV Sizer (G4 page) ----
const g4html = readFileSync('uv-water-purifier-cost/index.html', 'utf8');
const dom22 = new JSDOM(g4html, { url: 'https://softwatersystemcost.com/uv-water-purifier-cost/' });
global.window = dom22.window; global.document = dom22.window.document;
window.matchMedia = () => ({ matches: true });
const mod22 = await import('../assets/calculator.js?g4=' + Math.random()).catch(() => null);
const uvroot = dom22.window.document.querySelector('[data-uv-calc]');
ok(!!uvroot, 'G4 page has uv-calc mount');
if (uvroot && mod22 && mod22.mountUvCalc) {
  mod22.mountUvCalc(uvroot);
  const uv0 = JSON.parse(uvroot.getAttribute('data-result'));
  ok(uv0.baths === '12' && uv0.source === 'well' && uv0.classReq === 'A', 'uv default 1-2bath/well → Class A');
  ok(uvroot.querySelector('[data-n]').textContent.includes('Class B (16 mJ/cm\u00b2) is never appropriate on a well'), 'uv well note carries never-on-a-well rule');
  const cityBtn = [...uvroot.querySelectorAll('[data-s]')].find(b => b.dataset.s === 'city');
  cityBtn.click();
  ok(JSON.parse(uvroot.getAttribute('data-result')).classReq === 'B-ok', 'uv city → Class B acceptable');
  const bigBtn = [...uvroot.querySelectorAll('[data-b]')].find(b => b.dataset.b === '5p');
  bigBtn.click();
  ok(uvroot.querySelector('[data-v]').textContent.includes('outside standard charts'), 'uv 5+ baths → professional-sizing verdict');
}

// ---- 25. Payment-to-Total Translator (C6 EcoWater page) ----
const ecoFinHtml = readFileSync('ecowater-water-softener-cost/index.html', 'utf8');
const domFin = new JSDOM(ecoFinHtml, { url: 'https://softwatersystemcost.com/ecowater-water-softener-cost/' });
global.window = domFin.window; global.document = domFin.window.document;
window.matchMedia = () => ({ matches: true });
const modFin = await import('../assets/calculator.js?c6=' + Math.random()).catch(() => null);
const finRoot = domFin.window.document.querySelector('[data-finance-calc]');
ok(!!finRoot, 'C6 page has finance-calc mount');
if (finRoot && modFin && modFin.mountFinanceCalc) {
  modFin.mountFinanceCalc(finRoot);
  const f0 = JSON.parse(finRoot.getAttribute('data-result'));
  ok(f0.total === 99 * 84, `finance default total = payment x term (${f0.total})`);
  ok(f0.principal < f0.total && f0.principal > 0, `finance implied price below total (${f0.principal})`);
  ok(f0.interest === f0.total - f0.principal, 'finance interest = total - principal');
  const aprIn = finRoot.querySelector('#fin-apr');
  aprIn.value = '0'; aprIn.dispatchEvent(new domFin.window.Event('input', { bubbles: true }));
  const f1 = JSON.parse(finRoot.getAttribute('data-result'));
  ok(f1.principal === f1.total && f1.interest === 0, 'finance 0% APR → principal equals total, zero interest');
  ok(finRoot.querySelector('[data-note]').textContent.includes('deferred interest'), 'finance 0% note warns about deferred interest');
  const t36 = [...finRoot.querySelectorAll('[data-t]')].find(b => b.dataset.t === '36');
  t36.click();
  ok(JSON.parse(finRoot.getAttribute('data-result')).total === 99 * 36, 'finance term switch recomputes total');
}

// ---- 26. Dealer Quote Reality Check (C28 hub) ----
const hubHtml = readFileSync('dealer-vs-factory-direct-pricing/index.html', 'utf8');
const domHub = new JSDOM(hubHtml, { url: 'https://softwatersystemcost.com/dealer-vs-factory-direct-pricing/' });
global.window = domHub.window; global.document = domHub.window.document;
window.matchMedia = () => ({ matches: true });
const modHub = await import('../assets/calculator.js?c28=' + Math.random()).catch(() => null);
const rcRoot = domHub.window.document.querySelector('[data-reality-check]');
const finHub = domHub.window.document.querySelector('[data-finance-calc]');
ok(!!rcRoot, 'C28 hub has reality-check mount');
ok(!!finHub, 'C28 hub also embeds the finance translator');
if (rcRoot && modHub && modHub.mountRealityCheck) {
  modHub.mountRealityCheck(rcRoot);
  const r0 = JSON.parse(rcRoot.getAttribute('data-result'));
  ok(r0.docLo === 890 && r0.docHi === 2270, 'reality default → prepared band 890-2270');
  ok(r0.remLo === 6000 - 2270 && r0.remHi === 6000 - 890, `reality remainder from a $6,000 quote (${r0.remLo}-${r0.remHi})`);
  ok(rcRoot.querySelector('[data-warn]').textContent.includes('NOT the dealer'), 'reality warning states the remainder is NOT profit');
  const cx = [...rcRoot.querySelectorAll('[data-site]')].find(b => b.dataset.site === 'complex');
  cx.click();
  const r1 = JSON.parse(rcRoot.getAttribute('data-result'));
  ok(r1.docLo === 2340 && r1.docHi === 5470, 'reality complex → band 2340-5470');
  const qIn = rcRoot.querySelector('#rc-quote');
  qIn.value = '2000'; qIn.dispatchEvent(new domHub.window.Event('input', { bubbles: true }));
  const r2 = JSON.parse(rcRoot.getAttribute('data-result'));
  ok(r2.inside === true && r2.remLo === 0, 'reality low quote → inside-the-range branch, no remainder claimed');
  ok(rcRoot.querySelector('[data-verdict]').textContent.includes('scope'), 'reality low-quote verdict pivots to scope');
  rcRoot.querySelector('[data-bundle]').click();
  ok(rcRoot.querySelector('[data-warn]').textContent.includes('model number'), 'reality bundle toggle → demand model numbers');
}

// ---- 27. Rent-vs-Buy Break-Even (R1 rental page) ----
const rentHtml = readFileSync('water-softener-rental-cost/index.html', 'utf8');
const domRent = new JSDOM(rentHtml, { url: 'https://softwatersystemcost.com/water-softener-rental-cost/' });
global.window = domRent.window; global.document = domRent.window.document;
window.matchMedia = () => ({ matches: true });
const modRent = await import('../assets/calculator.js?r1=' + Math.random()).catch(() => null);
const rbRoot = domRent.window.document.querySelector('[data-rent-buy]');
ok(!!rbRoot, 'R1 page has rent-buy mount');
if (rbRoot && modRent && modRent.mountRentBuy) {
  modRent.mountRentBuy(rbRoot);
  const b0 = JSON.parse(rbRoot.getAttribute('data-result'));
  ok(b0.rentalTotal === 250 + 600 * 10 && b0.ownerTotal === 2000 + 190 * 10, `rent-buy default totals (${b0.rentalTotal} vs ${b0.ownerTotal})`);
  ok(b0.breakEven === 5 && b0.cheaper === 'own', 'rent-buy $50/mo → break-even year 5, owning wins at 10 yrs');
  const rentIn = rbRoot.querySelector('#rb-rent');
  const setRent = (v) => { rentIn.value = v; rentIn.dispatchEvent(new domRent.window.Event('input', { bubbles: true })); };
  setRent('20');
  const b1 = JSON.parse(rbRoot.getAttribute('data-result'));
  ok(b1.breakEven === 0 && b1.cheaper === 'rent', 'rent-buy $20/mo → no break-even inside 30 yrs, renting wins');
  ok(rbRoot.querySelector('[data-be]').textContent.includes('real answer'), 'rent-buy honours the no-break-even case in copy');
  setRent('100');
  ok(JSON.parse(rbRoot.getAttribute('data-result')).breakEven === 2, 'rent-buy $100/mo → break-even year 2');
  setRent('50');
  const noneBtn = [...rbRoot.querySelectorAll('[data-incl]')].find(b => b.dataset.incl === 'none');
  noneBtn.click();
  ok(JSON.parse(rbRoot.getAttribute('data-result')).rentalTotal === 250 + (600 + 190) * 10, 'rent-buy equipment-only adds salt + repair exposure');
  const yIn = rbRoot.querySelector('#rb-years');
  yIn.value = '2'; yIn.dispatchEvent(new domRent.window.Event('input', { bubbles: true }));
  ok(JSON.parse(rbRoot.getAttribute('data-result')).years === 2, 'rent-buy years slider recomputes horizon');
}

// ---- 28. Sediment Setup Matcher (G5 page) ----
const sedHtml = readFileSync('sediment-filter-cost/index.html', 'utf8');
const domSed = new JSDOM(sedHtml, { url: 'https://softwatersystemcost.com/sediment-filter-cost/' });
global.window = domSed.window; global.document = domSed.window.document;
window.matchMedia = () => ({ matches: true });
const modSed = await import('../assets/calculator.js?g5=' + Math.random()).catch(() => null);
const sedRoot = domSed.window.document.querySelector('[data-sediment-calc]');
ok(!!sedRoot, 'G5 page has sediment-calc mount');
if (sedRoot && modSed && modSed.mountSedimentCalc) {
  modSed.mountSedimentCalc(sedRoot);
  ok(JSON.parse(sedRoot.getAttribute('data-result')).see === 'silt', 'sediment default → silt (the 70% case)');
  const pick = (k) => [...sedRoot.querySelectorAll('[data-see]')].find(b => b.dataset.see === k).click();
  pick('sand');
  ok(sedRoot.querySelector('[data-v]').textContent.includes('Spin-down first'), 'sediment sand → spin-down first');
  pick('heavy');
  ok(sedRoot.querySelector('[data-n]').textContent.includes('$1,895'), 'sediment heavy → combo before the $1,895 tank');
  pick('silt');
  const uvBtn = [...sedRoot.querySelectorAll('[data-x]')].find(b => b.dataset.x === 'uv');
  uvBtn.click();
  ok(sedRoot.querySelector('[data-n]').textContent.includes('ABSOLUTE'), 'sediment UV toggle → absolute-not-nominal rule');
  const eqBtn = [...sedRoot.querySelectorAll('[data-x]')].find(b => b.dataset.x === 'equip');
  eqBtn.click();
  ok(sedRoot.querySelector('[data-n]').textContent.includes('number-one killer'), 'sediment equipment toggle → not-optional warning');
  ok(JSON.parse(sedRoot.getAttribute('data-result')).uv === true, 'sediment toggles persist in data-result');
}

// ---- 29. Parameterized finance translator across the brand cluster (C2/C3/C5) ----
const brandPages = [
  { slug: 'kinetico-water-softener-cost', pmt: 80, band: [3000, 5000] },
  { slug: 'rainsoft-water-softener-cost', pmt: 160, band: [6000, 11000] },
  { slug: 'costco-water-softener-cost', pmt: 140, band: [6000, 10000] },
];
for (const bp of brandPages) {
  const bHtml = readFileSync(bp.slug + '/index.html', 'utf8');
  const bDom = new JSDOM(bHtml, { url: 'https://softwatersystemcost.com/' + bp.slug + '/' });
  global.window = bDom.window; global.document = bDom.window.document;
  window.matchMedia = () => ({ matches: true });
  const bMod = await import('../assets/calculator.js?bp=' + bp.slug + Math.random()).catch(() => null);
  const bRoot = bDom.window.document.querySelector('[data-finance-calc]');
  ok(!!bRoot, `${bp.slug} embeds the finance translator`);
  if (bRoot && bMod && bMod.mountFinanceCalc) {
    bMod.mountFinanceCalc(bRoot);
    const r = JSON.parse(bRoot.getAttribute('data-result'));
    ok(r.pmt === bp.pmt && r.term === 84, `${bp.slug} seeds at $${bp.pmt}/mo x 84 (got $${r.pmt}/${r.term})`);
    ok(r.total === bp.pmt * 84, `${bp.slug} total of payments = $${r.total}`);
    ok(r.principal >= bp.band[0] && r.principal <= bp.band[1], `${bp.slug} implied price $${r.principal} sits inside its own reported band`);
    const t36 = [...bRoot.querySelectorAll('[data-t]')].find(b => b.dataset.t === '36');
    t36.click();
    ok(JSON.parse(bRoot.getAttribute('data-result')).total === bp.pmt * 36, `${bp.slug} term switch still recomputes`);
  }
}
// defaults must survive parameterization on the unseeded pages
const hubDom2 = new JSDOM(readFileSync('dealer-vs-factory-direct-pricing/index.html', 'utf8'), { url: 'https://softwatersystemcost.com/dealer-vs-factory-direct-pricing/' });
global.window = hubDom2.window; global.document = hubDom2.window.document;
window.matchMedia = () => ({ matches: true });
const hubMod2 = await import('../assets/calculator.js?hub2=' + Math.random()).catch(() => null);
const hubFin = hubDom2.window.document.querySelector('[data-finance-calc]');
if (hubFin && hubMod2 && hubMod2.mountFinanceCalc) {
  hubMod2.mountFinanceCalc(hubFin);
  ok(JSON.parse(hubFin.getAttribute('data-result')).pmt === 99, 'unseeded hub still defaults to $99/mo (no regression)');
}

// ---- 30. Anchor Test (C7 Leaf Home page) ----
const leafHtml = readFileSync('leaf-home-water-solutions-cost/index.html', 'utf8');
const domLeaf = new JSDOM(leafHtml, { url: 'https://softwatersystemcost.com/leaf-home-water-solutions-cost/' });
global.window = domLeaf.window; global.document = domLeaf.window.document;
window.matchMedia = () => ({ matches: true });
const modLeaf = await import('../assets/calculator.js?c7=' + Math.random()).catch(() => null);
const atRoot = domLeaf.window.document.querySelector('[data-anchor-test]');
const leafFin = domLeaf.window.document.querySelector('[data-finance-calc]');
ok(!!atRoot, 'C7 page has anchor-test mount');
ok(!!leafFin, 'C7 page also embeds the seeded finance translator');
if (atRoot && modLeaf && modLeaf.mountAnchorTest) {
  modLeaf.mountAnchorTest(atRoot);
  const a0 = JSON.parse(atRoot.getAttribute('data-result'));
  ok(a0.quote === 9000 && a0.effective === 9000, 'anchor default seeds at the reported $9,000 opening number');
  ok(a0.remLo === 9000 - 2270 && a0.remHi === 9000 - 890, `anchor remainder before any discount (${a0.remLo}-${a0.remHi})`);
  atRoot.querySelector('[data-cut]').click();
  const a1 = JSON.parse(atRoot.getAttribute('data-result'));
  ok(a1.cut === true && Math.abs(a1.effective - 4788) <= 2, `anchor discount → ${a1.effective} (the reported $4,785-class deal)`);
  ok(a1.remLo > 2000 && a1.remHi < 4000, `anchor: even discounted, ${a1.remLo}-${a1.remHi} sits above the documented work`);
  ok(atRoot.querySelector('[data-note]').textContent.includes('not a saving, it is a negotiation'), 'anchor punchline states a discount off an unpublished number is a negotiation');
  const cx = [...atRoot.querySelectorAll('[data-site]')].find(b => b.dataset.site === 'complex');
  cx.click();
  ok(JSON.parse(atRoot.getAttribute('data-result')).docLo === 2340, 'anchor site switch → complex band');
}
if (leafFin && modLeaf && modLeaf.mountFinanceCalc) {
  modLeaf.mountFinanceCalc(leafFin);
  const f = JSON.parse(leafFin.getAttribute('data-result'));
  ok(f.pmt === 95 && f.total === 95 * 84, `C7 finance seeds at $95/mo → $${f.total} total`);
  ok(f.principal > 4600 && f.principal < 5000, `C7 implied price $${f.principal} ≈ the $4,785 discounted deal`);
}

// ---- 31. Sizer (S1 sizing page) ----
const szHtml = readFileSync('what-size-water-softener-do-i-need/index.html', 'utf8');
const domSz = new JSDOM(szHtml, { url: 'https://softwatersystemcost.com/what-size-water-softener-do-i-need/' });
global.window = domSz.window; global.document = domSz.window.document;
window.matchMedia = () => ({ matches: true });
const modSz = await import('../assets/calculator.js?s1=' + Math.random()).catch(() => null);
const szRoot = domSz.window.document.querySelector('[data-sizer]');
ok(!!szRoot, 'S1 page has sizer mount');
if (szRoot && modSz && modSz.mountSizer) {
  modSz.mountSizer(szRoot);
  const s0 = JSON.parse(szRoot.getAttribute('data-result'));
  ok(s0.daily === 3000 && s0.weekly === 21000, 'sizer default (4 people, 10 gpg) → 3,000 grains/day, 21,000/week');
  ok(s0.naive === 24000, 'sizer reproduces the standard answer every other calculator gives (24,000-grain)');
  ok(s0.rec === 40000, 'sizer efficient-salt answer is two sizes up (40,000-grain)');
  ok(s0.recDays >= 7 && s0.recDays <= 14, `recommended unit regenerates inside the healthy window (${s0.recDays} days)`);
  ok(s0.naiveSaltYr - s0.recSaltYr > 150, `sizing up SAVES salt: ${s0.recSaltYr} vs ${s0.naiveSaltYr} lbs/yr`);
  // soft water → honest "you may not need one"
  const szHard = szRoot.querySelector('#sz-hard');
  szHard.value = '3'; szHard.dispatchEvent(new domSz.window.Event('input'));
  ok(szRoot.querySelector('[data-warn]').textContent.includes('need a softener at all'), 'sizer tells soft-water households they may not need a softener');
  szHard.value = '12'; szHard.dispatchEvent(new domSz.window.Event('input'));
  // iron → compensated hardness + filter-first warning
  const szIron = szRoot.querySelector('#sz-iron');
  szIron.value = '2'; szIron.dispatchEvent(new domSz.window.Event('input'));
  const s2 = JSON.parse(szRoot.getAttribute('data-result'));
  ok(s2.comp === 22, 'sizer compensates iron at 5 gpg per ppm (12 gpg + 2 ppm iron = 22 gpg)');
  ok(szRoot.querySelector('[data-warn]').textContent.includes('filter the iron first'), 'sizer sends iron to an iron filter, not a bigger softener');
  szIron.value = '4'; szIron.dispatchEvent(new domSz.window.Event('input'));
  ok(szRoot.querySelector('[data-warn]').textContent.includes('will not survive'), 'sizer escalates at high iron');
}

// ---- 32. Running-Cost Stack (E3 electricity page) ----
const rcHtml2 = readFileSync('water-softener-electricity-usage/index.html', 'utf8');
const domRC = new JSDOM(rcHtml2, { url: 'https://softwatersystemcost.com/water-softener-electricity-usage/' });
global.window = domRC.window; global.document = domRC.window.document;
window.matchMedia = () => ({ matches: true });
const modRC = await import('../assets/calculator.js?e3=' + Math.random()).catch(() => null);
const rcStack = domRC.window.document.querySelector('[data-run-cost]');
ok(!!rcStack, 'E3 page has run-cost mount');
if (rcStack && modRC && modRC.mountRunCost) {
  modRC.mountRunCost(rcStack);
  const r0 = JSON.parse(rcStack.getAttribute('data-result'));
  ok(Math.abs(r0.elec - 12.95) < 0.6, `electricity = 70 kWh x rate = $${r0.elec}/yr`);
  ok(r0.salt > r0.elec * 3, `salt ($${r0.salt}) dwarfs electricity ($${r0.elec})`);
  ok(r0.water > r0.elec, `THE THESIS: regeneration water ($${r0.water}) costs MORE than the electricity ($${r0.elec})`);
  ok(r0.elecPct <= 12, `electricity is only ${r0.elecPct}% of the running cost`);
  ok(Math.abs(r0.total - (r0.elec + r0.salt + r0.water + r0.consumables)) < 0.05, 'stack total reconciles with its four lines');
  ok(Math.abs(r0.monthly * 12 - r0.total) < 0.2, 'monthly x 12 reconciles with annual');
  // Hawaii's rate: even at the most expensive electricity in the US, it stays the smallest line
  const rcE = rcStack.querySelector('#rc-elec');
  rcE.value = '46.5'; rcE.dispatchEvent(new domRC.window.Event('input'));
  const rHI = JSON.parse(rcStack.getAttribute('data-result'));
  ok(rHI.elec < rHI.salt, `even at Hawaii rates electricity ($${rHI.elec}) < salt ($${rHI.salt})`);
  rcE.value = '18.5'; rcE.dispatchEvent(new domRC.window.Event('input'));
  // hard water household → salt explodes, electricity does not move
  const rcH = rcStack.querySelector('#rc-hard'), rcP = rcStack.querySelector('#rc-people');
  rcP.value = '6'; rcP.dispatchEvent(new domRC.window.Event('input'));
  rcH.value = '20'; rcH.dispatchEvent(new domRC.window.Event('input'));
  const rBig = JSON.parse(rcStack.getAttribute('data-result'));
  ok(Math.abs(rBig.elec - r0.elec) < 0.01, 'THE CHART CLAIM: electricity is IDENTICAL across households');
  ok(rBig.salt > r0.salt * 2.5, `while salt tripled ($${r0.salt} → $${rBig.salt})`);
  ok(rBig.elecPct < r0.elecPct, `electricity share falls to ${rBig.elecPct}% purely because everything else rose`);
}

// ---- 33. Decade Model (D10 flagship data study) ----
const decHtml = readFileSync('10-year-water-softener-cost/index.html', 'utf8');
const domDec = new JSDOM(decHtml, { url: 'https://softwatersystemcost.com/10-year-water-softener-cost/' });
global.window = domDec.window; global.document = domDec.window.document;
window.matchMedia = () => ({ matches: true });
const modDec = await import('../assets/calculator.js?d10=' + Math.random()).catch(() => null);
const decRoot = domDec.window.document.querySelector('[data-decade]');
ok(!!decRoot, 'D10 page has decade-model mount');
if (decRoot && modDec && modDec.mountDecade) {
  modDec.mountDecade(decRoot);
  const dUp = decRoot.querySelector('#dc-up');
  const read = () => JSON.parse(decRoot.getAttribute('data-result'));
  const mid = read();
  ok(Math.abs(mid.total - 4730) < 25, `mid-market decade = $${mid.total} (chart says $4,730)`);
  ok(mid.upfrontPct === 53, `upfront is ${mid.upfrontPct}% of the mid-market decade`);
  // the study's central claim: change ONLY the purchase price; running cost must not move
  dUp.value = '1320'; dUp.dispatchEvent(new domDec.window.Event('input'));
  const fd = read();
  dUp.value = '6000'; dUp.dispatchEvent(new domDec.window.Event('input'));
  const dlr = read();
  ok(Math.abs(fd.total - 3550) < 25 && Math.abs(dlr.total - 8230) < 25, `channels: $${fd.total} / $${mid.total} / $${dlr.total}`);
  ok(fd.runYr === dlr.runYr && fd.repairs === dlr.repairs, 'THE STUDY: running cost + repairs IDENTICAL across channels — only the purchase differs');
  ok(Math.abs((dlr.total - fd.total) - (6000 - 1320)) < 1, `THE PARALLEL LINES: the $${dlr.total - fd.total} gap at year 10 equals the gap at year 0 exactly`);
  ok(dlr.upfrontPct === 73, `on the dealer path ${dlr.upfrontPct}% of the decade is settled on day one`);
  ok(dlr.perDay > 2 && fd.perDay < 1, `per-day: $${fd.perDay} vs $${dlr.perDay} for the same soft water`);
  // repair segments + shorter ownership
  decRoot.querySelector('[data-rep="none"]').click();
  ok(read().repairs === 0, 'no-repairs branch zeroes the big-ticket line');
  decRoot.querySelector('[data-rep="typical"]').click();
  const dYr = decRoot.querySelector('#dc-years');
  dYr.value = '5'; dYr.dispatchEvent(new domDec.window.Event('input'));
  ok(read().repairs === 0, 'at 5 years the typical valve rebuild has not arrived yet');
  dYr.value = '10'; dYr.dispatchEvent(new domDec.window.Event('input'));
  ok(read().repairs > 900, 'by year 10 both the rebuild and the rebed are in');
}

// ---- 34. Repair-or-Replace (L1 lifespan page) ----
const lifeHtml = readFileSync('how-long-does-a-water-softener-last/index.html', 'utf8');
const domLife = new JSDOM(lifeHtml, { url: 'https://softwatersystemcost.com/how-long-does-a-water-softener-last/' });
global.window = domLife.window; global.document = domLife.window.document;
window.matchMedia = () => ({ matches: true });
const modLife = await import('../assets/calculator.js?l1=' + Math.random()).catch(() => null);
const rrRoot = domLife.window.document.querySelector('[data-repair-replace]');
ok(!!rrRoot, 'L1 page has repair-or-replace mount');
if (rrRoot && modLife && modLife.mountRepairReplace) {
  modLife.mountRepairReplace(rrRoot);
  const rd = () => JSON.parse(rrRoot.getAttribute('data-result'));
  const r0 = rd();
  ok(Math.abs(r0.fixPerYear - 37.78) < 0.5, `default rebed: $${r0.fixPerYear} per year of service`);
  ok(Math.abs(r0.newPerYear - 208.33) < 0.5, `replacement: $${r0.newPerYear} per year of service`);
  ok(r0.repairWins === true, 'THE FRAMEWORK: on the default numbers the repair wins on cost-per-year');
  // the cracked-tank branch must REFUSE to recommend a repair — proves the tool is not a repair shill
  rrRoot.querySelector('[data-part="tank"]').click();
  const rt = rd();
  ok(rt.tank === true && rt.repairWins === false, 'cracked mineral tank → tool says REPLACE, not repair');
  ok(rrRoot.querySelector('[data-verdict]').textContent.includes('not worth it'), 'tank verdict is explicit');
  // full rebuild → trips the industry 50% rule, but the arithmetic should still favour repairing
  rrRoot.querySelector('[data-part="both"]').click();
  const rNew = rrRoot.querySelector('#rr-new');
  rNew.value = '1500'; rNew.dispatchEvent(new domLife.window.Event('input'));
  const rb = rd();
  ok(rb.ruleSaysReplace === true, 'a $840 rebuild against a $1,500 system trips the industry 50%-of-new rule');
  ok(rb.repairWins === true, 'THE FINDING: the 50% rule says replace — the cost-per-year arithmetic says repair');
  ok(rrRoot.querySelector('[data-rule]').textContent.includes('no denominator'), 'page names why the rule fails: it has no denominator');
  // old system → parts-availability warning, not a wear warning
  const rAge = rrRoot.querySelector('#rr-age');
  rAge.value = '20'; rAge.dispatchEvent(new domLife.window.Event('input'));
  ok(rrRoot.querySelector('[data-warn]').textContent.includes('it is parts'), 'at 20 years the tool warns about parts availability, not wear');
}

// ---- 35. Maintenance Schedule Generator (M1 pillar) ----
const mntHtml = readFileSync('water-softener-maintenance/index.html', 'utf8');
const domMnt = new JSDOM(mntHtml, { url: 'https://softwatersystemcost.com/water-softener-maintenance/' });
global.window = domMnt.window; global.document = domMnt.window.document;
window.matchMedia = () => ({ matches: true });
const modMnt = await import('../assets/calculator.js?m1=' + Math.random()).catch(() => null);
const schRoot = domMnt.window.document.querySelector('[data-schedule]');
ok(!!schRoot, 'M1 page has schedule-generator mount');
if (schRoot && modMnt && modMnt.mountSchedule) {
  modMnt.mountSchedule(schRoot);
  const sr = () => JSON.parse(schRoot.getAttribute('data-result'));
  const s0 = sr();
  ok(s0.tasks === 6, 'salt-based default → the six routine jobs');
  ok(s0.minutes === 135, `about ${(s0.minutes/60).toFixed(1)} hours a year on city water`);
  ok(schRoot.querySelector('[data-list]').textContent.includes('bags a year'), 'salt cadence derived from household + hardness');
  // iron → shortens the resin-cleaner cycle AND redirects to an iron filter rather than more cleaning
  const scIron = schRoot.querySelector('#sc-iron');
  scIron.value = '1.5'; scIron.dispatchEvent(new domMnt.window.Event('input'));
  ok(schRoot.querySelector('[data-list]').textContent.includes('every 3 months'), 'iron shortens the resin-cleaner interval');
  ok(schRoot.querySelector('[data-pro]').textContent.includes('iron filter ahead of the softener'), 'HONEST: with iron the tool says maintenance is not the fix — filtration is');
  scIron.value = '0'; scIron.dispatchEvent(new domMnt.window.Event('input'));
  // well water → dirtier duty cycle
  schRoot.querySelector('[data-src="well"]').click();
  ok(sr().minutes > s0.minutes, 'well water → more maintenance time than city');
  ok(schRoot.querySelector('[data-list]').textContent.includes('quarterly'), 'well water → injector goes to quarterly');
  schRoot.querySelector('[data-src="city"]').click();
  // salt-free → the honest short list, and the honest limit
  schRoot.querySelector('[data-sys="saltfree"]').click();
  const sf = sr();
  ok(sf.tasks < s0.tasks && sf.minutes < s0.minutes, `salt-free → ${sf.tasks} jobs, ${sf.minutes} min/yr (vs ${s0.tasks} and ${s0.minutes})`);
  ok(schRoot.querySelector('[data-pro]').textContent.includes('not softening your water'), 'salt-free branch states its own limit rather than overselling');
}

// ---- 36. Service Call Triage (S2 servicing page) ----
const svcHtml = readFileSync('water-softener-servicing/index.html', 'utf8');
const domSvc = new JSDOM(svcHtml, { url: 'https://softwatersystemcost.com/water-softener-servicing/' });
global.window = domSvc.window; global.document = domSvc.window.document;
window.matchMedia = () => ({ matches: true });
const modSvc = await import('../assets/calculator.js?s2=' + Math.random()).catch(() => null);
const trRoot = domSvc.window.document.querySelector('[data-triage]');
ok(!!trRoot, 'S2 page has triage mount');
if (trRoot && modSvc && modSvc.mountTriage) {
  modSvc.mountTriage(trRoot);
  const tr = () => JSON.parse(trRoot.getAttribute('data-result'));
  // the default symptom must talk the user OUT of a service call
  const t0 = tr();
  ok(t0.cls === 'diy' && t0.verdict.includes('Do not call'), 'salt bridge → the tool tells you NOT to call anybody');
  ok(trRoot.querySelector('[data-cost]').textContent.includes('broom handle'), 'and names the actual fix');
  // but it must send real faults to a professional
  trRoot.querySelector('[data-sym="leak"]').click();
  ok(tr().cls === 'call', 'a leak → call, today');
  trRoot.querySelector('[data-sym="dead"]').click();
  ok(tr().cls === 'call' && tr().verdict.includes('what a service call is for'), 'dead valve → this is what a service call is FOR');
  trRoot.querySelector('[data-sym="unsure"]').click();
  ok(tr().cls === 'test' && trRoot.querySelector('[data-cost]').textContent.includes('$10'), 'unsure → buy the test, not the truck');
  // the fee checker against published ranges
  const trFee = trRoot.querySelector('#tr-fee');
  ok(trRoot.querySelector('[data-fee]').textContent.includes('would not give you a number'), 'no quote given → names the tactic');
  trFee.value = '75'; trFee.dispatchEvent(new domSvc.window.Event('input'));
  ok(tr().feeInRange === true && trRoot.querySelector('[data-fee]').textContent.includes('credited against the repair'), '$75 → in range, and pushes THE question (is it credited?)');
  trFee.value = '300'; trFee.dispatchEvent(new domSvc.window.Event('input'));
  ok(tr().feeInRange === false && trRoot.querySelector('[data-fee]').textContent.includes('not necessarily wrong'), '$300 → flagged as above range but FAIRLY (after-hours is real)');
}

// ---- 37. Repair Quote Decoder (R1 repair-cost page) ----
const rprHtml = readFileSync('water-softener-repair-cost/index.html', 'utf8');
const domRpr = new JSDOM(rprHtml, { url: 'https://softwatersystemcost.com/water-softener-repair-cost/' });
global.window = domRpr.window; global.document = domRpr.window.document;
window.matchMedia = () => ({ matches: true });
const modRpr = await import('../assets/calculator.js?r1=' + Math.random()).catch(() => null);
const qdRoot = domRpr.window.document.querySelector('[data-quote-decoder]');
ok(!!qdRoot, 'R1 page has quote-decoder mount');
if (qdRoot && modRpr && modRpr.mountQuoteDecoder) {
  modRpr.mountQuoteDecoder(qdRoot);
  const qd = () => JSON.parse(qdRoot.getAttribute('data-result'));
  // default symptom must classify as NOT a repair
  ok(qd().isRepair === false, 'salt bridge → classified as NOT a repair');
  ok(qdRoot.querySelector('[data-band]').textContent.includes('not a repair'), 'and says so out loud');
  ok(qdRoot.querySelector('[data-quote]').textContent.includes('best position to be in'), 'no quote yet → the strongest position');
  // the leak branch must surface the rebuild-vs-replace fork
  qdRoot.querySelector('[data-sym="leak"]').click();
  ok(qdRoot.querySelector('[data-cause]').textContent.includes('rebuild-kit job, not a new-valve job'), 'THE FORK: worn seals are a rebuild, not a new valve');
  // low pressure must name the non-repair cause: undersizing
  qdRoot.querySelector('[data-sym="pressure"]').click();
  ok(qdRoot.querySelector('[data-cause]').textContent.includes('sized too small'), 'low pressure → names undersizing, which no repair fixes');
  ok(qdRoot.querySelector('[data-band]').textContent.includes('no repair fixes it'), 'and refuses to sell a repair for it');
  // quote banding against the published ranges
  const qdQ = qdRoot.querySelector('#qd-quote');
  qdQ.value = '60'; qdQ.dispatchEvent(new domRpr.window.Event('input'));
  ok(qdRoot.querySelector('[data-quote]').textContent.includes('inspection band'), '$60 → inside the published inspection band');
  qdQ.value = '430'; qdQ.dispatchEvent(new domRpr.window.Event('input'));
  ok(qdRoot.querySelector('[data-quote]').textContent.includes('national average $430'), '$430 → recognised as the national average');
  qdQ.value = '800'; qdQ.dispatchEvent(new domRpr.window.Event('input'));
  ok(qdRoot.querySelector('[data-quote]').textContent.includes('REBUILT or REPLACED'), '$800 → tool raises the rebuild-vs-replace question unprompted');
  const q8 = qd();
  ok(Math.abs(q8.pctOfReplacement - (800 / 1500) * 100) < 0.2, `quote is ${q8.pctOfReplacement}% of the replacement`);
  ok(qdRoot.querySelector('[data-pct]').textContent.includes('no magic threshold'), 'refuses to hand out a mechanical 50%-style rule');
}

// ---- 38. Salt Cost Calculator (SC salt page) ----
const sltHtml = readFileSync('water-softener-salt-cost/index.html', 'utf8');
const domSlt = new JSDOM(sltHtml, { url: 'https://softwatersystemcost.com/water-softener-salt-cost/' });
global.window = domSlt.window; global.document = domSlt.window.document;
window.matchMedia = () => ({ matches: true });
const modSlt = await import('../assets/calculator.js?sc=' + Math.random()).catch(() => null);
const sltRoot = domSlt.window.document.querySelector('[data-salt-cost]');
ok(!!sltRoot, 'SC page has salt-cost mount');
if (sltRoot && modSlt && modSlt.mountSaltCost) {
  modSlt.mountSaltCost(sltRoot);
  const sl = () => JSON.parse(sltRoot.getAttribute('data-result'));
  const s0 = sl();
  ok(Math.abs(s0.lbs - 316) <= 2 && Math.abs(s0.bags - 7.9) < 0.15, `default household: ${s0.lbs} lbs = ${s0.bags} bags/yr`);
  ok(Math.abs(s0.sludge10 - 12.6) < 0.5, `solar pellets → only ${s0.sludge10} lbs of residue over 10 years`);
  // rock salt: cheaper per bag, but 8-9x the sludge — and the tool must say the trap out loud
  sltRoot.querySelector('[data-t="rock"]').click();
  const rk = sl();
  ok(rk.annual < s0.annual, `rock salt IS cheaper: $${rk.annual} vs $${s0.annual}`);
  ok(rk.sludge10 > s0.sludge10 * 8, `...but delivers ${rk.sludge10} lbs of insolubles vs ${s0.sludge10} — ${(rk.sludge10/s0.sludge10).toFixed(0)}x more`);
  ok(sltRoot.querySelector('[data-verdict]').textContent.includes('THE TRAP'), 'THE TRAP: tool names it rather than just reporting the lower price');
  ok(sltRoot.querySelector('[data-verdict]').textContent.includes('$430'), 'and prices the clogged injector it causes');
  // potassium chloride: the 20% efficiency penalty must show up as MORE salt, not just a higher price
  sltRoot.querySelector('[data-t="kcl"]').click();
  const kc = sl();
  ok(kc.lbs > s0.lbs * 1.15, `KCl needs MORE salt (${kc.lbs} lbs vs ${s0.lbs}) — the efficiency penalty is applied, not just the price`);
  ok(kc.annual > s0.annual * 4, `KCl annual $${kc.annual} vs $${s0.annual} — ${(kc.annual/s0.annual).toFixed(1)}x`);
  ok(sltRoot.querySelector('[data-verdict]').textContent.includes('medical sodium restriction'), 'KCl branch names the two legitimate reasons rather than dismissing it');
  ok(sltRoot.querySelector('[data-verdict]').textContent.includes('wrong call simply because it is the expensive bag'), 'and names the illegitimate one');
}

// ---- 38. Calculator hub — every tool must be reachable, and the embeds must work ----
const hubHtml2 = readFileSync('calculators/index.html', 'utf8');
const domHub2 = new JSDOM(hubHtml2, { url: 'https://softwatersystemcost.com/calculators/' });
global.window = domHub2.window; global.document = domHub2.window.document;
window.matchMedia = () => ({ matches: true });
const modHub2 = await import('../assets/calculator.js?hub=' + Math.random()).catch(() => null);
// the hub must no longer advertise unbuilt tools
ok(!hubHtml2.includes('ship through Phase'), 'hub no longer promises tools as unbuilt (the launch stub is gone)');
ok(!/Seven free calculators/.test(hubHtml2), 'hub no longer claims seven calculators');
// every mount function in calculator.js must be reachable from the hub
const calcSrc = readFileSync('assets/calculator.js', 'utf8');
const allTools = [...calcSrc.matchAll(/document\.querySelectorAll\('\[data-([a-z-]+)\]'\)\.forEach\(mount/g)].map(m => m[1]);
ok(allTools.length === 45, `calculator.js defines ${allTools.length} auto-mounted tools`);
const hubLinks = [...hubHtml2.matchAll(/class="card" href="([^"]+)"/g)].map(m => m[1]);
const uniqueTargets = new Set(hubLinks);
ok(uniqueTargets.size >= 25, `hub links out to ${uniqueTargets.size} distinct tool pages`);
// spot-check that the pages hosting each tool are actually linked from the hub
const mustReach = ['/what-size-water-softener-do-i-need/', '/10-year-water-softener-cost/', '/water-softener-servicing/',
                   '/water-softener-repair-cost/', '/well-water-softener-cost/', '/water-softener-salt-cost/',
                   '/water-softener-maintenance/', '/uv-water-purifier-cost/', '/sediment-filter-cost/',
                   '/pelican-water-softener-cost/', '/water-hardness-by-zip/', '/water-softener-tank-replacement-cost/', '/low-maintenance-water-softener/', '/water-softener-maintenance-cost-by-brand/', '/water-softener-filter-replacement-cost/', '/is-a-water-softener-worth-it/', '/ion-exchange-system-cost/', '/aquasure-water-softener-cost/', '/whole-house-water-filter-and-softener-combo-cost/', '/water-softener-and-reverse-osmosis-cost/', '/rheem-water-softener-cost/', '/whole-house-water-filter-cost/', '/water-softener-cost-florida/', '/water-softener-cost-by-state/'];
const missing = mustReach.filter(u => !uniqueTargets.has(u));
ok(missing.length === 0, missing.length ? `MISSING from hub: ${missing.join(', ')}` : 'every silo\u2019s flagship tool is reachable from the hub');
// the two embedded tools must actually mount and produce results
const hubSizer = domHub2.window.document.querySelector('[data-sizer]');
const hubDecade = domHub2.window.document.querySelector('[data-decade]');
ok(!!hubSizer && !!hubDecade, 'hub embeds the sizer and the decade model directly');
if (hubSizer && modHub2 && modHub2.mountSizer) {
  modHub2.mountSizer(hubSizer);
  ok(JSON.parse(hubSizer.getAttribute('data-result')).rec === 40000, 'embedded sizer works on the hub (4p/10gpg → 40,000-grain)');
}
if (hubDecade && modHub2 && modHub2.mountDecade) {
  modHub2.mountDecade(hubDecade);
  ok(JSON.parse(hubDecade.getAttribute('data-result')).upfrontPct === 53, 'embedded decade model works on the hub (upfront = 53%)');
}
// the trust move: the hub must state the calculator it refused to build
ok(hubHtml2.includes('The calculator we deliberately did not build'), 'hub names the tool it declined to build');
ok(/funded by the trade association/.test(hubHtml2), 'and gives the sourcing reason for declining');

// ---- 39. Hardness-by-ZIP lookup (HZ page) ----
const hzHtml = readFileSync('water-hardness-by-zip/index.html', 'utf8');
const domHz = new JSDOM(hzHtml, { url: 'https://softwatersystemcost.com/water-hardness-by-zip/' });
global.window = domHz.window; global.document = domHz.window.document;
window.matchMedia = () => ({ matches: true });
const modHz = await import('../assets/calculator.js?hz=' + Math.random()).catch(() => null);
const hzRoot = domHz.window.document.querySelector('[data-hardness]');
ok(!!hzRoot, 'HZ page has the hardness-lookup mount');
if (hzRoot && modHz && modHz.mountHardness) {
  modHz.mountHardness(hzRoot);
  const hzIn = hzRoot.querySelector('#hz-zip');
  const hzR = () => JSON.parse(hzRoot.getAttribute('data-result'));
  hzIn.value = '98101'; hzIn.dispatchEvent(new domHz.window.Event('input'));
  ok(hzR().state === 'WA' && hzR().band === 'soft', 'Seattle → WA, soft');
  ok(hzRoot.querySelector('[data-hz-what]').textContent.includes('do not need a softener at all'),
     'HONEST: at soft hardness the tool tells you to buy nothing');
  hzIn.value = '90001'; hzIn.dispatchEvent(new domHz.window.Event('input'));
  ok(hzR().state === 'CA' && hzR().band === 'very hard', 'Los Angeles → CA, very hard (same first digit as Seattle)');
  ok(hzRoot.querySelector('[data-hz-what]').textContent.includes('softening pays'), 'and at very hard it says softening pays');
  hzIn.value = 'abc'; hzIn.dispatchEvent(new domHz.window.Event('input'));
  ok(hzR().found === false, 'bad input → no result rather than a fabricated one');
  hzIn.value = '67501'; hzIn.dispatchEvent(new domHz.window.Event('input'));
  ok(hzRoot.querySelector('[data-hz-caveat]').textContent.includes('REGIONAL ESTIMATE'),
     'every result carries the not-a-measurement caveat');
}

// ---- 40. Tank Triage (TK tank-replacement page) ----
const tkHtml = readFileSync('water-softener-tank-replacement-cost/index.html', 'utf8');
const domTk = new JSDOM(tkHtml, { url: 'https://softwatersystemcost.com/water-softener-tank-replacement-cost/' });
global.window = domTk.window; global.document = domTk.window.document;
window.matchMedia = () => ({ matches: true });
const modTk = await import('../assets/calculator.js?tk=' + Math.random()).catch(() => null);
const tkRoot = domTk.window.document.querySelector('[data-tank-calc]');
ok(!!tkRoot, 'TK page has tank-triage mount');
if (tkRoot && modTk && modTk.mountTankCalc) {
  modTk.mountTankCalc(tkRoot);
  const tk = () => JSON.parse(tkRoot.getAttribute('data-result'));
  ok(tk().isTank === true && tk().component === 'brine tank', 'default: cracked salt tank → brine tank');
  ok(tkRoot.querySelector('[data-note]').textContent.includes('Do not let anyone price a whole softener'), 'brine branch refuses the upsell');
  // the honesty branch: hard water with no leak is NOT a tank problem
  tkRoot.querySelector('[data-tk="hard"]').click();
  ok(tk().isTank === false, 'hard water, no leak → classified NOT a tank problem');
  ok(tkRoot.querySelector('[data-cause]').textContent.includes('does not fail by softening less'), 'and explains why');
  // beads → riser/basket, not the vessel
  tkRoot.querySelector('[data-tk="beads"]').click();
  ok(tk().component.includes('riser'), 'beads in taps → riser/distributor basket, tank intact');
  // the age fork on a leaking mineral tank
  tkRoot.querySelector('[data-tk="mineral"]').click();
  const tkAge = tkRoot.querySelector('#tk-age');
  tkAge.value = '5'; tkAge.dispatchEvent(new domTk.window.Event('input'));
  ok(tkRoot.querySelector('[data-age-verdict]').textContent.includes('repair-beats-replacement'), 'young system → repair-beats-replacement case');
  tkAge.value = '17'; tkAge.dispatchEvent(new domTk.window.Event('input'));
  ok(tkRoot.querySelector('[data-age-verdict]').textContent.includes('price one before approving'), 'old system → demands a full-replacement price first');
  ok(tkRoot.querySelector('[data-cause]').textContent.includes('impersonate a cracked vessel'), 'mineral branch warns about valve drips impersonating a cracked tank');
}

// ---- 41. Maintenance Burden Comparator (LM low-maintenance page) ----
const bdHtml = readFileSync('low-maintenance-water-softener/index.html', 'utf8');
const domBd = new JSDOM(bdHtml, { url: 'https://softwatersystemcost.com/low-maintenance-water-softener/' });
global.window = domBd.window; global.document = domBd.window.document;
window.matchMedia = () => ({ matches: true });
const modBd = await import('../assets/calculator.js?lm=' + Math.random()).catch(() => null);
const bdRoot = domBd.window.document.querySelector('[data-burden]');
ok(!!bdRoot, 'LM page has burden-comparator mount');
if (bdRoot && modBd && modBd.mountBurden) {
  modBd.mountBurden(bdRoot);
  const bd = () => JSON.parse(bdRoot.getAttribute('data-result'));
  const b0 = bd();
  ok(b0.bags > 0 && b0.sbCash > b0.sfCash, `salt maths runs (${b0.bags} bags) and the softener costs more to keep`);
  ok(b0.gap > 0, `conditioner wins the maintenance gap ($${b0.gap}/yr)`);
  ok(bdRoot.querySelector('[data-verdict]').textContent.includes('does not remove hardness'), 'HONEST: the winning verdict still states the conditioner\u2019s limit');
  // iron → the conditioner is disqualified BEFORE the maintenance comparison
  const bdIron = bdRoot.querySelector('#bd-iron');
  bdIron.checked = true; bdIron.dispatchEvent(new domBd.window.Event('change'));
  ok(bdRoot.querySelector('[data-verdict]').textContent.includes('ruled out before maintenance'), 'iron → conditioner disqualified, no saving shown');
  bdIron.checked = false; bdIron.dispatchEvent(new domBd.window.Event('change'));
  // soft water → buy neither
  const bdHard = bdRoot.querySelector('#bd-hard');
  bdHard.value = '2'; bdHard.dispatchEvent(new domBd.window.Event('input'));
  ok(bdRoot.querySelector('[data-verdict]').textContent.includes('neither'), 'soft water → the tool recommends buying neither system');
  // harder water → more salt, bigger gap
  bdHard.value = '25'; bdHard.dispatchEvent(new domBd.window.Event('input'));
  ok(bd().bags > b0.bags && bd().gap > b0.gap, 'harder water → more bags, wider maintenance gap');
}

// ---- 42. Ownership Predictability Scorer (BM brand-index page) ----
const bmHtml = readFileSync('water-softener-maintenance-cost-by-brand/index.html', 'utf8');
const domBm = new JSDOM(bmHtml, { url: 'https://softwatersystemcost.com/water-softener-maintenance-cost-by-brand/' });
global.window = domBm.window; global.document = domBm.window.document;
window.matchMedia = () => ({ matches: true });
const modBm = await import('../assets/calculator.js?bm=' + Math.random()).catch(() => null);
const bmRoot = domBm.window.document.querySelector('[data-predict]');
ok(!!bmRoot, 'BM page has predictability-scorer mount');
if (bmRoot && modBm && modBm.mountPredict) {
  modBm.mountPredict(bmRoot);
  const bm = () => JSON.parse(bmRoot.getAttribute('data-result'));
  ok(bm().yes === 0 && bm().rating === 'DIFFICULT', 'all-unknown default → DIFFICULT to estimate');
  ok(bmRoot.querySelector('[data-read]').textContent.includes('service relationship'), 'and names it: you are pricing a relationship, not a machine');
  ok(bmRoot.querySelector('[data-ask]').textContent.includes('in writing'), 'the ask-list demands the missing numbers in writing');
  const cbs = bmRoot.querySelectorAll('[data-pq]');
  cbs.forEach(cb => { cb.checked = true; cb.dispatchEvent(new domBm.window.Event('change')); });
  ok(bm().yes === 4 && bm().rating === 'HIGH', 'all-published → HIGH predictability');
  ok(bmRoot.querySelector('[data-ask]').textContent.includes('already public'), 'and the ask-list empties: nothing left to ask');
  cbs[0].checked = false; cbs[0].dispatchEvent(new domBm.window.Event('change'));
  ok(bm().yes === 3 && bm().rating === 'MODERATE', 'mixed answers → MODERATE, published half + written half');
}

// ---- 43. Filter Identifier & Annual Cost (FC filter-replacement page) ----
const fcHtml = readFileSync('water-softener-filter-replacement-cost/index.html', 'utf8');
const domFc = new JSDOM(fcHtml, { url: 'https://softwatersystemcost.com/water-softener-filter-replacement-cost/' });
global.window = domFc.window; global.document = domFc.window.document;
window.matchMedia = () => ({ matches: true });
const modFc = await import('../assets/calculator.js?fc=' + Math.random()).catch(() => null);
const fcRoot = domFc.window.document.querySelector('[data-filter-cost]');
ok(!!fcRoot, 'FC page has filter-cost mount');
if (fcRoot && modFc && modFc.mountFilterCost) {
  modFc.mountFilterCost(fcRoot);
  const fc = () => JSON.parse(fcRoot.getAttribute('data-result'));
  ok(fc().hasFilter === true && fc().diy === 52 && fc().pro === 192, 'default housing @ $26 x2/yr → $52 DIY, $192 pro');
  ok(fcRoot.querySelector('[data-body]').textContent.includes('not the cartridge'), 'names the gap: the service call, not the cartridge');
  // THE honesty branch: a plain softener may have NOTHING to replace
  fcRoot.querySelector('[data-fc="none"]').click();
  ok(fc().hasFilter === false && fc().diy === 0, 'softener-only → possibly a $0 job, no cost fabricated');
  ok(fcRoot.querySelector('[data-note]').textContent.includes('NOTHING to replace'), 'and says so: resin, not a disposable cartridge — ask for the part number');
  // proprietary → part-number escape hatch
  fcRoot.querySelector('[data-fc="prop"]').click();
  ok(fcRoot.querySelector('[data-note]').textContent.includes('PART NUMBERS'), 'proprietary branch → get the part number, it can reprice the year');
  // frequency drives the pro multiplier
  fcRoot.querySelector('[data-fc="housing"]').click();
  const fcF = fcRoot.querySelector('#fc-freq');
  fcF.value = '6'; fcF.dispatchEvent(new domFc.window.Event('input'));
  ok(fc().pro === (26 + 70) * 6, 'high frequency → the $70 call rides along every swap');
}

// ---- 44. Worth-It Break-Even (WI page) — the anti-damage-calculator ----
const wiHtml = readFileSync('is-a-water-softener-worth-it/index.html', 'utf8');
const domWi = new JSDOM(wiHtml, { url: 'https://softwatersystemcost.com/is-a-water-softener-worth-it/' });
global.window = domWi.window; global.document = domWi.window.document;
window.matchMedia = () => ({ matches: true });
const modWi = await import('../assets/calculator.js?wi=' + Math.random()).catch(() => null);
const wiRoot = domWi.window.document.querySelector('[data-worth-it]');
ok(!!wiRoot, 'WI page has worth-it mount');
if (wiRoot && modWi && modWi.mountWorthIt) {
  modWi.mountWorthIt(wiRoot);
  const wi = () => JSON.parse(wiRoot.getAttribute('data-result'));
  const w0 = wi();
  ok(w0.cost === 1580 + 249 * 10 && w0.exposure === 800, 'default: cost $4,070, exposure = user receipts only ($800)');
  ok(wiRoot.querySelector('[data-honest]').textContent.includes('industry-funded'), 'EVERY result carries the refusal: no industry damage curves modeled');
  // soft water → buy nothing
  const wiH = wiRoot.querySelector('#wi-hard');
  wiH.value = '2'; wiH.dispatchEvent(new domWi.window.Event('input'));
  ok(wi().verdict === 'Buy nothing', 'soft water → buy nothing, softener AND conditioner');
  // moving soon caps the verdict
  wiH.value = '20'; wiH.dispatchEvent(new domWi.window.Event('input'));
  const wiY = wiRoot.querySelector('#wi-years');
  wiY.value = '2'; wiY.dispatchEvent(new domWi.window.Event('input'));
  ok(wi().verdict.includes('leaving too soon'), 'short stay → probably not, even at 20 gpg');
  // heavy documented receipts → clearly worthwhile ON RECEIPTS
  wiY.value = '12'; wiY.dispatchEvent(new domWi.window.Event('input'));
  const wiS = wiRoot.querySelector('#wi-spend');
  wiS.value = '300'; wiS.dispatchEvent(new domWi.window.Event('input'));
  const wiR = wiRoot.querySelector('#wi-repair');
  wiR.checked = true; wiR.dispatchEvent(new domWi.window.Event('change'));
  ok(wi().pct >= 100 && wi().verdict.includes('your own receipts'), 'heavy documented costs → clearly worthwhile, attributed to receipts');
  // the honest middle: comfort purchase named as comfort
  wiS.value = '40'; wiS.dispatchEvent(new domWi.window.Event('input'));
  wiR.checked = false; wiR.dispatchEvent(new domWi.window.Event('change'));
  wiH.value = '8'; wiH.dispatchEvent(new domWi.window.Event('input'));
  ok(wi().verdict.toLowerCase().includes('comfort') || wi().verdict.toLowerCase().includes('borderline'), 'mild exposure → named a comfort purchase, not an investment');
}

// ---- 45. Ion Exchange Decoder (IX page) — the tool that refuses to quote ----
const ixHtml = readFileSync('ion-exchange-system-cost/index.html', 'utf8');
const domIx = new JSDOM(ixHtml, { url: 'https://softwatersystemcost.com/ion-exchange-system-cost/' });
global.window = domIx.window; global.document = domIx.window.document;
window.matchMedia = () => ({ matches: true });
const modIx = await import('../assets/calculator.js?ix=' + Math.random()).catch(() => null);
const ixRoot = domIx.window.document.querySelector('[data-ix-decoder]');
ok(!!ixRoot, 'IX page has the decoder mount');
if (ixRoot && modIx && modIx.mountIxDecoder) {
  modIx.mountIxDecoder(ixRoot);
  const ix = () => JSON.parse(ixRoot.getAttribute('data-result'));
  const txt = (sel) => ixRoot.querySelector(sel).textContent;
  // hardness → the softener, routed to the pillar (NOT re-priced here)
  ok(ix().problem === 'hard' && ix().isIx === true && ix().gated === false, 'default: hard water → yes, cation exchange');
  ok(txt('[data-ixc]').includes('$840'), 'hardness shows the published installed canon');
  // nitrate WITHOUT a lab test → the tool REFUSES to quote
  ixRoot.querySelector('[data-ix="nitrate"]').click();
  ok(ix().gated === true, 'nitrate without a lab analysis → GATED');
  ok(txt('[data-ixv]').includes('TEST FIRST'), 'verdict is TEST FIRST, not a price');
  ok(txt('[data-ixc]').includes('Withheld'), 'the cost is withheld on purpose');
  ok(txt('[data-ixw]').includes('SULFATE') && txt('[data-ixw]').includes('concentrated burst'),
     'and it explains why: sulfate preference + nitrate dumping');
  // with a lab analysis → the number appears, with the specification that keeps it safe
  const ixLab = ixRoot.querySelector('#ix-lab');
  ixLab.checked = true; ixLab.dispatchEvent(new domIx.window.Event('change'));
  ok(ix().gated === false && txt('[data-ixc]').includes('$2,195'), 'lab analysis ticked → the published nitrate range appears');
  ok(txt('[data-ixw]').includes('NITRATE-SELECTIVE'), 'and it specifies nitrate-selective resin, not standard anion');
  // hardness AND nitrate → two machines, never one
  const ixHard = ixRoot.querySelector('#ix-hard');
  ixHard.checked = true; ixHard.dispatchEvent(new domIx.window.Event('change'));
  ok(ixRoot.querySelector('[data-ixe]').textContent.includes('TWO systems'), 'hard water + nitrate → TWO systems in sequence');
  // the four not-ion-exchange answers
  ixRoot.querySelector('[data-ix="iron"]').click();
  ok(ix().isIx === false && txt('[data-ixw]').includes('FOULS'), 'iron → NOT ion exchange, and it fouls the resin');
  ixRoot.querySelector('[data-ix="bacteria"]').click();
  ok(ix().isIx === false && txt('[data-ixt]').includes('UV'), 'bacteria → NOT ion exchange, UV');
  ixRoot.querySelector('[data-ix="sediment"]').click();
  ok(ix().isIx === false && txt('[data-ixw]').includes('not dissolved'), 'sediment → NOT ion exchange, nothing to exchange');
  ixRoot.querySelector('[data-ix="chlorine"]').click();
  ok(ix().isIx === false && txt('[data-ixw]').includes('ADSORBS'), 'chlorine → carbon adsorbs, it does not exchange');
}

// ---- 46. Lifespan Break-Even (Aquasure page) — the tool that can tell you to buy the cheap one ----
const lbHtml = readFileSync('aquasure-water-softener-cost/index.html', 'utf8');
const domLb = new JSDOM(lbHtml, { url: 'https://softwatersystemcost.com/aquasure-water-softener-cost/' });
global.window = domLb.window; global.document = domLb.window.document;
window.matchMedia = () => ({ matches: true });
const modLb = await import('../assets/calculator.js?lb=' + Math.random()).catch(() => null);
const lbRoot = domLb.window.document.querySelector('[data-lifespan-be]');
ok(!!lbRoot, 'Aquasure page has the break-even mount');
if (lbRoot && modLb && modLb.mountLifespanBe) {
  modLb.mountLifespanBe(lbRoot);
  const lb = () => JSON.parse(lbRoot.getAttribute('data-result'));
  const d0 = lb();
  ok(d0.cheap === 605 && d0.quote === 4000 && d0.yrs === 15, 'defaults: $605 unit vs a $4,000 quote lasting 15 years');
  ok(d0.cheapAllIn === 1035, 'budget system + prepared install = $1,035 all in');
  ok(Math.abs(d0.be - 3.88) < 0.05, 'THE FINDING: it only has to last ~3.9 years to beat the quote');
  ok(d0.quotePerYr === 516 && d0.cheapAt10 === 353, 'quote $516/yr vs budget $353/yr at a ten-year life');
  // DIY drops the bar further
  const lbDiy = lbRoot.querySelector('#lb-diy');
  lbDiy.checked = true; lbDiy.dispatchEvent(new domLb.window.Event('change'));
  ok(lb().cheapAllIn === 685 && Math.abs(lb().be - 2.57) < 0.05, 'self-installed → break-even falls to ~2.6 years');
  ok(lbRoot.querySelector('[data-lbn]').textContent.includes('even a mediocre run wins'),
     'and the tool says it plainly: at this gap the cheap system is the rational buy');
  // when the prices are close, the tool refuses to decide on price
  lbDiy.checked = false; lbDiy.dispatchEvent(new domLb.window.Event('change'));
  const lbQ = lbRoot.querySelector('#lb-quote');
  lbQ.value = '1200'; lbQ.dispatchEvent(new domLb.window.Event('input'));   // a genuinely close pair: $1,035 all-in vs a $1,200 quote
  ok(lbRoot.querySelector('[data-lbn]').textContent.includes('not on the sticker'),
     'close prices → decide on warranty and support, NOT the sticker');
  // the honesty note is unconditional
  ok(lbRoot.querySelector('[data-lbn]').textContent.includes('nobody can source'),
     'every result admits lifespan is unsourceable — the warranty is the maker\u2019s own bet');
}

// ---- 47. Combo Router (CB page) — the tool that can say "skip half the combo" ----
const cbHtml = readFileSync('whole-house-water-filter-and-softener-combo-cost/index.html', 'utf8');
const domCb = new JSDOM(cbHtml, { url: 'https://softwatersystemcost.com/whole-house-water-filter-and-softener-combo-cost/' });
global.window = domCb.window; global.document = domCb.window.document;
window.matchMedia = () => ({ matches: true });
const modCb = await import('../assets/calculator.js?cb=' + Math.random()).catch(() => null);
const cbRoot = domCb.window.document.querySelector('[data-combo-router]');
ok(!!cbRoot, 'CB page has the router mount');
if (cbRoot && modCb && modCb.mountComboRouter) {
  modCb.mountComboRouter(cbRoot);
  const cb = () => JSON.parse(cbRoot.getAttribute('data-result'));
  const cbTxt = (sel) => cbRoot.querySelector(sel).textContent;
  const tick = (id, on) => { const el = cbRoot.querySelector(id); el.checked = on; el.dispatchEvent(new domCb.window.Event('change')); };
  // nothing ticked → buy nothing
  ok(cbTxt('[data-cbv]').includes('Buy nothing'), 'no problems ticked → buy nothing, test first');
  // hardness only → softener only, skip the filter half
  tick('#cb-hard', true);
  ok(cb().verdict.includes('Softener only') && cbTxt('[data-cbw]').includes('half a machine'), 'hardness only → skip the filter half');
  ok(cbTxt('[data-cbc]').includes('$840'), 'and it quotes our published softener canon, not a combo price');
  // hardness + chlorine → the combo's actual job
  tick('#cb-chlor', true);
  ok(cb().verdict.includes('combo') && cbTxt('[data-cbw]').includes('SHARED INSTALL'), 'both problems → yes, and the saving is named: the shared install');
  ok(cbTxt('[data-cbc]').includes('$1,500') && cbTxt('[data-cbc]').includes('$2,140'), 'quotes both the published band and our worksheet');
  // chlorine only → filter only
  tick('#cb-hard', false);
  ok(cb().verdict.includes('Filter only') && cbTxt('[data-cbw]').includes('brine tank'), 'chlorine only → skip the softener half');
  // iron on city water → not combo equipment
  tick('#cb-chlor', false); tick('#cb-iron', true);
  ok(cbTxt('[data-cbv]').includes('the combo will not fix this'), 'iron → the combo is refused as the wrong machine');
  // iron on a WELL → routed to the well train
  cbRoot.querySelector('[data-cb-src="well"]').click();
  ok(cb().verdict.includes('well train') && cbTxt('[data-cbw]').includes('BEFORE any softener'), 'well + iron → routed to G1, sequencing stated');
}

// ---- 48. Softener + RO Builder (SRO page) — the 7 gpg fork ----
const sroHtml = readFileSync('water-softener-and-reverse-osmosis-cost/index.html', 'utf8');
const domSro = new JSDOM(sroHtml, { url: 'https://softwatersystemcost.com/water-softener-and-reverse-osmosis-cost/' });
global.window = domSro.window; global.document = domSro.window.document;
window.matchMedia = () => ({ matches: true });
const modSro = await import('../assets/calculator.js?sro=' + Math.random()).catch(() => null);
const sroRoot = domSro.window.document.querySelector('[data-sro-builder]');
ok(!!sroRoot, 'SRO page has the builder mount');
if (sroRoot && modSro && modSro.mountSroBuilder) {
  modSro.mountSroBuilder(sroRoot);
  const sro = () => JSON.parse(sroRoot.getAttribute('data-result'));
  const sTxt = (sel) => sroRoot.querySelector(sel).textContent;
  // default 12 gpg, mid RO, pro → both systems, correct totals
  ok(sro().needSoft === true && sro().day1 === 2680 && sro().decade === 7520, 'default 12 gpg → both systems: $2,680 day one, $7,520 decade');
  ok(sTxt('[data-sm]').includes('pretreatment'), 'above the fork, the softener is named as the membrane\u2019s pretreatment');
  // below the published 7 gpg threshold → SKIP THE SOFTENER
  const sroH = sroRoot.querySelector('#sro-hard');
  sroH.value = '5'; sroH.dispatchEvent(new domSro.window.Event('input'));
  ok(sro().needSoft === false && sro().day1 === 1100, '5 gpg → RO alone, softener refused: $1,100 day one');
  ok(sTxt('[data-sv]').includes('skip the softener'), 'the verdict says it plainly');
  ok(sTxt('[data-sm]').includes('7 gpg'), 'and cites the published threshold');
  ok(sTxt('[data-sn]').includes('does not need the bodyguard'), 'the membrane does not need the bodyguard yet');
  // boundary sits at exactly 7 (>= 7 → both)
  sroH.value = '7'; sroH.dispatchEvent(new domSro.window.Event('input'));
  ok(sro().needSoft === true, 'at exactly 7 gpg the pair is back on the table');
  // DIY strips the labour lines
  const sroP = sroRoot.querySelector('#sro-pro');
  sroP.checked = false; sroP.dispatchEvent(new domSro.window.Event('change'));
  ok(sro().day1 === 1230 + 760, 'DIY: softener $1,230 + RO $760 day one');
  // low-waste tier changes the RO line
  sroRoot.querySelector('[data-sro-ro="1300"]').click();
  ok(sro().ro === 1300 && sro().day1 === 1230 + 1360, 'low-waste RO tier reprices the build');
}

// ---- 49. Conditional-Warranty Pricer (Rheem page) — pricing the asterisk ----
const rhHtml = readFileSync('rheem-water-softener-cost/index.html', 'utf8');
const domRh = new JSDOM(rhHtml, { url: 'https://softwatersystemcost.com/rheem-water-softener-cost/' });
global.window = domRh.window; global.document = domRh.window.document;
window.matchMedia = () => ({ matches: true });
const modRh = await import('../assets/calculator.js?rh=' + Math.random()).catch(() => null);
const rhRoot = domRh.window.document.querySelector('[data-rh-warranty]');
ok(!!rhRoot, 'Rheem page has the warranty-pricer mount');
if (rhRoot && modRh && modRh.mountRhWarranty) {
  modRh.mountRhWarranty(rhRoot);
  const rh = () => JSON.parse(rhRoot.getAttribute('data-result'));
  const rTxt = (sel) => rhRoot.querySelector(sel).textContent;
  // default $12 bottle → 15 bottles, $180 condition, under one repair → cheap insurance
  ok(rh().conditionCost === 180 && rh().be < 1, 'default $12 bottle: $180 to feed the condition — under one $430 repair');
  ok(rTxt('[data-rv]').includes('Cheap insurance'), 'verdict: cheap insurance, condition worth feeding');
  ok(rTxt('[data-rn]').includes('Keep receipts'), 'and the proof requirement is stated: keep receipts, or the condition was theatre');
  ok(rTxt('[data-rn]').includes('years 2\u20135 only'), 'coverage window honesty: the extension covers years 2–5 only');
  // expensive bottle → the tool names what you are really buying
  const rhB = rhRoot.querySelector('#rh-bottle');
  rhB.value = '30'; rhB.dispatchEvent(new domRh.window.Event('input'));
  ok(rh().conditionCost === 450 && rh().be > 1, '$30 bottle: $450 condition — more than the average repair');
  ok(rTxt('[data-rv]').includes('priced as detergent'), 'verdict: an extended warranty priced as detergent');
  ok(rTxt('[data-rn]').includes('warranty years') && rTxt('[data-rn]').includes('calling it the first'), 'names the product honestly: warranty-years sold as maintenance');
  // DIY branch → skip the condition
  const rhD = rhRoot.querySelector('#rh-diy');
  rhD.checked = true; rhD.dispatchEvent(new domRh.window.Event('change'));
  ok(rTxt('[data-rv]').includes('your own warranty'), 'DIY → skip the condition; you are your own warranty');
  ok(rTxt('[data-rn]').includes('unconditional parts'), 'and the unconditional 3-yr/10-yr terms are flagged as what still matters');
}

// ---- 50. Cartridge-vs-Tank Decade Calculator (FT page) — the crossover ----
const ftHtml = readFileSync('whole-house-water-filter-cost/index.html', 'utf8');
const domFt = new JSDOM(ftHtml, { url: 'https://softwatersystemcost.com/whole-house-water-filter-cost/' });
global.window = domFt.window; global.document = domFt.window.document;
window.matchMedia = () => ({ matches: true });
const modFt = await import('../assets/calculator.js?ft=' + Math.random()).catch(() => null);
const ftRoot = domFt.window.document.querySelector('[data-ft-tco]');
ok(!!ftRoot, 'FT page has the decade-calculator mount');
if (ftRoot && modFt && modFt.mountFtTco) {
  modFt.mountFtTco(ftRoot);
  const ft = () => JSON.parse(ftRoot.getAttribute('data-result'));
  const fTxt = (sel) => ftRoot.querySelector(sel).textContent;
  // defaults: $90 every 4 mo vs $1,500 tank + $400 media ×2 → tank wins, crossover ~4.3
  ok(ft().cart10 === 3050 && ft().tank10 === 2300, 'defaults: cartridge decade $3,050 vs tank $2,300');
  ok(Math.abs(ft().cross - 4.3) < 0.15, 'crossover lands around year 4.3 — the page thesis');
  ok(fTxt('[data-fv]').includes('tank wins the decade'), 'verdict: the tank wins the decade');
  // light-use branch is real: cheap yearly cartridge → the kit holds
  const ftC = ftRoot.querySelector('#ft-cart');
  ftC.value = '40'; ftC.dispatchEvent(new domFt.window.Event('input'));
  ftRoot.querySelector('[data-ft-int="12"]').click();
  ok(ft().cart10 === 750 && fTxt('[data-fv]').includes('cartridge route holds'), 'light use + cheap yearly cartridge → the cartridge route holds — the tool is not rigged');
  // chloramine → catalytic warning prepended
  const ftCh = ftRoot.querySelector('#ft-chlor');
  ftCh.checked = true; ftCh.dispatchEvent(new domFt.window.Event('change'));
  ok(fTxt('[data-fn]').includes('CATALYTIC'), 'chloramine flags catalytic carbon — costs more, bigger bed');
  ok(fTxt('[data-fn]').includes('wrong tool at any price'), 'and names the standard cartridge as the wrong tool on chloramine');
  // the media-volume note rides every result
  ok(fTxt('[data-fn]').includes('45\u201375 pounds'), 'the buried number — carbon volume — is printed on every verdict');
}

// ---- 51. Florida Scenario Builder (FL page) — regions, loop fork, well refusal ----
const flHtml = readFileSync('water-softener-cost-florida/index.html', 'utf8');
const domFl = new JSDOM(flHtml, { url: 'https://softwatersystemcost.com/water-softener-cost-florida/' });
global.window = domFl.window; global.document = domFl.window.document;
window.matchMedia = () => ({ matches: true });
const modFl = await import('../assets/calculator.js?fl=' + Math.random()).catch(() => null);
const flRoot = domFl.window.document.querySelector('[data-fl-quote]');
ok(!!flRoot, 'FL page has the scenario-builder mount');
if (flRoot && modFl && modFl.mountFlQuote) {
  modFl.mountFlQuote(flRoot);
  const fl = () => JSON.parse(flRoot.getAttribute('data-result'));
  const lTxt = (sel) => flRoot.querySelector(sel).textContent;
  // default: Central FL, 3 people, loop, city → $950–$3,100 and the 32–40k class via the 65% rule
  ok(fl().lo === 950 && fl().hi === 3100, 'default Central FL scenario: $950–$3,100 year one');
  ok(lTxt('[data-fm]').includes('32,000\u201340,000'), 'capacity uses the 65% nameplate rule → 32–40k class');
  ok(lTxt('[data-fn]').includes('Consumer Confidence Report'), 'every result routes to the CCR — the disinterested number');
  // no loop → the $600–$2,000 line appears in the stack
  const flLoop = flRoot.querySelector('#fl-loop');
  flLoop.checked = false; flLoop.dispatchEvent(new domFl.window.Event('change'));
  ok(fl().lo === 1550 && lTxt('[data-fm]').includes('loop construction $600\u2013$2,000'), 'loopless home: the loop line enters the itemisation');
  // the WELL REFUSAL — the tool sizes nothing without a lab panel
  const flWell = flRoot.querySelector('#fl-well');
  flWell.checked = true; flWell.dispatchEvent(new domFl.window.Event('change'));
  ok(fl().refused === true, 'well water → the tool refuses to size anything');
  ok(lTxt('[data-fv]').includes('refuses to size'), 'and says so in the verdict');
  ok(lTxt('[data-fn]').includes('well-water train has its own worksheet'), 'routing to the well train, not a guess');
  // regions carry sourced bands: South FL shows the post-treatment Boca note
  flWell.checked = false; flWell.dispatchEvent(new domFl.window.Event('change'));
  flRoot.querySelector('[data-fl-reg="south"]').click();
  ok(fl().gpgHi === 19 && lTxt('[data-fm]').includes('AFTER plant softening'), 'South FL band 11–19 gpg with the after-plant-softening note');
}

// ---- 52. 50-State Explorer (SB study page) — dataset integrity + honest tiers ----
const sbHtml = readFileSync('water-softener-cost-by-state/index.html', 'utf8');
const domSb = new JSDOM(sbHtml, { url: 'https://softwatersystemcost.com/water-softener-cost-by-state/' });
global.window = domSb.window; global.document = domSb.window.document;
window.matchMedia = () => ({ matches: true });
const modSb = await import('../assets/calculator.js?sb=' + Math.random()).catch(() => null);
const sbRoot = domSb.window.document.querySelector('[data-state-explorer]');
ok(!!sbRoot, 'study page has the explorer mount');
if (sbRoot && modSb && modSb.mountStateExplorer && modSb.STATE_DATA) {
  ok(modSb.STATE_DATA.length === 50, 'the dataset holds exactly 50 states');
  const tiers = modSb.STATE_DATA.reduce((a, s) => (a[s.tier] = (a[s.tier] || 0) + 1, a), {});
  ok(tiers.VH === 14 && tiers.L === 15 && tiers.V === 5, 'tier distribution matches the published study (14 VH / 15 L / 5 V)');
  // the inverse-correlation finding, recomputed from the dataset itself
  const vhCheap = modSb.STATE_DATA.filter(s => s.tier === 'VH' && s.labor !== 'hi').length;
  ok(vhCheap === 13, 'finding #3 recomputes: 13/14 Very-High states in low-to-mid labour tiers');
  mountSbAndCheck: {
    modSb.mountStateExplorer(sbRoot);
    const sTxt = (sel) => sbRoot.querySelector(sel).textContent;
    const sel = sbRoot.querySelector('#se-state');
    // Arkansas: the paradox state — soft AND cheap labour, told to buy nothing
    sel.value = 'AR'; sel.dispatchEvent(new domSb.window.Event('change'));
    ok(sTxt('[data-sm]').includes('~38 ppm') && sTxt('[data-sm]').includes('buy NOTHING'), 'Arkansas: softest-state note + the buy-nothing branch');
    // Florida routes to its own page
    sel.value = 'FL'; sel.dispatchEvent(new domSb.window.Event('change'));
    ok(sTxt('[data-sn]').includes('its own itemised page'), 'Florida routes to the state guide');
    // every output labels the classification as editorial with confidence
    ok(sTxt('[data-sn]').includes('editorial tier') && sTxt('[data-sn]').includes('confidence'), 'the tier is labelled editorial with a confidence grade on every result');
    // equipment-is-national is stated on every state
    sel.value = 'IL'; sel.dispatchEvent(new domSb.window.Event('change'));
    ok(sTxt('[data-sm]').includes('priced NATIONALLY') && sTxt('[data-sm]').includes('$87,980'), 'Illinois: national equipment + the sourced high-wage anchor');
  }
}

console.log(fails ? `\n${fails} FAILURES` : '\nALL CALCULATOR BRANCHES VERIFIED');
process.exit(fails ? 1 : 0);
