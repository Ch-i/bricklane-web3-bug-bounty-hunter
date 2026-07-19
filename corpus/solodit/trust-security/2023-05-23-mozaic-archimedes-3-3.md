---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-3-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: Cache invariants
vuln_class: []
---

# Cache invariants

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

In some parts of the codebase, external calls are used to get values at every invocation 
although they are not expected to ever change. For example, the `convertLDtoMD()` function:
```solidity
        function convertLDtoMD(address _token, uint256 _amountLD) public view returns (uint256) {
                    uint8 _localDecimals = IERC20Metadata(_token).decimals();
                        if (MOZAIC_DECIMALS >= _localDecimals) {
                    return _amountLD * (10**(MOZAIC_DECIMALS - _localDecimals));
             } else {
        return _amountLD / (10**(_localDecimals - MOZAIC_DECIMALS));
                 }
         }
```
The token's `decimals()` are fixed. Consider caching them for improved performance.
