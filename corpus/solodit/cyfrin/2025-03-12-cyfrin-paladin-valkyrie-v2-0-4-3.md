---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-4-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Various typographical errors should be fixed
vuln_class: []
---

# Various typographical errors should be fixed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** The following is a list of typographical errors in both the code and documentation that should be fixed.

**Recommended Mitigation:** * `FullRangeHook`:
```diff
contract FullRangeHook is BaseHook, ReentrancyGuard, ITokenizedHook {
    ...
--  /// @notice Erorr raised if the tick spacing is not default
++  /// @notice Error raised if the tick spacing is not default
    error TickSpacingNotDefault();
    ...
}
```

* `MultiRangeHook`:
```diff
contract MultiRangeHook is BaseHook, ReentrancyGuard, ITokenizedHook {
    ...
--  /// @notice Erorr raised if the tick spacing is not default
++  /// @notice Error raised if the tick spacing is not default
    error TickSpacingNotDefault();
    ...
--  /// @notice Fees sotred from collected fees for each Range
++  /// @notice Fees stored from collected fees for each Range
    mapping(PoolId => mapping(RangeId => RangeStoredFees)) public rangesStoredFees;
}
```

* `ValkyrieHooklet`:
```diff
contract ValkyrieHooklet is IHooklet {
    ...

    /*
    This Hooklet needs the following flags in this contract
--  least siginificant bits of the deployement address :
++  least significant bits of the deployment address :
    uint160 internal constant BEFORE_TRANSFER_FLAG = 1 << 11;
    uint160 internal constant AFTER_INITIALIZE_FLAG = 1 << 8;
    uint160 internal constant AFTER_DEPOSIT_FLAG = 1 << 6;
    uint160 internal constant BEFORE_WITHDRAW_FLAG = 1 << 5;
    uint160 internal constant AFTER_SWAP_FLAG = 1;
    */

    constructor(IIncentiveManager _incentiveManager, IBunniHub _bunniHub) {
        incentiveManager = _incentiveManager;
        bunniHub = _bunniHub;
    }
    ...
    /// @inheritdoc IHooklet
    function beforeSwap(
        address,
        PoolKey calldata,
        IPoolManager.SwapParams calldata
    )
        external
        returns (
            bytes4 selector,
--            bool feeOverriden,
++            bool feeOverridden,
            uint24 fee,
            bool priceOverridden,
            uint160 sqrtPriceX96
        )
    {
        return (ValkyrieHooklet.beforeSwap.selector, false, 0, false, 0);
    }

    /// @inheritdoc IHooklet
    function beforeSwapView(
        address,
        PoolKey calldata,
        IPoolManager.SwapParams calldata
    )
        external
        view
        override
        returns (
            bytes4 selector,
--          bool feeOverriden,
++          bool feeOverridden,
            uint24 fee,
            bool priceOverridden,
            uint160 sqrtPriceX96
        )
    {
        return (ValkyrieHooklet.beforeSwap.selector, false, 0, false, 0);
    }
    ...
}
```

* `BaseIncentiveLogic`:
```diff
abstract contract BaseIncentiveLogic is Owner, ReentrancyGuard, IIncentiveLogic {
    ...
--  /// @notice State fo the reward data for an incentivized pool
++  /// @notice State for the reward data for an incentivized pool
    struct RewardData {
        /// @notice Timestamp at which the distribution ends
        uint32 endTimestamp;
        /// @notice Timestamp at which the last update was made
        uint32 lastUpdateTime;
        /// @notice Current rate per second for the distribution
        uint96 ratePerSec;
        /// @notice Last updated reward per token
        uint96 rewardPerTokenStored;
    }
    ...
    /// @notice Event emitted when fees are retrieved
--    event FeesRetreived(address indexed token, uint256 amount);
++    event FeesRetrieved(address indexed token, uint256 amount);
    ...
}
```

* `BasicIncentiveLogic`:
```diff
contract BasicIncentiveLogic is BaseIncentiveLogic {
    ...
    /// @inheritdoc BaseIncentiveLogic
    function depositRewards(IncentivizedPoolId id, address token, uint256 amount, uint256 duration)
        external
        override
        nonReentrant
    {
        ...
        if (endTimestampCache < block.timestamp) {
            ...
        } else {
--          // Calculates the remianing duration left for the current distribution
++          // Calculates the remaining duration left for the current distribution
            uint256 remainingDuration = endTimestampCache - block.timestamp;
            ...
        }

        ...
    }
```

* `BoostedIncentiveLogic`:
```diff
contract BoostedIncentiveLogic is BaseIncentiveLogic {
    ...
--  /// @dev Boostless factor for user whithout boosting power
++  /// @dev Boostless factor for user without boosting power
    uint256 private constant BOOSTLESS_FACTOR = 40;
    }
    ...
    function depositRewards(IncentivizedPoolId id, address token, uint256 amount, uint256 duration)
        external
        override
        nonReentrant
    {
        ...
        if (endTimestampCache < block.timestamp) {
            ...
        } else {
--          // Calculates the remianing duration left for the current distribution
++          // Calculates the remaining duration left for the current distribution
            uint256 remainingDuration = endTimestampCache - block.timestamp;
            ...
        }

        ...
--  /// @dev Updates the boosted balance of an user for an incentivized pool
++  /// @dev Updates the boosted balance of a user for an incentivized pool
    /// @param id Id of the incentivized pool
    /// @param account Address of the user
    function _updateUserBoostedBalance(IncentivizedPoolId id, address account) internal {
        ...
    }
    ...
--  /// @notice Updates the user reward state then the boosted balance of an user for an incentivized pool
++  /// @notice Updates the user reward state then the boosted balance of a user for an incentivized pool
    /// @param id Id of the incentivized pool
    /// @param account Address of the user
    function updateUserBoostedBalance(IncentivizedPoolId id, address account) external nonReentrant {
        ...
    }
}
```

