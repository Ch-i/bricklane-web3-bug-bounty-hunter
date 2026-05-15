---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: USDT token is settable more than once
vuln_class: []
---

# USDT token is settable more than once

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In TradingStorage.sol - Method setTokens() can set the address of the USDT token more than once. In TradingVaultV2.sol, we have setUSDT() which does not accept resetting the USDT address. Therefore, it is consistent to have the USDT setters in the contracts apply the same scheme.

**Recommendation** 

Reference to USDT better be immutable and set its value on deployment. Or apply the same approach which is already applied in TradingVaultV2.sol in method setUSDT().

**Fix** -  As of  commit a72e06b ,  dev team fixed the issue by making it settable only once on invoking initialize().
