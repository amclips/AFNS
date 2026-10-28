# America First News Syndicate (AFNS) — website v1

Static news site. A small Python script (standard library only, Python 3.12+) turns Markdown
files into plain HTML in `dist/`. No database, no build tools, no npm.

## Quick start
```bash
python3 build.py            # builds ./dist
python3 build.py --serve    # builds and serves at http://localhost:8000/AFNS/
```

## Adding an article
1. Copy `content/_TEMPLATE.md` to `content/<desk>/<slug>.md`.
   Desk folders: `courts`, `fraud-corruption`, `trump-administration`,
   `dsa-democrat-watch`, `geopolitics`, `israel`.
   The file name becomes the URL: `content/courts/my-ruling.md` -> `/AFNS/courts/my-ruling/`
   (the `/AFNS` prefix comes from `base_url`; see Configuration).
2. Fill in the front matter between the `---` lines:
   - `title`, `date` (YYYY-MM-DD), `summary` (required)
   - `key_points:` and `sources:` lists; each source is written as `Title | https://url`
   - optional: `status:` (shown as a badge, for example Alleged, Charged, Convicted, Sentenced, On trial), `featured: true` (the newest featured story is the home lead; other featured stories head the side list), `desk_lead: true` (first on its desk page, with a "Lead story" label), `image:` + `image_alt:` (story photos live in `static/img/stories/`), `image_credit:`, `image_source_url:`, `image_license:` (shown under the photo), `draft: true` (hides it), `byline:` (defaults to "AFNS Research Desk")
3. Write the body in Markdown below the front matter (`##` headings, `-` bullets, `**bold**`, `*italic*`, `[links](url)`, `> quotes`).
4. Run `python3 build.py` to preview. Pushing `main` publishes the site (see Publishing). Do not commit `dist/`.

Newest articles show first. The home page, desk pages, RSS feed (`feed.xml`) and `sitemap.xml` update automatically.

**Before launch:** delete the sample articles (every file with `sample: true`, all titled "Sample: ...").

## Configuration (one spot): `site.json`
- `x_handle` / `x_url`: the AFNS X account. Currently placeholders (`@AFNS_placeholder`, `https://x.com/`). Set the real handle, the URL `https://x.com/<handle>`, and `"x_is_placeholder": false`, then rebuild.
- `base_url`: the public site URL, path included. Currently `https://amclips.github.io/AFNS`. The generator uses that path for every internal link, stylesheet, script, image, favicon, canonical URL, Open Graph URL, RSS item, and sitemap entry. A root-relative Markdown link such as `[courts](/courts/)` is prefixed the same way. Moving to a custom domain later is a `base_url` change only — for example `https://afns.example.com` serves the site at `/`.
- `contact_email`: placeholder; shown on the contact page.
- `desks`: desk names, slugs, and blurbs. Adding a desk here and a matching `content/<slug>/` folder creates a new section.

## Layout
```
build.py          generator
site.json         site config (X handle, domain, desks)
content/          Markdown articles, one folder per desk
assets/           logos, favicon, hero banner, og image (copied to dist/assets)
static/css, js    stylesheet and small JS (mobile menu, copy link)
static/og/        1200×675 share cards, one PNG per real article
static/img/stories/  licensed story photos
CREDITS.csv       photo source, author, and license for each story
tools/og_cards.py share-card generator (Pillow); fonts in tools/fonts/
brand/            original uploaded brand images (not published)
dist/             generated site; this is what you host
screenshot.py     optional Playwright screenshots into screenshots/
```

## Publishing

Live site: <https://amclips.github.io/AFNS/>

**One-time:** in the GitHub repo, open **Settings → Pages** and set **Build and deployment → Source** to **GitHub Actions**. The site does not go live until that is selected.

After that, every push to `main` runs `.github/workflows/pages.yml`, which runs `python3 build.py` and deploys `dist/`. You can also start it from the Actions tab with **Run workflow**. `dist/` is gitignored; Actions builds it.

`base_url` must stay in sync with the Pages URL. It is `https://amclips.github.io/AFNS` for this project site.

## Share cards (X / link previews)
`python3 build.py` makes a 1200×675 branded card for every non-sample article, including stories that have a photo.
Cards are saved to `static/og/<slug>.png` and published under the `base_url` path (`/AFNS/og/<slug>.png` for this site).
Article pages use that file for `og:image` and `twitter:image` (`twitter:card` is `summary_large_image`).
A story with `image:` shows that photo, and a credit line, at the top of the article instead of the card. The card remains the link-preview image. JSON-LD `image` is the photo.
Pages without a card or a photo fall back to `assets/og-image.jpg`. Photo sources are listed in `CREDITS.csv`.

The PNGs are committed, so a build still publishes them when Pillow is not installed. With Pillow, a card is redrawn only when the article, `site.json`, or `tools/og_cards.py` is newer than the PNG. GitHub Actions installs Pillow before `python3 build.py`. Fonts (Oswald and Inter, OFL) are in `tools/fonts/`. The footer text on the cards (`amclips.github.io/AFNS`) is `FOOTER_URL` in `tools/og_cards.py`.

## Not live yet (placeholders)
- Newsletter sign-up and contact form are disabled and marked "Coming soon". No backend, no data collected.
- X account link and contact email are placeholders in `site.json`.
