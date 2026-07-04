#!/usr/bin/env python3
"""Thin, principled Lean-oracle verifier for counter-model certificates.

For the paper we verify certificates with *plain Lean* rather than the
competition judge, but we keep exactly the soundness guarantees that make
"Lean-verified" meaningful -- and drop the competition-specific artifacts
(the explicit-table `decideFin` convention, the one-level used-constants
allowlist that forced the `submission.impl` alias hack, the fixed 120s cap).

A certificate PASSES iff:
  1. Source contains no banned constructs: `native_decide` (trusts compiled
     code / bypasses the kernel), `sorry`, `admit`, or a user-declared `axiom`.
  2. `lake env lean <cert>` compiles with no errors (exit 0, no "error:").
  3. No `sorry` warning is emitted.
  4. Every theorem's `#print axioms` footprint is a subset of ALLOWED_AXIOMS
     and never includes `sorryAx` or `Lean.ofReduceBool` (the native_decide
     axiom). The cert file should end with `#print axioms <thm>` lines.

Usage:
  python paper/scripts/lean_oracle.py paper/certs/Order5v2_1593.lean
  python paper/scripts/lean_oracle.py --lake-dir . --timeout 600 <cert.lean>

Run from the Lean project root (so `lake env` resolves Mathlib).
Exit code 0 = PASS, 1 = FAIL.
"""
from __future__ import annotations
import argparse
import os
import re
import subprocess
import sys
import time

ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}

# Tokens that must never appear in a sound certificate's source.
BANNED_SOURCE = {
    "native_decide": "trusts compiled code, bypasses the kernel",
    "sorry": "incomplete proof",
    "admit": "incomplete proof",
}
# A user-declared axiom (`axiom foo : ...`) at the start of a line.
AXIOM_DECL_RE = re.compile(r"^\s*axiom\s", re.MULTILINE)
# The native_decide axiom, should it slip through into an axiom footprint.
FORBIDDEN_AXIOMS = {"sorryAx", "Lean.ofReduceBool", "Lean.trustCompiler"}


def strip_comments(src: str) -> str:
    """Remove -- line comments and /- -/ block comments (non-nested-safe enough
    for our certs) so token scans don't trip on documentation."""
    src = re.sub(r"/-.*?-/", " ", src, flags=re.DOTALL)
    src = re.sub(r"--[^\n]*", " ", src)
    return src


def scan_source(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    code = strip_comments(raw)
    problems = []
    for tok, why in BANNED_SOURCE.items():
        if re.search(r"\b" + re.escape(tok) + r"\b", code):
            problems.append(f"banned construct `{tok}` in source ({why})")
    if AXIOM_DECL_RE.search(code):
        problems.append("user-declared `axiom` in source (unproven assumption)")
    return problems


# `#print axioms` output forms:
#   'X' depends on axioms: [propext, Classical.choice, Quot.sound]
#   'X' does not depend on any axioms
AXIOM_LINE_RE = re.compile(
    r"'([^']+)' depends on axioms: \[([^\]]*)\]"
)
NOAXIOM_LINE_RE = re.compile(r"'([^']+)' does not depend on any axioms")


def parse_axioms(stdout: str) -> dict[str, set[str]]:
    """Map theorem name -> set of axioms it depends on."""
    found: dict[str, set[str]] = {}
    for m in AXIOM_LINE_RE.finditer(stdout):
        name = m.group(1)
        axset = {a.strip() for a in m.group(2).split(",") if a.strip()}
        found[name] = axset
    for m in NOAXIOM_LINE_RE.finditer(stdout):
        found.setdefault(m.group(1), set())
    return found


def check_axioms(found: dict[str, set[str]]) -> list[str]:
    problems = []
    if not found:
        problems.append(
            "no `#print axioms` output found -- add `#print axioms <thm>` "
            "lines to the certificate so its axiom footprint is auditable"
        )
    for name, axset in found.items():
        forbidden = axset & FORBIDDEN_AXIOMS
        if forbidden:
            problems.append(f"{name}: forbidden axiom(s) {sorted(forbidden)}")
        extra = axset - ALLOWED_AXIOMS
        if extra:
            problems.append(
                f"{name}: axiom(s) outside allowlist {sorted(extra)} "
                f"(allowed: {sorted(ALLOWED_AXIOMS)})"
            )
    return problems


def run_lean(cert: str, lake_dir: str, timeout: int):
    t0 = time.time()
    try:
        proc = subprocess.run(
            ["lake", "env", "lean", os.path.abspath(cert)],
            cwd=lake_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None, "", "", time.time() - t0
    return proc.returncode, proc.stdout, proc.stderr, time.time() - t0


def verify(cert: str, lake_dir: str, timeout: int) -> bool:
    print(f"== Lean-oracle verify: {cert} ==")

    src_problems = scan_source(cert)
    if src_problems:
        for p in src_problems:
            print(f"  FAIL(source): {p}")
        return False
    print("  source scan: OK (no native_decide / sorry / admit / axiom)")

    rc, out, err, secs = run_lean(cert, lake_dir, timeout)
    if rc is None:
        print(f"  FAIL(compile): timed out after {timeout}s")
        return False
    combined = out + "\n" + err
    if rc != 0 or re.search(r"^.*error:", combined, re.MULTILINE):
        print(f"  FAIL(compile): lean returned {rc} with errors ({secs:.1f}s)")
        for line in combined.splitlines():
            if "error:" in line:
                print("    " + line.strip())
        return False
    if re.search(r"declaration uses 'sorry'", combined):
        print("  FAIL(compile): a declaration uses 'sorry'")
        return False
    print(f"  compile: OK ({secs:.1f}s)")

    found = parse_axioms(combined)
    ax_problems = check_axioms(found)
    for name, axset in sorted(found.items()):
        shown = sorted(axset) if axset else "(none)"
        print(f"  axioms[{name}]: {shown}")
    if ax_problems:
        for p in ax_problems:
            print(f"  FAIL(axioms): {p}")
        return False
    print("  axiom footprint: OK (within allowlist, no sorryAx/native_decide)")
    print(f"== PASS ({secs:.1f}s) ==")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cert", help="path to the .lean certificate")
    ap.add_argument("--lake-dir", default=".", help="Lean project root (has lakefile)")
    ap.add_argument("--timeout", type=int, default=600, help="compile timeout (s)")
    args = ap.parse_args()
    ok = verify(args.cert, args.lake_dir, args.timeout)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
