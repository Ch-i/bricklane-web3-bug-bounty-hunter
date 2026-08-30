---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-8
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Change `Box` struct to use `uint128` saves 1 storage slot per `Box`
vuln_class: []
---

# Change `Box` struct to use `uint128` saves 1 storage slot per `Box`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** The current `Box` struct looks like this:
```solidity
  struct Box {
    uint256 blockTs;
    uint256 tier;
  }
```

This will require 2 storage slots for each `Box`. However neither `blockTs` nor `tier` require `uint256`; both can be changed to `uint128` which will pack each `Box` into 1 storage slot:

```solidity
  struct Box {
    uint128 blockTs;
    uint128 tier;
  }
```

This will halve the number of storage reads/writes when reading/writing boxes from/to storage.

**Mode:**
Fixed in commit [88c5f55](https://github.com/Earnft/dropbox-smart-contracts/commit/88c5f55d75d69aa2ba66779e27cddf47bddfac14#diff-3c794fa0376b06334bb77ee613047755475945d090c0853efd4cd33ddd57d6d4L9-R10).

**Cyfrin:** Verified.
