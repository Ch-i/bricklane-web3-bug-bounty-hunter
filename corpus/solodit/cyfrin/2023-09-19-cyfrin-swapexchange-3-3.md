---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-swapexchange-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-swapexchange
title: Use Custom Errors
vuln_class: []
---

# Use Custom Errors

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-swapexchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md)_

---

Instead of using error strings, to reduce deployment and runtime cost, you should use Custom Errors. This would save both deployment and runtime cost. Read more [here](https://blog.soliditylang.org/2021/04/21/custom-errors/).

```solidity
File: helpers/FeeData.sol

32:         require(feeValue < _feeDenominator, "Fee percentage must be less than 1");

```

```solidity
File: helpers/TransferHelper.sol

20:         require(rewardAddress != address(0), "Reward Address is Invalid");

87:         require(rewardAddress != address(0), "Reward Address is Invalid");

98:         require(rewardHandler.logTokenFee(token, fee), "LogTokenFee failed");

103:         require(rewardHandler.logNativeFee(fee), "LogTNativeFee failed");

```

```solidity
File: libraries/TransferUtils.sol

36:         require(erc20 != IERC20(address(0)), "Token Address is not an ERC20");

38:         require(erc20.transfer(to, amount), "ERC20 Transfer failed");

40:         require(balance >= (initialBalance + amount), "ERC20 Balance check failed");

45:         require(erc20 != IERC20(address(0)), "Token Address is not an ERC20");

47:         require(erc20.transferFrom(from, to, amount), "ERC20 Transfer failed");

49:         require(balance >= (initialBalance + amount), "ERC20 Balance check failed");

54:         require(flag == true, "ETH transfer failed");

```

**Protocol:** Fixed in commit [ffe50aa](https://github.com/SwapExchangeio/Contracts/commit/ffe50aa913d373724ec12bc704387dfaefaab7a5) and [9ba796f](https://github.com/SwapExchangeio/Contracts/commit/9ba796f6ff0161376b254d80db55d3bc33414a30)

**Cyfrin:** Verified.
