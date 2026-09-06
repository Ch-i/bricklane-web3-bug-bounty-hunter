---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Expired Private Client Cannot Be Re-added to Queue
vuln_class: []
---

# Expired Private Client Cannot Be Re-added to Queue

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `new_private_client()` function incorrectly rejects re-adding a wallet whose previous entry has expired. The function checks for duplicate wallet addresses before validating expiration status, preventing expired records from being treated as vacant slots.

In the record insertion logic (lines 131-133), the code checks if a wallet already exists:
```rust
if record.wallet == *wallet.key && record.creation_time != 0 {
    return Err(AlreadyExists(index));
}
```
However, this check occurs before the expiration validation. According to the `PrivateClient::is_vacant()` method (defined in `src/state/private_client.rs`), a record should be considered vacant if either:
1. `creation_time == 0` (uninitialized), or
2. `current_time > expiration_time` (expired)

The problem is that when iterating through records to find an insertion position, the duplicate check at line 131 returns an error immediately when a matching wallet is found, regardless of expiration status. This prevents the code from reaching the `is_vacant()` check at line 136, which would correctly identify expired records as reusable slots.

**Impact:** **Queue Slot Exhaustion:** Expired private client cannot be renewed.


**Recommended Mitigation:** Modify the duplicate wallet check to validate expiration status before returning an error. Only return `AlreadyExists` if the wallet matches and the record is still valid (not expired).

**Deriverse:** Fixed in commit [a626a26](https://github.com/deriverse/protocol-v1/commit/a626a2626a483e55f76b582f5bd49ff2a7b2d62a).

**Cyfrin:** Verified.
