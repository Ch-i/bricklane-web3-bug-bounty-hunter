---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-03-23-realms-core-attribute-voter-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-03-23-Realms-Core-Attribute-Voter.md
tags:
- firm:codespect
- report:2026-03-23-realms-core-attribute-voter
title: '[L-01] NFT ownership change without relinquishing vote leads to rent loss'
vuln_class: []
---

# [L-01] NFT ownership change without relinquishing vote leads to rent loss

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-03-23-Realms-Core-Attribute-Voter.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-03-23-Realms-Core-Attribute-Voter.md)_

---

**Files:** [relinquish_nft_vote.rs](https://github.com/Mythic-Project/governance-program-library/blob/b01a5054322e34e22cd017f716a74f4ddea513ab/programs/core-attribute-voter/src/instructions/relinquish_nft_vote.rs#L141)

**Description:**

The `relinquish_nft_vote(...)` instruction is used to reset the `voter_weight_record` account to close the designated `nft_vote_record` accounts that were created during the voting process. The instruction checks the `governing_token_owner` matches the one stored in `nft_vote_record`:

```rust
require!(
    nft_vote_record.governing_token_owner == *governing_token_owner,
    CoreNftAttributeVoterError::InvalidTokenOwnerForNftVoteRecord
);
```

The problem arises when an NFT owner casts a vote, and sells or transfers the NFT before calling `relinquish_nft_vote(...)`. Once the voting is finalized, and the call can be made to recover the rent, it cannot be done neither by the former or the new NFT owner because of the above validation within the `get_nft_vote_record_data_for_proposal_and_token_owner(...)`.

**Impact:** No impact to voting security, but the rent becomes unrecoverable.

**Recommendation:** Instead of validating against the `nft_vote_record.governing_token_owner` check for NFT ownership, this however can add additional complexity to the instruction.

**Status:** Acknowledged

**Client response:** Based on the code note: *If a voter votes with NFT and transfers the token then in the current version of the program the new owner can’t withdraw the vote. In order to support that scenario a change in spl-governance is needed. It would have to support revoke_vote instruction which would take as input VoteWeightRecord with the following values: weight_action: RevokeVote, weight_action_target: VoteRecord, voter_weight: sum(previous owner NFT weight). The instruction would decrease the previous voter total VoteRecord.voter_weight by the provided VoteWeightRecord.voter_weight. Once the spl-governance instruction is supported then nft-voter plugin should implement revoke_nft_vote instruction to supply the required VoteWeightRecord and delete relevant NftVoteRecords.*
