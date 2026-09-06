---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-15
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Tokens that were locked when `lockUpTime > 0` will be impossible to unlock
  if `lockUpTime` is set to zero
vuln_class: []
---

# Tokens that were locked when `lockUpTime > 0` will be impossible to unlock if `lockUpTime` is set to zero

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `LockUpManager::_unlockTokens` returns if `lockUpTime == 0`:
```solidity
function _unlockTokens(
    address holder,
    uint256 amount,
    bool disregardTime
) internal {
    LockUpStorage storage $ = _getLockUpStorage();
    uint32 lockUpTime = $._lockUpTime;
    // @audit returns if `lockUpTime == 0`
    if (lockUpTime == 0 || amount == 0) return;
```

**Impact:** Tokens that were locked when `lockUpTime > 0` will be impossible to unlock if `lockUpTime` is subsequently set to zero. Initially this won't cause any problems and users will be able to transfer tokens as normal, but if `lockUpTime` is changed to be greater than zero it will start to cause accounting-related problems as one of the protocol invariants is that the amount of tokens a user has locked should be <= to the token balance of the user.

This invariant would be violated since the lockups would still be present but the user could have transferred their tokens, causing underflow reverts in transfers when determine unlocked balance: `uint256 unlockedBalanceToSend = balance - getTokensLocked(sender);`

**Recommended Mitigation:** Even if `lockUpTime == 0`, proceed through to the `for` loop iterating over all token locks to unlock them. This maintains the  protocol invariant that the amount of tokens a user has locked is <= the user's token balance.

**Remora:** Fixed in commit [5db7f11](https://github.com/remora-projects/remora-smart-contracts/commit/5db7f11427f6e767a6042c443d552ee9c024494b).

**Cyfrin:** Verified.
