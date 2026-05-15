---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Missing zero address validation for `setCollateralWallet` in SEuroOffering.
vuln_class: []
---

# Missing zero address validation for `setCollateralWallet` in SEuroOffering.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

SEuroOffering.sol, in setCollateralWallet(address): input address is not asserted to be non-zero address.

**Recommendation**

require statement

**Re-audit comment**

Unresolved
