---
affected_contracts: []
derives_from: []
id: solodit-hexens-2025-02-03-rush-trading-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-02-03T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-03-Rush-Trading.md
tags:
- firm:hexens
- report:2025-02-03-rush-trading
title: '[RUSH1-6] _getIsUnwindThresholdMet should include subsidyAmount for threshold
  calculation'
vuln_class: []
---

# [RUSH1-6] _getIsUnwindThresholdMet should include subsidyAmount for threshold calculation

_Section severity (from Solodit section header): Low_  
_Audit firm: Hexens_  
_Source report: [2025-02-03-Rush-Trading.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-03-Rush-Trading.md)_

---

**Severity:** Low

**Description:** To unwind liquidity before the deadline, the current reserves must exceed the EARLY_UNWIND_THRESHOLD. This threshold should also include the subsidyAmount, since the initialWETHReserve is the sum of deployment.amount and deployment.subsidyAmount.
```
    function _getIsUnwindThresholdMet(address uniV2Pair) internal view returns (bool isUnwindThresholdMet) {
        LD.LiquidityDeployment storage deployment = _liquidityDeployments[uniV2Pair];
        (uint256 currentReserve,,) = _getOrderedReserves(uniV2Pair);
        uint256 targetReserve = deployment.amount + EARLY_UNWIND_THRESHOLD;
        isUnwindThresholdMet = currentReserve >= targetReserve;
    }
```

**Remediation:**  
```
    function _getIsUnwindThresholdMet(address uniV2Pair) internal view returns (bool isUnwindThresholdMet) {
        LD.LiquidityDeployment storage deployment = _liquidityDeployments[uniV2Pair];
        (uint256 currentReserve,,) = _getOrderedReserves(uniV2Pair);
--      uint256 targetReserve = deployment.amount + EARLY_UNWIND_THRESHOLD;
++      uint256 targetReserve = deployment.amount + deployment.subsidyAmount EARLY_UNWIND_THRESHOLD;
        isUnwindThresholdMet = currentReserve >= targetReserve;
    }
```

**Status:** Fixed

---
