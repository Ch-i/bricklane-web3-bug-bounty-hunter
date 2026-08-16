---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-05-21-daoventures-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2021-05-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md
tags:
- firm:zokyo
- report:2021-05-21-daoventures
title: Wrong comment in DVGToken.sol
vuln_class: []
---

# Wrong comment in DVGToken.sol

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-05-21-DAOventures.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md)_

---

**Description**

At line 73 there is a comment “Delegate votes from `msg.sender` to `delegatee`”, but actually
delegates function doesn’t delegate anything and doesn’t work with msg.sender. (delegates
does).

**Recommendation**:

Change comment to match actual function behaviour.
