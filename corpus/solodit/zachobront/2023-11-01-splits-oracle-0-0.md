---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-splits-oracle-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md
tags:
- firm:zachobront
- report:2023-11-01-splits-oracle
title: '[H-01] UniV3 Oracle unsafe on L2s in event of Sequencer downtime'
vuln_class: []
---

# [H-01] UniV3 Oracle unsafe on L2s in event of Sequencer downtime

_Section severity (from Solodit section header): High_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-splits-oracle.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md)_

---

The UniV3 oracle uses the built in `consult()` function provided by Uniswap's Oracle Library to query the pool and determine the time weighted price. This takes in a `secondsAgo` and observes the price at `secondsAgo` and `block.timestamp`, returning the time weighted average between these two points.

In the event that we haven't had any observation since `secondsAgo`, we assume the latest observation still holds:
```solidity
    function getSurroundingObservations(
        Observation[65535] storage self,
        uint32 time,
        uint32 target,
        int24 tick,
        uint16 index,
        uint128 liquidity,
        uint16 cardinality
    ) private view returns (Observation memory beforeOrAt, Observation memory atOrAfter) {
        // optimistically set before to the newest observation
        beforeOrAt = self[index];

        // if the target is chronologically at or after the newest observation, we can early return
        if (lte(time, beforeOrAt.blockTimestamp, target)) {
            if (beforeOrAt.blockTimestamp == target) {
                // if newest observation equals target, we're in the same block, so we can ignore atOrAfter
                return (beforeOrAt, atOrAfter);
            } else {
                // otherwise, we need to transform
                return (beforeOrAt, transform(beforeOrAt, target, tick, liquidity));
            }
        }
        ...
}
```
In the event that an L2's sequencer goes down, the time weighted price when it comes back online will be the extrapolated previous price. This will create an opportunity to push through transactions at the old price before it is updated. Even when the new price is observed, it will be assumed by the sequencer that the previous price held up until the moment it came back online, which will result in a slow, time weighted adjustment back to the current price.

Note that, in the case of Arbitrum, there is the ability to force transactions through the delayed inbox. If other users are forcing transactions into the given pool, this could solve the problem, but if not it could also make the problem worse by allowing an attacker to force a transaction that abuses the outdated price while the sequencer is down, guaranteeing inclusion.

**Recommendation**

Use the Chainlink oracle for all L2s.

**Review**

0xSplits will prioritize the Chainlink oracle for all L2s. In the event that they need to deploy the Uniswap oracle, they have implemented the following changes:
- check the Chainlink Sequencer Feed to confirm the sequencer is up
- confirm that the sequencer has been back up for at least 1 hour
- for each queried pool, confirm that the sequencer has been up for at least the period the TWAP will be taken over

This ensures that, even in the event that the sequencer goes down and therefore propagates the old prices throughout the downtime, that downtime will be completely out of the TWAP by the time the oracle can be queried.

These changes can be seen in the following commits: [3a8a7a01](https://github.com/0xSplits/splits-oracle/pull/5/commits/3a8a7a010d454628532aa4db3887a9330423467c), [59124dbc](https://github.com/0xSplits/splits-oracle/pull/5/commits/59124dbc46222dfdee74a7115965cd0a61fc9874), [46baca33](https://github.com/0xSplits/splits-oracle/pull/5/commits/46baca33aae9dac8db734af3c704ef8b77fed3e1)
