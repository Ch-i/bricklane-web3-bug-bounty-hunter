---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: '`calcFee` Would Return Incorrect Value For A Fee-On-Transfer targetToken'
vuln_class: []
---

# `calcFee` Would Return Incorrect Value For A Fee-On-Transfer targetToken

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity** - Low

**Status** - Acknowledged

**Description**

Inside calcFee function of VaultETH_V2 contract if the targetToken is a fee on transfer token then at the transfer on L263 , tokens less than ratioFee + fixedFee would be transferred . In this case the return value ratioFee + fixedFee would be incorrect since lesser tokens were transferred. 
**Client comment**: We are not going to use a fee-on-transfer tokens.
