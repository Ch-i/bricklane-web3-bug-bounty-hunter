---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Incorrect `SmartVaultV4` function arguments should be renamed
vuln_class: []
---

# Incorrect `SmartVaultV4` function arguments should be renamed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** The following functions in `SmartVaultV4` take an argument `_USDCTargetAmount`:
* `calculateAmountIn()`
* `swapCollateral()`
* `autoRedemption()`

However, this is semantically incorrect as it is intended to represent the target `USDs` redemption amount and so should be renamed to avoid confusion.

**The Standard DAO:** Fixed by commit [a03f0d5](https://github.com/the-standard/smart-vault/commit/a03f0d54637195d34ed17f9a7540d6f201eef55d).

**Cyfrin:** Verified. The function arguments have been renamed.
