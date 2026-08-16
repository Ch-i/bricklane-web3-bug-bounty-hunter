---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: Consider making `MembershipERC1155::totalSupply` `public`
vuln_class: []
---

# Consider making `MembershipERC1155::totalSupply` `public`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** The [`totalSupply`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L23) variable in the `MembershipERC1155` contract is currently marked as `private`:

```solidity
uint256 private totalSupply;
```

As this state variable could be valuable for off-chain computations, it is recommended to consider making it `public` for easier access.

**One World Project:** Updated in [`09b6f0f`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/09b6f0f978d2a8d2952a6938bf5756bec8a0170d).

**Cyfrin:** Verified. `totalSupply` is now public.
