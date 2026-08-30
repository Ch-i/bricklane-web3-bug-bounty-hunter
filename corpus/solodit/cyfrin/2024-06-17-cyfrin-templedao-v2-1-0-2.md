---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-0-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: The delegator resetting self-delegation causes multiple issues in the protocol
vuln_class: []
---

# The delegator resetting self-delegation causes multiple issues in the protocol

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** Whenever the vote power of delegators are changed, the validity of self-delegation of the delegator is not checked, which results in issues in multiple parts of the protocol.

- `unsetUserVoteDelegate`: It does not allow stakers to unset delegation through the function because it tries to subtract delegated balance from zero.
- `_withdrawFor`: It does not allow stakers to withdraw their assets because it tries to subtract delegated balance from zero.
- `_stakeFor`: It allows malicious stakers to get infinite voting power by repeating staking & modifying delegator & withdrawal process.

**Impact:** It allows attackers to repeat issues in `_stakeFor` to accumulate voting power, also it causes reverts in withdrawals.

**Proof of Concept:** Here's a scenario where a malicious attacker can get infinite voting power by repeating the following process:

1. Staker delegates to Bob.
2. Bob resets self-delegation.
3. The staker stakes the token.
4. The staker changes the delegation to another party.

**Recommended Mitigation:** In 3 functions above, it should validate if the delegator has self-delegation enabled at the time of function call.

**TempleDAO:** Fixed in [PR 1034](https://github.com/TempleDAO/temple/pull/1034)

**Cyfrin:** Verified

\clearpage
