---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Fees can be set greater than 100%
vuln_class: []
---

# Fees can be set greater than 100%

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

The variables managementFee and performanceFee can be updated using function setManagementFee() and setPerformanceFee() respectively. Although these functions have onlyRole(GOVERNANCE) function modifier, the contract allows setting these values to an arbitrarily high value, which could be greater than 100%.

**Recommendation**: 

Add validation while updating fee values in setManagementFee() and setPerformanceFee() such that new values are within acceptable limits. E.g. not more than 100%.

**Comment**: Multisig keys will be distributed and the signers will validate the fees before being set
