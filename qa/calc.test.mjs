// jsdom verification of all calculator branches (portfolio QA protocol)
import { JSDOM } from 'jsdom';
import { readFileSync } from 'fs';
import { estimate, grainTier, hardnessForZip, fmtRange } from '../assets/calc-core.js';

let fails = 0;
const ok = (cond, msg) => { console.log((cond ? 'PASS' : 'FAIL') + ' ' + msg); if (!cond) fails++; };

// ---- 1. Cost model branches (pure) ----
const base = { people: 3, gpg: 12, type: 'salt', install: 'pro', hasLoop: true };
const e1 = estimate(base);
ok(e1.rows.length === 4 && e1.low === 800 && e1.high === 1900, `salt/pro/loop → ${e1.low}-${e1.high} (exp 800-1900)`);
const e2 = estimate({ ...base, hasLoop: false });
ok(e2.low === 1400 && e2.high === 3900, `no-loop adds 600-2000 → ${e2.low}-${e2.high}`);
const e3 = estimate({ ...base, type: 'saltfree' });
ok(e3.rows.some(r => r.item.includes('conditioner')) && !e3.rows.some(r => r.item.includes('salt')), 'saltfree drops salt row');
const e4 = estimate({ ...base, install: 'diy' });
ok(e4.rows.some(r => r.item.includes('DIY')) && !e4.rows.some(r => r.item.includes('labor')), 'diy swaps labor rows');
ok(grainTier(1, 5) === 24 && grainTier(4, 12) === 32 && grainTier(5, 14) === 48 && grainTier(6, 20) === 64, 'grain tiers: 24/32/48/64');
ok(hardnessForZip('90210') === 10 && hardnessForZip('123') === null && hardnessForZip('abcde') === null, 'ZIP lookup validates 5 digits');
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
ok(result0.low === 1400 && result0.high === 3900, `initial data-result ${result0.low}-${result0.high} (default no-loop)`);

// toggle loop=yes → totals drop by 600-2000
const loopYes = [...root.querySelectorAll('.seg button')].find(b => b.textContent === 'Yes');
loopYes.click();
const r1 = JSON.parse(root.getAttribute('data-result'));
ok(r1.low === 800 && r1.high === 1900, `loop toggle updates data-result → ${r1.low}-${r1.high}`);
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

console.log(fails ? `\n${fails} FAILURES` : '\nALL CALCULATOR BRANCHES VERIFIED');
process.exit(fails ? 1 : 0);
