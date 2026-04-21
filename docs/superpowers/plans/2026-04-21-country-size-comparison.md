# Country Size Comparison — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-file `index.html` app that compares two countries by land area, rendering each country's SVG outline shape via D3.

**Architecture:** One `index.html` file holds all HTML, CSS, and JavaScript. D3-geo and topojson-client load from CDN. Country area data, ISO code mappings, and world TopoJSON geometry are embedded as JS constants generated during setup. Pure utility functions are unit-tested in a separate `tests/test.html`.

**Tech Stack:** HTML5, CSS3 custom properties, vanilla JavaScript ES6+, d3-geo v3, topojson-client v3, Natural Earth 110m TopoJSON (world-atlas@2), Inter (Google Fonts)

---

### Task 1: Initialize project and HTML skeleton

**Files:**
- Create: `index.html`
- Create: `tests/test.html`

- [ ] **Step 1: Initialize git repo**

```bash
cd /home/nikhilv/projects/class
git init
```

- [ ] **Step 2: Create index.html**

```html
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Country Size Comparison</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/d3-geo@3"></script>
  <script src="https://cdn.jsdelivr.net/npm/topojson-client@3"></script>
  <style>
    /* CSS — added in Task 2 */
  </style>
</head>
<body>
  <header>
    <h1>Country Size Comparison</h1>
    <button id="theme-toggle" aria-label="Toggle dark mode">🌙</button>
  </header>

  <main>
    <section class="input-row">
      <input type="text" id="country1" placeholder="Country 1" autocomplete="off" />
      <input type="text" id="country2" placeholder="Country 2" autocomplete="off" />
      <button id="compare-btn" disabled>Compare</button>
    </section>

    <section id="welcome-state" class="welcome">
      <div class="globe">🌍</div>
      <p>Type two countries above to compare their sizes</p>
    </section>

    <section id="results" class="results hidden">
      <div class="cards">
        <div id="card1" class="card"></div>
        <div id="card2" class="card"></div>
      </div>
      <div id="result-banner" class="result-banner"></div>
      <button id="restart-btn" class="restart">Restart</button>
    </section>
  </main>

  <script>
    // DATA — added in Tasks 3 & 4
    // UTILS — added in Task 5
    // RENDER — added in Tasks 6 & 7
    // APP — added in Task 8
    // INIT — added in Task 8
  </script>
</body>
</html>
```

- [ ] **Step 3: Create tests/test.html**

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>Unit Tests</title>
  <style>
    body { font-family: monospace; padding: 1rem; }
    .pass { color: green; }
    .fail { color: red; font-weight: bold; }
    h2 { margin-bottom: 1rem; }
  </style>
</head>
<body>
<h2>Unit Tests</h2>
<div id="output"></div>
<script src="../data/country_data.js"></script>
<script>
const _results = [];
function test(name, fn) {
  try { fn(); _results.push({ name, pass: true }); }
  catch(e) { _results.push({ name, pass: false, error: e.message }); }
}
function assert(val, msg) { if (!val) throw new Error(msg || 'Assertion failed'); }
function assertEqual(a, b) {
  if (a !== b) throw new Error(`Expected ${JSON.stringify(b)}, got ${JSON.stringify(a)}`);
}

// Utility functions — pasted here in Task 5
// Tests — added in Task 5

