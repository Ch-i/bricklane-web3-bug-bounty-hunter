---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-4-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: '`LibBytes::packAddressAndStem` calculated twice with the same parameters'
vuln_class: []
---

# `LibBytes::packAddressAndStem` calculated twice with the same parameters

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

`LibSilo::_removeDepositsFromAccount` [calls](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibSilo.sol#L597) `LibBytes::packAddressAndStem` after `LibTokenSilo::removeDepositFromAccount` has [already called](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibTokenSilo.sol#L239) the same function with the same parameters.

Consider refactoring to calculate `LibBytes::packAddressAndStem` once for each loop iteration in `LibSilo::_removeDepositsFromAccount`, then pass the result as a parameter in the call to `LibTokenSilo::removeDepositFromAccount`.
