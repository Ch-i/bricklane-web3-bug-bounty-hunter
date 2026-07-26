---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-4-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Remove redundant `uint256` cast in `PerpMarket::getMarkPrice`
vuln_class: []
---

# Remove redundant `uint256` cast in `PerpMarket::getMarkPrice`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Remove redundant `uint256` cast in `PerpMarket::getMarkPrice` since `self.configuration.skewScale` is [already](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/perpetuals/leaves/MarketConfiguration.sol#L30) `uint256`.

**Recommended Mitigation:**
```solidity
SD59x18 skewScale = sd59x18(self.configuration.skewScale.toInt256());
```

**Zaros:** Fixed in commit [560f291](https://github.com/zaros-labs/zaros-core/commit/560f2910e88ca7a8761b4e16e8717a2e75a94256).

**Cyfrin:** Verified.
