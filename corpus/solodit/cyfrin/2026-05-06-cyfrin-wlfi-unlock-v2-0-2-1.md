---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: '`WorldLibertyFinancialRegistry::wlfiBurnAllocation` leaves stale legacy-user
  storage and emits the wrong event when the full allocation is burned'
vuln_class: []
---

# `WorldLibertyFinancialRegistry::wlfiBurnAllocation` leaves stale legacy-user storage and emits the wrong event when the full allocation is burned

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** `WorldLibertyFinancialRegistry::wlfiBurnAllocation` decrements `userInfo.amount` by `_amount` and emits `LegacyUserUpdated`. When `_amount` equals the user's full remaining allocation, the entry is left partially populated in storage (`amount = 0`, but `category` and `isActivated` retain their previous values), and no `LegacyUserRemoved` event is emitted.

```solidity
function wlfiBurnAllocation(address _user, uint256 _amount) external {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }

    RegistryStorage storage $ = _getStorage();
    LegacyUser storage userInfo = $.legacyUserMap[_user];
    userInfo.amount -= uint112(_amount); // safe cast

    emit LegacyUserUpdated(_user, userInfo.amount, userInfo.category, userInfo.isActivated);
}
```

The on-chain view functions are unaffected because every reader gates on `amount != 0`:

- `isLegacyUser` (L157-L162)
- `isLegacyUserAndIsActivated` / `isLegacyUserAndIsNotActivated` (L164-L178)
- `_validateUserAndReturn` (L209-L220)

So from the perspective of on-chain consumers, the user ceases to be a legacy user the moment `amount` reaches zero, and a subsequent `agentBulkInsertLegacyUsers` cleanly overwrites the slot with `isActivated: false` (L115-L119). The concern is off-chain: the contract defines a dedicated `LegacyUserRemoved` event and emits it from  `agentBulkRemoveLegacyUsers` (L145) but not from the burn path, even though burning to zero is semantically the same state transition.

**Impact:** Indexers or monitoring systems that track the legacy-user set by listening to `LegacyUserRemoved` will miss users whose allocations are fully burned, producing a divergent off-chain view of legacy-user membership. The caller also misses the storage-clear gas refund that `agentBulkRemoveLegacyUsers` and `wlfiReallocateFrom` obtain via `delete`.

**Recommended Mitigation:** When the post-decrement amount is zero, delete the entry and emit `LegacyUserRemoved` instead of `LegacyUserUpdated`.

```solidity
function wlfiBurnAllocation(address _user, uint256 _amount) external {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }

    RegistryStorage storage $ = _getStorage();
    LegacyUser storage userInfo = $.legacyUserMap[_user];
    uint112 newAmount = userInfo.amount - uint112(_amount); // safe cast

    if (newAmount == 0) {
        delete $.legacyUserMap[_user];
        emit LegacyUserRemoved(_user);
    } else {
        userInfo.amount = newAmount;
        emit LegacyUserUpdated(_user, newAmount, userInfo.category, userInfo.isActivated);
    }
}
```

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.
