---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-14
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`InvestorLockManager::createLockForInvestor`, `removeLockRecordForInvestor`
  should revert for invalid investor id'
vuln_class: []
---

# `InvestorLockManager::createLockForInvestor`, `removeLockRecordForInvestor` should revert for invalid investor id

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `InvestorLockManager::createLockForInvestor` should revert for invalid investor id:
```diff
    function createLockForInvestor(string memory _investor, uint256 _valueLocked, uint256 _reasonCode, string calldata _reasonString, uint256 _releaseTime)
        public
        override
        validLock(_valueLocked, _releaseTime)
        onlyTransferAgentOrAboveOrToken
    {
+    require(!CommonUtils.isEmptyString(_investor), "Unknown investor");
```

The same applies to `removeLockRecordForInvestor` - perhaps create a modifier and use that modifier on both functions.

**Securitize:** Acknowledged; while this is true, it also allows us to fully lock an investorId BEFORE it actually gets created on chain. There are cases where we know the investor id beforehand and in that case we could use this.
