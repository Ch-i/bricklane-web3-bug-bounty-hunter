---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: Variables need not be initialized to zero
vuln_class: []
---

# Variables need not be initialized to zero

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

The default value for variables is zero, so initializing them to zero is redundant.

```solidity
File: contracts\OperatorTokenomics\SponsorshipPolicies\DefaultLeavePolicy.sol
10:           uint public penaltyPeriodSeconds = 0;

File: contracts\OperatorTokenomics\SponsorshipPolicies\VoteKickPolicy.sol
100:         uint sameSponsorshipPeerCount = 0;
226:         uint rewardsWei = 0;
```

**Client:** Fixed in commit [c847fab](https://github.com/streamr-dev/network-contracts/commit/c847fab3e57f1f2dc3aa26e8cb79d44c8ed86f5e).

**Cyfrin:** Verified.
