# Figures for the November 2026 update

The five figures in [*The IPv4 Market Update*](https://medium.com/@terrysweetser_90287/the-ipv4-market-update-0149c6167f4b) (November 2026). Run from the repository root with `uv run python`.

| Figure | What it shows | Script | Input |
|---|---|---|---|
| 1 | Estimated monthly value of all market transfers, against auction sales | `fig1_market_dollars.py` | `data/market_dollars.csv` |
| 2 | Addresses received by hyperscalers per quarter | `figures.py` | `prior_sales.csv`, `data/hyper_quarterly.csv` |
| 3 | Monthly price, dollar volume and number of sales in the auction sample | `figures.py` | `prior_sales.csv` |
| 4 | Median price per address, /16 against /24 | `figures.py` | `prior_sales.csv` |
| 5 | Registry transfers per half-year by block size | `fig5_registry.py` | `data/registry_bands.csv` |

Redraw all five into `outputs/` (gitignored):

```bash
mkdir -p outputs
uv run python figures/figures.py prior_sales.csv figures/data/hyper_quarterly.csv outputs
uv run python figures/fig1_market_dollars.py figures/data/market_dollars.csv outputs
uv run python figures/fig5_registry.py figures/data/registry_bands.csv outputs
```

`prior_sales.csv` is the IPv4.Global export described in the main README.

## The data files

The three CSVs in `data/` are aggregates of the RIR transfer logs: monthly or quarterly totals and counts by block size, with no prefixes and no organisation names.

- `market_dollars.csv`: each month's market transfers valued at the auction sample's trailing three-month median price per address for their size band. The low and high columns use the 25th and 75th percentile prices.
- `hyper_quarterly.csv`: addresses received by hyperscalers per quarter, against all market transfers.
- `registry_bands.csv`: market transfers per half-year by block-size band.

## Rebuilding the data files

`market_dollars.py`, `hyper_quarterly.py` and `registry_volume.py` rebuild the CSVs from a SQLite table of all five RIRs' transfer logs (`transfers`, one row per transfer, within and between registries). That table is not published here. They also need `org_lists.json`, which lists the hyperscaler names to match and the transfers to exclude as not being sales. That file is kept out of the repository; `org_lists.example.json` shows its format.

"Market transfers" means registry resource transfers, excluding mergers and acquisitions, moves where sender and recipient share a first word, and the listed non-sales. Leases do not appear in the logs, and a dealer's stock is counted when it arrives and again when it is sold on.
