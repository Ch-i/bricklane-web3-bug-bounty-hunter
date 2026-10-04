---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-03-23-realms-core-attribute-voter-0-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-03-23-Realms-Core-Attribute-Voter.md
tags:
- firm:codespect
- report:2026-03-23-realms-core-attribute-voter
title: '[L-02] Proposal validation asymmetry may lead to lost rent'
vuln_class: []
---

# [L-02] Proposal validation asymmetry may lead to lost rent

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-03-23-Realms-Core-Attribute-Voter.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-03-23-Realms-Core-Attribute-Voter.md)_

---

**Files:** [cast_nft_vote.rs](https://github.com/Mythic-Project/governance-program-library/blob/b01a5054322e34e22cd017f716a74f4ddea513ab/programs/core-attribute-voter/src/instructions/cast_nft_vote.rs#L73)

**Description:**

In the `cast_nft_vote(...)` we use `resolve_proposal_account(...)` to validate the `proposal` account, but it only checks the program owning the proposal and its state. This allows successful creation of the `asset_vote_record` for a proposal coming from a different realm. While the spl-governance `cast_vote(...)` would fail, it is not necessary to call it within the same instruction (if `cast_nft_vote` is used multiple times in multiple transaction due to high amount of NFTs). In the `relinquish_nft_vote(...)` there is a tighter validation of the `proposal` which needs to match the realm. If the `asset_vote_record` are created for incorrect proposal, it is hence not possible to recover the rent using `relinquish_nft_vote(...)`.

**Impact:** No impact to voting process, but certain incorrectly conducted voting leads to lost rent by the user.

**Recommendation:** Validate the `proposal` in the `cast_nft_vote(...)` in similar way as in `relinquish_nft_vote(...)`, or at least check the `governing_token_mint`.

**Status:** Fixed

**Client response:** Fixed in [5eb76c8b22b56a4fdad7c3311ae1c4f869e07b4a](https://github.com/Mythic-Project/governance-program-library/commit/5eb76c8b22b56a4fdad7c3311ae1c4f869e07b4a).
