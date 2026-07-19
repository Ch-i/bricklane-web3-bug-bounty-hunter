---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-3-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Unused errors
vuln_class: []
---

# Unused errors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** In the library [`Common`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/libs/Common.sol#L5-L6) there are two unused errors:
```solidity
error SignatureVerificationFailed();
error BadSignature();
```
Consider removing these.

**YieldFi:** Fixed in commit [`9aa242b`](https://github.com/YieldFiLabs/contracts/commit/9aa242b7351314fe07160e98699d8da14a1b9bc2)

**Cyfrin:** Verified.
