---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-4-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Unused custom errors and constants can be removed
vuln_class: []
---

# Unused custom errors and constants can be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** * `MultiRangeHook` [declares](https://github.com/PaladinFinance/Valkyrie/blob/6b97685d127c97bc369c0613943f45a547d89b18/src/hooks/MultiRangeHook.sol#L68-L69) the `RangeNotCreated()` custom error but it is never used. It would make sense to perform an associated check within `MultiRangeHook::addLiquidity`; however, [validation](https://github.com/PaladinFinance/Valkyrie/blob/6b97685d127c97bc369c0613943f45a547d89b18/src/hooks/MultiRangeHook.sol#L281-L282) is already performed and handled by a revert with the `RangeNotInitialized()` custom error if the corresponding LP token is `address(0)` which covers both cases. Hence, `RangeNotCreated()` may not needed and could be removed.

```solidity
 address lpToken = rangeLpToken[params.range.toId()];
if (lpToken == address(0)) revert RangeNotInitialized();
```

 * The `MAX_INT` constant is similarly declared in `MultiRangeHook` but not used and so can also be removed.

Unlike `FullRangeHook::beforeInitialize` shown below, `MultiRangeHook::beforeInitialize` does not enforce a default tick spacing despite the declaration of the `TickSpacingNotDefault()` custom error that is never actually used.

```solidity
function beforeInitialize(address, PoolKey calldata key, uint160)
    external
    override
    onlyPoolManager
    returns (bytes4)
{
    if (key.tickSpacing != 60) revert TickSpacingNotDefault();
    ...
}
```

If this error is not needed, then it should be removed; otherwise, the necessary validation should be performed.

* The `DistributionEndTooEarly()` custom error is declared in `BasicIncentiveLogic`, `BoostedIncentiveLogic`, and `TimeWeightedIncentiveLogic` but is not used. Instead, it appears that the duration is validated against `MIN_DURATION` with the `InvalidDuration()` error.

* `ConversionUnderflow()` is declared in `ValkyrieSubscriber` but never used.

**Paladin:** Fixed by commit [`2f727a5`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/2f727a58d47199ff7226350ef8573bf79a2064e7).

**Cyfrin:** Verified. Unused errors and constants have been removed.
