---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-1-9
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Missing Zero-Address Validation for parameters
vuln_class: []
---

# Missing Zero-Address Validation for parameters

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Statue**: Resolved

**Description**

In NarwhatTradingCallbacks contract, there is no zero-address validation constructor parameters. There is also no method to modify these addresses if by mistake set to address(0). 

In TradingStorage contract, setTokens(address _USDT) set the USDT token address and _USDT is not validated for zero-address. 

In LimitOrdersStorage contract, constructor parameters are not validated for zero-addres.There is also no method to modify these addresses if bymistake set address(0). 

In NarwhalReferrals contract, constructor parameters are not validated for zero-address. There is also no method to modify these addresses if by mistake set address(0). 

**Recommendation**: 

Add zero-address validation

**Fixed**: Issue fixed in commit a72e06b
