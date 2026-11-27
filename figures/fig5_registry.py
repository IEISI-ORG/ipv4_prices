"""Fig 4 from registry transfer counts. Usage: fig4_registry.py registry_bands.csv out_dir

registry_bands.csv comes from registry_volume.py: half-year x size band counts of market transfers
(all RIR logs, M&A and crude intra-group moves excluded).
"""
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")
BLUE, ORANGE, AQUA, YELLOW = "#257de0", "#f47230", "#00b894", "#f2a600"
INK, INK2, GRID = "#191919", "#666666", "#e6e6e6"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "text.color": INK, "axes.labelcolor": INK2,
    "axes.edgecolor": GRID, "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
    "axes.spines.right": False, "axes.spines.left": False, "axes.grid": True, "axes.grid.axis": "y",
    "grid.color": GRID, "grid.linewidth": 0.8, "savefig.dpi": 200,
})

hb = pd.read_csv(sys.argv[1], index_col=0)
out = Path(sys.argv[2])
bands = [("/16 or larger", BLUE), ("/17 to /19", AQUA), ("/20 to /23", YELLOW), ("/24", ORANGE)]
fig, axes = plt.subplots(1, 4, figsize=(12.5, 4.8))
fig.subplots_adjust(top=0.74, bottom=0.2, left=0.05, right=0.99, wspace=0.32)
for ax, (label, c) in zip(axes, bands):
    n = hb[label]
    ax.bar(range(len(n)), n, color=[c] * (len(n) - 1) + ["#cccccc"], width=0.78)
    ax.set_xticks(range(len(n)), [s[2:4] + "\n" + s[-2:] for s in n.index], fontsize=8.5)
    ax.set_title(label, loc="left", fontsize=12, fontweight="bold")
    for i in (len(n) - 3, len(n) - 2, len(n) - 1):
        ax.text(i, n.iloc[i], f"{int(n.iloc[i]):,}", ha="center", va="bottom", fontsize=8.5)
    ax.set_ylim(0, n.max() * 1.18)
axes[0].set_ylabel("Transfers per half-year")
fig.text(0.01, 0.985, "The small end of the registry market is shrinking", fontsize=15, fontweight="bold", va="top")
fig.text(0.01, 0.925, "Market transfers recorded by the RIRs per half-year. Grey: 2026 H2 to late November "
         "(five months; December, usually the busiest month, is still to come)", fontsize=11, color=INK2, va="top")
fig.text(0.01, 0.01, "Source: ARIN, RIPE NCC, APNIC, LACNIC and AFRINIC transfer logs, within and between registries. "
         "Mergers, moves within one group and known non-sales excluded. Each panel has its own scale.\nOne deal can be several records.",
         fontsize=8.5, color=INK2, va="bottom")
fig.savefig(out / "fig5_registry_by_size.png", facecolor="white")
print("wrote fig5_registry_by_size.png")
