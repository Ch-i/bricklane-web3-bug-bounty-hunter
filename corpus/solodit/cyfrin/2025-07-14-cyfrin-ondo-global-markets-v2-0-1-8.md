---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-14-cyfrin-ondo-global-markets-v2-0-1-8
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-14-cyfrin-ondo-global-markets-v2-0
title: Natspec enhancements
vuln_class: []
---

# Natspec enhancements

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-14-cyfrin-ondo-global-markets-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md)_

---

**Description:** * [`onUSD_Factory::deployonUSD`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/onUSDFactory.sol#L54-L76) is missing the `complianceView` parameter in its natspec.
* [`onUSD_Factory.onUSDDeployed`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/onUSDFactory.sol#L113-L126) event is missing parameters `name`, `ticker`, and `complianceView`
* [`GMTokenManager::constructor`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/GMTokenManager.sol#L140-L156) is missing `_onUsd` parameter
* [`GMTokenManager::adminProcessMint`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/GMTokenManager.sol#L376-L398) is missing `gmToken` parameter
* [`TokenPauseManager::unpauseAllTokens`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenPauseManager/TokenPauseManager.sol#L105-L113): the text `Only affects tokens paused by the pauseAllTokens function` could be worded better as this is _all_ tokens.

**Ondo:** Fixed in commit [`d7dc414`](https://github.com/ondoprotocol/rwa-internal/pull/471/commits/d7dc4144d42a5edb04a25814f42a677c8b798723)

**Cyfrin:** Verified.
