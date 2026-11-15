# SPDX-License-Identifier: Apache-2.0
"""upstream-watch.py against a fake GitHub API: no network.

Run: python3 -m unittest discover -s tests
"""
import importlib.util
import os
import sys
import tempfile
import unittest
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "upstream_watch", os.path.join(HERE, "..", "scripts", "upstream-watch.py"))
uw = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(uw)

PIN = "a" * 40
HEAD = "b" * 40
N = 600                       # commits since the pin: more than the API's 250 unpaged limit
MERGE_EVERY = 4               # every 4th commit is a merge (two parents)
BIG = {"c" + f"{7:039d}": 650, "c" + f"{9:039d}": 3000}   # commits with many files


def sha(i):
    return "c" + f"{i:039d}"


class FakeApi:
    def __init__(self, page_cap=None):
        self.page_cap = page_cap      # simulate an API that stops paging early
        self.calls = 0

    def __call__(self, path, params=None):
        self.calls += 1
        params = dict(params or {})
        if "?" in path:
            params.update({k: v[0] for k, v in parse_qs(urlparse(path).query).items()})
            path = path.split("?")[0]
        page = int(params.get("page", 1))
        per = int(params.get("per_page", 30))
        if path.endswith("/commits/master"):
            return {"sha": HEAD}
        if "/compare/" in path:
            if "OpenSTA" in path:
                return {"total_commits": 0, "ahead_by": 0, "commits": []}
            lo = (page - 1) * per
            if self.page_cap and page > self.page_cap:
                lo = N
            items = [{"sha": sha(i), "parents": [{}] * (2 if i % MERGE_EVERY == 0 else 1)}
                     for i in range(lo, min(lo + per, N))]
            return {"total_commits": N, "ahead_by": N, "commits": items}
        if "/contents/src/sta" in path:
            return {"sha": "d" * 40}
        if "/commits/" in path:
            s = path.rsplit("/", 1)[1]
            nfiles = BIG.get(s, 2)
            lo = (page - 1) * per
            files = []
            for k in range(lo, min(lo + per, nfiles, uw.FILES_MAX)):
                name = "src/drt/BUILD" if k == 0 else f"src/odb/src/f{k}.cpp"
                patch = "@@ x @@\n+    copts = [\"-O2\"]," if k == 0 else "@@ x @@ void f() {\n+x"
                files.append({"filename": name, "patch": patch, "changes": 1})
            return {"commit": {"message": f"title {s[-4:]}\n\nbody"}, "files": files}
        if path.startswith("search/issues"):
            return {"items": [], "total_count": 0}
        raise AssertionError(f"unexpected call {path}")


class Pagination(unittest.TestCase):
    def setUp(self):
        self.warnings = []

    def test_compare_lists_every_commit(self):
        uw.api = FakeApi()
        commits, ahead, total = uw.compare_all(uw.OR_REPO, PIN, HEAD, self.warnings)
        self.assertEqual((len(commits), ahead, total), (N, N, N))
        self.assertEqual(len({c["sha"] for c in commits}), N)
        self.assertEqual(self.warnings, [])

    def test_short_listing_warns(self):
        uw.api = FakeApi(page_cap=2)          # 200 of 600
        commits, _, _ = uw.compare_all(uw.OR_REPO, PIN, HEAD, self.warnings)
        self.assertEqual(len(commits), 200)
        self.assertTrue(any("200 of 600" in w for w in self.warnings), self.warnings)

    def test_commit_files_paged(self):
        uw.api = FakeApi()
        d = uw.commit_detail(uw.OR_REPO, sha(7), self.warnings)
        self.assertEqual(len(d["files"]), 650)
        self.assertEqual(self.warnings, [])

    def test_file_cap_warns(self):
        uw.api = FakeApi()
        d = uw.commit_detail(uw.OR_REPO, sha(9), self.warnings)
        self.assertEqual(len(d["files"]), uw.FILES_MAX)
        self.assertTrue(any("capped" in w for w in self.warnings), self.warnings)

    def test_missing_patch_warns(self):
        def api(path, params=None):
            return {"commit": {"message": "t"}, "files": [{"filename": "x.cpp", "changes": 9000}]}
        uw.api = api
        uw.commit_detail(uw.OR_REPO, sha(1), self.warnings)
        self.assertTrue(any("no diff" in w for w in self.warnings), self.warnings)


class Digest(unittest.TestCase):
    def test_full_run(self):
        uw.api = FakeApi()
        with tempfile.TemporaryDirectory() as t:
            with open(os.path.join(t, "upstream.yaml"), "w") as fh:
                fh.write(f"commit: {PIN}\n")
            cwd, argv = os.getcwd(), sys.argv
            try:
                os.chdir(t)
                sys.argv = ["upstream-watch.py", "--out", "out", "--date", "2026-01-01"]
                uw.main()
            finally:
                os.chdir(cwd)
                sys.argv = argv
            with open(os.path.join(t, "out", "latest.md")) as fh:
                body = fh.read()
        non_merge = N - len(range(0, N, MERGE_EVERY))
        self.assertIn(f"{N} commits ahead ({N} listed, {non_merge} non-merge)", body)
        # sha(9) has 3000 files, so the cap warning must be in the digest
        self.assertIn("Coverage warning", body)
        self.assertIn("capped", body)
        # every non-merge commit touches src/drt/BUILD with copts: all are build configuration hits
        section = body.split("## Build configuration")[1].split("## Commits by module")[0]
        self.assertEqual(section.count("\n- `"), non_merge)

    def test_rate_limit_stop_warns(self):
        fake = FakeApi()
        details = {"n": 0}

        def api(path, params=None):
            if "/commits/" in path and not path.endswith("/master"):
                details["n"] += 1
                if details["n"] > 5:
                    raise uw.urllib.error.HTTPError(path, 403, "rate limit", {}, None)
            return fake(path, params)
        uw.api = api
        with tempfile.TemporaryDirectory() as t:
            with open(os.path.join(t, "upstream.yaml"), "w") as fh:
                fh.write(f"commit: {PIN}\n")
            cwd, argv = os.getcwd(), sys.argv
            try:
                os.chdir(t)
                sys.argv = ["upstream-watch.py", "--out", "out", "--date", "2026-01-01"]
                uw.main()
            finally:
                os.chdir(cwd)
                sys.argv = argv
            with open(os.path.join(t, "out", "latest.md")) as fh:
                body = fh.read()
        self.assertIn("commit details stopped at 5 of 450 (HTTP 403)", body)


if __name__ == "__main__":
    unittest.main()
