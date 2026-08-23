---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-05-21-daoventures-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2021-05-21T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md
tags:
- firm:zokyo
- report:2021-05-21-daoventures
title: Unlimit mint in DVGToken.sol
vuln_class: []
---

# Unlimit mint in DVGToken.sol

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-05-21-DAOventures.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md)_

---

**Description**

The contract owner can mint unconditionally tokens to any address.

**Recommendation**:

Add restrictions, if possible. If not, add a comment that briefly explains how users are
protected from unexpected minting.
