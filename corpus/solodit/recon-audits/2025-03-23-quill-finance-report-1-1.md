---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-02] Low Liquidity Branches will likely use the Redistribution due to 20%
  vs 5% premium'
vuln_class: []
---

# [L-02] Low Liquidity Branches will likely use the Redistribution due to 20% vs 5% premium

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

The difference in premium seems way too high, this can lead to scenarios in which, for low liquidity branches, whales remove bold from the stability pool as a means to trigger a redistribution

This is because redistributions are 4 times more profitable to them


https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/TroveManager.sol#L436-L455

```solidity
        if (_boldInStabPool > 0) {
            debtToOffset = LiquityMath._min(_entireTroveDebt, _boldInStabPool);
            collSPPortion = _collToLiquidate * debtToOffset / _entireTroveDebt;
            (collToSendToSP, collSurplus) =
                _getCollPenaltyAndSurplus(collSPPortion, debtToOffset, liquidationPenaltySP, _price);
        }

        // Redistribution
        debtToRedistribute = _entireTroveDebt - debtToOffset;
        if (debtToRedistribute > 0) {
            uint256 collRedistributionPortion = _collToLiquidate - collSPPortion;
            if (collRedistributionPortion > 0) {
                (collToRedistribute, collSurplus) = _getCollPenaltyAndSurplus(
                    collRedistributionPortion + collSurplus, // Coll surplus from offset can be eaten up by red. penalty
                    debtToRedistribute,
                    liquidationPenaltyRedistribution, // _penaltyRatio
                    _price
                );
            }
        }
```

**Mitigation**

I believe for some highly volatile assets it may be best to raise the premium up to 10% for Liquidations in the Stability Pool

This statement is unbacked as I don't have the time to model the SP + the Liquidity of the whole system

I believe this is not as big of an issue for liquity because they will have very high correlation assets

Whereas for you it may not be the case
