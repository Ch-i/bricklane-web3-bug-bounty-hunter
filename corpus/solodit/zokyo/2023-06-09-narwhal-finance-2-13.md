---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-13
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
title: Use nonReentract modifier for claimRewards method
vuln_class: []
---

# Use nonReentract modifier for claimRewards method

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In NarwhalReferrals contract, add nonReentract modifier to the claimRewards method, just as added for signUp() and changeReferralLink() methods, as it transfer tokens and makes external calls.

**Recommendation**: 

Use nonReentrant modifier.

**Fixed**: Issue fixed in commit a72e06b
