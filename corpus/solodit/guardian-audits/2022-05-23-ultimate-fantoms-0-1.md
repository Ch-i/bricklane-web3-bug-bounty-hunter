---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md
tags:
- firm:guardian-audits
- report:2022-05-23-ultimate-fantoms
title: UF-2 | Denial-of-Service With Failed Call
vuln_class: []
---

# UF-2 | Denial-of-Service With Failed Call

_Section severity (from Solodit section header): Medium_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

`publicMint` relies on multiple external calls which can fail accidentally or deliberately. If just one consistently fails, users will not be able to mint.

**Recommendation**

Isolate external calls to another transaction(s). `wFTM` allocations could be distributed with a pull-over-push pattern.

**Resolution**

Ultimate Fantoms: Acknowledged, failed transactions can be resubmitted + the chance of a failed call is low.
