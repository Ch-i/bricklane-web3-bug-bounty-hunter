---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Silent failure can occur when delegating to a Diamond Proxy facet with no code
vuln_class: []
---

# Silent failure can occur when delegating to a Diamond Proxy facet with no code

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

**Description:** If the [Diamond proxy delegates](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/Diamond.sol#L35-L55) to an incorrect address or an implementation that has been self-destructed, the call to the "implementation" will return a success boolean despite no code being executed.

**Impact:** In the case of a payable function call with ETH attached, silent failure of the delegatecall to a non-existent implementation can result in this value being permanently lost.

**Proof of Concept:** The *No contract existence check* section of the article [*Good idea, bad design: How the Diamond standard falls short*](https://blog.trailofbits.com/2020/10/30/good-idea-bad-design-how-the-diamond-standard-falls-short/) by [Trail of Bits](https://www.trailofbits.com/) further details this issue.

**Recommended Mitigation:** Consider checking for contract existence when calling an arbitrary contract. Alternatively, in the interest of gas efficiency, only perform this check if the return data size of the call is zero since the opposite result means that some code was executed.
