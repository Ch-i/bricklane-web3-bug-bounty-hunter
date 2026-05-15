---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-12
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: '`SecuritizeAmmNavProvider` violates core AMM invariant that `k` should never
  decrease'
vuln_class: []
---

# `SecuritizeAmmNavProvider` violates core AMM invariant that `k` should never decrease

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** Both `SecuritizeAmmNavProvider::_curveBuy` and `_curveSell` round down when calculating new reserves:
```solidity
// `_curveBuy`
newQuote = Y + amountInQuote;
newBase = kLocal / newQuote; // @audit rounds down, k decreases

// `_curveSell`
newBase = X + amountInBase;
newQuote = kLocal / newBase; // @audit rounds down, k decreases
```
This causes users to receive slightly more output than mathematically correct and also `k` to effectively decrease over time.

Best practice is to have an invariant that `k` never decreases (as can be seen in [`UniswapV2Pair::swap`](https://github.com/Uniswap/v2-core/blob/master/contracts/UniswapV2Pair.sol#L182)). I.e. round in favor of the protocol.

**Impact:** Dust-level value leakage per trade; minimal practical impact due to virtual AMM design and periodic resets.

**Recommended Mitigation:** Consider explicitly rounding up using OZ [Math::ceilDiv](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/Math.sol#L183-L197).

**Securitize:** Fixed in commit [04d2392](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/04d2392c4944aead08bf7a4793fd57e625918910).

**Cyfrin:** Verified.
