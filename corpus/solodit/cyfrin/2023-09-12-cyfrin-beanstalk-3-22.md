---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-22
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Ambiguous comment in `LibEthUsdOracle::getPercentDifference` NatSpec
vuln_class: []
---

# Ambiguous comment in `LibEthUsdOracle::getPercentDifference` NatSpec

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

The following comment in the NatSpec of [`LibEthUsdOracle::getPercentDifference`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Oracle/LibEthUsdOracle.sol#L80-L83) is ambiguous:
> *Gets the percent difference between two values with 18 decimal precision.*

This function returns a percentage difference with 18 decimal precision but does not necessarily require that the values it takes as argument should be of 18 decimal precision; they should, however, both be of the same precision, which in this case is 6 decimals. It is recommended to reword the comment to make clearer these intentions and behaviours.
