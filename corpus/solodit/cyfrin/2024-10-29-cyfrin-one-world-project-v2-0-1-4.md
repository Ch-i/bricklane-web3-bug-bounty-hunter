---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-1-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: No membership restrictions placed on `PRIVATE` DAOs allows anyone to join
vuln_class: []
---

# No membership restrictions placed on `PRIVATE` DAOs allows anyone to join

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** [`MembershipDAOStructs::DAOType`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/libraries/MembershipDAOStructs.sol#L6-L10) exposes the different types a DAO can have, namely `PRIVATE`, `SPONSORED`, and the default `PUBLIC` which has no restrictions. DAOs of type `SPONSORED` are open but require the use of all tiers, and while `PRIVATE` may be expected to impose further limitations on membership, this case is not handled and so it is possible for anyone to join these DAOs.

**Impact:** Even if a DAO creator specifies `DAOType.PRIVATE`, there is no possibility to place restrictions on which accounts are allowed to join.

**Proof of Concept:** The following test can be added to `describe("Create New DAO Membership")` in `MembershipFactory.test.ts`:
```javascript
it("lets anyone join PRIVATE DAOs", async function () {
  await currencyManager.addCurrency(testERC20.address);

  // DAO membership is private
  DAOConfig.daoType = DAOType.PRIVATE;
  await membershipFactory.createNewDAOMembership(DAOConfig, TierConfig);

  const ensAddress = await membershipFactory.getENSAddress("testdao.eth");
  const membershipERC1155 = await MembershipERC1155.attach(ensAddress);

  await testERC20.mint(addr1.address, ethers.utils.parseEther("20"));
  await testERC20.connect(addr1).approve(membershipFactory.address, ethers.utils.parseEther("20"));

  // but anyone can join
  await expect(membershipFactory.connect(addr1).joinDAO(membershipERC1155.address, 1)).to.not.be.reverted;
});
```

**Recommended Mitigation:** Consider implementing an allowlist option or similar that the creator of a `PRIVATE` DAO can use to enforce membership restrictions.

**One World Project:** There are no intentions to disallow anyone from joining the private DAOs in smart contract, they are just mentioned that way to be obscured from public view in the website.

**Cyfrin:** Acknowledged.
