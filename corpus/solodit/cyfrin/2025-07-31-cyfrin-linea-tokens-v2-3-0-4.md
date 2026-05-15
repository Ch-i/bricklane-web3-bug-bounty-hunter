---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-31-cyfrin-linea-tokens-v2-3-0-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-31T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-31-cyfrin-linea-tokens-v2.3.md
tags:
- firm:cyfrin
- report:2025-07-31-cyfrin-linea-tokens-v2-3
title: Unused AccessControl in `L2LineaToken`
vuln_class: []
---

# Unused AccessControl in `L2LineaToken`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-31-cyfrin-linea-tokens-v2.3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-31-cyfrin-linea-tokens-v2.3.md)_

---

**Description:** `L2LineaToken` inherits `AccessControlUpgradeable` and grants `DEFAULT_ADMIN_ROLE` on initialization, but none of its functions (`mint`, `burn`, `syncTotalSupplyFromL1`) are protected by role checks. As a result, the AccessControl machinery isn’t actually enforcing any permissions. Consider removing `AccessControlUpgradeable`.

**Linea:** Acknowledged. Intentionally left in so that it is not forgotten in the future.

\clearpage
