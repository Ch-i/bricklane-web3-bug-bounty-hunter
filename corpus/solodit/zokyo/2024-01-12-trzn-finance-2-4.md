---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-2-4
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
title: Use `.call()` for transferring ETH
vuln_class: []
---

# Use `.call()` for transferring ETH

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In Contract VaultETH_V2, several instances are using payable(...).transfer(...) for sending native tokens to addresses. 
This uses a fixed 2300 gas and gas repricing may break this leading to execution fees not being refunded and being stuck in the contract forever resulting in loss of funds.

**Recommendation**: 

Use `.call()` instead to transfer native tokens with proper reentrancy mitigation.
