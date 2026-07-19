---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-4-9
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Optimize away `currentPeriodAmountTemp` variable in `RateLimiter::_addUsedAmount`
vuln_class: []
---

# Optimize away `currentPeriodAmountTemp` variable in `RateLimiter::_addUsedAmount`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** Optimize away `currentPeriodAmountTemp` in `RateLimiter::_addUsedAmount` by for example:
```solidity
  function _addUsedAmount(uint256 _usedAmount) internal {
    // @audit removed `currentPeriodAmountTemp`

    if (currentPeriodEnd < block.timestamp) {
      currentPeriodEnd = block.timestamp + periodInSeconds;
      // @audit removed assignment `currentPeriodAmountTemp = _usedAmount`
    } else {
      // @audit modifying `_usedAmount` instead of `currentPeriodAmountTemp`
      _usedAmount += currentPeriodAmountInWei;
    }

    // @audit use `_usedAmount` in check
    if (_usedAmount > limitInWei) {
      revert RateLimitExceeded();
    }

    // @audit use `_usedAmount` in assignment
    currentPeriodAmountInWei = _usedAmount;
  }
```

**Linea:**
Acknowledged; may be part of a future release.
