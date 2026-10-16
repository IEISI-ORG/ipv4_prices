# IPv4 Price Trends

Analysis of the secondary market for IPv4 addresses, using public auction data to track the
post-2022 price collapse and project when each subnet size effectively reaches zero.

The thesis: an IPv4 address was never an asset. Its price is the **deferral cost of IPv6
migration**, a "laziness tax" that falls as IPv6 gets cheaper to deploy. The data shows a
structural decline, not a cyclical dip.

## The analysis

[`ipv4_prices.ipynb`](ipv4_prices.ipynb) runs locally or in Google Colab. It has two parts.

**Published series (sections 1–4).** These are the charts and tables used in the articles below,
kept as published so each update is comparable with the last:

1. Monthly average price, the early-2022 peak, and the steepest monthly drops.
2. Linear regression per subnet size, projected to $0.
3. Third-degree polynomial per subnet size, projected to $0.
4. Exponential decay per subnet size, projected to $1.

**December 2026 additions (sections 5–12).** New, additive diagnostics:

5. Monte Carlo (geometric Brownian motion on monthly medians, seeded) with time-to-$1 distributions.
6. Vintage comparison: the linear and cubic $0 dates recomputed on the data as it stood at each article date.
7. Mix-shift test: simple mean vs median vs address-weighted price, per-size medians, and a decomposition
   of any monthly change into within-size repricing and block-mix effects.
8. Sell-side pressure: addresses sold vs transaction count, dollar volume, mean block size.
9. Concentration in /23–/24 blocks, a trailing volatility band, and large-block liquidity.
10. Scorecard for the five competing readings of the June 2026 uptick.
11. Predictions ledger: each dated claim from the articles beside its current reading.
12. Reproduction check against the June 2026 tables (runs when `AS_OF = '2026-06-19'`).

Section 3b bootstraps the linear and cubic fits to show how stable each model's $0 date is.

On the 2022 peak: the **monthly average** peaked at $52.19 in February 2022. Individual sales went
higher, topping out at $60.70 in November 2022, which is the figure behind "above $60" in the articles.
Section 1a lays the measures side by side.

## Data

Public IPv4 auction sales from **[IPv4.Global / Hilco Global](https://auctions.ipv4.global/prior-sales)**.

On that page set *Presets* to **All time**, click **Export**, and save the file as `prior_sales.csv`
beside the notebook (or upload it when prompted in Colab). The export has the columns
`DATE, BLOCK, RIR, FINAL PRICE, $/ADDRESS`; the notebook needs `DATE`, `BLOCK` and `$/ADDRESS`.
The file is gitignored. Note that Hilco revises the list retrospectively, so two exports cut at the
same date are not guaranteed to be identical.

To reproduce an earlier article's figures, set `AS_OF` in the setup cell (or the `IPV4_AS_OF`
environment variable) to that article's data cutoff, for example `2026-06-19`.

## Run it

With [uv](https://docs.astral.sh/uv/):

```bash
uv sync --group dev
uv run jupyter notebook ipv4_prices.ipynb
# or execute headless:
uv run jupyter nbconvert --to notebook --execute ipv4_prices.ipynb --output executed.ipynb
```

Without uv: `pip install pandas numpy matplotlib scikit-learn tqdm jupyter`.

Or open it in Colab via the badge at the top of the notebook.

Notebook outputs are stripped on commit. After cloning, run `uv run nbstripout --install` once so your
commits do the same. The notebook as published with the June 2026 article is tagged `v2026.06`.

PRs, tweaks, and feedback welcome.

## Background reading

The methodology and conclusions are written up in these articles, in order:

1. [IPv4 Address Sale Price Trends](https://medium.com/@terrysweetser_90287/ipv4-address-sale-price-trends-abf45620d34f) (November 2025): the original analysis identifying the 2022 inflection point and the asset-to-technical-debt repricing.
2. [IPv4 is Technical Debt](https://medium.com/@terrysweetser_90287/ipv4-is-technical-debt-fa6449dc06d4) (December 2025): why the price is collapsing. The cost of the IPv6 substitute is racing to zero.
3. [IPv4 Sale Price Trends: Update June 2026](https://medium.com/@terrysweetser_90287/ipv4-sale-price-trends-update-june-2026-adcfc27b8662): six-month check-in on the predictions.
4. December 2026 update: in preparation, using sections 5–12 of this notebook.

The argument for *acting* on this, aimed at technical leaders, is the book
[**Making the IPv6 Decision**](https://www.amazon.com.au/dp/B0H5QQTJXV/) by Terry Sweetser.

## License

See [LICENSE](LICENSE).
