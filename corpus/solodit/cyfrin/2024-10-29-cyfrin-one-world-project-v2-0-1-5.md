---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-1-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: DAO membership can exceed `MembershipDAOStructs::DAOConfig.maxMembers`
vuln_class: []
---

# DAO membership can exceed `MembershipDAOStructs::DAOConfig.maxMembers`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** The [`MembershipDAOStructs::DAOConfig.maxMembers`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/libraries/MembershipDAOStructs.sol#L18) field is intended as a cap to DAO membership, beyond which should not be exceeded; however, this is currently unused and there is no limit on how many members can join a DAO besides the limit for each respective tier.

**Impact:** Any number of members can join a DAO, limited only by the maximum amount for each tier.

**Proof of Concept:** The following test can be added to `describe("Create New DAO Membership")` in `MembershipFactory.test.ts`:
```javascript
it("can exceed maxMembers", async function () {
  // max members is 1
  DAOConfig.maxMembers = 1;
  await currencyManager.addCurrency(testERC20.address);
  await membershipFactory.createNewDAOMembership(DAOConfig, TierConfig);

  const ensAddress = await membershipFactory.getENSAddress("testdao.eth");
  const membershipERC1155 = await MembershipERC1155.attach(ensAddress);

  await testERC20.mint(addr1.address, ethers.utils.parseEther("20"));
  await testERC20.connect(addr1).approve(membershipFactory.address, ethers.utils.parseEther("20"));
  await testERC20.mint(addr2.address, ethers.utils.parseEther("20"));
  await testERC20.connect(addr2).approve(membershipFactory.address, ethers.utils.parseEther("20"));

  // two members can join
  await expect(membershipFactory.connect(addr1).joinDAO(membershipERC1155.address, 1)).to.not.be.reverted;
  await expect(membershipFactory.connect(addr2).joinDAO(membershipERC1155.address, 1)).to.not.be.reverted;
});
```

**Recommended Mitigation:** Consider validating the amount of members who have joined a DAO and enforce no more than `maxMembers`.

**One World Project:** maxMembers is only for data verification in backend. Updated the value acc to new data. Fixed in [`e60b078`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/e60b078f09d4ed0f1e509f36a2a6d42293815737) and [`510f305`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/510f305e24a89e0815934ab257a413b9e835607f)

**Cyfrin:** Verified. The sum of `tier.amount` cannot surpass `maxMembers` and `tier.amount` is validated when joining.
