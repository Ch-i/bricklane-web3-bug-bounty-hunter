---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: If zero xp is earned by all users, once game has concluded `SessionManager::claimRewards`
  panic reverts due to division by zero but game also can't be cancelled resulting
  in locked tokens
vuln_class: []
---

# If zero xp is earned by all users, once game has concluded `SessionManager::claimRewards` panic reverts due to division by zero but game also can't be cancelled resulting in locked tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `ProportionalToXPReward::getReward` divides by `totalXP`, but if none of the users have earned XP, this will panic revert due to division by zero:
```solidity
uint256 userXP;
uint256 totalXP;
for (uint256 i; i < winners.length; ++i) {
    (, uint256 xp,) = sessionStrategy.userResult(sessionId, winners[i]);
    if (i == position) {
        userXP = xp;
    }
    totalXP += xp;
}
reward = userXP * prizePool / totalXP;
```

`DefaultSession::setXPTiers` does not enforce non-zero xp tiers, it only enforces that at least two tiers must exist:
```solidity
function setXPTiers(uint256 gameId, uint256[] calldata _xpTiers) external {
    require(
        msg.sender == SessionManager(sessionManager).getCreator(gameId),
        NotGameCreator(SessionManager(sessionManager).getCreator(gameId), msg.sender)
    );
    require(_xpTiers.length >= 2, ArrayLengthMismatch());
    require(xpTiers[gameId].length == 0, XpTiersAlreadySet(gameId));
    require(SessionManager(sessionManager).getSessionState(gameId) == SessionState.Created, GameNotCreated(gameId));
    xpTiers[gameId] = _xpTiers;
    emit XpTiersSet(gameId, _xpTiers);
}
```

**Impact:** If zero xp is earned by all users, once game has concluded `SessionManager::claimRewards` panic reverts due to division by zero but game also can't be cancelled because it is in the `Concluded` state, resulting in locked tokens.

**Recommended Mitigation:** Consider enforcing minimum value of 1 for every xp tier in `DefaultSession::setXPTiers`.

**Majority Games:**
Fixed in commit [951a454](https://github.com/Engage-Protocol/engage-protocol/commit/951a45490d2867f80dbf56bb4ce915c44a9a1281) by enforcing non-zero values for every xp tier and also capping xp tiers to max 20.

**Cyfrin:** Verified.
