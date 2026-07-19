---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-14-cyfrin-ondo-global-markets-v2-0-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-14-cyfrin-ondo-global-markets-v2-0
title: '`GMTokenManager::mintWithAttestation` breaks Check-Effects-Interactions pattern'
vuln_class: []
---

# `GMTokenManager::mintWithAttestation` breaks Check-Effects-Interactions pattern

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-14-cyfrin-ondo-global-markets-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md)_

---

**Description:** In [`GMTokenManager::mintWithAttestation`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/GMTokenManager.sol#L196-L231), the function transfers tokens from the user before performing internal accounting operations such as rate limiting, burning, and minting. This violates the check-effects-interactions pattern, where external calls (like token transfers) should typically come after all internal state updates to reduce risk.

While the token being transferred is assumed to be a trusted stablecoin, this ordering increases the surface area for unexpected behavior if any integrated token misbehaves (e.g., via callback hooks, pausable logic, or fee-on-transfer behavior).

Consider reordering operations in `mintWithAttestation` to follow the check-effects-interactions pattern—performing rate limiting, burns, and mints **before** calling `token.transferFrom()`.

**Ondo:** Fixed in commit [`29bdeb9`](https://github.com/ondoprotocol/rwa-internal/pull/470/commits/29bdeb92b8de97be3de6a60d78bf91449be90827)

**Cyfrin:** Verified. rate limiting now done before external calls.
