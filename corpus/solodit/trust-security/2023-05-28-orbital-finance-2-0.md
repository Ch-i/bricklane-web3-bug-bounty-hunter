---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: TRST-L-1 Several popular ERC20 tokens are incompatible with the vault due to
  MAX approve
vuln_class: []
---

# TRST-L-1 Several popular ERC20 tokens are incompatible with the vault due to MAX approve

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

**Description:**
There are several instances where the vault approves use of funds to the manager or a trade 
router. It will set approval to MAX_UINT256. 
```solidity
         for (uint i = 0; i < tokens.length; i++) {
         //allow vault manager to withdraw tokens
                   IERC20(tokens[i]).safeIncreaseAllowance(ownerIn, 
         type(uint256).max); 
         }
```
The issue is that there are several popular tokens(https://github.com/d-xo/weird-erc20#revert-on-large-approvals--transfers) (UNI, COMP and others) which do not 
support allowances of above UINT_96. The contract will not be able to interoperate with 
them.

**Recommended Mitigation:**
Consider setting allowance to UINT_96. Whenever the allowance is consumed, perform re-approval up to UINT_96.

**Team Response:**
"Changed all allowance increases to type(uint96).max"

**Mitigation review:**
Fix is correct.
