---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-12
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: No events are emitted
vuln_class: []
---

# No events are emitted

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In NarwhalReferrals contract, no state changing methods emit events. It is advised to emit events atleast for claimRewards(), changeReferralLink() and signUp() methods.

**Recommendation**: 

Emit events for the suggested methods.

**Fixed**: Issue fixed in commit a72e06b
