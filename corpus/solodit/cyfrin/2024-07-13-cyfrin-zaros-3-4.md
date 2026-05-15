---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-3-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Inconsistent validation while creating/updating a perp market
vuln_class: []
---

# Inconsistent validation while creating/updating a perp market

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** `GlobalConfigurationBranch::createPerpMarket` [reverts](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/perpetuals/branches/GlobalConfigurationBranch.sol#L351-L353) if `maxFundingVelocity` is zero but the same check doesn't occur in `GlobalConfigurationBranch::updatePerpMarketConfiguration`.

**Recommended Mitigation:** Consider applying the same validations when creating and updating a perp market.

**Zaros:** Fixed in commit [ad2bcb1](https://github.com/zaros-labs/zaros-core/commit/ad2bcb114a9aaa0ed8838e05335d78badb51032b).

**Cyfrin:** Verified.
