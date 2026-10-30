# How-to — update a documented claim

Edit `data/protocols.json`; only write a factual assertion when an up-to-date official source supports it. Add the source URL to that protocol. If a rate changes, date the claim and preserve the former snapshot in Git. Rerun tests and regenerate the artifacts. Do not put inferred market liquidity or returns in the current design-only dataset. For separate live metrics, use `src/fetch_llama.py --live` when online, keeping API read-only.

### Reproduce illustrative micro-timeframe sensitivity

`python3 src/holding_cost_scenarios.py` writes 15 explicitly marked **hypothetical** scenario rows. Modify `ASSUMPTIONS` to conduct sensitivity tests. Do not relabel scenario values as observed fees or official smart-contract decay formulas.
