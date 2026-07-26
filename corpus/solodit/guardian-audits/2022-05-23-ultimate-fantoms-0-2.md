---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-0-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2022-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md
tags:
- firm:guardian-audits
- report:2022-05-23-ultimate-fantoms
title: UF-3 | Random Manipulation
vuln_class: []
---

# UF-3 | Random Manipulation

_Section severity (from Solodit section header): Medium_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

The `random` function relies on weak sources of pseudo-randomness from only on-chain attributes. A
validator node can manipulate the `block.timestamp` and therefore the random number. Therefore, the
`_sendTo` address can be manipulated in favor of the validator.

**Recommendation**

Utilize the Randomness pattern to obtain on-chain randomness and avoid validator manipulation or
obtain random numbers off-chain through an oracle.

**Resolution**

Ultimate Fantoms: Acknowledged in source code.
