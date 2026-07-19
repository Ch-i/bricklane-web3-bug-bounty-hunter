---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-1-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Front-running in referral link assignment leading to DoS of the functionality
vuln_class: []
---

# Front-running in referral link assignment leading to DoS of the functionality

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

The NarwhalReferrals.signUp function allows a user to register on the platform with a referral. It takes in two parameters, _user which is the sender’s address and _referral which is the address of the user who referred them. Then the function checks whether the refLinkToUser mapping has a value assigned to the current block number. This assumption allows a malicious user to front-run legitimate calls to the signUp function by calling it within the same block before legitimate users can register, in consequence preventing them from registering with their intended referral. Since the protocol is planned to be deployed on the Arbitrum network, this kind of denial of service attack would be cheap enough to perform.

**Recommendation**: 

Consider using a nonce-based system that is not dependent on the block.number.

**Fixed**: Protocol implemented nonce-based system.
