---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: '`AprPairFeed::getRoundData` can return data for a different round than the
  specified'
vuln_class: []
---

# `AprPairFeed::getRoundData` can return data for a different round than the specified

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** When updating round data on the `AprPairFeed`, the data is saved in the `rounds` mapping, which is accessed via the calculated `roundIdx`. The way in which the `roundIdx` is derived causes it to be repeated every 20 updates, from 0 to 20, over and over. This means that an older  `roundIdx` would eventually calculate the same `roundIdx` as a newer one. This can cause the problem that when retrieving data for a specific roundId, `AprPairFeed::getRoundData` returns data for a newer roundId.

```solidity
    function updateRoundDataInner(int64 aprTarget, int64 aprBase, uint64 t) internal {
        ...
        uint64 roundId = (latestRoundId + 1);
@>      uint64 roundIdx = roundId % roundsCap;

        latestRoundId = roundId;
        latestRound = TRound({
            aprTarget: aprTarget,
            aprBase: aprBase,
            updatedAt: t,
            answeredInRound: roundId
        });
@>      rounds[roundIdx] = latestRound;

        emit AnswerUpdated(aprTarget, aprBase, roundId, t);
    }

    function getRoundData(uint64 roundId) public view returns (TRound memory) {
@>      uint64 roundIdx = roundId % roundsCap;
        TRound memory round = rounds[roundIdx];
        require(round.updatedAt > 0, "No data present");
@>      return round;
    }

```

**Recommended Mitigation:** Consider validating that the data read from the `rounds` mapping matches the specified roundId.
```diff
    function getRoundData(uint64 roundId) public view returns (TRound memory) {
        uint64 roundIdx = roundId % roundsCap;
        TRound memory round = rounds[roundIdx];
        require(round.updatedAt > 0, "No data present");
+       require(round.answeredInRound == roundId, "old round");
        return round;
    }
```

**Strata:**
Fixed in commit [233e3d](https://github.com/Strata-Money/contracts-tranches/commit/233e3d398b9bb52929170572fed69d1083ee1ce1) by verifying the queried data corresponds to the same requested `roundId`.

**Cyfrin:** Verified.
