---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-17
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Users Cannot Change Their Vote Once Cast in a Voting Period
vuln_class: []
---

# Users Cannot Change Their Vote Once Cast in a Voting Period

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The voting system prevents users from changing or revoking their votes once they have voted in a voting round. While this maybe an intentional design to prevent duplicate voting, it may impact user experience if users make mistakes or want to change their vote before the voting period ends.

In `voting`, the system checks if a user has already voted:

```rust
if client_community_state.header.last_voting_counter
    >= client_community_state.header.current_voting_counter
{
    bail!(AlreadyVoted);
}
```

After a successful `vote`, `last_voting_counter` is set to the current `voting_counter`, which prevents the user from voting again in the same round, even if they want to:
- Correct a mistaken vote
- Change their vote choice (e.g., from INCREMENT to DECREMENT)
- Revoke their vote

**Impact:** Users who make mistakes cannot correct them or they cannot change their vote if they change their mind during the voting period.

**Recommended Mitigation:** Consider allow vote changes with proper accounting.

**Deriverse:** Fixed in commit [1689196](https://github.com/deriverse/protocol-v1/commit/1689196a00d0f06adc8de510dc5f2806fbd7c0d9).

**Cyfrin:** Verified.
