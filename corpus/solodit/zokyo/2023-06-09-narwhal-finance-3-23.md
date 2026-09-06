---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-23
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: No  need to use `storage` reference
vuln_class: []
---

# No  need to use `storage` reference

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In NarwhalReferrals contract, in the method `referKOLUnder(address _tier3, address _tier2)`, the referralDetails accessed on line#139 and line#140 uses storage reference variables. As these values are not modified in the method, memory reference can be used as well.

**Recommendation**: 

Update storage reference to memory on line#139 and line#140.

**Fixed**: Issue fixed in commit a72e06b
