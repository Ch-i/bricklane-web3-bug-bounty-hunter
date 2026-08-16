---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-L-2 Redundant checks in Vault V3
vuln_class: []
---

# TRST-L-2 Redundant checks in Vault V3

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:**
`depositProfitTokenForUsers()` and `withdrawProfit()` contain the following check:
```solidity
    if (block.timestamp <= lastProfitTime) {
       revert NYProfitTakingVault__ProfitTimeOutOfBounds();
          }
```
However, lastProfitTime is only ever set to block.timestamp. Therefore, it can never be 
larger than block.timestamp.

**Recommended Mitigation:**
It would be best in terms of gas costs and logical clarity to change the comparison to !=

**Team Response:**
Rejected. While valid, this change introduced significant errors during hardhat tests. As it 
can not impact production, we have left it as is.
