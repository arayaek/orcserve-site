# ORCSERVE marketing site

A small, maintainable static site for ORCSERVE. Pages are generated from one place so the
chrome (header, footer, `<head>`) and the **brand name** stay consistent everywhere.

## Build

```
python build.py
```

Writes the finished site into `site/` and copies `assets/` alongside it. Open
`site/index.html` in a browser, or host the whole `site/` folder on any static host
(GitHub Pages, Netlify, S3, Azure Static Web Apps, …).

## Structure

```
orcserve-site/
├── build.py            # the generator: brand, nav, page content, shared layout
├── assets/
│   ├── styles.css      # design system (edit the :root tokens to re-skin)
│   ├── site.js         # mobile menu, scroll reveal, footer year
│   ├── logo.svg        # full wordmark
│   └── favicon.svg     # browser-tab icon
└── site/               # GENERATED — do not edit by hand; rebuilt by build.py
```

## How to change things

- **Rename the product** (e.g. ORCSERVE ↔ ORCHSERVE): edit the single `BRAND` dict at the
  top of `build.py`, then rebuild. Nothing else needs to change.
- **Copy / page content:** edit the page functions in `build.py` (`home()`, `platform()`, …).
- **Look and feel:** edit the CSS custom properties in `:root` at the top of `styles.css`
  (colors, radius, fonts) — they cascade through the whole site.
- **Add a page:** write a function returning the page body, then add a row to `PAGES`.

## Before public launch

- Replace the `mailto:` contact form with a secure form service.
- Add real Privacy / Terms / Accessibility pages.
- Confirm the domain, entity name, and any customer/vendor claims are accurate.
- Add analytics and final social links.
- Run a trademark check on the final product name.
