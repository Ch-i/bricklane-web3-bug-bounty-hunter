---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: '`StrategyPassiveManagerUniswap` gives ERC20 token allowances to `unirouter`
  but doesn''t remove allowances when `unirouter` is updated'
vuln_class: []
---

# `StrategyPassiveManagerUniswap` gives ERC20 token allowances to `unirouter` but doesn't remove allowances when `unirouter` is updated

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `StrategyPassiveManagerUniswap` gives ERC20 token [allowances](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L745-L748) to `unirouter`:
```solidity
function _giveAllowances() private {
    IERC20Metadata(lpToken0).forceApprove(unirouter, type(uint256).max);
    IERC20Metadata(lpToken1).forceApprove(unirouter, type(uint256).max);
}
```

`unirouter` is inherited from `StratFeeManagerInitializable` which has an external function `setUnirouter` which allows `unirouter` to be [changed](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/beefy/StratFeeManagerInitializable.sol#L127-L130):
```solidity
 function setUnirouter(address _unirouter) external onlyOwner {
    unirouter = _unirouter;
    emit SetUnirouter(_unirouter);
}
```

The allowances can only be removed by [calling](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L726-L729) `StrategyPassiveManagerUniswap::panic` however `unirouter` can be changed any time via the `setUnirouter` function.

This allows the contract to enter a state where `unirouter` is updated via `setUnirouter` but the ERC20 token approvals given to the old `unirouter` are not removed.

**Impact:** The old `unirouter` contract will continue to have ERC20 token approvals for `StratFeeManagerInitializable` so it can continue to spend the protocol's tokens when this is not the protocol's intention as the protocol has changed `unirouter`.

**Recommended Mitigation:** 1) Make `StratFeeManagerInitializable::setUnirouter` `virtual` such that it can be overridden by child contracts.
2) `StrategyPassiveManagerUniswap` should override `setUnirouter` to remove all allowances before calling the parent function to update `unirouter`.

**Beefy:**
Fixed in commit [8fd397f](https://github.com/beefyfinance/experiments/commit/8fd397f54a47c6f305721335b00896938cec13fe).

**Cyfrin:** Verified.
