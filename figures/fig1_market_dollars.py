"""Fig 1: estimated monthly IPv4 market value vs the auction sample. Usage: fig1_market_dollars.py market_dollars.csv out_dir"""
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")
BLUE, ORANGE, INK, INK2, GRID = "#257de0", "#f47230", "#191919", "#666666", "#e6e6e6"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "text.color": INK, "axes.labelcolor": INK2,
    "axes.edgecolor": GRID, "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
    "axes.spines.right": False, "axes.spines.left": False, "axes.grid": True, "axes.grid.axis": "y",
    "grid.color": GRID, "grid.linewidth": 0.8, "savefig.dpi": 200,
})
d = pd.read_csv(sys.argv[1])
d = d[d.month >= "2024-11"].reset_index(drop=True)
out = Path(sys.argv[2])
x = range(len(d))
partial = d.month == "2026-11"
fig, ax = plt.subplots(figsize=(11, 5.6))
fig.subplots_adjust(top=0.79, bottom=0.17, left=0.07, right=0.98)
ax.bar(x, d.est_mid_M, width=0.8, color=[("#a9c9ef" if p else BLUE) for p in partial], zorder=2)
ax.errorbar(list(x), d.est_mid_M, yerr=[d.est_mid_M - d.est_low_M, d.est_high_M - d.est_mid_M],
            fmt="none", ecolor=INK2, elinewidth=1, capsize=2.5, zorder=3)
ax.bar(x, d.auction_M, width=0.38, color=ORANGE, zorder=4)
ax.set_xticks(list(x), [pd.Period(m).strftime("%b\n%y") if pd.Period(m).month in (2, 5, 8, 11) else "" for m in d.month], fontsize=9)
ax.set_ylabel("US$ million per month")
ax.set_ylim(0, 300)
i0 = list(d.month).index("2025-11")
ax.axvline(i0 - 0.5, color=INK2, lw=0.8, ls=(0, (3, 3)), zorder=1)
ax.text(i0 - 0.35, 290, "First article in this series,\nNov 2025", fontsize=9, color=INK2, va="top")
ifeb = list(d.month).index("2026-02")
ax.annotate("One 9.2M-address\nhyperscaler deal", (ifeb, d.est_high_M[ifeb] + 3), (ifeb - 0.2, 200), fontsize=9,
            color=INK2, ha="center", arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.text(len(d) - 1, d.est_high_M.iloc[-1] + 6, "to late\nNov", ha="center", fontsize=8.5, color=INK2)
ax.text(0.99, 0.97, "Blue: whole market (estimate, with range)\nOrange: sales on IPv4.Global",
        transform=ax.transAxes, ha="right", va="top", fontsize=9.5, color=INK)
fig.text(0.01, 0.985, "About $623 million of IPv4 addresses changed hands in the past year", fontsize=15,
         fontweight="bold", va="top")
fig.text(0.01, 0.93, "Estimated value of all market transfers per month, against the auction sample. "
         "November 2024 to October 2025: about $1.06 billion", fontsize=11, color=INK2, va="top")
fig.text(0.01, 0.01, "Estimate: RIR transfer logs (all five registries; mergers, group moves and known non-sales excluded) valued at "
         "IPv4.Global median price per address for each size band,\ntrailing three months. Range uses the 25th and 75th "
         "percentile prices only. Blocks larger than /16 take the /16-or-larger band price. Leases are not in the registry logs.",
         fontsize=8.5, color=INK2, va="bottom")
fig.savefig(out / "fig1_market_dollars.png", facecolor="white")
print("wrote fig1_market_dollars.png")
