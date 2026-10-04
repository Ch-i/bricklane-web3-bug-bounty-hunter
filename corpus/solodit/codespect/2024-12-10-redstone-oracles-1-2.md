---
affected_contracts: []
derives_from: []
id: solodit-codespect-2024-12-10-redstone-oracles-1-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2024-12-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2024-12-10-RedStone-Oracles.md
tags:
- firm:codespect
- report:2024-12-10-redstone-oracles
title: '[I-03] Potential Rounding Down Could Decrease Overall Price'
vuln_class: []
---

# [I-03] Potential Rounding Down Could Decrease Overall Price

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2024-12-10-RedStone-Oracles.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2024-12-10-RedStone-Oracles.md)_

---

**Files:** [NumericArrayLib.sol](https://github.com/redstone-finance/redstone-oracles-monorepo/blob/ff0f3dcb085f28bd80ddc096825701db6e14d0af/packages/evm-connector/contracts/libs/NumericArrayLib.sol#L17-L26)

**Description:**

The prices for the feeds are calculated as the median of all values. The median requires a sorted array of elements, taking the middle value. However, when the number of elements is even, the median is calculated as the arithmetic average of the two middle elements:

```solidity
uint256 sum = arr[middleIndex - 1] + arr[middleIndex];
return sum / 2;
```

Since Solidity does not support decimal numbers, some precision may be lost during this operation due to rounding down which could lead to different prices than was expected. This behaviour is likely known to the Redstone protocol, but it’s important to note this potential loss in precision to maintain reasonable decimal accuracy for the prices.

By default, Redstone feeds use eight decimals, where the expected precision loss is around 0.0000005%, which is considered negligible.

**Recommendation:** Ensure awareness of this rounding behaviour to maintain appropriate precision in price calculations.

**Status:** Acknowledged

**Client response:** Acknowledged!
