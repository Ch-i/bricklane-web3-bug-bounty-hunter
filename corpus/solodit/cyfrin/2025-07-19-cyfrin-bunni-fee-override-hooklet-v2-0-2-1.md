---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-19-cyfrin-bunni-fee-override-hooklet-v2-0-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-19-cyfrin-bunni-fee-override-hooklet-v2-0
title: Outdated reference to rebalance in `IHooklet::afterSwap` should be removed
vuln_class: []
---

# Outdated reference to rebalance in `IHooklet::afterSwap` should be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md)_

---

**Description:** There is an outdated reference to rebalance in the `IHooklet::afterSwap` dev comment which should be removed given `IHooklet::afterRebalance` has since been added:

```solidity
    /// @notice Called after a swap operation.
@>  /// @dev Also called after a rebalance order execution, in which case returnData will only have
@>  /// inputAmount and outputAmount filled out.
    /// @param sender The address of the account that initiated the swap.
    /// @param key The Uniswap v4 pool's key.
    /// @param params The swap's input parameters.
    /// @param returnData The swap operation's return data.
    function afterSwap(
        address sender,
        PoolKey calldata key,
        IPoolManager.SwapParams calldata params,
        SwapReturnData calldata returnData
    ) external returns (bytes4 selector);
```

**Bacon Labs:** Fixed in commit [0189567](https://github.com/Bunniapp/bunni-v2/pull/135/commits/018956782d344d0d5e27a0fc193872dce430e1a4).

**Cyfrin:** Verified. The reference has been removed.
