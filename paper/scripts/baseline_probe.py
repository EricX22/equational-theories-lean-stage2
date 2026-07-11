#!/usr/bin/env python3
"""The baseline portfolio, and the budget curve. Run this on the cluster.

WHY THIS EXISTS
    Every label in the corpus is a theorem except one: hard-tier membership, which
    means "no prover we ran finished." That is a fact about our effort, not about the
    law. It becomes a defensible claim only when the portfolio is strong, named,
    versioned and published, and only when we can show the budget is past the knee.

    This script produces both numbers:

      (a) RESOLUTION MATRIX  law × config × budget -> {TRIVIAL, AUSTIN, -}
          The hard tier is the set unresolved at B_max under EVERY config.
      (b) BUDGET CURVE       resolution rate vs log(budget), corpus-level.
          If the rate is still climbing at B_max, the frontier is under-budgeted and
          every downstream number is wrong. This is the gate in PAPER_PLAN.md §5C.

    Note the asymmetry between the two directions, it is the whole reason the
    portfolio must contain a completion prover and not just a refuter:

      TRIVIAL  (L |= x=y)   proof search.      Vampire/E in proof mode.
      AUSTIN   (nontrivial model exists)  saturation. The clause set closes, and by
                                          JRS the saturated set IS the model.

    A law resolved in either direction leaves the hard tier. Both are theorems.

CONFIG AXES THAT ACTUALLY MATTER
    A law whose completion diverges under one term ordering may complete under
    another; this is not a hypothetical, it is the normal behaviour of Knuth-Bendix
    completion. So: prover × ordering × saturation algorithm × budget.

      vampire  -sa otter | discount        -to kbo | lpo
      eprover  --auto | --satauto          (E's own scheduling)
      twee     unfailing completion, purpose-built for the unit equational fragment
               and the single most likely component to move the number

    Twee is NOT interchangeable with the Twee use in PAPER_PLAN.md §5B. There it is a
    *verification* tool: it may reduce a saturated set to a convergent TRS that CeTA
    can certify. Here it is a *baseline* component: it resolves laws, shrinking the
    hard tier. Same binary, unrelated jobs, do not conflate them.

    Infinox is neither: it proves "no nontrivial finite model", which is the admission
    ticket (PAPER_PLAN.md §5A), not a resolution.

HONEST ACCOUNTING
    Report the portfolio version, the exact flags, the hardware and the wall-clock
    budget. `--emit-docker` prints the pinned image spec. A baseline nobody can rerun
    is not a baseline.

USAGE
    python3 paper/scripts/baseline_probe.py --selftest --vampire paper/bin/vampire
    python3 paper/scripts/baseline_probe.py \
        --in paper/results/final_status.jsonl --status NO_FINITE_MODEL \
        --vampire paper/bin/vampire --eprover $(which eprover) --twee $(which twee) \
        --budgets 30,60,120,300,600 --shard 0/32 \
        --out paper/results/baseline_v1.jsonl --certs paper/certs/baseline

    python3 paper/scripts/baseline_probe.py --curve paper/results/baseline_v1.jsonl
"""
from __future__ import annotations
import argparse, glob, json, os, subprocess, sys, tempfile, time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms as et                                          # noqa: E402
from prove_status import _lawax, _proved, _satisfiable          # noqa: E402

PORTFOLIO_VERSION = "v1.0-draft"

# (name, prover, direction, argv). direction: "triv" = prove L |= x=y,
#                                            "sat"  = saturate L + (u != v).
CONFIGS = [
    ("vampire/triv/casc",        "vampire", "triv", ["--mode", "casc"]),
    ("vampire/triv/casc+lpo",    "vampire", "triv", ["--mode", "casc", "-to", "lpo"]),
    ("vampire/triv/discount",    "vampire", "triv", ["-sa", "discount"]),
    ("vampire/sat/otter+kbo",    "vampire", "sat",  ["-sa", "otter", "--show_active", "on"]),
    ("vampire/sat/otter+lpo",    "vampire", "sat",  ["-sa", "otter", "--show_active", "on",
                                                     "-to", "lpo"]),
    ("eprover/triv/auto",        "eprover", "triv", ["--auto", "-s"]),
    ("eprover/sat/satauto",      "eprover", "sat",  ["--satauto", "-s",
                                                     "--print-saturated=eigEIG"]),
    ("twee/complete",            "twee",    "both", []),
]

DOCKER = """\
FROM ubuntu:22.04
# pin every prover; a baseline nobody can rerun is not a baseline
RUN apt-get update && apt-get install -y build-essential curl ghc cabal-install
# vampire 5.0.1  commit 1b13eaf
# eprover 3.x
# twee 2.x       cabal install twee
# infinox        (admission ticket, not a resolver)
# csi, ttt2, ceta  (verification channel, see PAPER_PLAN.md 5B)
"""


