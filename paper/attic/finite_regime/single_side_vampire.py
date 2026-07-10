#!/usr/bin/env python3
import argparse, json, os, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl")
    ap.add_argument("--side", required=True, choices=["prove", "fmb"])
    ap.add_argument("--timeout", type=int, default=40)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.jsonl) if l.strip()]
    assert len(rows) == 1, "one pair at a time"
    r = rows[0]
    pid, eq1, eq2 = r["id"], r["equation1"], r["equation2"]

    with tempfile.TemporaryDirectory() as wd:
        if args.side == "prove":
            body = etp_terms.tptp_true(eq1, eq2)
            path = os.path.join(wd, f"{pid}_prove.p")
            open(path, "w").write(body)
            cmd = ["vampire", "--mode", "casc", "-t", f"{args.timeout}s", path]
        else:
            body = etp_terms.tptp_false(eq1, eq2)
            path = os.path.join(wd, f"{pid}_fmb.p")
            open(path, "w").write(body)
            cmd = ["vampire", "-sa", "fmb", "-t", f"{args.timeout}s", path]

        t0 = time.time()
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout + 4)
            out, err, rc = p.stdout, p.stderr, p.returncode
        except subprocess.TimeoutExpired:
            out, err, rc = "", "TIMEOUT", -9
        dt = round(time.time() - t0, 3)

        s = out + err
        if args.side == "prove":
            verdict = "true" if ("SZS status Theorem" in s or "SZS status Unsatisfiable" in s
                                  or "Refutation found" in s) else None
        else:
            verdict = "false" if ("SZS status Satisfiable" in s or "SZS status CounterSatisfiable" in s
                                   or "Exiting with 1 model" in s or "interpretation(" in s) else None

    with open(args.out, "w") as f:
        f.write(json.dumps(dict(id=pid, side=args.side, verdict=verdict, time=dt, rc=rc)) + "\n")
    print(f"{pid} {args.side} timeout={args.timeout}s -> verdict={verdict} time={dt}s")


if __name__ == "__main__":
    main()
