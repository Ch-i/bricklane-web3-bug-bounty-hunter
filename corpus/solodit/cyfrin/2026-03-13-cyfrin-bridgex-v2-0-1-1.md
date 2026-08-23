---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: '`PublicBridge, PrivateChainBridge::payReleaseFee` will revert from out-of-gas
  if too many releasers are added'
vuln_class: []
---

# `PublicBridge, PrivateChainBridge::payReleaseFee` will revert from out-of-gas if too many releasers are added

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** `PublicBridge, PrivateChainBridge::payReleaseFee` uses a push-based pattern to distribute fees, iterating over the entire `releasers` array and sending native tokens to each releaser individually:

```solidity
// PublicBridge.sol:390-397 (same pattern in PrivateChainBridge.sol:388-395)
uint256 distributed = 0;
for (uint i = 0; i < releasers.length; i++) {
    if (feePerReleaser > 0) {
        (bool success, ) = payable(releasers[i]).call{value: feePerReleaser}("");
        if (success) {
            distributed += feePerReleaser;
        }
    }
}
```

As acknowledged in the `README.md` (Known Issue 1 — releasers are trusted, Known Issue 7 — failed transfers are refunded to sender rather than held), this design intentionally skips failed transfers and refunds undistributed portions. However, the push pattern has two inherent drawbacks:

1. **Unbounded iteration:** Every call to `payReleaseFee` iterates the full `releasers` array. With the addition of Reserved enum values for future chain expansion, the number of releasers may grow. Gas cost scales linearly with the number of releasers, and at sufficient scale, `payReleaseFee` could exceed the block gas limit

2. **Partial failure discounts:** When some (but not all) releaser transfers fail, the undistributed portion is refunded to the caller while the full release credits are retained. For example, with 2 releasers and 1 failing, the user pays 50% of the intended fee but receives full release eligibility. The affected releaser receives no compensation for that release

A pull-based (withdrawal) pattern would address both concerns:

```solidity
// Pull-based alternative
mapping(address releaserAddr => uint256 feeBalance) public releaserFeeBalance;

function payReleaseFee() external payable nonReentrant whenNotPaused {
    require(msg.value >= releaseFee, "Insufficient fee");
    require(releasers.length > 0, "No releasers available");

    uint256 eligibleReleases = msg.value / releaseFee;
    uint256 totalFee = eligibleReleases * releaseFee;

    // O(1) — no iteration over releasers
    uint256 feePerReleaser = totalFee / releasers.length;
    uint256 remainingWei = totalFee - (feePerReleaser * releasers.length);
    for (uint256 i; i < releasers.length; i++) {
        releaserFeeBalance[releasers[i]] += feePerReleaser;
    }
    if (remainingWei > 0) {
        releaserFeeBalance[releasers[0]] += remainingWei;
    }

    eligibleBridgeReleases[msg.sender] += eligibleReleases;

    // Refund only the excess beyond full release fees
    uint256 refundAmount = msg.value - totalFee;
    if (refundAmount > 0) {
        (bool success, ) = payable(msg.sender).call{value: refundAmount}("");
        require(success, "Refund failed");
    }

    _processPendingReleases(msg.sender);
}

function claimReleaserFees() external {
    uint256 amount = releaserFeeBalance[msg.sender];
    require(amount > 0, "No fees to claim");
    releaserFeeBalance[msg.sender] = 0;
    (bool success, ) = payable(msg.sender).call{value: amount}("");
    require(success, "Transfer failed");
}
```

This eliminates partial refund complexity, ensures full fee accounting regardless of individual releaser transfer success, and makes `payReleaseFee` O(1) for the fee acceptance path (the releaser iteration for balance updates remains but involves no external calls).

**BridgeX:**
Acknowledged; we may implement a pull-based pattern in a subsequent version. For now the expected releaser set is small (2-5 addresses) so we will keep the current simple implementation.
