#!/usr/bin/env bash
# Best-effort installer for the ATP baselines (paper track).
# Vampire alone is a valid first baseline (covers prove via --mode casc AND
# finite-model via -sa fmb). E is a strong second prover. Prover9/Mace4 optional.
# run_baselines.py auto-skips whatever is missing, so partial installs are fine.
set -u
HERE="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$HERE/bin"; mkdir -p "$BIN"
echo "ATP bin dir: $BIN"
echo "  -> add to PATH for this shell:  export PATH=\"$BIN:\$PATH\""
echo

have(){ command -v "$1" >/dev/null 2>&1 && echo "  [ok] $1 -> $(command -v "$1")" || echo "  [--] $1 missing"; }
echo "current availability:"; for t in vampire eprover prover9 mace4; do have "$t"; done; echo

# --- Vampire: fetch latest release asset for linux ---
if ! command -v vampire >/dev/null 2>&1; then
  echo "fetching latest Vampire release asset (linux)..."
  url=$(curl -sL https://api.github.com/repos/vprover/vampire/releases/latest \
        | grep -oE '"browser_download_url": *"[^"]*"' | cut -d'"' -f4 \
        | grep -iE 'linux|static' | grep -ivE 'mac|win|arm|aarch' | head -1)
  if [ -n "${url:-}" ]; then
    echo "  $url"
    tmp="$BIN/.vampire_dl"
    if curl -fsSL "$url" -o "$tmp"; then
      case "$(file -b "$tmp" 2>/dev/null)" in
        *gzip*|*Zip*|*archive*) ( cd "$BIN" && tar xf "$tmp" 2>/dev/null || unzip -o "$tmp" >/dev/null 2>&1 )
                                 found=$(find "$BIN" -maxdepth 2 -type f -iname 'vampire*' ! -name '.vampire_dl' | head -1)
                                 [ -n "$found" ] && cp "$found" "$BIN/vampire" ;;
        *) cp "$tmp" "$BIN/vampire" ;;
      esac
      chmod +x "$BIN/vampire" 2>/dev/null
      "$BIN/vampire" --version >/dev/null 2>&1 && echo "  installed -> $BIN/vampire" \
        || echo "  downloaded but won't run; grab manually: https://github.com/vprover/vampire/releases"
      rm -f "$tmp"
    else
      echo "  download failed; install manually: https://github.com/vprover/vampire/releases"
    fi
  else
    echo "  couldn't auto-find a linux asset; install manually: https://github.com/vprover/vampire/releases"
  fi
fi

# --- E prover: try conda-forge ---
if ! command -v eprover >/dev/null 2>&1; then
  echo "installing E (eprover) via conda-forge (if conda present)..."
  conda install -y -c conda-forge eprover >/dev/null 2>&1 \
    && echo "  installed eprover" \
    || echo "  conda install failed; build/download from https://github.com/eprover/eprover"
fi

echo
echo "Prover9/Mace4 (LADR) are optional — Vampire's -sa fmb already covers model"
echo "finding. If wanted: https://www.cs.unm.edu/~mccune/prover9/"
echo
echo "re-check:"; for t in vampire eprover prover9 mace4; do have "$t"; done
