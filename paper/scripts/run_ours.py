#!/usr/bin/env python3
"""Run the FROZEN paper solver with ENABLE_LLM off and on.

The solved-set difference between the two runs is, by construction, the LLM's
marginal contribution (see solver.py header comment). The baseline is frozen as
a GIT REF (see paper/solver_frozen/README.md) -- materialized via `git show`,
not a file copy, because the Cowork sandbox truncates the large solver over the
mount. Each run patches the ENABLE_LLM constant in a throwaway copy, then drives
the existing harness:

    python -m pipeline.runner --submission <tmp> --problems <set> --output <json>

Requires the Lean judge / lake env the harness expects -- run in the real
environment. Use --dry-run to validate freeze + patch + command assembly without
invoking the judge.

Usage:
  python run_ours.py paper/problems/hard3.jsonl --runs both \
      --solver-ref ef84234 --out-dir paper/results [--dry-run]
"""
from __future__ import annotations
import argparse, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]            # .../equational-theories-lean-stage2
DEFAULT_REF = "ef84234"                       # pinned baseline (see solver_frozen/README.md)
DEFAULT_CONFIG = str(SCRIPT_DIR.parent / "config.paper.json")  # OpenRouter->o3; needs OPENROUTER_API_KEY
SOLVER_PATH_IN_REPO = "scripts/my_solver_merged/solver.py"
FLAG_RE = re.compile(r"^(ENABLE_LLM\s*=\s*)(True|False)", re.MULTILINE)


def materialize_baseline(ref: str) -> str:
    """Return the frozen solver source from the git object store (untruncated)."""
    try:
        src = subprocess.run(
            ["git", "show", f"{ref}:{SOLVER_PATH_IN_REPO}"],
            cwd=str(REPO_ROOT), capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"could not materialize {ref}:{SOLVER_PATH_IN_REPO}\n{e.stderr}")
    if not FLAG_RE.search(src):
        raise SystemExit("ENABLE_LLM assignment not found in frozen solver")
    # guard against the sandbox-truncation failure mode
    try:
        compile(src, "<frozen>", "exec")
    except SyntaxError as e:
        raise SystemExit(f"frozen solver does not compile (truncated ref?): {e}")
    return src


def load_solver_file(path: str) -> str:
    """Use a working-tree solver.py directly (fast iteration, pre-commit). Real
    env has no mount truncation, so reading the live file is safe here."""
    src = Path(path).read_text(encoding="utf-8")
    if not FLAG_RE.search(src):
        raise SystemExit(f"ENABLE_LLM assignment not found in {path}")
    try:
        compile(src, "<solver>", "exec")
    except SyntaxError as e:
        raise SystemExit(f"solver file does not compile: {e}")
    return src


def write_patched(src: str, dst_dir: Path, enable_llm: bool) -> str:
    patched = FLAG_RE.sub(lambda m: m.group(1) + ("True" if enable_llm else "False"),
                          src, count=1)
    (dst_dir / "solver.py").write_text(patched, encoding="utf-8")
    got = FLAG_RE.search(patched).group(2)
    assert got == ("True" if enable_llm else "False"), got
    return got


def run_mode(src: str, problems: str, enable_llm: bool, out_dir: Path,
             config: str | None, dry_run: bool, seed_from: Path | None = None) -> Path:
    tag = "llm" if enable_llm else "nollm"
    out_path = out_dir / f"ours_{tag}_{Path(problems).stem}.json"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Residual-only optimization: seed this run's output with an earlier run's
    # solved rows. The harness skips ids already marked solved (runner.py), so
    # only the residual is re-run. Sound because the solver runs its
    # deterministic stages BEFORE the LLM gate, so anything the no-LLM run
    # solved is solved identically here (used_llm=False) -- copying those rows
    # is equivalent to re-deriving them, at zero LLM cost.
    if seed_from and seed_from.exists() and not dry_run:
        shutil.copyfile(seed_from, out_path)
        print(f"[{tag}] seeded from {seed_from.name} -> o3 runs only on the residual")

    with tempfile.TemporaryDirectory() as tmp:
        sub = Path(tmp) / f"solver_{tag}"
        sub.mkdir()
        got = write_patched(src, sub, enable_llm)
        cmd = [sys.executable, "-m", "pipeline.runner",
               "--submission", str(sub),
               "--problems", str(problems),
               "--output", str(out_path)]
        if config:
            cmd += ["--config", config]
        print(f"[{tag}] ENABLE_LLM={got}  ->  {out_path}")
        print("      " + " ".join(cmd))
        if dry_run:
            print("      (dry-run: frozen solver materialized + compiles, flag patched; judge not invoked)")
            return out_path
        subprocess.run(cmd, cwd=str(REPO_ROOT), check=True)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("problems")
    ap.add_argument("--runs", choices=["both", "llm", "nollm"], default="both")
    ap.add_argument("--solver-ref", default=DEFAULT_REF,
                    help="git ref of the frozen baseline solver")
    ap.add_argument("--solver-file", default=None,
                    help="run this working-tree solver.py directly, skipping git "
                         "materialization (fast iteration before committing)")
    ap.add_argument("--out-dir", default=str(SCRIPT_DIR.parent / "results"))
    ap.add_argument("--config", default=DEFAULT_CONFIG,
                    help="defaults to paper/config.paper.json (OpenRouter->o3)")
    ap.add_argument("--seed-from", default=None,
                    help="for --runs llm: an existing no-LLM results json to seed "
                         "the run so o3 only touches the residual")
    ap.add_argument("--no-residual-seed", action="store_true",
                    help="in --runs both, do NOT seed the llm run from no-LLM "
                         "(run the full set through the llm path)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = materialize_baseline(args.solver_ref)
    print(f"frozen baseline: {args.solver_ref}  ({src.count(chr(10))+1} lines, compiles)")
    out_dir = Path(args.out_dir)

    if args.runs == "nollm":
        run_mode(src, args.problems, False, out_dir, args.config, args.dry_run)
    elif args.runs == "llm":
        seed = Path(args.seed_from) if args.seed_from else None
        run_mode(src, args.problems, True, out_dir, args.config, args.dry_run, seed_from=seed)
    else:  # both: no-LLM baseline first, then o3 only on its residual
        nollm_out = run_mode(src, args.problems, False, out_dir, args.config, args.dry_run)
        seed = None if args.no_residual_seed else nollm_out
        run_mode(src, args.problems, True, out_dir, args.config, args.dry_run, seed_from=seed)


if __name__ == "__main__":
    main()
