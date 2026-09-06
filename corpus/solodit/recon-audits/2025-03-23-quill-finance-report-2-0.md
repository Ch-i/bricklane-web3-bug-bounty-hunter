---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[G-01] Gas Optimizations'
vuln_class: []
---

# [G-01] Gas Optimizations

_Section severity (from Solodit section header): Gas_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**5k+ fetch price only if not shutdown**

https://github.com/subvisual/quill/blob/23e53123a16b12614d25bfb715e17dd41bcebbdd/contracts/src/BorrowerOperations.sol#L736-L739

```solidity
        (uint256 price,) = priceFeed.fetchPrice();
        if (!hasBeenShutDown) {
            _requireNewTCRisAboveCCR(_getNewTCRFromTroveChange(troveChange, price));
        }
```

You could fetch the price only if `!hasBeenShutDown`

**2.1k gas Can be made immutable**

I cannot find a setter, so you can save gas by making this immutable

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/TroveManager.sol#L225-L226

```solidity
        sequencerSentinel = _addressesRegistry.sequencerSentinel();

```

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/BorrowerOperations.sol#L31-L32

```solidity
    ISequencerSentinel internal sequencerSentinel;

```

**200+ Unnecessary Double Call**

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/CollateralRegistry.sol#L88-L114

```solidity

        // Gather and accumulate unbacked portions
        for (uint256 index = 0; index < totals.numCollaterals; index++) {
            ITroveManager troveManager = getTroveManager(index);
            (uint256 unbackedPortion, uint256 price, bool redeemable) =
                troveManager.getUnbackedPortionPriceAndRedeemability();
            prices[index] = price;
            if (redeemable) {
                totals.unbacked += unbackedPortion;
                unbackedPortions[index] = unbackedPortion;
            }
        }

        // There’s an unlikely scenario where all the normally redeemable branches (i.e. having TCR > SCR) have 0 unbacked
        // In that case, we redeem proportinally to branch size
        if (totals.unbacked == 0) {
            unbackedPortions = new uint256[](totals.numCollaterals);
            for (uint256 index = 0; index < totals.numCollaterals; index++) {
                ITroveManager troveManager = getTroveManager(index);
                (,, bool redeemable) = troveManager.getUnbackedPortionPriceAndRedeemability();
                if (redeemable) {
                    uint256 unbackedPortion = troveManager.getEntireSystemDebt();
                    totals.unbacked += unbackedPortion;
                    unbackedPortions[index] = unbackedPortion;
                }
            }
        }
```
