---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-27
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Add Missing Events in Critical functions
vuln_class: []
---

# Add Missing Events in Critical functions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

The NarwhalReferrals contract is missing events for critical functions such as signUp, changeReferralLink, referKOLUnder, incrementRewards, and incrementTier2Tier3. This can potentially lead to a security vulnerability, as it makes it more difficult for external parties to track and audit the actions taken by the contract.
In particular, the signUp function is a critical function, as it determines the user's initial referral link and referral source. Without an event to track this, it would be difficult for external parties to verify the integrity of the referral system. Additionally, the changeReferralLink function allows a user to change their referral source, and the lack of an event for this function could make it difficult to track when and how referral links are being changed.

**Recommendation** : 


Add events to this critical functions

**Fixed**: Issue fixed in commit a72e06b
