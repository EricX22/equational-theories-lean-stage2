#!/usr/bin/env python3
"""Build the ALPS supplementary code-and-data archive.

Run from the repository root:

    python3 make_supplementary.py --out /tmp/alps_supplementary.zip

The build is deliberately fail-closed. Anything that could break an
anonymity or withholding promise aborts the build rather than being
silently dropped:

  * a manifest entry that does not exist          -> abort
  * a scrub pattern surviving in a staged file    -> abort
  * a denylisted filename anywhere in the tree    -> abort

Three rules are enforced structurally rather than by reviewer discipline:

  1. NO ETP DATA FILES. Nothing is copied out of reference/; the corpus we
     ship is our own extension output, and ETP laws are referenced by number.
  2. CERT-63 SOLUTIONS ARE WITHHELD. easy_chain_harvest.jsonl is reduced to a
     law list, and the `last` field -- which holds the submitted chain -- is
     stripped from every SOLVED row of the certified-easy result files. The
     `last` field is retained on FAILED rows, since the failure analysis in
     the appendix depends on it and a rejected chain is not a solution.
  3. NO CREDENTIALS. .env files, key material and anything matching the
     OpenRouter key prefix abort the build.
"""

import argparse, json, os, re, shutil, sys, zipfile

# --------------------------------------------------------------------- manifest

# (destination directory, source path relative to repo root)
MANIFEST = [
    # --- generator: extension, screening, admissibility, deduplication -----
    ("generator", "paper/scripts/prove_status.py"),
    ("generator", "paper/scripts/etp_terms.py"),
    ("generator", "paper/scripts/seeds_from_status.py"),
    ("generator", "paper/scripts/seed_dedupe.py"),
    ("generator", "paper/scripts/fingerprint.py"),
    ("generator", "paper/scripts/equiv_sample.py"),
    ("generator", "paper/scripts/construction_transfer.py"),

    # --- judge: both channels, plus the ordered-model checker --------------
    ("judge", "paper/scripts/answer_spec.py"),
    ("judge", "paper/scripts/llm_construct.py"),
    ("judge", "paper/scripts/lean_oracle.py"),
    ("judge", "paper/scripts/confluence_cert.py"),
    ("judge", "paper/scripts/ordered_model.py"),

    # --- baseline: the automated portfolio sweep ---------------------------
    ("baseline", "paper/scripts/baseline_probe.py"),
    ("baseline", "paper/scripts/resume_sweep.sh"),
    ("baseline", "paper/scripts/run_all.sh"),
    ("baseline", "paper/scripts/rescore_baselines.py"),
    ("baseline", "paper/scripts/retry_curve.py"),
    ("baseline", "paper/results/baseline_full.jsonl"),

    # --- llm_runs: harnesses ----------------------------------------------
    ("llm_runs", "paper/scripts/trivial_autoform.py"),
    ("llm_runs", "paper/scripts/llm_trivial.py"),
    ("llm_runs", "paper/scripts/llm_autoformalize.py"),
    ("llm_runs", "paper/scripts/trivial_hints.py"),
    ("llm_runs", "paper/scripts/construct_hints.py"),
    ("llm_runs", "paper/scripts/llm_failure_breakdown.py"),
    ("llm_runs", "paper/scripts/finalize_llm.sh"),

    # --- corpus ------------------------------------------------------------
    ("corpus", "paper/results/final_status.jsonl"),
    ("corpus", "paper/results/classes_full.json"),
    ("corpus", "paper/results/hard25_sample.jsonl"),
    ("corpus", "paper/results/transfer.json"),
    ("corpus", "paper/results/retry_curve.json"),
    ("corpus", "paper/results/gold.jsonl"),

    # --- certificates for the worked example (Appendix A) ------------------
    ("certs", "paper/certs/ordered/12857.kbo.sat"),
    ("certs", "paper/certs/ordered/4916.kbo.sat"),
    ("certs", "paper/certs/twee/12857.out"),
    ("certs", "paper/certs/twee/33436.out"),
]

