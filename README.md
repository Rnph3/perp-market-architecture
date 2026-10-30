# PerpDEX Market Structure Research Kit — 2026-10-30

**STATUS: reproducible qualitative research prototype**. The current checked-in matrix is derived from primary protocol documentation. Do **not** call it a live trading-data backtest or evidence of winning returns.

## Quick start

```bash
python3 -m unittest discover -s tests -v
python3 src/build_report.py
python3 src/fetch_llama.py           # defaults to no network
python3 src/fetch_llama.py --live    # OPTIONAL: requires Internet, current free DefiLlama fees/revenue/OI
```

Outputs: `artifacts/research_report.md`, `artifacts/design_matrix.csv`, `artifacts/comparison.svg`; optionally `artifacts/live_metric_snapshot.json` if a network fetch succeeds. Dependencies: Python standard library only (tested on Python 3.14.0a3 on macOS; other versions untested).

### Documentation (Diátaxis)

- [Tutorial](docs/tutorial.md): regenerate and inspect the report.
- [How-to](docs/howto-update.md): update a protocol claim with evidence.
- [Reference](docs/reference.md): input/output schema and CLI.
- [Explanation](docs/explanation.md): why the research separation matters.

## Intended use

A reproducible, source-traceable starting point for comparing perpetual-DEX architectures (Sai, Hyperliquid, GMX, dYdX Chain) from public documentation, plus a transparent sensitivity table for holding-time costs. It is a structure comparison, not market intelligence.

## Evidence status

- [x] Source URLs for each venue (all 12 returned HTTP 200 on 2026-10-30).
- [x] Sai fee-schedule claims (0.05% base taker, 0% maker, 0.01% trigger, rapid-close fee exists) checked against the official fees page. Hyperliquid, GMX and dYdX entries: URLs reachable, content **not independently re-verified** — check before relying on them.
- [x] Four-source matrix generated reproducibly and tests pass locally.
- [x] Explicit separation between documented mechanism and unobserved market outcomes.
- [ ] Live API refresh (`--live`) **not executed**; no live figures are included.
- [ ] Original execution-quality experiment and actual statistical results **not yet conducted**.

## Publishing integrity

This report is a starting point for independent research. Verify current documentation and conclusions yourself, disclose AI assistance as required by each venue, avoid any unsupported claims of actual trading PnL, and distinguish public documentation from independent validation.

### Additional quantitative proof: explicitly hypothetical holding-cost sensitivity

Run `python3 src/holding_cost_scenarios.py`. This produces 15 transparent fee-sensitivity scenarios in `artifacts/illustrative_cost_sensitivity.csv` for 30-second, 3-minute, 12-minute, 30-minute and 1-day holding horizons. The example uses an **illustrative** 10,000 USD notional, 5 bps per side, 4 bps slippage, 115 bps maximum early-close penalty and 10% assumed annual borrowing. These are scenario **inputs**, **not observations**. Linear/step decay curves are deliberately hypothetical and do **not** represent Sai smart-contract implementation or verified trading costs. This is a falsifiable setup for a later real-data study, not a trade recommendation.

## Test results (2026-10-30, local)

- `python3 -m unittest discover -s tests -v`: 7 tests, OK.
- `python3 src/build_report.py` and `python3 src/holding_cost_scenarios.py` regenerate `artifacts/` byte-identically to the committed files.

## License

See `LICENSE`.
