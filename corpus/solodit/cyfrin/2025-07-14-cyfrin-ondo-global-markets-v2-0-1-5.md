---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-14-cyfrin-ondo-global-markets-v2-0-1-5
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
title: Inconsistent type usage for `IssuanceHours.HOUR_IN_SECONDS`
vuln_class: []
---

# Inconsistent type usage for `IssuanceHours.HOUR_IN_SECONDS`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-14-cyfrin-ondo-global-markets-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md)_

---

**Description:** In `IssuanceHours` the constant [`IssuanceHours.HOUR_IN_SECONDS`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/issuanceHours/IssuanceHours.sol#L38) field is declared as `uint`, while the rest of the codebase consistently uses `uint256`:
```solidity
/// Constant for the number of seconds in an hour
uint constant HOUR_IN_SECONDS = 3_600;
```

Consider updating the field to use `uint256` to align with the project's standard type declarations.

**Ondo:** Fixed in commit [`fe452a1`](https://github.com/ondoprotocol/rwa-internal/pull/470/commits/fe452a120f8afde757d19736c44b26d4b07fbca3)

**Cyfrin:** Verified. `HOUR_IN_SECONDS` uses type `int256` (since that removes a cast in `_validateTimezoneOffset`)
