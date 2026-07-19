---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-swapexchange-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-swapexchange
title: Fee-on-transfer tokens are not supported
vuln_class: []
---

# Fee-on-transfer tokens are not supported

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-swapexchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md)_

---

**Severity:** Medium

**Description:** The protocol intends to support all ERC20 tokens but does not support fee-on-transfer tokens.
The protocol utilizes the functions `TransferUtils::_transferERC20()` and `TransferUtils::_transferFromERC20()` to transfer ERC20 tokens.

```solidity
TransferUtils.sol
34:     function _transferERC20(address token, address to, uint256 amount) internal {
35:         IERC20 erc20 = IERC20(token);
36:         require(erc20 != IERC20(address(0)), "Token Address is not an ERC20");
37:         uint256 initialBalance = erc20.balanceOf(to);
38:         require(erc20.transfer(to, amount), "ERC20 Transfer failed");
39:         uint256 balance = erc20.balanceOf(to);
40:         require(balance >= (initialBalance + amount), "ERC20 Balance check failed");//@audit-issue reverts for fee on transfer token
41:     }
```

The implementation verifies that the transfer was successful by checking that the balance of the recipient is greater than or equal to the initial balance plus the amount transferred. This check will fail for fee-on-transfer tokens because the actual received amount will be less than the input amount. (Read [here](https://github.com/d-xo/weird-erc20#fee-on-transfer) about fee-on-transfer tokens)

Although there are very few fee-on-transfer tokens, the protocol can't say it supports all ERC20 tokens if it doesn't support these weird ERC20 tokens.

**Impact:** Fee-on-transfer tokens can not be used for the protocol.
Because of the rarity of these tokens, we evaluate this finding as a Medium risk.

**Recommended Mitigation:** The transfer utility functions can be updated to return the actually received amount.
Or clearly document that only standard ERC20 tokens are supported.

**Protocol:** We are choosing not to implement this at this stage.

**Cyfrin:** Acknowledged. As recommended, please mention this in user documentation.
