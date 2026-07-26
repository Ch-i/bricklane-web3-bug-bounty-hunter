---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Potential DoS of `SeasonFacet::gm` due to division by zero in `LibGauge::updateGaugePoints`
vuln_class: []
---

# Potential DoS of `SeasonFacet::gm` due to division by zero in `LibGauge::updateGaugePoints`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

There currently exists an edge case in [`LibGauge::updateGaugePoints`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibGauge.sol#L84) where it is possible to unintentionally DoS `SeasonFacet::gm` due to a potential division by zero. If there is only one newly whitelisted LP token in the Beanstalk protocol which therefore has no deposited BDV, execution will revert, thus preventing Beanstalk from advancing to the next Season. While it is unlikely that Beanstalk will encounter this issue so long as the existing whitelisted LP tokens remain, there is a small possibility that this could be an issue in the event of some future liquidity migration and so it should be handled accordingly.

```diff
...
// if there is only one pool, there is no need to update the gauge points.
if (whitelistedLpTokens.length == 1) {
    // Assumes that only Wells use USD price oracles.
    if (LibWell.isWell(whitelistedLpTokens[0]) && s.usdTokenPrice[whitelistedLpTokens[0]] == 0) {
        return (maxLpGpPerBdv, lpGpData, totalGaugePoints, type(uint256).max);
    }
    uint256 gaugePoints = s.ss[whitelistedLpTokens[0]].gaugePoints;
+   if (s.siloBalances[whitelistedLpTokens[0]].depositedBdv != 0) {
        lpGpData[0].gpPerBdv = gaugePoints.mul(BDV_PRECISION).div(
            s.siloBalances[whitelistedLpTokens[0]].depositedBdv
        );
+   }
    return (
        lpGpData[0].gpPerBdv,
        lpGpData,
        gaugePoints,
        s.siloBalances[whitelistedLpTokens[0]].depositedBdv
    );
}
...
```
