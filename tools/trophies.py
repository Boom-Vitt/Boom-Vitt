"""Trophy card in the BoomBigNose theme from live GitHub stats (public trophy services were down).

  GITHUB_TOKEN=... python tools/trophies.py <login> <out.svg>
"""
import json
import os
import sys
import urllib.request

LOGIN, OUT = sys.argv[1:3]
Q = """query($login:String!){user(login:$login){followers{totalCount}pullRequests{totalCount}issues{totalCount}
repositories(ownerAffiliations:OWNER,privacy:PUBLIC,first:100,isFork:false){totalCount nodes{stargazerCount}}
contributionsCollection{totalCommitContributions restrictedContributionsCount}}}"""
RANKS = ["SSS", "SS", "S", "AAA", "AA", "A", "B", "C"]
# value needed for each rank, best first
TIERS = {
    "Stars": [2000, 700, 200, 100, 50, 30, 10, 1],
    "Contributions": [4000, 2000, 1000, 500, 200, 100, 10, 1],
    "Followers": [1000, 400, 200, 100, 50, 20, 10, 1],
    "Pull requests": [1000, 500, 200, 100, 50, 20, 10, 1],
    "Issues": [1000, 500, 200, 100, 50, 20, 10, 1],
    "Repositories": [100, 80, 50, 40, 30, 20, 10, 1],
}
COLOR = {"SSS": "#F472B6", "SS": "#F59E0B", "S": "#FBBF24", "AAA": "#5EEAD4", "AA": "#5EEAD4", "A": "#5EEAD4", "B": "#94A3B8", "C": "#B45309"}


def stats():
    req = urllib.request.Request("https://api.github.com/graphql", json.dumps({"query": Q, "variables": {"login": LOGIN}}).encode(),
                                 {"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"})
    u = json.load(urllib.request.urlopen(req, timeout=30))["data"]["user"]
    c = u["contributionsCollection"]
    return {
        "Stars": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        "Contributions": c["totalCommitContributions"] + c["restrictedContributionsCount"],
        "Followers": u["followers"]["totalCount"],
        "Pull requests": u["pullRequests"]["totalCount"],
        "Issues": u["issues"]["totalCount"],
        "Repositories": u["repositories"]["totalCount"],
    }


def rank(name, v):
    return next((r for r, need in zip(RANKS, TIERS[name]) if v >= need), "?")


def card(i, name, v):
    r = rank(name, v)
    col = COLOR.get(r, "#475569")
    x = 10 + i * 198
    return f"""<g transform="translate({x},10)"><g class="in" style="animation-delay:{i * .12:.2f}s">
<rect width="186" height="160" rx="16" fill="#111a2e" stroke="{col}" stroke-opacity=".5"/>
<path d="M68 34h50v10c0 16-11 28-25 28s-25-12-25-28z" fill="{col}"/><path d="M68 40h-10c0 10 6 16 13 17M118 40h10c0 10-6 16-13 17" fill="none" stroke="{col}" stroke-width="4"/>
<rect x="88" y="72" width="10" height="12" fill="{col}"/><rect x="76" y="84" width="34" height="8" rx="3" fill="{col}"/>
<text x="93" y="58" text-anchor="middle" class="rk">{r}</text>
<text x="93" y="118" text-anchor="middle" class="nm">{name}</text>
<text x="93" y="142" text-anchor="middle" class="v" fill="{col}">{v:,}</text></g></g>"""


s = stats()
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1198" height="180" viewBox="0 0 1198 180" role="img" aria-label="GitHub trophies of {LOGIN}">
<style>text{{font-family:Inter,'Segoe UI',Arial,sans-serif}}.rk{{font-size:15px;font-weight:800;fill:#0b1220}}.nm{{font-size:15px;font-weight:600;fill:#cbd5e1}}
.v{{font-size:20px;font-weight:800}}.in{{animation:up .8s cubic-bezier(.2,.8,.2,1) both}}@keyframes up{{from{{opacity:0;transform:translateY(12px)}}}}
@media (prefers-reduced-motion:reduce){{.in{{animation:none}}}}</style>
{''.join(card(i, n, s[n]) for i, n in enumerate(TIERS))}
</svg>
"""
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w", encoding="utf-8").write(svg)
print(json.dumps(s))
