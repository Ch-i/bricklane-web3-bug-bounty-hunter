---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: '`SecuritizeAmmNavProvider` quote functions don''t reflect execution behavior
  due to missing baseline reset logic'
vuln_class: []
---

# `SecuritizeAmmNavProvider` quote functions don't reflect execution behavior due to missing baseline reset logic

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `SecuritizeAmmNavProvider::quoteBuyBase, quoteSellBase` are supposed to provide price quotes, however they don't simulate the behavior of `_checkAndResetBaseline` which is executed by actual buys and sells performed via `executeBuyBase, executeSellBase`.

**Impact:** Actual price execution can differ from the quoted price; the quotes may not be accurate because they don't simulate the `_checkAndResetBaseline` logic.

**Recommended Mitigation:** Either document this limitation clearly or implement the baseline reset simulation in quote functions (though this adds complexity to `view` functions).

**Securitize:** Fixed in commits [71e40b8](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/71e40b8fd5387aa8382cb85fe0de0c89ad399125), [d05482b](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/d05482b2d42a2c9df7451affb634444e5f545f51).

**Cyfrin:** Verified.
