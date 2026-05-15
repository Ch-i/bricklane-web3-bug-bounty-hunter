---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`TrustService::removeRole` doesn''t delete already owned entities so address
  which lost role can still manage existing entities'
vuln_class: []
---

# `TrustService::removeRole` doesn't delete already owned entities so address which lost role can still manage existing entities

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `TrustService::removeRole` doesn't delete entities so address which lost role can still manage existing entities.

**Proof of Concept:** Add PoC to `test/trust-service.test.ts`:
```typescript
    it('Should demonstrate orphaned entity relationships after role removal', async function() {
      const [owner, entityOwner, operator, resource] = await hre.ethers.getSigners();
      const { trustService } = await loadFixture(deployDSTokenRegulated);

      // Step 1: Give entityOwner ISSUER role
      await trustService.setRole(entityOwner, DSConstants.roles.ISSUER);
      expect(await trustService.getRole(entityOwner)).equal(DSConstants.roles.ISSUER);

      // Step 2: Create an entity owned by entityOwner
      const entityName = "TestEntity";
      const trustServiceFromEntityOwner = await trustService.connect(entityOwner);
      await trustServiceFromEntityOwner.addEntity(entityName, entityOwner);

      // Verify entity ownership
      expect(await trustService.getEntityByOwner(entityOwner)).equal(entityName);

      // Step 3: Add operator and resource to the entity
      await trustServiceFromEntityOwner.addOperator(entityName, operator);
      await trustServiceFromEntityOwner.addResource(entityName, resource);

      // Verify operator and resource are linked to entity
      expect(await trustService.getEntityByOperator(operator)).equal(entityName);
      expect(await trustService.getEntityByResource(resource)).equal(entityName);

      // Step 4: Remove entityOwner's ISSUER role
      await trustService.removeRole(entityOwner);
      expect(await trustService.getRole(entityOwner)).equal(DSConstants.roles.NONE);

      // Step 5: Demonstrate the bug - entity relationships still exist
      // These should ideally be cleaned up but they're not:
      expect(await trustService.getEntityByOwner(entityOwner)).equal(entityName);  // Still owns entity!
      expect(await trustService.getEntityByOperator(operator)).equal(entityName);   // Still linked!
      expect(await trustService.getEntityByResource(resource)).equal(entityName);  // Still linked!

      // Step 6: Show the security issue - entityOwner can still manage the entity
      // even without any role
      await expect(
        trustServiceFromEntityOwner.addOperator(entityName, hre.ethers.Wallet.createRandom())
      ).to.not.be.reverted;  // This should fail but doesn't!

      // The onlyEntityOwnerOrAbove modifier still passes because:
      // - entityOwner has NONE role (not MASTER/ISSUER)
      // - But ownersEntities[entityOwner] still equals entityName
      // - So the check passes even though they shouldn't have access
    });
```

**Recommended Mitigation:** When an address loses its role, delete entities it previously owned by clearing the entity ownership mappings.

**Securitize:** Fixed in commit [6cd6cca](https://github.com/securitize-io/dstoken/commit/6cd6ccae7201082e53befd6364aff8a1f57397f7); the relevant storage slots were deprecated and the associated functions were removed.

**Cyfrin:** Verified.
