---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: '`ComplianceServiceGlobalWhitelisted::getComplianceTransferableTokens` returns
  positive token amount for blacklisted users'
vuln_class: []
---

# `ComplianceServiceGlobalWhitelisted::getComplianceTransferableTokens` returns positive token amount for blacklisted users

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** `ComplianceServiceGlobalWhitelisted::getComplianceTransferableTokens` inherited from `ComplianceServiceWhitelisted` will return positive amount of transferable tokens even if the user is blacklisted; this is misleading  because they actually have ZERO transferable tokens due to being blacklisted.

```solidity
  function getComplianceTransferableTokens(
        address _who,
        uint256 _time,
        uint64 /*_lockTime*/
    ) public view virtual override returns (uint256) {
        require(_time > 0, "Time must be greater than zero");
        return getLockManager().getTransferableTokens(_who, _time);
    }
```

**Recommended Mitigation:** The function should return 0 for blacklisted addresses.

**Securitize:** Fixed in commit [dc11a37](https://github.com/securitize-io/dstoken/commit/dc11a37ca955ecb0ee03baedcf5f580e7085b1bd).

**Cyfrin:** Verified.

\clearpage
