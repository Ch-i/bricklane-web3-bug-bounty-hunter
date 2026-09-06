---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-10-13-gamestattion-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-10-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-10-13-Gamestattion.md
tags:
- firm:zokyo
- report:2021-10-13-gamestattion
title: In the function withdraw(), addLiquidity(), adminWithdraw() there is no check
  if the requesting token is supported.
vuln_class: []
---

# In the function withdraw(), addLiquidity(), adminWithdraw() there is no check if the requesting token is supported.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-10-13-Gamestattion.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-10-13-Gamestattion.md)_

---

**Recommendation**:

Add checking if the token is supporting:
require(supportedTokens.contains(tokenAddress_), “Token is not supported”)
