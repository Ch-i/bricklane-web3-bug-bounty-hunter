---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-10-13-gamestattion-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2021-10-13T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-10-13-Gamestattion.md
tags:
- firm:zokyo
- report:2021-10-13-gamestattion
title: The owner will be able to remove the token in the case when the liquidity is
  not zero and when the owner will try to call the adminWithdraw() for the deleted
  token it would be  impossible to withdraw that token from the contract balance.
vuln_class: []
---

# The owner will be able to remove the token in the case when the liquidity is not zero and when the owner will try to call the adminWithdraw() for the deleted token it would be  impossible to withdraw that token from the contract balance.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-10-13-Gamestattion.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-10-13-Gamestattion.md)_

---

**Re-audit**

The issue related to removing the supported tokens was fixed in the function
removeSupportedToken(). The function adminWithdraw() was deleted.
