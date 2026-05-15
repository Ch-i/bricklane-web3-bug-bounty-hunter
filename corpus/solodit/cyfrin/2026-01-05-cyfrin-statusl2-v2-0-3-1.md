---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-3-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Migrations to self are possible
vuln_class: []
---

# Migrations to self are possible

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Migrations to self are possible (if staked balance == 0). This causes weird state transitions like completely deleting the position due to the `delete vaultData[msg.sender];`. While no serious impact has been found yet (except self-harm, user mistake scenarios), it is advised to disallow that.

**Impact:** Unintended state transitions.

**Recommended Mitigation:**
```diff
function migrateToVault(address migrateTo) external onlyOwner onlyNotLeft {
+   require(migrateTo != address(this));
    // ...
}
```

**StatusL2:** Fixed in [08ada30](https://github.com/status-im/status-network-monorepo/commit/08ada30122a7fc604d6be284457f8f9b13677cf2).

**Cyfrin:** Verified.
