---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-14-vagabond-token-transmuter-2-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-12-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md
tags:
- firm:trust-security
- report:2022-12-14-vagabond-token-transmuter
title: TRST-L-3 Multiplier implementation causes limited functionality
vuln_class: []
---

# TRST-L-3 Multiplier implementation causes limited functionality

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-14-Vagabond Token Transmuter.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md)_

---

**Description:**
linearMultiplier and instantMultiplier are used to calculate output token amount from input 
token amount in transmute functions. 
```solidity
    uint256 allocation = (_inputTokenAmount * linearMultiplier) / 
        tokenDecimalDivider;
    …
    uint256 allocation = (_inputTokenAmount * instantMultiplier) / 
        tokenDecimalDivider;
```
The issue is that they are uint256 variables and can only multiply _inputTokenAmount, not 
divide it. It results in limited functionality of the protocol as vesting pairs where output 
tokens are valued more than input tokens cannot be used.

**Recommended Mitigation:**
Add a boolean state variable which will describe whether to multiply or divide by the 
multiplier.

**Team response:**
Acknowledged, but will not be fixed at this time as use case does not require division.
