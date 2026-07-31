#!/usr/bin/env bash
# package_supplementary.sh — assemble the AAAI-27 supplementary zip on the
# cluster. Run from the repo root:
#   bash paper/scripts/package_supplementary.sh
# Output: paper/supplementary.zip  (+ a manifest and scrub report on stdout)
#
# Assembles a FRESH staging dir (never zips the working tree, so no .git and
# no stray files), copies known artifacts, generates the released law list,
# runs the anonymization scrub, and refuses to zip if the scrub finds hits.
set -u
cd "$(dirname "$0")/../.." || exit 1
RES=paper/results
STAGE=paper/supplementary
ZIP=paper/supplementary.zip
rm -rf "$STAGE" "$ZIP"
mkdir -p "$STAGE"/{corpus,generator,judge,baseline,llm_runs}

missing=()
copy() {  # copy <src> <destdir> [required]
    src=$1; dst=$2; req=${3:-opt}
    if [ -e "$src" ]; then cp -r "$src" "$STAGE/$dst/"; echo "  + $src -> $dst/"
    else
        echo "  ! MISSING ($req): $src"
        [ "$req" = req ] && missing+=("$src")
    fi
}

echo "== README + appendix"
copy paper/supplementary_README.md . req
mv "$STAGE/supplementary_README.md" "$STAGE/README.md" 2>/dev/null
copy paper/latex/appendix.pdf . req   # compile appendix.tex first if missing

echo "== corpus/"
# Released law sets. Adjust names here if the cluster files differ.
for f in paper/results/admissible_pool*.jsonl paper/results/*class*map*.jsonl \
         paper/results/hard25_sample.jsonl paper/results/hard_tier*.jsonl; do
    [ -e "$f" ] && copy "$f" corpus
done
copy paper/results/hard25_sample.jsonl corpus req
# cert-63 LAW LIST (solutions withheld): derive from run A of the o3 cert file.
python3 - <<'PY'
import json
laws, seen = [], set()
for line in open("paper/results/llm_autoform_o3_cert63.jsonl", encoding="utf-8"):
    line = line.strip()
    if not line: continue
    law = json.loads(line)["law"]
    if law not in seen:
        seen.add(law); laws.append(law)
    if len(laws) == 63: break
assert len(laws) == 63
with open("paper/supplementary/corpus/cert63_laws.jsonl", "w", encoding="utf-8") as f:
    for law in laws:
        f.write(json.dumps({"law": law}, ensure_ascii=False) + "\n")
print("  + generated corpus/cert63_laws.jsonl (63 laws, chains withheld)")
PY
# Worked-example certificates for 12857/33436, if present:
mkdir -p "$STAGE/corpus/certs"
for f in paper/results/*12857* paper/results/*33436* paper/certs/*; do
    [ -e "$f" ] && cp -r "$f" "$STAGE/corpus/certs/" && echo "  + $f -> corpus/certs/"
done

echo "== generator/"
copy paper/scripts/prove_status.py generator req
for f in paper/scripts/*extend* paper/scripts/*screen* paper/scripts/*filter*; do
    [ -e "$f" ] && copy "$f" generator
done

echo "== judge/"
copy paper/scripts/answer_spec.py judge req
copy paper/scripts/llm_construct.py judge req
copy paper/scripts/ordered_model.py judge req
copy paper/bin/vampire judge req
# BSD 3-clause notice must accompany the binary:
for f in paper/bin/VAMPIRE_LICENCE paper/bin/LICENCE* paper/bin/LICENSE*; do
    [ -e "$f" ] && copy "$f" judge && lic=1
done
[ -n "${lic:-}" ] || { echo "  ! MISSING (req): Vampire licence file next to binary"; missing+=("VAMPIRE_LICENCE"); }

echo "== baseline/"
copy paper/scripts/baseline_probe.py baseline req
copy paper/scripts/run_remaining.sh baseline
copy paper/scripts/resume_sweep.sh baseline
copy paper/results/baseline_full_final.jsonl baseline req

echo "== llm_runs/"
copy paper/scripts/trivial_autoform.py llm_runs req
copy paper/scripts/llm_trivial.py llm_runs
copy paper/scripts/trivial_hints.py llm_runs req
copy paper/scripts/finalize_llm.sh llm_runs
copy paper/scripts/gpt41_fill63.sh llm_runs
for f in llm_autoform_o3_cert63 llm_autoform_o3_nohints63 llm_autoform_o3_repro \
         llm_autoform_o3_hard25 llm_autoform_o4mini_cert63 \
         llm_autoform_gpt41_nohints63 llm_autoform_gpt41_cert63 llm_autoform_gpt41 \
         llm_construct_o3_hard25 llm_construct_o4mini_hard25 llm_construct_gpt41_hard25 \
         cert63_input hard25_trivial_input; do
    copy "$RES/$f.jsonl" llm_runs req
done
# NEVER shipped: reference solutions + anything derived from them with chains.
for banned in easy_chain_harvest.jsonl o3_repro_set.jsonl; do
    if [ -e "$STAGE/llm_runs/$banned" ] || [ -e "$STAGE/corpus/$banned" ]; then
        echo "  ! FATAL: withheld file staged: $banned"; exit 1
    fi
done

echo "== scrub pass"
# 1) hard failures: usernames, home paths, API keys, repo URLs, git dirs
hits=$(grep -rIl "jrg4wx\|EricX22\|sk-or-\|api_key\s*=\s*['\"]\|/u/\|/home/" "$STAGE" 2>/dev/null)
find "$STAGE" -name ".git" -o -name "*.nohup" -o -name ".done*" | while read -r f; do
    echo "  ! removing: $f"; rm -rf "$f"
done
if [ -n "$hits" ]; then
    echo "  ! SCRUB HITS — fix these files, then rerun:"
    echo "$hits" | sed 's/^/      /'
    for f in $hits; do grep -hn "jrg4wx\|EricX22\|sk-or-\|/u/\|/home/" "$f" | head -3 | sed 's/^/        /'; done
    exit 1
fi
# 2) confirm no reference chains leaked into corpus files
if grep -l '"chain"' "$STAGE"/corpus/* 2>/dev/null; then
    echo "  ! FATAL: a corpus file contains chain data"; exit 1
fi
echo "  scrub clean"

echo "== manifest + zip"
[ ${#missing[@]} -gt 0 ] && { printf '  ! REQUIRED FILES MISSING:\n'; printf '      %s\n' "${missing[@]}"; \
    echo "  fix paths at the top of this script or place the files, then rerun"; exit 1; }
( cd paper && find supplementary -type f | sort | sed 's/^/  /' )
( cd paper && zip -qr supplementary.zip supplementary )
sz=$(du -m "$ZIP" | cut -f1)
echo "== DONE: $ZIP (${sz} MB)"
[ "$sz" -gt 50 ] && echo "== WARNING: over 50 MB — check the AAAI-27 supplementary size limit before uploading"
echo "== remember: upload appendix.pdf separately too if the form has a distinct slot"
