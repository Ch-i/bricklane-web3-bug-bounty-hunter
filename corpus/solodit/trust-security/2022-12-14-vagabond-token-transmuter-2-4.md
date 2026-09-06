---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-14-vagabond-token-transmuter-2-4
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
title: TRST-L-5 transmute functions may charge input tokens but not allocate any output
  tokens
vuln_class: []
---

# TRST-L-5 transmute functions may charge input tokens but not allocate any output tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-14-Vagabond Token Transmuter.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md)_

---

**Description:** 
`transmuteInstant()` calculates and distributes allocation like so:
```solidity
        uint256 allocation = (_inputTokenAmount * instantMultiplier) / 
             tokenDecimalDivider;
        …
        IERC20(inputTokenAddress).transferFrom(msg.sender, address(0), 
                _inputTokenAmount);
        SafeERC20.safeTransfer(IERC20(outputTokenAddress), msg.sender, 
        allocation);
```
The issue is that allocation result could be zero due to division by tokenDecimalDivider
which trims many decimal points. If user does not provide a sufficient input amount, 
allocation will be zero but the function won't revert. Therefore, function will charge user the 
input amount but not give in return any output amount. The issue repeats in 
`transmuteLinear()`. It is not severe because if allocation is zero, input amount was probably 
quite small, but still important to address for user experience.

**Recommended mitigation:**
If allocation amount is calculated to be zero, revert in transmute functions.

**Team response:**
Issue was fixed

**Mitigation review:**
Successful fix
