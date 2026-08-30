---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-stakepet-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-stakepet
title: A malicious user can grief a `StakePet` contract by creating massive number
  of pets
vuln_class: []
---

# A malicious user can grief a `StakePet` contract by creating massive number of pets

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-stakepet.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md)_

---

**Severity:** Medium

**Description:** The `StakePet::create` function facilitates the minting of a pet NFT by depositing collateral. However, its lack of a minimum deposit requirement for minting exposes it to potential abuse. A malicious user can exploit this by minting an excessive number of NFTs. Notably, this behaviour can strain functions like `StakePetManager::buryAllDeadPets`, which in turn calls `StakePetManager::getDeadNonBuriedPets`. This latter function iterates through all pet IDs to identify pets that are dead but not yet buried.

**Impact:** When a function processes an extensive and potentially unlimited list of pet IDs, there's a risk of it consuming all available gas. Consequently, it can fail, throwing an out-of-gas exception, which negatively affects users trying to interact with the contract.

**Recommended Mitigation:** To deter such griefing attacks, it's advisable to introduce a minimum deposit requirement for the creation of a new pet. Setting this threshold ensures that the mass-minting strategy becomes cost-prohibitive for attackers.

**Client:** Fixed in commit [a692abc](https://github.com/Ranama/StakePet/commit/a692abc038fdd8992916f93d213a38c30e3a9764).

**Cyfrin:** Verified.
