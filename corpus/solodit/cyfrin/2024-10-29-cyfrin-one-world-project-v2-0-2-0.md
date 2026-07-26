---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: '`MembershipERC1155` should use OpenZeppelin upgradeable base contracts'
vuln_class: []
---

# `MembershipERC1155` should use OpenZeppelin upgradeable base contracts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** `MembershipERC1155` is an implementation contract intended for use with `TransparentUpgradeableProxy`, controlled via an instance of `ProxyAdmin`; however, it does not utilize the OpenZeppelin upgradeable contracts which are designed to avoid storage collisions between upgrades.

**Impact:** Upgrading the contract with new OpenZeppelin libraries can lead to storage collisions.

**Recommended Mitigation:** Consider using the upgradeable versions of `ERC1155`, `AccessControl` and `Initializable`.

**One World Project:** Updated the openzeppelin version, and solidity version. Had to change some functions due to change in openzeppelin’s contracts in [`1c3e820`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/1c3e820adc53d977cd2337af1c2d524fc1ac2782).

**Cyfrin:** Verified. `MembershipERC1155` now uses upgradeable versions of OpenZeppelin contracts. OpenZeppelin library version upgraded as well.
