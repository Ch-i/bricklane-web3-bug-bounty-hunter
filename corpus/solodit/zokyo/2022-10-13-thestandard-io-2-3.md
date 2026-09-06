---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Excessive admin authority across contracts.
vuln_class: []
---

# Excessive admin authority across contracts.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

All contracts - Admin enjoys too much authority. The general theme of the code is that admin has power to call several functions like set BondingCurve, setCalculator, setTokenManager and more importantly granting roles in all the contracts which leads to enable him to manipulate funds. Some functions can be more highly severe to be left out controlled by one wallet more than other functions.

**Recommendation**

Apply governance / use multisig wallets.

**Re-audit comment**

Unresolved
