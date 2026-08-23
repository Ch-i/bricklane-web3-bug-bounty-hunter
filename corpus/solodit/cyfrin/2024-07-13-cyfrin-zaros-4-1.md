---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-4-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Don't initialize variables to default values
vuln_class: []
---

# Don't initialize variables to default values

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Don't initialize variables to default values as this is already done:

```solidity
File: src/tree-proxy/leaves/RootUpgrade.sol
70:        for (uint256 i = 0; i < selectorCount; i++) {
81:        for (uint256 i = 0; i < branchCount; i++) {
97:        for (uint256 i = 0; i < branchUpgrades.length; i++) {
117:        for (uint256 i = 0; i < selectors.length; i++) {
136:        for (uint256 i = 0; i < selectors.length; i++) {
171:        for (uint256 i = 0; i < selectors.length; i++) {
202:        for (uint256 i = 0; i < initializables.length; i++) {

File: src/perpetuals/leaves/GlobalConfiguration.sol
96:        for (uint256 i = 0; i < collateralTypes.length; i++) {

File: src/perpetuals/branches/GlobalConfigurationBranch.sol
185:        for (uint256 i = 0; i < liquidators.length; i++) {

File: src/perpetuals/leaves/PerpMarket.sol
345:            for (uint256 i = 0; i < params.customOrdersConfiguration.length; i++) {

File: src/perpetuals/leaves/TradingAccount.sol
145:        for (uint256 i = 0; i < self.marginCollateralBalanceX18.length(); i++) {
169:        for (uint256 i = 0; i < self.marginCollateralBalanceX18.length(); i++) {
229:        for (uint256 i = 0; i < self.activeMarketsIds.length(); i++) {
264:        for (uint256 i = 0; i < self.activeMarketsIds.length(); i++) {
420:        for (uint256 i = 0; i < globalConfiguration.collateralLiquidationPriority.length(); i++) {

File: src/perpetuals/branches/TradingAccountBranch.sol
122:        for (uint256 i = 0; i < tradingAccount.activeMarketsIds.length(); i++) {
168:        for (uint256 i = 0; i < tradingAccount.activeMarketsIds.length(); i++) {
241:        for (uint256 i = 0; i < data.length; i++) {

File: src/perpetuals/branches/LiquidationBranch.sol
103:        for (uint256 i = 0; i < accountsIds.length; i++) {
135:            for (uint256 j = 0; j < ctx.amountOfOpenPositions; j++) {
```

**Zaros:** Fixed in commit [1a7df5c](https://github.com/zaros-labs/zaros-core/commit/1a7df5c565233aa9a3a3b47bceb614e6a7d57cc4).

**Cyfrin:** Verified.
