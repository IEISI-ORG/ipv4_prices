"""Figs 2-4 for the November 2026 update. Usage: figures.py prior_sales.csv hyper_quarterly.csv out_dir"""
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")
BLUE, ORANGE, AQUA = "#257de0", "#f47230", "#00b894"
INK, INK2, GRID = "#191919", "#666666", "#e6e6e6"
CUTOFF = "26 Nov 2026"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "text.color": INK, "axes.labelcolor": INK2,
    "axes.edgecolor": GRID, "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
    "axes.spines.right": False, "axes.spines.left": False, "axes.grid": True, "axes.grid.axis": "y",
    "grid.color": GRID, "grid.linewidth": 0.8, "lines.linewidth": 2, "figure.dpi": 100, "savefig.dpi": 200,
})

sales_path, hyper_path, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(sales_path)
df["date"] = pd.to_datetime(df["DATE"], format="%m/%d/%Y")
df["ppa"] = df["$/ADDRESS"].str.replace(r"[$,]", "", regex=True).astype(float)
df["usd"] = df["FINAL PRICE"].str.replace(r"[$,]", "", regex=True).astype(float)
df["pfx"] = df["BLOCK"].str.lstrip("/").astype(int)
df["half"] = df.date.dt.year.astype(str) + " H" + (1 + (df.date.dt.month > 6)).astype(str)


def finish(fig, name, title, sub, note):
    fig.text(0.01, 0.985, title, fontsize=15, fontweight="bold", va="top")
    fig.text(0.01, 0.935, sub, fontsize=11, color=INK2, va="top")
    fig.text(0.01, 0.01, note, fontsize=8.5, color=INK2, va="bottom")
    fig.savefig(out / name, facecolor="white")
    plt.close(fig)


# Fig 2: hyperscaler receipts per quarter
h = pd.read_csv(hyper_path)
h = h[h.q >= "2023Q1"]
fig, ax = plt.subplots(figsize=(10, 5.2))
fig.subplots_adjust(top=0.80, bottom=0.17, left=0.06, right=0.98)
x = range(len(h))
cols = [BLUE if q < "2026Q2" else ORANGE for q in h.q]
ax.bar(x, h.hyper_M, color=cols, width=0.8)
ax.set_xticks(list(x), [q.replace("Q", "\nQ") for q in h.q], fontsize=9)
ax.set_ylabel("Million addresses received")
for i, (q, v) in enumerate(zip(h.q, h.hyper_M)):
    if q >= "2026Q1":
        ax.text(i, v + 0.15, f"{v:.1f}M" if v >= 0.2 else f"{v:.2f}M", ha="center", va="bottom", fontsize=9)
