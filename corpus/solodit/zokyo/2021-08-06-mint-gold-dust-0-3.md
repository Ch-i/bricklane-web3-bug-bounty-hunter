---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-0-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2021-08-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md
tags:
- firm:zokyo
- report:2021-08-06-mint-gold-dust
title: Explicitly mark visibility of state
vuln_class: []
---

# Explicitly mark visibility of state

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

contracts/OrderBook.sol#20, withdrawAddress
The storage variable has no visibility set. Such an issue is included to the standard auditor s
checklist. Missed visibility may lead to incorrect interaction with the smart contract.

**Recommendation**:
Explicitly mark visibility of state.
