---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-4-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Use unchecked block for increment operations in `distributeRewards`
vuln_class: []
---

# Use unchecked block for increment operations in `distributeRewards`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description**

In `Rewards::distributeRewards`, an `unchecked` block can be used to optimize gas consumption for increment operations inside the loop.

```solidity
function distributeRewards(uint48 epoch, uint48 batchSize) external onlyRole(REWARDS_DISTRIBUTOR_ROLE) {
    DistributionBatch storage batch = distributionBatches[epoch];
    uint48 currentEpoch = l1Middleware.getCurrentEpoch();

    if (batch.isComplete) revert AlreadyCompleted(epoch);
    // Rewards can only be distributed after a 2-epoch delay
    if (epoch >= currentEpoch - 2) revert RewardsDistributionTooEarly(epoch, currentEpoch - 2);

    address[] memory operators = l1Middleware.getAllOperators();
    uint256 operatorCount = 0;

    for (uint256 i = batch.lastProcessedOperator; i < operators.length && operatorCount < batchSize; i++) {
        // Calculate operator's total share based on stake and uptime
        _calculateOperatorShare(epoch, operators[i]);

        // Calculate and store vault shares
        _calculateAndStoreVaultShares(epoch, operators[i]);

        batch.lastProcessedOperator = i + 1;
        operatorCount++;
    }

    if (batch.lastProcessedOperator >= operators.length) {
        batch.isComplete = true;
    }
}
```

**Recommended Mitigation**

Introduce an `unchecked` block for increment operations to optimize gas usage.

```diff
function distributeRewards(uint48 epoch, uint48 batchSize) external onlyRole(REWARDS_DISTRIBUTOR_ROLE) {
    DistributionBatch storage batch = distributionBatches[epoch];
    uint48 currentEpoch = l1Middleware.getCurrentEpoch();

    if (batch.isComplete) revert AlreadyCompleted(epoch);
    // Rewards can only be distributed after a 2-epoch delay
    if (epoch >= currentEpoch - 2) revert RewardsDistributionTooEarly(epoch, currentEpoch - 2);

    address[] memory operators = l1Middleware.getAllOperators();
    uint256 operatorCount = 0;

-   for (uint256 i = batch.lastProcessedOperator; i < operators.length && operatorCount < batchSize; i++) {
+   for (uint256 i = batch.lastProcessedOperator; i < operators.length && operatorCount < batchSize;) {
        // Calculate operator's total share based on stake and uptime
        _calculateOperatorShare(epoch, operators[i]);

        // Calculate and store vault shares
        _calculateAndStoreVaultShares(epoch, operators[i]);

+       unchecked {
            batch.lastProcessedOperator = i + 1;
            operatorCount++;
+          i++;
+       }
    }

    if (batch.lastProcessedOperator >= operators.length) {
        batch.isComplete = true;
    }
}
```

**Suzaku:**
Fixed in commit [2fb0daf](https://github.com/suzaku-network/suzaku-core/commit/2fb0dafd684eeaf11b177602c5047d1e6ce2d715).

**Cyfrin:** Verified.
