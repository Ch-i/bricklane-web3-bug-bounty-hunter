---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-0-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Tokens can get stuck while calling deposit()
vuln_class: []
---

# Tokens can get stuck while calling deposit()

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In contract FEYTraderJoeProduct, 
If msg.value != 0 AND address(trancheConfig[_tranche].tokenAddress) != nativeToken, when calling the deposit() and depositFor() functions, it will result in the user's funds being stuck in the contract. It is advised to refund this amount in case the user sends AVAX and the tranchtokenAddress is not nativeToken.

The same issue also exists in the _makeInitialDeposit() function of the factory contract.

**Recommendation**: 

It is advised to add mechanisms in the contract to allow investors from withdrawing their stuck tokens in the contract. Or else refund the tokens immediately in case the tokens are stuck while calling the function.
