---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-4-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: '`posted.payload.clone()` copies entire VAA payload unnecessarily in `execute_vaa_v1`'
vuln_class: []
---

# `posted.payload.clone()` copies entire VAA payload unnecessarily in `execute_vaa_v1`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** In `ExecuteVaaV1::handler`:

```rust
let payload_bytes = posted.payload.clone();
```

Copies up to 1024 bytes on the heap. Consider decoding while the borrow is held, then storing raw bytes afterward.

**Recommended Mitigation:** Decode payload while the borrow is active, then store the raw bytes. Alternatively, use `to_vec()` instead of `clone()` for clarity.

**Securitize:** Fixed in [5cc0158](https://github.com/securitize-io/bc-solana-bridge-sc/commit/5cc01584342e4aaaadc36cf962fd862c81163607).

**Cyfrin:** Verified.
