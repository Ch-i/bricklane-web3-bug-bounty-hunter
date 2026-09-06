---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Use explicit unsigned integer sizing instead of `uint`
vuln_class: []
---

# Use explicit unsigned integer sizing instead of `uint`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** In Solidity `uint` automatically maps to `uint256` but it is considered good practice to specify the exact size when declaring variables:

```
Accounting.sol
200:    ) public view returns (uint jrtNavT1, uint srtNavT1, uint reserveNavT1) {

StrataCDO.sol
86:     uint totalAssetsOverall = strategy.totalAssets();
128:    uint jrtAssetsIn = isJrt_ ? baseAssets : 0;
129:    uint srtAssetsIn = isJrt_ ? 0          : baseAssets;
143:    uint jrtAssetsOut = isJrt_ ? baseAssets : 0;
144:    uint srtAssetsOut = isJrt_ ? 0          : baseAssets;
```


**Strata:**
Fixed in commit [506c4c](https://github.com/Strata-Money/contracts-tranches/commit/506c4c744dc6dea538bb8b69dade114bee1aeb5e).

**Cyfrin:** Verified.