# ------------------------------------------------------------------ running ---
def _sh(argv, stdin_text, timeout):
    with tempfile.TemporaryDirectory() as wd:
        p = os.path.join(wd, "p.p")
        with open(p, "w") as fh:
            fh.write(stdin_text)
        t0 = time.time()
        try:
            r = subprocess.run(argv + [p], capture_output=True, text=True,
                               timeout=timeout + 10)
            return r.stdout + r.stderr, time.time() - t0
        except subprocess.TimeoutExpired:
            return "", time.time() - t0


def _body(law, direction):
    if direction == "triv":
        return et.tptp_true(law, "x = y")
    ax, _ = _lawax(et, law)
    return ax + "\nfof(nt,axiom,?[U,V]: U != V).\n"


import re as _re

# The SZS ontology is the standard every one of these provers emits. Matching prose is
# how the twee column silently read zero in the first place; Gate 2 in run_all.sh caught
# it. Parse the status line, and only fall back to prose when there is none.
_SZS = _re.compile(r"SZS status\s+(\w+)")

# What each status means for OUR two questions. `L |= x=y` is the conjecture in the
# triv/both encodings; the sat encoding has no conjecture, only `L ∧ sK0 != sK1`.
_SZS_TRIV = {"Theorem", "Unsatisfiable", "ContradictoryAxioms"}
_SZS_AUSTIN = {"CounterSatisfiable", "Satisfiable"}


def _verdict(prover, direction, out):
    """Map prover output to a THEOREM, never to a guess.

    DIRECTION IS LOAD-BEARING. A `triv` config encodes the conjecture `L |= x=y`; its
    only sound positive verdict is TRIVIAL. If it fails and the prover happens to
    saturate, that saturation came from a proving strategy (`--mode casc`) that may be
    INCOMPLETE, so its CounterSatisfiable is NOT a trustworthy AUSTIN — return "".
    AUSTIN may be claimed only by a `sat` config (a dedicated complete saturation) or
    by twee (complete by construction). Conflating the two is how the selftest's
    'austin not trivial' check failed: a proving run reported AUSTIN off an untrusted
    saturation."""
    incomplete = "incomplete strategy" in out
    m = _SZS.search(out)
    if m:
        st = m.group(1)
        if st in _SZS_TRIV:
            return "TRIVIAL"                      # L |= x=y proved; sound in any encoding
        if st in _SZS_AUSTIN:
            if direction == "triv":
                return ""                         # untrusted: proving-mode saturation
            return "" if incomplete else "AUSTIN"
        return ""                                # GaveUp, Timeout, ResourceOut, Error
    # No SZS line. Fall back only to prose we have SEEN (twee 2.6.1, law 4916, 2026-07-10).
    if prover == "twee":
        if "RESULT: CounterSatisfiable" in out or "conjecture is not true" in out:
            return "AUSTIN"                        # twee completion is complete
        if "RESULT: Unsatisfiable" in out or "RESULT: Theorem" in out:
            return "TRIVIAL"
        return ""
    if direction == "triv":
        return "TRIVIAL" if _proved(out) else ""
    return "AUSTIN" if _satisfiable(out) else ""


def run_config(law, cfg, bins, budget, certs=None):
    name, prover, direction, argv = cfg
    exe = bins.get(prover)
    if not exe:
        return None
    if prover == "vampire":
        out, secs = _sh([exe] + argv + ["-t", f"{budget}s"], _body(law, direction), budget)
    elif prover == "eprover":
        out, secs = _sh([exe] + argv + [f"--cpu-limit={budget}"],
                        _body(law, direction), budget)
    else:
        # `--tstp` (off by default) makes Twee emit the SZS ontology; without it the
        # only signal is the prose line `RESULT: CounterSatisfiable`. No other flags:
        # every twee flag in this file used to be invented, and `--quiet` /
        # `--max-cpu-time` do not exist. The wall clock is enforced by `_sh`.
        # Bonus: twee prints its final rewrite system, so the cert is a JRS-style model.
        out, secs = _sh([exe, "--tstp"], et.tptp_true(law, "x = y"), budget)
    v = _verdict(prover, direction, out)
    if v and certs:
        os.makedirs(certs, exist_ok=True)
        tag = f"{abs(hash(law)) % (10**12)}_{name.replace('/', '_')}"
        with open(os.path.join(certs, f"{tag}.out"), "w") as fh:
            fh.write(f"% law: {law}\n% config: {name} @ {budget}s\n\n{out}")
    return {"config": name, "budget": budget, "verdict": v, "secs": round(secs, 2)}


# -------------------------------------------------------------------- curve ---
def curve(path):
    """Corpus-level resolution rate vs budget. The knee is the whole point."""
    seen, res = defaultdict(set), defaultdict(set)
    for fn in glob.glob(path):
        for line in open(fn):
            r = json.loads(line)
            seen[r["budget"]].add(r["law"])
            if r["verdict"]:
                res[r["budget"]].add(r["law"])
    print(f"portfolio {PORTFOLIO_VERSION}\n")
    print(f"{'budget':>8}  {'laws':>6}  {'resolved':>8}  {'rate':>7}   delta")
    prev = None
    for b in sorted(seen):
        n, k = len(seen[b]), len(res[b])
        rate = k / n if n else 0
        d = "" if prev is None else f"{rate - prev:+.3f}"
        print(f"{b:>8}  {n:>6}  {k:>8}  {rate:>7.3f}   {d}")
        prev = rate
    print("\nIf the delta is not flattening, B_max is before the knee and the hard "
          "tier is under-budgeted, not method-bound. See PAPER_PLAN.md 5C.")


