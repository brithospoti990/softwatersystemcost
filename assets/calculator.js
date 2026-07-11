// calculator.js — Cost Calculator UI (vanilla, no framework)
// Mounts on any element with [data-calc]. Variants: data-variant="full" | "embed".
// Exposes live state on data-result for the jsdom QA harness (spec §4.5).
import { estimate, hardnessForZip, fmtRange, countUp } from './calc-core.js';

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

document.querySelectorAll('[data-calc]').forEach(mountCalculator);
