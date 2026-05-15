---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-10
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Not mechanism to automatically cleanup locks that are already unlock-able on
  LockManagers
vuln_class: []
---

# Not mechanism to automatically cleanup locks that are already unlock-able on LockManagers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `InvestorLockManager` as well as `LockManager` contracts don't have a mechanism to automatically clean up unlock-able locks; it is only possible to remove locks via manual intervention using the function `removeLockRecord` or `removeLockRecordForInvestor`, none of which validates if the locking period has already passed or not.

**Impact:** The lack of a mechanism to automatically clear up already unlocked locks can cause multiple problems/inefficiencies, such as:
- Wasting gas when transferring tokens by iterating over and over on already unlocked locks
- Admin errors when deleting locks that could unintentionally remove the lock for a lockIndex that is actually locked and should remain as is.

**Recommended Mitigation:** Consider implementing a mechanism to automatically clean up already unlocked locks, similar to how the investors Issuances are automatically cleaned up by `ComplianceServiceRegulated::cleanUpInvestorIssuances`.

**Securitize:** Acknowledged.
