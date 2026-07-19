---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-13
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Returning true when the current time has reached the `expiration_time` in `is_vacant`
vuln_class: []
---

# Returning true when the current time has reached the `expiration_time` in `is_vacant`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** `is_vacant` is used in `deposit` and `new_private_client`. In deposit function, we check whether the user is a private client and `is_vacant` is false, meaning the record has not expired. In `new_private_client`, we check whether `is_vacant` returns true, meaning the record is vacant or has expired.
```rust
    pub fn is_vacant(&self, current_time: u32) -> bool {
        self.creation_time == 0 || current_time > self.expiration_time
    }
```

In `is_vacant`, we check whether the current time is greater than the expiration time. If the current time is equal to the expiration time, the function still returns false.

**Impact:** `is_vacant` allows an expired private client to deposit, and in `new_private_client` we do not update the record at the index even when the current time has reached the expiration.

**Recommended Mitigation:** `is_vacant` should return true when the current time is equal to the expiration time:
```rust
    pub fn is_vacant(&self, current_time: u32) -> bool {
        self.creation_time == 0 || current_time >= self.expiration_time
    }
```

**Deriverse:** Fixed in commit [408cd2](https://github.com/deriverse/protocol-v1/commit/408cd20e1339196735c2bed19e211fa4dddd931b).

**Cyfrin:** Verified.
