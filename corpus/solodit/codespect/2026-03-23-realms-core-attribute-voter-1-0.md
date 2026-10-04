---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-03-23-realms-core-attribute-voter-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-03-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-03-23-Realms-Core-Attribute-Voter.md
tags:
- firm:codespect
- report:2026-03-23-realms-core-attribute-voter
title: '[I-01] Not overriding the get_max_size method may lead to unnecessary CU consumption'
vuln_class: []
---

# [I-01] Not overriding the get_max_size method may lead to unnecessary CU consumption

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-03-23-Realms-Core-Attribute-Voter.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-03-23-Realms-Core-Attribute-Voter.md)_

---

**Original severity:** Best Practices

**Files:** [nft_vote_record.rs](https://github.com/Mythic-Project/governance-program-library/blob/b01a5054322e34e22cd017f716a74f4ddea513ab/programs/core-attribute-voter/src/state/nft_vote_record.rs#L40)

**Description:**

The `nft_vote_record` account implements `AccountMaxSize` but does not override the `get_max_size()` function. Because `get_max_size()` returns `None`, when creating the account via `create_and_serialize_account_signed(...)`, the account data is serialized in memory into a byte array to determine its length, rather than using the return value directly to allocate the account space.

**Impact:** This may consume slightly more CU when creating the account.

**Recommendation:** It is recommended to override the `get_max_size()` function when the account size can be determined, returning the actual size of the account.

**Status:** Fixed

**Client response:** Fixed in [5eb76c8b22b56a4fdad7c3311ae1c4f869e07b4a](https://github.com/Mythic-Project/governance-program-library/commit/5eb76c8b22b56a4fdad7c3311ae1c4f869e07b4a).
