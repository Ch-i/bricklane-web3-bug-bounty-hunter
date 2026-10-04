---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-2-3
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[L-04] Inappropriate slippage control is present in settleWithETH(...)'
vuln_class: []
---

# [L-04] Inappropriate slippage control is present in settleWithETH(...)

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchAuctionMarketplace.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchAuctionMarketplace.sol#L790)

**Description:**

`settleWithETH(...)` allows an NFT buyer to send ETH to purchase an NFT. The ETH is converted into DUTCH via the `DUTCHBondingHook` to settle for users in `AuctionAssist`.

```solidity
function settleWithETH(uint256 listingId_, uint256 maxPriceETH_) external payable whenNotPaused nonReentrant
{
    //...
    // 5. Get current NFT price, convert to DUTCH, and check slippage.
    CurrentPrice memory currentPrice_ = _getCurrentPrice(listingId_);
    if (currentPrice_.priceETH > maxPriceETH_) revert SlippageExceeded();

    // 6. Mark as settled (before external calls).
    listing_.settled = true;

    // 7. Swap ETH for exact DUTCH amount via bonding hook.
    // Hook will refund excess ETH back to this contract.
    uint256 ethUsed_ = _bondingHook.swapETHForDUTCH{value: msg.value}(
        currentPrice_.priceDUTCH,
        address(this)
    );
    //...
}
```

However, during the slippage check, the NFT's ETH price is used directly for comparison. The slippage from the DUTCH price in the transaction is not accounted for and cannot be controlled via parameters.

**Impact:** The actual ETH paid by the user may exceed the slippage parameter `maxPriceETH_`.

**Recommendation:** It is recommended to perform the slippage check by comparing `ethUsed_` with `maxPriceETH_`.

**Status:** Fixed

**Client response:** Fixed in [1b78ffeecea23ba20aaec534a580b35366dc6bda](https://github.com/dutch-protocol/Protocol-Contracts/commit/1b78ffeecea23ba20aaec534a580b35366dc6bda)
