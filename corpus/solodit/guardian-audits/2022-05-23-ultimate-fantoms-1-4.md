---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-1-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md
tags:
- firm:guardian-audits
- report:2022-05-23-ultimate-fantoms
title: UF-10 | Mint Fee Manipulation
vuln_class: []
---

# UF-10 | Mint Fee Manipulation

_Section severity (from Solodit section header): Low_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

Because the `getPrice` function is stepwise, anyone can mint 10 tokens as if they were all in a lower cost bracket while potentially only 1 was.

**Recommendation**

Compute the mint fee for each token, account for mints that traverse the fee increase, or accept the manipulation.

**Resolution**

Ultimate Fantoms: Acknowledged, protocol loss will be minimal if exploited.
