# ebsb.de

The EBSB GmbH website as plain static HTML/CSS/JS — no framework, no build step.
Rebuilt from the previous Wix site; all German copy is carried over verbatim.

## Run it locally

```
node scripts/serve.js 8080
```

Then open <http://localhost:8080>. Any static server works; there is nothing to compile.

## Layout

| Path | What |
|---|---|
| `index.html` … `404.html` | one file per page, complete and ready to serve |
| `assets/css/style.css` | the whole design system — tokens at the top |
| `assets/css/fonts.css` | `@font-face` for the self-hosted fonts |
| `assets/js/main.js` | nav, scroll reveal, contact form |
| `assets/fonts/` | Inter + Manrope (woff2, latin + latin-ext) |
| `assets/img/` | every image, as WebP with a PNG/JPEG fallback |
| `scripts/` | one-off helpers, not needed to serve the site |

## Two things still to wire up

**1. The contact form.** Create a free access key at <https://web3forms.com> (no
account required — you just confirm the address that should receive the mail),
then paste it in **two** places:

- `assets/js/main.js` → `const WEB3FORMS_KEY = "…"`
- `kontakt.html` → `<input type="hidden" name="access_key" value="…">`

Until then the form falls back to opening the visitor's mail client, so it is
never a dead end.

**2. Two sets of logos.** TSV Grünwald and Special Olympics are already in.
Still missing:

- **SV Straßlach logo** → replace the `<div class="logo-slot">` in
  `engagement.html` (the markup to use is in a comment right above it)
- **B2B client logos** for *Auswahl unser Kunden* → `assets/img/clients/`, then
  swap the placeholder `<li class="empty">` tiles in `b2b.html` for
  `<li><img src="assets/img/clients/NAME.png" alt="NAME" /></li>`

See `NEXT-STEPS.md` for the full open list.

## Editing

Header and footer are duplicated into every page so the files stay dependency-free.
Edit them in `index.html`, then run:

```
python scripts/sync-chrome.py
```

to copy them into the other pages (it handles the per-page `aria-current` and the
absolute paths `404.html` needs).

`scripts/fetch-assets.py` and `scripts/build-logo.py` re-download and re-process
the images from the old Wix CDN; `scripts/fetch-fonts.py` re-fetches the fonts.
None of them need to run again unless an asset changes.

## Privacy

The site loads **nothing** from a third party — fonts are self-hosted, there is no
analytics and no tracking. The only outbound request is the contact form POST,
and only when someone submits it. That means no cookie banner is required.

Note that `datenschutz.html` still carries the text from the Wix site, which
describes Google Analytics and Xing/LinkedIn/X/Facebook plugins. None of those
exist on this site — that section should be shortened before going live.

## Deploying to GitHub Pages

`CNAME` already contains `ebsb.de`. Push to a repo, enable Pages on the default
branch, then point the DNS at GitHub. Do not change DNS until you have checked
the site on the Pages preview URL.
