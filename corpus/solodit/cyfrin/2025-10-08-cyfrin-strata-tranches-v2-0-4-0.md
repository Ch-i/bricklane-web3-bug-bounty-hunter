---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Incorrect Comment and Missing Lower Bound for `minimumJrtSrtRatio` in `Accounting`
vuln_class: []
---

# Incorrect Comment and Missing Lower Bound for `minimumJrtSrtRatio` in `Accounting`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:**
```solidity
/// @dev minimum TVL ratio: TVLjrt/TVLsrt, e.g. >= 0.05%
```
```solidity
minimumJrtSrtRatio = 0.05e18;
```
The comment says “0.05%” (0.0005e18) but the value is 5% (0.05e18). and there is no check to prevent setting value <0.05%
and it may be intended to start with 5% ratio



**Recommended Mitigation:**
- Update comment to reflect intended 5% (e.g., “>= 5%”).
- In `Accounting::setMinimumJrtSrtRatio`, add `require(bps >= 0.0005e18, "RatioTooLow");` for a min bound.

**Strata:**
Fixed in commit [eefd73](https://github.com/Strata-Money/contracts-tranches/commit/eefd73cfee7783cb45b19e0763d83ba2fb0084af) and [c1afee2](https://github.com/Strata-Money/contracts-tranches/commit/c1afee2f0c14531ddbe88f81d4aa4f3325e87fd1). Updated comment and added check to validate lower bound for `minimumJrtSrtRatio`

**Cyfrin:** Verified.
