---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-18
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
title: '`MembershipFactory::joinDAO` will not function correctly with fee-on-transfer
  tokens'
vuln_class: []
---

# `MembershipFactory::joinDAO` will not function correctly with fee-on-transfer tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** While it is understood that the protocol does not intend to support fee-on-transfer tokens, it is prescient to note that `MembershipFactory::joinDAO` will [not function correctly](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L129-L130) if tokens of this type are ever added to the `CurrencyManager`:

```solidity
IERC20(daos[daoMembershipAddress].currency).transferFrom(msg.sender, owpWallet, platformFees);
IERC20(daos[daoMembershipAddress].currency).transferFrom(msg.sender, daoMembershipAddress, tierPrice - platformFees);
```

Here, the actual number of tokens received by `owpWallet` and `daoMembershipAddress` will be less than expected.

**One World Project:** Acknowledged. Fee on transfer tokens are not supported.

**Cyfrin:** Acknowledged.
