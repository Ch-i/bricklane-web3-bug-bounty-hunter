---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-5-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Emit event first to optimize away previous value variables
vuln_class: []
---

# Emit event first to optimize away previous value variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Emit event first to optimize away previous value variables, eg in `SablierEscrow::setTradeFee`:
```diff
-       UD60x18 previousTradeFee = tradeFee;
+       emit SetTradeFee(address(comptroller), tradeFee, newTradeFee);
        tradeFee = newTradeFee;
-       emit SetTradeFee(address(comptroller), previousTradeFee, newTradeFee);
```

Similar optimizations can be made in:
* `SablierLidoAdapter::setYieldFee`
* `SablierLidoAdapter::setSlippageTolerance`

**Sablier:** Acknowledged; we have the practice of emitting the events on the last line in the function.
