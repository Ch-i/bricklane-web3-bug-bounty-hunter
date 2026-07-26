---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-5-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Prefer `calldata` to `memory` for external read-only function inputs
vuln_class: []
---

# Prefer `calldata` to `memory` for external read-only function inputs

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** Prefer `calldata` to `memory` for external read-only function inputs:
* `SessionManager::createGame` & `QuestionManager::_commitQuestions`:
```solidity
224:        bytes32[] memory _promptHashes,
225:        address[] memory _promptStrategies,

45:    function _commitQuestions(uint256 _gameId, bytes32[] memory _questionHashes, address[] memory _promptStrategies)
```

* `DefaultSession::setXPTiers`:
```solidity
100:    function setXPTiers(uint256 gameId, uint256[] memory _xpTiers) external {
```

**Majestic Games:**
Fixed in commit [be290a6](https://github.com/Engage-Protocol/engage-protocol/commit/be290a6eae3b11b32c40699af6b7d072bbcf85d3).

**Cyfrin:** Verified.
