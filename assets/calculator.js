// calculator.js — Cost Calculator UI (vanilla, no framework)
// Mounts on any element with [data-calc]. Variants: data-variant="full" | "embed".
// Exposes live state on data-result for the jsdom QA harness (spec §4.5).
import { estimate, hardnessForZip, hardnessDetailForZip, fmtRange, countUp } from './calc-core.js?v=171';

function h(tag, cls, html) {
  const el = document.createElement(tag);
  if (cls) el.className = cls;
  if (html !== undefined) el.innerHTML = html;
  return el;
}

function segButton(label, pressed, onPress) {
  const b = h('button', null, label);
  b.type = 'button';
  b.setAttribute('aria-pressed', pressed ? 'true' : 'false');
  b.addEventListener('click', onPress);
  return b;
}

export function mountCalculator(root) {
  const variant = root.getAttribute('data-variant') || 'full';
  const state = { people: 3, gpg: 12, type: 'salt', install: 'pro', hasLoop: variant === 'embed', zip: '' };
  let cancelCount = () => {};

  root.classList.add('calc');
  if (variant === 'embed') root.classList.add('embed');

  // ---- inputs panel ----
  const inputs = h('div', 'inputs');

  const peopleWrap = h('div');
  peopleWrap.appendChild(h('label', null, 'How many people live in your home?')).setAttribute('for', 'calc-people');
  const pRow = h('div', 'slider-row');
  const pInput = h('input'); pInput.type = 'range'; pInput.min = '1'; pInput.max = '8'; pInput.step = '1'; pInput.value = String(state.people); pInput.id = 'calc-people';
  const pVal = h('span', 'slider-val', String(state.people));
  pRow.append(pInput, pVal); peopleWrap.appendChild(pRow); inputs.appendChild(peopleWrap);

  const gpgWrap = h('div');
  gpgWrap.appendChild(h('label', null, 'Water hardness (grains per gallon)')).setAttribute('for', 'calc-gpg');
  gpgWrap.appendChild(h('div', 'helper', 'Hardness is on your water report \u2014 or use the ZIP lookup below.'));
  const gRow = h('div', 'slider-row');
  const gInput = h('input'); gInput.type = 'range'; gInput.min = '1'; gInput.max = '30'; gInput.step = '1'; gInput.value = String(state.gpg); gInput.id = 'calc-gpg';
  const gVal = h('span', 'slider-val', String(state.gpg));
  gRow.append(gInput, gVal); gpgWrap.appendChild(gRow);
  let zipNote;
  if (variant === 'full') {
    const zRow = h('div', 'zip-row');
    const zInput = h('input'); zInput.type = 'text'; zInput.inputMode = 'numeric'; zInput.maxLength = 5; zInput.placeholder = 'ZIP'; zInput.setAttribute('aria-label', 'ZIP code for hardness lookup');
    const zBtn = h('button', null, 'Look up'); zBtn.type = 'button';
    zRow.append(zInput, zBtn); gpgWrap.appendChild(zRow);
    zipNote = h('div', 'helper'); zipNote.style.marginTop = '4px'; gpgWrap.appendChild(zipNote);
    zInput.addEventListener('input', () => { zInput.value = zInput.value.replace(/[^0-9]/g, '').slice(0, 5); state.zip = zInput.value; });
    zBtn.addEventListener('click', () => {
      const g = hardnessForZip(state.zip);
      if (g) { state.gpg = g; gInput.value = String(g); gVal.textContent = String(g); zipNote.textContent = 'Average hardness near ' + state.zip + ': ' + g + ' gpg (set above)'; update(); }
      else zipNote.textContent = 'Enter a 5-digit ZIP to look up average hardness.';
    });
  }
  inputs.appendChild(gpgWrap);

  function segGroup(question, helper, pairs, key) {
    const wrap = h('div');
    wrap.appendChild(h('span', 'q', question));
    if (helper) wrap.appendChild(h('div', 'helper', helper));
    const seg = h('div', 'seg');
    seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', question);
    const btns = pairs.map(([label, value]) => {
      const b = segButton(label, state[key] === value, () => {
        state[key] = value;
        btns.forEach((bb, i) => bb.setAttribute('aria-pressed', pairs[i][1] === state[key] ? 'true' : 'false'));
        update();
      });
      seg.appendChild(b); return b;
    });
    wrap.appendChild(seg); inputs.appendChild(wrap);
  }
  segGroup('System type', null, [['Salt-based', 'salt'], ['Salt-free', 'saltfree']], 'type');
  segGroup("Who installs it?", null, [['A plumber', 'pro'], ["I'll DIY it", 'diy']], 'install');
  if (variant === 'full') {
    segGroup('Do you already have a softener loop?', 'A loop is pre-run plumbing near where the unit sits. Most homes built after 2000 have one.', [['Yes', true], ['No / not sure', false]], 'hasLoop');
  }

  // ---- results panel ----
  const results = h('div', 'results');
  const figWrap = h('div');
  const fig = h('div', 'result-fig'); fig.setAttribute('role', 'status'); fig.setAttribute('aria-live', 'polite');
  const sub = h('div', 'result-sub', variant === 'embed'
    ? 'typical installed cost for your inputs \u00b7 assumes an existing loop'
    : 'typical installed cost for your inputs');
  figWrap.append(fig, sub); results.appendChild(figWrap);

  let qsBody = null;
  if (variant === 'full') {
    const qs = h('div', 'quote-sheet');
    qs.innerHTML = '<div class="qs-head"><span class="qs-eyebrow">Quote Sheet</span><span class="qs-title" data-qs-title></span></div>'
      + '<table><caption>Live itemized estimate</caption><thead><tr><th scope="col">Item</th><th scope="col" class="num">Low</th><th scope="col" class="num">High</th></tr></thead><tbody data-qs-body></tbody></table>'
      + '<div class="qs-foot"><span class="stamp">Data updated \u00b7 Jul 2026</span><a href="#sources">Sources \u2193</a></div>';
    results.appendChild(qs);
    qsBody = qs.querySelector('[data-qs-body]');
    var qsTitle = qs.querySelector('[data-qs-title]');
    const meth = h('details', 'methodology');
    meth.innerHTML = '<summary>How this calculator works</summary><p>Sizing: people \u00d7 75 gal/day \u00d7 hardness \u00d7 7-day reserve \u2192 grain tier. Unit prices from 2026 retail surveys; labor and loop-run figures from Angi/HomeAdvisor national data. Full methodology in the <a href="#sources">sources</a>.</p>';
    results.appendChild(meth);
  }

  root.append(inputs, results);

  const fmtCell = (n) => '$' + Math.round(n).toLocaleString('en-US');
  let prev = estimate(state);

  function update() {
    const est = estimate(state);
    if (est.low !== prev.low || est.high !== prev.high) {
      cancelCount();
      cancelCount = countUp(prev.low, prev.high, est.low, est.high, (t) => { fig.textContent = t; });
    } else {
      fig.textContent = fmtRange(est.low, est.high);
    }
    if (qsBody) {
      qsBody.innerHTML = est.rows.map((r) =>
        '<tr><td>' + r.item + '</td><td class="num">' + fmtCell(r.low) + '</td><td class="num">' + fmtCell(r.high) + '</td></tr>'
      ).join('') + '<tr class="total"><td class="label">Total installed</td><td class="num">' + fmtCell(est.low) + '</td><td class="num">' + fmtCell(est.high) + '</td></tr>';
      qsTitle.textContent = (state.type === 'salt' ? 'Salt-Based Softener' : 'Salt-Free Conditioner') + ', ' + state.people + '-Person Home';
    }
    root.setAttribute('data-result', JSON.stringify({ low: est.low, high: est.high, inputs: { people: state.people, gpg: state.gpg, type: state.type, install: state.install, hasLoop: state.hasLoop } }));
    prev = est;
  }

  pInput.addEventListener('input', (e) => { state.people = +e.target.value; pVal.textContent = e.target.value; update(); });
  gInput.addEventListener('input', (e) => { state.gpg = +e.target.value; gVal.textContent = e.target.value; update(); });

  fig.textContent = fmtRange(prev.low, prev.high);
  update();
}

export function mountSaltCalc(root) {
  root.classList.add('mini-calc');
  root.innerHTML = '<div class="mc-grid">'
    + '<div><label for="mc-bags">Bags of salt per year</label><div class="slider-row"><input id="mc-bags" type="range" min="4" max="16" step="1" value="10"><span class="slider-val" data-bags>10</span></div></div>'
    + '<div><label for="mc-price">Price per 40-lb bag</label><div class="slider-row"><input id="mc-price" type="range" min="5" max="10" step="1" value="7"><span class="slider-val" data-price>$7</span></div></div>'
    + '</div><div class="mc-out">Salt cost: <span class="fig" data-yr></span>/year &middot; <span class="fig" data-ten></span> over 10 years</div>';
  const bags = root.querySelector('#mc-bags'), price = root.querySelector('#mc-price');
  const update = () => {
    const b = +bags.value, p = +price.value;
    root.querySelector('[data-bags]').textContent = String(b);
    root.querySelector('[data-price]').textContent = '$' + p;
    root.querySelector('[data-yr]').textContent = '$' + (b * p);
    root.querySelector('[data-ten]').textContent = '$' + (b * p * 10).toLocaleString('en-US');
    root.setAttribute('data-result', JSON.stringify({ bags: b, price: p, yearly: b * p, tenYear: b * p * 10 }));
  };
  bags.addEventListener('input', update);
  price.addEventListener('input', update);
  update();
}

export function mountInstallCalc(root) {
  root.classList.add('mini-calc');
  const SCEN = {
    prepared: { label: 'Prepared home (loop, drain, outlet exist)', low: 290, high: 770 },
    noloop:   { label: 'No softener loop', low: 890, high: 2770 },
    full:     { label: 'Full site work (loop + drain + outlet + permit)', low: 890, high: 4120 }
  };
  root.innerHTML = '<span class="q">What does your home already have?</span>'
    + '<div class="seg" role="group" aria-label="Install scenario">'
    + '<button type="button" data-k="prepared" aria-pressed="true">Prepared</button>'
    + '<button type="button" data-k="noloop" aria-pressed="false">No loop</button>'
    + '<button type="button" data-k="full" aria-pressed="false">Nothing yet</button>'
    + '</div>'
    + '<div class="mc-out"><span data-lbl></span><br>Install-only cost: <span class="fig" data-range style="font-size:22px"></span></div>';
  const btns = [...root.querySelectorAll('button')];
  const set = (k) => {
    const sc = SCEN[k];
    btns.forEach(b => b.setAttribute('aria-pressed', b.dataset.k === k ? 'true' : 'false'));
    root.querySelector('[data-lbl]').textContent = sc.label;
    root.querySelector('[data-range]').textContent = '$' + sc.low.toLocaleString() + ' \u2013 $' + sc.high.toLocaleString();
    root.setAttribute('data-result', JSON.stringify({ scenario: k, low: sc.low, high: sc.high }));
  };
  btns.forEach(b => b.addEventListener('click', () => set(b.dataset.k)));
  set('prepared');
}

export function mountQuoteCheck(root) {
  root.classList.add('mini-calc');
  // Bands configurable per brand page via data attributes; defaults = Culligan (first deployment)
  const min = +(root.dataset.min || 1500), max = +(root.dataset.max || 9000), start = +(root.dataset.start || 4500);
  let bands;
  try { bands = JSON.parse(root.dataset.bands); } catch (e) { bands = null; }
  if (!bands) bands = [
    { upTo: 2499, band: 'below-typical', text: 'Below the typical reported band ($2,500\u2013$4,500). Reasonable \u2014 confirm exactly what\u2019s included: model, capacity, install scope, warranty.' },
    { upTo: 4500, band: 'typical', text: 'Inside the typical reported band ($2,500\u2013$4,500 installed). Ask for the line items anyway \u2014 the itemization is where savings hide.' },
    { upTo: 6500, band: 'upper', text: 'Upper end of published ranges ($1,800\u2013$6,500 installed). Legitimate for twin-tank or well systems \u2014 otherwise ask what justifies the premium, in writing.' },
    { upTo: Infinity, band: 'above-published', text: 'Above every published range we track. Industry guides warn high-pressure quotes reach $6,000\u2013$8,000. Get a second quote before signing anything.' }
  ];
  root.innerHTML = '<label for="qc-amt">Your quoted price (installed)</label>'
    + '<div class="slider-row"><input id="qc-amt" type="range" min="' + min + '" max="' + max + '" step="100" value="' + start + '"><span class="slider-val" data-amt style="min-width:72px"></span></div>'
    + '<div class="mc-out" data-verdict aria-live="polite"></div>';
  const amt = root.querySelector('#qc-amt');
  const update = () => {
    const v = +amt.value;
    const r = bands.find(b => v <= (b.upTo === null ? Infinity : b.upTo)) || bands[bands.length - 1];
    root.querySelector('[data-amt]').textContent = '$' + v.toLocaleString('en-US');
    root.querySelector('[data-verdict]').textContent = r.text;
    root.setAttribute('data-result', JSON.stringify({ amount: v, band: r.band }));
  };
  amt.addEventListener('input', update);
  update();
}

export function mountChannelCalc(root) {
  root.classList.add('mini-calc');
  // factory-direct comparable: published unit $600-$1,500 (+quality tier to $2,700 w/ pro install) per cost-guide data
  const CMP_LOW = 1200, CMP_HIGH = 3200;
  root.innerHTML = '<label for="cc-amt">The dealer quote in front of you (installed)</label>'
    + '<div class="slider-row"><input id="cc-amt" type="range" min="3000" max="9000" step="100" value="5500"><span class="slider-val" data-amt style="min-width:72px">$5,500</span></div>'
    + '<div class="mc-out">Comparable factory-direct route: <span class="fig">$1,200 \u2013 $3,200</span> installed<br>'
    + 'Implied channel premium: <span class="fig" data-save style="font-size:22px"></span></div>';
  const amt = root.querySelector('#cc-amt');
  const update = () => {
    const v = +amt.value;
    const lo = Math.max(0, v - CMP_HIGH), hi = Math.max(0, v - CMP_LOW);
    root.querySelector('[data-amt]').textContent = '$' + v.toLocaleString('en-US');
    root.querySelector('[data-save]').textContent = '$' + lo.toLocaleString('en-US') + ' \u2013 $' + hi.toLocaleString('en-US');
    root.setAttribute('data-result', JSON.stringify({ quote: v, savingsLow: lo, savingsHigh: hi }));
  };
  amt.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-calc]').forEach(mountCalculator);
