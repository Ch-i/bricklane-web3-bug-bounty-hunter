---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Use correct NatSpec tags
vuln_class: []
---

# Use correct NatSpec tags

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

Uses of `@dev See {IWell.fn}` should be replaced with `@inheritdoc IWell` to inherit the NatSpec documentation from the interface.

**Beanstalk:** Don’t see any instances of `@dev See {IWell.fn}`. Removed similar instances of `See: {IAquifer.fn}`. Looking at the natspec [documentation](https://docs.soliditylang.org/en/v0.7.6/natspec-format.html#inheritance-notes), it says “Functions without NatSpec will automatically inherit the documentation of their base function.” Thus, it seems that adding @inheritdoc tags is unnecessary.

**Cyfrin:** Acknowledged.
