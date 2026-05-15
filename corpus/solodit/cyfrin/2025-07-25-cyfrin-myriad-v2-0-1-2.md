---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Consider enforcing a `minAmount` to prevent rounding exploits
vuln_class: []
---

# Consider enforcing a `minAmount` to prevent rounding exploits

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** To protect against potential precision-based exploits or rounding errors, the protocol should consider enforcing a `minAmount` threshold (e.g., equivalent to $1 in token units) across user-facing actions such as trades, liquidity provision, and claims.

When very small amounts are allowed, they may trigger edge cases in rounding logic, fee calculations, or invariant enforcement, especially in markets using fixed-point math. Even if not currently exploitable, disallowing "dust" amounts provides a safer baseline.

Consider applying a protocol-wide `minAmount` check to user-facing actions such as `buy`, `sell`, `addLiquidity`, and `claim*` functions.

**Myriad:** Acknowledged. Even though the recommendation makes sense, it's quite complex to implement on a multi-token environment. There's a few points to consider, such as:

- ERC20 Token decimals - The standard is 18, however for stablecoins such as USDC or USDT is 6.
- ERC20 Token Price - Consider DAI and WETH - both have 18 decimals, however 1 DAI = 1$ and 1 WETH > $3700

Given the points above, a protocol-wide `minAmount` wouldn't be appropriate given we might be dealing with different decimals and prices for different markets. In order to implement this, it would have to be enforced on the `PredictionMarketManager` side of things, which in my opinion is an overhead of logic I'd like to avoid at this point.
