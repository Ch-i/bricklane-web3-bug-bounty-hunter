---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-11
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`DepositWithdraw, IBTCYHub, Pricer` allow only default admin to revoke role
  in contrast to the other contracts'
vuln_class: []
---

# `DepositWithdraw, IBTCYHub, Pricer` allow only default admin to revoke role in contrast to the other contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `BTCY` and `IBTCY` override `renounceRole, revokeRole` to prevent an only `DEFAULT_ADMIN_ROLE` from renouncing their role.

However the `DepositWithdraw, IBTCYHub, Pricer` contracts don't have a similar restriction; consider adding it if required.

**Aarc:** Fixed in commit [ae685aa](https://github.com/aarc-xyz/btcy-contracts-main/commit/ae685aa5ca8655b02cdd23239bb5f6581b989311).

**Cyfrin:** Verified.
