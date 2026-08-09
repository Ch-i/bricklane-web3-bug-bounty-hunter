---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2021-08-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md
tags:
- firm:zokyo
- report:2021-08-06-mint-gold-dust
title: Provide an error message for require statements
vuln_class: []
---

# Provide an error message for require statements

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

contracts/MGD.sol
Lines: 61, 77, 271, 312, 313, 395, 409, 410, 421, 422, 433, 434
contracts/OrderBook.sol
Lines: 52, 97
All mentioned require statements do not contain error messages. Such an approach affects
the further contract functioning, since any troubleshooting will require a lot of additional
actions.

**Recommendation**:

Provide error messages for required statements.
