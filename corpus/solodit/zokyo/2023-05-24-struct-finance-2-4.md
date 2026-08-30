---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-2-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Wrong Function visibility.
vuln_class: []
---

# Wrong Function visibility.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Informational

**Status**: Unresolved

**Description**

In contract DistributionManager:
getRecipients: this function was not called internally in the contracts, but it was declared as public

**Recommendation**: 

declare it as an external
_validateRecipientConfig: this function doesn’t need to be called externally.

**Recommendation**: 

declare it as an internal
In contract GACManaged.sol -
pause: this function was not called internally in the contracts, but it was declared as public

unpause: this function was not called internally in the contracts, but it was declared as public

**Recommendation**: 

declare it as an external
