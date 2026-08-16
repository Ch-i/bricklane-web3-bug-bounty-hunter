---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-1-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: '`_assertUSDCPrice` breaks the solidity style guide'
vuln_class: []
---

# `_assertUSDCPrice` breaks the solidity style guide

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** The `_assertUSDCPrice` function is public and starts with an underscore. According to the [solidity style guide](https://docs.soliditylang.org/en/latest/style-guide.html), this convention is suggested for non-external functions and state variables (private or internal).

**Recommended Mitigation:** Remove the `_`, or change the visibility of the function.

**Ondo:**
Fixed in commit [fc1c8fb](https://github.com/ondoprotocol/rwa-internal/commit/fc1c8fbd9efb77d4307611d83d7350d869a23e22).

**Cyfrin:** Verified.

\clearpage
