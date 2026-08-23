---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-3-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Same user can join the same game multiple times increasing their chance of
  winning by preventing other players from participating
vuln_class: []
---

# Same user can join the same game multiple times increasing their chance of winning by preventing other players from participating

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `SessionManager::joinGame` doesn't validate whether the user joining has already joined. As long as the game is still in the `Created` state, the same user can join multiple times each time incrementing `numContestants`.

**Impact:** The same user can take all or most of the available player positions massively increasing their chances of winning since less players are able to compete against them. When `MajorityChoicePrompt` is used this could be especially powerful.

Games have an optional `verificationRequired` "whitelist" feature to prevent the same player using multiple addresses from taking over a game, but a player can abuse this bug to bypasses the `verificationRequired` option since the same whitelisted address can join the same game multiple times preventing other players from joining.

**Recommended Mitigation:** `SessionManager::joinGame` should revert if `contestants[_gameId][msg.sender] == true`. Consider wrapping this into a modifier `onlyNotJoinedGame` and putting that modifier onto `joinGame`.

**Majority Games:**
Fixed in commit [2bba52d](https://github.com/Engage-Protocol/engage-protocol/commit/2bba52d8a8dfecf45566b2d0b1790161102becd2).

**Cyfrin:** Verified.
