---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-0-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Inconsistent math
vuln_class: []
---

# Inconsistent math

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Medium

**Status**: Acknowledged

**Description**

In contract FEYTraderJoeProduct, the math for _depositableJrTokens is inconsistent with the math for _depositableSrTokens in the invest() function. This is because,
 _depositableJrTokens = notionalMaxJr / Constants.DECIMAL_FACTOR

When we substitute notionalMaxJr, we get 
_depositableJrTokens = (productConfig.leverageThresholdMin * _srTotal.wadMul(_jrToSrRate) ) / Constants.DECIMAL_FACTOR

which is inconsistent and different from the formula for  _depositableSrTokens on line: 262-
_depositableSrTokens = (_jrTotal.wadMul(_srToJrRate) * Constants.DECIMAL_FACTOR) / (productConfig.leverageThresholdMax);

Logically, the Decimal factor should have been in the denominator for both  _depositableJrTokens and _depositableSrTokens or in the numerator simultaneously. The same goes for the leverageThreshold variables.

**Recommendation**: 

It is advised to review the math, its logic and formulae for the same.

**Comment**: The client acknowledged the issue, stating that the math derived is correct.
