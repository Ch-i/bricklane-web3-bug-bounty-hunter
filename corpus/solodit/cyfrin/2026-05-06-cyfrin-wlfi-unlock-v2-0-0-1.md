---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-0-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: '`ownerSetCategoryEnabled` disable is not enforced in the claim flow, allowing
  users in a disabled category to keep claiming'
vuln_class: []
---

# `ownerSetCategoryEnabled` disable is not enforced in the claim flow, allowing users in a disabled category to keep claiming

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** `ownerSetCategoryEnabled` toggles the per-category `enabled` flag, but the flag is only checked on entry-point functions that *assign* a user to a category — `_activateVest` and `wlfiSetCategory`:

```solidity
//WorldLibertyFinancialVester.sol#L44-L47
function ownerSetCategoryEnabled(uint8 _category, bool _enabled) external onlyWorldLibertyOwner(msg.sender) {
    _getStorage().categoryInfo[_category].enabled = _enabled;
    emit SetCategoryEnabled(_category, _enabled);
}
```

```solidity
//WorldLibertyFinancialVester.sol#L243-L245
function _activateVest(address _user, uint8 _category, uint112 _amount) internal {
    ...
    if (!$.categoryInfo[_category].enabled) {
        revert CategoryNotEnabled(_category);
    }
    ...
}
```

```
//WorldLibertyFinancialVester.sol#L164-L166
function wlfiSetCategory(address _user, uint8 _category) external whenNotPaused {
    ...
    if (!$.categoryInfo[_category].enabled) {
        revert CategoryNotEnabled(_category);
    }
    ...
}
```

The claim path — `_claim` → `_claimable` → `_unlockedTotal` — never reads `$.categoryInfo[_category].enabled`. It only consumes `templateCount` and `categoryTemplates[_category][i]`. Once a user's `UserInfo.category` has been set at activation (when `enabled` was true), the `enabled` flag becomes meaningless for their ongoing claims.

**Impact:** The `enabled` flag does not do what its name and natspec imply:

- Disabling a category via `ownerSetCategoryEnabled(_category, false)` has no effect on any user already assigned to that category; they continue to accrue unlocked amounts according to the templates and can freely call `wlfiClaimFor`.

**Recommended Mitigation:** Enforce the `enabled` flag in the claim flow. The cleanest place is `WorldLibertyFinancialVester::_claimable`, so both external `claimable` views and `_claim` honor it automatically:

```diff
    function _claimable(
        VesterStorage storage $,
        UserInfo memory _userInfo
    ) internal view returns (uint256) {
        if (!_userInfo.initialized) {
            return 0;
        }
+       if (!$.categoryInfo[_userInfo.category].enabled) {
+           return 0;
+       }

        uint256 unlocked = _unlockedTotal($, _userInfo.category, _userInfo.allocation);
        return unlocked > _userInfo.claimed ? unlocked - _userInfo.claimed : 0;
    }
```

If a hard revert is preferred over a silent zero, add the same check in `_claim` and revert with `CategoryNotEnabled(_userInfo.category)` so users get a clear error. Either way, the flag should be enforced consistently so admins have a per-category circuit breaker independent of the global pause.

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.

\clearpage