def selftest(bins):
    """Known answers. Nothing runs on the corpus until this prints SELFTEST OK."""
    ok = True
    AUSTIN = "x = y ◇ (x ◇ (x ◇ (y ◇ (z ◇ z))))"                       # 4916
    TRIV = "x = (((y ◇ (y ◇ (z ◇ z))) ◇ (x ◇ (x ◇ (z ◇ w)))) ◇ z)"     # from r2

    for law, cfgname, want in [(AUSTIN, "vampire/sat/otter+kbo", "AUSTIN"),
                               (TRIV,   "vampire/triv/casc",     "TRIVIAL")]:
        cfg = next(c for c in CONFIGS if c[0] == cfgname)
        r = run_config(law, cfg, bins, 20)
        got = r["verdict"] if r else "no-binary"
        ok &= (got == want)
        print(f"  {cfgname:24s} -> {got or '-':8s} want {want:8s} "
              f"{'OK' if got == want else 'FAIL'}  ({r['secs'] if r else 0}s)")

    # An Austin law must NOT be provable trivial. A false positive here would silently
    # relabel the whole corpus.
    cfg = next(c for c in CONFIGS if c[0] == "vampire/triv/casc")
    r = run_config(AUSTIN, cfg, bins, 10)
    got = r["verdict"] if r else "no-binary"
    ok &= (got == "")
    print(f"  {'austin not trivial':24s} -> {got or '-':8s} want {'-':8s} "
          f"{'OK' if got == '' else 'FAIL'}")

    missing = [p for p in ("eprover", "twee") if not bins.get(p)]
    if missing:
        print(f"  NOTE: {', '.join(missing)} absent — portfolio is INCOMPLETE, "
              f"any hard-tier claim from this run is provisional")
    print("SELFTEST OK" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp")
    ap.add_argument("--out")
    ap.add_argument("--certs")
    ap.add_argument("--status")
    ap.add_argument("--vampire")
    ap.add_argument("--eprover")
    ap.add_argument("--twee")
    ap.add_argument("--budgets", default="30,60,120,300,600")
    ap.add_argument("--n", type=int, default=0,
                    help="sample N laws (0 = all). THE CURVE IS A RATE: a few hundred "
                         "laws measure it as well as thousands, and the full sweep on "
                         "the hard tier costs ~5550 core-seconds PER LAW because "
                         "nothing resolves and every law walks the whole ladder.")
    ap.add_argument("--sample-seed", type=int, default=20260709)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--curve")
    ap.add_argument("--emit-docker", action="store_true")
    a = ap.parse_args()

    if a.emit_docker:
        print(DOCKER); return
    if a.curve:
        curve(a.curve); return

    bins = {"vampire": a.vampire, "eprover": a.eprover, "twee": a.twee}
    if a.selftest:
        sys.exit(selftest(bins))

    budgets = [int(b) for b in a.budgets.split(",")]
    i, n = (int(x) for x in a.shard.split("/"))

    laws = []
    for fn in glob.glob(a.inp):
        for line in open(fn):
            r = json.loads(line)
            if a.status and r.get("status") != a.status:
                continue
            laws.append(r["law"])
    laws = sorted(set(laws))
    if a.n and a.n < len(laws):
        import random
        random.Random(a.sample_seed).shuffle(laws)
        laws = sorted(laws[:a.n])
    mine = [lw for k, lw in enumerate(laws) if k % n == i]

    live = [c for c in CONFIGS if bins.get(c[1])]
    worst = len(mine) * len(live) * sum(budgets)
    print(f"{len(mine)} laws, budgets {budgets}, {len(live)} live configs", file=sys.stderr)
    print(f"WORST CASE for this shard: {worst} core-seconds = {worst/3600:.1f} core-hours "
          f"(nothing resolves => every law walks the whole ladder)", file=sys.stderr)

    # Append so the concurrent shards of ONE run share a file. There is NO resume: the
    # file is not read back, so a stale file from an earlier run would be silently mixed
    # in. run_all.sh truncates once before the fleet; a standalone caller must too.
    with open(a.out, "a") as fh:
        for lw in mine:
            for b in budgets:                    # ladder, early exit on resolution
                done = False
                for cfg in CONFIGS:
                    r = run_config(lw, cfg, bins, b, a.certs)
                    if r is None:
                        continue
                    r["law"] = lw
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                    fh.flush()
                    done |= bool(r["verdict"])
                if done:
                    break                        # resolved; higher budgets add nothing


if __name__ == "__main__":
    main()