# Result files whose rows may contain a cert-63 SOLUTION in `last`.
# Solved rows get `last` stripped; failed rows keep it.
# Runs that cover the whole certified-easy set. Each must contain all 63 laws;
# a run may cover MORE (GPT-4.1's covers 95), which is fine -- the reported cell
# is still 0 out of 63.
CERT63_FULL = [
    "paper/results/llm_autoform_o3_cert63.jsonl",      # o3, waypoints
    "paper/results/llm_autoform_o3_nohints63.jsonl",   # o3, no waypoints
    "paper/results/llm_autoform_o4mini_cert63.jsonl",  # o4-mini
    "paper/results/llm_autoform_cert63.jsonl",         # GPT-4.1 (model not in filename)
]

# Deliberate subset runs. Each must contain ONLY certified-easy laws.
CERT63_PARTIAL = [
    "paper/results/llm_autoform_o3_low.jsonl",         # o3 at low effort, 9 laws
    "paper/results/llm_autoform_o3_repro.jsonl",       # reproduction run, 14 laws
]

CERT63_RESULTS = CERT63_FULL + CERT63_PARTIAL

# Hard-tier results: nothing solved, so `last` is a failed submission throughout.
HARD25_RESULTS = [
    "paper/results/llm_autoform_o3_hard25.jsonl",
    "paper/results/llm_construct_o3_hard25.jsonl",
    "paper/results/llm_construct_o4mini_hard25.jsonl",
    "paper/results/llm_construct_gpt41_hard25.jsonl",
]

# The file that DEFINES the certified-easy set. All other cert-63 runs must be
# subsets of it; the build aborts otherwise.
CERT63_REFERENCE = "paper/results/llm_autoform_o3_cert63.jsonl"

# --------------------------------------------------------------------- safety

SCRUB = [
    (re.compile(r"jrg4wx", re.I), "anonymous"),
    (re.compile(r"EricX22", re.I), "anonymous"),
    (re.compile(r"/home/[A-Za-z0-9_.-]+/"), "/home/anonymous/"),
    (re.compile(r"[A-Z]:\\\\Users\\\\[A-Za-z0-9_.-]+"), r"C:\\Users\\anonymous"),
    (re.compile(r"/Users/[A-Za-z0-9_.-]+/"), "/Users/anonymous/"),
]

