---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-04-01-allianceblock-0-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2021-04-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-04-01-AllianceBlock.md
tags:
- firm:zokyo
- report:2021-04-01-allianceblock
title: Contract AutoStake lets anyone to set initial pool address, that can be exploited
  by setting immediately pool address after deploying/instantiating new contract.
vuln_class: []
---

# Contract AutoStake lets anyone to set initial pool address, that can be exploited by setting immediately pool address after deploying/instantiating new contract.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-04-01-AllianceBlock.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-04-01-AllianceBlock.md)_

---

**Recommendation**:
Allow only contract owner to set initial pool address.