document.querySelectorAll('[data-salt-calc]').forEach(mountSaltCalc);
document.querySelectorAll('[data-install-calc]').forEach(mountInstallCalc);
document.querySelectorAll('[data-quote-check]').forEach(mountQuoteCheck);
export function mountExpenseCalc(root) {
  root.classList.add('mini-calc');
  // sourced component ranges (see page sources): equipment tiers, install, site work, channel remainder
  const TIERS = { budget: [600, 900], mid: [900, 1500], premium: [1500, 2700] };
  const INSTALL = { diy: [50, 150], pro: [200, 500] };
  const ADDONS = { loop: [600, 2000], site: [350, 1200], removal: [50, 150], dealer: [2110, 5730] };
  const state = { tier: 'mid', install: 'pro', loop: false, site: false, removal: false, dealer: false };
  root.innerHTML = '<span class="q">Build the quote: what does your project include?</span>'
    + '<div class="seg" role="group" aria-label="Equipment tier" style="margin-bottom:10px">'
    + '<button type="button" data-tier="budget">Budget unit</button>'
    + '<button type="button" data-tier="mid" aria-pressed="true">Mid-tier unit</button>'
    + '<button type="button" data-tier="premium">Premium unit</button></div>'
    + '<div class="seg" role="group" aria-label="Installation" style="margin-bottom:10px">'
    + '<button type="button" data-install="diy">DIY install</button>'
    + '<button type="button" data-install="pro" aria-pressed="true">Pro install</button></div>'
    + '<div class="seg" role="group" aria-label="Add-ons">'
    + '<button type="button" data-addon="loop" aria-pressed="false">+ No loop (cut one in)</button>'
    + '<button type="button" data-addon="site" aria-pressed="false">+ Drain &amp; outlet missing</button>'
    + '<button type="button" data-addon="removal" aria-pressed="false">+ Old unit removal</button>'
    + '<button type="button" data-addon="dealer" aria-pressed="false">+ Dealer sales channel</button></div>'
    + '<div class="stackbar" data-stack style="margin-top:14px"></div>'
    + '<div class="stack-legend" data-legend></div>'
    + '<div class="mc-out">Your quote builds to: <span class="fig" data-total style="font-size:22px"></span></div>';
  const COLORS = { equip: '#16303F', install: '#1F7A5C', loop: '#E8A13D', site: '#5B6B75', removal: '#8FA98F', dealer: '#B3541E' };
  const LABELS = { equip: 'Equipment', install: 'Install', loop: 'Loop run', site: 'Drain + outlet', removal: 'Removal', dealer: 'Sales channel' };
  const update = () => {
    const parts = [['equip', TIERS[state.tier]], ['install', INSTALL[state.install]]];
    if (state.loop) parts.push(['loop', ADDONS.loop]);
    if (state.site) parts.push(['site', ADDONS.site]);
    if (state.removal) parts.push(['removal', ADDONS.removal]);
    if (state.dealer) parts.push(['dealer', ADDONS.dealer]);
    const low = parts.reduce((a, p) => a + p[1][0], 0), high = parts.reduce((a, p) => a + p[1][1], 0);
    const mids = parts.map(p => (p[1][0] + p[1][1]) / 2), sum = mids.reduce((a, b) => a + b, 0);
    root.querySelector('[data-stack]').innerHTML = parts.map((p, i) =>
      '<div style="width:' + (mids[i] / sum * 100).toFixed(1) + '%;background:' + COLORS[p[0]] + '" title="' + LABELS[p[0]] + '"></div>').join('');
    root.querySelector('[data-legend]').innerHTML = parts.map(p =>
      '<span><span class="sw" style="background:' + COLORS[p[0]] + '"></span>' + LABELS[p[0]] + ' $' + p[1][0].toLocaleString() + '\u2013$' + p[1][1].toLocaleString() + '</span>').join('');
    root.querySelector('[data-total]').textContent = '$' + low.toLocaleString('en-US') + ' \u2013 $' + high.toLocaleString('en-US');
    root.setAttribute('data-result', JSON.stringify({ tier: state.tier, install: state.install, loop: state.loop, site: state.site, removal: state.removal, dealer: state.dealer, low, high }));
  };
  root.querySelectorAll('[data-tier]').forEach(b => b.addEventListener('click', () => {
    state.tier = b.dataset.tier;
    root.querySelectorAll('[data-tier]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  root.querySelectorAll('[data-install]').forEach(b => b.addEventListener('click', () => {
    state.install = b.dataset.install;
    root.querySelectorAll('[data-install]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  root.querySelectorAll('[data-addon]').forEach(b => b.addEventListener('click', () => {
    state[b.dataset.addon] = !state[b.dataset.addon];
    b.setAttribute('aria-pressed', state[b.dataset.addon] ? 'true' : 'false');
    update();
  }));
  update();
}

document.querySelectorAll('[data-channel-calc]').forEach(mountChannelCalc);
export function mountBudgetFit(root) {
  root.classList.add('mini-calc');
  const state = { hh: '34', hard: 'hard' };
  root.innerHTML = '<span class="q">Which budget tier actually fits your home?</span>'
    + '<div class="seg" role="group" aria-label="Household size" style="margin-bottom:10px">'
    + '<button type="button" data-hh="12">1\u20132 people</button>'
    + '<button type="button" data-hh="34" aria-pressed="true">3\u20134 people</button>'
    + '<button type="button" data-hh="5p">5+ people</button></div>'
    + '<div class="seg" role="group" aria-label="Water hardness">'
    + '<button type="button" data-hard="mod">Moderate (&lt;7 gpg)</button>'
    + '<button type="button" data-hard="hard" aria-pressed="true">Hard (7\u201314)</button>'
    + '<button type="button" data-hard="vhard">Very hard (15+)</button></div>'
    + '<div class="mc-out"><strong data-tier></strong><br><span data-note style="font-size:15px"></span></div>';
  const verdict = () => {
    const { hh, hard } = state;
    if (hh === '5p' && hard !== 'mod') return { tier: 'under-1500', label: 'Under-$1,500 tier \u2014 firmly', note: 'Five-plus people on hard water is where sub-$700 cabinet units become a false economy: constant regeneration, salt overuse, early valve failure. Budget a 48k\u201364k metered two-tank system.' };
    if (hh === '5p' || (hh === '34' && hard === 'vhard')) return { tier: 'under-1500', label: 'Under-$1,500 tier', note: 'Your grain demand points to a 48k metered system with a rebuildable valve \u2014 the tier-2 upgrades (capacity, valve quality) are exactly the ones your household will use.' };
    if (hh === '34' && hard === 'hard') return { tier: 'either', label: 'Top of tier 1 / bottom of tier 2', note: 'A 32k\u201340k metered unit at $500\u2013$900 covers you on city water. Skip timer-clock models \u2014 metered regeneration is the one feature worth insisting on at this size.' };
    return { tier: 'under-700', label: 'Under-$700 tier works', note: 'A big-box cabinet unit or entry Fleck bundle realistically covers your demand. Confirm hardness with a test before buying \u2014 and if you\u2019re on a well, test iron too; it changes the equipment list.' };
  };
  const update = () => {
    const v = verdict();
    root.querySelector('[data-tier]').textContent = v.label;
    root.querySelector('[data-note]').textContent = v.note;
    root.setAttribute('data-result', JSON.stringify({ household: state.hh, hardness: state.hard, tier: v.tier }));
  };
  root.querySelectorAll('[data-hh]').forEach(b => b.addEventListener('click', () => {
    state.hh = b.dataset.hh;
    root.querySelectorAll('[data-hh]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  root.querySelectorAll('[data-hard]').forEach(b => b.addEventListener('click', () => {
    state.hard = b.dataset.hard;
    root.querySelectorAll('[data-hard]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  update();
}

document.querySelectorAll('[data-expense-calc]').forEach(mountExpenseCalc);
export function mountMaintCalc(root) {
  root.classList.add('mini-calc');
  const state = { salt: 'sodium', bags: 10, prefilter: true, plan: false };
  root.innerHTML = '<span class="q">Price your softener&rsquo;s upkeep</span>'
    + '<div class="seg" role="group" aria-label="Salt type" style="margin-bottom:10px">'
    + '<button type="button" data-salt="sodium" aria-pressed="true">Sodium chloride ($5\u2013$10/bag)</button>'
    + '<button type="button" data-salt="potassium" aria-pressed="false">Potassium ($50\u2013$70/bag)</button></div>'
    + '<div><label for="mt-bags">Bags per year</label><div class="slider-row"><input id="mt-bags" type="range" min="4" max="16" step="1" value="10"><span class="slider-val" data-bags>10</span></div></div>'
    + '<div class="seg" role="group" aria-label="Extras" style="margin-top:10px">'
    + '<button type="button" data-x="prefilter" aria-pressed="true">+ Sediment prefilter ($20\u2013$60/yr)</button>'
    + '<button type="button" data-x="plan" aria-pressed="false">+ Dealer service plan ($100\u2013$200/yr)</button></div>'
    + '<div class="mc-out">Annual upkeep: <span class="fig" data-yr style="font-size:22px"></span><br>'
    + '<span style="font-size:15px">10-year total: <span class="fig" data-ten></span> &middot; roughly <span class="fig" data-mo></span>/month</span></div>';
  const bags = root.querySelector('#mt-bags');
  const update = () => {
    const b = +bags.value;
    const bagCost = state.salt === 'sodium' ? [5, 10] : [50, 70];
    let lo = b * bagCost[0], hi = b * bagCost[1];
    if (state.prefilter) { lo += 20; hi += 60; }
    if (state.plan) { lo += 100; hi += 200; }
    root.querySelector('[data-bags]').textContent = String(b);
    root.querySelector('[data-yr]').textContent = '$' + lo.toLocaleString() + ' \u2013 $' + hi.toLocaleString();
    root.querySelector('[data-ten]').textContent = '$' + (lo * 10).toLocaleString() + ' \u2013 $' + (hi * 10).toLocaleString();
    root.querySelector('[data-mo]').textContent = '$' + Math.round(lo / 12) + ' \u2013 $' + Math.round(hi / 12);
    root.setAttribute('data-result', JSON.stringify({ salt: state.salt, bags: b, prefilter: state.prefilter, plan: state.plan, low: lo, high: hi }));
  };
  root.querySelectorAll('[data-salt]').forEach(btn => btn.addEventListener('click', () => {
    state.salt = btn.dataset.salt;
    root.querySelectorAll('[data-salt]').forEach(x => x.setAttribute('aria-pressed', x === btn ? 'true' : 'false'));
    update();
  }));
  root.querySelectorAll('[data-x]').forEach(btn => btn.addEventListener('click', () => {
    state[btn.dataset.x] = !state[btn.dataset.x];
    btn.setAttribute('aria-pressed', state[btn.dataset.x] ? 'true' : 'false');
    update();
  }));
  bags.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-budget-fit]').forEach(mountBudgetFit);
export function mountCostcoCalc(root) {
  root.classList.add('mini-calc');
  const CMP_LOW = 1200, CMP_HIGH = 3200; // published factory-direct comparable (unit + labor, existing loop)
  const state = { exec: false };
  root.innerHTML = '<label for="cw-amt">Your EcoWater-via-Costco quote</label>'
    + '<div class="slider-row"><input id="cw-amt" type="range" min="4000" max="10000" step="100" value="8000"><span class="slider-val" data-amt style="min-width:72px"></span></div>'
    + '<div class="seg" role="group" aria-label="Membership"><button type="button" data-exec aria-pressed="false">+ Executive member (2% back)</button></div>'
    + '<div class="mc-out">Member perks return: <span class="fig" data-back></span><br>'
    + 'Net cost after perks: <span class="fig" data-net style="font-size:22px"></span><br>'
    + '<span style="font-size:15px">Comparable factory-direct route: <span class="fig">$1,200 \u2013 $3,200</span> \u00b7 remaining channel premium: <span class="fig" data-prem></span></span></div>';
  const amt = root.querySelector('#cw-amt');
  const update = () => {
    const v = +amt.value;
    const rate = state.exec ? 0.12 : 0.10;
    const back = Math.round(v * rate);
    const net = v - back;
    const pLo = Math.max(0, net - CMP_HIGH), pHi = Math.max(0, net - CMP_LOW);
    root.querySelector('[data-amt]').textContent = '$' + v.toLocaleString('en-US');
    root.querySelector('[data-back]').textContent = '$' + back.toLocaleString('en-US') + (state.exec ? ' (10% card + 2%)' : ' (10% Shop Card)');
    root.querySelector('[data-net]').textContent = '$' + net.toLocaleString('en-US');
    root.querySelector('[data-prem]').textContent = '$' + pLo.toLocaleString('en-US') + ' \u2013 $' + pHi.toLocaleString('en-US');
    root.setAttribute('data-result', JSON.stringify({ quote: v, exec: state.exec, back, net, premLow: pLo, premHigh: pHi }));
  };
  root.querySelector('[data-exec]').addEventListener('click', (e) => {
    state.exec = !state.exec;
    e.currentTarget.setAttribute('aria-pressed', state.exec ? 'true' : 'false');
    update();
  });
  amt.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-maint-calc]').forEach(mountMaintCalc);
export function mountTcoCalc(root) {
  root.classList.add('mini-calc');
  const state = { hh: '34' };
  const BAGS = { '12': 8, '34': 12, '5p': 16 };
  root.innerHTML = '<span class="q">10-year cost: salt-free conditioner vs. salt-based softener</span>'
    + '<div class="seg" role="group" aria-label="Household size" style="margin-bottom:10px">'
    + '<button type="button" data-hh="12">1\u20132 people</button>'
    + '<button type="button" data-hh="34" aria-pressed="true">3\u20134 people</button>'
    + '<button type="button" data-hh="5p">5+ people</button></div>'
    + '<div class="mc-out">Salt-free TAC (installed + media): <span class="fig" data-sf style="font-size:20px"></span><br>'
    + 'Salt-based softener (installed + salt + re-bed): <span class="fig" data-sb style="font-size:20px"></span><br>'
    + '<span style="font-size:14px;color:#5B6B75">Different outcomes, priced honestly: the conditioner prevents scale; only the softener delivers actual soft water. Ranges from the sourced figures on this page.</span></div>';
  const update = () => {
    const bags = BAGS[state.hh];
    // salt-free: unit+install 650–2,400 + media replacements over a decade 100–800
    const sfLo = 650 + 100, sfHi = 2400 + 800;
    // salt-based: installed-on-loop 800–2,000 + salt bags x $5–$10 x 10 yrs + one re-bed 250–600
    const sbLo = 800 + bags * 5 * 10 + 250, sbHi = 2000 + bags * 10 * 10 + 600;
    root.querySelector('[data-sf]').textContent = '$' + sfLo.toLocaleString() + ' \u2013 $' + sfHi.toLocaleString();
    root.querySelector('[data-sb]').textContent = '$' + sbLo.toLocaleString() + ' \u2013 $' + sbHi.toLocaleString();
    root.setAttribute('data-result', JSON.stringify({ household: state.hh, saltFree: [sfLo, sfHi], saltBased: [sbLo, sbHi] }));
  };
  root.querySelectorAll('[data-hh]').forEach(b => b.addEventListener('click', () => {
    state.hh = b.dataset.hh;
    root.querySelectorAll('[data-hh]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  update();
}

document.querySelectorAll('[data-costco-calc]').forEach(mountCostcoCalc);
export function mountTwinFit(root) {
  root.classList.add('mini-calc');
  const state = { use: 'daytime', demand: 'moderate' };
  root.innerHTML = '<span class="q">Does your home actually need twin tanks?</span>'
    + '<div class="seg" role="group" aria-label="Water use pattern" style="margin-bottom:10px">'
    + '<button type="button" data-use="daytime" aria-pressed="true">Typical daytime household</button>'
    + '<button type="button" data-use="always" aria-pressed="false">Round-the-clock water use</button></div>'
    + '<div class="seg" role="group" aria-label="Demand">'
    + '<button type="button" data-demand="moderate" aria-pressed="true">City water, moderate\u2013hard</button>'
    + '<button type="button" data-demand="heavy" aria-pressed="false">Well / very hard / 5+ people</button></div>'
    + '<div class="mc-out"><strong data-v></strong><br><span data-n style="font-size:15px"></span></div>';
  const verdict = () => {
    const { use, demand } = state;
    if (use === 'always' && demand === 'heavy') return { fit: 'twin', v: 'Twin-tank territory \u2014 firmly', n: 'Heavy demand plus 24/7 use is exactly what twins exist for: one tank serves while the other regenerates, so there\u2019s no hard-water window and no reserve-capacity waste. Budget the $1,500\u2013$5,000 installed band.' };
    if (use === 'always') return { fit: 'twin-lean', v: 'Twin justified \u2014 by schedule, not hardness', n: 'Night-shift schedules and round-the-clock use erase the 2 a.m. regeneration window a single tank relies on. A DIY-class twin ($1,219\u2013$1,454 unit) covers this without dealer pricing.' };
    if (demand === 'heavy') return { fit: 'either', v: 'Either works \u2014 size decides', n: 'Heavy demand on a daytime schedule is usually solved cheaper by a correctly-sized, metered single tank with reserve capacity. Price a twin only if regeneration would run more than ~twice a week.' };
    return { fit: 'single', v: 'A metered single tank covers you', n: 'Your softener will regenerate at 2 a.m. while nobody\u2019s using water \u2014 the hard-water window a twin eliminates doesn\u2019t exist in your house. Put the twin premium into valve quality and capacity instead.' };
  };
  const update = () => {
    const r = verdict();
    root.querySelector('[data-v]').textContent = r.v;
    root.querySelector('[data-n]').textContent = r.n;
    root.setAttribute('data-result', JSON.stringify({ use: state.use, demand: state.demand, fit: r.fit }));
  };
  root.querySelectorAll('[data-use]').forEach(b => b.addEventListener('click', () => {
    state.use = b.dataset.use;
    root.querySelectorAll('[data-use]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  root.querySelectorAll('[data-demand]').forEach(b => b.addEventListener('click', () => {
    state.demand = b.dataset.demand;
    root.querySelectorAll('[data-demand]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  update();
}

document.querySelectorAll('[data-tco-calc]').forEach(mountTcoCalc);
export function mountWellCalc(root) {
  root.classList.add('mini-calc');
  // installed component ranges (sources on page): softener base, AIO iron, sediment, UV
  const BASE = [1000, 3500];
  const ADD = { iron: [1500, 2500], sediment: [200, 600], uv: [700, 2500] };
  const state = { iron: true, sediment: true, uv: false };
  root.innerHTML = '<span class="q">Build your well-treatment stack (softener included)</span>'
    + '<div class="seg" role="group" aria-label="Stack components">'
    + '<button type="button" data-w="iron" aria-pressed="true">+ Iron filter (AIO) \u2014 iron &gt;1 ppm</button>'
    + '<button type="button" data-w="sediment" aria-pressed="true">+ Sediment prefilter</button>'
    + '<button type="button" data-w="uv" aria-pressed="false">+ UV disinfection \u2014 bacteria positive</button></div>'
    + '<div class="mc-out">Well softener, installed: <span class="fig">$1,000 \u2013 $3,500</span><br>'
    + 'Your full stack, installed: <span class="fig" data-total style="font-size:22px"></span><br>'
    + '<span data-note style="font-size:14px;color:#5B6B75"></span></div>';
  const update = () => {
    let lo = BASE[0], hi = BASE[1];
    if (state.iron) { lo += ADD.iron[0]; hi += ADD.iron[1]; }
    if (state.sediment) { lo += ADD.sediment[0]; hi += ADD.sediment[1]; }
    if (state.uv) { lo += ADD.uv[0]; hi += ADD.uv[1]; }
    root.querySelector('[data-total]').textContent = '$' + lo.toLocaleString('en-US') + ' \u2013 $' + hi.toLocaleString('en-US');
    root.querySelector('[data-note]').textContent = state.iron
      ? 'Matched iron + softener packages run $695\u2013$1,095 below buying the pair separately \u2014 ask, or buy them as one system.'
      : 'No iron? Then this is a standard softener project \u2014 the full cost guide itemizes it.';
    root.setAttribute('data-result', JSON.stringify({ iron: state.iron, sediment: state.sediment, uv: state.uv, low: lo, high: hi }));
  };
  root.querySelectorAll('[data-w]').forEach(b => b.addEventListener('click', () => {
    state[b.dataset.w] = !state[b.dataset.w];
    b.setAttribute('aria-pressed', state[b.dataset.w] ? 'true' : 'false');
    update();
  }));
  update();
}

document.querySelectorAll('[data-twin-fit]').forEach(mountTwinFit);
export function mountSystemFit(root) {
  root.classList.add('mini-calc');
  const OPTS = {
    hardness: { v: 'Salt-based softener', r: '$1,200 \u2013 $3,800 installed', n: 'The whole-house standard for scale, soap, and skin \u2014 HomeGuide\u2019s installed band. Our full cost guide itemizes every line.', href: '/', label: 'Full cost guide' },
    bighouse: { v: 'Dual-tank softener', r: '$1,700 \u2013 $5,000 installed', n: '24/7 soft water for 5+ person homes and round-the-clock use \u2014 one tank serves while the other regenerates.', href: '/dual-tank-water-softener-cost/', label: 'Dual-tank guide' },
    scaleonly: { v: 'Salt-free conditioner', r: '$900 \u2013 $3,000 installed', n: 'Scale prevention with near-zero upkeep \u2014 no salt, no drain, no power. Honest catch: it conditions, it doesn\u2019t soften.', href: '/salt-free-water-softener-cost/', label: 'Salt-free guide' },
    well: { v: 'Well stack: iron filter + softener', r: '$2,700 \u2013 $6,600 installed', n: 'Iron over 1 ppm needs its own filter ahead of the softener \u2014 or the resin pays for it. Matched packages save $695\u2013$1,095.', href: '/well-water-softener-cost/', label: 'Well water guide' },
  };
  const state = { pick: 'hardness' };
  root.innerHTML = '<span class="q">Which whole-house system is your project?</span>'
    + '<div class="seg" role="group" aria-label="Water situation" style="margin-bottom:10px">'
    + '<button type="button" data-pick="hardness" aria-pressed="true">Scale + soap problems (city water)</button>'
    + '<button type="button" data-pick="bighouse" aria-pressed="false">Very hard + big household / 24-7 use</button>'
    + '<button type="button" data-pick="scaleonly" aria-pressed="false">Scale only \u2014 want zero upkeep</button>'
    + '<button type="button" data-pick="well" aria-pressed="false">Private well (iron / staining)</button></div>'
    + '<div class="mc-out"><strong data-v style="font-size:18px"></strong><br>'
    + '<span class="fig" data-r style="font-size:22px"></span><br>'
    + '<span data-n style="font-size:14px;color:#5B6B75"></span><br>'
    + '<a data-l href="/" style="font-weight:600"></a></div>';
  const update = () => {
    const o = OPTS[state.pick];
    root.querySelector('[data-v]').textContent = o.v;
    root.querySelector('[data-r]').textContent = o.r;
    root.querySelector('[data-n]').textContent = o.n;
    const a = root.querySelector('[data-l]');
    a.href = o.href;
    a.textContent = o.label + ' \u2192';
    root.setAttribute('data-result', JSON.stringify({ pick: state.pick, system: o.v }));
  };
  root.querySelectorAll('[data-pick]').forEach(b => b.addEventListener('click', () => {
    state.pick = b.dataset.pick;
    root.querySelectorAll('[data-pick]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  update();
}

document.querySelectorAll('[data-well-calc]').forEach(mountWellCalc);
export function mountFateCalc(root) {
  root.classList.add('mini-calc');
  const state = { cond: 'working', goal: 'dontwant' };
  const verdict = () => {
    const { cond, goal } = state;
    if (cond === 'old') return { fit: 'replace', v: 'Replace it \u2014 in one visit', n: 'At 10\u201315 years a softener is at end-of-life, and removal is typically bundled free (or $50\u2013$100) with a new install \u2014 paying for standalone removal now and installation later buys the same plumbing labor twice.' };
    if (cond === 'acting') return { fit: 'repair', v: 'Price a repair first', n: 'Repairs run $150\u2013$600 for most faults (service call $40\u2013$100). Under 10 years old, repair usually wins; the 10-year mark is where the math flips to replacement.' };
    if (goal === 'salt') return { fit: 'saltfree', v: 'Swap to salt-free \u2014 don\u2019t just remove', n: 'If the objection is salt bags, brine, and regeneration \u2014 not soft water itself \u2014 a TAC conditioner swap reuses your existing loop and keeps scale protection at near-zero upkeep.' };
    if (goal === 'spot') return { fit: 'relocate', v: 'Relocation \u2014 priced as two jobs', n: 'Moving a working softener = a removal ($150\u2013$500) plus a partial retrofit at the new spot (pipe by the foot, drain, outlet). Calculated from those components: roughly $750\u2013$2,800.' };
    return { fit: 'test', v: 'Test the water before you rip it out', n: 'A working softener is solving something \u2014 confirm what, for $50\u2013$150, before paying $150\u2013$500 to remove it and inheriting the scale it was stopping. If the test says soft supply, remove with confidence.' };
  };
  root.innerHTML = '<span class="q">Remove, repair, replace, or relocate?</span>'
    + '<div class="seg" role="group" aria-label="System condition" style="margin-bottom:10px">'
    + '<button type="button" data-cond="working" aria-pressed="true">Works fine</button>'
    + '<button type="button" data-cond="acting" aria-pressed="false">Acting up</button>'
    + '<button type="button" data-cond="old" aria-pressed="false">10+ years / dead</button></div>'
    + '<div class="seg" role="group" aria-label="Your goal">'
    + '<button type="button" data-goal="dontwant" aria-pressed="true">Don\u2019t want one at all</button>'
    + '<button type="button" data-goal="salt" aria-pressed="false">Tired of salt &amp; upkeep</button>'
    + '<button type="button" data-goal="spot" aria-pressed="false">Need it somewhere else</button></div>'
    + '<div class="mc-out"><strong data-v style="font-size:18px"></strong><br><span data-n style="font-size:14px;color:#5B6B75"></span></div>';
  const update = () => {
    const r = verdict();
    root.querySelector('[data-v]').textContent = r.v;
    root.querySelector('[data-n]').textContent = r.n;
    root.setAttribute('data-result', JSON.stringify({ cond: state.cond, goal: state.goal, fit: r.fit }));
  };
  root.querySelectorAll('[data-cond]').forEach(b => b.addEventListener('click', () => {
    state.cond = b.dataset.cond;
    root.querySelectorAll('[data-cond]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  root.querySelectorAll('[data-goal]').forEach(b => b.addEventListener('click', () => {
    state.goal = b.dataset.goal;
    root.querySelectorAll('[data-goal]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  update();
}

document.querySelectorAll('[data-system-fit]').forEach(mountSystemFit);
export function mountIronCalc(root) {
  root.classList.add('mini-calc');
  const state = { sulfur: false, softener: false };
  root.innerHTML = '<label for="fe-ppm">Your tested iron level (ppm)</label>'
    + '<div class="slider-row"><input id="fe-ppm" type="range" min="0" max="15" step="0.5" value="3"><span class="slider-val" data-ppm style="min-width:72px"></span></div>'
    + '<div class="seg" role="group" aria-label="Extras">'
    + '<button type="button" data-x="sulfur" aria-pressed="false">+ Rotten-egg smell (sulfur)</button>'
    + '<button type="button" data-x="softener" aria-pressed="false">+ Softener installed or planned</button></div>'
    + '<div class="mc-out"><strong data-v style="font-size:18px"></strong><br><span class="fig" data-r style="font-size:20px"></span><br><span data-n style="font-size:14px;color:#5B6B75"></span></div>';
  const tier = (ppm) => {
    if (ppm < 0.3) return { t: 'none', v: 'Below the staining threshold', r: '$0 \u2014 no dedicated filter', n: 'Under the 0.3 ppm secondary standard. If staining persists anyway, test manganese \u2014 black stains have their own culprit.' };
    if (ppm <= 1) return { t: 'borderline', v: 'Borderline zone \u2014 test before buying', r: '$0 \u2013 $2,500', n: 'Trace ferrous iron up to ~1 ppm is softener-tolerable. Confirm manganese and pH before spending on a dedicated filter you may not need.' };
    if (ppm <= 7) return { t: 'aio', v: 'AIO air-injection territory', r: '$1,200 \u2013 $2,500 installed', n: 'The chemical-free standard: one tank oxidizes and filters iron (and sulfur to ~8 ppm), $0/yr in chemicals, media good 6\u20138 years.' };
    return { t: 'high', v: 'High-iron: verify capacity ratings', r: '$1,500 \u2013 $4,000 installed', n: 'Above ~7 ppm, check each AIO model\u2019s rated capacity \u2014 many top out here \u2014 or step to chemical injection (chlorine/peroxide), which handles 15+ ppm and iron bacteria at $100\u2013$250/yr in chemicals.' };
  };
  const ppmInput = root.querySelector('#fe-ppm');
  const update = () => {
    const ppm = +ppmInput.value;
    const r = tier(ppm);
    root.querySelector('[data-ppm]').textContent = ppm.toFixed(1) + ' ppm';
    root.querySelector('[data-v]').textContent = r.v;
    root.querySelector('[data-r]').textContent = r.r;
    let note = r.n;
    if (state.sulfur && r.t === 'aio') note += ' Your sulfur smell rides along free \u2014 the same AIO tank handles both.';
    if (state.sulfur && r.t === 'high') note += ' With sulfur present, chemical injection covers both in one system.';
    if (state.softener) note += ' And the order is law: this filter goes FIRST \u2014 iron over ~1 ppm kills softener resin in 6\u201318 months.';
    root.querySelector('[data-n]').textContent = note;
    root.setAttribute('data-result', JSON.stringify({ ppm, sulfur: state.sulfur, softener: state.softener, tier: r.t }));
  };
  root.querySelectorAll('[data-x]').forEach(b => b.addEventListener('click', () => {
    state[b.dataset.x] = !state[b.dataset.x];
    b.setAttribute('aria-pressed', state[b.dataset.x] ? 'true' : 'false');
    update();
  }));
  ppmInput.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-fate-calc]').forEach(mountFateCalc);
export function mountPhCalc(root) {
  root.classList.add('mini-calc');
  const state = { iron: false, hard: false };
  root.innerHTML = '<label for="ph-val">Your tested pH</label>'
    + '<div class="slider-row"><input id="ph-val" type="range" min="5" max="8" step="0.1" value="6.5"><span class="slider-val" data-ph style="min-width:56px"></span></div>'
    + '<div class="seg" role="group" aria-label="Water extras">'
    + '<button type="button" data-p="iron" aria-pressed="false">+ Iron or heavy sediment</button>'
    + '<button type="button" data-p="hard" aria-pressed="false">+ Already hard (5+ gpg)</button></div>'
    + '<div class="mc-out"><strong data-v style="font-size:18px"></strong><br><span class="fig" data-r style="font-size:20px"></span><br><span data-n style="font-size:14px;color:#5B6B75"></span></div>';
  const tier = (ph) => {
    if (ph >= 7.0) return { t: 'none', v: 'No neutralizer needed', r: '$0', n: 'At 7.0+ your water isn\u2019t corrosive \u2014 spend nothing here. If you\u2019re seeing blue-green stains anyway, retest: pH swings seasonally on some wells.' };
    if (ph >= 6.0) return { t: 'calcite', v: 'Standard calcite territory', r: '$1,195 \u2013 $1,495 system', n: 'The 90% case: a non-backwashing upflow calcite tank \u2014 no electricity, no drain, DIY-friendly in 1\u20132 hours ($0\u2013$100) or $300\u2013$800 plumbed.' };
    if (ph >= 5.5) return { t: 'blend', v: 'Calcite + FloMag blend', r: '+ ~$200 on the system', n: 'Below 6.0, calcite alone corrects too slowly \u2014 the 90/10 FloMag blend works ~5\u00d7 faster. Same tank, upgraded media.' };
    return { t: 'deep', v: 'Deeply acidic \u2014 blend + careful sizing', r: '$1,395 \u2013 $1,895+ system', n: 'Field blends reach pH 4.0 and below, but sizing is everything down here \u2014 undersizing, not the media, is why neutralizers disappoint. Size up.' };
  };
  const phInput = root.querySelector('#ph-val');
  const update = () => {
    const ph = +phInput.value;
    const r = tier(ph);
    root.querySelector('[data-ph]').textContent = ph.toFixed(1);
    root.querySelector('[data-v]').textContent = r.v;
    root.querySelector('[data-r]').textContent = r.r;
    let note = r.n;
    if (state.iron && r.t !== 'none') note += ' With iron or sediment in the water, step to a BACKWASHING neutralizer ($1,695\u2013$1,895) \u2014 or treat the iron separately \u2014 because both foul a static calcite bed.';
    if (state.hard && r.t !== 'none') note += ' Already-hard water + the 2\u20135 gpg calcite adds = softener downstream; matched neutralizer + softener packages run $295\u2013$495 below separate purchases.';
    root.querySelector('[data-n]').textContent = note;
    root.setAttribute('data-result', JSON.stringify({ ph, iron: state.iron, hard: state.hard, tier: r.t }));
  };
  root.querySelectorAll('[data-p]').forEach(b => b.addEventListener('click', () => {
    state[b.dataset.p] = !state[b.dataset.p];
    b.setAttribute('aria-pressed', state[b.dataset.p] ? 'true' : 'false');
    update();
  }));
  phInput.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-iron-calc]').forEach(mountIronCalc);
export function mountUvCalc(root) {
  root.classList.add('mini-calc');
  const state = { baths: '12', source: 'well' };
  root.innerHTML = '<span class="q">Size your UV system \u2014 and get the class right</span>'
    + '<div class="seg" role="group" aria-label="Bathrooms" style="margin-bottom:10px">'
    + '<button type="button" data-b="12" aria-pressed="true">1\u20132 bathrooms</button>'
    + '<button type="button" data-b="34" aria-pressed="false">3\u20134 bathrooms</button>'
    + '<button type="button" data-b="5p" aria-pressed="false">5+ / irrigation / outbuildings</button></div>'
    + '<div class="seg" role="group" aria-label="Water source">'
    + '<button type="button" data-s="well" aria-pressed="true">Private well (sole barrier)</button>'
    + '<button type="button" data-s="city" aria-pressed="false">City water (extra layer)</button></div>'
    + '<div class="mc-out"><strong data-v style="font-size:18px"></strong><br><span class="fig" data-r style="font-size:20px"></span><br><span data-n style="font-size:14px;color:#5B6B75"></span></div>';
  const update = () => {
    const { baths, source } = state;
    let size, range;
    if (baths === '12') { size = '~9\u201312 GPM chamber'; range = '$500 \u2013 $1,500 installed'; }
    else if (baths === '34') { size = '~15\u201318 GPM chamber'; range = '$700 \u2013 $2,500 installed'; }
    else { size = '20+ GPM \u2014 outside standard charts'; range = 'get it sized professionally'; }
    let v, n;
    if (source === 'well') {
      v = 'NSF 55 Class A (40 mJ/cm\u00b2) \u2014 mandatory, ' + size;
      n = 'On a well, UV is your sole bacterial barrier: Class A is the only rating certified for microbiologically unsafe water. Class B (16 mJ/cm\u00b2) is never appropriate on a well \u2014 and most $150\u2013$400 budget units are Class B or uncertified. When between sizes, size UP: an undersized chamber under-doses at peak flow.';
    } else {
      v = 'Class B acceptable \u2014 supplemental layer, ' + size;
      n = 'On treated city water, UV is a belt-and-suspenders layer against rare contamination events, so a Class B (16 mJ/cm\u00b2) unit is a legitimate budget choice. Class A still buys certainty if anyone in the home is immunocompromised.';
    }
    root.querySelector('[data-v]').textContent = v;
    root.querySelector('[data-r]').textContent = range;
    root.querySelector('[data-n]').textContent = n;
    root.setAttribute('data-result', JSON.stringify({ baths, source, classReq: source === 'well' ? 'A' : 'B-ok' }));
  };
  root.querySelectorAll('[data-b]').forEach(b => b.addEventListener('click', () => {
    state.baths = b.dataset.b;
    root.querySelectorAll('[data-b]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  root.querySelectorAll('[data-s]').forEach(b => b.addEventListener('click', () => {
    state.source = b.dataset.s;
    root.querySelectorAll('[data-s]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  update();
}

document.querySelectorAll('[data-ph-calc]').forEach(mountPhCalc);
export function mountFinanceCalc(root) {
  root.classList.add('mini-calc');
  const P0 = +(root.getAttribute('data-pmt') || 99);
  const T0 = +(root.getAttribute('data-term') || 84);
  const A0 = +(root.getAttribute('data-apr') || 15.9);
  const state = { term: T0 };
  const fmt = (n) => '$' + Math.round(n).toLocaleString('en-US');
  const termBtn = (t) => '<button type="button" data-t="' + t + '" aria-pressed="' + (t === T0 ? 'true' : 'false') + '">' + t + ' mo</button>';
  root.innerHTML = '<label for="fin-pmt">The monthly payment you were quoted</label>'
    + '<div class="slider-row"><input id="fin-pmt" type="range" min="25" max="400" step="5" value="' + P0 + '"><span class="slider-val" data-pmt style="min-width:72px"></span></div>'
    + '<div class="seg" role="group" aria-label="Loan term" style="margin-bottom:10px">'
    + termBtn(36) + termBtn(60) + termBtn(84) + termBtn(120) + '</div>'
    + '<label for="fin-apr">APR from the disclosure</label>'
    + '<div class="slider-row"><input id="fin-apr" type="range" min="0" max="29.9" step="0.5" value="' + A0 + '"><span class="slider-val" data-apr style="min-width:64px"></span></div>'
    + '<div class="mc-out"><span style="font-size:14px;color:#5B6B75">Total of scheduled payments</span><br>'
    + '<span class="fig" data-total style="font-size:26px"></span><br>'
    + '<strong data-price style="font-size:16px"></strong><br>'
    + '<span data-int style="font-size:14px;color:#5B6B75"></span><br>'
    + '<span data-note style="font-size:13px;color:#5B6B75"></span></div>';
  const pmtIn = root.querySelector('#fin-pmt');
  const aprIn = root.querySelector('#fin-apr');
  const update = () => {
    const pmt = +pmtIn.value, n = state.term, apr = +aprIn.value;
    const i = apr / 100 / 12;
    const total = pmt * n;
    const principal = i === 0 ? total : pmt * (1 - Math.pow(1 + i, -n)) / i;
    const interest = total - principal;
    const share = total > 0 ? Math.round((interest / total) * 100) : 0;
    root.querySelector('[data-pmt]').textContent = '$' + pmt + '/mo';
    root.querySelector('[data-apr]').textContent = apr.toFixed(1) + '%';
    root.querySelector('[data-total]').textContent = fmt(total);
    root.querySelector('[data-price]').textContent = 'Implied system price \u2248 ' + fmt(principal);
    root.querySelector('[data-int]').textContent = interest > 0
      ? 'Interest: ' + fmt(interest) + ' \u2014 ' + share + '% of everything you hand over'
      : 'Interest: $0 at a true 0% APR';
    root.querySelector('[data-note]').textContent = apr === 0
      ? 'Check the paperwork: a true 0% APR means the total IS the price. \u201cNo interest if paid in full\u201d is deferred interest \u2014 a different animal (see below).'
      : 'Your numbers from your own disclosure \u2014 not any dealer\u2019s published terms. Fees and promo periods can move the real total.';
    root.setAttribute('data-result', JSON.stringify({ pmt, term: n, apr, total, principal: Math.round(principal), interest: Math.round(interest) }));
  };
  root.querySelectorAll('[data-t]').forEach(b => b.addEventListener('click', () => {
    state.term = +b.dataset.t;
    root.querySelectorAll('[data-t]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  pmtIn.addEventListener('input', update);
  aprIn.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-uv-calc]').forEach(mountUvCalc);
export function mountRealityCheck(root) {
  root.classList.add('mini-calc');
  const SITE = {
    prepared: { lo: 890, hi: 2270 },
    noloop: { lo: 1490, hi: 4270 },
    complex: { lo: 2340, hi: 5470 },
  };
  const state = { site: 'prepared', bundle: false };
  const fmt = (n) => '$' + Math.round(n).toLocaleString('en-US');
  root.innerHTML = '<label for="rc-quote">The installed total you were quoted</label>'
    + '<div class="slider-row"><input id="rc-quote" type="range" min="1500" max="10000" step="100" value="6000"><span class="slider-val" data-q style="min-width:84px"></span></div>'
    + '<div class="seg" role="group" aria-label="Your site condition" style="margin-bottom:10px">'
    + '<button type="button" data-site="prepared" aria-pressed="true">Loop, drain &amp; outlet already there</button>'
    + '<button type="button" data-site="noloop" aria-pressed="false">No softener loop</button>'
    + '<button type="button" data-site="complex" aria-pressed="false">No loop, no drain, tight access</button></div>'
    + '<div class="seg" role="group" aria-label="Bundled equipment">'
    + '<button type="button" data-bundle aria-pressed="false">+ The quote bundles extra equipment (filter / RO)</button></div>'
    + '<div class="mc-out"><span style="font-size:14px;color:#5B6B75">Documented cost of the work on your house</span><br>'
    + '<span class="fig" data-doc style="font-size:20px"></span><br>'
    + '<strong data-verdict style="font-size:17px;display:inline-block;margin-top:8px"></strong><br>'
    + '<span data-rem style="font-size:14px;color:#5B6B75"></span><br>'
    + '<span data-warn style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:8px"></span></div>';
  const qIn = root.querySelector('#rc-quote');
  const update = () => {
    const q = +qIn.value;
    const d = SITE[state.site];
    const inside = q <= d.hi;
    const remLo = Math.max(0, q - d.hi);
    const remHi = Math.max(0, q - d.lo);
    root.querySelector('[data-q]').textContent = fmt(q);
    root.querySelector('[data-doc]').textContent = fmt(d.lo) + ' \u2013 ' + fmt(d.hi);
    if (inside) {
      root.querySelector('[data-verdict]').textContent = 'Inside the documented range \u2014 the question isn\u2019t markup, it\u2019s scope';
      root.querySelector('[data-rem]').textContent = 'A quote at or below the documented cost of the work is not automatically the bargain it looks like. Ask what is excluded: site work, old-unit removal, permit, startup, haul-away.';
    } else {
      const pctLo = Math.round((remLo / q) * 100), pctHi = Math.round((remHi / q) * 100);
      root.querySelector('[data-verdict]').textContent = 'Unexplained / bundled remainder: ' + fmt(remLo) + ' \u2013 ' + fmt(remHi);
      root.querySelector('[data-rem]').textContent = 'Roughly ' + pctLo + '\u2013' + pctHi + '% of your quote sits above the published cost of the equipment class plus the labor and site work.';
    }
    let warn = 'That remainder is NOT the dealer\u2019s profit. It also funds the in-home appointment, the lead that produced it, vehicles, warehousing, insurance, licensing, admin, warranty reserves, a service department, and financing costs. It IS the part you are entitled to see itemized before you sign.';
    if (state.bundle) warn += ' And you have said extra equipment is bundled \u2014 part of that remainder is hardware nobody can price without model numbers. Ask for every model number on its own line.';
    root.querySelector('[data-warn]').textContent = warn;
    root.setAttribute('data-result', JSON.stringify({ quote: q, site: state.site, bundle: state.bundle, docLo: d.lo, docHi: d.hi, remLo, remHi, inside }));
  };
  root.querySelectorAll('[data-site]').forEach(b => b.addEventListener('click', () => {
    state.site = b.dataset.site;
    root.querySelectorAll('[data-site]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  const bBtn = root.querySelector('[data-bundle]');
  bBtn.addEventListener('click', () => {
    state.bundle = !state.bundle;
    bBtn.setAttribute('aria-pressed', state.bundle ? 'true' : 'false');
    update();
  });
  qIn.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-finance-calc]').forEach(mountFinanceCalc);
export function mountRentBuy(root) {
  root.classList.add('mini-calc');
  const SETUP = 250, OWN = 2000, OWN_YR = 190, SALT = 100;
  const state = { incl: 'all' };
  const fmt = (n) => '$' + Math.round(n).toLocaleString('en-US');
  root.innerHTML = '<label for="rb-rent">Your monthly rental payment</label>'
    + '<div class="slider-row"><input id="rb-rent" type="range" min="15" max="120" step="5" value="50"><span class="slider-val" data-r style="min-width:72px"></span></div>'
    + '<label for="rb-years">Years you expect to stay in the house</label>'
    + '<div class="slider-row"><input id="rb-years" type="range" min="1" max="20" step="1" value="10"><span class="slider-val" data-y style="min-width:72px"></span></div>'
    + '<div class="seg" role="group" aria-label="What the rental includes">'
    + '<button type="button" data-incl="all" aria-pressed="true">Service, repairs &amp; salt</button>'
    + '<button type="button" data-incl="service" aria-pressed="false">Service &amp; repairs; salt extra</button>'
    + '<button type="button" data-incl="none" aria-pressed="false">Equipment only</button></div>'
    + '<div class="mc-out"><span data-tot style="font-size:15px"></span><br>'
    + '<strong data-v class="fig" style="font-size:20px;display:inline-block;margin-top:6px"></strong><br>'
    + '<span data-be style="font-size:15px;color:#16303F"></span><br>'
    + '<span data-note style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:8px"></span></div>';
  const rIn = root.querySelector('#rb-rent'), yIn = root.querySelector('#rb-years');
  const annual = (rent) => rent * 12 + (state.incl === 'all' ? 0 : state.incl === 'service' ? SALT : OWN_YR);
  const update = () => {
    const rent = +rIn.value, years = +yIn.value;
    const ra = annual(rent);
    const rentalTotal = SETUP + ra * years;
    const ownerTotal = OWN + OWN_YR * years;
    let breakEven = 0;
    for (let n = 1; n <= 30; n++) {
      if (SETUP + ra * n > OWN + OWN_YR * n) { breakEven = n; break; }
    }
    const cheaper = rentalTotal < ownerTotal ? 'rent' : 'own';
    const diff = Math.abs(rentalTotal - ownerTotal);
    root.querySelector('[data-r]').textContent = '$' + rent + '/mo';
    root.querySelector('[data-y]').textContent = years + (years === 1 ? ' year' : ' years');
    root.querySelector('[data-tot]').textContent = 'Over ' + years + (years === 1 ? ' year' : ' years') + ' \u2014 renting: ' + fmt(rentalTotal) + ' \u00b7 owning: ' + fmt(ownerTotal);
    root.querySelector('[data-v]').textContent = cheaper === 'rent'
      ? 'Renting costs ' + fmt(diff) + ' less over your horizon'
      : 'Owning costs ' + fmt(diff) + ' less over your horizon';
    root.querySelector('[data-be]').textContent = breakEven
      ? 'Break-even: year ' + breakEven + ' \u2014 after that, every payment is money the owner isn\u2019t spending.'
      : 'No break-even inside 30 years. At this rate the rental stays cheaper for as long as you would plausibly stay \u2014 and that is a real answer, not a consolation prize.';
    root.querySelector('[data-note]').textContent = 'Flat-payment baseline: this assumes your rate never rises. Ownership is modelled at $2,000 installed (mid of our sourced $840\u2013$4,120 range) plus $190/yr for upkeep and a repair allowance. The rental also transfers repair risk, which is worth something real \u2014 the tool prices the money, not the peace of mind.';
    root.setAttribute('data-result', JSON.stringify({ rent, years, incl: state.incl, rentalTotal, ownerTotal, breakEven, cheaper }));
  };
  root.querySelectorAll('[data-incl]').forEach(b => b.addEventListener('click', () => {
    state.incl = b.dataset.incl;
    root.querySelectorAll('[data-incl]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  rIn.addEventListener('input', update);
  yIn.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-reality-check]').forEach(mountRealityCheck);
export function mountSedimentCalc(root) {
  root.classList.add('mini-calc');
  const OPTS = {
    sand: {
      v: 'Spin-down first \u2014 then a cartridge for the fines',
      r: '$145 \u2013 $360 equipment',
      n: 'A reusable screen spins coarse sand into a clear sump you flush in about ten seconds \u2014 zero cartridge cost, ever. But screens run 50\u2013100 micron, so fine silt passes straight through: add a 5-micron cartridge behind it if the water is also cloudy.',
    },
    silt: {
      v: 'One 20-inch cartridge housing, 5 micron',
      r: '$250 \u2013 $600 installed',
      n: 'The answer for roughly 70% of wells. A polyspun depth cartridge traps silt, clay and rust fines. Budget $30\u2013$100/yr in cartridges, changed every 3\u20136 months.',
    },
    heavy: {
      v: 'Spin-down + cartridge combo \u2014 before you spend $1,895',
      r: '$310 \u2013 $360 equipment',
      n: 'Heavy sediment eats cartridges in weeks. A spin-down upstream stretches them to 6\u201312 months. Only if cartridges STILL clog monthly does the $1,895 self-cleaning backwashing tank earn its price \u2014 and the specialist who sells that tank says most homes never need it.',
    },
    none: {
      v: 'One 5-micron cartridge, as insurance',
      r: '$250 \u2013 $600 installed',
      n: 'Nothing visible in the glass does not mean nothing is reaching your equipment. This stage exists to protect the expensive stages behind it \u2014 that is the whole job.',
    },
  };
  const state = { see: 'silt', uv: false, equip: false };
  root.innerHTML = '<span class="q">What do you actually see in the water?</span>'
    + '<div class="seg" role="group" aria-label="What you see" style="margin-bottom:10px">'
    + '<button type="button" data-see="sand" aria-pressed="false">Visible sand or grit</button>'
    + '<button type="button" data-see="silt" aria-pressed="true">Cloudy / silty</button>'
    + '<button type="button" data-see="heavy" aria-pressed="false">Heavy &amp; constant \u2014 clogging fixtures</button>'
    + '<button type="button" data-see="none" aria-pressed="false">Nothing \u2014 protecting equipment</button></div>'
    + '<div class="seg" role="group" aria-label="Downstream equipment">'
    + '<button type="button" data-x="uv" aria-pressed="false">+ Feeding a UV system</button>'
    + '<button type="button" data-x="equip" aria-pressed="false">+ Feeding a softener or iron filter</button></div>'
    + '<div class="mc-out"><strong data-v style="font-size:17px"></strong><br>'
    + '<span class="fig" data-r style="font-size:20px"></span><br>'
    + '<span data-n style="font-size:14px;color:#5B6B75"></span></div>';
  const update = () => {
    const o = OPTS[state.see];
    root.querySelector('[data-v]').textContent = o.v;
    root.querySelector('[data-r]').textContent = o.r;
    let note = o.n;
    if (state.uv) note += ' Feeding a UV system? Specify 5-micron ABSOLUTE, not nominal \u2014 absolute means 99.9% of particles at that size, and UV cannot disinfect water it cannot penetrate.';
    if (state.equip) note += ' And in front of a softener or iron filter this is not optional: sediment is the number-one killer of softener resin, iron-filter media beds and UV sleeves.';
    root.querySelector('[data-n]').textContent = note;
    root.setAttribute('data-result', JSON.stringify({ see: state.see, uv: state.uv, equip: state.equip }));
  };
  root.querySelectorAll('[data-see]').forEach(b => b.addEventListener('click', () => {
    state.see = b.dataset.see;
    root.querySelectorAll('[data-see]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  root.querySelectorAll('[data-x]').forEach(b => b.addEventListener('click', () => {
    state[b.dataset.x] = !state[b.dataset.x];
    b.setAttribute('aria-pressed', state[b.dataset.x] ? 'true' : 'false');
    update();
  }));
  update();
}

document.querySelectorAll('[data-rent-buy]').forEach(mountRentBuy);
export function mountAnchorTest(root) {
  root.classList.add('mini-calc');
  const SITE = { prepared: { lo: 890, hi: 2270 }, noloop: { lo: 1490, hi: 4270 }, complex: { lo: 2340, hi: 5470 } };
  const DISCOUNT = 0.468;
  const state = { site: 'prepared', cut: false };
  const fmt = (n) => '$' + Math.round(n).toLocaleString('en-US');
  root.innerHTML = '<label for="at-quote">The first number they said out loud</label>'
    + '<div class="slider-row"><input id="at-quote" type="range" min="1500" max="10000" step="100" value="9000"><span class="slider-val" data-q style="min-width:84px"></span></div>'
    + '<div class="seg" role="group" aria-label="Your site condition" style="margin-bottom:10px">'
    + '<button type="button" data-site="prepared" aria-pressed="true">Loop, drain &amp; outlet already there</button>'
    + '<button type="button" data-site="noloop" aria-pressed="false">No softener loop</button>'
    + '<button type="button" data-site="complex" aria-pressed="false">No loop, no drain, tight access</button></div>'
    + '<div class="seg" role="group" aria-label="Same-visit discount">'
    + '<button type="button" data-cut aria-pressed="false">+ Apply a same-visit &ldquo;supervisor&rdquo; discount</button></div>'
    + '<div class="mc-out"><span style="font-size:14px;color:#5B6B75">Documented cost of the work on your house</span><br>'
    + '<span class="fig" data-doc style="font-size:19px"></span><br>'
    + '<strong data-v style="font-size:17px;display:inline-block;margin-top:8px"></strong><br>'
    + '<span data-rem style="font-size:14px;color:#5B6B75"></span><br>'
    + '<span data-note style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:8px"></span></div>';
  const qIn = root.querySelector('#at-quote');
  const update = () => {
    const q = +qIn.value;
    const eff = state.cut ? q * (1 - DISCOUNT) : q;
    const d = SITE[state.site];
    const remLo = Math.max(0, eff - d.hi), remHi = Math.max(0, eff - d.lo);
    const pctLo = eff > 0 ? Math.round((remLo / eff) * 100) : 0;
    const pctHi = eff > 0 ? Math.round((remHi / eff) * 100) : 0;
    root.querySelector('[data-q]').textContent = fmt(q);
    root.querySelector('[data-doc]').textContent = fmt(d.lo) + ' \u2013 ' + fmt(d.hi);
    root.querySelector('[data-v]').textContent = state.cut
      ? 'After the discount: ' + fmt(eff)
      : 'On the table: ' + fmt(eff);
    root.querySelector('[data-rem]').textContent = remHi > 0
      ? 'Above the documented cost of the work: ' + fmt(remLo) + ' \u2013 ' + fmt(remHi) + ' (' + pctLo + '\u2013' + pctHi + '% of what you would pay)'
      : 'This lands at or below the documented cost of the work \u2014 now the question is scope: ask what is excluded.';
    root.querySelector('[data-note]').textContent = 'The discount rate here (47%) is one customer\u2019s published account, not a policy and not a promise. And that is the whole lesson: a discount off a number nobody publishes is not a saving, it is a negotiation. The documented cost of the work does not move when a salesperson phones his supervisor.';
    root.setAttribute('data-result', JSON.stringify({ quote: q, cut: state.cut, effective: Math.round(eff), site: state.site, docLo: d.lo, docHi: d.hi, remLo: Math.round(remLo), remHi: Math.round(remHi) }));
  };
  root.querySelectorAll('[data-site]').forEach(b => b.addEventListener('click', () => {
    state.site = b.dataset.site;
    root.querySelectorAll('[data-site]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  const cutBtn = root.querySelector('[data-cut]');
  cutBtn.addEventListener('click', () => {
    state.cut = !state.cut;
    cutBtn.setAttribute('aria-pressed', state.cut ? 'true' : 'false');
    update();
  });
  qIn.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-sediment-calc]').forEach(mountSedimentCalc);
export function mountSizer(root) {
  root.classList.add('mini-calc');
  const LADDER = [
    { name: 24000, cuft: 0.75 }, { name: 32000, cuft: 1.0 }, { name: 40000, cuft: 1.25 },
    { name: 48000, cuft: 1.5 }, { name: 64000, cuft: 2.0 }, { name: 80000, cuft: 2.5 },
  ];
  const EFF = 0.65, GPD = 75, LEAN = 6, MAXSALT = 15;
  const n = (x) => Math.round(x).toLocaleString('en-US');
  root.innerHTML = '<label for="sz-people">People in the house</label>'
    + '<div class="slider-row"><input id="sz-people" type="range" min="1" max="8" step="1" value="4"><span class="slider-val" data-p style="min-width:76px"></span></div>'
    + '<label for="sz-hard">Water hardness (grains per gallon)</label>'
    + '<div class="slider-row"><input id="sz-hard" type="range" min="1" max="40" step="1" value="10"><span class="slider-val" data-h style="min-width:76px"></span></div>'
    + '<label for="sz-iron">Iron (ppm) &mdash; well water only</label>'
    + '<div class="slider-row"><input id="sz-iron" type="range" min="0" max="6" step="0.5" value="0"><span class="slider-val" data-i style="min-width:76px"></span></div>'
    + '<div class="mc-out"><span data-load style="font-size:14px;color:#5B6B75"></span><br>'
    + '<strong data-rec class="fig" style="font-size:22px;display:inline-block;margin-top:6px"></strong><br>'
    + '<span data-regen style="font-size:15px;color:#16303F"></span><br>'
    + '<span data-naive style="font-size:14px;color:#5B6B75;display:inline-block;margin-top:8px"></span><br>'
    + '<span data-salt style="font-size:14px;color:#5B6B75"></span><br>'
    + '<span data-warn style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:8px"></span></div>';
  const pIn = root.querySelector('#sz-people'), hIn = root.querySelector('#sz-hard'), iIn = root.querySelector('#sz-iron');
  const update = () => {
    const people = +pIn.value, hard = +hIn.value, iron = +iIn.value;
    const comp = hard + iron * 5;
    const daily = people * GPD * comp;
    const weekly = daily * 7;
    const naive = LADDER.find(u => u.name >= weekly) || LADDER[LADDER.length - 1];
    const rec = LADDER.find(u => u.name * EFF >= weekly) || LADDER[LADDER.length - 1];
    const recDays = (rec.name * EFF) / daily;
    const recSaltYr = (365 / recDays) * rec.cuft * LEAN;
    const naiveDays = naive.name / daily;
    const naiveSaltYr = (365 / naiveDays) * naive.cuft * MAXSALT;
    const bags = (naiveSaltYr - recSaltYr) / 40;
    root.querySelector('[data-p]').textContent = people + (people === 1 ? ' person' : ' people');
    root.querySelector('[data-h]').textContent = hard + ' gpg';
    root.querySelector('[data-i]').textContent = iron + ' ppm';
    root.querySelector('[data-load]').textContent = 'Compensated hardness ' + comp + ' gpg \u00b7 ' + n(daily) + ' grains/day \u00b7 ' + n(weekly) + ' grains over 7 days';
    root.querySelector('[data-rec]').textContent = n(rec.name) + '-grain (' + rec.cuft + ' cu ft)';
    root.querySelector('[data-regen]').textContent = 'Regenerates about every ' + recDays.toFixed(1) + ' days at an efficient salt dose \u2014 inside the healthy 7\u201314 day window.';
    root.querySelector('[data-naive]').textContent = naive.name < rec.name
      ? 'Most sizing calculators would send you to a ' + n(naive.name) + '-grain unit. It only reaches that number at its maximum salt dose. Run it lean instead and it delivers about ' + n(naive.name * EFF) + ' grains \u2014 regenerating every ' + ((naive.name * EFF) / daily).toFixed(1) + ' days, which is more cycles, more water, and more wear on the valve.'
      : 'The standard calculation and the efficient-salt calculation agree on this one.';
    root.querySelector('[data-salt]').textContent = bags > 0.5
      ? 'Salt: roughly ' + n(recSaltYr) + ' lbs/yr on the recommended unit versus ' + n(naiveSaltYr) + ' lbs/yr forcing the smaller one to its nameplate \u2014 about ' + bags.toFixed(1) + ' fewer 40-lb bags a year ($' + n(bags * 5) + '\u2013$' + n(bags * 10) + ' at Angi\u2019s $5\u2013$10 a bag).'
      : 'Salt: roughly ' + n(recSaltYr) + ' lbs/yr at the efficient dose.';
    let warn = '';
    if (hard <= 3) warn = 'At ' + hard + ' gpg your water is already soft. Before buying anything, ask whether you need a softener at all \u2014 the honest answer here is often no.';
    else if (iron >= 3) warn = 'At ' + iron + ' ppm, iron is doing ' + Math.round((iron * 5 / comp) * 100) + '% of the resin\u2019s work \u2014 and iron fouls the bed as it goes. A softener alone will not survive this. Put an iron filter in front of it.';
    else if (iron >= 1) warn = 'Above 1 ppm, iron does not just consume capacity \u2014 it coats the resin and shortens its life. Size the softener, but filter the iron first.';
    root.querySelector('[data-warn]').textContent = warn;
    root.setAttribute('data-result', JSON.stringify({ people, hard, iron, comp, daily, weekly, naive: naive.name, rec: rec.name, recDays: +recDays.toFixed(1), recSaltYr: Math.round(recSaltYr), naiveSaltYr: Math.round(naiveSaltYr) }));
  };
  [pIn, hIn, iIn].forEach(el => el.addEventListener('input', update));
  update();
}

document.querySelectorAll('[data-anchor-test]').forEach(mountAnchorTest);
export function mountRunCost(root) {
  root.classList.add('mini-calc');
  const LADDER = [
    { name: 24000, cuft: 0.75 }, { name: 32000, cuft: 1.0 }, { name: 40000, cuft: 1.25 },
    { name: 48000, cuft: 1.5 }, { name: 64000, cuft: 2.0 }, { name: 80000, cuft: 2.5 },
  ];
  const EFF = 0.65, GPD = 75, LEAN = 6, KWH = 70, GALREGEN = 27.5, CONSUM = 40;
  const d = (x) => '$' + x.toFixed(0);
  const n = (x) => Math.round(x).toLocaleString('en-US');
  root.innerHTML = '<label for="rc-people">People</label>'
    + '<div class="slider-row"><input id="rc-people" type="range" min="1" max="8" step="1" value="4"><span class="slider-val" data-p style="min-width:72px"></span></div>'
    + '<label for="rc-hard">Hardness (gpg)</label>'
    + '<div class="slider-row"><input id="rc-hard" type="range" min="1" max="40" step="1" value="10"><span class="slider-val" data-h style="min-width:72px"></span></div>'
    + '<label for="rc-elec">Your electricity rate (cents/kWh &mdash; US average 18.83)</label>'
    + '<div class="slider-row"><input id="rc-elec" type="range" min="12" max="47" step="0.5" value="18.5"><span class="slider-val" data-e style="min-width:72px"></span></div>'
    + '<label for="rc-water">Water + sewer ($ per 1,000 gallons)</label>'
    + '<div class="slider-row"><input id="rc-water" type="range" min="5" max="30" step="1" value="18"><span class="slider-val" data-w style="min-width:72px"></span></div>'
    + '<label for="rc-salt">Salt ($ per 40-lb bag)</label>'
    + '<div class="slider-row"><input id="rc-salt" type="range" min="4" max="14" step="0.5" value="7"><span class="slider-val" data-s style="min-width:72px"></span></div>'
    + '<div class="mc-out"><table style="width:100%;border-collapse:collapse;font-size:14px;margin-bottom:10px">'
    + '<tr><td style="padding:3px 0">Electricity <span style="color:#5B6B75">(~70 kWh/yr)</span></td><td class="num" style="text-align:right;font-variant-numeric:tabular-nums" data-c-elec></td></tr>'
    + '<tr><td style="padding:3px 0">Salt</td><td class="num" style="text-align:right;font-variant-numeric:tabular-nums" data-c-salt></td></tr>'
    + '<tr><td style="padding:3px 0">Regeneration water + sewer</td><td class="num" style="text-align:right;font-variant-numeric:tabular-nums" data-c-water></td></tr>'
    + '<tr><td style="padding:3px 0">Consumables &amp; routine service</td><td class="num" style="text-align:right;font-variant-numeric:tabular-nums" data-c-con></td></tr>'
    + '</table><strong data-c-total class="fig" style="font-size:20px"></strong><br>'
    + '<span data-c-mo style="font-size:15px;color:#16303F"></span><br>'
    + '<span data-c-punch style="font-size:14px;color:#5B6B75;display:inline-block;margin-top:8px"></span><br>'
    + '<span data-c-warn style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:6px"></span></div>';
  const els = ['rc-people','rc-hard','rc-elec','rc-water','rc-salt'].map(i => root.querySelector('#' + i));
  const update = () => {
    const [people, hard, cents, wrate, bag] = els.map(e => +e.value);
    const daily = people * GPD * hard;
    const weekly = daily * 7;
    const unit = LADDER.find(u => u.name * EFF >= weekly) || LADDER[LADDER.length - 1];
    const cap = unit.name * EFF;
    const regens = (daily * 365) / cap;
    const elec = KWH * (cents / 100);
    const saltLbs = regens * unit.cuft * LEAN;
    const salt = (saltLbs / 40) * bag;
    const gals = regens * GALREGEN;
    const water = (gals / 1000) * wrate;
    const total = elec + salt + water + CONSUM;
    const pct = Math.round((elec / total) * 100);
    root.querySelector('[data-p]').textContent = people;
    root.querySelector('[data-h]').textContent = hard + ' gpg';
    root.querySelector('[data-e]').textContent = cents.toFixed(1) + '\u00a2';
    root.querySelector('[data-w]').textContent = '$' + wrate;
    root.querySelector('[data-s]').textContent = '$' + bag.toFixed(2);
    root.querySelector('[data-c-elec]').textContent = d(elec);
    root.querySelector('[data-c-salt]').textContent = d(salt) + '  (' + n(saltLbs) + ' lbs)';
    root.querySelector('[data-c-water]').textContent = d(water) + '  (' + n(gals) + ' gal)';
    root.querySelector('[data-c-con]').textContent = d(CONSUM);
    root.querySelector('[data-c-total]').textContent = d(total) + ' a year to run';
    root.querySelector('[data-c-mo]').textContent = 'About ' + d(total / 12) + ' a month \u00b7 regenerating roughly ' + regens.toFixed(0) + ' times a year';
    root.querySelector('[data-c-punch]').textContent = 'Electricity is ' + pct + '% of it. The question that brought you here is the smallest number on the list \u2014 and the water going down the drain during regeneration costs you ' + (water > elec ? 'more' : 'about the same') + '.';
    root.querySelector('[data-c-warn]').textContent = regens > 61
      ? 'At ' + regens.toFixed(0) + ' regenerations a year this system is cycling every ' + (365 / regens).toFixed(1) + ' days \u2014 inside a week. That is a sizing problem, not a running-cost problem: it needs more capacity or a twin.'
      : 'Excludes the purchase price, installation, and the big-ticket repairs \u2014 which are annualised separately below.';
    root.setAttribute('data-result', JSON.stringify({ people, hard, cents, elec: +elec.toFixed(2), salt: +salt.toFixed(2), water: +water.toFixed(2), gals: Math.round(gals), consumables: CONSUM, total: +total.toFixed(2), monthly: +(total / 12).toFixed(2), elecPct: pct, regens: +regens.toFixed(1) }));
  };
  els.forEach(e => e.addEventListener('input', update));
  update();
}

document.querySelectorAll('[data-sizer]').forEach(mountSizer);
export function mountDecade(root) {
  root.classList.add('mini-calc');
  const LADDER = [
    { name: 24000, cuft: 0.75 }, { name: 32000, cuft: 1.0 }, { name: 40000, cuft: 1.25 },
    { name: 48000, cuft: 1.5 }, { name: 64000, cuft: 2.0 }, { name: 80000, cuft: 2.5 },
  ];
  const EFF = 0.65, GPD = 75, LEAN = 6, KWH = 70, CENTS = 18.83, GALREGEN = 27.5,
        WRATE = 18, BAG = 7, CONSUM = 40, REBUILD = 570, REBED = 295;
  const state = { rep: 'typical' };
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  root.innerHTML = '<label for="dc-up">What you pay up front (equipment + installation)</label>'
    + '<div class="slider-row"><input id="dc-up" type="range" min="800" max="9000" step="100" value="2500"><span class="slider-val" data-u style="min-width:80px"></span></div>'
    + '<label for="dc-people">People</label>'
    + '<div class="slider-row"><input id="dc-people" type="range" min="1" max="8" step="1" value="4"><span class="slider-val" data-p style="min-width:80px"></span></div>'
    + '<label for="dc-hard">Hardness (gpg)</label>'
    + '<div class="slider-row"><input id="dc-hard" type="range" min="1" max="40" step="1" value="10"><span class="slider-val" data-h style="min-width:80px"></span></div>'
    + '<label for="dc-years">Years you expect to own it</label>'
    + '<div class="slider-row"><input id="dc-years" type="range" min="5" max="15" step="1" value="10"><span class="slider-val" data-y style="min-width:80px"></span></div>'
    + '<div class="seg" role="group" aria-label="Repair assumption">'
    + '<button type="button" data-rep="none" aria-pressed="false">No major repairs</button>'
    + '<button type="button" data-rep="typical" aria-pressed="true">Typical</button>'
    + '<button type="button" data-rep="heavy" aria-pressed="false">Rough ride</button></div>'
    + '<div class="mc-out"><strong data-total class="fig" style="font-size:24px"></strong><br>'
    + '<span data-per style="font-size:15px;color:#16303F;display:inline-block;margin-top:4px"></span><br>'
    + '<span data-split style="font-size:14px;color:#5B6B75;display:inline-block;margin-top:8px"></span><br>'
    + '<span data-punch style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px;font-weight:600"></span></div>';
  const uIn = root.querySelector('#dc-up'), pIn = root.querySelector('#dc-people'),
        hIn = root.querySelector('#dc-hard'), yIn = root.querySelector('#dc-years');
  const update = () => {
    const up = +uIn.value, people = +pIn.value, hard = +hIn.value, years = +yIn.value;
    const daily = people * GPD * hard;
    const unit = LADDER.find(u => u.name * EFF >= daily * 7) || LADDER[LADDER.length - 1];
    const regens = (daily * 365) / (unit.name * EFF);
    const salt = (regens * unit.cuft * LEAN / 40) * BAG;
    const water = (regens * GALREGEN / 1000) * WRATE;
    const elec = KWH * (CENTS / 100);
    const runYr = salt + water + elec + CONSUM;
    const rebed = REBED * unit.cuft;
    let rep = 0;
    if (state.rep === 'typical') rep = (years >= 7 ? REBUILD : 0) + (years >= 10 ? rebed : 0);
    if (state.rep === 'heavy') rep = (years >= 5 ? REBUILD : 0) + (years >= 8 ? rebed : 0) + (years >= 6 ? 500 : 0) + (years >= 13 ? REBUILD : 0);
    const running = runYr * years;
    const total = up + running + rep;
    const pct = Math.round((up / total) * 100);
    root.querySelector('[data-u]').textContent = d(up);
    root.querySelector('[data-p]').textContent = people;
    root.querySelector('[data-h]').textContent = hard + ' gpg';
    root.querySelector('[data-y]').textContent = years + ' yrs';
    root.querySelector('[data-total]').textContent = d(total) + ' over ' + years + ' years';
    root.querySelector('[data-per]').textContent = d(total / years) + ' a year \u00b7 ' + d(total / years / 12) + ' a month \u00b7 $' + (total / years / 365).toFixed(2) + ' a day';
    root.querySelector('[data-split]').textContent = 'Up front ' + d(up) + '  \u00b7  running ' + d(running) + ' (' + d(runYr) + '/yr)  \u00b7  repairs ' + d(rep);
    root.querySelector('[data-punch]').textContent = pct + '% of it was decided the day you bought. Everything you will actually notice \u2014 the salt, the water, the power \u2014 is the other ' + (100 - pct) + '%.';
    root.setAttribute('data-result', JSON.stringify({ up, people, hard, years, rep: state.rep, runYr: +runYr.toFixed(2), running: +running.toFixed(2), repairs: +rep.toFixed(2), total: +total.toFixed(2), upfrontPct: pct, perDay: +(total / years / 365).toFixed(2) }));
  };
  root.querySelectorAll('[data-rep]').forEach(b => b.addEventListener('click', () => {
    state.rep = b.dataset.rep;
    root.querySelectorAll('[data-rep]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  [uIn, pIn, hIn, yIn].forEach(e => e.addEventListener('input', update));
  update();
}

document.querySelectorAll('[data-run-cost]').forEach(mountRunCost);
export function mountRepairReplace(root) {
  root.classList.add('mini-calc');
  const PART = {
    resin:  { label: 'Resin exhausted or fouled', cost: 340, buys: 9 },
    valve:  { label: 'Control valve failing',     cost: 570, buys: 8 },
    both:   { label: 'Both \u2014 a full rebuild',    cost: 840, buys: 10 },
    tank:   { label: 'Cracked mineral tank',      cost: 0,   buys: 0 },
  };
  const state = { part: 'resin' };
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  root.innerHTML = '<div class="seg" role="group" aria-label="What failed" style="margin-bottom:12px">'
    + '<button type="button" data-part="resin" aria-pressed="true">Resin</button>'
    + '<button type="button" data-part="valve" aria-pressed="false">Control valve</button>'
    + '<button type="button" data-part="both" aria-pressed="false">Both</button>'
    + '<button type="button" data-part="tank" aria-pressed="false">Cracked tank</button></div>'
    + '<label for="rr-age">How old is the system?</label>'
    + '<div class="slider-row"><input id="rr-age" type="range" min="1" max="25" step="1" value="12"><span class="slider-val" data-a style="min-width:74px"></span></div>'
    + '<label for="rr-fix">The repair quote</label>'
    + '<div class="slider-row"><input id="rr-fix" type="range" min="150" max="1500" step="10" value="340"><span class="slider-val" data-f style="min-width:74px"></span></div>'
    + '<label for="rr-buys">Years you think the repair buys</label>'
    + '<div class="slider-row"><input id="rr-buys" type="range" min="1" max="12" step="1" value="9"><span class="slider-val" data-b style="min-width:74px"></span></div>'
    + '<label for="rr-new">The replacement quote (installed)</label>'
    + '<div class="slider-row"><input id="rr-new" type="range" min="1200" max="8000" step="100" value="2500"><span class="slider-val" data-n style="min-width:74px"></span></div>'
    + '<label for="rr-life">Expected life of the new system</label>'
    + '<div class="slider-row"><input id="rr-life" type="range" min="8" max="20" step="1" value="12"><span class="slider-val" data-l style="min-width:74px"></span></div>'
    + '<div class="mc-out"><span style="font-size:14px;color:#5B6B75">Cost per year of service</span><br>'
    + '<strong data-verdict class="fig" style="font-size:20px;display:inline-block;margin-top:4px"></strong><br>'
    + '<span data-compare style="font-size:15px;color:#16303F;display:inline-block;margin-top:6px"></span><br>'
    + '<span data-rule style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:10px"></span><br>'
    + '<span data-warn style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:6px"></span></div>';
  const aIn = root.querySelector('#rr-age'), fIn = root.querySelector('#rr-fix'),
        bIn = root.querySelector('#rr-buys'), nIn = root.querySelector('#rr-new'), lIn = root.querySelector('#rr-life');
  const update = () => {
    const age = +aIn.value, fix = +fIn.value, buys = +bIn.value, nw = +nIn.value, life = +lIn.value;
    const fixPer = fix / buys, newPer = nw / life;
    const ratio = newPer / fixPer;
    const tank = state.part === 'tank';
    root.querySelector('[data-a]').textContent = age + ' yrs';
    root.querySelector('[data-f]').textContent = d(fix);
    root.querySelector('[data-b]').textContent = buys + ' yrs';
    root.querySelector('[data-n]').textContent = d(nw);
    root.querySelector('[data-l]').textContent = life + ' yrs';
    root.querySelector('[data-verdict]').textContent = tank
      ? 'Replace \u2014 this is the one repair that is not worth it'
      : 'Repair: ' + d(fixPer) + '/yr  \u00b7  Replace: ' + d(newPer) + '/yr';
    root.querySelector('[data-compare]').textContent = tank
      ? 'A cracked mineral tank is the failure that ends a softener honestly. Everything else in the cabinet is a part.'
      : (fixPer < newPer
          ? 'The repair buys a year of soft water for ' + ratio.toFixed(1) + '\u00d7 less than the new system does. On these numbers, fix it.'
          : 'The repair costs more per year of service than the replacement does. On these numbers, replace it.');
    const half = fix > 0.5 * nw;
    root.querySelector('[data-rule]').textContent = tank ? ''
      : (half
        ? 'The industry rule of thumb \u2014 replace once repairs pass 50% of a new unit \u2014 says replace. It has no denominator: it never asks how many years the repair buys. ' + (fixPer < newPer ? 'Here the arithmetic disagrees with the rule.' : 'Here the arithmetic happens to agree with it.')
        : 'Under the industry 50%-of-new rule this repair is comfortably worth doing \u2014 but the rule is not why. The cost per year of service is.');
    root.querySelector('[data-warn]').textContent = tank ? ''
      : (age >= 18
        ? 'At ' + age + ' years, the real question is not wear, it is parts. Before paying for anything, confirm the valve is a rebuildable industry-standard type and the parts still exist. If it is proprietary and unsupported, the repair is a bet you may not be able to place twice.'
        : 'Test the water before you spend anything. Iron above ~0.3 ppm and chlorine are what kill resin \u2014 replace the beads without fixing the cause and you buy the same failure again.');
    root.setAttribute('data-result', JSON.stringify({ part: state.part, age, fix, buys, nw, life, fixPerYear: +fixPer.toFixed(2), newPerYear: +newPer.toFixed(2), repairWins: !tank && fixPer < newPer, tank, ruleSaysReplace: half }));
  };
  root.querySelectorAll('[data-part]').forEach(b => b.addEventListener('click', () => {
    state.part = b.dataset.part;
    root.querySelectorAll('[data-part]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    const p = PART[state.part];
    if (p.cost) { fIn.value = p.cost; bIn.value = p.buys; }
    update();
  }));
  [aIn, fIn, bIn, nIn, lIn].forEach(e => e.addEventListener('input', update));
  update();
}

document.querySelectorAll('[data-decade]').forEach(mountDecade);
export function mountSchedule(root) {
  root.classList.add('mini-calc');
  const LADDER = [
    { name: 24000, cuft: 0.75 }, { name: 32000, cuft: 1.0 }, { name: 40000, cuft: 1.25 },
    { name: 48000, cuft: 1.5 }, { name: 64000, cuft: 2.0 }, { name: 80000, cuft: 2.5 },
  ];
  const EFF = 0.65, GPD = 75, LEAN = 6;
  const state = { sys: 'salt', src: 'city' };
  root.innerHTML = '<div class="seg" role="group" aria-label="System type" style="margin-bottom:8px">'
    + '<button type="button" data-sys="salt" aria-pressed="true">Salt-based softener</button>'
    + '<button type="button" data-sys="saltfree" aria-pressed="false">Salt-free conditioner</button></div>'
    + '<div class="seg" role="group" aria-label="Water source" style="margin-bottom:10px">'
    + '<button type="button" data-src="city" aria-pressed="true">City water</button>'
    + '<button type="button" data-src="well" aria-pressed="false">Well water</button></div>'
    + '<label for="sc-people">People</label>'
    + '<div class="slider-row"><input id="sc-people" type="range" min="1" max="8" step="1" value="4"><span class="slider-val" data-p style="min-width:70px"></span></div>'
    + '<label for="sc-hard">Hardness (gpg)</label>'
    + '<div class="slider-row"><input id="sc-hard" type="range" min="1" max="40" step="1" value="10"><span class="slider-val" data-h style="min-width:70px"></span></div>'
    + '<label for="sc-iron">Iron (ppm)</label>'
    + '<div class="slider-row"><input id="sc-iron" type="range" min="0" max="6" step="0.1" value="0"><span class="slider-val" data-i style="min-width:70px"></span></div>'
    + '<div class="mc-out"><strong data-head style="font-size:15px;display:inline-block;margin-bottom:8px"></strong>'
    + '<ul data-list style="margin:0 0 10px;padding-left:18px;font-size:14px;line-height:1.75"></ul>'
    + '<span data-tally class="fig" style="font-size:16px"></span><br>'
    + '<span data-pro style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:8px"></span></div>';
  const pIn = root.querySelector('#sc-people'), hIn = root.querySelector('#sc-hard'), iIn = root.querySelector('#sc-iron');
  const update = () => {
    const people = +pIn.value, hard = +hIn.value, iron = +iIn.value;
    const well = state.src === 'well';
    const dirty = well || iron >= 0.3;
    root.querySelector('[data-p]').textContent = people;
    root.querySelector('[data-h]').textContent = hard + ' gpg';
    root.querySelector('[data-i]').textContent = iron.toFixed(1) + ' ppm';
    const tasks = [];
    let mins = 0, consum = 0;
    if (state.sys === 'saltfree') {
      tasks.push('<strong>Replace the sediment prefilter</strong> \u2014 every 6\u201312 months. This is the job.');
      tasks.push('<strong>Test your water once a year</strong> \u2014 a conditioner controls scale, it does not remove hardness, so the gpg reading will not drop. You are checking that nothing else changed.');
      if (well) tasks.push('<strong>On a well:</strong> keep sediment and iron off the media \u2014 pretreatment matters more here than any maintenance task.');
      mins = 35; consum = 60;
      root.querySelector('[data-head]').textContent = 'Your maintenance schedule \u2014 salt-free conditioner';
      root.querySelector('[data-tally]').textContent = 'About ' + mins + ' minutes a year, roughly $' + consum + ' in filters.';
      root.querySelector('[data-pro]').textContent = 'No salt. No brine tank. No regeneration. There is genuinely almost nothing to maintain \u2014 which is the honest case for a conditioner, and the honest limit of one: it is not softening your water, it is conditioning the scale.';
    } else {
      const daily = people * GPD * hard;
      const unit = LADDER.find(u => u.name * EFF >= daily * 7) || LADDER[LADDER.length - 1];
      const regens = (daily * 365) / (unit.name * EFF);
      const lbs = regens * unit.cuft * LEAN;
      const bags = lbs / 40;
      const weeks = bags > 0 ? 52 / bags : 52;
      tasks.push('<strong>Look at the salt \u2014 monthly.</strong> Salt should sit a few inches above the water. At your numbers you will empty roughly <strong>' + bags.toFixed(1) + ' bags a year</strong> \u2014 a 40-lb bag about every ' + weeks.toFixed(0) + ' weeks.');
      tasks.push('<strong>Feel for a bridge \u2014 every few months.</strong> Push a broom handle down through the salt. If it stops on a crust with a void underneath, break it. That crust is why a full tank can still fail to regenerate.');
      tasks.push('<strong>Clean the injector / venturi \u2014 ' + (dirty ? 'quarterly' : 'twice a year') + '.</strong> Warm soapy water, small brush, reassemble in the exact order it came apart. This is the part that actually clogs.');
      tasks.push('<strong>Resin cleaner \u2014 every ' + (iron >= 0.3 ? '3' : '6') + ' months.</strong> Into the brine well, then run a manual regeneration.' + (iron >= 0.3 ? ' Your iron reading is why this is on the short cycle.' : ''));
      tasks.push('<strong>Wash the brine tank \u2014 when it is dirty' + (dirty ? ', realistically about once a year on your water' : ', which for most city-water homes is every year or two') + '.</strong> Not on a calendar. Look in it.');
      tasks.push('<strong>Test your water \u2014 quarterly.</strong> The only task that tells you whether the other five worked.');
      mins = 135 + (dirty ? 45 : 0);
      consum = 30 + (iron >= 0.3 ? 20 : 0);
      root.querySelector('[data-head]').textContent = 'Your maintenance schedule \u2014 salt-based softener' + (well ? ', well water' : '');
      root.querySelector('[data-tally]').textContent = 'About ' + (mins / 60).toFixed(1) + ' hours a year, plus roughly $' + consum + ' in consumables \u2014 on top of the salt.';
      root.querySelector('[data-pro]').textContent = (iron >= 0.3
        ? 'At ' + iron.toFixed(1) + ' ppm, iron is fouling the resin faster than any cleaner can keep up with. Maintenance is not the fix here \u2014 an iron filter ahead of the softener is. '
        : '') + 'Call a professional for: electrical faults, a valve that will not cycle, leaks from anything under pressure, or hard water that persists after you have cleaned everything above. Those are repairs, not maintenance.';
    }
    root.querySelector('[data-list]').innerHTML = tasks.map(t => '<li>' + t + '</li>').join('');
    root.setAttribute('data-result', JSON.stringify({ sys: state.sys, src: state.src, people, hard, iron, tasks: tasks.length, minutes: mins, consumables: consum }));
  };
  root.querySelectorAll('[data-sys]').forEach(b => b.addEventListener('click', () => {
    state.sys = b.dataset.sys;
    root.querySelectorAll('[data-sys]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  root.querySelectorAll('[data-src]').forEach(b => b.addEventListener('click', () => {
    state.src = b.dataset.src;
    root.querySelectorAll('[data-src]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  [pIn, hIn, iIn].forEach(e => e.addEventListener('input', update));
  update();
}

document.querySelectorAll('[data-repair-replace]').forEach(mountRepairReplace);
export function mountTriage(root) {
  root.classList.add('mini-calc');
  const SYM = {
    bridge: { label: 'Hard water \u2014 but the salt tank still looks full', verdict: 'Do not call anybody yet', cls: 'diy',
      body: 'This is a salt bridge until proven otherwise: a crust across the salt with a void under it, so the salt never reaches the water. Full tank, hard water, no brine. Push a broom handle down through the salt, break the crust, run a manual regeneration.', cost: 'Cost to fix: a broom handle.' },
    salt: { label: 'Salt IS going down, but the water is hard', verdict: 'Test before you call', cls: 'test',
      body: 'The system is regenerating and still failing, so the salt is not the problem. Either the hardness setting is wrong, the resin is spent or fouled, or the injector is drawing weakly. Clean the injector and dose a resin cleaner first \u2014 both are free-ish. If it is still hard after that, now you have a real diagnostic question and a technician is worth paying.', cost: 'Cost to try first: about $15.' },
    leak: { label: 'It is leaking', verdict: 'Call. Today.', cls: 'call',
      body: 'Anything leaking under pressure is not a maintenance job. Put the unit on bypass, which usually restores hard water to the house and stops the leak, and then book someone. This is exactly the kind of visit a service call exists for.', cost: 'Expect a service call at $40\u2013$100, plus repair at $150\u2013$600 if a part has failed.' },
    dead: { label: 'No display, or it will not regenerate at all', verdict: 'This is what a service call is for', cls: 'call',
      body: 'Electrical fault, failed motor, or a control valve that will not cycle. There is nothing in the DIY list that fixes this and guessing at it can turn a $200 repair into a new system. Check the obvious first \u2014 is it plugged in, is the bypass open \u2014 then book a diagnostic.', cost: 'Service call $40\u2013$100; typical repair $150\u2013$600 all in.' },
    unsure: { label: 'Something is off but I cannot tell what', verdict: 'Buy the test, not the truck', cls: 'test',
      body: 'A technician\u2019s first move is to test your water. You can do that yourself this afternoon. Test the raw water and the treated water: if treated hardness is near zero, the softener is working and your problem is somewhere else. If it is not, you now know something a phone call cannot tell you \u2014 and you can say it out loud when you book.', cost: 'A test kit is $10\u2013$25. Some companies bill $100\u2013$300 for the same information.' },
  };
  const state = { sym: 'bridge' };
  root.innerHTML = '<div class="seg" role="group" aria-label="What is happening" style="margin-bottom:12px;flex-wrap:wrap">'
    + Object.keys(SYM).map((k, i) => '<button type="button" data-sym="' + k + '" aria-pressed="' + (i === 0 ? 'true' : 'false') + '">' + SYM[k].label + '</button>').join('')
    + '</div>'
    + '<label for="tr-fee">The trip or diagnostic fee you were quoted on the phone</label>'
    + '<div class="slider-row"><input id="tr-fee" type="range" min="0" max="350" step="5" value="0"><span class="slider-val" data-f style="min-width:96px"></span></div>'
    + '<div class="mc-out"><strong data-verdict class="fig" style="font-size:19px"></strong><br>'
    + '<span data-body style="font-size:14.5px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.6"></span><br>'
    + '<span data-cost style="font-size:14px;color:#5B6B75;display:inline-block;margin-top:8px;font-weight:600"></span><br>'
    + '<span data-fee style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:10px"></span></div>';
  const fIn = root.querySelector('#tr-fee');
  const update = () => {
    const s = SYM[state.sym];
    const fee = +fIn.value;
    root.querySelector('[data-verdict]').textContent = s.verdict;
    root.querySelector('[data-body]').textContent = s.body;
    root.querySelector('[data-cost]').textContent = s.cost;
    root.querySelector('[data-f]').textContent = fee === 0 ? 'not quoted' : '$' + fee;
    let msg;
    if (fee === 0) {
      msg = 'They would not give you a number? That is the whole problem. The trip charge is knowable before anyone drives anywhere \u2014 ask for it, ask whether it is credited against the repair, and ask the hourly rate after the first hour. A company that will not quote a trip charge is not protecting you from uncertainty; it is protecting itself from comparison.';
    } else if (fee <= 100) {
      msg = '$' + fee + ' sits inside the published range for a softener service call and inspection ($40\u2013$100, parts not included). That is a fair number. Now ask the second question: is it credited against the repair if you go ahead?';
    } else if (fee <= 180) {
      msg = '$' + fee + ' is above the softener-specific service-call range ($40\u2013$100) but within what is published for a billed diagnostic hour ($65\u2013$180). Ask what it actually includes \u2014 and whether it comes off the repair.';
    } else {
      msg = '$' + fee + ' is above every published range on this page for a routine visit. It is not necessarily wrong \u2014 emergency and after-hours work carries a $75\u2013$350 surcharge on top of hourly rates that run 2\u20133\u00d7 normal \u2014 but you should be told which of those you are buying, out loud, before the truck moves.';
    }
    root.querySelector('[data-fee]').textContent = msg;
    root.setAttribute('data-result', JSON.stringify({ symptom: state.sym, verdict: s.verdict, cls: s.cls, fee, feeInRange: fee > 0 && fee <= 100 }));
  };
  root.querySelectorAll('[data-sym]').forEach(b => b.addEventListener('click', () => {
    state.sym = b.dataset.sym;
    root.querySelectorAll('[data-sym]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  fIn.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-schedule]').forEach(mountSchedule);
export function mountQuoteDecoder(root) {
  root.classList.add('mini-calc');
  const SYM = {
    bridge: { label: 'Salt is not going down &amp; water is hard', cause: 'A salt bridge \u2014 a crust across the salt with a void underneath, so no brine forms. HomeGuide names this as one of the most common softener "faults".', repair: false, band: 'Cost: a broom handle. This is not a repair.', ask: 'If a technician quotes you a part for this, ask them to show you the bridge first.' },
    flood: { label: 'Brine tank full of water / not draining', cause: 'Per HomeGuide: float valve set too high, a clogged drain line or injector, salt mushing, or a broken entry valve. The tank should fill no higher than 10\u201312 inches.', repair: false, band: 'Usually $0\u2013$20. A float switch, if it truly failed, is a small part.', ask: 'Ask them to check the float height and the drain line before quoting any part.' },
    norgen: { label: 'It will not regenerate at all', cause: 'Per HomeGuide: a broken or misconfigured timer, a blocked drain hose, or a plugged injector/venturi \u2014 and "in rare cases" the motor. Note the order: the cheap causes come first, and the motor is explicitly rare.', repair: true, band: 'Anywhere from $0 (a clog) to a control-board or motor replacement inside the $150\u2013$600 repair band.', ask: 'Ask: did you clear the injector and the drain line before concluding it was the motor?' },
    leak: { label: 'It is leaking', repair: true, cause: 'Per HomeGuide: a loose water-line connection, worn rotor-valve SEALS, or a cracked tank. Those three have wildly different prices \u2014 and the seals are a rebuild-kit job, not a new-valve job.', band: 'Loose fitting: near zero. Worn seals: a ~$100 rebuild kit plus labour. Cracked tank: $150\u2013$500 for the tank.', ask: 'Ask WHICH of the three it is, and if it is the seals, ask why a rebuild kit will not do.' },
    pressure: { label: 'Low water pressure through the house', repair: true, cause: 'Per HomeGuide: fouled or clogged resin, iron and sediment, a clogged prefilter \u2014 or a system that was simply sized too small, which is not a fault at all.', band: 'Resin replacement $200\u2013$400. But if it is sizing, no repair fixes it.', ask: 'Ask them to test your hardness and iron before touching the resin \u2014 replacing fouled resin without removing the iron buys the same failure again.' },
    beads: { label: 'Resin beads coming out of the taps', repair: true, cause: 'Per HomeGuide: a broken screen, a failed seal, or a cracked basket / upper distributor \u2014 typically where chlorine has eaten the plastic. This one is real.', band: 'The broken part plus resin: expect the $200\u2013$400 resin line on top of the repair.', ask: 'Ask whether a carbon prefilter goes in front of the new resin \u2014 otherwise the chlorine eats that too.' },
  };
  const state = { sym: 'bridge' };
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  root.innerHTML = '<div class="seg" role="group" aria-label="Symptom" style="margin-bottom:12px;flex-wrap:wrap">'
    + Object.keys(SYM).map((k, i) => '<button type="button" data-sym="' + k + '" aria-pressed="' + (i === 0 ? 'true' : 'false') + '">' + SYM[k].label + '</button>').join('')
    + '</div>'
    + '<label for="qd-quote">The repair quote you were given</label>'
    + '<div class="slider-row"><input id="qd-quote" type="range" min="0" max="1500" step="10" value="0"><span class="slider-val" data-q style="min-width:96px"></span></div>'
    + '<label for="qd-new">A comparable replacement, installed</label>'
    + '<div class="slider-row"><input id="qd-new" type="range" min="700" max="3000" step="50" value="1500"><span class="slider-val" data-n style="min-width:96px"></span></div>'
    + '<div class="mc-out"><strong data-cause style="font-size:14.5px;display:inline-block;line-height:1.6"></strong><br>'
    + '<span data-band class="fig" style="font-size:15px;display:inline-block;margin-top:8px"></span><br>'
    + '<span data-ask style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:6px"></span><br>'
    + '<span data-quote style="font-size:14px;color:#16303F;display:inline-block;margin-top:10px;font-weight:600"></span><br>'
    + '<span data-pct style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:6px"></span></div>';
  const qIn = root.querySelector('#qd-quote'), nIn = root.querySelector('#qd-new');
  const update = () => {
    const s = SYM[state.sym];
    const q = +qIn.value, nw = +nIn.value;
    const pct = nw > 0 ? (q / nw) * 100 : 0;
    root.querySelector('[data-cause]').innerHTML = s.cause;
    root.querySelector('[data-band]').textContent = s.band;
    root.querySelector('[data-ask]').textContent = 'Ask this: ' + s.ask;
    root.querySelector('[data-q]').textContent = q === 0 ? 'none yet' : d(q);
    root.querySelector('[data-n]').textContent = d(nw);
    let qmsg, pmsg;
    if (q === 0) {
      qmsg = 'No quote yet \u2014 which is the best position to be in. Read the cause above before anybody prices anything.';
      pmsg = '';
    } else {
      if (q <= 80) qmsg = d(q) + ' is inside the published inspection band ($40\u2013$80). You are paying to find out what is wrong, which is the one thing worth paying for.';
      else if (q <= 600) qmsg = d(q) + ' sits inside the published repair range of $150\u2013$600 (national average $430). That is a normal number \u2014 now make them itemise it.';
      else if (q <= 1000) qmsg = d(q) + ' is above the published repair range ($150\u2013$600) though below HomeGuide\u2019s stated maximum of $1,500. At this level ask specifically whether the control valve is being REBUILT or REPLACED \u2014 the parts differ by roughly 5\u00d7.';
      else qmsg = d(q) + ' is approaching the published maximum for any softener repair ($1,500) and is inside replacement territory. Get a second quote before you approve this one.';
      pmsg = 'That quote is ' + pct.toFixed(0) + '% of a ' + d(nw) + ' replacement. There is no magic threshold here \u2014 what matters is what it buys: ' + (pct < 25 ? 'at this level, a repair that restores a sound system is almost always the better arithmetic.' : pct < 50 ? 'weigh it against the system\u2019s age and its repair history, not against a rule of thumb.' : 'at this share, ask what the next failure will cost \u2014 and whether the parts for it will still exist.');
    }
    root.querySelector('[data-quote]').textContent = qmsg;
    root.querySelector('[data-pct]').textContent = pmsg;
    root.setAttribute('data-result', JSON.stringify({ symptom: state.sym, isRepair: s.repair, quote: q, replacement: nw, pctOfReplacement: +pct.toFixed(1) }));
  };
  root.querySelectorAll('[data-sym]').forEach(b => b.addEventListener('click', () => {
    state.sym = b.dataset.sym;
    root.querySelectorAll('[data-sym]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  [qIn, nIn].forEach(e => e.addEventListener('input', update));
  update();
}

document.querySelectorAll('[data-triage]').forEach(mountTriage);
export function mountSaltCost(root) {
  root.classList.add('mini-calc');
  const LADDER = [
    { name: 24000, cuft: 0.75 }, { name: 32000, cuft: 1.0 }, { name: 40000, cuft: 1.25 },
    { name: 48000, cuft: 1.5 }, { name: 64000, cuft: 2.0 }, { name: 80000, cuft: 2.5 },
  ];
  const EFF = 0.65, GPD = 75, LEAN = 6, REPAIR = 430;
  const TYPE = {
    rock:  { label: 'Rock salt',          purity: 0.965, price: 6,  extra: 1.0 },
    solar: { label: 'Solar pellets',      purity: 0.996, price: 7,  extra: 1.0 },
    evap:  { label: 'Evaporated pellets', purity: 0.999, price: 9,  extra: 1.0 },
    kcl:   { label: 'Potassium chloride', purity: 0.99,  price: 28, extra: 1.2 },
  };
  const state = { t: 'solar' };
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  const n = (x) => Math.round(x).toLocaleString('en-US');
  root.innerHTML = '<div class="seg" role="group" aria-label="Salt type" style="margin-bottom:12px;flex-wrap:wrap">'
    + Object.keys(TYPE).map(k => '<button type="button" data-t="' + k + '" aria-pressed="' + (k === 'solar' ? 'true' : 'false') + '">' + TYPE[k].label + '</button>').join('')
    + '</div>'
    + '<label for="sl-people">People</label>'
    + '<div class="slider-row"><input id="sl-people" type="range" min="1" max="8" step="1" value="4"><span class="slider-val" data-p style="min-width:70px"></span></div>'
    + '<label for="sl-hard">Hardness (gpg)</label>'
    + '<div class="slider-row"><input id="sl-hard" type="range" min="1" max="40" step="1" value="10"><span class="slider-val" data-h style="min-width:70px"></span></div>'
    + '<label for="sl-price">Price per 40-lb bag</label>'
    + '<div class="slider-row"><input id="sl-price" type="range" min="4" max="35" step="0.5" value="7"><span class="slider-val" data-pr style="min-width:70px"></span></div>'
    + '<div class="mc-out"><strong data-total class="fig" style="font-size:21px"></strong><br>'
    + '<span data-use style="font-size:14px;color:#5B6B75;display:inline-block;margin-top:6px"></span><br>'
    + '<span data-sludge style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px"></span><br>'
    + '<span data-verdict style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:8px;line-height:1.6"></span></div>';
  const pIn = root.querySelector('#sl-people'), hIn = root.querySelector('#sl-hard'), prIn = root.querySelector('#sl-price');
  const update = () => {
    const t = TYPE[state.t];
    const people = +pIn.value, hard = +hIn.value, price = +prIn.value;
    const daily = people * GPD * hard;
    const unit = LADDER.find(u => u.name * EFF >= daily * 7) || LADDER[LADDER.length - 1];
    const regens = (daily * 365) / (unit.name * EFF);
    const baseLbs = regens * unit.cuft * LEAN;
    const lbs = baseLbs * t.extra;
    const bags = lbs / 40;
    const yr = bags * price;
    const sludge10 = lbs * 10 * (1 - t.purity);
    root.querySelector('[data-p]').textContent = people;
    root.querySelector('[data-h]').textContent = hard + ' gpg';
    root.querySelector('[data-pr]').textContent = '$' + price.toFixed(2);
    root.querySelector('[data-total]').textContent = d(yr) + ' a year \u00b7 ' + d(yr * 10) + ' over ten';
    root.querySelector('[data-use]').textContent = n(lbs) + ' lbs = ' + bags.toFixed(1) + ' bags a year \u2014 one 40-lb bag about every ' + (52 / bags).toFixed(0) + ' weeks'
      + (t.extra > 1 ? ' (including the ~20% extra potassium chloride needs to do the same work)' : '');
    root.querySelector('[data-sludge]').textContent = 'Insoluble residue into your brine tank over ten years: ' + n(sludge10) + ' lbs';
    let v;
    if (state.t === 'rock') {
      const save = bags * (7 - price > 0 ? 7 - price : 0);
      const yrs = save > 0 ? REPAIR / save : 999;
      v = 'THE TRAP: at this price rock salt saves you about ' + d(save) + ' a year against solar pellets. One clogged injector \u2014 the documented consequence of exactly this residue \u2014 costs $430 at the national average. '
        + (save > 0 ? 'The cheap salt would need to run ' + Math.round(yrs) + ' years without a single incident to break even. The softener itself lasts 10\u201315.' : 'There is no saving here at all.');
    } else if (state.t === 'kcl') {
      v = 'Potassium chloride regenerates less efficiently \u2014 published guidance says raise your hardness setting 10\u201320% \u2014 so you buy more of a product that already costs several times as much. It is the right call for a genuine medical sodium restriction, or for septic and garden discharge. It is the wrong call simply because it is the expensive bag on the shelf.';
    } else if (state.t === 'evap') {
      v = 'The purest option: under 0.2% insoluble matter. Worth it on very hard water (15+ gpg) or if you want the brine tank to stay clean for years. On ordinary city water, solar pellets do nearly the same job for less.';
    } else {
      v = 'The sensible default for most households: 99.6% pure, pellets dissolve evenly and bridge far less than crystals, and the residue is a fraction of rock salt\u2019s. This is the salt I would put in my own tank.';
    }
    root.querySelector('[data-verdict]').textContent = v;
    root.setAttribute('data-result', JSON.stringify({ type: state.t, people, hard, price, lbs: Math.round(lbs), bags: +bags.toFixed(1), annual: +yr.toFixed(2), tenYear: +(yr * 10).toFixed(2), sludge10: +sludge10.toFixed(1) }));
  };
  root.querySelectorAll('[data-t]').forEach(b => b.addEventListener('click', () => {
    state.t = b.dataset.t;
    root.querySelectorAll('[data-t]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    prIn.value = TYPE[state.t].price;
    update();
  }));
  [pIn, hIn, prIn].forEach(e => e.addEventListener('input', update));
  update();
}

export function mountTechDecider(root) {
  root.classList.add('mini-calc');
  const state = { want: 'scale' };
  root.innerHTML = '<label style="display:block;margin-bottom:6px">What do you actually want?</label>'
    + '<div class="seg" role="group" aria-label="Desired outcome" style="margin-bottom:10px;flex-wrap:wrap">'
    + '<button type="button" data-want="scale" aria-pressed="true">Protect pipes &amp; appliances from scale</button>'
    + '<button type="button" data-want="soft" aria-pressed="false">Genuinely soft water \u2014 feel, spots, less soap</button>'
    + '<button type="button" data-want="both" aria-pressed="false">Both</button></div>'
    + '<label for="td-hard">Hardness (gpg)</label>'
    + '<div class="slider-row"><input id="td-hard" type="range" min="1" max="90" step="1" value="12"><span class="slider-val" data-h style="min-width:72px"></span></div>'
    + '<label for="td-iron">Iron (ppm)</label>'
    + '<div class="slider-row"><input id="td-iron" type="range" min="0" max="6" step="0.1" value="0"><span class="slider-val" data-i style="min-width:72px"></span></div>'
    + '<div class="mc-out"><strong data-verdict class="fig" style="font-size:19px"></strong><br>'
    + '<span data-body style="font-size:14.5px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.6"></span><br>'
    + '<span data-block style="font-size:13.5px;color:#B44A2E;display:inline-block;margin-top:8px;font-weight:600"></span><br>'
    + '<span data-run style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:8px"></span></div>';
  const hIn = root.querySelector('#td-hard'), iIn = root.querySelector('#td-iron');
  const update = () => {
    const hard = +hIn.value, iron = +iIn.value;
    root.querySelector('[data-h]').textContent = hard + ' gpg';
    root.querySelector('[data-i]').textContent = iron.toFixed(1) + ' ppm';
    // Pentair's OWN manual: iron/manganese/sulfur/tannin must be removed first; NaturSoft rated to 75 gpg max
    const ironBlocks = iron >= 0.3;
    const overSpec = hard > 75;
    let verdict, body, block = '', run;
    if (state.want === 'soft' || state.want === 'both') {
      verdict = 'You need ion exchange. A conditioner cannot do this.';
      body = 'Slippery-feeling water, no spots on the glassware and half the detergent are all consequences of hardness being REMOVED from the water. A salt-free conditioner does not remove it \u2014 it changes the shape of it so it will not stick. Pentair states this plainly in their own FAQ: the alternative "only addresses water hardness" scale, and they do not call it a softener.'
        + (state.want === 'both' ? ' If you want both outcomes, the salt softener already gives you both \u2014 it removes the hardness AND therefore the scale.' : '');
      run = 'Running cost of the salt route: roughly $151/yr on our own worksheet \u2014 mostly salt.';
    } else {
      if (overSpec) {
        verdict = 'Out of spec \u2014 for the conditioner, not for you.';
        body = 'At ' + hard + ' gpg you are past the 75 gpg maximum hardness Pentair publishes for NaturSoft in its own installation manual. That is not a marketing limit, it is theirs. At this hardness you are in salt territory.';
        run = '';
      } else if (ironBlocks) {
        verdict = 'A conditioner is the right idea \u2014 but not before you deal with the iron.';
        body = 'Scale protection without salt is a legitimate goal and the certified evidence behind it is real. But Pentair\u2019s own manual says iron, manganese, sulfur and tannin "should be removed prior" to the system. At ' + iron.toFixed(1) + ' ppm you have iron.';
        block = 'Fit an iron filter ahead of anything else, or the media you just bought is being fouled from day one.';
        run = 'Running cost once it is in: about $22\u2013$44/yr for prefilters, plus carbon media roughly every five years. No salt. No electricity. No wastewater.';
      } else {
        verdict = 'A salt-free conditioner is a legitimate answer here.';
        body = 'You want scale protection, not soft water \u2014 and that is exactly what this technology does. NaturSoft carries a DVGW certification for 99.6% scale prevention, which is the strongest independent performance evidence anyone in the salt-free category has. Your water will still test hard, because nothing was removed. If that is fine with you, this is a genuinely good fit.';
        run = 'Running cost: about $22\u2013$44/yr for prefilters, plus carbon media roughly every five years. Against roughly $151/yr for a salt softener \u2014 no salt, no electricity, no wastewater, no drain.';
      }
    }
    root.querySelector('[data-verdict]').textContent = verdict;
    root.querySelector('[data-body]').textContent = body;
    root.querySelector('[data-block]').textContent = block;
    root.querySelector('[data-run]').textContent = run;
    root.setAttribute('data-result', JSON.stringify({ want: state.want, hard, iron, needsSalt: state.want !== 'scale' || overSpec, ironBlocks, overSpec }));
  };
  root.querySelectorAll('[data-want]').forEach(b => b.addEventListener('click', () => {
    state.want = b.dataset.want;
    root.querySelectorAll('[data-want]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  [hIn, iIn].forEach(e => e.addEventListener('input', update));
  update();
}

export function mountHardness(root) {
  root.classList.add('mini-calc');
  root.innerHTML = '<label for="hz-zip">Your ZIP code</label>'
    + '<div class="slider-row"><input id="hz-zip" type="text" inputmode="numeric" maxlength="5" placeholder="e.g. 67501" '
    + 'style="flex:1;padding:10px 12px;border:1px solid #D9DED9;font-size:16px;font-family:inherit"></div>'
    + '<div class="mc-out"><strong data-hz-head class="fig" style="font-size:20px"></strong><br>'
    + '<span data-hz-band style="font-size:15px;color:#16303F;display:inline-block;margin-top:4px"></span><br>'
    + '<span data-hz-what style="font-size:14px;color:#5B6B75;display:inline-block;margin-top:8px;line-height:1.6"></span><br>'
    + '<span data-hz-caveat style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.6"></span></div>';
  const zIn = root.querySelector('#hz-zip');
  const update = () => {
    const d = hardnessDetailForZip(zIn.value);
    const head = root.querySelector('[data-hz-head]');
    if (!d) {
      head.textContent = 'Enter a 5-digit ZIP';
      root.querySelector('[data-hz-band]').textContent = '';
      root.querySelector('[data-hz-what]').textContent = '';
      root.querySelector('[data-hz-caveat]').textContent = '';
      root.setAttribute('data-result', JSON.stringify({ zip: zIn.value, found: false }));
      return;
    }
    head.textContent = d.lo + '\u2013' + d.hi + ' gpg  (' + d.state + ')';
    root.querySelector('[data-hz-band]').textContent = 'Typically ' + d.band + ' \u2014 USGS bands: soft to 3.5, moderately hard to 7, hard to 10.5, very hard above.';
    root.querySelector('[data-hz-what]').textContent = d.mid <= 3.5
      ? 'At this hardness the honest answer is often that you do not need a softener at all. Test before you buy anything \u2014 and be sceptical of anyone who tells you otherwise without a reading.'
      : d.mid <= 7
        ? 'Borderline. Scale forms slowly at this level. A softener is a preference here, not a necessity \u2014 size it on a real reading, not on this estimate.'
        : 'Hard enough that softening pays. Use the midpoint of ' + d.mid + ' gpg to size a system \u2014 then confirm with a real test, because the spread inside your own state is wider than the spread between many states.';
    root.querySelector('[data-hz-caveat]').textContent = 'This is a REGIONAL ESTIMATE from state-level data \u2014 it is not a measurement of your tap. Hardness varies between neighbouring towns, between wells and mains, and by season. Your utility publishes the real figure in its annual Consumer Confidence Report, free. A home test kit costs $10\u2013$25. Either beats a ZIP code.';
    root.setAttribute('data-result', JSON.stringify({ zip: zIn.value, found: true, state: d.state, lo: d.lo, hi: d.hi, mid: d.mid, band: d.band }));
  };
  zIn.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-quote-decoder]').forEach(mountQuoteDecoder);
export function mountTankCalc(root) {
  root.classList.add('mini-calc');
  const SYM = {
    brine: { label: 'The salt tank is cracked or leaking', comp: 'brine tank',
      cause: 'The brine tank is unpressurised plastic \u2014 the simplest, cheapest vessel in the whole system. Published replacement range: $125\u2013$700, and most residential tanks sit at the bottom of it.',
      note: 'This is a lift-and-swap job. Do not let anyone price a whole softener for a cracked salt tank.', tank: true },
    mineral: { label: 'The tall pressure tank is leaking from the body', comp: 'mineral tank',
      cause: 'First, dry everything and watch where the water actually starts \u2014 valve-seal drips run down the tank and impersonate a cracked vessel. If the body itself weeps or cracks, the tank is done: a fiberglass pressure vessel is not patchable.',
      note: 'A bare tank is $150\u2013$500 \u2014 but a PRE-LOADED tank (tank + resin + riser, assembled) publishes at $370\u2013$433, and your existing valve screws onto it.', tank: true },
    beads: { label: 'Resin beads are coming out of the taps', comp: 'riser / distributor basket',
      cause: 'The tank is almost certainly fine. Beads escape when the internal riser tube or its distributor basket cracks \u2014 usually chlorine-embrittled plastic. The vessel around it is intact.',
      note: 'A pre-loaded tank ($370\u2013$433) includes a new riser, basket AND fresh resin \u2014 often simpler than fishing a broken basket out of a 48-inch tube.', tank: true },
    hard: { label: 'Water is hard again \u2014 but nothing is leaking', comp: 'not the tank',
      cause: 'This is not a tank problem. A tank fails by leaking, cracking or shedding beads \u2014 it does not fail by softening less. Hard water with an intact tank is settings, a salt bridge, a clogged injector, or exhausted resin.',
      note: 'Work through the free checks first; if it is the resin, that is $200\u2013$400 \u2014 in the existing tank.', tank: false },
  };
  const state = { sym: 'brine' };
  root.innerHTML = '<div class="seg" role="group" aria-label="What is happening" style="margin-bottom:12px;flex-wrap:wrap">'
    + Object.keys(SYM).map((k, i) => '<button type="button" data-tk="' + k + '" aria-pressed="' + (i === 0 ? 'true' : 'false') + '">' + SYM[k].label + '</button>').join('')
    + '</div>'
    + '<label for="tk-age">Age of the softener</label>'
    + '<div class="slider-row"><input id="tk-age" type="range" min="0" max="25" step="1" value="6"><span class="slider-val" data-a style="min-width:80px"></span></div>'
    + '<div class="mc-out"><strong data-comp class="fig" style="font-size:18px"></strong><br>'
    + '<span data-cause style="font-size:14.5px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.6"></span><br>'
    + '<span data-note style="font-size:14px;color:#5B6B75;display:inline-block;margin-top:8px;font-weight:600;line-height:1.6"></span><br>'
    + '<span data-age-verdict style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.6"></span></div>';
  const aIn = root.querySelector('#tk-age');
  const update = () => {
    const s = SYM[state.sym];
    const age = +aIn.value;
    root.querySelector('[data-a]').textContent = age + ' yrs';
    root.querySelector('[data-comp]').textContent = s.tank ? 'Likely: the ' + s.comp : 'Likely: ' + s.comp;
    root.querySelector('[data-cause]').textContent = s.cause;
    root.querySelector('[data-note]').textContent = s.note;
    let v;
    if (!s.tank) {
      v = 'Age barely matters here \u2014 diagnose before spending. Our maintenance and repair guides walk the free checks in order.';
    } else if (state.sym === 'brine') {
      v = 'At any age, a brine tank is worth replacing on its own \u2014 it does not care how old the rest of the system is.';
    } else if (age >= 15) {
      v = 'At ' + age + ' years, think hard before putting a new pressure vessel under a valve of the same vintage. Published lifespan is 10\u201315 years, a complete system is $700\u2013$3,000 installed \u2014 price one before approving tank plus valve work on this unit.';
    } else if (age >= 10) {
      v = 'At ' + age + ' years you are inside the published 10\u201315-year lifespan band. A pre-loaded tank is a fair bet IF the valve is healthy \u2014 have its piston and seals checked while the system is apart, because that is a 48-month wear part.';
    } else {
      v = 'At ' + age + ' years the rest of the system has plenty left. Replacing the tank (or just the riser) restores it \u2014 this is exactly the repair-beats-replacement case.';
    }
    root.querySelector('[data-age-verdict]').textContent = v;
    root.setAttribute('data-result', JSON.stringify({ symptom: state.sym, component: s.comp, isTank: s.tank, age }));
  };
  root.querySelectorAll('[data-tk]').forEach(b => b.addEventListener('click', () => {
    state.sym = b.dataset.tk;
    root.querySelectorAll('[data-tk]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  aIn.addEventListener('input', update);
  update();
}

document.querySelectorAll('[data-hardness]').forEach(mountHardness);
export function mountBurden(root) {
  root.classList.add('mini-calc');
  const LADDER = [24, 32, 40, 48, 64, 80], EFF = 0.65, GPD = 75, LEAN = 6;
  const CUFT = { 24: 0.75, 32: 1.0, 40: 1.25, 48: 1.5, 64: 2.0, 80: 2.5 };
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  root.innerHTML = '<label for="bd-people">People</label>'
    + '<div class="slider-row"><input id="bd-people" type="range" min="1" max="8" step="1" value="4"><span class="slider-val" data-p style="min-width:70px"></span></div>'
    + '<label for="bd-hard">Hardness (gpg)</label>'
    + '<div class="slider-row"><input id="bd-hard" type="range" min="1" max="40" step="1" value="10"><span class="slider-val" data-h style="min-width:70px"></span></div>'
    + '<label for="bd-salt">Salt price per 40-lb bag</label>'
    + '<div class="slider-row"><input id="bd-salt" type="range" min="5" max="10" step="0.5" value="7"><span class="slider-val" data-s style="min-width:70px"></span></div>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:8px"><input id="bd-iron" type="checkbox"> Iron in the water (&ge;0.3 ppm)</label>'
    + '<div class="mc-out"><div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">'
    + '<div><strong style="font-size:13px;color:#5B6B75">SALT-BASED SOFTENER</strong><br><span data-sb-cash class="fig" style="font-size:19px"></span><br><span data-sb-detail style="font-size:13px;color:#5B6B75;line-height:1.6;display:inline-block;margin-top:4px"></span></div>'
    + '<div><strong style="font-size:13px;color:#5B6B75">SALT-FREE CONDITIONER</strong><br><span data-sf-cash class="fig" style="font-size:19px"></span><br><span data-sf-detail style="font-size:13px;color:#5B6B75;line-height:1.6;display:inline-block;margin-top:4px"></span></div>'
    + '</div><span data-verdict style="font-size:14px;color:#16303F;display:inline-block;margin-top:14px;line-height:1.65;font-weight:600"></span></div>';
  const pIn = root.querySelector('#bd-people'), hIn = root.querySelector('#bd-hard'), sIn = root.querySelector('#bd-salt'), iIn = root.querySelector('#bd-iron');
  const update = () => {
    const people = +pIn.value, hard = +hIn.value, salt = +sIn.value, iron = iIn.checked;
    root.querySelector('[data-p]').textContent = people;
    root.querySelector('[data-h]').textContent = hard + ' gpg';
    root.querySelector('[data-s]').textContent = '$' + salt.toFixed(2);
    const daily = people * GPD * hard;
    const tier = LADDER.find(t => t * 1000 * EFF >= daily * 7) || 80;
    const regens = (daily * 365) / (tier * 1000 * EFF);
    const bags = (regens * CUFT[tier] * LEAN) / 40;
    const saltCost = bags * salt;
    const sbCash = saltCost + 27.5 + 13 + 30;   // salt + cleaner/strips mid $27.50 + electricity $13 + regen water ~$30
    const sbAnnu = 25 + 30;                      // valve kit $100/4yr + resin $300/10yr
    const sfCash = 60;                           // prefilter cartridges
    const sfAnnu = 300 / 4.5;                    // TAC media $100-500 every 3-6 yrs, midpoints
    root.querySelector('[data-sb-cash]').textContent = d(sbCash) + '/yr cash';
    root.querySelector('[data-sb-detail]').innerHTML = bags.toFixed(1) + ' bags of salt (' + d(saltCost) + ') + consumables + utilities.<br>+' + d(sbAnnu) + '/yr annualised parts &middot; ~2\u00bc hrs of your time';
    root.querySelector('[data-sf-cash]').textContent = d(sfCash) + '/yr cash';
    root.querySelector('[data-sf-detail]').innerHTML = 'Prefilter cartridges only. No salt, no regeneration, $0 electricity.<br>+' + d(sfAnnu) + '/yr annualised media &middot; ~35 min of your time';
    let v;
    const gap = (sbCash + sbAnnu) - (sfCash + sfAnnu);
    if (hard <= 3) {
      v = 'At ' + hard + ' gpg, the honest answer is neither system \u2014 there is very little hardness to treat. Test before you buy anything.';
    } else if (iron) {
      v = 'Stop at the iron. TAC conditioning media is fouled by iron, and manufacturer specs commonly disqualify iron-bearing water outright \u2014 on this water the conditioner is ruled out before maintenance ever enters the comparison. Treat the iron first, then re-run this.';
    } else {
      v = 'On your numbers the conditioner runs about ' + d(gap) + ' a year less to keep \u2014 and about 2 hours less of your time. The catch is the outcome, not the upkeep: a conditioner controls scale; it does not remove hardness. If you want water that tests soft, the softener is the only one of these two that delivers it, and its maintenance bill is the price of that.';
    }
    root.querySelector('[data-verdict]').textContent = v;
    root.setAttribute('data-result', JSON.stringify({ people, hard, salt, iron, bags: +bags.toFixed(1), sbCash: Math.round(sbCash), sbAnnu: Math.round(sbAnnu), sfCash, sfAnnu: Math.round(sfAnnu), gap: Math.round(gap) }));
  };
  [pIn, hIn, sIn].forEach(e => e.addEventListener('input', update));
  iIn.addEventListener('change', update);
  update();
}

document.querySelectorAll('[data-tank-calc]').forEach(mountTankCalc);
export function mountPredict(root) {
  root.classList.add('mini-calc');
  const QS = [
    { k: 'prices', q: 'Can you see equipment prices before a salesperson visits your home?' },
    { k: 'parts', q: 'Are replacement parts and consumables sold publicly at retail?' },
    { k: 'diy', q: 'Does the manual let a competent homeowner do routine maintenance?' },
    { k: 'anyplumber', q: 'Can any local plumber service it, or only the brand\u2019s own network?' },
  ];
  const state = { prices: false, parts: false, diy: false, anyplumber: false };
  root.innerHTML = QS.map(x => '<label style="display:flex;gap:10px;align-items:flex-start;margin-top:10px;font-size:14.5px;line-height:1.5"><input type="checkbox" data-pq="' + x.k + '" style="margin-top:3px"> ' + x.q + '</label>').join('')
    + '<div class="mc-out"><strong data-rating class="fig" style="font-size:18px"></strong><br>'
    + '<span data-read style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.65"></span><br>'
    + '<span data-ask style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.6"></span></div>';
  const update = () => {
    const yes = Object.values(state).filter(Boolean).length;
    let rating, read;
    if (yes === 4) {
      rating = 'HIGH predictability';
      read = 'You can price the equipment, the consumables, the routine work and the labour before you spend a dollar. Whatever this system costs to own, you can compute it in advance \u2014 which is the whole game.';
    } else if (yes >= 2) {
      rating = 'MODERATE predictability';
      read = 'Part of the ownership cost is checkable in advance and part of it lives behind a quote. Budget the published half, and get the unpublished half \u2014 service rates, part prices, plan terms \u2014 in writing before you sign, not after.';
    } else {
      rating = 'DIFFICULT TO ESTIMATE';
      read = 'Almost nothing here can be priced before a sales conversation. Be clear-eyed about what that means: you are not just buying a machine, you are entering a service relationship \u2014 and the relationship, not the hardware, is what you need to price.';
    }
    const missing = [];
    if (!state.prices) missing.push('the installed price and every service rate, in writing');
    if (!state.parts) missing.push('what the three most common replacement parts cost, with part numbers');
    if (!state.diy) missing.push('which routine tasks void nothing if you do them yourself');
    if (!state.anyplumber) missing.push('what happens to service pricing once the warranty ends');
    root.querySelector('[data-rating]').textContent = rating;
    root.querySelector('[data-read]').textContent = read;
    root.querySelector('[data-ask]').textContent = missing.length
      ? 'Before signing, get: ' + missing.join('; ') + '.'
      : 'Nothing left to ask \u2014 the numbers are already public.';
    root.setAttribute('data-result', JSON.stringify({ yes, rating: rating.split(' ')[0] }));
  };
  root.querySelectorAll('[data-pq]').forEach(cb => cb.addEventListener('change', () => {
    state[cb.dataset.pq] = cb.checked; update();
  }));
  update();
}

document.querySelectorAll('[data-burden]').forEach(mountBurden);
export function mountFilterCost(root) {
  root.classList.add('mini-calc');
  const SYS = {
    none: { label: 'Just a softener \u2014 no separate housing', hasFilter: false,
      note: 'Then there may be NOTHING to replace. A standard ion-exchange softener contains resin and gravel, not a disposable cartridge. If an invoice says \u201csoftener filter,\u201d ask for the part number before paying \u2014 you may be looking at a resin job, a valve part, or a line item in search of a purpose.' },
    housing: { label: 'A cartridge housing on the pipe before it', hasFilter: true,
      note: 'That is a sediment prefilter \u2014 the classic 10-inch clear or blue housing. Standard sizes, published prices, and a five-minute DIY swap.' },
    bigblue: { label: 'A large \u201cBig Blue\u201d whole-house housing', hasFilter: true,
      note: 'Large-format 4.5\u2033 cartridges: more capacity, higher per-cartridge price, same standard threads and the same DIY procedure.' },
    prop: { label: 'A dealer-installed proprietary system', hasFilter: true,
      note: 'Then the cartridge price depends on the brand\u2019s dealer network, and many publish nothing. Get the MODEL and CARTRIDGE PART NUMBERS from the housing \u2014 many \u201cproprietary\u201d housings take standard-size cartridges, and that one fact can reprice your whole maintenance year.' },
  };
  const state = { sys: 'housing' };
  root.innerHTML = '<div class="seg" role="group" aria-label="What do you have" style="margin-bottom:12px;flex-wrap:wrap">'
    + Object.keys(SYS).map((k, i) => '<button type="button" data-fc="' + k + '" aria-pressed="' + (k === 'housing' ? 'true' : 'false') + '">' + SYS[k].label + '</button>').join('')
    + '</div>'
    + '<label for="fc-price">Cartridge price</label>'
    + '<div class="slider-row"><input id="fc-price" type="range" min="10" max="80" step="1" value="26"><span class="slider-val" data-pr style="min-width:70px"></span></div>'
    + '<label for="fc-freq">Changes per year</label>'
    + '<div class="slider-row"><input id="fc-freq" type="range" min="1" max="6" step="1" value="2"><span class="slider-val" data-fr style="min-width:70px"></span></div>'
    + '<div class="mc-out"><strong data-head class="fig" style="font-size:18px"></strong><br>'
    + '<span data-body style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.65"></span><br>'
    + '<span data-note style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.6"></span></div>';
  const pIn = root.querySelector('#fc-price'), fIn = root.querySelector('#fc-freq');
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  const update = () => {
    const s = SYS[state.sys], price = +pIn.value, freq = +fIn.value;
    root.querySelector('[data-pr]').textContent = d(price);
    root.querySelector('[data-fr]').textContent = freq + '\u00d7';
    if (!s.hasFilter) {
      root.querySelector('[data-head]').textContent = 'Possibly a $0 job';
      root.querySelector('[data-body]').textContent = 'Check for a cartridge housing before you budget for cartridges.';
    } else {
      const diy = price * freq, pro = (price + 70) * freq;
      root.querySelector('[data-head]').textContent = d(diy) + '/yr DIY \u00b7 ' + d(pro) + '/yr with a pro visit each time';
      root.querySelector('[data-body]').textContent = 'Five years: ' + d(diy * 5) + ' DIY vs ' + d(pro * 5) + ' pro \u2014 the gap is the $70 midpoint service call riding along ' + freq + ' time' + (freq > 1 ? 's' : '') + ' a year, not the cartridge. Changing it yourself even half the time keeps most of it.';
    }
    root.querySelector('[data-note]').textContent = s.note;
    root.setAttribute('data-result', JSON.stringify({ sys: state.sys, hasFilter: s.hasFilter, price, freq, diy: s.hasFilter ? price * freq : 0, pro: s.hasFilter ? (price + 70) * freq : 0 }));
  };
  root.querySelectorAll('[data-fc]').forEach(b => b.addEventListener('click', () => {
    state.sys = b.dataset.fc;
    root.querySelectorAll('[data-fc]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  [pIn, fIn].forEach(e => e.addEventListener('input', update));
  update();
}

document.querySelectorAll('[data-predict]').forEach(mountPredict);
export function mountWorthIt(root) {
  root.classList.add('mini-calc');
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  root.innerHTML = '<label for="wi-hard">Your water hardness (gpg)</label>'
    + '<div class="slider-row"><input id="wi-hard" type="range" min="1" max="30" step="1" value="10"><span class="slider-val" data-h style="min-width:70px"></span></div>'
    + '<label for="wi-years">Years you expect to stay</label>'
    + '<div class="slider-row"><input id="wi-years" type="range" min="2" max="20" step="1" value="10"><span class="slider-val" data-y style="min-width:70px"></span></div>'
    + '<label for="wi-spend">What hard water already costs you per year (descaler, vinegar runs, extra cleaning, spotted-glass rewashes)</label>'
    + '<div class="slider-row"><input id="wi-spend" type="range" min="0" max="300" step="10" value="80"><span class="slider-val" data-s style="min-width:70px"></span></div>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:8px"><input id="wi-repair" type="checkbox"> A scale-related repair in the last 5 years (heater element, clogged valve, choked fixture)</label>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:6px"><input id="wi-soft" type="checkbox" checked> I want water that actually tests soft (lather, no spotting) \u2014 not just less scale</label>'
    + '<div class="mc-out"><strong data-verdict class="fig" style="font-size:18px"></strong><br>'
    + '<span data-math style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.65"></span><br>'
    + '<span data-honest style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.6"></span></div>';
  const hIn = root.querySelector('#wi-hard'), yIn = root.querySelector('#wi-years'), sIn = root.querySelector('#wi-spend');
  const rIn = root.querySelector('#wi-repair'), softIn = root.querySelector('#wi-soft');
  const update = () => {
    const hard = +hIn.value, years = +yIn.value, spend = +sIn.value, repair = rIn.checked, wantSoft = softIn.checked;
    root.querySelector('[data-h]').textContent = hard + ' gpg';
    root.querySelector('[data-y]').textContent = years + ' yrs';
    root.querySelector('[data-s]').textContent = d(spend);
    const cost = 1580 + 249 * years;                        // prepared-install midpoint + all-in annual midpoint
    const exposure = spend * years + (repair ? 430 * (years / 5) : 0); // their receipts + published avg repair at their reported rate
    const pct = cost > 0 ? Math.round((exposure / cost) * 100) : 0;
    let v, m;
    m = 'Ownership over ' + years + ' years: about ' + d(cost) + ' (prepared install midpoint + running costs). Your own receipts, projected: ' + d(exposure) + ' \u2014 covering ' + pct + '% of it.';
    if (hard <= 3) {
      v = 'Buy nothing';
      m = 'At ' + hard + ' gpg your water is soft by USGS classification. There is nothing here for a softener to earn back \u2014 and nothing for a conditioner either.';
    } else if (years <= 3) {
      v = 'Probably not \u2014 you are leaving too soon';
      m += ' Most of a softener\u2019s cost lands on day one; ' + years + ' years is rarely enough runway to matter, and softeners are not reliably reflected in resale prices.';
    } else if (pct >= 100) {
      v = 'Clearly worthwhile \u2014 on your own receipts';
      m += ' You are already paying softener money without owning a softener.';
    } else if (pct >= 60) {
      v = 'Probably worthwhile';
      m += ' Your documented costs carry most of the bill; the lather, the spotless glass and the un-scrubbed shower door only have to be worth ' + d(cost - exposure) + ' to you over ' + years + ' years.';
    } else if (hard >= 15 && wantSoft) {
      v = 'A strong practical case \u2014 mostly lifestyle';
      m += ' At ' + hard + ' gpg the daily experience gap is large, but be honest about the label: you are buying comfort and convenience with some cost recovery, not an investment.';
    } else if (wantSoft) {
      v = 'Borderline \u2014 a comfort purchase with partial payback';
      m += ' The remaining ' + d(cost - exposure) + ' is what soft-water living costs you over ' + years + ' years. Some people pay it happily. Nobody should pretend it pays itself.';
    } else {
      v = 'Probably not worth it \u2014 consider scale control instead';
      m += ' If less scale is the whole goal, a salt-free conditioner does that smaller job for less money and 35 minutes a year.';
    }
    root.querySelector('[data-verdict]').textContent = v;
    root.querySelector('[data-math]').textContent = m;
    root.querySelector('[data-honest]').textContent = 'What this tool deliberately does NOT do: model appliance-lifespan or soap savings. The famous figures behind those claims come from industry-funded, accelerated-test research \u2014 your receipts are better evidence about your house.';
    root.setAttribute('data-result', JSON.stringify({ hard, years, spend, repair, wantSoft, cost, exposure, pct, verdict: v }));
  };
  [hIn, yIn, sIn].forEach(e => e.addEventListener('input', update));
  [rIn, softIn].forEach(e => e.addEventListener('change', update));
  update();
}

document.querySelectorAll('[data-filter-cost]').forEach(mountFilterCost);
export function mountIxDecoder(root) {
  root.classList.add('mini-calc');
  const P = {
    hard: { label: 'Hard water', ix: true, kind: 'YES \u2014 CATION exchange',
      tech: 'Salt-based water softener',
      cost: '$840\u2013$4,120 installed \u2014 every line itemised on our cost pillar',
      why: 'Hardness minerals are POSITIVE ions. Cation resin swaps calcium and magnesium for sodium. This is the ion exchange system most people are actually shopping for, and it is the one this site prices in full.',
      gate: false },
    nitrate: { label: 'Nitrate', ix: true, kind: 'YES \u2014 ANION exchange (specialty)',
      tech: 'Nitrate-selective anion exchange unit',
      cost: '$2,195\u2013$3,295 equipment, whole house \u00b7 from $275 for an under-sink RO if you only need safe drinking water',
      why: 'Nitrate is a NEGATIVE ion. A softener\u2019s cation resin ignores it completely \u2014 wrong charge, wrong resin, no amount of salt fixes it. This is a dedicated anion unit, and the resin must be nitrate-SELECTIVE.',
      gate: true },
    iron: { label: 'Iron / manganese', ix: false, kind: 'NO \u2014 not an ion exchange problem',
      tech: 'Oxidation + filtration (air injection, greensand)',
      cost: 'Priced separately in our iron filter guide',
      why: 'And it is worse than merely "not ion exchange": iron FOULS ion exchange resin. Iron must be removed BEFORE any IX system \u2014 not by it. Put a softener or a nitrate unit on iron water and you are paying to destroy the resin you just bought.',
      gate: false },
    sediment: { label: 'Sediment / cloudiness', ix: false, kind: 'NO \u2014 not an ion exchange problem',
      tech: 'Mechanical filtration',
      cost: 'Priced separately in our sediment filter guide',
      why: 'Ion exchange only touches DISSOLVED ions. Sediment is not dissolved \u2014 there is nothing for a resin to trade with. You need a strainer, not chemistry.',
      gate: false },
    bacteria: { label: 'Bacteria', ix: false, kind: 'NO \u2014 not an ion exchange problem',
      tech: 'UV disinfection',
      cost: 'Priced separately in our UV guide',
      why: 'Ion exchange does not disinfect. No resin, at any price, kills anything. If a well test came back positive, this is a UV question and a plumbing question, not a resin question.',
      gate: false },
    chlorine: { label: 'Chlorine taste / odour', ix: false, kind: 'NO \u2014 not an ion exchange problem',
      tech: 'Activated carbon',
      cost: 'Priced separately in our whole-house filter guide',
      why: 'Carbon ADSORBS \u2014 it holds molecules on its surface. That is a different mechanism from exchanging ions, and it happens to be the cheaper one.',
      gate: false },
    pfas: { label: 'PFAS', ix: false, kind: 'MOSTLY NO \u2014 not the residential answer',
      tech: 'Activated carbon or reverse osmosis',
      cost: 'Lab test first, then priced by route',
      why: 'Specialty anion resins for PFAS do exist industrially, but the proven residential routes are carbon and reverse osmosis. Either way this is a lab-test-first problem, not a catalogue-browsing problem.',
      gate: true },
  };
  const state = { p: 'hard' };
  root.innerHTML = '<div class="seg" role="group" aria-label="Your water problem" style="margin-bottom:14px;flex-wrap:wrap">'
    + Object.keys(P).map(k => '<button type="button" data-ix="' + k + '" aria-pressed="' + (k === 'hard' ? 'true' : 'false') + '">' + P[k].label + '</button>').join('')
    + '</div>'
    + '<label style="display:flex;gap:8px;align-items:flex-start;margin-top:6px;line-height:1.5"><input type="checkbox" id="ix-lab" style="margin-top:3px"> I have a current certified lab analysis of my water</label>'
    + '<label style="display:flex;gap:8px;align-items:flex-start;margin-top:6px;line-height:1.5"><input type="checkbox" id="ix-hard" style="margin-top:3px"> I also have hard water</label>'
    + '<div class="mc-out"><strong data-ixv class="fig" style="font-size:18px"></strong><br>'
    + '<span data-ixt style="font-size:15px;color:#16303F;font-weight:700;display:inline-block;margin-top:8px"></span><br>'
    + '<span data-ixc style="font-size:14px;color:#16303F;display:inline-block;margin-top:6px;line-height:1.6"></span><br>'
    + '<span data-ixw style="font-size:13.5px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.65"></span>'
    + '<span data-ixe style="font-size:13.5px;color:#B44A2E;display:none;margin-top:10px;line-height:1.65;font-weight:600"></span></div>';
  const lab = root.querySelector('#ix-lab'), alsoHard = root.querySelector('#ix-hard');
  const update = () => {
    const p = P[state.p], gated = p.gate && !lab.checked;
    let v, t, c, w;
    if (gated) {
      v = 'TEST FIRST \u2014 do not buy this system blind';
      t = p.tech + ' (probably) \u2014 but the number is withheld on purpose';
      c = 'Withheld. A price is the least useful thing I can hand you here.';
      w = 'Standard anion resin prefers SULFATE to nitrate. In high-sulfate well water it fills up with sulfate, leaves the nitrate in your water, and on exhaustion can release the captured nitrate back in a concentrated burst \u2014 water leaving the system worse than the water entering it. The trade literature warns that anion resins can also pick up heavy metals and arsenic and dump those at dangerous levels. Get a certified panel \u2014 nitrate, sulfate, iron, hardness \u2014 then tick the box. The number will still be here.';
    } else {
      v = p.kind;
      t = p.tech;
      c = p.cost;
      w = p.why;
      if (state.p === 'nitrate') {
        w += ' Specify NITRATE-SELECTIVE (sulfate-deselective) resin, not standard anion resin, and make sure the feed water is iron-free \u2014 iron fouls it.';
      }
    }
    root.querySelector('[data-ixv]').textContent = v;
    root.querySelector('[data-ixt]').textContent = t;
    root.querySelector('[data-ixc]').textContent = c;
    root.querySelector('[data-ixw]').textContent = w;
    const ex = root.querySelector('[data-ixe]');
    if (alsoHard.checked && state.p === 'nitrate') {
      ex.textContent = 'Hard water too? Then it is TWO systems, plumbed in sequence. The softener does not touch nitrate and the nitrate unit does not soften \u2014 anyone quoting one box for both is selling you a story. The trade literature also prefers soft feed water for these resins, which is an argument for sequence, not substitution.';
      ex.style.display = 'inline-block';
    } else if (alsoHard.checked && state.p !== 'hard') {
      ex.textContent = 'Hard water too? That is a separate, cation-exchange machine on top of whatever the row above says. Two problems, two boxes.';
      ex.style.display = 'inline-block';
    } else {
      ex.style.display = 'none';
    }
    root.setAttribute('data-result', JSON.stringify({ problem: state.p, isIx: p.ix, gated, alsoHard: alsoHard.checked, kind: p.kind }));
  };
  root.querySelectorAll('[data-ix]').forEach(b => b.addEventListener('click', () => {
    state.p = b.dataset.ix;
    root.querySelectorAll('[data-ix]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  [lab, alsoHard].forEach(e => e.addEventListener('change', update));
  update();
}

document.querySelectorAll('[data-worth-it]').forEach(mountWorthIt);
export function mountLifespanBe(root) {
  root.classList.add('mini-calc');
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  const ANNUAL = 249;   // our sourced all-in running midpoint \u2014 IDENTICAL for both machines, so it cancels out of the break-even
  const PRO = 430;      // prepared-install midpoint (our published band; Aquasure's own support quotes $300\u2013$600)
  const DIY = 80;       // fittings/flex lines only (our published $40\u2013$120 band)
  root.innerHTML = '<label for="lb-cheap">Published price of the budget system</label>'
    + '<div class="slider-row"><input id="lb-cheap" type="range" min="300" max="1500" step="5" value="605"><span class="slider-val" data-lbc style="min-width:70px"></span></div>'
    + '<label for="lb-quote">The quote you are comparing it against (installed)</label>'
    + '<div class="slider-row"><input id="lb-quote" type="range" min="800" max="8000" step="100" value="4000"><span class="slider-val" data-lbq style="min-width:70px"></span></div>'
    + '<label for="lb-years">How long you expect the pricier system to last</label>'
    + '<div class="slider-row"><input id="lb-years" type="range" min="8" max="20" step="1" value="15"><span class="slider-val" data-lby style="min-width:70px"></span></div>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:8px"><input id="lb-diy" type="checkbox"> I will install the budget system myself</label>'
    + '<div class="mc-out"><strong data-lbv class="fig" style="font-size:20px"></strong><br>'
    + '<span data-lbm style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.65"></span><br>'
    + '<span data-lbn style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.6"></span></div>';
  const cIn = root.querySelector('#lb-cheap'), qIn = root.querySelector('#lb-quote'), yIn = root.querySelector('#lb-years'), diy = root.querySelector('#lb-diy');
  const update = () => {
    const cheap = +cIn.value, quote = +qIn.value, yrs = +yIn.value, isDiy = diy.checked;
    const install = isDiy ? DIY : PRO;
    const cheapAllIn = cheap + install;
    root.querySelector('[data-lbc]').textContent = d(cheap);
    root.querySelector('[data-lbq]').textContent = d(quote);
    root.querySelector('[data-lby]').textContent = yrs + ' yrs';
    const be = quote > 0 ? (yrs * cheapAllIn) / quote : 0;
    const quotePerYr = quote / yrs + ANNUAL;
    const cheapAt10 = cheapAllIn / 10 + ANNUAL;
    root.querySelector('[data-lbv]').textContent = 'Break-even: ' + be.toFixed(1) + ' years';
    root.querySelector('[data-lbm]').textContent =
      'Your quote works out to ' + d(quotePerYr) + '/yr over ' + yrs + ' years. The budget system, ' +
      (isDiy ? 'self-installed' : 'professionally installed') + ', comes to ' + d(cheapAllIn) +
      ' all in \u2014 so it matches that quote if it survives ' + be.toFixed(1) + ' years, and costs ' + d(cheapAt10) +
      '/yr if it lasts ten. Running costs are the same salt in both machines, so they cancel: this is purely about the box and how long it lives.';
    let note;
    if (be <= 4) {
      note = 'At this gap, even a mediocre run wins. I am not going to argue with arithmetic I just handed you \u2014 if the cheap system clears ' + be.toFixed(1) + ' years, it was the rational buy.';
    } else if (be >= yrs * 0.8) {
      note = 'These two prices are close enough that lifespan barely moves the answer. Decide this one on warranty, support and who does the install \u2014 not on the sticker.';
    } else {
      note = 'It has to last ' + be.toFixed(1) + ' years. The honest question is whether the warranty you can actually get IN WRITING covers that long.';
    }
    root.querySelector('[data-lbn]').textContent = note +
      ' Lifespan is the one number nobody can source \u2014 not me, not the brochure. A warranty is the manufacturer\u2019s own bet on it, which is exactly why a warranty stated three different ways matters more than the sticker price.';
    root.setAttribute('data-result', JSON.stringify({ cheap, quote, yrs, isDiy, cheapAllIn, be: +be.toFixed(2), quotePerYr: Math.round(quotePerYr), cheapAt10: Math.round(cheapAt10) }));
  };
  [cIn, qIn, yIn].forEach(e => e.addEventListener('input', update));
  diy.addEventListener('change', update);
  update();
}

document.querySelectorAll('[data-ix-decoder]').forEach(mountIxDecoder);
export function mountComboRouter(root) {
  root.classList.add('mini-calc');
  root.innerHTML = '<div style="font-weight:700;margin-bottom:6px">Which of these does your water actually have?</div>'
    + '<label style="display:flex;gap:8px;align-items:center"><input type="checkbox" id="cb-hard"> Scale, spots, poor lather (hardness)</label>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:4px"><input type="checkbox" id="cb-chlor"> Chlorine taste or smell</label>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:4px"><input type="checkbox" id="cb-sed"> Grit, cloudiness, sediment</label>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:4px"><input type="checkbox" id="cb-iron"> Rust stains, metallic taste, rotten-egg smell</label>'
    + '<div class="seg" role="group" aria-label="Water source" style="margin-top:12px">'
    + '<button type="button" data-cb-src="city" aria-pressed="true">City water</button>'
    + '<button type="button" data-cb-src="well" aria-pressed="false">Private well</button></div>'
    + '<div class="mc-out"><strong data-cbv class="fig" style="font-size:18px"></strong><br>'
    + '<span data-cbc style="font-size:15px;color:#16303F;font-weight:700;display:inline-block;margin-top:8px"></span><br>'
    + '<span data-cbw style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.65"></span></div>';
  const boxes = { hard: root.querySelector('#cb-hard'), chlor: root.querySelector('#cb-chlor'),
                  sed: root.querySelector('#cb-sed'), iron: root.querySelector('#cb-iron') };
  const state = { src: 'city' };
  const update = () => {
    const hard = boxes.hard.checked, chlor = boxes.chlor.checked, sed = boxes.sed.checked, iron = boxes.iron.checked;
    let v, c, w;
    if (state.src === 'well' && (iron || sed)) {
      v = 'A well train \u2014 not this page\u2019s combo';
      c = 'Priced in our well water guide, stage by stage';
      w = 'Iron and sediment on a well must be handled BEFORE any softener or carbon vessel \u2014 iron fouls softener resin and coats carbon. The city-water combo on this page is the wrong shopping list; the well train sequences the same jobs in the right order.';
    } else if (iron) {
      v = 'Iron treatment first \u2014 the combo will not fix this';
      c = 'A dedicated iron filter, priced separately';
      w = 'A carbon-plus-softener combo is not iron equipment. Above about 0.3 ppm, iron shortens softener resin life; a combo bought for an iron problem is two machines paying for one mistake.';
    } else if (!hard && !chlor && !sed) {
      v = 'Buy nothing yet';
      c = '$0 \u2014 plus a water test';
      w = 'Nothing you ticked needs treatment. If something feels wrong anyway, measure before you spend: a test costs less than one bag-year of salt, and \u201cthe water seems off\u201d has sold a great many combos.';
    } else if (hard && (chlor || sed)) {
      v = 'YES \u2014 this is the combo\u2019s actual job';
      c = '$1,500\u2013$4,000 installed (published combo band) \u00b7 our itemised sheet runs $2,140\u2013$6,720 year one';
      w = 'Two different problems, two different machines: carbon adsorbs chlorine, ion exchange removes hardness. Neither does the other\u2019s job, so a coordinated pair is honest engineering here \u2014 and the saving is in the SHARED INSTALL, not the tanks.';
    } else if (hard) {
      v = 'Softener only \u2014 skip the filter half';
      c = '$840\u2013$4,120 installed (our published canon)';
      w = 'Hardness is the whole problem you ticked, and a softener is the whole answer. A combo here sells you a carbon vessel for chlorine you do not taste \u2014 half a machine you did not need, plus its cartridges forever.';
    } else {
      v = 'Filter only \u2014 skip the softener half';
      c = '$800\u2013$3,000 installed (published carbon whole-house band)';
      w = 'Chlorine and sediment are filtration jobs; there is no hardness on your list for a softener to remove. Buying the combo anyway adds a brine tank, salt hauling and regeneration water to a problem carbon solves alone.';
    }
    root.querySelector('[data-cbv]').textContent = v;
    root.querySelector('[data-cbc]').textContent = c;
    root.querySelector('[data-cbw]').textContent = w;
    root.setAttribute('data-result', JSON.stringify({ hard, chlor, sed, iron, src: state.src, verdict: v }));
  };
  Object.values(boxes).forEach(b => b.addEventListener('change', update));
  root.querySelectorAll('[data-cb-src]').forEach(b => b.addEventListener('click', () => {
    state.src = b.dataset.cbSrc;
    root.querySelectorAll('[data-cb-src]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  update();
}

document.querySelectorAll('[data-lifespan-be]').forEach(mountLifespanBe);
export function mountSroBuilder(root) {
  root.classList.add('mini-calc');
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  root.innerHTML = '<label for="sro-hard">Your measured hardness (gpg)</label>'
    + '<div class="slider-row"><input id="sro-hard" type="range" min="1" max="25" step="1" value="12"><span class="slider-val" data-sh style="min-width:70px"></span></div>'
    + '<div class="seg" role="group" aria-label="RO tier" style="margin-top:10px">'
    + '<button type="button" data-sro-ro="350" aria-pressed="false">Basic RO ($300\u2013$500)</button>'
    + '<button type="button" data-sro-ro="700" aria-pressed="true">Mid RO (~$700)</button>'
    + '<button type="button" data-sro-ro="1300" aria-pressed="false">Low-waste RO ($1,000\u2013$1,500)</button></div>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:10px"><input id="sro-pro" type="checkbox" checked> Professional installation for both</label>'
    + '<div class="mc-out"><strong data-sv class="fig" style="font-size:18px"></strong><br>'
    + '<span data-sm style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.65"></span><br>'
    + '<span data-sn style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.6"></span></div>';
  const hIn = root.querySelector('#sro-hard'), pro = root.querySelector('#sro-pro');
  const state = { ro: 700 };
  const update = () => {
    const hard = +hIn.value, isPro = pro.checked;
    root.querySelector('[data-sh]').textContent = hard + ' gpg';
    const needSoft = hard >= 7;
    const softDay1 = isPro ? 1580 : 1230;                    // prepared midpoint / unit+fittings only
    const roDay1 = state.ro + (isPro ? 400 : 60);            // pro RO install midpoint of reconciled band / DIY fittings
    const roRun = 235;                                        // consumables $175 mid + wastewater ~$60 mid
    const softRun = 249;
    let day1, run10, v, m, n;
    if (!needSoft) {
      day1 = roDay1; run10 = roRun * 10;
      v = 'RO alone \u2014 skip the softener: ' + d(day1) + ' day one, ~' + d(day1 + run10) + ' per decade';
      m = 'At ' + hard + ' gpg you are under the ~7 gpg feed threshold one RO maker publishes for good membrane life. An under-sink RO with proper prefilters can run on your water as-is \u2014 a whole-house softener here would be ' + d(isPro ? 1580 : 1230) + ' of equipment solving a problem you do not have.';
      n = 'If scale, spotting or lather bothers you anyway, that is a hardness complaint \u2014 retest, and revisit. But do not buy the softener to protect the membrane at ' + hard + ' gpg; the membrane does not need the bodyguard yet.';
    } else {
      day1 = softDay1 + roDay1; run10 = (softRun + roRun) * 10;
      v = 'Both systems: ' + d(day1) + ' day one, ~' + d(day1 + run10) + ' per decade';
      m = 'Softener ' + d(softDay1) + ' + RO ' + d(roDay1) + ' day one; running ' + d(softRun + roRun) + '/yr (salt, regen utilities, RO cartridges, membrane fund, reject water). At ' + hard + ' gpg the softener is not just comfort equipment \u2014 it is the RO membrane\u2019s pretreatment: softened feed extends membrane life and lets the unit run at lower waste.';
      n = 'Two jobs, two machines: the softener treats every tap; the RO purifies one. Doing both installs in one visit typically saves one service-call mobilization \u2014 real, but modest. The decade is what to compare, not the sticker.';
    }
    root.querySelector('[data-sv]').textContent = v;
    root.querySelector('[data-sm]').textContent = m;
    root.querySelector('[data-sn]').textContent = n;
    root.setAttribute('data-result', JSON.stringify({ hard, ro: state.ro, isPro, needSoft, day1, decade: day1 + run10 }));
  };
  hIn.addEventListener('input', update);
  pro.addEventListener('change', update);
  root.querySelectorAll('[data-sro-ro]').forEach(b => b.addEventListener('click', () => {
    state.ro = +b.dataset.sroRo;
    root.querySelectorAll('[data-sro-ro]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  update();
}

document.querySelectorAll('[data-combo-router]').forEach(mountComboRouter);
export function mountRhWarranty(root) {
  root.classList.add('mini-calc');
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  root.innerHTML = '<label for="rh-bottle">Rheem Cleaner, price per bottle (read it off the shelf \u2014 we do not invent numbers)</label>'
    + '<div class="slider-row"><input id="rh-bottle" type="range" min="5" max="30" step="1" value="12"><span class="slider-val" data-rb style="min-width:70px"></span></div>'
    + '<label for="rh-years">Years you expect to own it</label>'
    + '<div class="slider-row"><input id="rh-years" type="range" min="3" max="15" step="1" value="10"><span class="slider-val" data-ry style="min-width:70px"></span></div>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:8px"><input id="rh-diy" type="checkbox"> I would repair it myself (rebuild kits, published ~$100)</label>'
    + '<div class="mc-out"><strong data-rv class="fig" style="font-size:18px"></strong><br>'
    + '<span data-rm style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.65"></span><br>'
    + '<span data-rn style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.6"></span></div>';
  const bIn = root.querySelector('#rh-bottle'), yIn = root.querySelector('#rh-years'), diy = root.querySelector('#rh-diy');
  const update = () => {
    const bottle = +bIn.value, years = +yIn.value, isDiy = diy.checked;
    root.querySelector('[data-rb]').textContent = d(bottle);
    root.querySelector('[data-ry]').textContent = years + ' yrs';
    const bottlesPerYr = 3;                                   // "every four months" — Rheem's own maintenance guidance
    const conditionCost = bottle * bottlesPerYr * 5;          // keeping the extension alive through years 1–5
    const repair = isDiy ? 100 : 430;                         // published rebuild-kit ~$100 / published $430 average repair
    const be = conditionCost / repair;
    let v, m, n;
    if (isDiy) {
      v = 'Skip the condition \u2014 you are your own warranty';
      m = 'A parts-and-labour warranty mostly insures LABOUR, and you just said you supply that for free. Keeping the extension alive costs ' + d(conditionCost) + ' over five years (' + (bottlesPerYr * 5) + ' bottles at ' + d(bottle) + '); a DIY valve rebuild runs about $100 in published parts. Use cleaner if your resin needs it \u2014 not to feed a warranty you would rarely invoke.';
      n = 'The 3-year electronics and 10-year tank coverage stay yours either way \u2014 those are the unconditional parts, and for a DIY owner they are the ones that matter.';
    } else if (be <= 1) {
      v = 'Cheap insurance \u2014 the condition is worth feeding';
      m = 'At ' + d(bottle) + ' a bottle, keeping the extended warranty alive costs ' + d(conditionCost) + ' across years 1\u20135 \u2014 less than ONE published-average repair (' + d(repair) + '). If it prevents or covers a single parts-and-labour event in years 2\u20135, it paid for itself.';
      n = 'Two honest footnotes: the extension covers years 2\u20135 only \u2014 your years 6\u2013' + years + ' are on the 10-year tank and your own wallet \u2014 and the claim lives or dies on PROOF of the every-four-months routine. Keep receipts, or the condition was theatre.';
    } else {
      v = 'An extended warranty priced as detergent';
      m = 'At ' + d(bottle) + ' a bottle, the condition costs ' + d(conditionCost) + ' over five years \u2014 ' + be.toFixed(1) + '\u00d7 the published average repair (' + d(repair) + '). You are prepaying more than the coverage is statistically likely to return, one bottle at a time.';
      n = 'That does not make the cleaner useless \u2014 chlorinated city water genuinely fouls resin \u2014 but be clear which product you are buying: resin maintenance, or warranty years. At this price you are buying the second and calling it the first.';
    }
    root.querySelector('[data-rv]').textContent = v;
    root.querySelector('[data-rm]').textContent = m;
    root.querySelector('[data-rn]').textContent = n;
    root.setAttribute('data-result', JSON.stringify({ bottle, years, isDiy, conditionCost, be: +be.toFixed(2) }));
  };
  [bIn, yIn].forEach(e => e.addEventListener('input', update));
  diy.addEventListener('change', update);
  update();
}

document.querySelectorAll('[data-sro-builder]').forEach(mountSroBuilder);
export function mountFtTco(root) {
  root.classList.add('mini-calc');
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  root.innerHTML = '<label for="ft-cart">Cartridge price (published band $50\u2013$200 \u2014 read yours off the listing)</label>'
    + '<div class="slider-row"><input id="ft-cart" type="range" min="30" max="200" step="5" value="90"><span class="slider-val" data-fc1 style="min-width:70px"></span></div>'
    + '<div class="seg" role="group" aria-label="Cartridge change interval" style="margin-top:8px">'
    + '<button type="button" data-ft-int="4" aria-pressed="true">Every 4 months</button>'
    + '<button type="button" data-ft-int="6" aria-pressed="false">Every 6 months</button>'
    + '<button type="button" data-ft-int="12" aria-pressed="false">Yearly</button></div>'
    + '<label for="ft-tank" style="margin-top:10px;display:block">Carbon tank system (published $1,195\u2013$2,495 across designs and sizes)</label>'
    + '<div class="slider-row"><input id="ft-tank" type="range" min="1100" max="2500" step="50" value="1500"><span class="slider-val" data-ft1 style="min-width:80px"></span></div>'
    + '<label for="ft-media">Replacement media per change \u2014 priced at the vendor; we do not invent numbers</label>'
    + '<div class="slider-row"><input id="ft-media" type="range" min="150" max="700" step="25" value="400"><span class="slider-val" data-fm1 style="min-width:80px"></span></div>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:8px"><input id="ft-chlor" type="checkbox"> My utility uses CHLORAMINE (check your water report)</label>'
    + '<div class="mc-out"><strong data-fv class="fig" style="font-size:18px"></strong><br>'
    + '<span data-fm style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.65"></span><br>'
    + '<span data-fn style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.6"></span></div>';
  const cIn = root.querySelector('#ft-cart'), tIn = root.querySelector('#ft-tank'), mIn = root.querySelector('#ft-media'), ch = root.querySelector('#ft-chlor');
  const state = { interval: 4 };
  const CART_DAY1 = 350;   // Big Blue housing kit class — published from $259, plus fittings
  const update = () => {
    const cart = +cIn.value, tank = +tIn.value, media = +mIn.value, chloramine = ch.checked;
    root.querySelector('[data-fc1]').textContent = d(cart);
    root.querySelector('[data-ft1]').textContent = d(tank);
    root.querySelector('[data-fm1]').textContent = d(media);
    const perYr = 12 / state.interval;
    const cartYr = cart * perYr;
    const cart10 = CART_DAY1 + cartYr * 10;
    const tank10 = tank + media * 2;                 // media every 4\u20135 yrs \u2192 two changes per decade
    const gap0 = tank - CART_DAY1;                   // day-one gap
    const cross = cartYr > 0 ? gap0 / cartYr : 99;   // years for cartridges to eat the gap (media not yet due)
    let v, m;
    if (cart10 > tank10) {
      v = 'The tank wins the decade: ' + d(tank10) + ' vs ' + d(cart10);
      m = 'The cartridge system is ' + d(gap0) + ' cheaper on day one \u2014 and spends ' + d(cartYr) + ' a year erasing that lead. It stops being the cheap option around year ' + Math.max(1, Math.round(cross)) + ', before the tank has even bought its first media change. Across ten years the \u201ccheap\u201d system costs ' + d(cart10 - tank10) + ' more.';
    } else {
      v = 'The cartridge route holds: ' + d(cart10) + ' vs ' + d(tank10);
      m = 'At ' + d(cart) + ' a cartridge changed ' + (perYr === 1 ? 'yearly' : 'every ' + state.interval + ' months') + ', the running stream stays small enough that the tank\u2019s day-one premium never pays back inside a decade. Light water use and cheap cartridges are the one profile where the housing kit is the rational buy \u2014 just check the maths again if your interval shortens.';
    }
    let n = 'The number most listings bury: HOW MUCH CARBON. A cartridge holds a few pounds; a 1.5\u20132.5 cu ft tank holds roughly 45\u201375 pounds \u2014 contact time is the whole mechanism, and you cannot get it from a slim housing.';
    if (chloramine) {
      n = 'CHLORAMINE CHANGES THE SHOPPING LIST: standard granular carbon does a poor job on it \u2014 you need CATALYTIC carbon, which costs more and wants a bigger bed because the reaction is slower. A standard cartridge on chloramine water is the wrong tool at any price. ' + n;
    }
    root.querySelector('[data-fv]').textContent = v;
    root.querySelector('[data-fm]').textContent = m;
    root.querySelector('[data-fn]').textContent = n;
    root.setAttribute('data-result', JSON.stringify({ cart, tank, media, chloramine, interval: state.interval, cart10, tank10, cross: +cross.toFixed(1) }));
  };
  [cIn, tIn, mIn].forEach(e => e.addEventListener('input', update));
  ch.addEventListener('change', update);
  root.querySelectorAll('[data-ft-int]').forEach(b => b.addEventListener('click', () => {
    state.interval = +b.dataset.ftInt;
    root.querySelectorAll('[data-ft-int]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  update();
}

document.querySelectorAll('[data-rh-warranty]').forEach(mountRhWarranty);
export function mountFlQuote(root) {
  root.classList.add('mini-calc');
  const d = (x) => '$' + Math.round(x).toLocaleString('en-US');
  const REGIONS = {
    panhandle: { name: 'Panhandle / Big Bend', lo: 3, hi: 7,  note: 'sand-and-gravel aquifer country \u2014 the soft corner of the state' },
    central:   { name: 'Central FL (Orlando / Villages)', lo: 8, hi: 15, note: 'deep Floridan limestone \u2014 published figures for the same cities span widely; the CCR settles it' },
    tampa:     { name: 'Tampa Bay', lo: 10, hi: 11, note: 'utility-reported: Tampa ~10.9 gpg, St Pete ~9.7' },
    south:     { name: 'South FL (Miami\u2013WPB)', lo: 11, hi: 19, note: 'Biscayne limestone; Boca reads 14.6\u201318.9 gpg AFTER plant softening' },
    jax:       { name: 'Jacksonville', lo: 15, hi: 15, note: 'utility-reported ~15.3 gpg \u2014 deep Floridan wells' }
  };
  root.innerHTML = '<div class="seg" role="group" aria-label="Florida region" style="flex-wrap:wrap">'
    + Object.entries(REGIONS).map(([k, r], i) => '<button type="button" data-fl-reg="' + k + '" aria-pressed="' + (i === 1 ? 'true' : 'false') + '">' + r.name + '</button>').join('')
    + '</div>'
    + '<label for="fl-people" style="margin-top:10px;display:block">People in the household</label>'
    + '<div class="slider-row"><input id="fl-people" type="range" min="1" max="8" step="1" value="3"><span class="slider-val" data-fp style="min-width:60px"></span></div>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:8px"><input id="fl-loop" type="checkbox" checked> My home has a softener loop (check the garage wall)</label>'
    + '<label style="display:flex;gap:8px;align-items:center;margin-top:6px"><input id="fl-well" type="checkbox"> I am on a private well</label>'
    + '<div class="mc-out"><strong data-fv class="fig" style="font-size:18px"></strong><br>'
    + '<span data-fm style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.65"></span><br>'
    + '<span data-fn style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.6"></span></div>';
  const pIn = root.querySelector('#fl-people'), loop = root.querySelector('#fl-loop'), well = root.querySelector('#fl-well');
  const state = { region: 'central' };
  const update = () => {
    const people = +pIn.value, hasLoop = loop.checked, isWell = well.checked;
    const r = REGIONS[state.region];
    root.querySelector('[data-fp]').textContent = people;
    let v, m, n;
    if (isWell) {
      v = 'Well water: this tool refuses to size anything yet';
      m = 'A Florida private well needs a lab test before any equipment number means anything \u2014 iron, sulfur, manganese and pH all change what you buy and what order it plumbs in. A softener sized from a hardness guess can be the wrong machine entirely on a well.';
      n = 'Test first ($150\u2013$350 for a proper well panel, or start with a home kit). Then the well-water train has its own worksheet on this site \u2014 that is where your numbers go.';
      root.setAttribute('data-result', JSON.stringify({ region: state.region, people, isWell: true, refused: true }));
    } else {
      // capacity from the region's SOURCED band: people × 75 gal × gpg × 7 days
      const grLo = people * 75 * r.lo * 7, grHi = people * 75 * r.hi * 7;
      const need = grHi / 0.65;  // our published sizing rule: ~65% of nameplate is usable between regens
      const cap = need <= 32000 ? '24,000\u201332,000' : need <= 40000 ? '32,000\u201340,000' : need <= 48000 ? '40,000\u201348,000' : '48,000\u201364,000';
      // year-one: unit + prepared install + loop adder + FL permit + salt scaled by hardness
      const lo = 600 + 240 + (hasLoop ? 0 : 600) + 50 + (r.lo >= 10 ? 80 : 60);
      const hi = 2000 + 620 + (hasLoop ? 0 : 2000) + 300 + (r.hi >= 10 ? 180 : 120);
      v = 'Your ' + r.name + ' scenario: ' + d(lo) + '\u2013' + d(hi) + ' year one';
      m = 'Published hardness band for your region: ' + r.lo + '\u2013' + r.hi + ' gpg (' + r.note + '). At ' + people + ' people that is roughly ' + Math.round(grLo/1000) + 'k\u2013' + Math.round(grHi/1000) + 'k grains a week \u2014 shop the ' + cap + ' grain class. The itemised stack: unit $600\u2013$2,000, prepared install $240\u2013$620' + (hasLoop ? ' (your loop saves the big line)' : ', loop construction $600\u2013$2,000 because there is none') + ', Florida plumbing permit $50\u2013$300, first-year salt scaled to your hardness.';
      n = 'The band is a screening number from published utility data \u2014 your utility\u2019s Consumer Confidence Report is the real one, it is free, and it was not produced by anyone selling softeners. Read that before any quote.';
      root.setAttribute('data-result', JSON.stringify({ region: state.region, people, hasLoop, isWell: false, refused: false, lo, hi, gpgLo: r.lo, gpgHi: r.hi }));
    }
    root.querySelector('[data-fv]').textContent = v;
    root.querySelector('[data-fm]').textContent = m;
    root.querySelector('[data-fn]').textContent = n;
  };
  pIn.addEventListener('input', update);
  [loop, well].forEach(e => e.addEventListener('change', update));
  root.querySelectorAll('[data-fl-reg]').forEach(b => b.addEventListener('click', () => {
    state.region = b.dataset.flReg;
    root.querySelectorAll('[data-fl-reg]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    update();
  }));
  update();
}

document.querySelectorAll('[data-ft-tco]').forEach(mountFtTco);
export const STATE_DATA = [
  {abbr:'AL',name:'Alabama',tier:'L',labor:'mid',conf:'M',note:'Coastal-plain and surface sources run softer; interior limestone pockets exist'},
  {abbr:'AK',name:'Alaska',tier:'V',labor:'hi',conf:'L',note:'Enormous source variation; most systems surface-fed and softer'},
  {abbr:'AZ',name:'Arizona',tier:'VH',labor:'mid',conf:'H',note:'Desert Southwest hard-water core; Phoenix and Tucson among the hardest big-city supplies'},
  {abbr:'AR',name:'Arkansas',tier:'L',labor:'lo',conf:'H',note:'USGS-attributed state average ~38 ppm \u2014 among the softest in the nation'},
  {abbr:'CA',name:'California',tier:'V',labor:'hi',conf:'M',note:'Famously split: Sierra surface water soft, Central Valley and SoCal groundwater hard \u2014 and the labor spread (Fresno vs San Francisco) is just as wide'},
  {abbr:'CO',name:'Colorado',tier:'V',labor:'mid',conf:'M',note:'Front Range surface water softer; plains groundwater hard'},
  {abbr:'CT',name:'Connecticut',tier:'L',labor:'hi',conf:'H',note:'New England granite geology \u2014 soft to moderately hard'},
  {abbr:'DE',name:'Delaware',tier:'M',labor:'mid',conf:'L',note:'Coastal-plain moderate; local variation'},
  {abbr:'FL',name:'Florida',tier:'VH',labor:'mid',conf:'H',note:'Limestone state; our Florida guide itemises it \u2014 utility readings 3\u201319 gpg, state average 9.6 gpg'},
  {abbr:'GA',name:'Georgia',tier:'L',labor:'lo',conf:'H',note:'Piedmont and surface sources mostly soft-to-moderate'},
  {abbr:'HI',name:'Hawaii',tier:'M',labor:'hi',conf:'M',note:'Volcanic geology, moderate; the highest plumber wages in the nation (BLS median $124,550)'},
  {abbr:'ID',name:'Idaho',tier:'H',labor:'mid',conf:'M',note:'Snake River Plain groundwater hard'},
  {abbr:'IL',name:'Illinois',tier:'H',labor:'hi',conf:'H',note:'Limestone aquifers hard; the highest plumber mean wage cited in BLS data ($87,980)'},
  {abbr:'IN',name:'Indiana',tier:'VH',labor:'mid',conf:'H',note:'A standout: Indianapolis regularly tests above 250 ppm; limestone bedrock statewide'},
  {abbr:'IA',name:'Iowa',tier:'VH',labor:'mid',conf:'H',note:'Glacial-deposit groundwater; upper-Midwest hard belt'},
  {abbr:'KS',name:'Kansas',tier:'VH',labor:'lo',conf:'H',note:'A standout: parts of western Kansas exceed 350 ppm; High Plains aquifer 200\u2013300 ppm'},
  {abbr:'KY',name:'Kentucky',tier:'M',labor:'lo',conf:'M',note:'Karst limestone regions hard; surface systems softer'},
  {abbr:'LA',name:'Louisiana',tier:'L',labor:'lo',conf:'M',note:'Coastal-plain and river sources mostly softer'},
  {abbr:'ME',name:'Maine',tier:'L',labor:'mid',conf:'H',note:'Granite New England \u2014 soft'},
  {abbr:'MD',name:'Maryland',tier:'M',labor:'hi',conf:'M',note:'Piedmont-to-coastal transition; moderate and variable'},
  {abbr:'MA',name:'Massachusetts',tier:'L',labor:'hi',conf:'H',note:'Soft surface supplies; among the highest construction wages (~$48.90/hr cited)'},
  {abbr:'MI',name:'Michigan',tier:'H',labor:'mid',conf:'H',note:'Glacial groundwater hard across much of the state'},
  {abbr:'MN',name:'Minnesota',tier:'VH',labor:'hi',conf:'H',note:'\'Not far behind\' the standouts \u2014 glacial calcium-rich deposits'},
  {abbr:'MS',name:'Mississippi',tier:'L',labor:'lo',conf:'M',note:'Mostly softer sources; the lowest plumber wages cited (BLS median $49,550)'},
  {abbr:'MO',name:'Missouri',tier:'H',labor:'mid',conf:'M',note:'Ozark karst and plains groundwater hard'},
  {abbr:'MT',name:'Montana',tier:'H',labor:'mid',conf:'M',note:'Northern plains groundwater hard'},
  {abbr:'NE',name:'Nebraska',tier:'VH',labor:'lo',conf:'H',note:'\'Not far behind\' the standouts \u2014 High Plains aquifer country'},
  {abbr:'NV',name:'Nevada',tier:'VH',labor:'mid',conf:'H',note:'Desert Southwest core; Las Vegas supply among the hardest anywhere'},
  {abbr:'NH',name:'New Hampshire',tier:'L',labor:'hi',conf:'H',note:'Granite state, literally \u2014 soft'},
  {abbr:'NJ',name:'New Jersey',tier:'M',labor:'hi',conf:'M',note:'Variable; among the highest construction wages (~$45.60/hr cited)'},
  {abbr:'NM',name:'New Mexico',tier:'VH',labor:'lo',conf:'H',note:'Desert Southwest hard-water core'},
  {abbr:'NY',name:'New York',tier:'V',labor:'hi',conf:'H',note:'NYC\'s Catskill surface water is famously soft; upstate groundwater runs hard \u2014 one state, two answers'},
  {abbr:'NC',name:'North Carolina',tier:'L',labor:'lo',conf:'H',note:'Coastal and Piedmont mostly soft-to-moderate'},
  {abbr:'ND',name:'North Dakota',tier:'VH',labor:'mid',conf:'H',note:'Top of the \'nearly unbroken band\' of hard-to-very-hard from the Dakotas to Texas'},
  {abbr:'OH',name:'Ohio',tier:'H',labor:'mid',conf:'H',note:'Limestone and glacial aquifers hard'},
  {abbr:'OK',name:'Oklahoma',tier:'VH',labor:'lo',conf:'H',note:'Hard-water plains belt'},
  {abbr:'OR',name:'Oregon',tier:'L',labor:'hi',conf:'H',note:'Cascade surface water soft'},
  {abbr:'PA',name:'Pennsylvania',tier:'V',labor:'mid',conf:'M',note:'Ridge-and-valley limestone hard; Appalachian plateau softer'},
  {abbr:'RI',name:'Rhode Island',tier:'L',labor:'hi',conf:'H',note:'New England soft'},
  {abbr:'SC',name:'South Carolina',tier:'L',labor:'lo',conf:'H',note:'Coastal-plain softer'},
  {abbr:'SD',name:'South Dakota',tier:'VH',labor:'mid',conf:'H',note:'Hard-to-very-hard plains band'},
  {abbr:'TN',name:'Tennessee',tier:'M',labor:'lo',conf:'M',note:'Karst regions hard; surface systems moderate'},
  {abbr:'TX',name:'Texas',tier:'VH',labor:'lo',conf:'H',note:'Bottom of the plains band; San Antonio regularly tests above 300 ppm'},
  {abbr:'UT',name:'Utah',tier:'VH',labor:'mid',conf:'H',note:'Desert Southwest core'},
  {abbr:'VT',name:'Vermont',tier:'L',labor:'mid',conf:'H',note:'New England soft'},
  {abbr:'VA',name:'Virginia',tier:'M',labor:'mid',conf:'M',note:'Coastal soft to valley limestone hard \u2014 variable'},
  {abbr:'WA',name:'Washington',tier:'L',labor:'hi',conf:'H',note:'Cascade surface water soft; among the highest trade wages (~$47.30/hr cited)'},
  {abbr:'WV',name:'West Virginia',tier:'M',labor:'lo',conf:'M',note:'Appalachian variable; among the lowest plumber wages cited (BLS median $49,630)'},
  {abbr:'WI',name:'Wisconsin',tier:'H',labor:'mid',conf:'H',note:'Glacial and dolomite aquifers hard'},
  {abbr:'WY',name:'Wyoming',tier:'H',labor:'mid',conf:'M',note:'Plains and basin groundwater hard'}
];

export function mountStateExplorer(root) {
  root.classList.add('mini-calc');
  const TIERS = {
    VH: { label: 'Very High hard-water exposure', advice: 'Hardness will drive system sizing here \u2014 measure it, size from the number, and expect the capacity conversation to be real rather than an upsell.' },
    H:  { label: 'High hard-water exposure', advice: 'Hard water is the regional norm \u2014 verify your local number on the CCR; sizing matters.' },
    M:  { label: 'Moderate exposure', advice: 'Genuinely mixed \u2014 your utility\u2019s number decides whether a softener earns its keep.' },
    L:  { label: 'Lower exposure', advice: 'Much of this state runs soft \u2014 TEST BEFORE BUYING ANYTHING; the correct purchase here is often nothing.' },
    V:  { label: 'Highly variable', advice: 'One state, several answers \u2014 statewide generalisations mislead here more than anywhere; only your CCR or a test kit settles it.' }
  };
  const LABOR = {
    lo:  'lower-wage labor market (BLS anchors: Arkansas $46,750 / Mississippi $49,550 plumber wages) \u2014 the labor line lands at the low end of the national $240\u2013$620 prepared band',
    mid: 'mid-range labor market \u2014 budget the middle of the national $240\u2013$620 prepared band',
    hi:  'high-wage labor market (BLS anchors: Illinois $87,980 mean / Hawaii $124,550 median) \u2014 the same 4-hour install carries up to roughly twice the labor dollars of the cheapest states'
  };
  root.innerHTML = '<label for="se-state">Pick your state</label>'
    + '<select id="se-state" style="width:100%;padding:10px;font-size:15px;border:1.5px solid #16303F;border-radius:6px;background:#fff;margin-top:6px">'
    + STATE_DATA.map(s => '<option value="' + s.abbr + '"' + (s.abbr === 'TX' ? ' selected' : '') + '>' + s.name + '</option>').join('')
    + '</select>'
    + '<div class="mc-out"><strong data-sv class="fig" style="font-size:18px"></strong><br>'
    + '<span data-sm style="font-size:14px;color:#16303F;display:inline-block;margin-top:8px;line-height:1.65"></span><br>'
    + '<span data-sn style="font-size:13px;color:#5B6B75;display:inline-block;margin-top:10px;line-height:1.6"></span></div>';
  const sel = root.querySelector('#se-state');
  const update = () => {
    const s = STATE_DATA.find(x => x.abbr === sel.value);
    const t = TIERS[s.tier];
    root.querySelector('[data-sv]').textContent = s.name + ': ' + t.label;
    let m = s.note + '. ' + t.advice + ' Cost side: equipment is priced NATIONALLY \u2014 the same published softeners ship to every state \u2014 while your ' + LABOR[s.labor] + ', plus a $0\u2013$300 permit line depending on your county.';
    let n = 'Classification: editorial tier from the USGS regional hardness pattern (confidence: ' + (s.conf === 'H' ? 'high' : s.conf === 'M' ? 'medium' : 'limited') + '). It describes your REGION, not your tap \u2014 the CCR or a test kit gives the number that actually sizes a system.';
    if (s.abbr === 'FL') n = 'Florida has its own itemised page on this site \u2014 regional readings 3\u201319 gpg, the permit line, and the loop question, all sourced. ' + n;
    if (s.tier === 'L') m += ' The honest translation: many households here should buy NOTHING \u2014 verify before any quote.';
    root.querySelector('[data-sm]').textContent = m;
    root.querySelector('[data-sn]').textContent = n;
    root.setAttribute('data-result', JSON.stringify({ abbr: s.abbr, tier: s.tier, labor: s.labor, conf: s.conf }));
  };
  sel.addEventListener('change', update);
  update();
}

document.querySelectorAll('[data-fl-quote]').forEach(mountFlQuote);
document.querySelectorAll('[data-state-explorer]').forEach(mountStateExplorer);
document.querySelectorAll('[data-tech-decider]').forEach(mountTechDecider);
document.querySelectorAll('[data-salt-cost]').forEach(mountSaltCost);