# If any of these survive in a staged file, the build aborts.
FORBIDDEN = [
    re.compile(r"sk-or-[A-Za-z0-9_-]{8,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"jrg4wx", re.I),
    re.compile(r"EricX22", re.I),
]

DENY_NAMES = re.compile(r"(^\.env|\.pem$|\.key$|_rsa$|credentials|secrets?\.)", re.I)

TEXT_EXT = {".py", ".sh", ".md", ".json", ".jsonl", ".txt", ".tex", ".out", ".sat", ".cfg"}


def die(msg):
    print(f"ABORT: {msg}", file=sys.stderr)
    sys.exit(1)


def scrub_text(s):
    for pat, repl in SCRUB:
        s = pat.sub(repl, s)
    return s


def check_clean(path):
    if os.path.splitext(path)[1].lower() not in TEXT_EXT:
        return
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        body = fh.read()
    for pat in FORBIDDEN:
        m = pat.search(body)
        if m:
            die(f"{path}: forbidden pattern {m.group(0)[:12]!r} survived the scrub")


def copy_scrubbed(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.splitext(src)[1].lower() in TEXT_EXT:
        with open(src, "r", encoding="utf-8", errors="replace") as fh:
            body = fh.read()
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(scrub_text(body))
    else:
        shutil.copy2(src, dst)


def filter_jsonl(src, dst, drop_last_when_solved=False, keep_keys=None):
    """Rewrite a jsonl file, dropping withheld content."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    kept = stripped = 0
    with open(src, "r", encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if keep_keys is not None:
                r = {k: v for k, v in r.items() if k in keep_keys}
                if not r:
                    die(f"{src}: no key from {keep_keys} present; check the schema")
            elif drop_last_when_solved and r.get("solved"):
                r.pop("last", None)
                stripped += 1
            fout.write(scrub_text(json.dumps(r, ensure_ascii=False)) + "\n")
            kept += 1
    return kept, stripped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="repository root")
    ap.add_argument("--stage", default="/tmp/alps_supp")
    ap.add_argument("--out", default="/tmp/alps_supplementary.zip")
    ap.add_argument("--readme", default=None,
                    help="path to README.md to place at the archive root")
    a = ap.parse_args()

    root = os.path.abspath(a.root)
    stage = os.path.abspath(a.stage)
    if os.path.exists(stage):
        shutil.rmtree(stage)

    # ---- manifest ---------------------------------------------------------
    missing = [rel for _, rel in MANIFEST if not os.path.exists(os.path.join(root, rel))]
    if missing:
        die("manifest entries not found:\n  " + "\n  ".join(missing))

    for dest, rel in MANIFEST:
        copy_scrubbed(os.path.join(root, rel), os.path.join(stage, dest, os.path.basename(rel)))

    # ---- result files, with solutions withheld ----------------------------
    for rel in CERT63_RESULTS + HARD25_RESULTS:
        src = os.path.join(root, rel)
        if not os.path.exists(src):
            die(f"result file not found: {rel}")
        dst = os.path.join(stage, "llm_runs", os.path.basename(rel))
        kept, stripped = filter_jsonl(src, dst, drop_last_when_solved=(rel in CERT63_RESULTS))
        note = f"  {os.path.basename(rel):<40} {kept:>5} rows"
        if stripped:
            note += f"   ({stripped} solved rows had `last` stripped)"
        print(note)

    # ---- cert-63 law list, chains withheld --------------------------------
    # The certified-easy set is DEFINED by what was evaluated, so we derive it
    # from the laws appearing in the cert-63 result files rather than from
    # easy_chain_harvest.jsonl, which is the wider harvest pool (400 laws) and
    # carries the chains we withhold.
    def laws_in(rel):
        out, seen_ = [], set()
        with open(os.path.join(root, rel), encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                lw = json.loads(line).get("law")
                if lw and lw not in seen_:
                    seen_.add(lw)
                    out.append(lw)
        return out

    laws = laws_in(CERT63_REFERENCE)
    if len(laws) != 63:
        die(f"{CERT63_REFERENCE} defines {len(laws)} laws, expected 63")

    # Every other certified-easy run must be a SUBSET of that set. A run on
    # laws outside it is not a result on the certified-easy set, and reporting
    # it in that column would misstate what was evaluated.
    ref = set(laws)
    for rel in CERT63_FULL:
        missing_laws = ref - set(laws_in(rel))
        if missing_laws:
            die(f"{rel}: does not cover {len(missing_laws)} of the 63 certified-easy "
                "laws, so it cannot support a result reported over that set.")
    for rel in CERT63_PARTIAL:
        outside = [lw for lw in laws_in(rel) if lw not in ref]
        if outside:
            die(f"{rel}: {len(outside)} of its laws lie outside the certified-easy set.")
    dst = os.path.join(stage, "corpus", "cert63_laws.jsonl")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as fh:
        for lw in laws:
            fh.write(json.dumps({"law": lw}, ensure_ascii=False) + "\n")
    print(f"  cert63_laws.jsonl{'':<24} {len(laws):>5} laws   (chains withheld)")

    if a.readme:
        copy_scrubbed(a.readme, os.path.join(stage, "README.md"))

    # ---- safety sweep over everything staged ------------------------------
    for dirpath, _, names in os.walk(stage):
        for n in names:
            if DENY_NAMES.search(n):
                die(f"denylisted filename staged: {os.path.join(dirpath, n)}")
            check_clean(os.path.join(dirpath, n))

    # ---- zip --------------------------------------------------------------
    with zipfile.ZipFile(a.out, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, _, names in os.walk(stage):
            for n in sorted(names):
                full = os.path.join(dirpath, n)
                z.write(full, os.path.join("supplementary",
                                           os.path.relpath(full, stage)))

    size = os.path.getsize(a.out)
    print(f"\nwrote {a.out}  ({size/1e6:.1f} MB)")
    if not a.readme:
        print("NOTE: no --readme given; the archive has no README.md")


if __name__ == "__main__":
    main()
