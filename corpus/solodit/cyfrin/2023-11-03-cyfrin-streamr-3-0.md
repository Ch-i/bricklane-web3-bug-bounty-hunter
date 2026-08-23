---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: Redundant requirement
vuln_class: []
---

# Redundant requirement

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

The first requirement is redundant because the second one is enough.

```solidity
File: contracts\OperatorTokenomics\SponsorshipPolicies\VoteKickPolicy.sol
156:         require(reviewerState[target][voter] != Reviewer.NOT_SELECTED, "error_reviewersOnly"); //@audit-issue redundant
157:         require(reviewerState[target][voter] == Reviewer.IS_SELECTED, "error_alreadyVoted");
```

**Client:** We want to give an informative error message for the case where a non-reviewer tries to vote. So: prefer to keep it.

**Cyfrin:** Acknowledged.
