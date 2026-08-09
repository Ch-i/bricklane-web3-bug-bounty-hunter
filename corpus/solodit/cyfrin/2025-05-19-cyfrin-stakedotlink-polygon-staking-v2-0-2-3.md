---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: Incorrect event emission when removing fees via the `PolygonStrategy::updateFee`
vuln_class: []
---

# Incorrect event emission when removing fees via the `PolygonStrategy::updateFee`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** Fee for a given index can be removed by passing `_feeBasisPoints = 0` for a given fee index.

Current logic is swapping the fee at the index with that of the last index in the `fees` array, and then popping the last element of the `fees` array.

However, the event emitted for this action suggests that the fee at the index is updated to 0. This is incorrect because the fee at the index is the fee corresponding to the last index of the original `fees` array. Additionally, in this scenario, the `UpdateFee` event is emitting the `receiver` passed as an input to the function without verifying if this receiver indeed matches the receiver for the removed fee index.

```solidity
function updateFee(
        uint256 _index,
        address _receiver,
        uint256 _feeBasisPoints
    ) external onlyOwner {

        if (_feeBasisPoints == 0) {
            fees[_index] = fees[fees.length - 1];
            fees.pop();

        } else {
              // ... code
        }
        emit UpdateFee(_index, _receiver, _feeBasisPoints); //@audit if _feeBasisPoints == 0, the fee for the index is now the fee in the last index (for old array)
    }
```

**Recommended Mitigation:** Consider adding an event `RemoveFee` similar to `AddFee` for the special case when `_feeBasisPoints == 0`. This will clearly separate the scenario where fee at an index is just updated v/s removed altogether.


**Stake.Link:** Resolved in [PR 151](https://github.com/stakedotlink/contracts/pull/151/commits/bd29a3eee47f41ad9418418d7c959e7372b1f755)

**Cyfrin:** Resolved.
