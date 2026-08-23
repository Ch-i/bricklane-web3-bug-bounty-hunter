---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-06-cyfrin-benqi-collateral-migrator-v2-0-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-06-cyfrin-benqi-collateral-migrator-v2-0
title: User LTV always worsens after migration
vuln_class: []
---

# User LTV always worsens after migration

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md)_

---

**Description:** The flow for migrating collateral between two markets is as follows:

1. The end user calls `CollateralMigrator::migrateCollateral` with the required swap parameters.
2. `CollateralMigrator` takes a flash loan from a Trader Joe liquidity pair.
3. Using the flash loan, `CollateralMigrator` opens a position in the target market.
4. With the position now overcollateralized, the original source market position can be closed.
5. The source tokens are swapped for target tokens.
6. The target tokens are used to repay the flash loan along with the associated fees.
7. Any remaining target tokens are deposited into the target market on behalf of the user.

The issue lies in how flash loan fees affect the resulting position.

Consider the following example:

You have a position where you’ve borrowed 50 ETH against 110 USDC, giving you an LTV of ~45%. You want to migrate the collateral from USDC to DAI. For simplicity, assume:
- A 10% flash loan fee, and
- A 1:1 USDC/DAI exchange rate.

The largest flash loan you can take is 100 DAI, since the additional 10 DAI needed to cover the fee must come from the swap proceeds.

You then swap your 110 USDC for 110 DAI and repay the 100 DAI loan plus 10 DAI in fees. This leaves you with 0 DAI left over. Your new collateral position is now just 100 DAI backing 50 ETH, raising your LTV to 50%.

Because the flash loan must be repaid with fees, and those fees must come from the user’s existing collateral, every migration necessarily increases the user’s LTV, reducing their margin of safety.

**Impact:** Collateral migration always results in a higher LTV post-migration, increasing the user’s liquidation risk.

**Recommended Mitigation:** Consider adding a parameter allowing users to optionally top up the transaction with additional target tokens to cover the flash loan fees. This would preserve their original LTV.

**Benqi:** Fixed in commit [`afe450e`](https://github.com/woof-software/benqi-collateral-migrator/commit/afe450e3908305e39a732928a06bfdcae7d38d36)

**Cyfrin:** Verified. A parameter `extraFunds` was added to `migrateCollateral` that allows the user to top up, keeping their LTV the same.
