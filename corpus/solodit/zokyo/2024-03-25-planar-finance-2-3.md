---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-2-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Cache the `_tokens` length
vuln_class: []
---

# Cache the `_tokens` length

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Status**:  Unresolved

**Severity**: Informational

**Source**: BalanceFetcher.sol

**Description**:

Cache the value of `_tokens.length` to save gas as its a Calldata not memory
```solidity
 for(uint256 i = 0; i < _tokens.length; i++) {
            if(!isContract(_tokens[i])) {
                continue;
            }
            try IERC20(_tokens[i]).balanceOf(_owner) returns(uint256 balance) {
                balances[i] = balance;
            } catch {}
        }
```
