---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-14-cyfrin-ondo-global-markets-v2-0-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-14-cyfrin-ondo-global-markets-v2-0
title: Inconsistent unpause role in `onUSD`
vuln_class: []
---

# Inconsistent unpause role in `onUSD`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-14-cyfrin-ondo-global-markets-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md)_

---

**Description:** [`onUSD::unpause`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/onUSD.sol#L200-L202) is restricted to `DEFAULT_ADMIN_ROLE`, unlike other contracts in the system that use a dedicated `UNPAUSER_ROLE`. This breaks consistency in access control design and limits flexibility in delegating unpause authority:
```solidity
function unpause() public override onlyRole(DEFAULT_ADMIN_ROLE) {
  _unpause();
}
```

Consider using `UNPAUSER_ROLE` for `onUSD::unpause` to align with the pattern used across other contracts.

**Ondo:** Fixed in commit [`650c527`](https://github.com/ondoprotocol/rwa-internal/pull/470/commits/650c527100dbb655e9a485a5568c7796fdde3cc1)

**Cyfrin:** Verified.`UNPAUSER_ROLE` used in `USDon::unpause` (renamed)
