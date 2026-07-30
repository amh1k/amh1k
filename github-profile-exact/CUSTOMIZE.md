# Customize this README package

This package is designed to **look very close to the approved dashboard concept** while keeping your project cards and OSS listings editable.

## What is safe to change without regenerating any SVG?

You can freely edit all of these directly in `README.md`:

- Featured project repositories
- OSS repository names and links
- Social/profile links
- GitHub username in widget URLs
- Short bullet descriptions in the OSS block

## Change a featured project card

For each featured project card, update these two places:

```html
<a href="https://github.com/OWNER/REPO">
<img src="https://github-readme-stats.vercel.app/api/pin/?username=OWNER&repo=REPO..." />
```

## Change an OSS repository listing

Replace the badge label and its PR-search URL:

```text
https://github.com/OWNER/REPO/pulls?q=is%3Apr+author%3AYOUR_USERNAME
```

You can also update the bullet text right below the badges.

## Change your GitHub username everywhere

Find and replace `amh1k` inside `README.md`.

That updates:
- GitHub stats
- streak card
- contribution calendar
- contribution activity graph
- PR-search links

## When would you edit the SVG files?

Only if you want to change the **identity text or fixed artwork**:

- `assets/hero.svg` → name, intro sentence, waveform header
- `assets/terminal-cta.svg` → footer quote card
- `assets/section-divider.svg` → decorative line only

## Files included

```text
README.md
CUSTOMIZE.md
assets/
  hero.svg
  terminal-cta.svg
  section-divider.svg
```
