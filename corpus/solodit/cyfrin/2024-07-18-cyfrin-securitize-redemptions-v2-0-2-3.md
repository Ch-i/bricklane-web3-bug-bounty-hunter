---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-2-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Missing validation of `msg.value` in the function `SecuritizeSwap::executePreApprovedTransaction()`
vuln_class: []
---

# Missing validation of `msg.value` in the function `SecuritizeSwap::executePreApprovedTransaction()`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** `SecuritizeSwap` allows anyone to execute pre-approved transactions using the function `SecuritizeSwap::executePreApprovedTransaction`. This function validates that the protocol is not paused and the length of `params` parameter is two and then calls `doExecuteByInvestor()`.
```solidity
SecuritizeSwap.sol
191:         uint256 value = _params[0];
192:         uint256 gasLimit = _params[1];
193:         assembly {
194:             let ptr := add(_data, 0x20)
195:             let result := call(gasLimit, _destination, value, ptr, mload(_data), 0, 0)
196:             let size := returndatasize()
197:             returndatacopy(ptr, 0, size)
198:             switch result
199:             case 0 {
200:                 revert(ptr, size)
201:             }
202:             default {
203:                 return(ptr, size)
204:             }
205:         }
```
Looking at the implementation of `doExecuteByInvestor`, `params[0]` is used as a value to make a call to `_destination`.
But the `params[0]` was NOT validated to be same to the actual `msg.value` and there is no mechanism to refund the excessive value either.
Due to this problem, if the provided `msg.value` is greater than the `params[0]` (which is included in the signed hash), the residual amount of native token is permanently locked in the contract.

**Impact:** We evaluate the impact to be MEDIUM given that it is unlikely the caller makes a call with excessive `msg.value`.

**Recommended Mitigation:** Require the `msg.value` to be the same to `params[0]` or return the excessive amount to the caller.

**Securitize:** Revised the function in commit [b09460](https://bitbucket.org/securitize_dev/securitize-swap/commits/b094604b341123a49c8abbd6e1c3d53d7c102f28). In this case we used OpenZeppelin `Address.functionCall(_destination, _data)` function for non-payable transactions. The msg.value is 0.
Also the `SecuritizeSwap::executePreApprovedTransaction()` function is not payable.

**Cyfrin:** Verified.

\clearpage
