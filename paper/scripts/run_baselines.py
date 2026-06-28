#!/usr/bin/env python3
"""Run classical ATP baselines over ETP implication problems.

Two sides per problem:
  prove side  (eq1 |= eq2 ?)  -> Vampire (casc), E         -> verdict "true"
  model side  (counterexample) -> Vampire (fmb),  Mace4     -> verdict "false"
  Prover9 (prove) / Mace4 (model) share one LADR file.

Each tool, per problem, yields a verdict in {true, false, None(unknown)}. The
union of definitive verdicts across tools is the classical portfolio (VBS),
computed later by build_matrix.py. This script only records raw per-tool runs.

Binaries are looked up on PATH; any missing tool is skipped with a warning, so
the script is safe to run in a partial environment. Inputs are generated on the
fly via etp_terms (no dependency on the competition solver).

Usage:
  python run_baselines.py paper/problems/hard3.jsonl \
      --out paper/results/baselines_hard3.jsonl --timeout 60 \
      --tools vampire,eprover,prover9,mace4 [--limit 20]
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys, tempfile, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms  # noqa: E402


# --- per-tool adapters -----------------------------------------------------
# Each: bin, side ("prove"|"model"), fmt ("tptp"|"ladr"),
#       cmd(file, t) -> list[str], parse(out, err, rc) -> "true"|"false"|None
def _vampire_casc(f, t):   return ["vampire", "--mode", "casc", "-t", str(t), f]
def _vampire_fmb(f, t):    return ["vampire", "--mode", "fmb", "-t", str(t), f]
def _eprover(f, t):        return ["eprover", "--auto", "--tptp3-format", "-s",
                                   f"--soft-cpu-limit={t}", f]
def _prover9(f, t):        return ["prover9", "-t", str(t), "-f", f]
def _mace4(f, t):          return ["mace4", "-t", str(t), "-f", f]


def _parse_prove(out, err, rc):
    s = out + err
    if "SZS status Theorem" in s or "SZS status Unsatisfiable" in s \
       or "Refutation found" in s or "THEOREM PROVED" in s or "Proof found" in s:
        return "true"
    return None  # CounterSatisfiable / Satisfiable / GaveUp / Timeout -> unknown


def _parse_model(out, err, rc):
    s = out + err
    if "SZS status Satisfiable" in s or "SZS status CounterSatisfiable" in s \
       or "Exiting with 1 model" in s or "interpretation(" in s:
        return "false"
    return None


TOOLS = {
    "vampire":  dict(bin="vampire", side="prove", fmt="tptp", cmd=_vampire_casc, parse=_parse_prove),
    "vampire_fmb": dict(bin="vampire", side="model", fmt="tptp", cmd=_vampire_fmb, parse=_parse_model),
    "eprover":  dict(bin="eprover", side="prove", fmt="tptp", cmd=_eprover, parse=_parse_prove),
    "prover9":  dict(bin="prover9", side="prove", fmt="ladr", cmd=_prover9, parse=_parse_prove),
    "mace4":    dict(bin="mace4",   side="model", fmt="ladr", cmd=_mace4,   parse=_parse_model),
}
# user-facing --tools names map to one or more registry keys
ALIASES = {"vampire": ["vampire", "vampire_fmb"], "eprover": ["eprover"],
           "prover9": ["prover9"], "mace4": ["mace4"]}


def make_input(spec, eq1, eq2, workdir, pid):
    if spec["fmt"] == "tptp":
        body = etp_terms.tptp_true(eq1, eq2) if spec["side"] == "prove" \
            else etp_terms.tptp_false(eq1, eq2)
        ext = "p"
    else:
        body = etp_terms.ladr_input(eq1, eq2)
        ext = "in"
    path = os.path.join(workdir, f"{pid}_{spec['side']}.{ext}")
    with open(path, "w") as fh:
        fh.write(body)
    return path


def run_one(spec, path, timeout):
    cmd = spec["cmd"](path, timeout)
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout + 10)
        out, err, rc = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired:
        out, err, rc = "", "TIMEOUT", -9
    dt = round(time.time() - t0, 3)
    return spec["parse"](out, err, rc), dt, rc, " ".join(cmd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl")
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--tools", default="vampire,eprover,prover9,mace4")
    ap.add_argument("--limit", type=int, default=0, help="0 = all")
    args = ap.parse_args()

    keys = []
    for name in args.tools.split(","):
        keys += ALIASES.get(name.strip(), [name.strip()])
    # drop tools whose binary is absent
    active = []
    for k in keys:
        spec = TOOLS[k]
        if shutil.which(spec["bin"]):
            active.append(k)
        else:
            print(f"  WARN: {spec['bin']} not on PATH -> skipping {k}", file=sys.stderr)
    if not active:
        print("No ATP binaries available; nothing to run.", file=sys.stderr)
        # still create empty output so downstream join is well-defined
        open(args.out, "w").close()
        return

    rows = []
    with open(args.jsonl, encoding="utf-8") as fh:
        problems = [json.loads(l) for l in fh if l.strip()]
    if args.limit:
        problems = problems[: args.limit]

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with tempfile.TemporaryDirectory() as wd:
        for i, row in enumerate(problems, 1):
            pid, eq1, eq2 = row["id"], row["equation1"], row["equation2"]
            for k in active:
                spec = TOOLS[k]
                try:
                    path = make_input(spec, eq1, eq2, wd, f"{pid}_{k}")
                    verdict, dt, rc, cmd = run_one(spec, path, args.timeout)
                except Exception as e:  # noqa: BLE001
                    verdict, dt, rc, cmd = None, 0.0, None, f"ERROR:{e}"
                rows.append(dict(id=pid, tool=k, side=spec["side"],
                                 verdict=verdict, gold=row.get("answer"),
                                 time=dt, rc=rc, cmd=cmd))
            if i % 25 == 0:
                print(f"  ...{i}/{len(problems)}", file=sys.stderr)

    with open(args.out, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    solved = sum(1 for r in rows if r["verdict"])
    print(f"wrote {len(rows)} runs ({solved} definitive) -> {args.out}")


if __name__ == "__main__":
    main()
