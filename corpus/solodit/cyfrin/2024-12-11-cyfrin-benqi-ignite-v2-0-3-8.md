---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-8
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Missing modifiers
vuln_class: []
---

# Missing modifiers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** Despite the use of OpenZeppelin libraries for re-entrancy guards and pausable functionality, not all external functions have the `nonReentrant` and pausable modifiers applied, so cross-function re-entrancy may be possible and functions could be called when not intended. Specifically:

- [`Ignite::registerWithStake`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L202), unlike other registration functions, is missing the `whenNotPaused` modifier.
- [`Ignite::registerWithPrevalidatedQiStake`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L361) is missing both the `nonReentrant` and `whenNotPaused` modifiers.
-  [`StakingContract::registerNode`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L400), which calls `Ignite::registerWithPrevalidatedQiStake`, does not have the `whenNotPaused` modifier applied either.
- The `whenPaused` and `whenNotPaused` modifiers are not applied to any of the pausable functions in both contracts. This is not strictly required but prescient to note.

**Recommended Mitigation:** Add the necessary modifiers where appropriate.

**BENQI:** The registration functions call `_register()` which enforces pause checks. The `nonReentrant` modifier was not added to `Ignite::registerWithPrevalidatedStake` since it is a permissioned function with no unsafe external calls. The `whenNotPaused` modifier has been added to `StakingContract::registerNode` in commit [4956824](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/commit/4956824ad9703927c1eab68aa9b2e215cf91f62b).

**Cyfrin:** Verified.
