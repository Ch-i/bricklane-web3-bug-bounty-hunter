---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-4-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Reorder calldata input checks before non-immutable storage reads in 8 admin
  setters
vuln_class: []
---

# Reorder calldata input checks before non-immutable storage reads in 8 admin setters

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Across 8 admin setters, a calldata/parameter input check is performed AFTER a cold SLOAD of a non-immutable state variable. When the input check reverts, the caller pays the SLOAD (~2100 gas cold) before the revert. Moving the calldata check to position 2 (between the `msg.sender` check against an immutable and the non-immutable SLOAD) is pareto-better: same cost on success, SLOADs skipped on failing zero-address or out-of-bound calls.

Affected sites:

1. `ArmadaToken::setWindDownContract` at `contracts/governance/ArmadaToken.sol:88-95` - `windDownContractSet` SLOAD before `_windDownContract != address(0)`
2. `ArmadaGovernor::setCrowdfundAddress` at `contracts/governance/ArmadaGovernor.sol:445-453` - `deployer` and `crowdfundAddressLocked` SLOADs before `_crowdfund == address(0)` (2 skippable)
3. `ArmadaGovernor::setStewardContract` at `contracts/governance/ArmadaGovernor.sol:458-466` - `deployer` and `stewardContractLocked` SLOADs before `_steward == address(0)` (2 skippable)
4. `ArmadaGovernor::setWindDownContract` at `contracts/governance/ArmadaGovernor.sol:738-746` - `windDownContractSet` SLOAD before `_windDownContract == address(0)`
5. `ShieldPauseController::setWindDownContract` at `contracts/governance/ShieldPauseController.sol:134-140` - `windDownContractSet` SLOAD before `_windDownContract != address(0)`
6. `ArmadaRedemption::setWindDown` at `contracts/governance/ArmadaRedemption.sol:101-106` - `windDown` SLOAD before `_windDown != address(0)`
7. `ArmadaWindDown::setRevenueThreshold` at `contracts/governance/ArmadaWindDown.sol:189-194` - `triggered` SLOAD before `_newThreshold > 0`
8. `ArmadaWindDown::setWindDownDeadline` at `contracts/governance/ArmadaWindDown.sol:210-215` - `triggered` SLOAD before `_newDeadline > block.timestamp`

**Recommended Mitigation:** Reorder each site so parameter checks follow the immutable `msg.sender` guard and precede the non-immutable SLOAD:

```solidity
// ArmadaToken::setWindDownContract - example
require(msg.sender == tokenDeployer, "ArmadaToken: not deployer");
require(_windDownContract != address(0), "ArmadaToken: zero address");
require(!windDownContractSet, "ArmadaToken: wind-down already set");
```

Apply the same reorder to the remaining 7 sites.

**Armada:** Fixed in commit [c878446](https://github.com/ship-armada/armada-poc/commit/c87844605f678dd6a4ede60f65fb41e1ca200be4).

**Cyfrin:** Verified, remaining potential optimizations:
* `ArmadaGovernor::setCrowdfundAddress, setStewardContract` still check `deployer` (SLOAD) before the input parameter checks
* `ArmadaGovernor::setWindDownContract` checks `timelock` (SLOAD) before input parameter
