---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-2-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: '`assert` is used to enforce user-reachable invariants in `WorldLibertyFinancialVester`'
vuln_class: []
---

# `assert` is used to enforce user-reachable invariants in `WorldLibertyFinancialVester`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** Solidity's `assert` is documented as a check for conditions that should never be false and triggers a `Panic(0x01)` when it fails. The vester uses `assert` in several places where the condition is actually reachable through normal user or admin actions, not only through impossible internal states:

```solidity
// WorldLibertyFinancialVester.sol#L108-L114
userInfo.allocation -= uint112(_amount); // safe cast
assert(userInfo.claimed <= userInfo.allocation);

$.totalAllocated -= uint112(_amount);
assert($.totalClaimed <= $.totalAllocated);
```

```solidity
// WorldLibertyFinancialVester.sol#L303
assert(_allocation != 0); // This should never be 0
```

```solidity
// WorldLibertyFinancialVester.sol#L341
assert(_segmentCap != 0);
```

```solidity
// WorldLibertyFinancialVester.sol#L362
assert(span != 0);
```

The `assert(userInfo.claimed <= userInfo.allocation)` assertion at L111 is the most important: it fails whenever the caller asks to burn an amount that would push the user's new allocation below what they have already claimed (see L-03). That is a user-reachable condition — the user simply pre-claims under their old category — yet the failure mode is an unnamed panic rather than a descriptive revert.

`_unlockedTotal`'s `assert(_allocation != 0)` is also user-reachable through `claimable(user)` if a fully-burned user ever exists: `_claimable` gates on `!_userInfo.initialized` but not on `_userInfo.allocation == 0`. Under the current V3 logic the allocation cannot be zero while initialized is true (the only burn path burns at most 10%), but this is an implicit invariant held up by every caller rather than an invariant enforced at the function boundary.

**Impact:**
- Worse error surface: panics consume calldata-sized gas and leak no structured information, so operators and off-chain dashboards see a bare `Panic(0x01)` instead of a named error like `BurnExceedsUnclaimed(address,uint112,uint112)` or `AllocationIsZero(address)`.
- Harder to reason about: `assert` conventionally signals "can never happen". Using it for user-reachable conditions masks the fact that these are real edge cases that need explicit handling.

**Recommended Mitigation:** Replace the user-reachable asserts with named `revert`s. Example for `wlfiBurnAllocation` . For `_unlockedTotal`, prefer returning `0` over asserting when `_allocation == 0`, so that `claimable(user)` and `_claim(user)` cannot panic if the allocation is ever zeroed out:

```solidity
function _unlockedTotal(
    VesterStorage storage $,
    uint8 _category,
    uint112 _allocation
) internal view returns (uint256) {
    if (_allocation == 0) {
        return 0;
    }
    uint8 count = $.categoryInfo[_category].templateCount;
    ...
}
```

Keep `assert` only for truly impossible invariants (e.g. proofs that a downstream library has already validated), and document why each remaining `assert` cannot be triggered by any caller-reachable state.

**WLFI:** Acknowledged.
