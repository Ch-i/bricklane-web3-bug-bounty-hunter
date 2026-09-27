---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-18-maitreja-staking-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md
tags:
- firm:codespect
- report:2026-02-18-maitreja-staking
title: '[I-01] Emergency withdrawals blocked in case of too many stakes'
vuln_class: []
---

# [I-01] Emergency withdrawals blocked in case of too many stakes

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-18-Maitreja-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md)_

---

**Files:** [ProgressiveStaking.sol](https://github.com/whaleden-mjtd/maitme-contracts-staking/blob/ce61102843ceb1c27d875b394490ff859577016c/src/ProgressiveStaking.sol#L341)

**Description:**

For the `StakePosition` dynamic array, there is no maximum length limit. Although the array decreases when positions are removed, a user holding too many positions at the same time could have the emergency withdrawals affected. Positions of Web2 accounts, are managed under a single admin address. If this address holds an excessive number of users’ positions, in case of a security issue, emergency withdrawals may fail due to out-of-gas errors. And it may affect the `calculateTotalRewards(...)` view function. The emergency withdrawal functionality will reach its gas limits between 7,672 and 8,172 amount of positions for a single address.

**Impact:** Emergency withdrawal functionality not available for Web2 accounts.

**Recommendation:** Place a reasonable limit on how many stakes each address can open. For Web2 distribute the stakes across multiple custodial addresses.

**Status:** Fixed
