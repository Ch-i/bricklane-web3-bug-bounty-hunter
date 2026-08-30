---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-1-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Add explicit check to prevent underflow revert in `PredictionMarketV3_4::calcSellAmount`
vuln_class: []
---

# Add explicit check to prevent underflow revert in `PredictionMarketV3_4::calcSellAmount`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** In [`PredictionMarketV3_4::calcSellAmount`](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/PredictionMarketV3_4.sol#L434) following line may revert due to an underflow if the user attempts to sell too many shares:

```solidity
endingOutcomeBalance = (endingOutcomeBalance * outcomeShares).ceilDiv(outcomeShares - amountPlusFees);
```

If `amountPlusFees >= outcomeShares`, the denominator becomes zero or negative, causing a revert. While this is mathematically expected, it may be confusing for users who receive no clear indication of what went wrong.

Consider adding an explicit check such as:

```solidity
require(amountPlusFees < outcomeShares, "a>s");
```

This provides a clearer error message and avoids reverting due to underflow during calculation.

**Myriad:** Fixed in [PR#80](https://github.com/Polkamarkets/polkamarkets-js/pull/80), commit [`90a2742`](https://github.com/Polkamarkets/polkamarkets-js/pull/80/commits/90a274240da4b4a020098ff4d018b6df908e816b)

**Cyfrin:** Verified. A check to verify there's more outcome shares than amount is now in place.
