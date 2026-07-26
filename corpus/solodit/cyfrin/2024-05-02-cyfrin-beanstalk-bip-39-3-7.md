---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-3-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Use of average grown stalk per BDV is not correctly documented
vuln_class: []
---

# Use of average grown stalk per BDV is not correctly documented

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

The nature of the Gauge Point system is to distribute new stalk among whitelisted LP and BEAN deposits based on their Bean-denominated value (BDV). The average grown stalk per BDV also takes into account the BDV of unripe assets, linked to their respective underlying asset based on the following ratio:

$$\frac{paidFertilizer}{mintedFertilzier} \times \frac{totalUnderlying(urAsset)}{supply(urAsset)}$$

While considering the BDV of unripe assets for the average grown stalk per BDV is mathematically correct, this metric lacks practical sense due to a portion of the average grown stalk per BDV never being issued, causing it to lose its semantic meaning.

```solidity
// LibGauge::updateGrownStalkEarnedPerSeason
uint256 totalBdv = totalLpBdv.add(beanDepositedBdv);
...
uint256 newGrownStalk = uint256(s.seedGauge.averageGrownStalkPerBdvPerSeason)
    .mul(totalBdv) // This BDV does not include unripe asset BDV
    .div(BDV_PRECISION);
```

As can be seen, the clear intention of this calculation is to issue `newGrownStalk` for a season but only take into account the BDV corresponding to whitelisted LPs and BEAN. Given that it is never issued, the rest of the grown stalk per BDV could be considered implicitly burned. This design decision should be better documented, making it clear how the unissued grown stalk is considered.
