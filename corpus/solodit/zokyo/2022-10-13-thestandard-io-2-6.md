---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-2-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Discrepancy in `getBucketMidpoint` logic in BondingCurve.sol.
vuln_class: []
---

# Discrepancy in `getBucketMidpoint` logic in BondingCurve.sol.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

Bonding Curve.sol - in body of getBucketPrice(): getBucketMidpoint(bucketIndex) is supposed to represent x in this formula: $y=k^{*}(x/m)\wedge j+i,$ where $x=$ current total supply of sEURO by Bonding Curve according to doc provided in code which is ibcoTotalSupply. But we have getBucketMidpoint (bucketIndex) = (bucket Index bucketSize) + (bucketSize / 2) which is kind of a quantized quantity of ibcoTotalSupply and not the same.

**Recommendation**

Align the implementation of `getBucketMidpoint` with the documented formula or update the documentation to reflect the current quantized approach.

**Re-audit comment**

Unresolved.

fix-1:
No change done by devs here to address the issue. The developing team might tell us that this does not harm the tokenomics of the project. Based upon their knowledge about the tokenomics the issue shall be considered irrelevant from our side.
