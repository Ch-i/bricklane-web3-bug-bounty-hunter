---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-12
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Curators will lose reward for an epoch if they lose ownership of vault after
  epoch but before distribution
vuln_class: []
---

# Curators will lose reward for an epoch if they lose ownership of vault after epoch but before distribution

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The `Rewards` contract calculates and assigns curator shares for each epoch by calling `VaultTokenized(vault).owner()` to determine the curator (vault owner) who should receive rewards. However, this fetches the current owner of the vault at the time of reward distribution, not the owner during the epoch for which rewards are being distributed. Since `VaultTokenized` inherits from `OwnableUpgradeable`, ownership can be transferred at any time using `transferOwnership`. This means that if a vault changes ownership after an epoch ends but before rewards are distributed for that epoch, the new owner will receive the curator rewards for past epochs, even if they were not the owner during those epochs.

**Impact:** Curator rewards for a given epoch can be claimed by the current owner of the vault, regardless of who owned the vault during that epoch. This allows actors to acquire vaults after an epoch ends but before rewards are distributed, enabling them to retroactively claim curator rewards for periods they did not contribute to. The original owner, who was entitled to the rewards for their activity during the epoch, loses their rightful rewards. This undermines the fairness and intended incentive structure of the protocol.

**Proof of Concept:**
1. Change the `MockVault.sol` to:
```solidity
// SPDX-License-Identifier: BUSL-1.1
// SPDX-FileCopyrightText: Copyright 2024 ADDPHO
pragma solidity 0.8.25;

interface IVaultTokenized {
    function collateral() external view returns (address);
    function delegator() external view returns (address);
    function activeBalanceOfAt(address, uint48, bytes calldata) external view returns (uint256);
    function activeSharesOfAt(address, uint48, bytes calldata) external view returns (uint256);
    function activeSharesAt(uint48, bytes calldata) external view returns (uint256);
    function owner() external view returns (address);
}

contract MockVault is IVaultTokenized {
    address private _collateral;
    address private _delegator;
    address private _owner;
    mapping(address => uint256) public activeBalance;
    mapping(uint48 => uint256) private _totalActiveShares;

    constructor(address collateralAddress, address delegatorAddress, address owner_) {
        _collateral = collateralAddress;
        _delegator = delegatorAddress;
        _owner = owner_;
    }

    function collateral() external view override returns (address) {
        return _collateral;
    }

    function delegator() external view override returns (address) {
        return _delegator;
    }

    function activeBalanceOfAt(address account, uint48, bytes calldata) public view override returns (uint256) {
        return activeBalance[account];
    }

    function setActiveBalance(address account, uint256 balance) public {
        activeBalance[account] = balance;
    }

    function owner() public view override returns (address) {
        return _owner;
    }

    function activeSharesOfAt(address account, uint48, bytes calldata) public view override returns (uint256) {
        return 100;
    }

    function activeSharesAt(uint48 timestamp, bytes calldata) public view override returns (uint256) {
        uint256 totalShares = _totalActiveShares[timestamp];
        return totalShares > 0 ? totalShares : 200; // Default to 200 if not explicitly set
    }

    function setTotalActiveShares(uint48 timestamp, uint256 totalShares) public {
        _totalActiveShares[timestamp] = totalShares;
    }

    // Added function to transfer ownership
    function transferOwnership(address newOwner) public {
        require(msg.sender == _owner, "Only owner can transfer ownership");
        require(newOwner != address(0), "New owner cannot be zero address");
        _owner = newOwner;
    }
}
```

2. Add the following test to the `RewardsTest.t.sol`:
```solidity
function test_curatorSharesAssignedToCurrentOwnerInsteadOfHistorical() public {
	uint48 epoch = 1;
	uint256 uptime = 4 hours;

	// Step 1: Setup stakes for epoch 1 to generate curator shares
	_setupStakes(epoch, uptime);

	// Step 2: Get a vault and its initial owner (Owner A)
	address vault = vaultManager.vaults(0);
	address ownerA = MockVault(vault).owner();
	address ownerB = makeAddr("OwnerB");

	// Step 3: Warp to after epoch 1 ends
	uint256 epoch2Start = middleware.getEpochStartTs(epoch + 1);
	vm.warp(epoch2Start);

	// Step 4: Transfer ownership from Owner A to Owner B
	vm.prank(ownerA);
	MockVault(vault).transferOwnership(ownerB);

	// Step 5: Warp to a time when rewards can be distributed (after 2 epochs)
	uint256 distributionTime = middleware.getEpochStartTs(epoch + 3);
	vm.warp(distributionTime);

	// Step 6: Distribute rewards for epoch 1
	address[] memory operators = middleware.getAllOperators();
	vm.prank(REWARDS_DISTRIBUTOR_ROLE);
	rewards.distributeRewards(epoch, uint48(operators.length));

	// Step 7: Verify curator shares assignment
	uint256 curatorShareA = rewards.curatorShares(epoch, ownerA);
	uint256 curatorShareB = rewards.curatorShares(epoch, ownerB);

	assertEq(curatorShareA, 0, "Owner A should have no curator shares for epoch 1");
	assertGt(curatorShareB, 0, "Owner B should have curator shares for epoch 1");

	// Step 8: Owner B claims curator rewards
	vm.prank(ownerB);
	rewards.claimCuratorFee(address(rewardsToken), ownerB);
	uint256 ownerBBalance = rewardsToken.balanceOf(ownerB);
	assertGt(ownerBBalance, 0, "Owner B should have received curator rewards");

	// Step 9: Owner A attempts to claim and reverts
	vm.prank(ownerA);
	vm.expectRevert(abi.encodeWithSelector(IRewards.NoRewardsToClaim.selector, ownerA));
	rewards.claimCuratorFee(address(rewardsToken), ownerA);
}
```

**Recommended Mitigation:** Track and store the owner of each vault at the end of every epoch, and use this historical ownership data when assigning curator shares and distributing rewards. This ensures that curator rewards are always credited to the correct owner for each epoch, regardless of subsequent ownership transfers. Implementing an ownership snapshot mechanism at epoch boundaries or when ownership changes can help achieve this.

**Suzaku:**
Acknowledged.

**Cyfrin:** Acknowledged.
