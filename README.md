# Country Size Comparison

A browser-based app for comparing the land area of two countries side by side, with SVG country shape outlines and a result banner showing which is bigger and by how much.

## Live Demo

Open `index.html` via a local web server (see below). Works in any modern browser with an internet connection (CDN dependencies: D3 v7, topojson-client v3).

## How to Run Locally

**Requirements:** Python 3 (or any HTTP server)

```bash
cd gianfranco
python3 -m http.server 8080
```

Then open **http://localhost:8080** in your browser.

> **Important:** Open via `http://localhost:8080`, not by double-clicking the file. Some browsers block CDN scripts when loading `file://` URLs.

## How to Use

1. Type a country name in each input box (e.g. `France`, `USA`, `New Zealand`)
2. Press **Compare** or hit Enter
3. See the SVG shapes side by side with areas in mi²
4. Use the 🌙 button to toggle dark mode
5. Press **Restart** to compare again

**Supported name formats:** Full names, abbreviations, and common aliases all work — `usa`, `US`, `United States`, `America`; `uk`, `england`, `Britain`; `turkey`, `Türkiye`; etc.

## File Structure

```
gianfranco/
├── index.html          # The entire app (single file, ~140KB)
├── data/
│   ├── country_data.js # 249 countries: area (mi²), ISO codes, aliases
│   ├── countries-110m.json  # Natural Earth 110m TopoJSON (source data)
│   └── generate.py     # Script to regenerate country_data.js
├── tests/
│   └── test.html       # Unit tests (open in browser)
└── docs/
    └── superpowers/
        ├── specs/      # Design specification
        └── plans/      # Implementation plan
```

## Regenerating Country Data

If you want to update the country data (e.g. new countries or corrected areas):

```bash
cd gianfranco/data
python3 generate.py > country_data.js
```

This calls the [RestCountries API](https://restcountries.com) and outputs `country_data.js` with updated areas (converted from km² to mi²). After regenerating, the data is automatically used by `tests/test.html`.

To re-embed the TopoJSON into `index.html`, update the `const WORLD_TOPO = ...` assignment in the `<script>` block with the contents of `countries-110m.json`.

## Running Tests

Open `http://localhost:8080/tests/test.html` in your browser. All 11 tests should show green checkmarks.

## Dependencies

All loaded from CDN at runtime:

| Library | Version | Purpose |
|---|---|---|
| [D3](https://d3js.org) | v7 | Geographic projection, SVG rendering |
| [topojson-client](https://github.com/topojson/topojson-client) | v3 | Decode TopoJSON → GeoJSON features |
| [Inter](https://fonts.google.com/specimen/Inter) | — | Font (Google Fonts) |

## Troubleshooting

**Shapes don't appear:** Make sure you're accessing the app via `http://localhost:8080` (not `file://`). The CDN scripts (D3, topojson) must load for shapes to render.

**Country not found:** Try alternate spellings. The alias table covers most common variations. Check `data/country_data.js` → `COUNTRY_ALIASES` for supported names.

**Port already in use:** Change the port: `python3 -m http.server 3000` and open `http://localhost:3000`.
