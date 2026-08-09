---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-26-cyfrin-eulerswap-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-05-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-26-cyfrin-eulerswap-v2-0
title: Unused imports and errors
vuln_class: []
---

# Unused imports and errors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-26-cyfrin-eulerswap-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md)_

---

**Description:** The following imports are unused:
- [`IEVC` and `IEVault`, `EulerSwapPeriphery.sol#L6-L7`](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/EulerSwapPeriphery.sol#L6-L7)

And the following error is unused:
- [`InvalidQuery`, `EulerSwapFactory.sol#L36`](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/EulerSwapFactory.sol#L36)

Consider removing them.

**Euler:** Fixed in commit [`6109f53`](https://github.com/euler-xyz/euler-swap/pull/96/commits/6109f53c7b49be41867d9857d6bb0b6869761a02)

**Cyfrin:** Verified.
