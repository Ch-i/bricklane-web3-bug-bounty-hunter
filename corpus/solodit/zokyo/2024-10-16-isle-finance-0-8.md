---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-0-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: Incorrect Sharing of ERC20 Allowance State Across Functions in Pool Contract
vuln_class: []
---

# Incorrect Sharing of ERC20 Allowance State Across Functions in Pool Contract

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**: 

In the Pool contract, the ERC20 allowance state of the shares is shared across multiple functions (requestRedeem, redeem, and removeShares), which can lead to potential misuse by a spender in a manner not intended by the owner. Specifically, if a user approves a certain amount of shares to one spender for requestRedeem and later to another spender for redeem, the second spender could mistakenly or maliciously call requestRedeem or removeShares, exploiting the granted allowance.
This scenario demonstrates that sharing approval states across different functionalities introduces complex behavior not originally intended in the ERC20 standard, which is designed primarily for token transfers between wallets. Such complexities necessitate a more robust logic to ensure security and proper handling of ERC20 allowances.

**Recommendation**: 

To mitigate this issue, it is recommended to introduce a new wrapped token in the Pool contract to represent the shares under the custody of the WithdrawalManager. This wrapped token should have its own allowance and transfer mechanisms, separate from the primary ERC20 token. By doing so, the risk of misuse shall be reduced and align the implementation more closely with the original ERC20 standard's intended use case.
 
Since the ways of spending the allowance are clearly defined within the contract, there’s no need to implement a 1:1 allowance control logic like approve() and transferFrom(). For example, if a user approves an allowance to a spender using an external ERC20, we implement transferFrom() within our requestRedeem, redeem, and removeShares functions. This means the user still can’t control what specific actions the spender might take (if the spender is an EOA). However, if the spender is a verified contract (open source), the user can review the function logic to verify the specific actions being executed.
The reason ERC20 requires a 1:1 approve() and spending logic is to maintain compatibility and flexibility. This setup allows other contracts to directly integrate with transferFrom() to use the allowance, ensuring seamless interaction with various external contracts. Within the ERC20 standard itself, the logic is straightforward: one approve() function is directly tied to the specific spending function transferFrom(), which keeps things clean and simple. However, outside of ERC20, the actual action performed still depends on the function being executed in the contract address (CA) spender or, if it’s an EOA, on the spender’s behavior.
.
