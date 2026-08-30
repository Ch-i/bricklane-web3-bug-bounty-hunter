---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2021-08-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md
tags:
- firm:zokyo
- report:2021-08-06-mint-gold-dust
title: Missing zero check during initialization
vuln_class: []
---

# Missing zero check during initialization

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

contracts/OrderBook.sol#48, withdrawAddress
The variable is actively used in the contract, though is not checked against the zero address.
Since there is no ability to change the value and since the initialization is performed only in the
initializer the issue is classified as Low.

**Recommendation**:

Add check that the address is not zero.
