---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Cache storage variables in memory when read multiple times without being changed
vuln_class: []
---

# Cache storage variables in memory when read multiple times without being changed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** As reading from storage is considerably more expensive than reading from memory, cache storage variables in memory when read multiple times without being changed:

File: `NodeOperatorRegistry.sol`
```solidity
// @audit cache `numOperators` in memory from storage
// to prevent reading same value multiple times
113:    uint128[] memory operatorAssignedDetails = new uint128[](numOperators + 1);
125:     for (uint128 operatorId = 1; operatorId <= numOperators; operatorId++) {

// @audit save incremented value in memory
// to prevent reading same value multiple times, eg:
// uint128 newNumOperators = ++numOperators;
305:    numOperators += 1;
// then use `newNumOperators` in L314,315
314:    getOperatorIdForAddress[_operatorAddress] = numOperators;
315:    getOperatorForOperatorId[numOperators] = operator;
// @audit `Operator` struct can also be initialized this way:
// getOperatorForOperatorId[numOperators] = Operator(true, _rewardAddress, _operatorAddress, _name, 0);

// @audit cache `getOperatorForOperatorId[operatorId].activeValidators`
660:    if (getOperatorForOperatorId[operatorId].activeValidators == 0) {
666:      getOperatorForOperatorId[operatorId].activeValidators - 1
```

File: `RepricingOracle.sol`
```solidity
// @audit cache rate when checked after repricing and use
// cached version when processing withdrawals since the rate
// only changes during repricing which has already occurred
125:    if (swETHToETHRate > AccessControlManager.swETH().swETHToETHRate()) {
132:        AccessControlManager.swETH().swETHToETHRate() // The rate to use for processing withdrawals

// @audit cache `upgradeableRepriceSnapshot.meta.blockNumber` in memory from storage
// to prevent reading same value multiple times
290:    bool useOldSnapshot = upgradeableRepriceSnapshot.meta.blockNumber == 0;
294:      : upgradeableRepriceSnapshot.meta.blockNumber;

// @audit cache `maximumRepriceBlockAtSnapshotStaleness` in memory from storage
// to prevent reading same value multiple times
317:    if (snapshotStalenessInBlocks > maximumRepriceBlockAtSnapshotStaleness) {
320:        maximumRepriceBlockAtSnapshotStaleness
```

File: `swETH.sol`
```solidity
// @audit cache `lastRepriceUNIX` in memory from storage
// to prevent reading same value multiple times
222:    uint256 timeSinceLastReprice = block.timestamp - lastRepriceUNIX;
249:    if (lastRepriceUNIX != 0) {

// @audit cache `minimumRepriceTime` in memory from storage
// to prevent reading same value multiple times
224:    if (timeSinceLastReprice < minimumRepriceTime) {
226:        minimumRepriceTime - timeSinceLastReprice

// @audit cache `nodeOperatorRewardPercentage` in memory from storage
// to prevent reading same value multiple times
233:      nodeOperatorRewardPercentage;
281:      UD60x18 nodeOperatorRewardPortion = wrap(nodeOperatorRewardPercentage)

// @audit cache `swETHToETHRateFixed` in memory from storage
// to prevent reading same value multiple times
253:        swETHToETHRateFixed
256:      uint256 maximumRepriceDiff = wrap(swETHToETHRateFixed)

// @audit no need to re-read storage values, use the in-memory variables
// that storage locations were just updated from to eliminate redundant but
// expensive storage reads
337:    lastRepriceETHReserves = totalReserves;
338:    lastRepriceUNIX = block.timestamp;
339:    swETHToETHRateFixed = updatedSwETHToETHRateFixed;

341:   emit Reprice(
342:      lastRepriceETHReserves, // @audit use `totalReserves` instead
343:       swETHToETHRateFixed,   // @audit use `updatedSwETHToETHRateFixed` instead
344:       nodeOperatorRewards,
345:       swellTreasuryRewards,
346:       totalETHDeposited

// @audit the first check will fail most of the time during regular usage so
// `swETHToETHRateFixed` will be read twice from storage with the same value
374:    if (swETHToETHRateFixed == 0) {
375:    return wrap(swETHToETHRateFixed);
```

File: `swEXIT.sol`
```solidity
// @audit consider caching `withdrawRequestMinimum` and `withdrawRequestMaximum`
// in memory to avoid an extra storage read in the revert case
193:    if (amount < withdrawRequestMinimum) {
194:       revert WithdrawRequestTooSmall(amount, withdrawRequestMinimum);
195:     }

197:     if (amount > withdrawRequestMaximum) {
198:      revert WithdrawRequestTooLarge(amount, withdrawRequestMaximum);
199:     }
```

**Swell:** Fixed in commits [23be897](https://github.com/SwellNetwork/v3-contracts-lst/commit/23be89740b7659ab4d98435d6a924364635fb9ca), [3f85df3](https://github.com/SwellNetwork/v3-contracts-lst/commit/3f85df3ba0e91b26e4234b15ad94f492fa6d46ec).

**Cyfrin:**
Verified.
