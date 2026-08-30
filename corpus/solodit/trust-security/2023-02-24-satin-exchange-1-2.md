---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-M-3 BaseV1Pair could break because of overflow
vuln_class: []
---

# TRST-M-3 BaseV1Pair could break because of overflow

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
In the function _update(), called internally by `mint()`, `burn()` and `swap()`, the following code 
is executed:
```solidity
    uint256 timeElapsed = blockTimestamp - blockTimestampLast;
     // overflow is desired
    if (timeElapsed > 0 && _reserve0 != 0 && _reserve1 != 0) {
      reserve0CumulativeLast += _reserve0 * timeElapsed;
        reserve1CumulativeLast += _reserve1 * timeElapsed;
     }
```
This is forked from UniswapV2 source code, and it’s meant and known to overflow. It works 
fine if solidity < 0.8.0 is used but reverts when solidity >= 0.8.0 is used.
If this happens all the core functionalities of the pool would break, including `mint()`, `burn()`, 
and `swap()`.

**Recommended Mitigation:**
Wrap the operation around an unchecked{} block so that when the variable overflows it 
loops back to 0 instead of reverting.

**Team Response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, the operation has been wrapped around an 
unchecked{} block
