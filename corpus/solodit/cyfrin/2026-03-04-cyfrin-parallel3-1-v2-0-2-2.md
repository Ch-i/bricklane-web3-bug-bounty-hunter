---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: Missing validation allows `userDeviation > burnRatioDeviation`, silently disabling
  burn ratio protection
vuln_class: []
---

# Missing validation allows `userDeviation > burnRatioDeviation`, silently disabling burn ratio protection

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** In `LibOracle::readBurn`, `readSpotAndTarget` snaps `oracleValue` to `targetPrice` when spot is within `userDeviation`. The burn ratio check (L84) then compares the already-snapped value against `burnRatioDeviation`. If `userDeviation > burnRatioDeviation`, depegs between the two thresholds are snapped away before the ratio check sees them — the check compares `targetPrice` against itself and never triggers.

`LibSetters::setOracle` validates only via `readMint` (L153), which ignores `burnRatioDeviation`. Nothing enforces `burnRatioDeviation >= userDeviation`.

**Impact:** When triggered, the burn ratio penalty is silently disabled — `getBurnOracle` returns `minRatio = BASE_18` and all burns proceed at full value during a depeg that should have activated the penalty.

**Proof of Concept:**
1. Oracle set with `userDeviation=5%`, `burnRatioDeviation=2%`
2. Collateral depegs to 0.96 (4% — between the two thresholds)
3. `readSpotAndTarget` snaps 0.96 → 1.0 → ratio check on L84 passes → `ratio = BASE_18`
4. Burns proceed at full value; the depeg is invisible

**Recommended Mitigation:** Add in `LibSetters::setOracle`:

```solidity
(uint128 userDeviation, uint128 burnRatioDeviation) = abi.decode(hyperparameters, (uint128, uint128));
if (userDeviation > burnRatioDeviation) revert InvalidParams();
```

**Parallel:** Fixed in commit [bc4574a](https://github.com/parallel-protocol/parallel-parallelizer/commit/bc4574ac3f794e53952092f264e3863af6247b5b#diff-dc2d240c037d4c60536e1992723693494bd288601798008bae2a168763783ccb).

**Cyfrin:** Verified. Remediated by implementing the recommended mitigation.
