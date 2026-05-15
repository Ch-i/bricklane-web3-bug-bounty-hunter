---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-07-21-itrustfinance-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2021-07-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-21-ITrustFinance.md
tags:
- firm:zokyo
- report:2021-07-21-itrustfinance
title: Usage of standard libraries is preferrable
vuln_class: []
---

# Usage of standard libraries is preferrable

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-07-21-ITrustFinance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-21-ITrustFinance.md)_

---

**Description**

To transfer admin rights, it is recommended to use the OZ AccessControl library.
To protect against reentry it is recommended to use the OZ ReentrancyGuard library.
For assigning roles and adding admins, it is recommended to use the OZ AccessControl
library.
For pausable functionality it is recommended to use the OZ Pausable library.
This approach will help in elimination of possible bugs, simplify the codebase and increase the
overall code quality.

**Recommendation**:

Consider usage of standard openzeppelin libraries.
