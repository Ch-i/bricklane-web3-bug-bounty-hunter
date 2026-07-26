---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-stakepet-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-stakepet
title: Exit fees implementation is inconsistent with documentation
vuln_class: []
---

# Exit fees implementation is inconsistent with documentation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-stakepet.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md)_

---

**Severity:** Low

**Description:** Inline comments of `StakePet` contract indicate that exit fee is charged as % of the collateral.

```
The contract also has an early exit fee, which is a percentage of the collateral taken if a participant chooses to exit early.
```

However, implementation shows that exit fee is charged as a [percent of yield](https://github.com/Ranama/StakePet/blob/9ba301823b5062d657baa3462224da498dc4bb46/src/StakePet.sol#L559)

```
uint256 earlyExitFee = (uint256(yieldToWithdraw) * EARLY_EXIT_FEE) / BASIS_POINT
```

**Recommended Mitigation:** Consider correcting code documentation to reflect actual implementation

**Client:** Fixed in [54a4dcb](https://github.com/Ranama/StakePet/commit/54a4dcbb696da3138dc0fdd8e7032d664d32b7da)

**Cyfrin:** Verified.
