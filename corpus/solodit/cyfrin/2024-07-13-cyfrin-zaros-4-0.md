---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-4-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Use named return variables to save 9 gas per return variable
vuln_class: []
---

# Use named return variables to save 9 gas per return variable

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Use named return variables to [save 9 gas per return variable](https://x.com/DevDacian/status/1796396988659093968) and also simplify function code:

```solidity
File: src/external/ChainlinkUtil.sol
84:        returns (FeeAsset memory)

File: src/perpetuals/branches/OrderBranch.sol
128:        returns (UD60x18, UD60x18) // @audit in getMarginRequirementForTrade()
144:    function getActiveMarketOrder(uint128 tradingAccountId) external pure returns (MarketOrder.Data memory) {

File: src/perpetuals/leaves/PerpMarket.sol
97:        returns (UD60x18) // @audit in getMarkPrice()

File: src/tree-proxy/RootProxy.sol
50:    function _implementation() internal view override returns (address) {

// @audit refactor to:
function _implementation() internal view override returns (address branch) {
    RootUpgrade.Data storage rootUpgrade = RootUpgrade.load();

    branch = rootUpgrade.getBranchAddress(msg.sig);
    if (branch == address(0)) revert Errors.UnsupportedFunction(msg.sig);
}
```

**Zaros:** Fixed in commit [4972f52](https://github.com/zaros-labs/zaros-core/commit/4972f52e04ebbcbe0d56ad2136d8023bb5fc0d9f).

**Cyfrin:** Verified.
