---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-26-cyfrin-eulerswap-v2-0-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-05-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-26-cyfrin-eulerswap-v2-0
title: Lack of input validation
vuln_class: []
---

# Lack of input validation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-26-cyfrin-eulerswap-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md)_

---

**Description:** In the [constructor](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/EulerSwapFactory.sol#L44-L50) for `EulerSwapFactory` there's no sanity check that the addresses for  `evkFactory_`, `eulerSwapImpl_`, and `feeOwner_` aren't `address(0)` which is a simple mistake to make.

Consider validating that these are not `address(0)`.

For example:
```solidity
require(evkFactory_ != address(0), "Zero address");
require(eulerSwapImpl_ != address(0), "Zero address");
require(feeOwner_ != address(0), "Zero address");
```

**Euler:** Acknowledged.

\clearpage
