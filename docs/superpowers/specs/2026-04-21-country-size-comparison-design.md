# Country Size Comparison — Design Spec

**Date:** 2026-04-21  
**Type:** Single-file web application  
**Author:** Gianfranco (via Claude Code)

---

## Overview

A utility web app that lets users type in two country names and instantly compare their land areas. The app shows which country is bigger, by how much, and displays each country's SVG outline shape side by side. Target users are students and geography enthusiasts who want a quick, visual answer without doing manual research.

---

## Technical Stack

- **Delivery:** Single self-contained `index.html` file
- **CDN dependencies (internet required):**
  - `d3-geo` — geographic projection and rendering
  - `topojson-client` — parsing world TopoJSON data
- **No backend, no build step, no frameworks**

---

## Embedded Data (baked into the HTML file)

Three JavaScript variables defined in a `<script>` block:

| Variable | Contents | Approx. Size |
|---|---|---|
| `WORLD_TOPO` | Natural Earth 110m simplified TopoJSON | ~120 KB |
| `COUNTRIES` | ISO alpha-3 → `{ area: number, numeric: string }` (~250 entries) | ~10 KB |
| `COUNTRY_ALIASES` | Lowercase name/abbreviation → ISO alpha-3 | ~6 KB |

`COUNTRIES` combines the area data and the ISO numeric code (e.g. `"840"` for USA) needed to look up features in the TopoJSON, which uses ISO numeric as its key.

The alias table handles common variations: `"usa"`, `"united states"`, `"us"` → `"USA"`; `"uk"`, `"england"`, `"britain"` → `"GBR"`; etc.

All user input is lowercased before alias lookup so casing is irrelevant.

---

## UI Layout

### Header
- App title "Country Size Comparison" (left)
- Light/dark mode toggle button (right)
- Mode preference persisted in `localStorage`

### Input Row
- Two text inputs side by side, one labeled "Country 1", one labeled "Country 2"
- Bold "Compare" button centered below
- Compare button disabled (grayed out) until both fields have text
- Pressing Enter in either input triggers Compare
- On mobile (< 640px): inputs stack vertically

### Welcome State
- Shown on initial load and after Restart
- Centered message: "Type two countries above to compare their sizes"
- Subtle world map or globe icon

### Results Area (replaces welcome state after comparison)

**Country Cards (two, side by side):**
- Each card gets one of 6 vibrant accent colors (coral, teal, amber, violet, sky blue, lime). On each Compare, card 1 is assigned a random color from the palette; card 2 is assigned a different random color from the remaining 5.
- Top of card: SVG viewport showing country shape, centered and scaled to fill the space, rendered in the card's accent color
- Below shape: country name in bold
- Below name: land area formatted with commas (e.g., `3,796,742 mi²`)

**Result Banner (below both cards):**
- Shows the winning country and multiplier: `"Mexico is 36× bigger than New Zealand"`
- Banner background uses the winner's accent color

**Restart Button:**
- Bold, centered below the result banner
- Fades results out, clears inputs, returns to welcome state

### Error States
- Unknown country: card shows red border + `"Country not found — try another name"`
- Result banner hidden until both cards are valid
- Same country entered twice: banner shows `"You entered the same country twice!"`

---

## Visual Style

- **Vibe:** Bold & colorful, inspired by TrueSize.com
- **Dark mode:** Deep navy background, white text
- **Light mode:** Clean white background, dark text
- **Typography:** `Inter` (Google Fonts) or system sans-serif fallback; large chunky numbers for area figures
- **Accent palette:** 6 colors — coral `#FF6B6B`, teal `#4ECDC4`, amber `#FFE66D`, violet `#A78BFA`, sky blue `#38BDF8`, lime `#84CC16`

---

## Interactions & Transitions

- Results fade in on Compare (~300ms CSS transition)
- Country shape SVGs animate in with a subtle scale-up effect
- Compare button shows a spinner while D3 renders shapes
- Restart button fades results out before resetting

---

## Rendering Logic

1. User submits two country names
2. Each name is lowercased → alias table lookup → ISO alpha-3 code
3. ISO alpha-3 → `COUNTRIES[code].numeric` → TopoJSON feature lookup
4. D3 `geoPath` + `fitSize` projection renders the feature into an `<svg>` element sized to the card
5. ISO alpha-3 → `COUNTRIES[code].area` → display area
6. Compare the two areas → compute multiplier → display result banner

---

## Edge Cases

| Scenario | Behavior |
|---|---|
| Unknown name | Red error card; other card renders normally |
| Same country twice | Both cards render; banner says "You entered the same country twice!" |
| Empty input | Compare button disabled; no error shown |
| Very small country (e.g., Vatican) | Shape scaled up via `fitSize` to fill card; area number shown normally |
| Name with different casing | Lowercased before lookup; all variants match |

---

## Out of Scope

- Comparison by population, GDP, or other metrics
- More than two countries at once
- Saving or sharing comparisons
- Animations beyond simple fade/scale transitions
