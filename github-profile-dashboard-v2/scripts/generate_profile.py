#!/usr/bin/env python3
"""Generate GitHub-safe profile SVG assets from profile.config.json.

The script uses only the Python standard library. With GITHUB_TOKEN set, it
fetches live GitHub data. Without a token it renders the configured fallbacks.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import os
import random
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "profile.config.json"
ASSETS = ROOT / "assets"
API = "https://api.github.com"
GRAPHQL = "https://api.github.com/graphql"

BG = "#0d1117"
PANEL = "#0b0f14"
BORDER = "#26303a"
BORDER_SOFT = "#1c2530"
TEXT = "#e6edf3"
SOFT = "#b8c0cc"
MUTED = "#8b949e"
CYAN = "#22d3ee"
BLUE = "#60a5fa"
PURPLE = "#a855f7"
GREEN = "#39d353"


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def read_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def request_json(url: str, token: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-svg-generator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_live(config: dict[str, Any], token: str) -> dict[str, Any] | None:
    if not token:
        return None

    username = config["username"]
    query = """
    query Profile($login: String!, $prQuery: String!) {
      user(login: $login) {
        repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC) {
          totalCount
          nodes { stargazerCount }
        }
        contributionsCollection {
          totalCommitContributions
          totalIssueContributions
          totalPullRequestContributions
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays { date contributionCount weekday }
            }
          }
        }
      }
      search(query: $prQuery, type: ISSUE) { issueCount }
    }
    """
    try:
        raw = request_json(
            GRAPHQL,
            token,
            method="POST",
            payload={
                "query": query,
                "variables": {"login": username, "prQuery": f"author:{username} is:pr"},
            },
        )
        if raw.get("errors"):
            raise RuntimeError(raw["errors"])
        user = raw["data"]["user"]
        collection = user["contributionsCollection"]
        weeks = collection["contributionCalendar"]["weeks"]
        days = [day for week in weeks for day in week["contributionDays"]]
        current, longest = streaks(days)
        stats = {
            "public_repos": user["repositories"]["totalCount"],
            "stars": sum(node["stargazerCount"] for node in user["repositories"]["nodes"]),
            "pull_requests": raw["data"]["search"]["issueCount"],
            "commits": collection["totalCommitContributions"],
            "total_contributions": collection["contributionCalendar"]["totalContributions"],
            "current_streak": current,
            "longest_streak": longest,
        }

        projects = []
        for item in config["projects"]:
            project = dict(item)
            try:
                repo_data = request_json(f"{API}/repos/{item['repo']}", token)
                project.update(
                    description=repo_data.get("description") or item.get("fallback_description", ""),
                    language=repo_data.get("language") or item.get("fallback_language", "Code"),
                    stars=repo_data.get("stargazers_count", 0),
                    forks=repo_data.get("forks_count", 0),
                    url=repo_data.get("html_url") or f"https://github.com/{item['repo']}",
                )
            except Exception:
                project.update(
                    description=item.get("fallback_description", ""),
                    language=item.get("fallback_language", "Code"),
                    stars=item.get("fallback_stars", 0),
                    forks=item.get("fallback_forks", 0),
                    url=f"https://github.com/{item['repo']}",
                )
            projects.append(project)

        oss = []
        for item in config["oss"]:
            repo = item["repo"]
            base_q = f"author:{username} is:pr repo:{repo}"
            merged_q = f"author:{username} is:pr is:merged repo:{repo}"
            try:
                total = request_json(f"{API}/search/issues?q={urllib.parse.quote_plus(base_q)}&per_page=1", token).get("total_count", 0)
                merged = request_json(f"{API}/search/issues?q={urllib.parse.quote_plus(merged_q)}&per_page=1", token).get("total_count", 0)
            except Exception:
                total, merged = 0, 0
            oss.append({**item, "prs": total, "merged": merged, "url": f"https://github.com/{repo}/pulls?q=is%3Apr+author%3A{username}"})

        return {"stats": stats, "days": days, "projects": projects, "oss": oss, "live": True}
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError, KeyError, TypeError, ValueError) as exc:
        print(f"warning: live GitHub fetch failed: {exc}")
        return None


def streaks(days: list[dict[str, Any]]) -> tuple[int, int]:
    parsed = sorted((dt.date.fromisoformat(d["date"]), int(d["contributionCount"])) for d in days)
    if not parsed:
        return 0, 0
    longest = 0
    run = 0
    for _, count in parsed:
        if count > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    today = dt.date.today()
    by_date = dict(parsed)
    cursor = today if by_date.get(today, 0) > 0 else today - dt.timedelta(days=1)
    current = 0
    while by_date.get(cursor, 0) > 0:
        current += 1
        cursor -= dt.timedelta(days=1)
    return current, longest


def fallback_data(config: dict[str, Any]) -> dict[str, Any]:
    projects = []
    for item in config["projects"]:
        projects.append(
            {
                **item,
                "description": item.get("fallback_description", ""),
                "language": item.get("fallback_language", "Code"),
                "stars": item.get("fallback_stars", 0),
                "forks": item.get("fallback_forks", 0),
                "url": f"https://github.com/{item['repo']}",
            }
        )
    oss = [{**item, "prs": 0, "merged": 0, "url": f"https://github.com/{item['repo']}/pulls?q=is%3Apr+author%3A{config['username']}"} for item in config["oss"]]
    return {
        "stats": dict(config["fallback_stats"]),
        "days": preview_days(config["username"]),
        "projects": projects,
        "oss": oss,
        "live": False,
    }


def preview_days(seed: str) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    today = dt.date.today()
    start = today - dt.timedelta(days=52 * 7 - 1)
    days = []
    for i in range(52 * 7):
        date = start + dt.timedelta(days=i)
        # A restrained placeholder pattern; the workflow replaces this with live data.
        count = 0 if rng.random() < 0.48 else rng.choice([1, 1, 2, 2, 3, 4, 6])
        days.append({"date": date.isoformat(), "contributionCount": count, "weekday": date.weekday()})
    return days


def write(name: str, content: str) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / name).write_text(content, encoding="utf-8")


def svg_start(width: int, height: int, title: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{BLUE}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
  <linearGradient id="faint" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".2" stop-color="{CYAN}" stop-opacity=".55"/><stop offset=".8" stop-color="{PURPLE}" stop-opacity=".55"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></linearGradient>
  <filter id="glow" x="-30%" y="-100%" width="160%" height="300%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>
  .mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}}
  .sans{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
</style>
'''


def hero_svg(config: dict[str, Any]) -> str:
    name = esc(config["name"])
    line1, line2 = [esc(x) for x in config["headline"]]
    return svg_start(1400, 250, f"{name} profile header") + f'''
<style>
  .cursor{{animation:blink 1s steps(1,end) infinite}} .wave{{stroke-dasharray:12 10;animation:flow 10s linear infinite}}
  .d1{{animation:pulse 2.5s ease-in-out infinite}} .d2{{animation:pulse 2.5s ease-in-out .8s infinite}} .d3{{animation:pulse 2.5s ease-in-out 1.6s infinite}}
  @keyframes blink{{50%{{opacity:0}}}} @keyframes flow{{to{{stroke-dashoffset:-360}}}} @keyframes pulse{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}
  @media(prefers-reduced-motion:reduce){{.cursor,.wave,.d1,.d2,.d3{{animation:none}}}}
</style>
<rect width="1400" height="250" rx="18" fill="{BG}"/>
<rect x="1" y="1" width="1398" height="248" rx="17" fill="none" stroke="{BORDER_SOFT}"/>
<text x="38" y="70" class="mono" font-size="52" font-weight="700" fill="{TEXT}">Hi, I’m </text>
<text x="270" y="70" class="mono" font-size="52" font-weight="700" fill="url(#accent)">{name}</text>
<text x="768" y="70" class="mono" font-size="38" fill="{CYAN}">*</text>
<rect x="812" y="26" width="7" height="54" rx="3" fill="{TEXT}" class="cursor"/>
<text x="40" y="126" class="mono" font-size="22" fill="{SOFT}">{line1}</text>
<text x="40" y="166" class="mono" font-size="22" fill="{SOFT}">{line2.split('always learning.')[0]}</text>
<text x="604" y="166" class="mono" font-size="22" fill="url(#accent)">always learning.</text>
<g transform="translate(790,26)" fill="none" stroke-linecap="round">
  <path d="M0 87 H560" stroke="url(#faint)"/>
  <path class="wave" filter="url(#glow)" d="M0 87 C35 87 42 72 72 72 C104 72 111 104 142 104 C176 104 184 48 220 48 C255 48 262 128 300 128 C338 128 346 42 386 42 C425 42 432 118 470 118 C506 118 522 73 560 73" stroke="url(#accent)" stroke-width="3"/>
  <circle class="d1" cx="142" cy="104" r="4" fill="{CYAN}" stroke="none"/><circle class="d2" cx="300" cy="128" r="4" fill="{BLUE}" stroke="none"/><circle class="d3" cx="470" cy="118" r="4" fill="{PURPLE}" stroke="none"/>
</g>
<path d="M38 220 H1362" stroke="{BORDER}"/>
</svg>'''


def social_button(label: str, key: str) -> str:
    icon = {"portfolio": "//", "linkedin": "in", "email": "@", "leetcode": "&lt;&gt;", "codeforces": "|||"}.get(key, "-")
    color = {"portfolio": CYAN, "linkedin": BLUE, "email": SOFT, "leetcode": "#facc15", "codeforces": PURPLE}.get(key, CYAN)
    return svg_start(250, 72, label) + f'''
<rect x="1" y="1" width="248" height="70" rx="12" fill="{BG}" stroke="{BORDER}"/>
<text x="24" y="47" class="mono" font-size="24" font-weight="700" fill="{color}">{icon}</text>
<text x="68" y="45" class="mono" font-size="17" font-weight="700" letter-spacing="1.6" fill="{TEXT}">{esc(label)}</text>
</svg>'''


def section_title(title: str, symbol: str) -> str:
    return svg_start(1400, 70, title) + f'''
<rect width="1400" height="70" fill="{BG}"/>
<text x="6" y="45" class="mono" font-size="30" fill="{CYAN}">{esc(symbol)}</text>
<text x="52" y="45" class="sans" font-size="25" font-weight="700" fill="{TEXT}">{esc(title)}</text>
<path d="M300 36 H1394" stroke="{BORDER}"/>
</svg>'''


def level_color(count: int) -> str:
    if count <= 0:
        return "#151b23"
    if count == 1:
        return "#0d4f5b"
    if count <= 3:
        return "#0f7182"
    if count <= 6:
        return "#17a9bd"
    return CYAN


def stats_svg(config: dict[str, Any], data: dict[str, Any]) -> str:
    s = data["stats"]
    days = data["days"][-31 * 7:]
    weeks = [days[i:i+7] for i in range(0, len(days), 7)]
    status = "LIVE" if data["live"] else "SYNC ON FIRST WORKFLOW RUN"
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    chunks = [svg_start(1400, 315, "GitHub statistics and contribution activity")]
    chunks.append(f'<rect width="1400" height="315" fill="{BG}"/>')
    panels = [(0, 0, 515, 290), (535, 0, 245, 290), (800, 0, 600, 290)]
    for x, y, w, h in panels:
        chunks.append(f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}" rx="15" fill="{PANEL}" stroke="{BORDER}"/>')
    chunks.append(f'<text x="28" y="43" class="mono" font-size="21" fill="{CYAN}">{esc(config["username"])}-010</text><text x="168" y="43" class="mono" font-size="20" fill="{TEXT}">/ GitHub Stats</text>')
    rows = [("*", "Total Stars Earned", s["stars"]), ("+", "Commits this year", s["commits"]), ("PR", "Pull Requests", s["pull_requests"]), ("[]", "Public Repositories", s["public_repos"])]
    y = 88
    for icon, label, value in rows:
        chunks.append(f'<text x="28" y="{y}" class="mono" font-size="21" fill="{CYAN}">{icon}</text><text x="62" y="{y}" class="mono" font-size="18" fill="{SOFT}">{esc(label)}:</text><text x="350" y="{y}" class="mono" font-size="18" fill="{TEXT}">{esc(value)}</text>')
        y += 48
    # ring
    chunks.append(f'<circle cx="446" cy="153" r="57" fill="none" stroke="#202635" stroke-width="12"/><circle cx="446" cy="153" r="57" fill="none" stroke="url(#accent)" stroke-width="12" stroke-linecap="round" stroke-dasharray="286 358" transform="rotate(-90 446 153)"/><text x="446" y="165" text-anchor="middle" class="mono" font-size="37" fill="{TEXT}">{esc(config.get("rank_label", "A+"))}</text>')
    # streak
    chunks.append(f'<text x="560" y="43" class="mono" font-size="20" fill="{SOFT}">Current Streak</text><text x="658" y="135" text-anchor="middle" class="mono" font-size="55" fill="{CYAN}">{esc(s["current_streak"])}</text><text x="658" y="174" text-anchor="middle" class="mono" font-size="24" fill="{TEXT}">days</text><text x="658" y="224" text-anchor="middle" class="mono" font-size="16" fill="{PURPLE}">longest: {esc(s["longest_streak"])}</text>')
    # heatmap
    chunks.append(f'<text x="826" y="43" class="mono" font-size="20" fill="{TEXT}">GitHub Contributions</text><text x="1370" y="64" text-anchor="end" class="mono" font-size="12" fill="{MUTED}">{esc(status)}</text>')
    x0, y0, cell, gap = 828, 74, 12, 5
    for wi, week in enumerate(weeks):
        for di, day in enumerate(week):
            count = int(day.get("contributionCount", 0))
            chunks.append(f'<rect x="{x0 + wi*(cell+gap)}" y="{y0 + di*(cell+gap)}" width="{cell}" height="{cell}" rx="2" fill="{level_color(count)}"/>')
    chunks.append(f'<circle cx="829" cy="258" r="5" fill="{GREEN}"/><text x="844" y="264" class="mono" font-size="14" fill="{MUTED}">updated {esc(now)}</text><text x="1370" y="264" text-anchor="end" class="mono" font-size="14" fill="{SOFT}">{esc(s["total_contributions"])} contributions</text>')
    chunks.append('</svg>')
    return ''.join(chunks)


def wrap_lines(text: str, width: int = 42, limit: int = 2) -> list[str]:
    lines = textwrap.wrap(text or "", width=width, break_long_words=False, break_on_hyphens=False)
    lines = lines[:limit]
    if len(lines) == limit and len(' '.join(lines)) < len(text):
        lines[-1] = lines[-1].rstrip(' .') + '…'
    return lines or [""]


def project_svg(project: dict[str, Any], index: int) -> str:
    title = project.get("label") or project["repo"].split("/")[-1]
    lines = wrap_lines(project.get("description", ""), 42, 2)
    icon = ["[]", "~", "&lt;/&gt;"][index % 3]
    accent = [CYAN, PURPLE, BLUE][index % 3]
    chunks = [svg_start(440, 230, title), f'<rect x="1" y="1" width="438" height="228" rx="16" fill="{PANEL}" stroke="{BORDER}"/>']
    chunks.append(f'<text x="28" y="68" class="mono" font-size="42" fill="{accent}">{icon}</text><text x="94" y="58" class="mono" font-size="23" font-weight="700" fill="{TEXT}">{esc(title)}</text>')
    for i, line in enumerate(lines):
        chunks.append(f'<text x="94" y="{94+i*31}" class="mono" font-size="16" fill="{SOFT}">{esc(line)}</text>')
    chunks.append(f'<path d="M24 170 H416" stroke="{BORDER_SOFT}"/><circle cx="32" cy="200" r="7" fill="{accent}"/><text x="50" y="206" class="mono" font-size="16" fill="{SOFT}">{esc(project.get("language", "Code"))}</text><text x="252" y="206" class="mono" font-size="16" fill="{SOFT}">* {esc(project.get("stars",0))}</text><text x="344" y="206" class="mono" font-size="16" fill="{SOFT}">fork {esc(project.get("forks",0))}</text>')
    chunks.append('</svg>')
    return ''.join(chunks)


def oss_card_svg(item: dict[str, Any], index: int) -> str:
    accent = [CYAN, BLUE, PURPLE][index % 3]
    return svg_start(300, 96, item["label"]) + f'''
<rect x="1" y="1" width="298" height="94" rx="13" fill="{PANEL}" stroke="{BORDER}"/>
<circle cx="30" cy="48" r="14" fill="none" stroke="{accent}" stroke-width="4"/><path d="M22 48 h16 M30 40 v16" stroke="{accent}" stroke-width="2"/>
<text x="58" y="42" class="mono" font-size="16" font-weight="700" fill="{TEXT}">{esc(item['label'])}</text>
<text x="58" y="68" class="mono" font-size="13" fill="{MUTED}">{esc(item.get('prs',0))} PRs · {esc(item.get('merged',0))} merged</text>
</svg>'''


def oss_graph_svg(items: list[dict[str, Any]], live: bool) -> str:
    values = [int(x.get("prs", 0)) for x in items]
    if not live and max(values, default=0) == 0:
        values = [3, 2, 1]
    maxv = max(values + [1])
    bars = []
    for i, (item, value) in enumerate(zip(items, values)):
        h = 15 + int(38 * value / maxv)
        x = 170 + i * 36
        bars.append(f'<rect x="{x}" y="{72-h}" width="18" height="{h}" rx="4" fill="{[CYAN,BLUE,PURPLE][i%3]}" opacity=".9"/>')
    status = "live PR activity" if live else "preview — workflow syncs live data"
    return svg_start(440, 96, "Open source contribution pulse") + f'''
<rect x="1" y="1" width="438" height="94" rx="13" fill="{PANEL}" stroke="{BORDER}"/>
<text x="24" y="38" class="mono" font-size="17" font-weight="700" fill="{TEXT}">OSS contribution pulse</text>
<text x="24" y="66" class="mono" font-size="12" fill="{MUTED}">{esc(status)}</text>
<path d="M154 76 H412" stroke="{BORDER_SOFT}"/>{''.join(bars)}
</svg>'''


def footer_svg(config: dict[str, Any]) -> str:
    stack = "  ·  ".join(config.get("stack", []))
    return svg_start(1400, 145, "Code Review Learn Repeat") + f'''
<rect x="1" y="1" width="1398" height="143" rx="16" fill="{PANEL}" stroke="{BORDER}"/>
<rect x="28" y="24" width="4" height="96" rx="2" fill="{CYAN}"/>
<text x="62" y="58" class="mono" font-size="23" fill="{TEXT}">&gt; Code. Review. Learn. </text><text x="356" y="58" class="mono" font-size="23" fill="{PURPLE}">Repeat.</text>
<text x="62" y="94" class="mono" font-size="16" fill="{MUTED}">Building software beyond the happy path.</text>
<text x="1360" y="57" text-anchor="end" class="mono" font-size="18" fill="url(#accent)">{esc(stack)}</text>
<text x="1360" y="95" text-anchor="end" class="mono" font-size="14" fill="{MUTED}">profile assets generated from profile.config.json</text>
</svg>'''


def write_readme(config: dict[str, Any]) -> None:
    socials = "\n  ".join(
        f'<a href="{esc(item["url"])}"><img src="./assets/social-{esc(item["key"])}.svg" width="18.5%" alt="{esc(item["label"])}" /></a>'
        for item in config["socials"]
    )
    projects = "\n  ".join(
        f'<a href="https://github.com/{esc(item["repo"])}"><img src="./assets/project-{i+1}.svg" width="32%" alt="{esc(item.get("label") or item["repo"].split("/")[-1])}" /></a>'
        for i, item in enumerate(config["projects"])
    )
    oss_count = max(1, len(config["oss"]))
    oss_width = "22%" if oss_count == 3 else f"{max(14, int(66 / oss_count))}%"
    oss_cards = "\n  ".join(
        f'<a href="https://github.com/{esc(item["repo"])}/pulls?q=is%3Apr+author%3A{esc(config["username"])}"><img src="./assets/oss-{i+1}.svg" width="{oss_width}" alt="{esc(item["label"])} contributions" /></a>'
        for i, item in enumerate(config["oss"])
    )
    name = esc(config["name"])
    readme = (
        "<!-- AUTO-GENERATED by scripts/generate_profile.py. Edit profile.config.json instead. -->\n\n"
        f'<p align="center">\n  <img src="./assets/hero.svg" width="100%" alt="{name}" />\n</p>\n\n'
        f'<p align="center">\n  {socials}\n</p>\n\n'
        '<p align="center">\n  <img src="./assets/stats.svg" width="100%" alt="GitHub statistics and contribution activity" />\n</p>\n\n'
        '<p align="center"><img src="./assets/section-projects.svg" width="100%" alt="Featured Projects" /></p>\n\n'
        f'<p align="center">\n  {projects}\n</p>\n\n'
        '<p align="center"><img src="./assets/section-oss.svg" width="100%" alt="Open Source Contributions" /></p>\n\n'
        f'<p align="center">\n  {oss_cards}\n  <img src="./assets/oss-graph.svg" width="32%" alt="Open source contribution graph" />\n</p>\n\n'
        '<p align="center">\n  <img src="./assets/footer.svg" width="100%" alt="Code. Review. Learn. Repeat." />\n</p>\n'
    )
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

def main() -> None:
    config = read_config()
    token = os.getenv("GITHUB_TOKEN", "").strip()
    data = fetch_live(config, token) or fallback_data(config)

    write("hero.svg", hero_svg(config))
    for social in config["socials"]:
        write(f"social-{social['key']}.svg", social_button(social["label"], social["key"]))
    write("stats.svg", stats_svg(config, data))
    write("section-projects.svg", section_title("Featured Projects", "</>"))
    for i, project in enumerate(data["projects"]):
        write(f"project-{i+1}.svg", project_svg(project, i))
    write("section-oss.svg", section_title("Open Source Contributions", "(o)"))
    for i, item in enumerate(data["oss"]):
        write(f"oss-{i+1}.svg", oss_card_svg(item, i))
    write("oss-graph.svg", oss_graph_svg(data["oss"], data["live"]))
    write("footer.svg", footer_svg(config))
    write_readme(config)
    print(f"generated profile assets ({'live' if data['live'] else 'fallback'} data)")


if __name__ == "__main__":
    main()
