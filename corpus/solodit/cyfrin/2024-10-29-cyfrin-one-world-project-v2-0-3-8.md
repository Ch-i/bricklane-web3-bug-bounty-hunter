---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: Unused variables should be used or removed
vuln_class: []
---

# Unused variables should be used or removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** There following variables are declared but unused throughout the codebase:

* [`MembershipDAOStructs::UINT64_MAX`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/libraries/MembershipDAOStructs.sol#L4)
* [`MembershipERC1155::deployer`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L21)
* [`CurrencyManager::admin`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/CurrencyManager.sol#L21)

Consider using or removing these variables.

**One World Project:** Removed in [`09b6f0f`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/09b6f0f978d2a8d2952a6938bf5756bec8a0170d).

**Cyfrin:** Verified. The above variables have all been removed.
