---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Allowance reset for incorrect token in `SmartVaultYieldManager::_sellUSDC`
vuln_class: []
---

# Allowance reset for incorrect token in `SmartVaultYieldManager::_sellUSDC`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** When swapping `USDC` in `SmartVaultYieldManager::_sellUSDC`, there is an allowance given to the router:

```solidity
IERC20(USDC).safeApprove(uniswapRouter, _balance);
ISwapRouter(uniswapRouter).exactInput(ISwapRouter.ExactInputParams({
    /* snip: swap */
}));
IERC20(USDs).safeApprove(uniswapRouter, 0);
```
Consistent with all other swaps performed in this contract, the allowance is reset after interaction with the router; however, in this instance, the allowance is [incorrectly reset](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L193) to `0` for `USDs` instead of `USDC`.

**Impact:** There can be small `USDC` dust allowances left on the router.

**Recommended Mitigation:** Replace `USDs` with `USDC`:

```diff
  IERC20(USDC).safeApprove(uniswapRouter, _balance);
  ISwapRouter(uniswapRouter).exactInput(ISwapRouter.ExactInputParams({
      /* snip: swap */
  }));
- IERC20(USDs).safeApprove(uniswapRouter, 0);
+ IERC20(USDC).safeApprove(uniswapRouter, 0);
```

**The Standard DAO:** Fixed by commit [`217de3a`](https://github.com/the-standard/smart-vault/commit/217de3a777ec692e3ecc781464d8644814df3ab9).

**Cyfrin:** Verified, approval is now reset for `USDC`.
