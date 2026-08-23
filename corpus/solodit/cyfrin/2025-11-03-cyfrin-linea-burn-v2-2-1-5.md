---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: Require condition `_minLineaOut > 0` offers no protection against malicious
  BURNER_ROLE behaviour
vuln_class: []
---

# Require condition `_minLineaOut > 0` offers no protection against malicious BURNER_ROLE behaviour

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** Function burnAndBridge in RollupRevenueVault is only callable by the BURNER_ROLE. During this call, the BURNER_ROLE can pass in arbitrary `_swapData` to call on the V3DexSwap contract. The swap() function contains the following check:
```solidity
require(_minLineaOut > 0, ZeroMinLineaOutNotAllowed());
```

However, this check provides no protection against malicious behaviour by the BURNER_ROLE since `_minLineaOut` can be passed as 1 wei instead.

**Impact:** Loss of ETH is intended to be bridged to L1 as part of the burn and bridge mechanism.

**Proof of Concept:** **Recommended Mitigation:**
It is recommended to either implement a configurable slippage percent on the swap amount that `_minLineaOut` should not exceed or consider acknowledging this risk.

**Linea:** Acknowledged.

**Cyfrin:** Acknowledged.
