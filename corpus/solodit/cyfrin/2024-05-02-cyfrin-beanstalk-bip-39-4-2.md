---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-4-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: '`LibTokenSilo::stemTipForToken` calculated multiple times with same parameter'
vuln_class: []
---

# `LibTokenSilo::stemTipForToken` calculated multiple times with same parameter

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

`LibTokenSilo::stemTipForToken` is calculated multiple times with the same [parameter](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibSilo.sol#L604) in `LibSilo::_removeDepositsFromAccount`. This wastes gas since `LibTokenSilo::stemTipForToken` is always called with the same `token` parameter during bulk withdrawals, performing 4 SLOAD operations on storage that does not change.

Consider calculating the stem tip once before entering the loop then pass the result as a parameter to `stalkReward()`.

The same issue also occurs in `ConvertFacet::_withdrawTokens`.
