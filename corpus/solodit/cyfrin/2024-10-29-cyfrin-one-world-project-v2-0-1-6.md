---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-1-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: Lowest tier (highest index) membership cannot be upgraded
vuln_class: []
---

# Lowest tier (highest index) membership cannot be upgraded

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** For `SPONSORED` DAOs, members are permitted to upgrade from a lower tier membership to a higher tier by burning two tokens within a call to [`MembershipFactory::upgradeTier`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L135-L144). This logic attempts to [validate](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L140) that the current tier can be upgraded:

```solidity
require(daos[daoMembershipAddress].noOfTiers > fromTierIndex + 1, "No higher tier available.");
```

However, one important detail here to note is that the highest tier membership has the lowest tier index when [referenced](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L140-L142) within `MembershipFactory::upgradeTier`. Hence, the highest tier is denoted by `0` and the lowest tier with the highest index, `6`, meaning that the above validation is off-by-one. `7 > 6 + 1` is `false` and it is not possible to upgrade from the lowest tier (highest index) membership. Also note that attempted upgrades from the highest tier (lowest index) fail only due to a [revert on underflow](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L142) when attempting to mint.

**Impact:** DAO members cannot upgrade the lowest tier memberships to higher tiers.

**Proof of Concept:** The following test can be added to `describe("Upgrade Tier")` in `MembershipFactory.test.ts`:
```javascript
it("cannot upgrade from lowest tier, highest index", async function () {
  const fromTierIndex = 6;
  await testERC20.mint(addr1.address, ethers.utils.parseEther("1000000"));
  await testERC20.connect(addr1).approve(membershipFactory.address, ethers.utils.parseEther("1000000"));

  await membershipFactory.connect(addr1).joinDAO(membershipERC1155.address, fromTierIndex);
  await membershipFactory.connect(addr1).joinDAO(membershipERC1155.address, fromTierIndex);

  // cannot upgrade from highest index, lowest tier, because of off-by-one
  await expect(membershipFactory.connect(addr1).upgradeTier(membershipERC1155.address, fromTierIndex)).to.be.revertedWith("No higher tier available.");
});
```

**Recommended Mitigation:** Remove the `+ 1`:

```diff
-    require(daos[daoMembershipAddress].noOfTiers > fromTierIndex + 1, "No higher tier available.");
+    require(daos[daoMembershipAddress].noOfTiers > fromTierIndex, "No higher tier available.");
```

**One World Project:** Fixed in [`0a94d44`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/0a94d44bd51b69bbaa2a624f545bdebff0785535).

**Cyfrin:** Verified. Comparison is now `>=`.
