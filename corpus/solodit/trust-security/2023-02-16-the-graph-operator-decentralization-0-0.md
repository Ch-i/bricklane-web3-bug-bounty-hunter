---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-16-the-graph-operator-decentralization-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-02-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-16-The%20Graph%20Operator%20Decentralization.md
tags:
- firm:trust-security
- report:2023-02-16-the-graph-operator-decentralization
title: TRST-M-1 Operator can spoof query fees to make net profit from pool
vuln_class: []
---

# TRST-M-1 Operator can spoof query fees to make net profit from pool

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-16-The Graph Operator Decentralization.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-16-The%20Graph%20Operator%20Decentralization.md)_

---

**Description:**
Operators call `collect()` to pay query fees to the indexer. The fees are accumulated for all allocations that end in the same epoch in a Rebates.Pool structure, later to be split per indexer using the Cobb-Douglas production function.
This fee structure should be resistant to query fee donations that:
⦁	Lower another indexer's total rebate amount
⦁	Result in a net positive for the donator (query fee MEV)
However, stress testing of the function found that guarantee 2 is not held. Operators, which are transitioning to be a decentralized role, can fake queries and increase their portion of the pool. This does not directly harm other indexers, because their share of the pool increases as well. However, the share of the rebate pool that stays in the protocol decreases.
An example is provided below. The rewards per indexer are calculated as follows:
 
𝑟𝑒𝑤𝑎𝑟𝑑(i) = totalRewards * (fee/totalFees)^𝛼 * (stake/totalStake)^1-𝛼 

Suppose 𝛼 = 0.4523, and the layout of pool participants is as follows:


|  Participant  | Fee  | Stake|
|---------------|------|------|
| Participant 1 | 511  | 515  |
| Participant 2 | 794  | 1    |


The calculated rewards are:
𝑟𝑒𝑤𝑎𝑟𝑑(1) = 1305 ∗ ( 511/1305 )^0.4523 ∗ ( 515/516 )^1−0.4523 ≅ 853

r𝑒𝑤𝑎𝑟𝑑(2) = 1305 ∗ ( 794/1305 )^0.4523 ∗ ( 1/516 )^1−0.4523 ≅ 34

Fees of the rebate pool not rewarded:
r𝑒𝑚𝑎𝑖𝑛𝑖𝑛𝑔 = 1305 − 853 − 34 = 418
At this point, participant 1 donates 720. The new layout is:

|  Participant  | Fee   | Stake|
|---------------|-------|------|
| Participant 1 | 1231  | 515  |
| Participant 2 | 794   | 1    |

The calculated rewards are:


r𝑒𝑤𝑎𝑟𝑑(1) = 2025 ∗ ( 1231/1305 )^0.4523 ∗ ( 515/516 )^1−0.4523 ≅ 1615

r𝑒𝑤𝑎𝑟𝑑(2) = 2025 ∗ ( 794/1305 )^0.4523 ∗ ( 1/516 )^1−0.4523 ≅ 43

Fees of the rebate pool not rewarded:
𝑟𝑒𝑚𝑎𝑖𝑛𝑖𝑛𝑔 = 2025 − 1615 − 43 = 367

Calculating pool loss (of profits) from donation:
𝑙𝑜𝑠𝑠 = 418 − 367 = 51

Profit was split between the participants:

𝑝𝑟𝑜𝑓𝑖𝑡(1) = 1615 − 720 − 853 = 42

𝑝𝑟𝑜𝑓𝑖𝑡(2) = 43 − 34 = 9

Attackers can donate query fees at any point before the allocation is finalized, which is when 
a certain number of epochs have passed since it was closed. This means in the final block 
there will be incentives for large amounts of MEV activity of the different participants, to the 
loss of the protocol.
A python script that fuzzes the Cobb-Douglas formula has been provided separately.


**Recommended Mitigation:**
Consider making use of a different awarding formula, which would disincentivize forging of 
query activities.

**Team Response:**
Acknowledged. There is ongoing economic research on alternatives to Cobb-Douglas, but for 
now we think this is an acceptable consequence of decentralizing gateways.
