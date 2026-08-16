---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-16
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Improper header handling in `SpotFeesReport` logging causes DoS on swap instruction
vuln_class: []
---

# Improper header handling in `SpotFeesReport` logging causes DoS on swap instruction

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** In `match_orders`, `ref_payment` handles `client.header` being None by defaulting to 0, but `ref_client_id` uses `ok_or` and returns an error if `header` is None. This causes the function to fail when `total_fees` > 0 and `header` is None.

```rust
            solana_program::log::sol_log_data(&[bytemuck::bytes_of::<SpotFeesReport>(
                &SpotFeesReport {
                    tag: log_type::SPOT_FEES,
                    fees: total_fees,
                    ref_payment,
                    ref_client_id: client
                        .header
                        .as_ref()
                        .ok_or(drv_err!(DeriverseErrorKind::ClientPrimaryAccountMustBeSome))?
                        .ref_client_id,
                    ..SpotFeesReport::zeroed()
                },
            )]);
```

This will always happen when the user is using the swap instruction.

**Impact:** The impact is high, as this issue results in a permanent DOS whenever the swap instruction is executed and `total_fees > 0` is true.

**Recommended Mitigation:** Consider handling this gracefully instead of reverting when the header is None.

**Deriverse:** Fixed in commit [4f7bc8](https://github.com/deriverse/protocol-v1/commit/4f7bc8ac68325aa93b339ff91c0ac794ea17ffd9).

**Cyfrin:** Verified.
