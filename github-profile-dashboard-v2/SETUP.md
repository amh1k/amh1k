# Setup and customization

This version avoids unreliable third-party README widgets. Every visible card is a local SVG, so GitHub cannot replace it with broken alt text or a large error panel.

## Install

Copy everything into your profile repository:

```text
amh1k/amh1k
├── .github/workflows/update-profile.yml
├── assets/
├── scripts/generate_profile.py
├── profile.config.json
└── README.md
```

Commit and push. Then open **Actions → Update profile dashboard → Run workflow** once. The workflow uses the repository `GITHUB_TOKEN`, fetches live profile/repository data, regenerates the SVG assets and commits them.

## Replace projects or OSS repositories

Edit only `profile.config.json`.

```json
{
  "projects": [
    {"repo": "OWNER/REPO", "label": "Visible project name"}
  ],
  "oss": [
    {"repo": "OWNER/REPO", "label": "Visible OSS name"}
  ]
}
```

The generator also rewrites the matching links in `README.md`. You edit only `profile.config.json`; the next workflow run updates the card text, links, descriptions, languages, stars, forks and PR counts.

## Change name, intro, stack or social labels

Edit `profile.config.json`, then run the workflow. The generator rewrites the social destinations in `README.md` from the same config because each local SVG button is wrapped in a normal clickable link.

## Live data included

- total stars across public owned repositories
- public repository count
- authored pull request count
- current-year commit and contribution counts
- current and longest contribution streaks
- contribution heatmap
- project description, language, stars and forks
- authored and merged PR counts for each configured OSS repository

## Why this structure

GitHub strips custom CSS and does not provide a general dashboard layout system inside README files. Separate locally generated SVG sections preserve the exact proportions while keeping every link clickable and every data block automatically refreshable.
