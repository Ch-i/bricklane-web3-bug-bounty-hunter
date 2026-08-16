---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-19
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Inaccurate comment in `LibTokenSilo::removeDepositFromAccount` NatSpec should
  be updated
vuln_class: []
---

# Inaccurate comment in `LibTokenSilo::removeDepositFromAccount` NatSpec should be updated

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Legacy Silo v2 Deposits are stored in a [legacy mapping](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/AppStorage.sol#L149), now deprecated but maintained as legacy deposits that have not been migrated remain stored here. [This line](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibTokenSilo.sol#L218) in the `LibTokenSilo::removeDepositFromAccount` NatSpec appears to refer to the legacy deposits mapping and should be updated to the new [Silo v3 deposits](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/AppStorage.sol#L156) stored as a mapping `uint256` to `Deposit`. If this comment already intends to refer to the new deposits mapping, it should be made clear that `[token][stem]` is meant to indicate the concatenation of the token address and stem value to get the deposit identifier used as a key to the mapping.
