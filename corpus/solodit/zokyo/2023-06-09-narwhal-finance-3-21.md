---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-21
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: No need to initialise variable to their default values
vuln_class: []
---

# No need to initialise variable to their default values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In TradingVaultV2, these variables periodFinish & rewardRate is initialized to 0 which is not necessary as storage variable are by default initialized to their default values.

**Recommendation**: 

update it to remove the initialization with the default values.

**Fixed**: Issue fixed in commit a72e06b
