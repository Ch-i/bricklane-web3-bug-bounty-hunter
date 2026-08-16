---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-02-28-cyfrin-stakedotlink-v2-0-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-02-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-02-28-cyfrin-stakedotlink-v2.0.md
tags:
- firm:cyfrin
- report:2025-02-28-cyfrin-stakedotlink-v2-0
title: Unnecessary token transfer when withdrawing reward tokens
vuln_class: []
---

# Unnecessary token transfer when withdrawing reward tokens

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-02-28-cyfrin-stakedotlink-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-02-28-cyfrin-stakedotlink-v2.0.md)_

---

**Description:** When claiming non-LINK reward tokens, the tokens are transferred `Vault -> FundFlowController -> nonLINKRewardReceiver`:

[`Vault::withdrawTokenRewards`](https://github.com/stakedotlink/audit-2025-02-linkpool/blob/046c65a9c771315816bc59533183f52661af8e5e/contracts/linkStaking/base/Vault.sol#L168-L178) transfers to `msg.sender` (`FundFlowController`):
```solidity
function withdrawTokenRewards(address[] calldata _tokens) external onlyFundFlowController {
    for (uint256 i = 0; i < _tokens.length; ++i) {
        IERC20Upgradeable rewardToken = IERC20Upgradeable(_tokens[i]);
        uint256 balance = rewardToken.balanceOf(address(this));
        if (balance != 0) rewardToken.safeTransfer(msg.sender, balance);
    }
}
```

and [`FundFlowController::withdrawTokenRewards`](https://github.com/stakedotlink/audit-2025-02-linkpool/blob/046c65a9c771315816bc59533183f52661af8e5e/contracts/linkStaking/FundFlowController.sol#L312-L323) transfers to the protocol wallet `nonLINKRewardReceiver`:
```solidity
function withdrawTokenRewards(address[] calldata _vaults, address[] calldata _tokens) external {
    for (uint256 i = 0; i < _vaults.length; ++i) {
        IVault(_vaults[i]).withdrawTokenRewards(_tokens);
    }

    for (uint256 i = 0; i < _tokens.length; ++i) {
        IERC20Upgradeable rewardToken = IERC20Upgradeable(_tokens[i]);
        if (address(rewardToken) == linkToken) revert InvalidToken();
        uint256 balance = rewardToken.balanceOf(address(this));
        if (balance != 0) rewardToken.safeTransfer(nonLINKRewardReceiver, balance);
    }
}
```

This could be optimized by letting the vault transfer to `nonLINKRewardReceiver` directly, thus removing one token transfer from the flow:

```solidity
function withdrawTokenRewards(address[] calldata _vaults, address[] calldata _tokens) external {
    // cache linkToken
    address _linkToken = linkToken;

    // check for LINK token
    for (uint256 i = 0; i < _tokens.length; ) {
        if (_tokens[i] == _linkToken) revert InvalidToken();
        unchecked { ++i; }
    }

    for (uint256 i = 0; i < _vaults.length; ++i) {
        // add `nonLINKRewardReceiver` in the call to vault.withdrawTokenRewards
        IVault(_vaults[i]).withdrawTokenRewards(_tokens, nonLINKRewardReceiver);
    }
}
```

```diff
- function withdrawTokenRewards(address[] calldata _tokens) external onlyFundFlowController {
+ function withdrawTokenRewards(address[] calldata _tokens, address _receiver) external onlyFundFlowController {
      for (uint256 i = 0; i < _tokens.length; ++i) {
          IERC20Upgradeable rewardToken = IERC20Upgradeable(_tokens[i]);
          uint256 balance = rewardToken.balanceOf(address(this));
-         if (balance != 0) rewardToken.safeTransfer(msg.sender, balance);
+         if (balance != 0) rewardToken.safeTransfer(_receiver, balance);
      }
  }
```

As `Vault::withdrawTokenRewards` is already protected by `onlyFundFlowController` this poses no extra risk.

**Stake.Link:** Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage
