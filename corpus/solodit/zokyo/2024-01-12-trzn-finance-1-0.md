---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Use `SafeTransfer` Instead Of Transfer
vuln_class: []
---

# Use `SafeTransfer` Instead Of Transfer

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity** - Medium

**Status** - Resolved

**Description**

In the swapBforA function (SwapOnetoOne_V2.sol) there is a ERC20 transfer taking place at L90 . The return value of the transfer is not checked so it is possible that the transfer fails silently (returning a false ) and the rest of the function executes normally . In that case token balances and fees would be updated without any transfer taking place.

**Recommendation**:

Use safeTransfer or check the return value of the transfer
