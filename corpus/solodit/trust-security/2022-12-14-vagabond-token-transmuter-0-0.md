---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-14-vagabond-token-transmuter-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-12-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md
tags:
- firm:trust-security
- report:2022-12-14-vagabond-token-transmuter
title: TRST-H-1 Linear vesting users may not receive vested amount
vuln_class: []
---

# TRST-H-1 Linear vesting users may not receive vested amount

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2022-12-14-Vagabond Token Transmuter.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md)_

---

**Description:**
TokenTransmuter supports two types of transmutations, linear and instant. In linear, 
allocated amount is released across time until fully vested, while in instant the entire 
amount is released immediately. **transmuteLinear()** checks that there is enough output 
tokens left in the contract before accepting transfer of input tokens.
 ```solidity
        require(IERC20(outputTokenAddress).balanceOf(address(this)) >= 
            (totalAllocatedOutputToken - totalReleasedOutputToken), 
        "INSUFFICIENT_OUTPUT_TOKEN");
             IERC20(inputTokenAddress).transferFrom(msg.sender, address(0), 
        _inputTokenAmount);
 ```
However, `transmuteInstant()` lacks any remaining balance checks, and will operate as long 
as the function has enough output tokens to satisfy the request.

```solidity
        IERC20(inputTokenAddress).transferFrom(msg.sender, address(0), 
             _inputTokenAmount);
        SafeERC20.safeTransfer(IERC20(outputTokenAddress), msg.sender, 
             allocation);
        emit OutputTokenInstantReleased(msg.sender, allocation, 
             outputTokenAddress);
```
As a result, it is not ensured that tokens that have been reserved for linear distribution will 
be available when users request to claim them. An attacker may empty the output balance 
with a large instant transmute and steal future vested tokens of users.

**Recommended Mitigation:**
In transmuteInstant, add a check similar to the one in transmuteLinear. It will ensure 
allocations are kept faithfully.

**Team response:**
Issue was fixed.

**Mitigation review:**
The suggestion has been implemented. transmuteInstant checks that a sufficient balance is 
reserved for future linear vested tokens
