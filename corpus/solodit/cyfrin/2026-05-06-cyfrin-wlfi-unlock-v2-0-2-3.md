---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-2-3
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
title: Redundant `assert` in `WorldLibertyFinancialV3::_electVestingUpdate` after
  self-write
vuln_class: []
---

# Redundant `assert` in `WorldLibertyFinancialV3::_electVestingUpdate` after self-write

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** At the end of `WorldLibertyFinancialV3::_electVestingUpdate`, the function asserts that the registry now has the new `category` that the same transaction just wrote two lines above:

```solidity
VESTER.wlfiSetCategory(_account, newCategory);
REGISTRY.wlfiSetCategory(_account, newCategory);

assert(REGISTRY.getLegacyUserCategory(_account) == newCategory);

emit VestingUpdated(_account, oldCategory, newCategory);
```

`REGISTRY.wlfiSetCategory` unconditionally executes `userInfo.category = _category`, so the postcondition cannot fail under normal control flow:

```solidity
function wlfiSetCategory(address _user, uint8 _category) external {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }

    RegistryStorage storage $ = _getStorage();
    LegacyUser storage userInfo = $.legacyUserMap[_user];
    userInfo.category = _category;

    emit LegacyUserUpdated(_user, userInfo.amount, _category, userInfo.isActivated);
}
```

The only realistic way the assert can trigger is a malicious or upgraded registry implementation, in which case the assert cannot protect the user anyway. The check pays an external call and a storage read every election to verify a value the same transaction just wrote.


**Recommended Mitigation:** Remove the assert.

```diff
     VESTER.wlfiSetCategory(_account, newCategory);
     REGISTRY.wlfiSetCategory(_account, newCategory);

-    assert(REGISTRY.getLegacyUserCategory(_account) == newCategory);
     emit VestingUpdated(_account, oldCategory, newCategory);
```

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.
