---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-2-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: No check for address(0)
vuln_class: []
---

# No check for address(0)

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In Contract VaultETH_V2, the method transferOwnership(address newOwner) does not check if the `address newOwner`  is address(0) or not. If it is set by mistake then it will be irreversible.

In Contract VaultETH_V2, the method UpdateRiskManager(...) does not check if `address to` is address(0) or not. If set by mistake, the Risk Manager ratio will be set to address(0).

**Recommendation**: Update the above methods to add validations for address(0) check.
