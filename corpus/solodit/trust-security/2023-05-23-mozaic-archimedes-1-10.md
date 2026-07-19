---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-1-10
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-M-11 No slippage protection for cross-chain swaps in StargatePlugin
vuln_class: []
---

# TRST-M-11 No slippage protection for cross-chain swaps in StargatePlugin

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
The StargatePlugin calls StargateRouter's swap() function to do a cross-chain swap.
```solidity 
            // Swaps
            IStargateRouter(_router).swap(_dstChainId, _srcPoolId, _dstPoolId, 
                  payable(address(this)), _amountLD, 0, IStargateRouter.lzTxObj(0, 0, "0x"), abi.encodePacked(_to), bytes(""));
``` 
It will pass 0 as the minimum amount of tokens to receive. This pattern is vulnerable to 
sandwich attacks, where the fee or conversion rate is pumped to make the user receive hardly 
any tokens. In Layer Zero, the equilibrium fee can be manipulated to force such losses.

**Recommended mitigation:**
Calculate accepted slippage off-chain, and pass it to the `_swapRemote()` function for 
validation.

**Team response:**
Fixed.

**Mitigation review:**
Affected function has been removed
