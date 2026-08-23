---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: '`SecuritizeAmmNavProvider` missing `whenNotPaused` modifier on important state-changing
  functions'
vuln_class: []
---

# `SecuritizeAmmNavProvider` missing `whenNotPaused` modifier on important state-changing functions

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `SecuritizeAmmNavProvider` inherits from `BaseContract` which inherits from `PausableUpgradeable`, but does not have the `whenNotPaused` modifier on important state-changing functions.

**Impact:** Pausing `SecuritizeAmmNavProvider` has no effect; important state-changing functions can continue to be called even when the contract is paused. Looking at the other NAV providers this doesn't seem to be intended, eg  `SecuritizeInternalNavProvider::setRate` has the `whenNotPaused` modifier.

**Recommended Mitigation:** Add the `whenNotPaused` modifier to important state-changing functions such as `SecuritizeAmmNavProvider::resetBaseline, setPriceScaleFactor, executeBuyBase, executeSellBase`.

**Securitize:** Fixed in commit [f09cb9a](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/f09cb9a621b2fee4890d4cca7b952ec0398a6d1e).

**Cyfrin:** Verified.
