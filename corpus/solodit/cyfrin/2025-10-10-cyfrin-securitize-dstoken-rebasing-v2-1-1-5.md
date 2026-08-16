---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-1-5
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
title: '`euRetailInvestorsCount` is susceptible to underflow when transferring tokens
  between retail and qualified investors of the same country on the EU region'
vuln_class: []
---

# `euRetailInvestorsCount` is susceptible to underflow when transferring tokens between retail and qualified investors of the same country on the EU region

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** The root cause of this problem is that a qualified EU investor with tokens on its balance would not increment the `euRetailInvestorsCount` when the investor is downgraded to a retail investor.
This puts the system in an inconsistent state. The qualified investor could've received tokens while he was qualified, and after he is downgraded to retail, he transfers all of his balance to another investor. This will cause the `euRetailInvestorsCount` to be decremented because a retail investor is no longer a holder.
- This problem occurs because the qualified investor was downgraded to retail while he had tokens on his balance, but the `euRetailInvestorsCount` was not incremented.

```solidity
    function adjustInvestorsCountsByCountry(
        ...
    ) internal {
        ...
//@audit-info => euRetailInvestorsCount are not modified for Qualified EU Investors
        } else if (countryCompliance == EU && !getRegistryService().isQualifiedInvestor(_id)) {
            if(_increase == CommonUtils.IncDec.Increase) {
                euRetailInvestorsCount[_country]++;
            }
            else {
                euRetailInvestorsCount[_country]--;
            }
        }
        ...
    }
```

As is demonstrated on the PoC, the `euRetailInvestorsCount` for France is messed up in a scenario as shown below:
1. A French retail EU investor transfers some of its balance (partial transfer) to a qualified (non-retail) French investor
2. The qualified French investor becomes retail and transfers all of its balance back to the French retail investor1
    - Here, the `euRetailInvestorsCount` will be messed up
3. The retail French investor1 attempts to transfer all of its balance out and gets an underflow because the retail counter for France is already 0.

**Impact:** In addition to the risk of reaching the status of underflow, the `euRetailInvestorsCount` will be off from the real number of investors that should be tracked.

**Proof of Concept:** Add the next PoC to `dstoken-regulated.test.ts` test file
```js
    it.only('underflow on euRetailInvestorsCount PoC', async function () {
      const [investor, investor2, usInvestor] = await hre.ethers.getSigners();
      const { dsToken, registryService, complianceService, complianceConfigurationService } = await loadFixture(deployDSTokenRegulated);
      await complianceConfigurationService.setCountryCompliance(INVESTORS.Country.FRANCE, INVESTORS.Compliance.EU);
      await complianceConfigurationService.setEURetailInvestorsLimit(10);
      await registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, investor, registryService);
      await registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_2, investor2, registryService);
      await registerInvestor(INVESTORS.INVESTOR_ID.US_INVESTOR_ID, usInvestor, registryService);
      await registryService.setCountry(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, INVESTORS.Country.FRANCE);
      await registryService.setCountry(INVESTORS.INVESTOR_ID.INVESTOR_ID_2, INVESTORS.Country.FRANCE);
      await registryService.setCountry(INVESTORS.INVESTOR_ID.US_INVESTOR_ID, INVESTORS.Country.USA);

      //@audit-info => Set investor2 as a qualified investor!
      await registryService.setAttribute(INVESTORS.INVESTOR_ID.INVESTOR_ID_2, 4, 1, 0, 'abcde');

      await dsToken.issueTokens(investor, 500);
      const valueToTransfer = 100;

      //@audit-info => a retail EU investor transfers to a qualified (non-retail) EU investor
      const dsTokenFromInvestor = await dsToken.connect(investor);
      await dsTokenFromInvestor.transfer(investor2, valueToTransfer);
      expect(await complianceService.getEURetailInvestorsCount(INVESTORS.Country.FRANCE)).equal(1);

      //@audit-info => Set investor2 as retail investor - non-qualified!
      await registryService.setAttribute(INVESTORS.INVESTOR_ID.INVESTOR_ID_2, 4, 0, 0, 'abcde');
      const dsTokenFromInvestor2 = await dsToken.connect(investor2);
      //@audit-info => The old qualified investor, currently retail, transfers all its balance to another retail EU investor
      await dsTokenFromInvestor2.transfer(investor, valueToTransfer);
      expect(await complianceService.getEURetailInvestorsCount(INVESTORS.Country.FRANCE)).equal(0);

      //@audit-info => investor1 tries to transfer all of its balance to an investor on another country and reverts bcs of underflow on euRetailInvestorsCount
      await expect(dsTokenFromInvestor.transfer(usInvestor, 500)).to.be.reverted;
    });
```

**Recommended Mitigation:** Consider incrementing the `euRetailInvestorsCount` when converting a qualified EU investor to a retail EU investor, and such an investor has an investorBalance.

**Securitize:** Acknowledged; it is not realistic to account for changes between qualified and not qualified statuses. Implementing this logic would add complexity to investor and attribute updates and in any case can be solved operationally.
