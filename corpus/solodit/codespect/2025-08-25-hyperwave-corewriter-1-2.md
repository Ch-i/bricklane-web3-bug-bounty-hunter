---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-25-hyperwave-corewriter-1-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md
tags:
- firm:codespect
- report:2025-08-25-hyperwave-corewriter
title: '[I-03] Possible overflow during price tolerance control'
vuln_class: []
---

# [I-03] Possible overflow during price tolerance control

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-25-Hyperwave-CoreWriter.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md)_

---

**Files:** [`TradeStakeManager.sol`](https://github.com/SwellNetwork/hlp-corewriter/blob/a48131cc4317304b4a7f32d90f5d8404abd6466d/src/TradeStakeManager.sol#L234)

**Description:**

The `6dabdeeec70afc123d694fac0fcbb2d90ddb4c87` commit introduced control on perps price using tolerance parameter which can be set by the `GOVERNOR` role for each `perpIndex`. The price privided by the `OPERATOR` during sell and buy order placing is compared against `markPrice` which is obtained from the HyperCore and is scaled to 8 decimals by the `_getMarkPxForPerp(...)` function.

Below `minPrice` and `maxPrice` calculation can revert during the multiplication part, especially for the last one. In case the `markPrice * (10000 + toleranceBps)` crosses the `type(uint64).max` value, overflow happens.

```solidity
uint64 markPrice = _getMarkPxForPerp(perpIndex);
uint64 minPrice = (markPrice * (10000 - toleranceBps)) / 10000;
uint64 maxPrice = (markPrice * (10000 + toleranceBps)) / 10000;
```

As the `markPrice` is checked inside `_getMarkPxForPerp(...)` to be lower than `type(uint64).max`, such situation can theoretically happen, If the returned `markPrice` is above 922383322851620. That is assuming the maximum possible `toleranceBps` value, which is `19_999`.

**Impact:** Order placement will revert in case the price is sufficiently high. The above number, when interpreted as an 8 decimal USDC price, is $9.223.372 hence it is not likely to happen in the near future; however, if the HyperCore introduces other quote currencies in the future, it might become a problem.

**Recommendation:** Introduce `uint256` casting to the operation, before casting it down to `uint64`.

**Status:** Fixed

**Client response:** Resolved in [4108aed13b26ad0cb70fc42d2dba99eec145af7c](https://github.com/SwellNetwork/hlp-corewriter/pull/58/commits/4108aed13b26ad0cb70fc42d2dba99eec145af7c)
