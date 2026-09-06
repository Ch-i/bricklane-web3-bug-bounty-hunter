---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-07-cyfrin-securitize-dstoken-whitelist-svm-v2-0-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-11-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-07-cyfrin-securitize-dstoken-whitelist-svm-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-07-cyfrin-securitize-dstoken-whitelist-svm-v2-0
title: Transaction size limit could be exceeded with non-empty hashes
vuln_class: []
---

# Transaction size limit could be exceeded with non-empty hashes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-07-cyfrin-securitize-dstoken-whitelist-svm-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-07-cyfrin-securitize-dstoken-whitelist-svm-v2.0.md)_

---

**Description:** The `whitelist` instruction accepts variable-length strings (`investor_id`, `collision_hash`, `proof_hash`) that are encoded in CPI data buffers.

Solana enforces a 1,232-byte transaction size limit, which might limit the whitelisting feature in some edge cases.

**Impact:** The production configuration uses empty strings for `collision_hash` and `proof_hash`, which keeps transaction sizes below the 1,232-byte limit.

However, if non-empty hashes are used in the future, the transaction size could exceed the limit when adding 5 or more levels in a single transaction, causing the transaction to fail.

**Proof of Concept:** With the configuration using empty hashes, the `whitelist` instruction maintains a safety margin below the 1,232-byte transaction limit:

| Levels | Transaction Size | Margin | Status |
|--------|------------------|--------|--------|
| 2 | 994 bytes | 238 bytes | Safe |
| 3 | 1,016 bytes | 216 bytes | Safe |
| 5 | 1,060 bytes | 172 bytes | Safe |

For comparison, if non-empty 32-character hashes were used, the transaction would revert with 5 or more levels:

| Levels | Transaction Size | Margin | Status |
|--------|------------------|--------|--------|
| 2 | 1,098 bytes | 134 bytes | Safe |
| 3 | 1,143 bytes | 89 bytes | Safe |
| 5 | 1,233 bytes | -1 byte | Exceeds limit |

The development team confirmed that production will use empty strings for `collision_hash` and all `proof_hash` values. The validation `rbac_utils::is_valid_hash` accepts empty strings as valid:

```rust
pub fn is_valid_hash(hash: &str) -> bool {
     hash.is_ascii() && hash.len() <= 32
}
```

**Recommended Mitigation:** No mitigation required for the current configuration, but consider documenting this behavior.

If future requirements change to use non-empty hashes with 5 or more levels, the function would need to be split into separate transactions to avoid reverting.

**Securitize:** Acknowledged.

\clearpage
