"""Quarterly hyperscaler receipts (market transfers, excl. intra-group and M&A) from the NRO unified db, read-only."""
import sqlite3
import sys
import pandas as pd

from common import drop_non_sales, load_org_lists
LISTS = load_org_lists()
HYPER = tuple(LISTS["hyperscalers"])
FALSE_POS = tuple(LISTS["hyperscaler_false_positives"])
con = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
t = pd.read_sql("select * from transfers where transfer_date >= '2023-01-01'", con)
t = drop_non_sales(t, LISTS["non_sales"]).copy()
t["date"] = pd.to_datetime(t.transfer_date.str[:10])
def lo(col):
    return t[col].fillna("").str.lower()


t["to_l"], t["from_l"] = lo("to_org"), lo("from_org")


def hit(name):
    """First hyperscaler key found in an organisation name, or None."""
    if any(f in name for f in FALSE_POS):
        return None
    return next((h for h in HYPER if h in name), None)


t["hto"], t["hfrom"] = t.to_l.apply(hit), t.from_l.apply(hit)
print("latest per log:", t.groupby("log_rir").date.max().dt.date.to_dict())
mkt = t[t.transfer_type != "MERGER_ACQUISITION"]
h = mkt[mkt.hto.notna() & mkt.hfrom.isna()].copy()
h["q"] = h.date.dt.to_period("Q")
mkt = mkt.assign(q=mkt.date.dt.to_period("Q"))
allq = mkt.groupby("q").addresses.sum() / 1e6
out = pd.DataFrame({"hyper_M": h.groupby("q").addresses.sum() / 1e6, "hyper_n": h.groupby("q").size(),
                    "largest_pfx": h.groupby("q").prefix_len.min(), "all_market_M": allq}).fillna(0)
out["hyper_share_%"] = out.hyper_M / out.all_market_M * 100
print(out.round(3).to_string())
print("\nby buyer, 2026:\n", h[h.date >= "2026-01-01"].groupby("hto").addresses.sum().div(1e6).round(3).sort_values(ascending=False))
print("\nby buyer, 2025:\n", h[(h.date >= "2025-01-01") & (h.date < "2026-01-01")].groupby("hto").addresses.sum().div(1e6).round(3).sort_values(ascending=False))
out.round(4).to_csv(sys.argv[2])
