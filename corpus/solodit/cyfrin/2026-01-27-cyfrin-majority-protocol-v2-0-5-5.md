---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-5-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: More efficient implementation of `SessionManager::joinGame` via better storage
  packing
vuln_class: []
---

# More efficient implementation of `SessionManager::joinGame` via better storage packing

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `SessionManager::joinGame` performs these 4 storage reads:
```solidity
// reads games[_gameId].state up to 2 times
require(
    games[_gameId].state == SessionState.Created || games[_gameId].state == SessionState.Ongoing,
    InvalidGameState(SessionState.Created, games[_gameId].state)
);
// reads games[_gameId].numContestants once
require(
    games[_gameId].numContestants < maximumContestants,
    TooManyContestants(maximumContestants, games[_gameId].numContestants)
);
// reads games[_gameId].verificationRequired once
if (games[_gameId].verificationRequired) {
    require(isVerificationApproved[msg.sender], NotVerified(msg.sender));
}
```

The `Game` struct can be refactored to pack `state`, `numContestants` and `verificationRequired` into the same storage slot like this:
```solidity
struct Game {
    uint256 gameId;
    uint256 startTime;
    uint256 endTime;
    address sessionStrategy;
    address rewardStrategy;
    uint256 originalStartTime;
    address creator;
    address creatorfeeReceiver;
    uint32 numContestants;
    SessionState state;
    bool verificationRequired;
}
```

Then all 3 can be read inside `SessionManager::joinGame` through just one storage read:
```solidity
Game storage gameRef = games[_gameId];
(uint32 numContestants, SessionState state, bool verificationRequired)
    = (gameRef.numContestants, gameRef.state, gameRef.verificationRequired);

// remaining checks/processing follows as normal
```

**Majority Games:**
Fixed in commit [c7eafa2](https://github.com/Engage-Protocol/engage-protocol/commit/c7eafa2037270b0358e37c6f547950a37df01fe6).

**Cyfrin:** Verified.
