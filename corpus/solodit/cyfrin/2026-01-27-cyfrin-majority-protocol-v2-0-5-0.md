---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-5-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Use `uint128` to pack `DepositManager::protocolFee`, `maxCreatorFee` into the
  same storage slot
vuln_class: []
---

# Use `uint128` to pack `DepositManager::protocolFee`, `maxCreatorFee` into the same storage slot

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `DepositManager::protocolFee`, `maxCreatorFee` (and the same fields inside the `GamePool` struct) will always be < `BASIS_POINTS=10000`, so they can be declared as `uint128` to pack both of them into the same storage slot.

This means that functions such as `DepositManager::getRewards` which read both of them can perform only 1 storage read instead of 2.

**Majority Games:**
Fixed in commit [adedfc2](https://github.com/Engage-Protocol/engage-protocol/commit/adedfc2224c118fd2ac88eeec826bd4be48d8b6e).

**Cyfrin:** Verified.
