---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-2-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: '`FiveFiftyRule::_removeFromEntity` will revert or not work in some cases'
vuln_class: []
---

# `FiveFiftyRule::_removeFromEntity` will revert or not work in some cases

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** The marked line in the code below is using the wrong length `len`. It should be `eLen`.

```solidity
    function _removeFromEntity(
        address entity,
        address[] calldata investors
    ) internal {
        uint256 len = investors.length;
        for (uint256 i; i<len; ++i) {
            address[] storage ens = findEntity[investors[i]];
            uint256 eLen = ens.length;
@>          for (uint256 j; j<len; ++j) {
                if (ens[j] == entity) {
                    if (j != eLen-1 && eLen > 1)
                        ens[j] = ens[eLen-1];
                    ens.pop();
                    break;
                }
            }
        }
    }
```

When `len > eLen` this will lead to reverts if the investor is not found when `j < eLen`.
The result is spurious reverts.

**Impact:** Functions impacted by the reverts are  `deleteEntity` and `removeFromEntity`.

For the `removeFromEntity` case it's possible to repeatedly call it where the `investors` parameter is an array of length 1.

However, for the `deleteEntity` cases this is not possible. The `investors` parameter must contain all of the investors in the entity. If it does not then `findEntity` mapping will still contain entries that it shouldn't.

**Proof of Concept:** Add this to `FiveFiftyRuleTest.t.sol`

```
import "forge-std/Test.sol";
```

and also

```solidity
    function test_cyfrin_removeEntity_indexBug() public {
        address user0 = getDomesticUser(0);
        address user1 = getDomesticUser(1);
        address user2 = getDomesticUser(2);
        address entity = getDomesticUser(3);


        address[] memory investors = new address[](3);
        investors[0] = user0;
        investors[0] = user1;
        investors[0] = user2;

        fiveFiftyProxy.createEntity(entity, user0, 1e6, 1_000_000, investors);

        address[] memory investorsToRemove = new address[](2);
        investorsToRemove[0] = user0;
        investorsToRemove[1] = user1;

        // since investorsToRemove.length == 2 and entities.length == 1 we get a revert
        vm.expectRevert(stdError.indexOOBError);
        fiveFiftyProxy.removeFromEntity(entity, investorsToRemove);

    }
```

**Recommended Mitigation:**
```diff
-          for (uint256 j; j<len; ++j) {
+          for (uint256 j; j<eLen; ++j) {
```

**Remora**
Fixed at commit [5ed4324](https://github.com/remora-projects/remora-dynamic-tokens/commit/5ed432479dec26cb1bcb7484e765eb7319f76c0a)

**Cyfrin:** Verified.
