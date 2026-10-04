---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-1-5
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[M-06] The swapETHForDUTCH function does not charge royalty fees'
vuln_class: []
---

# [M-06] The swapETHForDUTCH function does not charge royalty fees

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DUTCHBondingHook.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DUTCHBondingHook.sol#L734)

**Description:**

Purchasing DUTCH through Uniswap V4 requires paying a 10% tax fee. The `swapExactETHForDUTCH(...)` function, used in `DutchAuctionMarketplace` to swap ETH for DUTCH when buying NFTs, does not incur the tax fee.

```solidity
function swapETHForDUTCH(...)
    external
    payable
    whenNotPaused
    nonReentrant
    returns (uint256 ethUsed_)
{
    //...
    // 1. Calculate ETH needed (no tax for marketplace).
    ethUsed_ = _calculateMintCost(exactDutchAmount_);
    //...
}
```

However, in `DutchAuctionMarketplace`, listing and settlement lack access control. A user can list their own NFT, set `minPrice` to 0 to avoid paying the listing fee, and then call `settleWithETH(...)` to buy their own listed NFT. The ETH they input will be swapped for DUTCH with 0 tax fee, and they only need to pay a 2.5% marketplace fee. This allows them to acquire DUTCH while bypassing most of the tax fee.

**Impact:** `swapExactETHForDUTCH(...)` could be exploited to acquire DUTCH at a lower fee.

**Recommendation:** It is recommended to apply the tax fee in `swapETHForDUTCH(...)` for listings that are not from `DutchVault`.

**Status:** Fixed

**Client response:** Fixed in commit [2dfad0d5e39282955bd2a1098d5d9d249be003ff](https://github.com/dutch-protocol/Protocol-Contracts/commit/2dfad0d5e39282955bd2a1098d5d9d249be003ff)

**Client response:** The preview fix is reverted and a new is implemented in [PR-99](https://github.com/dutch-protocol/Protocol-Contracts/pull/99). Previously, we added tax to all `settleWithETH` purchases. That is undesired behaviour. In the new PR, we keep no tax, but only protocol listings can be bought with ETH. This prevents this attack vector. Also, in this PR we add a view method on the hook to get the current no tax ETH needed for the purchase.

**Client response:** Fixed in [ee8512b51c68567c69237d215e56754d2cd2ca96](https://github.com/dutch-protocol/Protocol-Contracts/commit/ee8512b51c68567c69237d215e56754d2cd2ca96)
