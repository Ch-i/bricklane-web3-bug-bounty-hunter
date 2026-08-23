---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-15
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Shadowing of `AppStorage` storage pointer variable `s` in Facets which inherit
  `ReentrancyGuard`
vuln_class: []
---

# Shadowing of `AppStorage` storage pointer variable `s` in Facets which inherit `ReentrancyGuard`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

The `AppStorage` storage pointer variable `s` is [defined in `ReentrancyGuard`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/ReentrancyGuard.sol#L17) as the sole variable in its first storage slot. Both [`MigrationFacet::getDepositLegacy`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/MigrationFacet.sol#L95) and [`LegacyClaimWithdrawalFacet::getWithdrawal`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/SiloFacet/LegacyClaimWithdrawalFacet.sol#L71) shadow this existing declaration within the body of functions relating to legacy deposits/withdrawals. While this does not pose a security risk, it is recommended to remove the shadowed declarations, instead using the storage pointer defined in the inherited contract.
