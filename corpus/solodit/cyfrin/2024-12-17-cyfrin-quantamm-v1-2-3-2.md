---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-3-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: '`AntimomentumUpdateRule.parameterDescriptions` initialized too long'
vuln_class: []
---

# `AntimomentumUpdateRule.parameterDescriptions` initialized too long

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** [`AntimomentumUpdateRule.parameterDescriptions`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/rules/AntimomentumUpdateRule.sol#L16-L18) is initialized as length 3 but only two entries are used:
```solidity
parameterDescriptions = new string[](3); // @audit should be 2
parameterDescriptions[0] = "Kappa: Kappa dictates the aggressiveness of response to a signal change TODO";
parameterDescriptions[1] = "Use raw price: 0 = use moving average, 1 = use raw price to be used as the denominator";
```
Consider initializing it as `new string[](2)`.

**QuantAMM:** Fixed in [`91241ca`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/91241ca9e72b8a4fc964cc2df34f5aeb82f7ca39)

**Cyfrin:** Verified.
