---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-13
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: The Beacon proxy pattern is better suited to upgrading multiple instances of
  `MembershipERC1155`
vuln_class: []
---

# The Beacon proxy pattern is better suited to upgrading multiple instances of `MembershipERC1155`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** Currently, new membership DAOs are deployed as [Transparent upgradeable proxies](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L66-L70), managed by a [single instance](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L40) of `ProxyAdmin` [exposed](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L155-L163) to the privileged `EXTERNAL_CALLER` role. Assuming that the intention is to upgrade all DAO proxies in the event the `MembershipERC1155` implementation requires updating, it will be cumbersome to iterate through each contract to perform the upgrade. The [Beacon proxy pattern](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/beacon/BeaconProxy.sol) is better-suited to performing this type of global implementation upgrade for all managed proxies and thus recommended over the existing design.

**One World Project:** The Upgrades will be choices for each DAO separately. So kept as it is.

**Cyfrin:** Acknowledged.
