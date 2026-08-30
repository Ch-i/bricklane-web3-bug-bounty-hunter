---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: '`SablierBob::enter` can be temporarily bricked for adapter vaults when STETH
  is paused'
vuln_class: []
---

# `SablierBob::enter` can be temporarily bricked for adapter vaults when STETH is paused

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** The `SablierBob::enter` function calls the `SablierLidoAdapter::stake` function.

```solidity
if (address(vault.adapter) != address(0)) {
            // Interaction: Transfer token from caller to the adapter.
            vault.token.safeTransferFrom(msg.sender, address(vault.adapter), amount);

            // Interaction: stake the tokens via the adapter.
            vault.adapter.stake(vaultId, msg.sender, amount);
```

In case of the `SablierLidoAdapter`, the function calls `STETH::submit` that reverts when either staking is paused or the staking limit is exceeded. In such a case, users cannot enter vaults utilizing this adapter.

```solidity
        require(!stakeLimitData.isStakingPaused(), "STAKING_PAUSED");

        if (stakeLimitData.isStakingLimitSet()) {
            uint256 currentStakeLimit = stakeLimitData.calculateCurrentStakeLimit();
            require(_amount <= currentStakeLimit, "STAKE_LIMIT");
```

A similar instance exists for the withdrawal flow. The `SablierLidoAdapter::_wstETHToWeth` function performs an unwrap on the `wstETH` contract, which transfers `stETH` to the adapter. Since `stETH` transfers can be paused, this would prevent users from exiting within the grace period or redeeming when the vault has settled or expired.

```solidity
function _transferShares(address _sender, address _recipient, uint256 _sharesAmount) internal {
        require(_sender != address(0), "TRANSFER_FROM_ZERO_ADDR");
        require(_recipient != address(0), "TRANSFER_TO_ZERO_ADDR");
        require(_recipient != address(this), "TRANSFER_TO_STETH_CONTRACT");
        _whenNotStopped();
```

**Recommended Mitigation:** Consider notifying users on the user interface about such temporary vault entry restrictions. In case of a prolonged restriction, it is recommended to update the default adapter for the token to `address(0)`. This would allow users to utilize the Bob protocol without involving adapters for yield generation.

**Sablier:** Acknowledged; we will notify users in the UI.

\clearpage
