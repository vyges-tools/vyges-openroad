#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Weekly digest of upstream OpenROAD changes since the commit this repo pins.

Reads the pin from upstream.yaml, compares it with upstream master through the GitHub REST API,
and writes a Markdown report: the commits per module, the functions each one touched (from the
diff hunk headers), the commits that changed regression goldens, the commits that changed the
build configuration (compiler flags, toolchain), the OpenSTA submodule's movement, and the open
pull requests and issues active in the last week.

Public facts about the upstream project only. Standard library only, so the workflow needs no
installs. Token: GITHUB_TOKEN. It makes about one call per commit since the pin (plus one per
extra 300 files); the Actions token allows 1000 an hour.

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
# Build configuration: compile/link flags and the C++ toolchain decide the code the compiler emits.
BUILD_RC = re.compile(r"^(\.bazelrc|MODULE\.bazel|bazel/.+)$")
BUILD_FILE = re.compile(r"(^|/)(BUILD|BUILD\.bazel)$|\.bzl$")
FLAG_LINE = re.compile(r"\b(copts|cxxopts|conlyopts|linkopts)\b")
FEATURE_LINE = re.compile(r"\bfeatures\b")
# Bazel features that check includes or headers and leave the generated code as it is.
NEUTRAL_FEATURES = {"layering_check", "parse_headers", "header_modules", "module_maps"}
# Python package locks under bazel/ pin tooling, not the C/C++ build.
NOT_BUILD_CONFIG = re.compile(r"^bazel/.*requirements[^/]*\.(txt|in)$")
TOOLCHAIN_LINE = re.compile(r"\b(llvm|toolchains_llvm|rules_cc|cc_toolchain|clang|libcxx|glibc)\b")


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


def changed_lines(patch):
    """The added and removed lines of a unified diff, without the +/- marker."""
    return [ln[1:] for ln in (patch or "").splitlines()
            if ln[:1] in "+-" and not ln.startswith(("+++", "---"))]


def flag_line(ln):
    """A BUILD line that sets compile/link options, or a feature other than a header check."""
    if FLAG_LINE.search(ln):
        return True
    if FEATURE_LINE.search(ln):
        named = {x.lstrip("-") for x in re.findall(r"[\"']([^\"']+)[\"']", ln)}
        return not named or not named <= NEUTRAL_FEATURES
    return False


def build_config_hit(f):
    """True when a changed file touches the build configuration.

    .bazelrc, MODULE.bazel and bazel/** always count. MODULE.bazel.lock counts only when a changed
    line names a toolchain module (dependency bumps elsewhere in the lock are left out). A BUILD
    file counts only when a changed line touches copts / linkopts, or features other than the
    header checks. Python package locks under bazel/ are left out. A file whose diff GitHub does
    not return (too large) cannot be judged and is left out too."""
    name, patch = f["filename"], f.get("patch")
    if NOT_BUILD_CONFIG.match(name):
        return False
    if BUILD_RC.match(name):
        return True
    if name == "MODULE.bazel.lock":
        return any(TOOLCHAIN_LINE.search(ln) for ln in changed_lines(patch))
    if BUILD_FILE.search(name):
        return any(flag_line(ln) for ln in changed_lines(patch))
    return False


PAGE = 100          # compare: commits per page (the API's maximum)
FILES_PAGE = 300    # commit detail: files per page (the API's default and maximum)
FILES_MAX = 3000    # commit detail: the API never returns more files than this


def compare_all(repo, base, head, warnings):
    """Every commit between base and head, following the compare API's pages.

    Without paging the compare API stops at 250 commits. The count actually listed is checked
    against total_commits; any shortfall becomes a warning, never a silent truncation."""
    commits, page, first = [], 1, None
    while True:
        r = api(f"repos/{repo}/compare/{base}...{head}", {"per_page": str(PAGE), "page": str(page)})
        first = first or r
        batch = r.get("commits", [])
        commits.extend(batch)
        if len(batch) < PAGE or len(commits) >= r.get("total_commits", 0):
            break
        page += 1
    total = first.get("total_commits", len(commits))
    if len(commits) < total:
        warnings.append(f"{repo}: compare listed {len(commits)} of {total} commits")
    return commits, first.get("ahead_by", total), total


