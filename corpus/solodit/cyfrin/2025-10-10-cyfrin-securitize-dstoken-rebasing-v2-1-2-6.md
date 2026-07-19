---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`TrustService::changeEntityOwner` can overwrite existing `_newOwner` record,
  breaking 1-1 relationship between owners and addresses'
vuln_class: []
---

# `TrustService::changeEntityOwner` can overwrite existing `_newOwner` record, breaking 1-1 relationship between owners and addresses

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `TrustService::changeEntityOwner` can overwrite existing `_newOwner` record, breaking 1-1 relationship between owners and addresses.

**Proof of Concept:** Add PoC to `test/trust-service.test.ts`:
```typescript
    it('overwrite existing owner breaks 1-1 relationship', async function() {
      const [owner, firstOwner, secondOwner] = await hre.ethers.getSigners();
      const { trustService } = await loadFixture(deployDSTokenRegulated);

      // Setup: Create two entities with different owners
      await trustService.setRole(firstOwner, DSConstants.roles.ISSUER);
      await trustService.setRole(secondOwner, DSConstants.roles.ISSUER);

      const entity1 = "Entity1";
      const entity2 = "Entity2";

      const trustServiceFromFirst = await trustService.connect(firstOwner);
      await trustServiceFromFirst.addEntity(entity1, firstOwner);

      const trustServiceFromSecond = await trustService.connect(secondOwner);
      await trustServiceFromSecond.addEntity(entity2, secondOwner);

      // Verify initial state
      expect(await trustService.getEntityByOwner(firstOwner)).equal(entity1);
      expect(await trustService.getEntityByOwner(secondOwner)).equal(entity2);

      // Change entity1 owner from firstOwner to secondOwner
      await trustService.changeEntityOwner(entity1, firstOwner, secondOwner);

      // Bug: secondOwner now owns both entities in the forward mapping
      // but reverse mapping shows only entity1
      expect(await trustService.getEntityByOwner(secondOwner)).equal(entity1);
      // entity2 is now orphaned - no way to find its owner through getEntityByOwner

      // firstOwner has no entity in reverse mapping
      expect(await trustService.getEntityByOwner(firstOwner)).equal("");
    });
```

Run with: `npx hardhat test --grep "overwrite existing owner"`.

**Recommended Mitigation:** Add modifier `onlyNewEntityOwner(_newOwner)` to function `changeEntityOwner`.

**Securitize:** Fixed in commit [6cd6cca](https://github.com/securitize-io/dstoken/commit/6cd6ccae7201082e53befd6364aff8a1f57397f7); the relevant storage slots were deprecated and the associated functions were removed.

**Cyfrin:** Verified.
