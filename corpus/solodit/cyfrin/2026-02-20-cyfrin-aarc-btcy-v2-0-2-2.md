---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`ERC4626::deposit,redeem,mint,withdraw` should revert if they would return
  zero'
vuln_class: []
---

# `ERC4626::deposit,redeem,mint,withdraw` should revert if they would return zero

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** It is good defensive practice to revert if `ERC4626::deposit,redeem,mint,withdraw` would return zero since it never makes sense for these functions to return zero when provided with non-zero inputs; such behavior is only used by blackhats to manipulate vaults commonly via "stealth donation" attacks. Affected contracts:

* `BTCY.sol`

**Aarc:** Fixed in commit [b40ab8a](https://github.com/aarc-xyz/btcy-contracts-main/commit/b40ab8a4dd6dbdaf67abc63ae23ec836d5d83c82).

**Cyfrin:** Verified.
