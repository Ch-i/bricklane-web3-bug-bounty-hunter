---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-10
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
title: Method `referKOLUnder` does not validate if same address is used for tier2
  and tier3
vuln_class: []
---

# Method `referKOLUnder` does not validate if same address is used for tier2 and tier3

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In NarwhalReferrals contract, the method `referKOLUnder(address _tier3, address _tier2)` does not check if  `_tier3 == _tier2`. In that case, any address will be able to refer itself.
This method is called by owner only so severity is low but adding a check is advised.

**Recommendation**: 

Add the following require statement.
`require(_tier3 != _tier2, “no same addresses”)`
**Fixed**: Issue fixed in commit a72e06b
