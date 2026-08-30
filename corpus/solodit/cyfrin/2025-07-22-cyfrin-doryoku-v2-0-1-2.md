---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Vesting Durations Might be out of Bounds Which Allows Immediate Withdrawals
vuln_class: []
---

# Vesting Durations Might be out of Bounds Which Allows Immediate Withdrawals

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** Vesting has a limit for minimum and maximum duration it can have. Within initial configuration, minimum duration is *10 days* while the maximum is *180 days*.

However `vest` doesn't confirm vesting duration is within bounds (specifically, relevant check is commented out):
```solidity
        // Validate vest duration is within bounds
        // require!(dur_secs >= min_secs, ErrorCode::VestDurationTooShort);
        // require!(dur_secs <= max_secs, ErrorCode::VestDurationTooLong);
```
Because of this, user's can vest less than minimum duration and be treated as if they have vested the minimum duration.
Particularly it is possible to vest for *1 second* and then withdraw as if the amount is vested for *10 days*.

**Impact:** Vesting duration bounds are not protected, users can bypass minimum duration and perform back to back deposit and withdraw, leading to receiving funds without vesting.

**Recommended Mitigation:** Uncomment checks for vesting duration.

**Doryoku:**
Fixed in [d16e369](https://github.com/Warlands-Nft/xbelo/commit/d16e36999cb5f00474fbdb2666ddd7f26a3a31c9).

**Cyfrin:** Verified.
