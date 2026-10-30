# Reference — schema and execution

`data/protocols.json`: root `as_of` (YYYY-MM-DD), `research_question`, `scope`, `protocols[]`. Each protocol has: `name`, `execution`, `liquidity`, `collateral_and_settlement`, `funding_model`, `fee_mechanism`, `risk_focus`, `caveat`, `source_urls[]`.

`src/build_report.py --root PATH`: reads `PATH/data/protocols.json`, emits CSV, Markdown, SVG to `PATH/artifacts/`.

`src/fetch_llama.py --live --out PATH`: makes 3 read-only requests to DefiLlama **free** endpoints: fees, revenue and open interest. It does not download derivatives volume because the latter requires a paid API plan as of 2026-10-30. Missing metrics stay `null` and are never replaced with zero.
