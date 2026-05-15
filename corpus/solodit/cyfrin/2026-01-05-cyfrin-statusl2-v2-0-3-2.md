---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-3-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: '`totalMPAccrued` accrual should start from first stake'
vuln_class: []
---

# `totalMPAccrued` accrual should start from first stake

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** The StakeManager contract initializes `lastMPUpdatedTime` to `block.timestamp` during deployment. This timestamp is used to calculate MP accrual periods in the `StakeManager::_totalMP` function. However, when the first user stakes, `lastMPUpdatedTime` is not updated to the current timestamp due to a logic flaw in `StakeManager::_updateGlobalMP`.

During first stake it doesn't update `lastMPUpdatedTime`, because this line lies under condition `if (newTotalMPAccrued > totalMPAccrued)` which is false because before first stake MP are 0:

```solidity
    function stake(
        uint256 amount,
        uint256 lockPeriod,
        uint256 currentLockUntil
    )
        external
        onlyNotEmergencyMode
        whenNotPaused
        onlyTrustedCodehash
        onlyRegisteredVault
        returns (uint256 newLockUntil)
    {
        if (amount == 0) {
            revert StakeManager__AmountCannotBeZero();
        }

@>      _updateGlobalState();
        _updateVault(msg.sender, true);
        ...
    }

    function _updateGlobalState() internal virtual {
@>      _updateGlobalMP();
        _updateRewardIndex();
    }

    function _updateGlobalMP() internal {
        uint256 newTotalMPAccrued = _totalMP();
@>      if (newTotalMPAccrued > totalMPAccrued) {
            totalMPAccrued = newTotalMPAccrued;
            lastMPUpdatedTime = block.timestamp;
        }
    }
```
 Suppose following scenario:
1) Contract is deployed and initialized
2) After 0.5 year there is first stake
3) 1 year passes
4) `totalMPAccrued` will contain extra amount equal to `firstStakeAmount * 0.5 year`

**Impact:** Turns out variable `totalMPAccrued` is not used on-chain, so there is no meaningful impact.

**Proof of Concept:** Paste into `status-network-contracts/test/stake-manager/MPAccrualAfterDelayTest.t.sol`, execute with `forge test --match-test test_MPAccrualIncludesTimeBeforeFirstStake -vvv`
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import { StakeManagerTest } from "./StakeManagerBase.t.sol";
import { MultiplierPointMath } from "../../src/math/MultiplierPointMath.sol";

contract MPAccrualAfterDelayTest is StakeManagerTest {
    function setUp() public virtual override {
        super.setUp();
    }

    /**
     *
     * Scenario:
     * 1. Contract is initialized at T0, lastMPUpdatedTime = T0
     * 2. 1 year passes (no one stakes)
     * 3. At T1 (T0 + 1 year) Alice makes the first stake
     * 4. During first stake, lastMPUpdatedTime does NOT update to T1 (remains T0)
     *    Reason: totalMaxMP == 0, so _totalMP() returns totalMPAccrued (0)
     *            and condition (newTotalMPAccrued > totalMPAccrued) is false
     * 5. Another 1 year passes
     * 6. At T2 (T0 + 2 years) update is called
     * 7. MP accrues for period (T2 - T0) = 2 years instead of (T2 - T1) = 1 year
     */
    function test_CRITICAL_MPAccrualIncludesTimeBeforeFirstStake() public {
        uint256 stakeAmount = 1000e18;
        uint256 YEAR = 365 days;

        uint256 initTime = block.timestamp;

        vm.warp(block.timestamp + YEAR);
        uint256 firstStakeTime = block.timestamp;

        _stake(alice, stakeAmount, 0);

        // lastMPUpdatedTime did not update to first stake time
        assertEq(
            streamer.lastMPUpdatedTime(),
            initTime
        );

        uint256 expectedInitialMP = stakeAmount;

        vm.warp(block.timestamp + YEAR);
        uint256 updateTime = block.timestamp;

        _updateVault(alice);

        // Calculate expected MP
        uint256 mpFor1Year = MultiplierPointMath._accrueMP(stakeAmount, YEAR);
        uint256 expectedTotalMP = expectedInitialMP + mpFor1Year;

        // Calculate actual MP
        uint256 mpFor2Years = MultiplierPointMath._accrueMP(stakeAmount, updateTime - initTime);
        uint256 wrongTotalMP = expectedInitialMP + mpFor2Years;

        // MP accrued for 2 years instead of 1 year
        assertEq(
            streamer.totalMPAccrued(),
            wrongTotalMP,
            "BUG: MP accrued for 2 years (since init) instead of 1 year (since first stake)"
        );

        emit log_named_uint("Expected MP after 1 year", expectedTotalMP);
        emit log_named_uint("Actual MP (wrong)", wrongTotalMP);
        emit log_named_uint("Overcount (MP for extra year)", wrongTotalMP - expectedTotalMP);
        emit log_named_uint("Time since init (2 years)", updateTime - initTime);
        emit log_named_uint("Time since first stake (1 year)", updateTime - firstStakeTime);
    }
}

```

**Recommended Mitigation:** Always update `lastMPUpdatedTime`:
```diff
    function _updateGlobalMP() internal {
        uint256 newTotalMPAccrued = _totalMP();
+       lastMPUpdatedTime = block.timestamp;
        if (newTotalMPAccrued > totalMPAccrued) {
            totalMPAccrued = newTotalMPAccrued;
-           lastMPUpdatedTime = block.timestamp;
        }
    }
```

Or use same pattern as in `_updateVault`, i.e. send flag `bool forceMPUpdate`:
```solidity
    function _updateVault(address vaultAddress, bool forceMPUpdate) internal virtual {
        ...
@>      if (accruedMP > 0 || forceMPUpdate) {
            vault.mpAccrued += accruedMP;
@>          vault.lastMPUpdateTime = block.timestamp;
            totalMPStaked += accruedMP;
        }
    }
```

**StatusL2:** Fixed in [56a7b64](https://github.com/status-im/status-network-monorepo/commit/56a7b64a782150b2a87563621212b076e35f84f5).

**Cyfrin:** Verified.
