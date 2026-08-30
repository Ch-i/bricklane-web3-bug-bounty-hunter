---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-4-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Cache storage slots read multiple times within the same function
vuln_class: []
---

# Cache storage slots read multiple times within the same function

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Storage slots are SLOAD'd multiple times within a single function without caching. Once a slot has been read or written inside a function and cannot change before the next access, re-reading is a redundant ~100-gas warm SLOAD. Cache into a local and read the local.

**ArmadaCrowdfund**

1. `_iterateCappedDemand` at `contracts/crowdfund/ArmadaCrowdfund.sol:832`. Loop reads `node.hop` three times per iteration (`:839, :842, :844`) through a storage pointer. Up to ~1,500 iterations per `finalize` per the design note at `:828`. Cache `uint8 hop = node.hop; address addr = node.addr;` once per iteration. Saves up to ~3,000 warm SLOADs per finalize.

2. `_iterateCappedDemand` at `contracts/crowdfund/ArmadaCrowdfund.sol:832`. `p.committed` read at `:840` (`if (p.committed == 0) continue;`) and twice at `:843` (`p.committed < cap ? p.committed : cap`) with no intervening write. Cache `uint256 committed = p.committed;` after the zero-check. Up to 2 SLOADs per non-zero iteration; ~3,000 SLOADs per finalize at the ~1,500-node maximum.

3. `finalize` at `contracts/crowdfund/ArmadaCrowdfund.sol:392`. `saleSize` written at `:413` or `:415`, re-read at `:428, :439, :469`. Compute into a local, assign the storage once, use the local downstream. 3 SLOADs.

4. `finalize` at `contracts/crowdfund/ArmadaCrowdfund.sol:392`. `cappedDemand` written by `_computeCappedDemand` (call at `:399`, write at `:856`), then re-read at `:403` and `:412` with no intervening write. Cache to a local after the call. 1 SLOAD.

5. `finalize` at `contracts/crowdfund/ArmadaCrowdfund.sol:392`. `totalAllocatedArm` written at `:446`, re-read at `:469` in the `Finalized` emit. Compute into a local first: `uint256 allocatedArm = (totalAllocUsdc_ * 1e18) / ARM_PRICE; totalAllocatedArm = allocatedArm; emit Finalized(saleSize, allocatedArm, ...);`. 1 SLOAD.

6. `claim` at `contracts/crowdfund/ArmadaCrowdfund.sol:481`. Inside the per-hop loop at `:493`, `p.committed` read at `:495` (`if (p.committed == 0) continue;`) and again at `:497` (passed to `_computeAllocation(p.committed, h, ...)`) with no intervening write. Cache `uint256 committed = p.committed;` after the zero-check. Up to 3 SLOADs per claim. Same pattern in the view function `computeAllocation` at `:647-654`.

7. `_computeAllocation` at `contracts/crowdfund/ArmadaCrowdfund.sol:803`. `finalDemands[hop]` and `finalCeilings[hop]` each read at `:812` and `:817`. Cache both at the top. 2 SLOADs per hop-claim.

8. `withdrawUnallocatedArm` at `contracts/crowdfund/ArmadaCrowdfund.sol:555`. `phase` read at `:557` and `:563`. Cache. 1 SLOAD.

**ArmadaGovernor**

9. `_initProposal` at `contracts/governance/ArmadaGovernor.sol:827`. `armToken` read at `:854, :855, :858` (last inside a loop). Cache once. Saves 1 + N SLOADs per proposal.

10. `_initProposal` at `contracts/governance/ArmadaGovernor.sol:827`. `p.snapshotBlock` written at `:837`, re-read at `:854` inside `armToken.getPastTotalSupply(p.snapshotBlock)`. Use `block.number - 1` directly at the call site, or cache before the storage write. 1 SLOAD.

