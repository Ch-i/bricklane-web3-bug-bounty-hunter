---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[H-01] Contribution oversubscription will cause calimReward(...) call revert
  due to insufficient funds for late callers'
vuln_class: []
---

# [H-01] Contribution oversubscription will cause calimReward(...) call revert due to insufficient funds for late callers

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`AuctionAssist.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/AuctionAssist.sol)

**Description:**

The `recordPurchase(...)` function allows total contribution shares to exceed 100% when multiple users contribute to a collection. The function caps each individual user's share at 10,000 BPS (100%), but does not normalize the total when the sum of all shares exceeds 10,000 BPS.

```solidity
function recordPurchase(...) external returns (uint256 purchaseId_) {
    //...
    // 7. Calculate and store contributor shares based on actual cost.
    for (uint256 i; i < contributors_.length; ++i) {
        address contributor_ = contributors_[i];
        uint256 contributionAmount_ =
            _contributions[contributor_][collection_].amount;

        if (contributionAmount_ > 0) {
            // Calculate share as (contribution * 10000) / cost.
            // @audit The total of `contributionAmount_` may be greater than `costETH_`.
            uint256 shareBPS_ =
                (contributionAmount_ * 10000) / costETH_;

            // Cap at 10000 BPS (100%) to prevent over-distribution.
            if (shareBPS_ > 10000) {
                shareBPS_ = 10000;
            }

            _purchaseShares[purchaseId_][contributor_] = shareBPS_;
            purchase_.contributors.push(contributor_);
        }
    }
    //...
}
```

If user A contributed 50% of the NFT price and user B contributed 60%, the late `claimReward(...)` caller's transaction will either revert, or pull the tokens that belong to other users from different contributed settlements, causing their claim call to revert.

**Impact:** Contribution oversubscription will cause 100% fund loss for late `claimReward(...)` callers.

**Recommendation:** Remove contribution oversubscription option for a single purchase or normalize shares proportionally when total exceeds 10,000 BPS.

**Status:** Fixed

**Client response:** Fixed in [74ee906fd0f0588124acef2486a951415685e31d](https://github.com/dutch-protocol/Protocol-Contracts/commit/74ee906fd0f0588124acef2486a951415685e31d)
