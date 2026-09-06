---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-2-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: '`MbpsFeeManager::setFeePercentageMBPS` allows setting fee greater than max'
vuln_class: []
---

# `MbpsFeeManager::setFeePercentageMBPS` allows setting fee greater than max

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `MbpsFeeManager::setFeePercentageMBPS` allows setting fee greater than max; recommend enforcing a maximum fee percentage eg:
```diff
contract MbpsFeeManager is IFeeManager, BaseContract {
    uint256 public constant FEE_DENOMINATOR = 100_000;
+   uint256 public constant MAX_FEE = 10_000; // 10%

    function setFeePercentageMBPS(uint256 _fee) external onlyRole(DEFAULT_ADMIN_ROLE) {
+       require(_fee <= MAX_FEE);
        uint256 oldFee = feePercentageMBPS;
        feePercentageMBPS = _fee;
        emit FeeUpdated(oldFee, _fee);
    }
```

**Securitize:** Acknowledged.

\clearpage