11. `_initProposal` at `contracts/governance/ArmadaGovernor.sol:827`. `p.voteStart` written at `:838`, re-read at `:839` in `p.voteEnd = p.voteStart + params.votingPeriod`. Cache: `uint256 voteStart_ = block.timestamp + params.votingDelay; p.voteStart = voteStart_; p.voteEnd = voteStart_ + params.votingPeriod;`. 1 SLOAD.

12. `proposeStewardSpend` at `contracts/governance/ArmadaGovernor.sol:680`. `stewardContract` read at `:687, :688, :689`; `treasuryAddress` read at `:705` inside the per-token loop. Cache both. 2 + (tokens.length - 1) SLOADs.

13. `queue` at `contracts/governance/ArmadaGovernor.sol:903`. `p.proposalType` read at `:907, :908, :913`; `stewardContract` read at `:914, :915, :916`; `timelock` read at `:928, :932`. Cache all three. 5 SLOADs.

14. `queue` at `contracts/governance/ArmadaGovernor.sol:903`. Storage dynamic arrays `p.targets`, `p.values`, `p.calldatas` are passed to `timelock.hashOperationBatch` at `:928-930` AND `timelock.scheduleBatch` at `:932-937`. Each cross-contract call ABI-encodes the arrays from storage independently. Load once into memory locals (`address[] memory tgts = p.targets;` etc.) and pass the locals to both calls. Savings scale with batch size - per-element duplicate SLOAD avoided.

15. `execute` at `contracts/governance/ArmadaGovernor.sol:943`. `p.proposalType` read at `:947, :948, :953`; `stewardContract` read at `:954, :955, :956`. Cache both. 4 SLOADs.

16. `veto` at `contracts/governance/ArmadaGovernor.sol:570`. `securityCouncil` read at `:571` (`if (msg.sender != securityCouncil)`) and `:572` (`if (securityCouncil == address(0))`); `timelock` read at `:584, :587`. Cache both. 2 SLOADs.

17. `setWindDownActive` at `contracts/governance/ArmadaGovernor.sol:752`. `windDownContract` read at `:753` (`if (msg.sender != windDownContract)`) and `:754` (`if (windDownContract == address(0))`). Cache. 1 SLOAD.

18. `resolveRatification` at `contracts/governance/ArmadaGovernor.sol:598`. `timelock` read at `:624, :628`. Cache. 1 SLOAD.

19. `state` at `contracts/governance/ArmadaGovernor.sol:995`. `p.proposalType` read at `:1005, :1018`; `p.voteEnd` read at `:1002, :1023`. Cache both. 2 SLOADs.

20. `_checkOutflowFeasibility` at `contracts/governance/ArmadaGovernor.sol:1183`. `treasuryAddress` read inside two loops at `:1195` and `:1226`. Hoist above the loops. Saves (calldatas.length + tokenCount - 2) SLOADs.

21. `_validateTimelockCalldata` at `contracts/governance/ArmadaGovernor.sol:1236`. `timelock` read at `:1238` inside the per-target loop. Hoist. Saves (targets.length - 1) SLOADs.

22. `_checkQuietPeriod` at `contracts/governance/ArmadaGovernor.sol:1257`. `crowdfundAddress` read at `:1258` and `:1260`. Cache. 1 SLOAD.

23. `setExcludedAddresses` at `contracts/governance/ArmadaGovernor.sol:424`. `treasuryAddress` read at `:431` inside the per-address loop. Hoist above the loop. Saves (addrs.length - 1) SLOADs.

**ArmadaTreasuryGov**

24. `stewardSpend` at `contracts/governance/ArmadaTreasuryGov.sol:152`. `budget.limit` read at `:162` and `:176` through the `budget` storage pointer with no intervening write. Cache `uint256 limit = budget.limit;` after the authorized check. 1 SLOAD.

25. `_lazyActivate` at `contracts/governance/ArmadaTreasuryGov.sol:363`. `config.pendingLimitAbsoluteActivation` read at `:366, :367`; `config.pendingLimitBpsActivation` at `:376, :377`; `config.pendingWindowDurationActivation` at `:386, :387`. Each activation slot is read twice in the boolean (`> 0 && block.timestamp >= X`) before any write. Cache each at the top of its `if`. 3 SLOADs.

