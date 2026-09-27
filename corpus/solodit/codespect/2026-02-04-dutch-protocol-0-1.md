---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-0-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[H-02] Contributions not reset after purchase allows infinite reward claims'
vuln_class: []
---

# [H-02] Contributions not reset after purchase allows infinite reward claims

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`AuctionAssist.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/AuctionAssist.sol#L309)

**Description:**

The `recordPurchase(...)` function calculates contributor shares based on their contribution amounts stored in `_contributions[contributor_][collection_].amount`. However, after recording a purchase and snapshotting the shares, these contribution amounts are never reset.

```solidity
function recordPurchase(...) external returns (uint256 purchaseId_) {
    // ...
    for (uint256 i; i < contributors_.length; ++i) {
        address contributor_ = contributors_[i];
        // @audit contribution amount is read but never reset
        uint256 contributionAmount_ =
            _contributions[contributor_][collection_].amount;

        if (contributionAmount_ > 0) {
            uint256 shareBPS_ = (contributionAmount_ * 10000) / costETH_;
            // ...
            _purchaseShares[purchaseId_][contributor_] = shareBPS_;
            purchase_.contributors.push(contributor_);
        }
    }
    // @audit no reset of _contributions[contributor_][collection_].amount
}
```

**Impact:** This allows a contributor who made a single contribution to receive reward shares for every subsequent NFT purchase from that collection indefinitely:

1. User contributes 1 ETH to Collection A;
2. NFT 1 is purchased for 2 ETH — User receives 50% share (1 ETH / 2 ETH);
3. NFT 2 is purchased for 2 ETH — User still has 1 ETH recorded, receives another 50% share;
4. This repeats for every future purchase, draining rewards meant for new contributors.

The vulnerability effectively allows infinite DUTCH token extraction from a single contribution, severely diluting rewards for legitimate contributors and draining protocol funds.

**Recommendation:** Reset contribution amounts after recording a purchase.

**Status:** Fixed

**Client response:** Fixed in commit [b5bacb594faa34b4d77a87588f0b8fbd0b781b6d](https://github.com/dutch-protocol/Protocol-Contracts/commit/b5bacb594faa34b4d77a87588f0b8fbd0b781b6d)
