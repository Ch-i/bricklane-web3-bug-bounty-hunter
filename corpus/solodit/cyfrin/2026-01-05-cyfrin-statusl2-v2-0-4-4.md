---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Consider simplifying formulas in `MultiplierPointMath.sol`
vuln_class: []
---

# Consider simplifying formulas in `MultiplierPointMath.sol`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** For some reason `MultiplierPointMath.sol` uses 100 in formulas instead of simplifying to this:
```diff
-   uint256 public constant MP_APY = 100;

    function _accrueMP(uint256 _balance, uint256 _deltaTime) internal pure returns (uint256 accruedMP) {
-       return Math.mulDiv(_balance, _deltaTime * MP_APY, YEAR * 100);
+       return Math.mulDiv(_balance, _deltaTime, YEAR);
    }
```

Expected `_balance` variable has 1e18 precision, so multiplying with 100 doesn't change anything. Removing it from calculations will make code easier to read.

**Recommended Mitigation:** Consider simplifying formulas in `MultiplierPointMath.sol`.

**StatusL2:** Fixed in [16c5b3c](https://github.com/status-im/status-network-monorepo/commit/16c5b3c64009042515491d8ad39d7e812ec4a841).

**Cyfrin:** Verified.
