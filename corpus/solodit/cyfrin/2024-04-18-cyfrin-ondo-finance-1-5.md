---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-1-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Consider allowing `ROUSG::burn` to burn dust amounts
vuln_class: []
---

# Consider allowing `ROUSG::burn` to burn dust amounts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** `ROUSG::burn` is used by admins to burn `rOUSG` tokens from any account for regulatory reasons.

It does not allow burning a share amount smaller than 1e4, because this is less than a wei of `OUSG`.

```solidity
if (ousgSharesAmount < OUSG_TO_ROUSG_SHARES_MULTIPLIER)
      revert UnwrapTooSmall();
```

Depending on the current and future regulatory situation it could be necessary to always be able to burn all shares from users.

**Recommended Mitigation:** Consider allowing the `burn` function to burn all remaining shares even if under the minimum amount.

**Ondo:**
Fixed in commit [2aa437a](https://github.com/ondoprotocol/rwa-internal/commit/2aa437aa78435fc4533c3a9d223460da34e71647).

**Cyfrin:** Verified.
