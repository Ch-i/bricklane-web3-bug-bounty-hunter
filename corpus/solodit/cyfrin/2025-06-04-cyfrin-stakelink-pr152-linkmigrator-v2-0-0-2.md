---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0-0-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-06-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0
title: Existing Chainlink stakers can skip queue by bypassing migration requirements
vuln_class: []
---

# Existing Chainlink stakers can skip queue by bypassing migration requirements

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md)_

---

**Description:** The purpose of `LINKMigrator` is that users can migrate their existing position from the Chainlink community pool to stake.link vaults, even when the community pool is at full utilization, since vacating a position frees up space. For users without an existing position, a queueing system (`PriorityQueue`) is used to wait for available slots in the community pool.

However, a user with an existing position can exploit this mechanism by faking a migration. By moving their position to another address (e.g., a small contract they control), they can bypass the queue and open a new position in stake.link if space is available.

Migration begins with a call to [`LINKMigrator::initiateMigration`](https://github.com/stakedotlink/contracts/blob/0bd5e1eecd866b2077d6887e922c4c5940a6b452/contracts/linkStaking/LINKMigrator.sol#L79-L92):

```solidity
function initiateMigration(uint256 _amount) external {
    if (_amount == 0) revert InvalidAmount();

    uint256 principal = communityPool.getStakerPrincipal(msg.sender);

    if (principal < _amount) revert InsufficientAmountStaked();
    if (!_isUnbonded(msg.sender)) revert TokensNotUnbonded();

    migrations[msg.sender] = Migration(
        uint128(principal),
        uint128(_amount),
        uint64(block.timestamp)
    );
}
```

Here, the user's principal is recorded. Later, the migration is completed via `transferAndCall`, which triggers [`LINKMigrator::onTokenTransfer`](https://github.com/stakedotlink/contracts/blob/0bd5e1eecd866b2077d6887e922c4c5940a6b452/contracts/linkStaking/LINKMigrator.sol#L100-L117):

```solidity
uint256 amountWithdrawn = migration.principalAmount -
    communityPool.getStakerPrincipal(_sender);
if (amountWithdrawn < _value) revert InsufficientTokensWithdrawn();
```

This compares the recorded and current principal to verify the withdrawal. However, it does not validate that the total staked amount in the community pool has decreased. As a result, a user can withdraw their position, transfer it to a contract they control, and still pass the check, allowing them to deposit directly into stake.link and bypass the queue.

**Impact:** A user with an existing position in the Chainlink community vault can circumvent the queue system and gain direct access to stake.link staking. This requires being in the claim period, having sufficient LINK to stake again, and available space in the Chainlink community vault. It also resets the bonding period, meaning the user would need to wait another 28 days (the Chainlink bonding period at the time of writing) before interacting with the new position. Nevertheless, this behavior could lead to unfair queue-skipping and undermine the fairness of the protocol.

**Proof of Concept:** Add the following test to `link-migrator.ts` which demonstrates the queue bypass by simulating a migration and re-staking via a third contract::
```javascript
it('can bypass queue using existing position', async () => {
  const { migrator, communityPool, accounts, token, stakingPool } = await loadFixture(
    deployFixture
  )

  // increase max pool size so we have space for the extra position
  await communityPool.setMaxPoolSize(toEther(3000))

  // deploy our small contract to hold the existing position
  const chainlinkPosition = (await deploy('ChainlinkPosition', [
    communityPool.target,
    token.target,
  ])) as ChainlinkPosition

  // get to claim period
  await communityPool.unbond()
  await time.increase(unbondingPeriod)

  // start batch transaction
  await ethers.provider.send('evm_setAutomine', [false])

  // 1. call initiate migration
  await migrator.initiateMigration(toEther(1000))

  // 2. unstake
  await communityPool.unstake(toEther(1000))

  // 3. transfer the existing position to a contract you control
  await token.transfer(chainlinkPosition.target, toEther(1000))
  await chainlinkPosition.deposit()

  // 4. transferAndCall a new position bypassing the queue
  await token.transferAndCall(
    migrator.target,
    toEther(1000),
    ethers.AbiCoder.defaultAbiCoder().encode(['bytes[]'], [[encodeVaults([])]])
  )
  await ethers.provider.send('evm_mine')
  await ethers.provider.send('evm_setAutomine', [true])

  // user has both a 1000 LINK position in stake.link StakingPool and chainlink community pool
  assert.equal(fromEther(await communityPool.getStakerPrincipal(accounts[0])), 0)
  assert.equal(fromEther(await stakingPool.balanceOf(accounts[0])), 1000)
  assert.equal(fromEther(await communityPool.getStakerPrincipal(chainlinkPosition.target)), 1000)

  // community pool is full again
  assert.equal(fromEther(await communityPool.getTotalPrincipal()), 3000)
  assert.equal(fromEther(await stakingPool.totalStaked()), 2000)
  assert.deepEqual(await migrator.migrations(accounts[0]), [0n, 0n, 0n])
})
```
Along with `ChainlinkPosition.sol`:
```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.15;

import "./interfaces/IStaking.sol";
import "../core/interfaces/IERC677.sol";

contract ChainlinkPosition {

    IStaking communityPool;
    IERC677 link;

    constructor(address _communityPool, address _link) {
        communityPool = IStaking(_communityPool);
        link = IERC677(_link);
    }

    function deposit() public {
        link.transferAndCall(address(communityPool), link.balanceOf(address(this)), "");
    }
}
```

**Recommended Mitigation:** In `LINKMigrator::onTokenTransfer`, consider validating that the total principal in the community pool has decreased by at least `_value`, to ensure the migration reflects an actual exit from the community pool.

**stake.link:**
Fixed in [`de672a7`](https://github.com/stakedotlink/contracts/commit/de672a77813d507896502c20241618230af1bd85)

**Cyfrin:** Verified. Recommended mitigation was implemented. Community pool total principal is now recorded in `initiateMigration` then compared to the new pool total principal in `onTokenTransfer`.

\clearpage
