---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-4-2
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
title: Cache memory array length if expected size of array is >= 3
vuln_class: []
---

# Cache memory array length if expected size of array is >= 3

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Cache memory array length if [expected size of array is >= 3](https://x.com/DevDacian/status/1791490921881903468):

```solidity
File: src/tree-proxy/leaves/RootUpgrade.sol
97:        for (uint256 i = 0; i < branchUpgrades.length; i++) {
117:        for (uint256 i = 0; i < selectors.length; i++) {
136:        for (uint256 i = 0; i < selectors.length; i++) {
171:        for (uint256 i = 0; i < selectors.length; i++) {
202:        for (uint256 i = 0; i < initializables.length; i++) {

File: src/perpetuals/leaves/GlobalConfiguration.sol
96:        for (uint256 i = 0; i < collateralTypes.length; i++) {

File: src/perpetuals/leaves/PerpMarket.sol
// @audit the `if` statement can be removed as it is obsolete;
// the `for` loop will never execute if `length == 0`
344:        if (params.customOrdersConfiguration.length > 0) {
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

File: src/perpetuals/branches/LiquidationBranch.sol
57:            if (i >= globalConfiguration.accountsIdsWithActivePositions.length()) break;
```

**Zaros:** Fixed in commit [3c5d345](https://github.com/zaros-labs/zaros-core/commit/3c5d3456eefa7cde1c834895a1eb600387d2f37a).

**Cyfrin:** Verified.
