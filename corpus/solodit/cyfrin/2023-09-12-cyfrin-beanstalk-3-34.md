---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-34
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Contract upgrades must consider that `msg.value` is persisted through `delegatecall`
vuln_class: []
---

# Contract upgrades must consider that `msg.value` is persisted through `delegatecall`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Given that `msg.value` is persisted through `delegatecall`, it is important that future contract upgrades consider the possibility of this behavior being weaponized within loops that may make unsafe use of this value. While this does not appear to be immediately exploitable, there have previously been other variants [discovered in the wild](https://samczsun.com/two-rights-might-make-a-wrong/). To reiterate, special attention must be paid to the implications of additions in any future upgrades that may introduce unsafe use of `msg.value` within loops, especially considering usage with low-level calls in the `DepotFacet`, `FarmFacet`, `Pipeline`, and `LibETH`/`LibWETH`.

\clearpage
