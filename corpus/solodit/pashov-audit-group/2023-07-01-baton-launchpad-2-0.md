---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-07-01-baton-launchpad-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-07-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md
tags:
- firm:pashov-audit-group
- report:2023-07-01-baton-launchpad
title: '[L-01] The `payable` methods in `Nft` can result in stuck ETH'
vuln_class: []
---

# [L-01] The `payable` methods in `Nft` can result in stuck ETH

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-07-01-Baton Launchpad.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md)_

---

Multiple methods in `ERC721AUpgradeable` (for example the overriden `transferFrom`) have the `payable` keyword, which means they can accept ETH. While this is a gas optimization, it can result in ETH getting stuck in the `Nft` contract, as it inherits `ERC721AUpgradeable`. You can override `payable` methods and revert on `msg.value != 0` to protect from this problem.
