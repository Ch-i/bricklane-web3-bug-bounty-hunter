---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: '`PartialPolicyEngine::deserialize_checked` version auto-detection heuristic
  can misidentify account layout, corrupting lock period data'
vuln_class: []
---

# `PartialPolicyEngine::deserialize_checked` version auto-detection heuristic can misidentify account layout, corrupting lock period data

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** The `PartialPolicyEngine::deserialize_checked` function auto-detects whether a PolicyEngine account uses a v1 layout (65-byte header) or v2 layout (106-byte header) using a byte-level heuristic:

```rust
// policy_engine.rs:74-81
if data.len() >= v2_end {
    let bool_byte = data[v2_start + MAPPING_SIZE];
    if bool_byte <= 1 {
        let acc = Self::try_from_slice(&data[v2_start..v2_end])?;
        return Ok(acc);
    }
}
```

A v1 account's data ends at byte 354 (8 + 65 + 256 + 25). If the PolicyEngine program reallocates the account to >= 395 bytes while still using v1 layout, trailing zero bytes at position 370 satisfy `bool_byte <= 1`. The code then reads the 256-byte country-to-region mapping from offset 114 instead of 73 (a 41-byte shift) and reads `IssuancePolicies` (`us_lock_period`, `non_us_lock_period`) from the wrong offset, producing arbitrary values.

This finding composes with the `u64-to-i64` cast in `validate_locked_tokens` (locked_tokens.rs:38): if the corrupted `lock_period` bytes exceed `i64::MAX` (2^63), the `lock_period as i64` cast wraps to a negative value, making `unlock_time` always in the past. All issuance locks appear expired, completely bypassing US regulatory lock enforcement.

**Impact:** Corrupted country-to-region mapping produces incorrect region lookups, selecting the wrong lock period (US vs non-US). Combined with the `u64-to-i64` cast, if the corrupted lock period value exceeds 2^63, all locks appear expired. US investors subject to regulatory holding periods (e.g., Reg D 12-month lock) could bridge tokens immediately after issuance. The severity depends on whether the external PolicyEngine program reallocates v1 accounts beyond 354 bytes, which is outside this codebase's control.

**Proof of Concept:**
1. PolicyEngine v1 account: `[8B disc][65B header][256B mapping][25B IssuancePolicies]` = 354 bytes
2. PolicyEngine program reallocates account to 512 bytes (e.g., upgrade preparation); trailing bytes zero-filled
3. User calls `bridge_ds_tokens`, triggering `validate_locked_tokens`
4. `PartialPolicyEngine::deserialize_checked`: `data.len()` (512) >= 395, `data[370]` == 0x00 passes `<= 1`
5. Mapping read from offset 114 instead of 73; `us_lock_period` read from wrong offset
6. If corrupted `us_lock_period` bytes >= 2^63: `lock_period as i64` wraps negative at locked_tokens.rs:38
7. `unlock_time = issue_time + negative_value` is always in the past
8. All issuance locks appear expired; US investor bridges locked tokens

**Recommended Mitigation:** Replace the heuristic with deterministic version detection. For mainnet where only v2 accounts exist:

```rust
require_gte!(data.len(), v2_end, BridgeError::InvalidPolicyEngineAccount);
let acc = Self::try_from_slice(&data[v2_start..v2_end])?;
Ok(acc)
```

If backward compatibility is needed, use exact account data length matching.

Also fix the `u64-to-i64` cast in locked_tokens.rs:38:

```rust
let lock_period_i64 = i64::try_from(lock_period)
    .map_err(|_| error!(BridgeError::InvalidPolicyEngineAccount))?;
let unlock_time = issuance.issue_time.saturating_add(lock_period_i64);
```

**Securitize:** Fixed in [d36968e](https://github.com/securitize-io/bc-solana-bridge-sc/commit/d36968e161e18a7774304f3af6e4adc97d395438).

**Cyfrin:** Verified.
