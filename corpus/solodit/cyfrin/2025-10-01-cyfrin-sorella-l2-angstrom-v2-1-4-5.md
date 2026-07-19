---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-4-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: '`AngstromL2::_computeAndCollectProtocolSwapFee` computation can be simplified'
vuln_class: []
---

# `AngstromL2::_computeAndCollectProtocolSwapFee` computation can be simplified

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `AngstromL2::_computeAndCollectProtocolSwapFee` currently performs the following computation:

```solidity
    uint256 fee = exactIn
        ? absTargetAmount * protocolFeeE6 / FACTOR_E6
@>      : absTargetAmount * FACTOR_E6 / (FACTOR_E6 - protocolFeeE6) - absTargetAmount;
    fee128 = fee.toInt128();
```

However, the highlighted line can be simplified to:

```diff
absTargetAmount * protocolFeeE6 / (FACTOR_E6 - protocolFeeE6)
```

**Sorella Labs:** Fixed in commit [aa90806](https://github.com/SorellaLabs/l2-angstrom/commit/aa9080697d683aae327de2c64f638f2730c193dd).

**Cyfrin:** Verified. The calculation has been simplified.

\clearpage
