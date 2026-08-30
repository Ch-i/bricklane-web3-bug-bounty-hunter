---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-2-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Missing mechanism to track Votes
vuln_class: []
---

# Missing mechanism to track Votes

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

There should be a mechanism to track votes for each round of decision. Otherwise it can result in incorrect consensus being calculated in new rounds of decision making. For example, let's say there are 3 users of the Multisig- Alice, Bob and Eve. Let's say in round 1, Alice casted true, Bob casted true and Eve casted false via the vote() function. Now let's say if the numConfirmationsRequired is 2, then the function getStatus() will return true. But let's say now that a new decision is to be made and a new round of Voting starts. This time everyone Votes in the same way except Bob who forgets to vote. In the case the votestatuses of Alice, Bob and Eve should have been true, false and false respectively. But instead it is now true, true and false respectively. This would result in getStatus() again returning as true instead of false. This can lead to inconsistent or incorrect decisions being made.

**Recommendation**: 

It is advised to review business and operational logic and introduce a mechanism to track votes for each round of decision being made. And then reset the voting status before each new round of voting.
