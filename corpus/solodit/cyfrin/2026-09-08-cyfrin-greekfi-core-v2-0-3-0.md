---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-3-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: '`Receipt::collectFees` loads the same fee accumulator twice'
vuln_class: []
---

# `Receipt::collectFees` loads the same fee accumulator twice

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `Receipt::collectFees` reads `feeAccrued[token]` once for the zero-value guard and again immediately afterward to calculate the collectible amount. There is no intervening write or external call, and optimized IR retains both mapping storage loads.

**Recommended Mitigation:** Load `feeAccrued[token]` into a local variable, use the local for the zero-value guard, and derive the collectible amount from the same local.

**GreekFi:** Fixed in [PR37](https://github.com/greekfi/contracts/pull/37)

**Cyfrin:** Verified. Receipt now loads the fee accumulator once and reuses the cached value.
