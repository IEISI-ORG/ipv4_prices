# IPv4 Price Trends

Analysis of the secondary market for IPv4 addresses, using public auction data to track the
post-2022 price collapse and project when each subnet size effectively reaches zero.

The thesis: an IPv4 address was never an asset. Its price is the **deferral cost of IPv6
migration** — a "laziness tax" that falls as IPv6 gets cheaper to deploy. The data shows a
structural decline, not a cyclical dip, heading toward a terminal liquidity event for larger
subnets around 2027.

## The analysis

[`ipv4_prices.ipynb`](ipv4_prices.ipynb) (runs in Google Colab) does the following:

1. **Loads & cleans** sale records from IPv4.Global's prior-sales export.
2. **Finds the inflection point** — the monthly-average peak (early 2022, above $60/address)
   and the five steepest monthly drops.
3. **Projects the decline per subnet size** using four independent models, each estimating
   when prices reach $0 (or $1):
   - Linear regression
   - 3rd-degree polynomial
   - Exponential decay (log-linear)
   - Monte Carlo simulation (Geometric Brownian Motion, 2000 paths × 20 years)

The four models are a deliberate comparison: they bracket the uncertainty rather than asserting
a single forecast. As of June 2026 the data tracks closest to the cubic polynomial, with the
average price near $20 and curves for different subnet sizes converging toward a $0 "event
horizon" in 2027.

## Data

Public IPv4 auction sales from **[IPv4.Global / Hilco Global](https://auctions.ipv4.global/prior-sales)**.

Export the prior-sales table to `prior_sales.csv` (columns include `date`, `$/address`, `block`)
and place it beside the notebook, or upload it when prompted in Colab.

## Run it

```bash
pip install pandas numpy matplotlib scikit-learn tqdm
jupyter notebook ipv4_prices.ipynb
```

Or open it directly in Colab via the badge at the top of the notebook. PRs, tweaks, and feedback
welcome.

## Background reading

The methodology and conclusions are written up in three articles, in order:

1. [IPv4 Address Sale Price Trends](https://medium.com/@terrysweetser_90287/ipv4-address-sale-price-trends-abf45620d34f) — the original analysis identifying the 2022 inflection point and the asset-to-technical-debt repricing.
2. [IPv4 is Technical Debt](https://medium.com/@terrysweetser_90287/ipv4-is-technical-debt-fa6449dc06d4) — why the price is collapsing: the cost of the IPv6 substitute is racing to zero.
3. [IPv4 Sale Price Trends: Update June 2026](https://medium.com/@terrysweetser_90287/ipv4-sale-price-trends-update-june-2026-adcfc27b8662) — six-month check-in on the predictions.

The argument for *acting* on this — aimed at technical leaders — is the book
[**Making the IPv6 Decision**](https://www.amazon.com.au/dp/B0H5QQTJXV/) by Terry Sweetser.

## License

See [LICENSE](LICENSE).
