---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-3-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: '`GlobalConfigurationBranch::updateSettlementConfiguration` can be called for
  a non-existent `marketId`'
vuln_class: []
---

# `GlobalConfigurationBranch::updateSettlementConfiguration` can be called for a non-existent `marketId`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** `GlobalConfigurationBranch::updateSettlementConfiguration` doesn't validate if the `marketId` exists:

```solidity
function updateSettlementConfiguration(
    uint128 marketId,
    uint128 settlementConfigurationId,
    SettlementConfiguration.Data memory newSettlementConfiguration
)
    external
    onlyOwner
{
    SettlementConfiguration.update(marketId, settlementConfigurationId, newSettlementConfiguration);

    emit LogUpdateSettlementConfiguration(msg.sender, marketId, settlementConfigurationId);
}
```

But other functions like `updatePerpMarketStatus` do validate that the `marketId` exists:

```solidity
function updatePerpMarketStatus(uint128 marketId, bool enable) external onlyOwner {
    GlobalConfiguration.Data storage globalConfiguration = GlobalConfiguration.load();
    PerpMarket.Data storage perpMarket = PerpMarket.load(marketId);

    if (!perpMarket.initialized) {
        revert Errors.PerpMarketNotInitialized(marketId);
    }
```

**Recommended Mitigation:** Verify `marketId` validity in `updateSettlementConfiguration`.

**Zaros:** Fixed in commit [75be42e](https://github.com/zaros-labs/zaros-core/commit/75be42e892c13cb26876d66b0c5184971700714e).

**Cyfrin:** Verified.
