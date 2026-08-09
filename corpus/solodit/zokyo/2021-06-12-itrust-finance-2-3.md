---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Re-use local variable
vuln_class: []
---

# Re-use local variable

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

Vault.sol, line 188, “require(msg.value == _AdminFee)”
Variable adminFee was added for gas savings and can be re-used in the expression instead of
_AdminFee.

**Recommendation**:

Re-use local variable
