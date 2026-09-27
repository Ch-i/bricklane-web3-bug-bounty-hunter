---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-02-11-tempest-bridge-oracle-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-02-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-02-11-Tempest-Bridge-Oracle.md
tags:
- firm:codespect
- report:2025-02-11-tempest-bridge-oracle
title: '[I-01] Initially isSequencerDown is false which may incorrectly allow price
  feed calls'
vuln_class: []
---

# [I-01] Initially isSequencerDown is false which may incorrectly allow price feed calls

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-02-11-Tempest-Bridge-Oracle.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-02-11-Tempest-Bridge-Oracle.md)_

---

**Files:** [`BridgeOracle.sol`](https://github.com/Tempest-Finance/tempest_smart_contract/blob/f9da49e15ea8f8f66670cb269814c9dd9fde875c/src/utils/BridgeOracle.sol)

**Description:**

During contract construction, the `isSequencerDown` is not initialized, meaning it is initially set to `false`. Contract deployment may happen at a time that the sequencer is down at the L2 chain without a Chainlink Sequencer Uptime Feed. For a short time, until the off-chain keeper is set up to call `setIsSequencerDown(...)` with the correct value, all calls for the `latestAnswer()` and `numeraireLatestAnswer()` will incorrectly go through.

**Impact:** After contract deployment, the `BridgeOracle` contract will return prices for any `latestAnswer()` and `numeraireLatestAnswer()` calls even if the sequencer is actually down.

**Recommendation:** Set the `isSequencerDown` variable to equal to `true` in the constructor until the off-chain keeper is fully set up.

**Status:** Fixed

**Update from the Tempest:** Fixed in [da18fc4f0f642926e53890833c268c83ce1a829d](https://github.com/Tempest-Finance/tempest_smart_contract/pull/203/commits/da18fc4f0f642926e53890833c268c83ce1a829d)
