---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-4-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Reorder emit before storage write to eliminate `old` local variables
vuln_class: []
---

# Reorder emit before storage write to eliminate `old` local variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Several functions assign a storage slot to a local (`oldX` / `previousX`) only to feed it into an event emission after the SSTORE. The local is dead weight - emitting the event before overwriting storage reads the same value directly from the still-current slot, eliminating the local and the stack slot held across the SSTORE. The Solidity optimizer cannot perform this reorder itself because emits are observable side effects.

Affected sites:

- `contracts/governance/RevenueLock.sol:248` - `oldMax = maxObservedRevenue` is read solely for the `ObservedRevenueUpdated` emit at `:250`.
- `contracts/governance/ArmadaGovernor.sol:474` - `previousDeployer = deployer` is read solely for the `DeployerCleared` emit at `:477`.
- `contracts/governance/ArmadaGovernor.sol:614` - `oldSC = securityCouncil` is read solely for the `SecurityCouncilUpdated` emit at `:633`.
- `contracts/governance/ArmadaTreasuryGov.sol:368` - `oldActive = config.limitAbsolute` is read solely for the `OutflowLimitAbsoluteActivated` emit at `:373`.
- `contracts/governance/ArmadaTreasuryGov.sol:378` - `oldActive = config.limitBps` is read solely for the `OutflowLimitBpsActivated` emit at `:383`.
- `contracts/governance/ArmadaTreasuryGov.sol:388` - `oldActive = config.windowDuration` is read solely for the `OutflowWindowDurationActivated` emit at `:393`.

**Impact:** Per call site, saves the stack slot held across the SSTORE plus the associated stack-shuffling bytecode. Hottest sites are the three `_lazyActivate` branches (hit on every outflow setter activation) and `RevenueLock::_updateMaxObservedRevenue` (hit on every `release` and `sync`).

**Recommended Mitigation:** Emit the event before the SSTORE so the "old" argument reads the still-current storage value:

```solidity
// RevenueLock::_updateMaxObservedRevenue
if (capped > maxObservedRevenue) {
    emit ObservedRevenueUpdated(maxObservedRevenue, capped, reported);
    maxObservedRevenue = capped;
}

// ArmadaGovernor::clearDeployer
emit DeployerCleared(deployer);
deployer = address(0);

// ArmadaTreasuryGov::_lazyActivate (apply to all 3 branches; example: limitAbsolute)
uint256 newActive = config.pendingLimitAbsolute;
emit OutflowLimitAbsoluteActivated(token, config.limitAbsolute, newActive);
config.limitAbsolute = newActive;
config.pendingLimitAbsolute = 0;
config.pendingLimitAbsoluteActivation = 0;
```

In `_lazyActivate`, retain `newActive` so the pending-slot read isn't repeated across the emit and the SSTORE; only `oldActive` is removed.

For the `oldSC` site in `ArmadaGovernor`, hoist the `SecurityCouncilUpdated` emit to immediately before `securityCouncil = address(0)` at `:615`. This changes the relative ordering of `SecurityCouncilUpdated` against the `ProposalRestored` and `SecurityCouncilEjected` emits at `:631-632`; if external indexers depend on that ordering, leave this site as-is.

**Armada:** Fixed in commit [e22f661](https://github.com/ship-armada/armada-poc/commit/e22f661e41f4e6fbb527d12f78bb9fde25aca827).

**Cyfrin:** Verified.