* `TimeWeightedIncentiveLogic`:
```diff
contract TimeWeightedIncentiveLogic is BaseIncentiveLogic {
    /// @notice Event emitted when rewards are withdrawn from a pool
    event RewardsWithdrawn(
--      IncentivizedPoolId indexed id, address indexed token, address indexed recepient, uint256 amount
++      IncentivizedPoolId indexed id, address indexed token, address indexed recipient, uint256 amount
    );
    ...
--  /// @notice Rewards checckpoints for an user
++  /// @notice Rewards checkpoints for an user
    struct RewardCheckpoint {
        /// @notice Timestamp of the checkpoint
        uint128 timestamp;
        /// @notice Duration of the position in the pool
        uint128 duration;
    }
    ...
    function _depositRewards(
        IncentivizedPoolId id,
        address token,
        uint256 amount,
        uint256 duration,
        uint256 requiredDuration,
        RewardType rewardType
    ) internal {
        ...
        if (endTimestampCache < block.timestamp) {
            ...
        } else {
            ...
--          // Calculates the remianing duration left for the current distribution
++          // Calculates the remaining duration left for the current distribution
            uint256 remainingDuration = endTimestampCache - block.timestamp;
            ...
        }

        IncentiveManager(incentiveManager).addPoolIncentiveSystem(id);
        // Sync pool total liquidity if not already done
        if(!poolSynced[id]) {
            _syncPoolLiquidity(id);
            poolSynced[id] = true;
        }

        emit RewardsDeposited(id, token, amount, duration);
    }
    ...
--  function _earnedTimeWeigthed(IncentivizedPoolId id, address token, address account, uint256 newRewardPerToken)
++  function _earnedTimeWeighted(IncentivizedPoolId id, address token, address account, uint256 newRewardPerToken)
        internal
        view
        returns (uint256 earnedAmount, uint256 leftover)
    {
        ...
    }
}
```

* `IncentiveManager`:
```diff
contract IncentiveManager is Owner, ReentrancyGuard {
    using IncentivizedPoolIdLibrary for IncentivizedPoolKey;

    /// @notice Struct representing an Incentive System
    struct IncentiveSystem {
--      /// @notice Address of the Incentive logix
++      /// @notice Address of the Incentive logic
        address system;
        /// @notice Flag to notify the system when a swap occurs
        bool updateOnSwap;
    }
    ...
--  /// @notice Notifies the initialization of a pool buy a listed Hook
++  /// @notice Notifies the initialization of a pool by a listed Hook
    /// @param id PoolId for the given pool
    /// @param lpToken Address of the liquidity token associated with the pool
    function notifyInitialize(PoolId id, address lpToken) external onlyAllowedHooks {
        ...
    }
    ...
--  function notifyAddLiquidty(PoolId id, address lpToken, address account, int256 liquidityDelta)
++  function notifyAddLiquidity(PoolId id, address lpToken, address account, int256 liquidityDelta)
        external
        onlyAllowedHooks
    {
        ...
    }
--  function notifyRemoveLiquidty(PoolId id, address lpToken, address account, int256 liquidityDelta)
++  function notifyRemoveLiquidity(PoolId id, address lpToken, address account, int256 liquidityDelta)
        external
        onlyAllowedHooks
    {
        ...
    }
}
```

* `IncentivesZap`:
```diff
--  /// @title IncetivesZap
++  /// @title IncentivesZap
    /// @author Koga - Paladin
--  /// @notice Contract to claim rewards accross multiple IncentiveLogic contracts
++  /// @notice Contract to claim rewards across multiple IncentiveLogic contracts
    contract IncentivesZap {
        using IncentivizedPoolIdLibrary for IncentivizedPoolKey;

          /// @notice Parameters for claiming incentives
          struct ClaimedParams {
              address source;
              IncentivizedPoolId id;
              address account;
          }

          /// @notice Claims multiple incentives from multiple IncentiveLogic contracts at once
          /// @param params Array of ClaimedParams
          function claimZap(ClaimedParams[] calldata params) external {
              // @gas cheaper not to cache length for calldata array input
              for(uint256 i; i < params.length; i++) {
                  IIncentiveLogic(params[i].source).claimAll(params[i].id, params[i].account, params[i].account);
              }
          }

      }
```

* `ValkyrieSubscriber`:
```diff
      /// @title ValkyrieSubscriber
      /// @author Koga - Paladin
--  /// @notice Subsciber contract to connect UniswapV4 PositionManager with the IncentiveManager
++  /// @notice Subscriber contract to connect UniswapV4 PositionManager with the IncentiveManager
    contract ValkyrieSubscriber is ISubscriber {
        ...
        /// @notice Error emitted when a tokenId is not subscribed
--      error NotSubsribed();
++      error NotSubscribed();
        ...
    }
```

**Paladin:** Fixed by commit [`9272153`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/92721532aafc3a1a287c0acd70b345aaa2753562).

**Cyfrin:** Verified. The errors have been fixed.
