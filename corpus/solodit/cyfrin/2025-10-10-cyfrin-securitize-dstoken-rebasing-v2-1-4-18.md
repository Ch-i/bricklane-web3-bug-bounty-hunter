---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-18
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`ComplianceServiceRegulated::getComplianceTransferableTokens` should call
  `IDSLockManager::getTransferableTokensForInvestor`'
vuln_class: []
---

# `ComplianceServiceRegulated::getComplianceTransferableTokens` should call `IDSLockManager::getTransferableTokensForInvestor`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `ComplianceServiceRegulated::getComplianceTransferableTokens` already loads the registry and fetches the investor id, so therefore it should call `IDSLockManager::getTransferableTokensForInvestor` instead of `getTransferableTokens` to save again loading the registry and again fetching the investor id:
```diff
    function getComplianceTransferableTokens(
        address _who,
        uint256 _time,
        uint64 _lockTime
    ) public view override returns (uint256) {
        require(_time != 0, "Time must be greater than zero");
        string memory investor = getRegistryService().getInvestor(_who);

-       uint256 balanceOfInvestor = getLockManager().getTransferableTokens(_who, _time);
+       uint256 balanceOfInvestor = getLockManager().getTransferableTokensForInvestor(investor, _time);

```

**Securitize:** Fixed in commit [382eaae](https://github.com/securitize-io/dstoken/commit/382eaae50dbf5a9a33ce343268e6dc9d257428c2).

**Cyfrin:** Verified.
