---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-d2-hype-corewriter-v2-0-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-d2-hype-corewriter-v2-0
title: '`Hype_module::assetAddress` can be `pure`'
vuln_class: []
---

# `Hype_module::assetAddress` can be `pure`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md)_

---

**Description:** `Hype_module::assetAddress` neither reads nor writes state. Mark it `internal pure` to enable compiler optimizations, allow static analysis/staticcall-style usage, and slightly reduce gas/bytecode size while preventing accidental state access.

**D2:** Fixed in commit [`a217930`](https://github.com/d2sd2s/d2-contracts/commit/a2179308e7ecef2247cd51af52ddb90f4507d896)

**Cyfrin:** Verified.

\clearpage
