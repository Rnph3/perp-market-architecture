# Perpetual DEX Market Structure: Sai vs Hyperliquid vs GMX vs dYdX Chain
**Documentation snapshot:** 2026-10-30. **Type:** qualitative protocol research, NOT live financial performance.

## Research question
How does venue architecture change counterparty, execution, funding and liquidity-provider risk in perpetual DEXs?

## Executive summary
The trading venue is not just its interface. An oracle-priced vault-backed venue exposes liquidity-provider inventory and oracle/settlement risks; an order-book venue shifts execution quality toward resting liquidity and matching mechanics. These are structural observations, not evidence that one design performs better.

## Source-traceable design matrix
| Venue | Execution | Backing liquidity | Funding/borrow | Principal risk |
|---|---|---|---|---|
| Sai | Oracle-settled automated market maker | SLP liquidity vaults | OI-imbalance borrowing fee charged to crowded side; not necessarily paid to opposite-side traders | Oracle integrity, pool solvency, dynamic leverage and rapid-close costs |
| Hyperliquid | Onchain central-limit-order-book-style matching (price-time priority) | Resting maker orders and market makers | Perpetual funding payments for spot-price convergence | Order-book depth, market-maker concentration, oracle/mark and margining |
| GMX | Oracle-priced pool-based perpetual execution | GM / GLV vault liquidity | Adaptive funding plus utilization/borrowing fees | Pool PnL limits, utilization and withdrawal constraints |
| dYdX Chain | Validator-maintained in-memory order books with block matching | Distributed resting orders / market makers | Perpetual market funding (specific rate formulas not compared) | Order dissemination, mempool latency, consensus, liquidations |

## Venue-by-venue mechanics

### Sai
- **Execution:** Oracle-settled automated market maker.
- **Liquidity:** SLP liquidity vaults.
- **Collateral/settlement:** USDC / stNIBI supported; self-custodied; gasless trading (bridge gas still possible).
- **Funding:** OI-imbalance borrowing fee charged to crowded side; not necessarily paid to opposite-side traders.
- **Fee mechanism:** 0.05% base taker; 0% maker; 0.01% trigger; additional decaying rapid-close fee applies to very short holds.
- **Researchable failure mode:** Oracle integrity, pool solvency, dynamic leverage and rapid-close costs.
- **Limitation:** Fee schedule and protected market parameters can change; no direct performance claim..
**Primary sources:**
  - https://sai.fun/docs/learn
  - https://sai.fun/docs/learn/trading/fees
  - https://sai.fun/docs/dev/sai-core/

### Hyperliquid
- **Execution:** Onchain central-limit-order-book-style matching (price-time priority).
- **Liquidity:** Resting maker orders and market makers.
- **Collateral/settlement:** HyperCore clearinghouse and margin engine.
- **Funding:** Perpetual funding payments for spot-price convergence.
- **Fee mechanism:** Order book spread and maker/taker economics (rates excluded pending fee-tier snapshot).
- **Researchable failure mode:** Order-book depth, market-maker concentration, oracle/mark and margining.
- **Limitation:** Order-book state may diverge from quoted liquidity under stress; effective fees vary by account tier..
**Primary sources:**
  - https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/order-book
  - https://hyperliquid.gitbook.io/hyperliquid-docs/trading/contract-specifications
  - https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/oracle

### GMX
- **Execution:** Oracle-priced pool-based perpetual execution.
- **Liquidity:** GM / GLV vault liquidity.
- **Collateral/settlement:** Liquidity pools back trader profits and losses.
- **Funding:** Adaptive funding plus utilization/borrowing fees.
- **Fee mechanism:** Published open/close fees and separate open-interest-imbalance price impact, borrowing and network fees.
- **Researchable failure mode:** Pool PnL limits, utilization and withdrawal constraints.
- **Limitation:** Fee and price impact vary by market, position and conditions..
**Primary sources:**
  - https://docs.gmx.io/docs/intro/
  - https://docs.gmx.io/docs/providing-liquidity/
  - https://docs.gmx.io/docs/trading/fees/

### dYdX Chain
- **Execution:** Validator-maintained in-memory order books with block matching.
- **Liquidity:** Distributed resting orders / market makers.
- **Collateral/settlement:** Cosmos SDK application-chain software; validator consensus.
- **Funding:** Perpetual market funding (specific rate formulas not compared).
- **Fee mechanism:** Order book / maker-taker design; absolute rates excluded pending current protocol snapshot.
- **Researchable failure mode:** Order dissemination, mempool latency, consensus, liquidations.
- **Limitation:** Documentation applies to dYdX Chain software; deployed instances can vary..
**Primary sources:**
  - https://docs.dydx.exchange/
  - https://docs.dydx.exchange/concepts-limit-order-book-and-matching
  - https://docs.dydx.exchange/introduction-onboarding_faqs

## Falsifiable follow-up questions
1. For a fixed notional and liquidity regime, what is the realized all-in execution cost (including rapid-close penalties, funding, and price impact)?
2. Under large price jumps, which mechanism absorbs losses: liquidity providers, resting orders, insurance/clearing, or liquidation cascades?
3. How much execution quality varies with position holding horizon (30 seconds vs 30 minutes vs 1 day)?
4. Which stated risk controls can be verified onchain or through public historical events?

## Data gaps / research integrity
- No verified October 30 trading volume, TVL, open interest or realized PnL snapshot was fetched in the current execution environment.
- DefiLlama current *derivatives volume* overview requires an API plan; this project does not use it or claim free access.
- Fees and open interest may be available from separate free endpoints; their methodology and instrument coverage can differ.
- The comparison does NOT endorse or recommend trading any product; it is a public-documentation audit.

## Reproducibility
`python3 src/build_report.py` regenerates the matrix, Markdown and SVG without external dependencies. For fresh DefiLlama free fees/OI data run `python3 src/fetch_llama.py --live`; live data is not a prerequisite for the qualitative report.

## References
- **Sai**: https://sai.fun/docs/learn · https://sai.fun/docs/learn/trading/fees · https://sai.fun/docs/dev/sai-core/
- **Hyperliquid**: https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/order-book · https://hyperliquid.gitbook.io/hyperliquid-docs/trading/contract-specifications · https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/oracle
- **GMX**: https://docs.gmx.io/docs/intro/ · https://docs.gmx.io/docs/providing-liquidity/ · https://docs.gmx.io/docs/trading/fees/
- **dYdX Chain**: https://docs.dydx.exchange/ · https://docs.dydx.exchange/concepts-limit-order-book-and-matching · https://docs.dydx.exchange/introduction-onboarding_faqs
