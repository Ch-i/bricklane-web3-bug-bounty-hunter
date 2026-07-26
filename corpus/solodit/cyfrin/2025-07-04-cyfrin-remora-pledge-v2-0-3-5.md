---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`LockUpManager::LockUpStorage::_regLockUpTime` is never used'
vuln_class: []
---

# `LockUpManager::LockUpStorage::_regLockUpTime` is never used

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `LockUpManager::LockUpStorage::_regLockUpTime` is never used:
```solidity
$ rg "_regLockUpTime"
RWAToken/LockUpManager.sol
36:        uint32 _regLockUpTime; //lock up time for foreign to domestic trades
```

Either remove it or add a comment noting it will be used in the future but is currently not used.

**Remora:** Fixed in commit [91aed23](https://github.com/remora-projects/remora-smart-contracts/commit/91aed23b0a372a0aa3a7eac6e8e4a98563cea615) by adding a note noting it is intended for future use.

**Cyfrin:** Verified.
