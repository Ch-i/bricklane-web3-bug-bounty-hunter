---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-12
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: '`read_current_sequence` uses `ANCHOR_DISCRIMINATOR_LEN` for raw Wormhole `u64`
  data'
vuln_class: []
---

# `read_current_sequence` uses `ANCHOR_DISCRIMINATOR_LEN` for raw Wormhole `u64` data

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** `read_current_sequence` borrows the constant `ANCHOR_DISCRIMINATOR_LEN` (8 bytes) to bound-check and copy the first 8 bytes of the Wormhole sequence tracker account as a little-endian `u64`.

```rust
/// Reads the current sequence from the Wormhole sequence tracker account.
/// The account stores the next sequence to be used by post_message.
/// Returns 0 if the account is uninitialized (first message).
fn read_current_sequence(account: &AccountInfo<'_>) -> Result<u64> {
    let data = account.try_borrow_data()?;

    // If the account is uninitialized, return 0.
    if data.len() < ANCHOR_DISCRIMINATOR_LEN {
        return Ok(0);
    }

    let mut buf = [0u8; ANCHOR_DISCRIMINATOR_LEN];
    buf.copy_from_slice(&data[0..ANCHOR_DISCRIMINATOR_LEN]);

    Ok(u64::from_le_bytes(buf))
}
```

This is functionally correct because `ANCHOR_DISCRIMINATOR_LEN == 8`, which matches the width of a u64. However, the constant name is specific to Anchor discriminators, while the Wormhole sequence tracker account here is being parsed as raw Wormhole data rather than an Anchor discriminator-prefixed account.


**Impact:** The code works correctly today. The concern is limited to readability and maintenance: future reviewers or maintainers may incorrectly infer that the Wormhole sequence account follows an Anchor discriminator-based layout, or may update one side of the logic without recognizing that the constant is only being used as a generic 8-byte width.

**Recommended Mitigation:** Introduce a dedicated constant (e.g. `WORMHOLE_SEQUENCE_U64_LEN` or reuse a single `U64_LEN` if the project adds one) whose name reflects **raw integer size**, not Anchor discriminators.

**Securitize:** Fixed in [52040d3](https://github.com/securitize-io/bc-solana-bridge-sc/commit/52040d3d4d1509320f3f701d7e872a3c6294a839).

Introduced a dedicated file-local constant WORMHOLE_SEQUENCE_LEN = 8 in bridge_ds_tokens.rs and replaced the misleading ANCHOR_DISCRIMINATOR_LEN usages in read_current_sequence. Behavior is unchanged.
**Cyfrin:** Confrimed.
