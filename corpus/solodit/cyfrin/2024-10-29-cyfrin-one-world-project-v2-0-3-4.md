---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-4
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
title: '`MembershipFactory::owpWallet` lacks explicitly declared visibility'
vuln_class: []
---

# `MembershipFactory::owpWallet` lacks explicitly declared visibility

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** [`MembershipFactory::owpWallet`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L20) has no declared visibility:

```solidity
address owpWallet;
```

This gives it the default `internal` visibility; however, it is best practice to explicitly specify the visibility for state variables in the contract.

**One World Project:** Made public in [`09b6f0f`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/09b6f0f978d2a8d2952a6938bf5756bec8a0170d).

**Cyfrin:** Verified. `owpWallet` is public.
