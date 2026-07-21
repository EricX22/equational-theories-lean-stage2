#!/usr/bin/env python3
"""Figure: renewability by order — Austin density rises, new-class density persists.

Data (frozen, NUMBERS_FINAL.md, 2026-07-18; order 5 excluded — ETP-curated, not ours):
  order 6:  29 Austin / 1,418 screened = 20.5 per 1k ; new classes 16.9 per 1k
  order 7: 117 Austin / 4,803 screened = 24.4 per 1k ; new classes 19.4 per 1k
  order 8: 105 Austin / 4,138 screened = 25.4 per 1k ; new classes 16.2 per 1k

Print-first design: two series encoded by lightness (dark ink vs light gray),
readable in grayscale and under any CVD; direct value labels; recessive axis.
Output sized for one AAAI column (3.3 in wide).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "DejaVu Serif"],
    "font.size": 8,
    "axes.linewidth": 0.6,
    "pdf.fonttype": 42,
})

orders = ["6", "7", "8"]
austin = [20.5, 24.4, 25.4]      # Austin laws per 1k screened
newcls = [16.9, 19.4, 16.2]      # new distinct classes per 1k screened

DARK, LIGHT = "#2b3440", "#c3c9d0"
INK, MUTED = "#1a1a1a", "#555555"

fig, ax = plt.subplots(figsize=(3.3, 1.85))
x = np.arange(len(orders))
w = 0.36
b1 = ax.bar(x - w/2 - 0.01, austin, w, color=DARK, label="Austin laws", zorder=3)
b2 = ax.bar(x + w/2 + 0.01, newcls, w, color=LIGHT, label="new classes", zorder=3)

for bars, col in ((b1, INK), (b2, MUTED)):
    for r in bars:
        ax.annotate(f"{r.get_height():.1f}", (r.get_x() + r.get_width()/2, r.get_height()),
                    xytext=(0, 1.5), textcoords="offset points",
                    ha="center", va="bottom", fontsize=7, color=col)

ax.set_xticks(x)
ax.set_xticklabels([f"order {o}" for o in orders])
ax.set_ylabel("per 1,000 laws screened", fontsize=8)
ax.set_ylim(0, 29.5)
ax.set_yticks([0, 10, 20])
ax.tick_params(axis="both", length=0, labelsize=8, colors=MUTED)
ax.grid(axis="y", color="#e3e5e8", linewidth=0.6, zorder=0)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#c9ccd1")

ax.legend(frameon=False, fontsize=7.5, loc="upper left", bbox_to_anchor=(0.0, 1.06),
          handlelength=1.1, handleheight=0.9, borderpad=0, ncol=2, columnspacing=1.2)

fig.tight_layout(pad=0.4)
fig.savefig("/tmp/alps/fig_density.pdf")
fig.savefig("/tmp/alps/fig_density.png", dpi=200)
print("written fig_density.pdf/.png")
