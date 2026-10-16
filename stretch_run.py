"""Stretch runs: the notebook's own code with ONE change, without touching results.json.

    python stretch_run.py --epochs 10 --out results_epochs10.json
    python stretch_run.py --extra data/extra_backed.csv --out results_plus50_backed.json

Same labels.csv, same seed-42 split and the same 36 test posts as the main run
(asserted against test_split.csv), so the numbers compare directly.
"""
import argparse
import json

import nbformat
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--epochs", type=int, help="override EPOCHS")
ap.add_argument("--extra", help="CSV of extra rows added to the TRAIN split only")
args = ap.parse_args()

# Code cells: 0 device, 1 repo, 2 settings, 3 load, 4 check, 5 split, 6 train, 7 evaluate.
cells = [c.source for c in nbformat.read("takemeter.ipynb", as_version=4).cells if c.cell_type == "code"]
ns = {}
for src in cells[:3]:
    exec(src, ns)
if args.epochs:
    ns["EPOCHS"] = args.epochs
for src in cells[3:6]:
    exec(src, ns)

assert set(ns["test_df"].text) == set(pd.read_csv("test_split.csv").text), "test split differs from the main run"
if args.extra:
    extra = pd.read_csv(args.extra)
    assert not set(extra.text) & set(ns["df"].text), "extra rows overlap labels.csv"
    ns["train_df"] = pd.concat([ns["train_df"], extra[["text", "label"]]], ignore_index=True)

exec(cells[6], ns)                                  # trains on ns["train_df"]
exec(cells[7].split("results = evaluate(")[0], ns)  # definitions only, so results.json is left alone

r = ns["evaluate"](ns["trainer"], ns["tokenizer"], ns["test_df"], ns["LABELS"], seed=ns["SEED"])
r.update(device=ns["DEVICE"], torch_version=ns["torch"].__version__, epochs=ns["EPOCHS"],
         n_train=len(ns["train_df"]), extra=args.extra)
with open(args.out, "w") as f:
    json.dump(r, f, indent=2)

print(f"\naccuracy {r['accuracy']:.3f}   macro F1 {r['f1_macro']:.3f}   -> {args.out}")
for label, s in r["per_label"].items():
    print(f"  {label:<10} F1 {s['f1']:.3f}  P {s['precision']:.3f}  R {s['recall']:.3f}  (n={s['support']})")
c = r["confidence"]
print(f"confidence: most-sure third {c['accuracy_most_confident_third']:.3f}, least-sure {c['accuracy_least_confident_third']:.3f}")