i26 = list(h.q).index("2026Q1")
ax.annotate("One 9.2M-address deal,\n11 Feb 2026", (i26, 9.8), (i26 - 3.2, 10.6), fontsize=9, color=INK2,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.text(len(h) - 1, 1.4, "Oct to\nlate Nov", ha="center", fontsize=8.5, color=INK2)
ax.set_ylim(0, 12)
finish(fig, "fig2_hyperscaler_receipts.png", "Hyperscaler buying has mostly stopped",
       "IPv4 addresses received by the hyperscale cloud providers, per quarter. "
       "Orange: since April 2026",
       "Source: RIR transfer logs (ARIN, RIPE NCC, APNIC, LACNIC, AFRINIC) to 16-26 Nov 2026. Market transfers only; "
       "mergers and moves within one group excluded.\nBuyers matched on organisation name.")

# Fig 4: the size premium flipped
halves = [f"{y} H{k}" for y in range(2020, 2027) for k in (1, 2)]
med = df[df.pfx.isin([16, 24])].groupby(["half", "pfx"]).ppa.median().unstack().reindex(halves)
n16 = df[df.pfx == 16].groupby("half").size().reindex(halves).fillna(0).astype(int)
fig, ax = plt.subplots(figsize=(10, 5.2))
fig.subplots_adjust(top=0.80, bottom=0.17, left=0.06, right=0.90)
xi = list(range(len(halves)))
ax.plot(xi, med[24], color=ORANGE, marker="o", ms=6)
ax.plot(xi, med[16], color=BLUE, marker="o", ms=6)
ax.set_xticks(list(xi), [s.replace(" ", "\n") for s in halves], fontsize=9)
ax.set_ylabel("Median US$ per address")
last = len(halves) - 1
ax.text(last + 0.25, med[24].iloc[-1], f"/24  ${med[24].iloc[-1]:.2f}", color=INK, va="center", fontsize=10)
ax.text(last + 0.25, med[16].iloc[-1], f"/16  ${med[16].iloc[-1]:.2f}", color=INK, va="center", fontsize=10)
i23 = halves.index("2023 H1")
ax.annotate("2023 (6 sales): a /16 cost more\nper address than a /24", (i23, med[16].iloc[i23]), (i23 - 3.5, 58),
            fontsize=9, color=INK2, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.annotate("2026: half as much", (last, med[16].iloc[-1]), (last - 3.3, 6), fontsize=9, color=INK2,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.set_ylim(0, 62)
ax.set_xlim(-0.5, last + 1.6)
finish(fig, "fig4_size_premium.png", "Big blocks went from a premium to a discount",
       "Median sale price per address, /16 and /24 blocks, by half-year",
       f"Source: IPv4.Global prior sales to {CUTOFF}. /16 sales per half-year are few "
       f"({n16.min()}-{n16.max()}); no /16 sold in 2024 H1, so that point is missing. 2026 H2 is to 26 Nov.")

# Fig 3: flat prices, falling volume
m = df[(df.date >= "2025-04-01")].copy()
m["mon"] = m.date.dt.to_period("M")
months = pd.period_range("2025-04", "2026-11", freq="M")
big = m[m.pfx <= 19].groupby("mon").ppa.median().reindex(months)
small = m[m.pfx == 24].groupby("mon").ppa.median().reindex(months)
usd = m.groupby("mon").usd.sum().reindex(months).fillna(0) / 1e6
cnt = m.groupby("mon").size().reindex(months).fillna(0)
deal = m[(m.pfx == 14) & (m.date.dt.to_period("M") == pd.Period("2026-11"))].usd.sum() / 1e6
fig, axes = plt.subplots(3, 1, figsize=(10, 8.4), sharex=True, gridspec_kw=dict(height_ratios=[1.2, 1, 0.8]))
fig.subplots_adjust(top=0.88, bottom=0.09, left=0.08, right=0.88, hspace=0.32)
xi = list(range(len(months)))
a = axes[0]
a.plot(xi, small, color=ORANGE, marker="o", ms=4)
a.plot(xi, big, color=BLUE, marker="o", ms=4)
a.text(xi[-1] + 0.4, small.iloc[-1], "/24", va="center")
a.text(xi[-1] + 0.4, big.iloc[-1], "/14 to /19", va="center")
a.set_title("Median US$ per address", loc="left", fontsize=11, color=INK2)
a.set_ylim(0, 36)
a.axvspan(xi[list(months).index(pd.Period("2026-04"))] - 0.5, xi[-1] + 0.5, color="#f3f3f3", zorder=0)
a.text(xi[list(months).index(pd.Period("2026-04"))], 32, "Since April 2026: no longer falling", fontsize=9, color=INK2)
b = axes[1]
b.bar(xi, usd - [deal if p == pd.Period("2026-11") else 0 for p in months], color=BLUE, width=0.78)
b.bar(xi[-1], deal, bottom=usd.iloc[-1] - deal, color="#9fc3ef", width=0.78)
b.text(xi[-1] + 0.5, usd.iloc[-1] - deal / 2, f"one /14,\n${deal:.2f}M", va="center", fontsize=8.5, color=INK2)
b.set_title("Dollar volume, US$ million", loc="left", fontsize=11, color=INK2)
c = axes[2]
c.bar(xi, cnt, color=AQUA, width=0.78)
c.set_title("Number of sales", loc="left", fontsize=11, color=INK2)
c.set_ylim(0, 115)
c.set_xticks(xi, [p.strftime("%b\n%y") if p.month in (1, 4, 7, 10) else "" for p in months], fontsize=9)
finish(fig, "fig3_price_vs_volume.png", "Prices may be stable but volume is still falling",
       "Monthly, April 2025 to November 2026 (November to the 26th)",
       f"Source: IPv4.Global prior sales to {CUTOFF}.")
print("wrote", sorted(p.name for p in out.glob("*.png")))
