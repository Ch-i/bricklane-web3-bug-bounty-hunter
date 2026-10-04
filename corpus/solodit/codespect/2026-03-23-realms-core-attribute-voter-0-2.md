---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-03-23-realms-core-attribute-voter-0-2
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
title: '[L-03] Setting max_voter_weight_expiry to a non-None value in the update_max_voter_weight_record(...)
  instruction increases overhead for governance users'
vuln_class: []
---

# [L-03] Setting max_voter_weight_expiry to a non-None value in the update_max_voter_weight_record(...) instruction increases overhead for governance users

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-03-23-Realms-Core-Attribute-Voter.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-03-23-Realms-Core-Attribute-Voter.md)_

---

**Files:** [update_max_voter_weight_record.rs](https://github.com/CODESPECT-security/061-Realms-Voter/blob/69c6e8fc091ef17a5cec828b484ed633c6e047b5/programs/core-attribute-voter/src/instructions/update_max_voter_weight_record.rs#L35)

**Description:**

The `max_voter_weight_record` stores the total weight of the collections configured in the `registrar`, and this value is used in spl-gov to calculate the `max_voter_weight`. When the `configure_collection(...)` instruction updates a `registrar`’s collection configuration, the `max_voter_weight_record` is updated with `max_voter_weight_expiry` set to [`None`](https://github.com/CODESPECT-security/061-Realms-Voter/blob/69c6e8fc091ef17a5cec828b484ed633c6e047b5/programs/core-attribute-voter/src/instructions/configure_collection.rs#L114). Because `max_voter_weight` only changes during such updates, this setting can avoid bundling a call to the `update_max_voter_weight_record(...)` instruction during [spl-gov operations](https://github.com/Mythic-Project/solana-program-library/blob/5afaf6f5c85700277a54584d85ef737fda0a8903/governance/program/src/addins/max_voter_weight.rs#L18) to update it. However, the [`update_max_voter_weight_record(...)`](https://github.com/CODESPECT-security/061-Realms-Voter/blob/69c6e8fc091ef17a5cec828b484ed633c6e047b5/programs/core-attribute-voter/src/instructions/update_max_voter_weight_record.rs#L35) instruction incorrectly sets `max_voter_weight_expiry` to the current slot instead of `None`.

**Impact:** Anyone can call the `update_max_voter_weight_record(...)` instruction to set `max_voter_weight_expiry` to a non-None value, forcing governance participants to bundle a call to `update_max_voter_weight_record(...)` in related operations.

**Recommendation:** It is recommended that the `update_max_voter_weight_record(...)` instruction should not set `max_voter_weight_expiry` to a non-None value.

**Status:** Fixed

**Client response:** Fixed in [5eb76c8b22b56a4fdad7c3311ae1c4f869e07b4a](https://github.com/Mythic-Project/governance-program-library/commit/5eb76c8b22b56a4fdad7c3311ae1c4f869e07b4a).
