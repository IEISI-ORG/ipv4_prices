"""Estimate monthly IPv4 market dollar volume: registry transfers valued at auction-sample prices.

Usage: market_dollars.py prior_sales.csv nro-unified.db out.csv

Registry side: market transfers (RESOURCE_TRANSFER only; M&A and HISTORICAL excluded; crude intra-group
filter drops transfers whose sender and recipient share a first word; known non-sales from org_lists.json). Price side: IPv4.Global sales,
trailing 3-month 25th/50th/75th percentile $/address per size band. Blocks larger than /16 take the
"/16 or larger" band price; blocks smaller than /24 take the /24 price.
"""
import sqlite3
import sys

import numpy as np
import pandas as pd

from common import load_org_lists, market_transfers

QUANTILES = np.array([0.25, 0.5, 0.75])
BANDS = [(0, 16, "/16 or larger"), (17, 19, "/17-/19"), (20, 21, "/20-/21"), (22, 23, "/22-/23"), (24, 32, "/24")]




def band(p: int) -> str:
    return next(name for lo, hi, name in BANDS if lo <= p <= hi)


sales = pd.read_csv(sys.argv[1])
sales["date"] = pd.to_datetime(sales["DATE"], format="%m/%d/%Y")
sales["ppa"] = sales["$/ADDRESS"].str.replace(r"[$,]", "", regex=True).astype(float)
sales["usd"] = sales["FINAL PRICE"].str.replace(r"[$,]", "", regex=True).astype(float)
sales["band"] = sales["BLOCK"].str.lstrip("/").astype(int).map(band)
sales["m"] = sales.date.dt.to_period("M")

con = sqlite3.connect(f"file:{sys.argv[2]}?mode=ro", uri=True)
t = pd.read_sql("select transfer_date, prefix_len, addresses, from_org, to_org, transfer_type from transfers "
                "where transfer_date >= '2024-01-01' and transfer_type = 'RESOURCE_TRANSFER'", con)
t = market_transfers(t, load_org_lists())
t["m"] = pd.to_datetime(t.transfer_date.str[:10]).dt.to_period("M")
t = t[t.addresses.fillna(0) > 0]
t["band"] = (32 - np.log2(t.addresses)).round().clip(0, 32).astype(int).map(band)  # effective prefix from size

months = pd.period_range("2024-03", "2026-11", freq="M")
rows = []
for m in months:
    window = sales[(sales.m > m - 3) & (sales.m <= m)]
    q = window.groupby("band").ppa.quantile(QUANTILES).unstack()
    wide = sales[(sales.m > m - 12) & (sales.m <= m)].groupby("band").ppa.quantile(QUANTILES).unstack()
    q = q.reindex(wide.index).fillna(wide)  # bands with no sales in 3 months fall back to 12 months
    reg = t[t.m == m].groupby("band").addresses.sum()
    est = {k: float((reg * q[k].reindex(reg.index)).sum()) for k in (0.25, 0.5, 0.75)}
    missing = reg[q[0.5].reindex(reg.index).isna()].sum()
    rows.append({"month": str(m), "registry_addrs_M": reg.sum() / 1e6, "est_low_M": est[0.25] / 1e6,
                 "est_mid_M": est[0.5] / 1e6, "est_high_M": est[0.75] / 1e6,
                 "auction_M": sales[sales.m == m].usd.sum() / 1e6, "unpriced_addrs": int(missing)})
out = pd.DataFrame(rows)
out["auction_share_%"] = 100 * out.auction_M / out.est_mid_M
out.round(2).to_csv(sys.argv[3], index=False)
pd.set_option("display.width", 160)
print(out[out.month >= "2025-11"].round(2).to_string(index=False))
q = out.assign(q=pd.PeriodIndex(out.month, freq="M").asfreq("Q")).groupby("q")[["registry_addrs_M", "est_low_M", "est_mid_M", "est_high_M", "auction_M"]].sum()
print("\nby quarter\n", q.round(1).to_string())
