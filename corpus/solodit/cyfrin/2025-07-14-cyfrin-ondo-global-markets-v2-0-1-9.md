---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-14-cyfrin-ondo-global-markets-v2-0-1-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-14-cyfrin-ondo-global-markets-v2-0
title: Missing `nonReentrant` modifier on `GMTokenManager` mint/redeem
vuln_class: []
---

# Missing `nonReentrant` modifier on `GMTokenManager` mint/redeem

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-14-cyfrin-ondo-global-markets-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md)_

---

**Description:** The [`GMTokenManager::mintWithAttestation`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/GMTokenManager.sol#L170-L175) and [`GMTokenManager::redeemWithAttestation`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/GMTokenManager.sol#L248-L253) functions  perform external token transfers and internal state updates but do not use the `nonReentrant` modifier. While `GMTokenManager` inherits from OpenZeppelin's `ReentrancyGuard`, which is currently unused, the modifier is not applied to these functions.

Consider adding the `nonReentrant` modifier to `mintWithAttestation` and `redeemWithAttestation`.

**Ondo:** Fixed in commit [`d7dc414`](https://github.com/ondoprotocol/rwa-internal/pull/471/commits/d7dc4144d42a5edb04a25814f42a677c8b798723)

**Cyfrin:** Verified.

\clearpage
