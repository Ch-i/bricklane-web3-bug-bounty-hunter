---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-3-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Confusing variable naming in fee manager contracts
vuln_class: []
---

# Confusing variable naming in fee manager contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The fee manager contracts use confusing variable names for fee percentage values.
In `MbpsFeeManager`, the variable `fee` represents a fee percentage in MBPS (milli basis points), not an actual fee amount. The comment even clarifies "Fee expressed in mbps (1000 mbps = 1%)", and the calculation formula `(amount * fee + FEE_DENOMINATOR - 1) / FEE_DENOMINATOR` shows that `fee` is used as a percentage rate. However, the variable name `fee` typically implies an actual fee amount rather than a percentage rate. For example, the fee manager contract exposes a function `getFee(uint256 amount)`.

This naming convention creates confusion for those who expect `fee` to represent an actual fee amount rather than a percentage rate used in calculations.

**Impact:** The confusing variable names could lead to integration errors, misunderstanding of fee calculations, and potential bugs in contracts that interact with the fee managers.

**Recommended Mitigation:** Rename the fee variables to clearly indicate they represent percentages:

```diff
- uint256 public fee;
+ uint256 public feeMBPS;
```
Consider using `feePercentageMBPS` for even better clarity.

**Securitize:** Fixed in commit [6a5d45](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/6a5d45daf788fe573cb435f24a033472b336b21a).

**Cyfrin:** Verified.
