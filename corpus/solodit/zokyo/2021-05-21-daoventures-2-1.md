---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-05-21-daoventures-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-05-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md
tags:
- firm:zokyo
- report:2021-05-21-daoventures
title: Unnecessary ‘public’ keyword for constructor of DAOstake contract
vuln_class: []
---

# Unnecessary ‘public’ keyword for constructor of DAOstake contract

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-05-21-DAOventures.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md)_

---

**Description**

Visibility (public / external) is not needed for constructors anymore: To prevent a contract
from being created, it can be marked abstract. This makes the visibility concept for
constructors obsolete.

**Recommendation**:

Remove ‘public’ keyword from constructor.
