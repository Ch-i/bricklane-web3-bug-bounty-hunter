---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: No event emission when initializing parameters
vuln_class: []
---

# No event emission when initializing parameters

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** On the constructors of the [`L1LineaTokenBurner`](https://github.com/Consensys/linea-monorepo/blob/8285efababe0689aec5f0a21a28212d9d22df22e/contracts/src/operational/L1LineaTokenBurner.sol#L21-L27) and [`V3DexSwap` ](https://github.com/Consensys/linea-monorepo/blob/8285efababe0689aec5f0a21a28212d9d22df22e/contracts/src/operational/V3DexSwap.sol#L31-L41)contracts, there are no event emissions to log the values of the parameters that were initialized.
The same occurs when reinitializing the values on the [`RollupRevenueVault`](https://github.com/Consensys/linea-monorepo/blob/8285efababe0689aec5f0a21a28212d9d22df22e/contracts/src/operational/RollupRevenueVault.sol#L98-L160).

**Recommended Mitigation:** Consider emitting events to log the values of the initialized parameters.

**Linea:** Fixed at [PR 1604](https://github.com/Consensys/linea-monorepo/pull/1604)

**Cyfrin:** Verified.
