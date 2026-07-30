# Customizing this profile README

The design is deliberately reusable. **Project names and OSS repository names are stored in `README.md`, not in either SVG asset.**

## Change a featured project

In the `~/featured-projects` block, update these two values for one card:

```html
href="https://github.com/OWNER/REPO"
...
username=OWNER&repo=REPO
```

The card is generated dynamically from GitHub data, so changing the URL is enough.

## Change an OSS repository

In the `~/open-source` block, edit the badge label and its link. The current links show pull requests authored by `amh1k` inside each upstream repository:

```text
https://github.com/OWNER/REPO/pulls?q=is%3Apr+author%3Aamh1k
```

## Reuse for another GitHub account

Find and replace:

- `amh1k` with the new GitHub username
- personal links and email
- the name and tagline inside `assets/header.svg`

Editing SVG text is not regeneration; open the SVG in any text editor and replace the visible strings.

## Live-data behavior

- The contribution graph fetches recent GitHub activity automatically.
- Project cards fetch repository metadata automatically.
- These public services use caching, so updates are automatic but not instant.

## Files

```text
README.md
assets/header.svg          # animated; identity only
assets/section-divider.svg # static reusable divider
CUSTOMIZE.md
```
