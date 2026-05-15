---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-3
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
title: Unnecessary storage gap in `MembershipERC1155` can be removed
vuln_class: []
---

# Unnecessary storage gap in `MembershipERC1155` can be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** `MembershipERC1155` declares a [storage gap](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L212-L213) at the very end of the contract:

```solidity
uint256[50] private __gap;
```

Such gaps are intended for use by abstract base contracts as they allow state variables to be added to the contract storage layout without "shifting down" the total number of utilized storage slots and thus potentially causing storage collisions in the inheriting contract.

`MembershipERC1155` is not intended to be used as a base contract inherited by other contracts and so has no need for a storage gap, meaning the one present is unnecessary and can be removed.

**One World Project:** Removed in [`09b6f0f`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/09b6f0f978d2a8d2952a6938bf5756bec8a0170d).

**Cyfrin:** Verified. `__gap` has been removed.
