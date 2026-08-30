---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-14-cyfrin-ondo-global-markets-v2-0-1-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-14-cyfrin-ondo-global-markets-v2-0
title: Inconsistent role for `GMTokenManager::setIssuanceHours`
vuln_class: []
---

# Inconsistent role for `GMTokenManager::setIssuanceHours`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-14-cyfrin-ondo-global-markets-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md)_

---

**Description:** The [`GMTokenManager::setIssuanceHours`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/GMTokenManager.sol#L400-L410) function is restricted to `CONFIGURER_ROLE`, whereas other configuration and role assignment functions across the system are typically restricted to `DEFAULT_ADMIN_ROLE`. This inconsistency may cause confusion about which roles are responsible for governance and configuration actions.

Consider aligning access control by restricting `setIssuanceHours` to `DEFAULT_ADMIN_ROLE`, consistent with similar configuration functions elsewhere.

**Ondo:** Fixed in commit [`3d18299`](https://github.com/ondoprotocol/rwa-internal/pull/470/commits/3d18299bab888ef204073581d92ffbc3de13ad30)

**Cyfrin:** Verified. `DEFAULT_ADMIN_ROLE` is now used for `GMTokenManager::setIssuanceHours`.
