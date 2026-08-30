---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-14-vagabond-token-transmuter-2-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-12-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md
tags:
- firm:trust-security
- report:2022-12-14-vagabond-token-transmuter
title: TRST-L-6 emergencyPull introduces substantial risks
vuln_class: []
---

# TRST-L-6 emergencyPull introduces substantial risks

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-14-Vagabond Token Transmuter.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md)_

---

The **emergencyPull()** function is only callable by owner, and transfers the entire output 
token balance to a controlled destination. Use of **emergencyPull()** will make any linear 
vesting be cancelled without refund to the user. It is recommended that only the non allocated output tokens can be transferred out, as done in **outputTokenPull()**. Additionally, 
project should make sure the multisig address has a timelock in order to further protect 
users from compromised owner scenarios.

**Mitigation review:**
The fix adds a check that remaining balance is greater than the required balance, but 
actually transfers the entire output token balance. It should transfer out only the delta.
Therefore, the previous issue still exists.
```solidity
        uint256 outputTokenBalance = 
             IERC20(outputTokenAddress).balanceOf(address(this));
                uint256 vestingRequiredBalance = totalAllocatedOutputToken -
        totalReleasedOutputToken;
        require(outputTokenBalance > vestingRequiredBalance, 
            "NO_UNALLOCATED_TOKENS");
        SafeERC20.safeTransfer(IERC20(outputTokenAddress), 
             _emergencyOutputDestination, 
        IERC20(outputTokenAddress).balanceOf(address(this)));
```
