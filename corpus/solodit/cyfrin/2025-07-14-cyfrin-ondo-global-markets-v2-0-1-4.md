---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-14-cyfrin-ondo-global-markets-v2-0-1-4
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
title: Unnecessary boolean comparisons in `GMTokenManager`
vuln_class: []
---

# Unnecessary boolean comparisons in `GMTokenManager`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-14-cyfrin-ondo-global-markets-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md)_

---

**Description:** Both in [`GMTokenManager::_verifyQuote#L329`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/GMTokenManager.sol#L329) and [`GMTokenManager::adminProcessMint#L389`](http://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/GMTokenManager.sol#L389) there's a boolean comparison:
```solidity
if (gmTokenAccepted[gmToken] == false) revert GMTokenNotRegistered();
```
This is redundant. Consider simplifying it to:
```solidity
if (!gmTokenAccepted[gmToken]) revert GMTokenNotRegistered();
```

**Ondo:** Fixed in commit [`1877211`](https://github.com/ondoprotocol/rwa-internal/pull/470/commits/1877211865727c6ae6e1587550266a43973d722c)

**Cyfrin:** Verified.
