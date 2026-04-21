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
