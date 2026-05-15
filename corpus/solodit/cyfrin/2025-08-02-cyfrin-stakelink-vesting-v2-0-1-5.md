---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-1-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-08-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-02-cyfrin-stakelink-vesting-v2-0
title: '`SDLVesting::claimRESDLRewards()` can be used to drain the entire vesting
  contract balance in edge case'
vuln_class: []
---

# `SDLVesting::claimRESDLRewards()` can be used to drain the entire vesting contract balance in edge case

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:** The `SDLVesting::claimRESDLRewards` function transfers the entire token balance to the beneficiary for each specified reward token. If the admin mistakenly adds SDL token as a reward token in the `RewardsPoolController`, the beneficiary could call `SDLVesting::claimRESDLRewards([sdlToken])` to instantly drain all vested and unvested SDL tokens from the contract, completely bypassing the vesting schedule.

```solidity
    function claimRESDLRewards(address[] calldata _tokens) external onlyBeneficiary {
        sdlPool.withdrawRewards(_tokens);

        for (uint256 i = 0; i < _tokens.length; ++i) {
            IERC20 token = IERC20(_tokens[i]);
            uint256 balance = token.balanceOf(address(this));

            if (balance != 0) {
                token.safeTransfer(beneficiary, balance);
            }
        }
    }
```
This happens because the entire `token.balanceOf(address(this));` is transferred to the beneficiary.

Consider adding a check to prevent SDL token from being claimed as a reward:

```diff
function claimRESDLRewards(address[] calldata _tokens) external onlyBeneficiary {
    sdlPool.withdrawRewards(_tokens);

    for (uint256 i = 0; i < _tokens.length; ++i) {
+       if (_tokens[i] == address(sdlToken)) continue; // Skip SDL token

        IERC20 token = IERC20(_tokens[i]);
        uint256 balance = token.balanceOf(address(this));
        if (balance != 0) {
            token.safeTransfer(beneficiary, balance);
        }
    }
}
```

**Stake.Link:** Fixed in commit [`e458512`](https://github.com/stakedotlink/contracts/commit/e4585124c05137848196d4ca759c3e9d28b963e1)

**Cyfrin:** Verified. `_tokens[i]` now checked to not be equal to `sdlToken`.
