---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-5-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Unnecessary liquidity sync can be removed
vuln_class: []
---

# Unnecessary liquidity sync can be removed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** The `BaseIncentiveLogic::_syncPoolLiquidity` method is used to synchronize the internal liquidity accounting of an incentivized pool in storage for the corresponding logic contract and is only expected to be executed once; however, there are several instances where this has been included when it is unnecessary which wastes gas in each execution.

The only locations where syncs are necessary include:
* After tokens are deposited, the total liquidity must be synced.
* When `BaseIncentiveLogic::notifyBalanceChange` is executed, the user's liquidity must be synced.
* When `BaseIncentiveLogic::notifyTransfer` is executed, both users' liquidity must be synced.

These three instances are already implemented properly in the following snippets:

```solidity
abstract contract BaseIncentiveLogic is Owner, ReentrancyGuard, IIncentiveLogic {
    ...
    function _updateAllUserState(IncentivizedPoolId id, address account) internal virtual {
        if(!userLiquiditySynced[id][account]) {
            _syncUserLiquidity(id, account);
            userLiquiditySynced[id][account] = true;
        }
        ...
    }

    function notifyBalanceChange(IncentivizedPoolId id, address account, uint256 amount, bool increase)
        external
        virtual
        onlyIncentiveManager
    {
        _updateAllUserState(id, account);   // This syncs user's liquidity

        PoolState storage _state = poolStates[id];
        if (increase) {
            _state.totalLiquidity += amount;
            _state.userLiquidity[account] += amount;
        } else {
            _state.totalLiquidity -= amount;
            _state.userLiquidity[account] -= amount;
        }
    }

    function notifyTransfer(IncentivizedPoolId id, address from, address to, uint256 amount)
        external
        virtual
        onlyIncentiveManager
    {
        _updateAllUserState(id, from);      // This syncs from's liquidity
        _updateAllUserState(id, to);        // This syncs to's liquidity

        PoolState storage _state = poolStates[id];
        _state.userLiquidity[from] -= amount;
        _state.userLiquidity[to] += amount;
    }
}
```

```solidity
contract BasicIncentiveLogic is BaseIncentiveLogic {
    function depositRewards(IncentivizedPoolId id, address token, uint256 amount, uint256 duration)
        external
        override
        nonReentrant
    {
        ...
        IncentiveManager(incentiveManager).addPoolIncentiveSystem(id);
        if(!poolSynced[id]) {
            _syncPoolLiquidity(id);
            poolSynced[id] = true;
        }

        emit RewardsDeposited(id, token, amount, duration);
    }
}
```

**Recommended Mitigation:** These following liquidity synchronization can be removed to avoid wasting gas in each execution of the widely used `_updateRewardState()` function:

```diff
abstract contract BaseIncentiveLogic is Owner, ReentrancyGuard, IIncentiveLogic {
    function _updateRewardState(IncentivizedPoolId id, address token, address account) internal virtual {
        // Sync pool total liquidity if not already done
--      if(!poolSynced[id]) {
--          _syncPoolLiquidity(id);
--          poolSynced[id] = true;
--      }

        RewardData storage _state = poolRewardData[id][token];
        uint96 newRewardPerToken = _newRewardPerToken(id, token).toUint96();
        _state.rewardPerTokenStored = newRewardPerToken;

        uint32 endTimestampCache = _state.endTimestamp;
        _state.lastUpdateTime = block.timestamp < endTimestampCache ? block.timestamp.toUint32() : endTimestampCache;

        // Update user state if an account is provided
        if (account != address(0)) {
--          if(!userLiquiditySynced[id][account]) {
--              _syncUserLiquidity(id, account);
--              userLiquiditySynced[id][account] = true;
--          }

            UserRewardData storage _userState = userRewardStates[id][account][token];
            _userState.accrued = _earned(id, token, account).toUint160();
            _userState.lastRewardPerToken = newRewardPerToken;
        }
    }
    ...
}
```

**Paladin:** This was kept, and even if redundant, we want it as an extra security to prevent any edge case scenario where a Hook/Subscriber is added via the Manager and already has existing deposits/liquidity for users, rewards are deposited, and so the `_updateRewardState()` method is not called via `updateUserState()` or a similar method, and the liquidity would not be synced correctly for the user.

**Cyfrin:** Acknowledged.
