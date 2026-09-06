---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-14
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`IBTCY::_checkBTCYVaultTransfer` bypassed for `mint`'
vuln_class: []
---

# `IBTCY::_checkBTCYVaultTransfer` bypassed for `mint`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `IBTCY::transfer, transferFrom` call to prevent transfers to the `BTCY` vault, however there is no similar check inside `mint` enabling tokens to be minted to the `BTCY` vault.

This allows `MINTER_ROLE` to directly mint `IBTCY` tokens to the `BTCY` vault which effectively donates assets that inflate `BTCY` share value.

If this is intended it should be explicitly noted in comments, otherwise it should be prevented.

**Aarc:** Acknowledged; added explicit comment in commit [261ffb7](https://github.com/aarc-xyz/btcy-contracts-main/commit/261ffb743191de740b60bb1de8d388bcf78b94f5).
