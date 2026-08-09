---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: Lack of validation to prevent receiving less LINEA tokens for the swap than
  the expected `minAmountOut`
vuln_class: []
---

# Lack of validation to prevent receiving less LINEA tokens for the swap than the expected `minAmountOut`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** There is no validation on the [`V3DexSwap::swap` ](https://github.com/Consensys/linea-monorepo/blob/8285efababe0689aec5f0a21a28212d9d22df22e/contracts/src/operational/V3DexSwap.sol#L50-L74)to prevent the dex swapper from receiving fewer tokens than the specified `minAmountOut`. It is true that most routers indeed enforce the received `amountOut` to be at least `minAmountOut`. However, full reliance on the router performing this validation poses a potential problem in case the dex swapper is updated to work with a router that does not perform this check.

**Recommended Mitigation:** Consider validating that the received LINEA tokens for the swap are at least the expected `minAmountOut`.

**Linea:** Fixed at [PR 1604](https://github.com/Consensys/linea-monorepo/pull/1604)

**Cyfrin:** Verified. Added a check to verify the caller received at least the specified `_minLineaOut` of  LINEA token.