def commit_detail(repo, sha, warnings):
    """A commit with its complete file list: the detail API pages files 300 at a time."""
    d = api(f"repos/{repo}/commits/{sha}", {"per_page": str(FILES_PAGE), "page": "1"})
    files, page = list(d.get("files", [])), 1
    while len(files) == page * FILES_PAGE and len(files) < FILES_MAX:
        page += 1
        more = api(f"repos/{repo}/commits/{sha}",
                   {"per_page": str(FILES_PAGE), "page": str(page)}).get("files", [])
        files.extend(more)
        if len(more) < FILES_PAGE:
            break
    if len(files) >= FILES_MAX:
        warnings.append(f"{sha[:10]}: file list capped at {FILES_MAX} by the API")
    no_patch = sum(1 for f in files if f.get("changes") and "patch" not in f)
    if no_patch:
        warnings.append(f"{sha[:10]}: {no_patch} file(s) with no diff returned (too large); "
                        "their functions and build lines are not read")
    d["files"] = files
    return d


def submodule_sha(ref):
    # OpenSTA moved from src/sta to openroad/sta in upstream's src/ -> openroad/ rename
    # (37a84d0a3e, 2026-11-17); try the new path first, then the old one for older refs.
    for path in ("openroad/sta", "src/sta"):
        try:
            return api(f"repos/{OR_REPO}/contents/{path}", {"ref": ref}).get("sha")
        except urllib.error.HTTPError:
            continue
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--days", type=int, default=7)
    a = ap.parse_args()

    pin = read_pin()
    head = api(f"repos/{OR_REPO}/commits/master")["sha"]
    warnings = []
    listed, ahead_by, total = compare_all(OR_REPO, pin, head, warnings)
    commits = [c for c in listed if len(c["parents"]) == 1]  # merges add no change of their own

    by_module = defaultdict(list)       # module -> [(sha, title, [funcs], [goldens])]
    golden_commits = []
    build_commits = []                  # (sha, title, [files])
    for i, c in enumerate(commits):
        try:
            d = commit_detail(OR_REPO, c["sha"], warnings)
        except urllib.error.HTTPError as e:   # rate limit: say where it stopped, never truncate silently
            warnings.append(f"commit details stopped at {i} of {len(commits)} (HTTP {e.code})")
            break
        title = d["commit"]["message"].split("\n")[0]
        mods = defaultdict(lambda: ([], []))
        build_files = [f["filename"] for f in d.get("files", []) if build_config_hit(f)]
        if build_files:
            build_commits.append((c["sha"][:10], title, build_files))
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
        sc, _, _ = compare_all(STA_REPO, sta_pin, sta_head, warnings)
        sta_commits = [(x["sha"][:9], x["commit"]["message"].split("\n")[0])
                       for x in sc if len(x["parents"]) == 1]

    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)).strftime("%Y-%m-%d")
    q = f"repo:{OR_REPO} updated:>={since}"
    def search(kind):
        r = api("search/issues", {"q": urllib.request.quote(f"{q} is:{kind}"), "per_page": "100",
                                  "sort": "updated"})
        return r["items"], r["total_count"]
    prs, prs_total = search("pr")
    issues, issues_total = search("issue")

    L = [f"# Upstream OpenROAD — weekly digest {a.date}", "",
         f"- Pinned: `{pin[:12]}` · master: `{head[:12]}` · {ahead_by} commits ahead "
         f"({len(listed)} listed, {len(commits)} non-merge)",
         f"- OpenSTA submodule: `{(sta_pin or '?')[:9]}` → `{(sta_head or '?')[:9]}`"
         + (f" ({len(sta_commits)} commits)" if sta_commits else " (unchanged)"),
         f"- Window for pull requests and issues: updated since {since}"]
    L += [f"- Coverage warning: {w}" for w in warnings] or ["- Coverage: every commit and file listed"]
    L += [""]
    L += ["## Behaviour changes (regression goldens updated)", ""]
    if golden_commits:
        L += ["| Module | Commit | Title | Goldens |", "|---|---|---|---|"]
        for m, s, t, g in golden_commits:
            shown = ", ".join(x.split("/")[-1] for x in g[:6]) + (f" +{len(g)-6}" if len(g) > 6 else "")
            L.append(f"| {m} | `{s}` | {t} | {shown} |")
    else:
        L.append("None.")
    L += ["", "## Build configuration (compiler flags, toolchain)", ""]
    if build_commits:
        for s, t, files in build_commits:
            shown = ", ".join(files[:6]) + (f" +{len(files)-6}" if len(files) > 6 else "")
            L.append(f"- `{s}` {t} — {shown}")
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
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    print(f"wrote {a.out}/{a.date}.md: {ahead_by} ahead, {len(listed)} listed, {len(commits)} non-merge, {len(golden_commits)} golden changes, "
          f"{len(build_commits)} build configuration changes, "
          f"{len(prs)} PRs, {len(issues)} issues")


if __name__ == "__main__":
    main()