26. `_effectiveParams` at `contracts/governance/ArmadaTreasuryGov.sol:591`. Same pattern as `_lazyActivate`: `config.pendingLimitAbsoluteActivation` at `:596, :597`; `config.pendingLimitBpsActivation` at `:600, :601`; `config.pendingWindowDurationActivation` at `:604, :605`. Cache each. 3 SLOADs.

27. `_effectiveLimit` at `contracts/governance/ArmadaTreasuryGov.sol:458`. `config.limitAbsolute` read twice at `:460` (`pctLimit > config.limitAbsolute ? pctLimit : config.limitAbsolute`); `config.floorAbsolute` read twice at `:461` (`limit > config.floorAbsolute ? limit : config.floorAbsolute`). Cache both. 2 SLOADs.

**ArmadaRedemption**

28. `redeem` at `contracts/governance/ArmadaRedemption.sol:118`. `windDown` read at `:134, :135`. Cache. 1 SLOAD.

**ShieldPauseController**

29. `pauseShields` at `contracts/governance/ShieldPauseController.sol:107`. `pauseExpiry` written at `:118` then re-read at `:119` in the `ShieldsPaused` emit. Compute into a local first: `uint256 expiry = block.timestamp + MAX_PAUSE_DURATION; pauseExpiry = expiry; emit ShieldsPaused(msg.sender, expiry);`. 1 SLOAD.

**TreasurySteward**

30. `electSteward` at `contracts/governance/TreasurySteward.sol:47`. `termStart` written at `:50` (`= block.timestamp`) then read twice at `:51` in `emit StewardElected(_steward, termStart, termStart + TERM_DURATION)`. Use `block.timestamp` directly in the emit. 2 SLOADs.

**RevenueCounter**

31. `syncStablecoinRevenue` at `contracts/governance/RevenueCounter.sol:59`. `feeCollector` read at `:60, :62`; `recognizedRevenueUsd` written at `:70` then re-read at `:72` for the emit. Cache both. 2 SLOADs.

32. `attestRevenue` at `contracts/governance/RevenueCounter.sol:81`. `recognizedRevenueUsd` read at `:82, :84, :86, :89`. Cache at top. 3 SLOADs.

33. `setFeeCollector` at `contracts/governance/RevenueCounter.sol:97`. `feeCollector` read at `:99, :100, :109`; `recognizedRevenueUsd` written at `:104` and re-read at `:105` for the emit. Cache both. 3 SLOADs on the delta > 0 path.

**RevenueLock**

34. `_updateMaxObservedRevenue` at `contracts/governance/RevenueLock.sol:240`. `maxObservedRevenue` read at `:245, :247, :248`. Cache at top. 2 SLOADs.

35. `getCappedObservedRevenue` at `contracts/governance/RevenueLock.sol:218`. `maxObservedRevenue` read at `:222, :223`. Cache. 1 SLOAD.

36. `release` at `contracts/governance/RevenueLock.sol:146`. `released[msg.sender]` written at `:160` then re-read at `:165` in the `Released` emit. Use `uint256 newReleased = alreadyReleased + amount; released[msg.sender] = newReleased; emit Released(..., newReleased);`. 1 SLOAD.

**Recommended Mitigation:** Apply the per-site caching above. For loops, hoist invariant slot reads above the loop and copy storage-pointer struct fields into memory locals once per iteration. For write-then-read patterns, compute the value into a local first, store the local once, then emit/use the local.

**Armada:** Fixed in [3312412](https://github.com/ship-armada/armada-poc/commit/3312412ad09a9b9e9e231e1317e81d3dd5111dd9).

**Cyfrin:** Verified with following observations:
* item 23 not implemented
* cached `budget.limit` not used when computing `remaining` in `ArmadaTreasuryGov::stewardSpend`
