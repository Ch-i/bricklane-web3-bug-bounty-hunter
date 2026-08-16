---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-1-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Changing investor country to the same country inflates investor count erroneously
  triggering max investor errors
vuln_class: []
---

# Changing investor country to the same country inflates investor count erroneously triggering max investor errors

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Changing investor country to the same country inflates investor count.

**Impact:** Inflating the investor count will erroneously trigger `MAX_INVESTORS_IN_CATEGORY` error in `ComplianceServiceRegulated::completeTransferCheck`. This does not require any error on the admin's part since the admin can call `RegistryService::updateInvestor` where the country remains the same but other investor properties are being changed, and this ends up calling `ComplianceServiceRegulated::adjustInvestorCountsAfterCountryChange` and inflating the investor count.

**Proof of Concept:** Add PoC to `test/compliance-service-regulated.test.ts`:
```typescript
    it('Changing to the same country inflates investor count', async function() {
      const [wallet] = await hre.ethers.getSigners();
      const { dsToken, registryService, complianceConfigurationService, complianceService } = await loadFixture(deployDSTokenRegulated);

      // Setup
      await complianceConfigurationService.setCountryCompliance(INVESTORS.Country.USA, INVESTORS.Compliance.US);

      await registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, wallet, registryService);
      await registryService.setAttribute(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, 2, 1, 0, ""); // Make accredited

      // Set initial country and issue tokens
      await registryService.setCountry(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, INVESTORS.Country.USA);
      await dsToken.setCap(1000);
      await dsToken.issueTokens(wallet, 100);

      // Verify initial state: 1 US investor
      expect(await complianceService.getUSInvestorsCount()).to.equal(1);

      // Change country from USA to USA
      await registryService.setCountry(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, INVESTORS.Country.USA);

      // bug: us investor count increased even though it is the same investor
      //      and their country hasn't actually changed
      expect(await complianceService.getUSInvestorsCount()).to.equal(2);
    });
```

Run with: `npx hardhat test --grep "Changing to the same country inflates investor count"`

**Recommended Mitigation:** `ComplianceServiceRegulated::adjustInvestorCountsAfterCountryChange` should revert or simply not adjust anything if `_country` and `_prevCountry` are the same.

The second option (not adjust anything) may be preferred since this can end up being called from an original call to `RegistryService::updateInvestor` where the country remains the same but other investor properties are being changed.

**Securitize:** Fixed in commit [86d4135](https://github.com/securitize-io/dstoken/commit/86d413548c5a41cc662681c1d7a67c8135d808e7) by changing `RegistryService::setCountry` (which calls `ComplianceServiceRegulated::adjustInvestorCountsAfterCountryChange` to not process if the countries are the same.

As part of another issue `ComplianceServiceRegulated::adjustInvestorCountsAfterCountryChange` was also changed to correctly decrement previous country so calling this function directly with identical countries would decrement then increment resulting in no net change to investor counts which is correct.

**Cyfrin:** Verified.
