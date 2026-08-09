---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Accumulation of dust amounts due to rounding in `_tokenDistribution()`
vuln_class: []
---

# Accumulation of dust amounts due to rounding in `_tokenDistribution()`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** `_tokenDistribution()` computes each share independently with integer division:

```solidity
function _tokenDistribution(uint256 amount) internal view returns (uint256, uint256, uint256) {
    uint256 beneficiaryAmount = (amount * beneficiaryPercentage) / PERCENTAGE_DIVISOR;
    uint256 creatorAmount = (amount * creatorPercentage) / PERCENTAGE_DIVISOR;
    uint256 vaultAmount = (amount * vaultPercentage) / PERCENTAGE_DIVISOR;
    return (beneficiaryAmount, creatorAmount, vaultAmount);
}
```

If `beneficiaryPercentage + creatorPercentage + vaultPercentage == 10000` but any division truncates, `beneficiaryAmount + creatorAmount + vaultAmount < amount`, leaving 1–2 wei of “dust”.

**Impact:** Dust gradually accumulating lost and never reaching the intended recipients.


**Recommended Mitigation:** Calculate `beneficiaryAmount` and `creatorAmount` as above, then set
```solidity
vaultAmount = amount - beneficiaryAmount - creatorAmount;
```
to guarantee full distribution without dust.

**OctoDeFi:** Fixed in PR [\#16](https://github.com/octodefi/strategy-builder-plugin/pull/16).

**Cyfrin:** Verified. The `vaultAmount` is now calculated as the remainder after deducting the beneficiary and creator amounts.
