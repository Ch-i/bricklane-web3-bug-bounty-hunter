---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-19
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Missing Zero Check Validation in setMaxNegativePnlOnOpenP Function
vuln_class: []
---

# Missing Zero Check Validation in setMaxNegativePnlOnOpenP Function

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**:

The setMaxNegativePnlOnOpenP function in the PairInfos contract sets the maximum negative profit and loss percentage that can be incurred on opening a trade. However, there is no check for whether the value passed as the input parameter is zero, which could lead to unexpected results.
If a manager passes a value of zero as the input parameter, it would effectively disable the maximum negative PnL check, which could result in trades being opened that incur significantly higher losses than expected. 

**Recommendation**:

To address this vulnerability, a zero check validation should be added to the setMaxNegativePnlOnOpenP function to prevent the input parameter from being set to zero. This would ensure that the maximum negative PnL check is always enforced, which would help to prevent unexpected losses.

**Fixed**: Issue fixed in commit a72e06b
