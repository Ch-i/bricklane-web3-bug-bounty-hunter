---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-4-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: 'Storage round-trips: helpers write state that callers immediately re-read
  instead of returning the value'
vuln_class: []
---

# Storage round-trips: helpers write state that callers immediately re-read instead of returning the value

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** A helper writes a storage slot, returns control to the caller, and the caller (directly or via a sibling helper) then SLOADs that same slot instead of receiving it as a return value. Fix: have the writer return the just-computed value(s) and use the returned locals.

1. `ArmadaCrowdfund::_computeCappedDemand` at `contracts/crowdfund/ArmadaCrowdfund.sol:851` writes `cappedDemand` (`:856`) and `hopStats[h].cappedCommitted` for h=0,1,2 (`:854`). `finalize` re-reads `cappedDemand` at `:403, :412`, and `_computeHopAllocations` (called at `:428`) re-reads `hopStats[0,1,2].cappedCommitted` at `:768, :778, :791`. Return `(uint256 cappedDemand_, uint256[3] memory perHopCapped_)` and pass `perHopCapped_` into `_computeHopAllocations`. Keeps the state writes for external readers. Saves ~2,200 gas on `cappedDemand` plus 3 warm SLOADs on `hopStats` per finalize.

2. `ArmadaGovernor::_initProposal` at `contracts/governance/ArmadaGovernor.sol:827` writes `p.voteStart` (`:838`) and `p.voteEnd` (`:839`). All three callers re-read them for the `ProposalCreated` emit: `_createRatificationProposal` at `:662-664`, `proposeStewardSpend` at `:726-728`, `propose` at `:813-815`. Return `(uint256 voteStart, uint256 voteEnd)`. Saves 2 SLOADs per proposal creation.

3. `ArmadaTreasuryGov::_lazyActivate` at `contracts/governance/ArmadaTreasuryGov.sol:363` conditionally writes `config.limitAbsolute, limitBps, windowDuration`. Callers re-read: `setOutflowWindow` at `:276`, `setOutflowLimitBps` at `:305`, `setOutflowLimitAbsolute` at `:331`, `_checkAndRecordOutflow` at `:419, :422, :459-460`. Return the post-activation `(windowDuration, limitBps, limitAbsolute)` tuple. Saves 1-3 SLOADs per call; `_checkAndRecordOutflow` is hit by every `distribute` and `stewardSpend`.

4. `RevenueLock::_updateMaxObservedRevenue` at `contracts/governance/RevenueLock.sol:240` conditionally writes `maxObservedRevenue` at `:249`. `release` at `:152-154` re-reads it via `_unlockBpsForRevenue(maxObservedRevenue)`. Return the effective post-ratchet value (the prior value when no advance occurs). Saves 1 SLOAD per beneficiary claim.

**Recommended Mitigation:** Add named return values to each writer and have callers consume the returned locals.

**Armada:** Fixed in commit [4f7924b](https://github.com/ship-armada/armada-poc/commit/4f7924b3a7fe29a0c6bae728fd19c2d04689007d).

**Cyfrin:** Verified.
