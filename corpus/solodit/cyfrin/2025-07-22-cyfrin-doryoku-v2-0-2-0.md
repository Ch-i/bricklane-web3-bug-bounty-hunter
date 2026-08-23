---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Consider Two-step Ownership Transfer
vuln_class: []
---

# Consider Two-step Ownership Transfer

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** In both `xbelo` and `clmm_lp_farming` programs, ownership is transferred within one function call, namely `transfer_admin`.
This pattern comes with it risks, any mistake can lead to losing ability to update vesting parameters for `xbelo` program, and losing pausability functionality for `clmm_lp_farming` program considering these functions are only callable by the admin.

**Recommended Mitigation:** Consider implementing two step ownership transfer for safer ownership transfer. This requires two functions:
1- Assigning the next admin: Current admin proposes a `new_admin`.
2- Accepting ownership: `new_admin` accepts ownership.

**Doryoku:**
Fixed in [41676f1](https://github.com/Warlands-Nft/xbelo/commit/41676f1ad0572f9b08fcd53c1d0a4a39b4fb9685) and [fad227e](https://github.com/Warlands-Nft/belo_clmm_lp_farming/commit/fad227e80c53e207a8836365ed0c8449a17f2992).

**Cyfrin:** Verified.
