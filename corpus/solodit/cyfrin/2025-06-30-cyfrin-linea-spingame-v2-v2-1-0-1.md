---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-0-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-06-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-30-cyfrin-linea-spingame-v2-v2-1
title: Asynchronous VRF request fulfillment uses stale or incorrect parameters due
  to lack of request-specific data tracking
vuln_class: []
---

# Asynchronous VRF request fulfillment uses stale or incorrect parameters due to lack of request-specific data tracking

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-30-cyfrin-linea-spingame-v2-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md)_

---

**Description:** The `SpinGame` contract has a critical architectural flaw in how it handles asynchronous VRF requests. The contract stores user boost values and prize configurations globally rather than tying them to specific requests, leading to inconsistent game behavior when prize structures change or users make multiple participation requests.

There are two primary issues:

First, prize configurations lack versioning. The `SpinGame::updatePrizes` function completely resets the prize structure by deleting existing `prizeIds` and resetting `totalProbabilities` to zero before adding new prizes. When a user calls `SpinGame::participate`, they receive a signature based on the current prize structure. However, if `SpinGame::updatePrizes` is called between the request and VRF fulfillment, the `SpinGame::_fulfillRandomness` function will use the updated prize structure instead of the one the user expected when participating. This means users could win entirely different prizes than what was available when they participated.

Second, request-specific data is not properly tracked. The `SpinGame::participate` function stores the user's boost value in `userToBoost[user]`, but this mapping gets overwritten if the same user participates again with a different boost before the first request is fulfilled. When `SpinGame::_fulfillRandomness` executes, it retrieves the boost using `uint64 userBoost = userToBoost[user]`, which may not be the boost value from the original request. This creates scenarios where a user who participated with a 150% boost could have their request fulfilled with a 500% boost if they made a second participation with higher boost before the first VRF callback.

The contract only tracks minimal request data through `requestIdToUser` and `requestIdTimestamp` mappings, but fails to capture the complete context needed for proper request fulfillment including the specific boost value and prize structure version at request time.

**Impact:** Users may receive different prizes or win probabilities than expected when they participated, leading to unfair game outcomes and potential loss of funds.

```
// Scenario 1: Prize structure changes between request and fulfillment
1. User calls participate() when Prize A (50% chance) and Prize B (30% chance) are available
2. Controller calls updatePrizes() with Prize C (60% chance) and Prize D (20% chance)
3. VRF fulfills the request using new prize structure with C and D instead of A and B

// Scenario 2: Multiple participations with different boosts
1. User calls participate() with 150% boost, gets requestId1
2. User calls participate() with 500% boost, gets requestId2
3. VRF fulfills requestId1 but uses 500% boost instead of 150%
```

**Recommended Mitigation:** Implement request-specific data tracking with prize versioning:

```diff
+ uint256 public prizeVersion;
+ mapping(uint256 requestId => uint64 boost) public requestIdToBoost;
+ mapping(uint256 requestId => uint256 prizeVersion) public requestIdToPrizeVersion;

function updatePrizes(Prize[] calldata _prizes) external onlyController {
    delete prizeIds;
    totalProbabilities = 0;
+   prizeVersion++;
    _addPrizes(_prizes);
}

function participate(
    uint64 _nonce,
    uint256 _expirationTimestamp,
    uint64 _boost,
    Signature calldata _signature
) external returns (uint256) {
    // ... existing validation ...

-   userToBoost[user] = _boost;
    uint256 requestId = _requestRandomness("");

    requestIdToUser[requestId] = user;
    requestIdTimestamp[requestId] = block.timestamp;
+   requestIdToBoost[requestId] = _boost;
+   requestIdToPrizeVersion[requestId] = prizeVersion;

    // ... rest of function ...
}

function _fulfillRandomness(
    uint256 _randomness,
    uint256 _requestId,
    bytes memory
) internal override {
    address user = requestIdToUser[_requestId];
    if (user == address(0)) {
        revert InvalidRequestId(_requestId);
    }

+   // Verify prize version hasn't changed
+   if (requestIdToPrizeVersion[_requestId] != prizeVersion) {
+       revert PrizeVersionMismatch();
+   }

-   uint64 userBoost = userToBoost[user];
+   uint64 userBoost = requestIdToBoost[_requestId];

    // ... rest of fulfillment logic ...

+   delete requestIdToBoost[_requestId];
+   delete requestIdToPrizeVersion[_requestId];
}
```

**Linea:** Acknowledged. We have discussed L2 issue internally. We decided to not fix it because the prizes will be generally the same just with new allocations. In the case of different prizes, we are okay with the behavior that users can win different prizes.

\clearpage
