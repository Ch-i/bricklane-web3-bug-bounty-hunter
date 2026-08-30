---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Voting is allowed even after voting period's end time.
vuln_class: []
---

# Voting is allowed even after voting period's end time.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `voting()` function does not validate whether the voting period has ended before processing and recording votes. The function only checks the voting end time in the `finalize_voting()` call at the very end, but by that point the user's vote has already been cast and included in the voting tallies. This allows the last user to submit a vote even after the official voting period has expired, as long as they call the function before anyone else triggers the finalization.
```rust
//here vote has been included even if end time has been passed of this period
        match data.choice {
            VoteOption::DECREMENT => {
                community_account_header.voting_decr += voting_tokens;
            }
            VoteOption::INCREMENT => {
                community_account_header.voting_incr += voting_tokens;
            }
            _ => community_account_header.voting_unchange += voting_tokens,
        }
....
// the call to finalize voting is made later, so the late user's vote has been included
        community_state.finalize_voting(time, clock.slot as u32)?;
```
**Impact:**
- Malicious actors can cast votes after the voting period has officially ended
-  Late voter(if is holding many tokens) gain knowledge of current vote tallies and can strategically vote to influence outcomes in his favor.

**Recommended Mitigation:** Implement a check which errors when user tries to cast vote affter official `CommunityState.header.voting_end_time` time prior to casting vote & making call to `finalize voting`

**Deriverse**
Fixed in commit: [a5194d]9https://github.com/deriverse/protocol-v1/commit/a5194d26218f0828e83481ebb2a6f7071773b13a)

**Cyfrin:** Verified.
