---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2021-08-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md
tags:
- firm:zokyo
- report:2021-08-06-mint-gold-dust
title: Compares to a boolean constant
vuln_class: []
---

# Compares to a boolean constant

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

contracts/MGD.sol#240:
flaggedNFTS[_tokenId] == true
contracts/MGD.sol#52 55:
require(protocolAdmins[_msgSender()] == true)
contracts/MGD.sol#61 64
require(_org.orgAdmin[_msgSender()] == true || protocolAdmins[_msgSender()] == true)
contracts/OrderBook.sol#209
require(order.orderValid == true,Orderbook ERR: order not valid)
Boolean constants can be used directly and do not need to be compared to true or false. Thus
it will perform a minimal gas usage optimization.

**Recommendation**:

Remove comparison to the bool constant and use the statement directly.
