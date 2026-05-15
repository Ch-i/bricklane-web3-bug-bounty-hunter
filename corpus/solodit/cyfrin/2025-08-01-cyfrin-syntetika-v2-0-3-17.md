---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-17
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: '`StakingVault::distributeYield` should revert when there are no vault shares'
vuln_class: []
---

# `StakingVault::distributeYield` should revert when there are no vault shares

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** `StakingVault::distributeYield` should revert when there are no vault shares, and in the updated code when the vault shares are only `DEAD_SHARES`. This could be elegantly implemented as:
```diff
    function distributeYield(
        uint256 yieldAmount,
        uint256 timestamp
    ) external onlyOwner {
+       require(totalSupply() > DEAD_SHARES, NoStakers());
```

**Syntetika:**
Fixed in commit [1b9d7f8](https://github.com/SyntetikaLabs/monorepo/commit/1b9d7f8968be39a815ced0d1545d9aec54530413).

**Cyfrin:** Verified.
