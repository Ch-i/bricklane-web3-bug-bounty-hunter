---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-16
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Emit events prior to external interactions
vuln_class: []
---

# Emit events prior to external interactions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

To strictly conform to the [Checks Effects Interactions pattern](https://fravoll.github.io/solidity-patterns/checks_effects_interactions.html), it is recommended to emit events before any external interactions. Implementing this pattern is generally advised to ensure correct migration through state reconstruction, which in this case, it should not be affected given that all instances in `Well.sol` are protected by the `nonReentrant` modifier, but it is still good practice.

**Beanstalk:** Decided not to implement due to the complexity of the change and its optionality.

**Cyfrin:** Acknowledged.
