---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-d2-hype-corewriter-v2-0-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-d2-hype-corewriter-v2-0
title: Parameter name mismatch between interface and implementation may be misleading
vuln_class: []
---

# Parameter name mismatch between interface and implementation may be misleading

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md)_

---

**Description:** In `IHype_Module`, the parameter names differ from the implementation:

* `hyper_sendSpot(uint64 token, uint64 _wei)` vs implementation uses `asset` for the first `uint64`
* `hyper_addApiWallet(address wallet, string calldata apiKey)` vs implementation uses `name` for the `string calldata`

The `apiKey` name is especially risky as it may lead someone to submit a secret API key on-chain, which would be permanently public.

Consider aligning interface and implementation parameter names (e.g., use `asset` and `name/label`).

**D2:** Fixed in commit [`5c5cec4`](https://github.com/d2sd2s/d2-contracts/commit/5c5cec46325b7ac061d49d8035c4901ed5db4ed4)

**Cyfrin:** Verified.

\clearpage
