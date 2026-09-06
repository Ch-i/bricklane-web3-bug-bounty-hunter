---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-22
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`ComplianceConfigurationService::getWorldWideForceFullTransfer` is not applied
  to US investors'
vuln_class: []
---

# `ComplianceConfigurationService::getWorldWideForceFullTransfer` is not applied to US investors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `ComplianceConfigurationService::getWorldWideForceFullTransfer` function name implies global application across all regions, but the implementation only applies this setting to non-US investors. In the `completeTransferCheck` function, the worldwide setting is checked exclusively in the non-US investor code path, while US investors are only subject to the region-specific `getForceFullTransfer()` setting:
```solidity
 if (_args.fromRegion == US) {
           ...
            }
        } else {
           ...
                IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getWorldWideForceFullTransfer() &&
                _args.fromInvestorBalance > _args.value
            ) { //@audit the getgetWorldWideForceFullTransfer is not being checked for us investor?
                return (50, ONLY_FULL_TRANSFER);
            }
        }

```

This creates a fundamental inconsistency where "worldwide" compliance settings do not actually apply worldwide.

**Impact:** Us investor can bypass `ComplianceConfigurationService::getWorldWideForceFullTransfer` restrictions.

**Proof of Concept:** Run the next proof of concept in `dstoken-regulated.test.ts`
```typescript
describe('Worldwide Force Full Transfer Bug POC', function () {
        it('Should demonstrate that getWorldWideForceFullTransfer is not applied to US investors', async function () {
          const [usInvestor, nonUsInvestor, differentInvestor] = await hre.ethers.getSigners();
          const { dsToken, registryService, complianceService, complianceConfigurationService } = await loadFixture(deployDSTokenRegulatedWithRebasingAndEighteenDecimal);

          // Setup: Register investors
          await registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, usInvestor, registryService);
          await registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_2, nonUsInvestor, registryService);
          await registerInvestor(INVESTORS.INVESTOR_ID.US_INVESTOR_ID_2, differentInvestor, registryService);

          // Set countries
          await registryService.setCountry(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, INVESTORS.Country.USA);
          await registryService.setCountry(INVESTORS.INVESTOR_ID.INVESTOR_ID_2, INVESTORS.Country.GERMANY);
          await registryService.setCountry(INVESTORS.INVESTOR_ID.US_INVESTOR_ID_2, INVESTORS.Country.FRANCE);

          // Set country compliance
          await complianceConfigurationService.setCountryCompliance(INVESTORS.Country.USA, 1); // US = compliant
          await complianceConfigurationService.setCountryCompliance(INVESTORS.Country.GERMANY, 2); // Germany = EU
          await complianceConfigurationService.setCountryCompliance(INVESTORS.Country.FRANCE, 2); // France = EU

          // Set all compliance rules - no limits and short lock period for testing
          await complianceConfigurationService.setAll(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 150, 1, 1, 0], // No investor limits, 1 second lock period
            [false, false, false, false, false] // Disable all compliance checks initially
          );

          // Issue tokens to both investors
          await dsToken.issueTokens(usInvestor.address, 200);
          await dsToken.issueTokens(nonUsInvestor.address, 200);

          // Wait for lock period to expire
          await time.increase(2); // Wait 2 seconds to ensure lock period expires

          // Configure compliance settings
          await complianceConfigurationService.setForceFullTransfer(false); // Disable US-specific force full transfer
          await complianceConfigurationService.setWorldWideForceFullTransfer(true); // Enable worldwide force full transfer

          // Verify balances
          expect(await dsToken.balanceOf(usInvestor.address)).to.equal(200);
          expect(await dsToken.balanceOf(nonUsInvestor.address)).to.equal(200);

          // Non-US investor partial transfer - should fail (correct behavior)
          await expect(
            dsToken.connect(nonUsInvestor).transfer(differentInvestor.address, 100)
          ).to.be.revertedWith('Only full transfer');

           // US investor partial transfer - should succeed due to bug
           await dsToken.connect(usInvestor).transfer(differentInvestor.address, 100);
           expect(await dsToken.balanceOf(usInvestor.address)).to.equal(100);
           expect(await dsToken.balanceOf(differentInvestor.address)).to.equal(100);

        });
      });
```


**Recommended Mitigation:** Ensure `ComplianceConfigurationService::getWorldWideForceFullTransfer` truly applies worldwide by modifying the US investor code path to also check the worldwide setting:.

**Securitize:** Acknowledged; by design.
