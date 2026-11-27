"""Registry market-transfer volume (excl. M&A and crude intra-group), monthly and by size band per half-year."""
import sqlite3
import sys
import pandas as pd

from common import load_org_lists, market_transfers


con = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
t = pd.read_sql("select * from transfers where transfer_date>='2023-01-01' and transfer_type='RESOURCE_TRANSFER'", con)
t = market_transfers(t, load_org_lists())
t["date"] = pd.to_datetime(t.transfer_date.str[:10])
t["m"] = t.date.dt.to_period("M")
mm = t[t.date >= "2025-04-01"].groupby("m").agg(records=("addresses", "size"), addrs_M=("addresses", lambda s: round(s.sum()/1e6, 2)),
     big=("prefix_len", lambda s: (s <= 16).sum()), mid=("prefix_len", lambda s: s.between(17, 19).sum()), s24=("prefix_len", lambda s: (s == 24).sum()))
print(mm.to_string())
t["half"] = t.date.dt.year.astype(str) + " H" + (1 + (t.date.dt.month > 6)).astype(str)
t["band"] = pd.cut(t.prefix_len, [0, 16, 19, 23, 24], labels=["/16 or larger", "/17 to /19", "/20 to /23", "/24"])
hb = t.groupby(["half", "band"], observed=True).size().unstack()
print("\n", hb.to_string())
hb.to_csv(sys.argv[2])
print("\nlatest per log:", t.groupby("log_rir").date.max().dt.date.to_dict())
