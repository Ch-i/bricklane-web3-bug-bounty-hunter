---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-16
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
title: Burn and seize functions can be DoS when investor has several wallets that
  they control
vuln_class: []
---

# Burn and seize functions can be DoS when investor has several wallets that they control

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** The `burn` function in `TokenLibrary.sol` checks `walletsBalances[_who]` (individual wallet balance, see the arrow above) instead of `investorsBalances[investorId]` (total investor balance across all wallets). This allows investors with multiple registered wallets to make their tokens unburnable by transferring tokens between their own wallets.

```solidity
function burn(
        TokenData storage _tokenData,
        address[] memory _services,
        address _who,
        uint256 _value,
        ISecuritizeRebasingProvider _rebasingProvider
    ) public returns (uint256) {
        uint256 sharesToBurn = _rebasingProvider.convertTokensToShares(_value);

        require(sharesToBurn <= _tokenData.walletsBalances[_who], "Not enough balance"); <---------

        IDSComplianceService(_services[COMPLIANCE_SERVICE]).validateBurn(_who, _value);

        _tokenData.walletsBalances[_who] -= sharesToBurn;
        updateInvestorBalance(
            _tokenData,
            IDSRegistryService(_services[REGISTRY_SERVICE]),
            _who,
            sharesToBurn,
            CommonUtils.IncDec.Decrease
        );

        _tokenData.totalSupply -= sharesToBurn;
        return sharesToBurn;
    }

```

When an investor transfers tokens from their original wallet to another wallet they control, the burn function will fail with "Not enough balance" even though the investor still owns the tokens in their total balance.

**Impact:** If the admin doesn't use private mempools when performing sensitive operations such as burn or seize, investors can front-run to temporarily prevent token burning by transferring tokens between their own wallets.

**Proof of Concept:** Run the next proof of concept in `dstoken-regulated.test.ts`:

```typescript
describe('Burn DoS Vulnerability POC', function() {
        it('Should demonstrate that burn can be DoS by transferring between investor wallets', async function() {
          const [investor, wallet2, wallet3] = await hre.ethers.getSigners();
          const { dsToken, registryService } = await loadFixture(deployDSTokenRegulatedWithRebasingAndEighteenDecimal);

          // Register investor with multiple wallets
          await registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, investor.address, registryService);
          await registryService.addWallet(wallet2.address, INVESTORS.INVESTOR_ID.INVESTOR_ID_1);
          await registryService.addWallet(wallet3.address, INVESTORS.INVESTOR_ID.INVESTOR_ID_1);

          // Issue tokens to investor
          await dsToken.issueTokens(investor.address, 1000);

          // Transfer tokens between investor's own wallets
          await dsToken.connect(investor).transfer(wallet2.address, 1000);

          // Now investor has 0 balance in original wallet but 1000 total
          expect(await dsToken.balanceOf(investor.address)).to.equal(0);
          expect(await dsToken.balanceOfInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_1)).to.equal(1000);

          // VULNERABILITY: Burn fails because wallet balance is 0, even though investor has tokens
          await expect(dsToken.burn(investor.address, 100, 'DoS test'))
            .to.be.revertedWith('Not enough balance');
        });
      });

```

**Recommended Mitigation:** Possible mitigation options include:
* perform sensitive admin transactions such as burn and seize through private mempool services like [flashbots](https://docs.flashbots.net/flashbots-protect/overview) so they can't be front-run
* remove the `addWalletByInvestor` function to prevent investors from continually adding more wallets and distributing their tokens to them
* add `burnAll` and `seizeAll` functions to `DSToken` which iterate over every wallet belonging to an investor and burn/seize all their tokens

**Securitize:** Fixed in commit [05c5bad](https://github.com/securitize-io/dstoken/commit/05c5bada3c2801b1333fc96f4abc5226a84471f0) by removing `addWalletByInvestor`. Operations team to consider advice regarding running sensitive admin transactions via private mempools.

**Cyfrin:** Verified.
