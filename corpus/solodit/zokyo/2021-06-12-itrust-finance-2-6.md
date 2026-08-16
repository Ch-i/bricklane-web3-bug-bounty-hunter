---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-2-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Useless boolean return
vuln_class: []
---

# Useless boolean return

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

StakingData.sol, endRound(), addVault() - always return true, which makes the return value
useless.

**Recommendation**:

remove return value.