window.addEventListener('load', () => {
  const div = document.getElementById('output');
  _results.forEach(r => {
    const el = document.createElement('div');
    el.className = r.pass ? 'pass' : 'fail';
    el.textContent = (r.pass ? '✓ ' : '✗ ') + r.name + (r.error ? ': ' + r.error : '');
    div.appendChild(el);
  });
});
</script>
</body>
</html>
```

- [ ] **Step 4: Start local server and verify page loads**

```bash
python3 -m http.server 8080 &
```

Open `http://localhost:8080`. Expected: heading "Country Size Comparison", globe emoji, no JS console errors.

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test.html
git commit -m "feat: add HTML skeleton and test runner"
```

---

### Task 2: CSS design system

**Files:**
- Modify: `index.html` — replace `/* CSS — added in Task 2 */` with full stylesheet

- [ ] **Step 1: Replace the CSS comment with this stylesheet**

```css
:root {
  --bg: #ffffff;
  --surface: #f3f4f6;
  --text: #111827;
  --text-muted: #6b7280;
  --border: #e5e7eb;
  --transition: 0.3s ease;
}
[data-theme="dark"] {
  --bg: #0f172a;
  --surface: #1e293b;
  --text: #f1f5f9;
  --text-muted: #94a3b8;
  --border: #334155;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  transition: background var(--transition), color var(--transition);
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  border-bottom: 1px solid var(--border);
}
header h1 { font-size: 1.25rem; font-weight: 900; }
#theme-toggle {
  background: none;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.4rem 0.75rem;
  cursor: pointer;
  font-size: 1rem;
  color: var(--text);
}
main { max-width: 900px; margin: 0 auto; padding: 2rem 1rem; }
.input-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
  margin-bottom: 2rem;
}
.input-row input {
  flex: 1;
  min-width: 200px;
  padding: 0.75rem 1rem;
  border: 2px solid var(--border);
  border-radius: 12px;
  background: var(--surface);
  color: var(--text);
  font-size: 1rem;
  font-family: inherit;
  transition: border-color var(--transition);
}
.input-row input:focus { outline: none; border-color: #38BDF8; }
#compare-btn {
  padding: 0.75rem 2rem;
  background: #38BDF8;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: opacity var(--transition), transform var(--transition);
}
#compare-btn:disabled { opacity: 0.4; cursor: not-allowed; }
#compare-btn:not(:disabled):hover { transform: translateY(-1px); }
.welcome { text-align: center; padding: 4rem 2rem; color: var(--text-muted); }
.globe { font-size: 4rem; margin-bottom: 1rem; }
.welcome p { font-size: 1.125rem; }
.hidden { display: none !important; }
.results { animation: fadeIn var(--transition) forwards; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}
.card {
  border-radius: 20px;
  padding: 1.5rem;
  background: var(--surface);
  border: 2px solid var(--border);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  min-height: 280px;
  transition: border-color var(--transition);
}
.card.error { border-color: #ef4444; }
.card .error-msg { color: #ef4444; font-size: 0.9rem; text-align: center; margin-top: 2rem; }
.card svg {
  width: 100%;
  height: 180px;
  animation: scaleIn 0.4s ease forwards;
}
@keyframes scaleIn {
  from { transform: scale(0.85); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}
.card .country-name { font-size: 1.25rem; font-weight: 700; }
.card .country-area { font-size: 2rem; font-weight: 900; letter-spacing: -0.5px; }
.result-banner {
  border-radius: 16px;
  padding: 1.25rem 2rem;
  text-align: center;
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 1.5rem;
}
.restart {
  display: block;
  margin: 0 auto;
  padding: 0.75rem 2.5rem;
  background: var(--text);
  color: var(--bg);
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: opacity var(--transition);
}
.restart:hover { opacity: 0.8; }
@media (max-width: 640px) {
  .cards { grid-template-columns: 1fr; }
  .input-row { flex-direction: column; }
  #compare-btn { width: 100%; }
}
```

- [ ] **Step 2: Verify in browser**

Reload `http://localhost:8080`. Expected:
- Styled header with title and 🌙 button
- Two inputs and a grayed-out Compare button
- Globe and helper text centered below

- [ ] **Step 3: Add spinner and fade-out CSS**

Add these rules at the end of the `<style>` block (before the closing `</style>`):

```css
/* Compare button loading state */
#compare-btn.loading {
  opacity: 0.7;
  cursor: wait;
  pointer-events: none;
}
#compare-btn.loading::after {
  content: ' ⏳';
}

/* Results fade-out on Restart */
.results.exiting {
  animation: fadeOut 0.25s ease forwards;
}
@keyframes fadeOut {
  from { opacity: 1; transform: translateY(0); }
  to   { opacity: 0; transform: translateY(8px); }
}
```

- [ ] **Step 4: Verify in browser**

Reload `http://localhost:8080`. Expected:
- Styled header with title and 🌙 button
- Two inputs and a grayed-out Compare button
- Globe and helper text centered below

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat: add CSS design system with light/dark mode"
```

---

### Task 3: Generate and embed country data

**Files:**
- Create: `data/generate.py`
- Create: `data/country_data.js` (generated output)
- Modify: `index.html` — replace `// DATA — added in Tasks 3 & 4` with embedded data

- [ ] **Step 1: Create data/generate.py**

```python
#!/usr/bin/env python3
"""Run once to regenerate data/country_data.js from RestCountries API."""
import json, urllib.request

url = "https://restcountries.com/v3.1/all?fields=cca3,ccn3,area,name"
with urllib.request.urlopen(url) as resp:
    raw = json.loads(resp.read())

countries = {}
for c in raw:
    alpha3 = c.get("cca3", "")
    numeric = c.get("ccn3", "")
    area_km2 = c.get("area") or 0
    name = c.get("name", {}).get("common", alpha3)
    if alpha3 and numeric and area_km2 > 0:
        countries[alpha3] = {
            "name": name,
            "area": round(area_km2 * 0.386102),
            "numeric": numeric
        }

countries = dict(sorted(countries.items()))

# Extra aliases: lowercase name / abbreviation → ISO alpha-3
aliases = {
    "usa": "USA", "us": "USA", "united states": "USA", "america": "USA",
    "uk": "GBR", "britain": "GBR", "england": "GBR", "great britain": "GBR",
    "russia": "RUS", "south korea": "KOR", "north korea": "PRK",
    "iran": "IRN", "syria": "SYR", "tanzania": "TZA",
    "taiwan": "TWN", "congo": "COD", "dr congo": "COD",
    "vietnam": "VNM", "laos": "LAO", "ivory coast": "CIV",
    "czech republic": "CZE", "czechia": "CZE",
    "turkey": "TUR", "turkiye": "TUR", "türkiye": "TUR",
    "swaziland": "SWZ", "eswatini": "SWZ",
    "cape verde": "CPV", "cabo verde": "CPV",
    "new zealand": "NZL", "nz": "NZL",
    "australia": "AUS", "aus": "AUS",
    "uae": "ARE", "emirates": "ARE",
    "vatican": "VAT", "holy see": "VAT", "vatican city": "VAT",
    "south africa": "ZAF",
    "saudi arabia": "SAU",
    "south sudan": "SSD",
    "new caledonia": "NCL",
    "french guiana": "GUF",
}
# Add each country's common name (lowercased) if not already present
for alpha3, data in countries.items():
    key = data["name"].lower()
    if key not in aliases:
        aliases[key] = alpha3

aliases = dict(sorted(aliases.items()))

print("const COUNTRIES =", json.dumps(countries, ensure_ascii=False) + ";")
print()
print("const COUNTRY_ALIASES =", json.dumps(aliases, ensure_ascii=False) + ";")
```

- [ ] **Step 2: Run the script**

```bash
python3 data/generate.py > data/country_data.js
```

Verify output:
```bash
head -1 data/country_data.js
```
Expected: `const COUNTRIES = {"ABW":...`

```bash
grep -c '"numeric"' data/country_data.js
```
Expected: a number ≥ 200

- [ ] **Step 3: Embed in index.html**

Replace `// DATA — added in Tasks 3 & 4` in the `<script>` tag with:

```javascript
// ---- COUNTRY DATA (generated by data/generate.py) ----
```

Then paste the entire contents of `data/country_data.js` on the next line.

- [ ] **Step 4: Verify in browser console**

Open `http://localhost:8080`, open DevTools console, run:
```javascript
console.log(COUNTRIES['FRA']);
```
Expected: `{name: "France", area: 248429, numeric: "250"}` (area may differ slightly by a few hundred)

```javascript
console.log(COUNTRY_ALIASES['usa']);
```
Expected: `"USA"`

- [ ] **Step 5: Commit**

```bash
git add data/generate.py data/country_data.js index.html
git commit -m "feat: embed country area data and alias table"
```

---

### Task 4: Embed world TopoJSON

**Files:**
- Create: `data/countries-110m.json` (downloaded)
- Create: `data/world_topo.js` (wrapped as JS constant)
- Modify: `index.html` — add WORLD_TOPO after COUNTRY_ALIASES

- [ ] **Step 1: Download Natural Earth 110m TopoJSON**

```bash
curl -s "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json" -o data/countries-110m.json
```

Verify:
```bash
wc -c data/countries-110m.json
```
Expected: between 100000 and 200000 bytes.

- [ ] **Step 2: Wrap as JS constant**

```bash
printf 'const WORLD_TOPO = ' > data/world_topo.js
cat data/countries-110m.json >> data/world_topo.js
printf ';' >> data/world_topo.js
```

- [ ] **Step 3: Embed in index.html**

In the `<script>` tag, directly after the `COUNTRY_ALIASES` constant, add:

```javascript
// ---- WORLD TOPO (Natural Earth 110m via world-atlas@2) ----
```

Then paste the contents of `data/world_topo.js` on the next line.

- [ ] **Step 4: Verify in browser console**

```javascript
console.log(Object.keys(WORLD_TOPO.objects));
```
Expected: `["countries", "land"]`

```javascript
console.log(topojson.feature(WORLD_TOPO, WORLD_TOPO.objects.countries).features.length);
```
Expected: a number between 170 and 250.

- [ ] **Step 5: Commit**

```bash
git add data/countries-110m.json data/world_topo.js index.html
git commit -m "feat: embed Natural Earth 110m world TopoJSON"
```

---

### Task 5: Country lookup utilities and unit tests

**Files:**
- Modify: `index.html` — replace `// UTILS — added in Task 5`
- Modify: `tests/test.html` — add utility functions and tests

- [ ] **Step 1: Write the failing tests in tests/test.html**

In `tests/test.html`, replace `// Utility functions — pasted here in Task 5` and `// Tests — added in Task 5` with:

```javascript
// ---- Utility functions (keep in sync with index.html) ----
const ACCENT_COLORS = ['#FF6B6B','#4ECDC4','#FFE66D','#A78BFA','#38BDF8','#84CC16'];

function lookupCountry(input) {
  const key = (input || '').trim().toLowerCase();
  if (!key) return null;
  const alpha3 = COUNTRY_ALIASES[key];
  if (!alpha3) return null;
  const data = COUNTRIES[alpha3];
  if (!data) return null;
  return { alpha3, name: data.name, area: data.area, numeric: data.numeric };
}

function formatArea(sqMiles) {
  return sqMiles.toLocaleString('en-US') + ' mi²';
}

function compareCountries(c1, c2) {
  if (c1.alpha3 === c2.alpha3) return { same: true };
  const bigger  = c1.area >= c2.area ? c1 : c2;
  const smaller = c1.area >= c2.area ? c2 : c1;
  return { bigger, smaller, multiplier: (bigger.area / smaller.area).toFixed(1), same: false };
}

function pickTwoColors() {
  const idx1 = Math.floor(Math.random() * ACCENT_COLORS.length);
  let idx2 = Math.floor(Math.random() * (ACCENT_COLORS.length - 1));
  if (idx2 >= idx1) idx2++;
  return [ACCENT_COLORS[idx1], ACCENT_COLORS[idx2]];
}

// ---- Tests ----
test('lookupCountry: exact common name', () => {
  const r = lookupCountry('France');
  assert(r !== null, 'should find France');
  assertEqual(r.alpha3, 'FRA');
  assert(r.area > 200000, 'France area should be > 200k mi²');
  assertEqual(r.numeric, '250');
});

test('lookupCountry: alias "usa"', () => {
  const r = lookupCountry('USA');
  assert(r !== null, 'should find USA via alias');
  assertEqual(r.alpha3, 'USA');
});

test('lookupCountry: case insensitive', () => {
  const r = lookupCountry('FRANCE');
  assert(r !== null, 'should be case-insensitive');
  assertEqual(r.alpha3, 'FRA');
});

test('lookupCountry: whitespace trimmed', () => {
  const r = lookupCountry('  Germany  ');
  assert(r !== null, 'should trim whitespace');
  assertEqual(r.alpha3, 'DEU');
});

test('lookupCountry: unknown returns null', () => {
  assertEqual(lookupCountry('Narnia'), null);
});

test('lookupCountry: empty string returns null', () => {
  assertEqual(lookupCountry(''), null);
});

test('formatArea: formats with commas and mi²', () => {
  assertEqual(formatArea(3796742), '3,796,742 mi²');
});

test('formatArea: small number no commas', () => {
  assertEqual(formatArea(116), '116 mi²');
});

test('compareCountries: larger country wins', () => {
  const c1 = { alpha3: 'RUS', name: 'Russia',      area: 6601668, numeric: '643' };
  const c2 = { alpha3: 'NZL', name: 'New Zealand', area: 104428,  numeric: '554' };
  const r = compareCountries(c1, c2);
  assertEqual(r.same, false);
  assertEqual(r.bigger.alpha3, 'RUS');
  assertEqual(r.smaller.alpha3, 'NZL');
  assert(parseFloat(r.multiplier) > 60, 'Russia should be 60+ times bigger');
});

test('compareCountries: same alpha3 returns same:true', () => {
  const c = { alpha3: 'FRA', name: 'France', area: 248429, numeric: '250' };
  assertEqual(compareCountries(c, c).same, true);
});

test('pickTwoColors: returns two different colors', () => {
  for (let i = 0; i < 20; i++) {
    const [a, b] = pickTwoColors();
    assert(a !== b, 'colors must be different');
    assert(ACCENT_COLORS.includes(a), 'color1 must be in palette');
    assert(ACCENT_COLORS.includes(b), 'color2 must be in palette');
  }
});
```

- [ ] **Step 2: Open tests/test.html and confirm all tests fail**

Open `http://localhost:8080/tests/test.html`. All tests should fail with errors like "COUNTRIES is not defined" (because `country_data.js` isn't embedded yet) or similar. This confirms tests are being found and run.

- [ ] **Step 3: Add utils to index.html**

Replace `// UTILS — added in Task 5` with the same utility functions from step 1 (minus the `// ---- Utility functions` comment header):

```javascript
const ACCENT_COLORS = ['#FF6B6B','#4ECDC4','#FFE66D','#A78BFA','#38BDF8','#84CC16'];

function lookupCountry(input) {
  const key = (input || '').trim().toLowerCase();
  if (!key) return null;
  const alpha3 = COUNTRY_ALIASES[key];
  if (!alpha3) return null;
  const data = COUNTRIES[alpha3];
  if (!data) return null;
  return { alpha3, name: data.name, area: data.area, numeric: data.numeric };
}

function formatArea(sqMiles) {
  return sqMiles.toLocaleString('en-US') + ' mi²';
}

function compareCountries(c1, c2) {
  if (c1.alpha3 === c2.alpha3) return { same: true };
  const bigger  = c1.area >= c2.area ? c1 : c2;
  const smaller = c1.area >= c2.area ? c2 : c1;
  return { bigger, smaller, multiplier: (bigger.area / smaller.area).toFixed(1), same: false };
}

function pickTwoColors() {
  const idx1 = Math.floor(Math.random() * ACCENT_COLORS.length);
  let idx2 = Math.floor(Math.random() * (ACCENT_COLORS.length - 1));
  if (idx2 >= idx1) idx2++;
  return [ACCENT_COLORS[idx1], ACCENT_COLORS[idx2]];
}
```

- [ ] **Step 4: Run tests — all 11 should pass**

Open (or reload) `http://localhost:8080/tests/test.html`. All 11 tests should show green checkmarks.

If the France numeric test fails: run `console.log(COUNTRIES['FRA'])` in the main page console and update the `assertEqual(r.numeric, '250')` assertion to match the actual value from the API response.

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test.html
git commit -m "feat: add lookup, format, and comparison utilities with unit tests"
```

---

### Task 6: D3 country shape rendering

**Files:**
- Modify: `index.html` — replace `// RENDER — added in Tasks 6 & 7`

- [ ] **Step 1: Confirm renderCountryShape is not yet defined**

In browser console:
```javascript
renderCountryShape('250', document.getElementById('card1'), '#FF6B6B');
```
Expected: `Uncaught ReferenceError: renderCountryShape is not defined`

- [ ] **Step 2: Add render functions to index.html**

Replace `// RENDER — added in Tasks 6 & 7` with:

```javascript
function getCountryFeature(numericCode) {
  return topojson
    .feature(WORLD_TOPO, WORLD_TOPO.objects.countries)
    .features
    .find(f => String(f.id) === String(numericCode)) || null;
}

function renderCountryShape(numericCode, cardEl, color) {
  const existing = cardEl.querySelector('svg');
  if (existing) existing.remove();
  const feature = getCountryFeature(numericCode);
  if (!feature) return;

  const svgEl = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svgEl.setAttribute('viewBox', '0 0 200 150');
  cardEl.insertBefore(svgEl, cardEl.firstChild);

  const projection = d3.geoNaturalEarth1().fitSize([200, 150], feature);
  const pathGen = d3.geoPath().projection(projection);

  d3.select(svgEl)
    .append('path')
    .datum(feature)
    .attr('d', pathGen)
    .attr('fill', color)
    .attr('stroke', 'white')
    .attr('stroke-width', 0.5);
}

function renderCard(cardEl, country, color) {
  cardEl.className = 'card';
  cardEl.innerHTML = '';
  cardEl.style.borderColor = color;

  renderCountryShape(country.numeric, cardEl, color);

  const nameEl = document.createElement('div');
  nameEl.className = 'country-name';
  nameEl.textContent = country.name;
  cardEl.appendChild(nameEl);

  const areaEl = document.createElement('div');
  areaEl.className = 'country-area';
  areaEl.textContent = formatArea(country.area);
  cardEl.appendChild(areaEl);
}

function renderError(cardEl, message) {
  cardEl.className = 'card error';
  cardEl.innerHTML = '';
  const msg = document.createElement('div');
  msg.className = 'error-msg';
  msg.textContent = message;
  cardEl.appendChild(msg);
}
```

- [ ] **Step 3: Smoke-test France in browser console**

```javascript
const c = lookupCountry('france');
document.getElementById('welcome-state').classList.add('hidden');
document.getElementById('results').classList.remove('hidden');
renderCard(document.getElementById('card1'), c, '#FF6B6B');
```

Expected: France's hexagon-ish outline appears in card1, coral/red, with "France" and the area below it.

- [ ] **Step 4: Smoke-test a small country**

```javascript
const c = lookupCountry('vatican');
renderCard(document.getElementById('card2'), c, '#4ECDC4');
```

Expected: a small dot or tiny shape for Vatican, scaled up by D3 `fitSize` to fill the SVG viewport. Area shows a small number.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat: add D3 country shape rendering and card component"
```

---

### Task 7: Result banner

**Files:**
- Modify: `index.html` — add renderBanner directly after renderError

- [ ] **Step 1: Confirm renderBanner is not defined**

In browser console:
```javascript
renderBanner({ same: true }, null);
```
Expected: `Uncaught ReferenceError: renderBanner is not defined`

- [ ] **Step 2: Add renderBanner to index.html directly after renderError**

```javascript
function renderBanner(comparison, winnerColor) {
  const banner = document.getElementById('result-banner');
  banner.style.display = 'block';
  if (comparison.same) {
    banner.textContent = 'You entered the same country twice!';
    banner.style.background = '#6b7280';
    return;
  }
  banner.textContent =
    comparison.bigger.name + ' is ' + comparison.multiplier + '× bigger than ' + comparison.smaller.name;
  banner.style.background = winnerColor;
}
```

- [ ] **Step 3: Smoke-test in console**

```javascript
const c1 = lookupCountry('russia');
const c2 = lookupCountry('new zealand');
renderBanner(compareCountries(c1, c2), '#FF6B6B');
```

Expected: banner reads "Russia is X× bigger than New Zealand" with coral background.

- [ ] **Step 4: Test same-country banner**

```javascript
const c = lookupCountry('canada');
renderBanner(compareCountries(c, c), null);
```

Expected: banner reads "You entered the same country twice!" with gray background.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat: add result banner with winner highlight"
```

---

### Task 8: App wiring — input handling, state, and init

**Files:**
- Modify: `index.html` — replace `// APP — added in Task 8` and `// INIT — added in Task 8`

- [ ] **Step 1: Add app state functions**

Replace `// APP — added in Task 8` with:

```javascript
function showWelcome() {
  document.getElementById('welcome-state').classList.remove('hidden');
  document.getElementById('results').classList.add('hidden');
  document.getElementById('result-banner').style.display = 'none';
}

function showResults(c1, c2, color1, color2) {
  document.getElementById('welcome-state').classList.add('hidden');
  const resultsEl = document.getElementById('results');
  resultsEl.classList.remove('hidden');
  resultsEl.style.animation = 'none';
  resultsEl.offsetHeight; // trigger reflow to replay animation
  resultsEl.style.animation = '';

  if (c1 && c2) {
    renderCard(document.getElementById('card1'), c1, color1);
    renderCard(document.getElementById('card2'), c2, color2);
    const comparison = compareCountries(c1, c2);
    const winnerColor = comparison.same
      ? '#6b7280'
      : comparison.bigger.alpha3 === c1.alpha3 ? color1 : color2;
    renderBanner(comparison, winnerColor);
  } else {
    if (c1) renderCard(document.getElementById('card1'), c1, color1);
    else renderError(document.getElementById('card1'), 'Country not found — try another name');
    if (c2) renderCard(document.getElementById('card2'), c2, color2);
    else renderError(document.getElementById('card2'), 'Country not found — try another name');
    document.getElementById('result-banner').style.display = 'none';
  }
}

function handleCompare() {
  const val1 = document.getElementById('country1').value;
  const val2 = document.getElementById('country2').value;
  const btn = document.getElementById('compare-btn');
  btn.classList.add('loading');
  // Defer rendering one frame so the spinner renders before the synchronous D3 work
  setTimeout(() => {
    const [color1, color2] = pickTwoColors();
    showResults(lookupCountry(val1), lookupCountry(val2), color1, color2);
    btn.classList.remove('loading');
  }, 0);
}
```

- [ ] **Step 2: Add init block**

Replace `// INIT — added in Task 8` with:

```javascript
(function init() {
  const btn = document.getElementById('compare-btn');
  const i1  = document.getElementById('country1');
  const i2  = document.getElementById('country2');

  function updateBtn() {
    btn.disabled = !(i1.value.trim() && i2.value.trim());
  }

  i1.addEventListener('input', updateBtn);
  i2.addEventListener('input', updateBtn);
  i1.addEventListener('keydown', e => { if (e.key === 'Enter' && !btn.disabled) handleCompare(); });
  i2.addEventListener('keydown', e => { if (e.key === 'Enter' && !btn.disabled) handleCompare(); });
  btn.addEventListener('click', handleCompare);

  document.getElementById('restart-btn').addEventListener('click', () => {
    const resultsEl = document.getElementById('results');
    resultsEl.classList.add('exiting');
    setTimeout(() => {
      resultsEl.classList.remove('exiting');
      i1.value = '';
      i2.value = '';
      updateBtn();
      showWelcome();
    }, 250);
  });

  const toggle = document.getElementById('theme-toggle');
  toggle.addEventListener('click', () => {
    const html = document.documentElement;
    const going = html.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    html.setAttribute('data-theme', going);
    toggle.textContent = going === 'dark' ? '☀️' : '🌙';
    localStorage.setItem('theme', going);
  });

  const saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
    toggle.textContent = saved === 'dark' ? '☀️' : '🌙';
  }

  showWelcome();
})();
```

- [ ] **Step 3: End-to-end test — happy path**

1. Page loads → welcome state visible, Compare disabled
2. Type "France" and "Germany" → Compare enables
3. Click Compare → both shapes render, banner shows which is bigger
4. Click Restart → inputs clear, welcome state returns

- [ ] **Step 4: End-to-end test — error path**

1. Type "xyz" in Country 1 and "Canada" in Country 2
2. Click Compare → card1 shows red error border + "Country not found", card2 renders Canada, banner is hidden

- [ ] **Step 5: End-to-end test — same country**

1. Type "France" in both inputs → Compare
2. Both cards render France, banner says "You entered the same country twice!"

- [ ] **Step 6: End-to-end test — Enter key**

Fill both inputs, press Enter in either field → comparison runs.

- [ ] **Step 7: Commit**

```bash
git add index.html
git commit -m "feat: wire up compare, restart, dark mode, and Enter key"
```

---

### Task 9: Polish and responsive verification

**Files:**
- No code changes expected unless issues are found in step 1–5

- [ ] **Step 1: Test dark mode toggle and persistence**

Click 🌙 → page goes dark navy. Refresh → stays dark. Click ☀️ → back to light.

- [ ] **Step 2: Test mobile layout**

In Chrome DevTools, set viewport to 375px wide. Expected:
- Inputs stack vertically, full width
- Cards stack vertically, full width
- No horizontal scrolling

- [ ] **Step 3: Test SVG edge cases**

| Input | Expected |
|---|---|
| `Vatican` | Very small shape, scaled up via fitSize |
| `Russia` | Large multi-part shape fills card |
| `United States` | Works via alias; contiguous US + Alaska |
| `New Zealand` | Two islands both appear |
| `Indonesia` | Many islands all appear |

If any shape is missing (returns null from `getCountryFeature`), the card still renders with name and area — just no SVG. This is acceptable for 110m resolution data (some very small territories may not have a polygon).

- [ ] **Step 4: Check browser console for errors**

Run through all flows (compare, restart, error, dark mode) with DevTools console open. Zero errors expected.

- [ ] **Step 5: Final commit**

```bash
git add index.html
git commit -m "chore: verify polish, responsive layout, and edge cases"
```

---

### Task 10: Smoke test checklist

- [ ] Open `http://localhost:8080` — welcome state visible
- [ ] Type two valid countries → shapes render, banner shows winner with ×
- [ ] Type one invalid country → error card on that side, other renders normally
- [ ] Restart clears inputs and returns to welcome
- [ ] Dark mode persists after page refresh
- [ ] Mobile viewport (375px) — cards and inputs stack vertically, no scroll
- [ ] `http://localhost:8080/tests/test.html` — all 11 unit tests pass (green)
- [ ] Zero console errors throughout all flows

```bash
git log --oneline
```
Expected: 9–10 commits.
