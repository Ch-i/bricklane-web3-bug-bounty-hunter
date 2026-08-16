---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`launchTeam` self-registers at hop-1 in week 1 and bypasses the week-1-only
  launch-team invite window via the regular `ArmadaCrowdfund::invite` path in weeks
  2-3'
vuln_class: []
---

# `launchTeam` self-registers at hop-1 in week 1 and bypasses the week-1-only launch-team invite window via the regular `ArmadaCrowdfund::invite` path in weeks 2-3

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `launchTeamInvite` (`ArmadaCrowdfund.sol:252-277`) has no `invitee != launchTeam` check. During week 1, `launchTeam` can call `launchTeamInvite(launchTeam, 0)` to self-register at hop-1; stacking the call up to `maxInvitesReceived = 10` yields an outgoing hop-2 budget of `10 * 2 = 20` invites.

After week 1, the regular `invite(invitee, 1)` path (`:224-245`) is gated only by `windowEnd` and has no `msg.sender != launchTeam` check, so `launchTeam` originates hop-2 invites throughout weeks 2–3 via this path. `_addSeed(launchTeam)` (`:185-202`) has the same missing guard. `launchTeam` cannot commit USDC (`:287`, `:358`), so this is a bypass of the week-1 invite-origination constraint, not a capital grab.

**Spec-Intent Gap:**

`specs/CROWDFUND.md` §Word-of-Mouth Whitelist: "launch-team-issued invites originate from a designated `(launch_team_address, ROOT)` sentinel node ... **This node is not a participant and makes no commitment.**"

§Summary of Design Decisions — Invite window: "Launch team: days 1–7 only ... **no new launch team invites can be issued**" after week 1.

Code permits `launchTeam` to become a participant node and originate invites after week 1 — contradicting both commitments.

**Recommended Mitigation:**
```solidity
// in invite():
require(msg.sender != launchTeam, "ArmadaCrowdfund: launchTeam cannot invite via regular path");
// in launchTeamInvite():
require(invitee != launchTeam, "ArmadaCrowdfund: launchTeam cannot be invitee");
// in _addSeed():
require(seed != launchTeam, "ArmadaCrowdfund: launchTeam cannot be a seed");
```

**Armada:** Fixed in commit [ff894b0](https://github.com/ship-armada/armada-poc/commit/ff894b02337212df984dddb762ce0cf61b582f9c).

**Cyfrin:** Verified.
