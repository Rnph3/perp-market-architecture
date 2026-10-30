# Explanation — separate architecture from observed performance

Oracle+pool venues shift some risk onto pooled liquidity; order-book venues depend on posted liquidity, matching, and clearing mechanics. Those are structural differences, not a reason to claim one venue has better fills, lower effective costs, or lower tail risk. To compare realized execution costs one needs matched instruments, comparable notional, volatility, time of day, leverage, funding period, and a reproducible sample. Official documentation is necessary but not sufficient to show production behavior.
