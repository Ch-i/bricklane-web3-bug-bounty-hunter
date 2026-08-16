---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-13
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Consider enhancing `BTCY::_checkIBTCYTransfer` to also prevent transfers to
  `address(this)`
vuln_class: []
---

# Consider enhancing `BTCY::_checkIBTCYTransfer` to also prevent transfers to `address(this)`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Consider enhancing `BTCY::_checkIBTCYTransfer` to also prevent transfers to `address(this)`; if a user sends BTCY shares to `address(this)`, those shares are effectively burned (held by the vault, never redeemable). While this is a user error, the same protective pattern applied for iBTCY could also cover `address(this)`.

**Aarc:** Fixed in commit [3d5932e](https://github.com/aarc-xyz/btcy-contracts-main/commit/3d5932e246f6c0a5a7a3bb3a74e9bfabc2ea33ab).

**Cyfrin:** Verified.
