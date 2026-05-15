---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-12
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: '`MembershipFactory::tiers` will almost always return incorrect state'
vuln_class: []
---

# `MembershipFactory::tiers` will almost always return incorrect state

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** [`MembershipFactory::tiers`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L45-L50) exposes the [`_tiers`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L23) mapping for external consumption, containing specifically the important [`minted`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/libraries/MembershipDAOStructs.sol#L35) state member that indicates how many membership tokens have been minted for a given tier; however, it is not updated in either `MembershipFactory::joinDAO`, unlike the [parallel data structure](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L128), or `MembershipFactory::upgradeTier`, where both state updates are missing. This means that only the [initial configuration state](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L85) will be returned, unless a call is made to `MembershipFactory::updateDAOMembership` in which case the mappings for a given DAO are [synchronized](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L114). Again, this will only be correct until another membership is minted, after which the actual number of tokens minted for a given tier will exceed that stored in the mapping.

**Recommended Mitigation:** Consider updating both parallel data structures appropriately. Assuming other state update issues are fixed, the [`daos`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L22) mapping could be used to return the correct state; however, this would require either modifying `MembershipFactory::tiers` to return the `daos.tiers` array or implementing a separate call to query a specific array as the public mapping will not return it by default when simply querying `daos()`. In this case, the `_tiers` mapping is redundant and can be completely removed.

**One World Project:** Removed in [`09b6f0f`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/09b6f0f978d2a8d2952a6938bf5756bec8a0170d).

**Cyfrin:** Verified. `_tiers` is removed and `MembershipFactory::tiers` now returns the `dao.tiers` array.
