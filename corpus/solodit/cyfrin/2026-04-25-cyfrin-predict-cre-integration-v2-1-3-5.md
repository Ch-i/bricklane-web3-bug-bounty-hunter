---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-3-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Explicit `payouts[0] = 0` and `payouts[1] = 0` writes a zero value
vuln_class: []
---

# Explicit `payouts[0] = 0` and `payouts[1] = 0` writes a zero value

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** `ChainlinkAdapter::_constructPayouts` explicitly writes `0` to an already-zero memory slot — dead code.

```solidity
88:            payouts[0] = 0;
89:            payouts[1] = 1;
98:            payouts[0] = 1;
99:            payouts[1] = 0;
```

**Impact:** Dead code; minor gas waste.

**Recommended Mitigation:** Drop redundant zero writes.

**Predict.fun:** Acknowledged; yes it is dead code but we're trying to avoid ambiguity.
