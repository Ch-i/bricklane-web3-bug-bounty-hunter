---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-15
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: 'Inconsistent access-control patterns: mixed Ownable/AccessControl and mixed
  internal/external role revocation'
vuln_class: []
---

# Inconsistent access-control patterns: mixed Ownable/AccessControl and mixed internal/external role revocation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Grouping of stylistic/consistency issues in how access control is implemented. Neither is an exploitable gap, but both are drift risks and sources of reader confusion.

---

**1. `StakingVault` mixes `onlyOwner` with `onlyRole(DEFAULT_ADMIN_ROLE)`**

`StakingVault` mixes two access-control models - most admin setters use `onlyRole(DEFAULT_ADMIN_ROLE)` but `setCooldownDuration` and `setMinAssetsAmount` use `onlyOwner`. Since `Ownable`'s owner is set via `__Blacklistable_init(_initialAdmin)`, these happen to converge on the same address at init, but the inconsistency is a drift risk: future admin-role changes via `AccessControl` will not affect owner and vice versa.

**Recommended:** Pick one access-control model (`AccessControl` roles) for the whole contract.

---

**2. `Minter` mixes `_revokeRole` with external `revokeRole`**

Within the same contract, `setCustodian` calls `revokeRole(CUSTODIAN_ROLE, $.custodian)` (public, re-runs access control), while `setDistributor` and `setPauser` call `_revokeRole(...)` (internal). Both paths are gated by `DEFAULT_ADMIN_ROLE` so both succeed, but the style is inconsistent and the public version wastes gas on duplicate access-control checks.

**Recommended:** Use `_revokeRole` consistently.

---

**Syntetika:** Fixed in commit [`9b6a03e`](https://github.com/SyntetikaLabs/monorepo/commit/9b6a03e51c6b99660ab643e60c5ec970c11f169e)

**Cyfrin:** Verified.
