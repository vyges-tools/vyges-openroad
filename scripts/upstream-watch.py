#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Weekly digest of upstream OpenROAD changes since the commit this repo pins.

Reads the pin from upstream.yaml, compares it with upstream master through the GitHub REST API,
and writes a Markdown report: the commits per module, the functions each one touched (from the
diff hunk headers), the commits that changed regression goldens, the OpenSTA submodule's
movement, and the open pull requests and issues active in the last week.

Public facts about the upstream project only. Standard library only, so the workflow needs no
installs. Token: GITHUB_TOKEN (the Actions token is enough for the ~150 calls a week takes).

Usage: upstream-watch.py --out reports/upstream-watch [--date YYYY-MM-DD] [--days 7]
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict

OR_REPO = "The-OpenROAD-Project/OpenROAD"
STA_REPO = "The-OpenROAD-Project/OpenSTA"
API = "https://api.github.com"
# Regression goldens: a commit that changes one changed the tool's observable behaviour.
GOLDEN = re.compile(r"\.(ok|defok|guideok|segsok|vok|odbok|spefok|rptok|lefok|gdsok)$")
HUNK_FUNC = re.compile(r"^@@ [^@]* @@ ?(.*)$", re.M)


def api(path, params=None):
    url = path if path.startswith("http") else f"{API}/{path}"
    if params:
        url += ("&" if "?" in url else "?") + "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "X-GitHub-Api-Version": "2022-11-28"})
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def read_pin(path="upstream.yaml"):
    for line in open(path):
        m = re.match(r"\s*commit:\s*([0-9a-f]{40})", line)
        if m:
            return m.group(1)
    sys.exit("upstream.yaml: no 40-hex commit")


def module_of(filename):
    parts = filename.split("/")
    if parts[0] == "src" and len(parts) > 1:
        return parts[1]
    return "(top)"


def func_context(patch):
    """Function names from the hunk headers git puts after the second @@."""
    names = []
    for ctx in HUNK_FUNC.findall(patch or ""):
        ctx = ctx.strip()
        if not ctx:
            continue
        # Only a C/C++/Tcl function signature names a function; a bare context line (a BUILD
        # list, a DEF statement) says nothing about which behaviour moved, so it is dropped.
        m = re.search(r"([A-Za-z_][\w:~]*)\s*\(", ctx)
        if m and m.group(1) not in ("if", "for", "while", "switch", "return", "cc_test", "cc_library"):
            names.append(m.group(1))
        elif re.match(r"(class|struct|namespace|proc)\s", ctx):
            names.append(ctx.split("{")[0].strip()[:60])
    return names


def submodule_sha(ref):
    try:
        return api(f"repos/{OR_REPO}/contents/src/sta", {"ref": ref}).get("sha")
    except urllib.error.HTTPError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--days", type=int, default=7)
    a = ap.parse_args()

    pin = read_pin()
    head = api(f"repos/{OR_REPO}/commits/master")["sha"]
    cmp = api(f"repos/{OR_REPO}/compare/{pin}...{head}", {"per_page": "250"})
    commits = [c for c in cmp["commits"] if len(c["parents"]) == 1]  # merges add no change of their own

    by_module = defaultdict(list)       # module -> [(sha, title, [funcs], [goldens])]
    golden_commits = []
    for c in commits:
        d = api(f"repos/{OR_REPO}/commits/{c['sha']}")
        title = d["commit"]["message"].split("\n")[0]
        mods = defaultdict(lambda: ([], []))
        for f in d.get("files", []):
            m = module_of(f["filename"])
            funcs, golds = mods[m]
            funcs.extend(func_context(f.get("patch")))
            if GOLDEN.search(f["filename"]):
                golds.append(f["filename"])
        for m, (funcs, golds) in mods.items():
            by_module[m].append((c["sha"][:10], title, sorted(set(funcs)), golds))
            if golds:
                golden_commits.append((m, c["sha"][:10], title, golds))

    sta_pin, sta_head = submodule_sha(pin), submodule_sha(head)
    sta_commits = []
    if sta_pin and sta_head and sta_pin != sta_head:
        sc = api(f"repos/{STA_REPO}/compare/{sta_pin}...{sta_head}", {"per_page": "250"})
        sta_commits = [(x["sha"][:9], x["commit"]["message"].split("\n")[0])
                       for x in sc["commits"] if len(x["parents"]) == 1]

    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)).strftime("%Y-%m-%d")
    q = f"repo:{OR_REPO} updated:>={since}"
    def search(kind):
        r = api("search/issues", {"q": urllib.request.quote(f"{q} is:{kind}"), "per_page": "100",
                                  "sort": "updated"})
        return r["items"], r["total_count"]
    prs, prs_total = search("pr")
    issues, issues_total = search("issue")

    L = [f"# Upstream OpenROAD — weekly digest {a.date}", "",
         f"- Pinned: `{pin[:12]}` · master: `{head[:12]}` · {cmp['ahead_by']} commits ahead "
         f"({len(commits)} non-merge)",
         f"- OpenSTA submodule: `{(sta_pin or '?')[:9]}` → `{(sta_head or '?')[:9]}`"
         + (f" ({len(sta_commits)} commits)" if sta_commits else " (unchanged)"),
         f"- Window for pull requests and issues: updated since {since}", ""]
    L += ["## Behaviour changes (regression goldens updated)", ""]
    if golden_commits:
        L += ["| Module | Commit | Title | Goldens |", "|---|---|---|---|"]
        for m, s, t, g in golden_commits:
            shown = ", ".join(x.split("/")[-1] for x in g[:6]) + (f" +{len(g)-6}" if len(g) > 6 else "")
            L.append(f"| {m} | `{s}` | {t} | {shown} |")
    else:
        L.append("None.")
    L += ["", "## Commits by module (functions from the diff hunk headers)", ""]
    for m in sorted(by_module, key=lambda k: (-len(by_module[k]), k)):
        L.append(f"### {m} ({len(by_module[m])})")
        for s, t, funcs, _ in by_module[m]:
            fx = f" — {', '.join(funcs[:12])}" + (" …" if len(funcs) > 12 else "") if funcs else ""
            L.append(f"- `{s}` {t}{fx}")
        L.append("")
    if sta_commits:
        L += ["## OpenSTA", ""] + [f"- `{s}` {t}" for s, t in sta_commits] + [""]
    for name, items, total in (("Pull requests", prs, prs_total), ("Issues", issues, issues_total)):
        shown = f"{len(items)} of {total}, most recent first" if total > len(items) else f"{total}"
        L += [f"## {name} updated this week ({shown})", ""]
        for it in items:
            state = it["state"]
            if it.get("pull_request", {}).get("merged_at"):
                state = "merged"
            L.append(f"- #{it['number']} [{state}] {it['title']}")
        L.append("")

    os.makedirs(a.out, exist_ok=True)
    body = "\n".join(L) + "\n"
    for fn in (f"{a.date}.md", "latest.md"):
        with open(os.path.join(a.out, fn), "w") as fh:
            fh.write(body)
    print(f"wrote {a.out}/{a.date}.md: {len(commits)} commits, {len(golden_commits)} golden changes, "
          f"{len(prs)} PRs, {len(issues)} issues")


if __name__ == "__main__":
    main()
