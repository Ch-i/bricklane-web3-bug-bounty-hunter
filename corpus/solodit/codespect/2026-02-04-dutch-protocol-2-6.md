---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-2-6
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[L-07] Unused vaultFee'
vuln_class: []
---

# [L-07] Unused vaultFee

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchAuctionMarketplace.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchAuctionMarketplace.sol#L991)

**Description:**

In `DutchAuctionMarketplace`, selling an NFT incurs a `_sellerFeeOnSettled`. In the `_settleInternal(...)` function, a portion of `_dutchToken` is sent to the `dutchVault` as `vaultFee_`.

```solidity
function _settleInternal(...) internal {
    //...
    if (vaultFee_ != 0) {
        IERC20(address(_dutchToken)).safeTransfer( //NOTE
            _dutchVaultAddress, vaultFee_
        );
    }
    //...
}
```

However, in `dutchVault`, this portion of `_dutchToken` fees is not utilized.

**Impact:** The `_dutchToken` fees that are sent will be stuck.

**Recommendation:** It is recommended to merge `vaultFee_` into `burnFee` and burn the corresponding `_dutchToken`.

**Status:** Acknowledged

**Client response:** We acknowledge this issue. We are aware, that dutch vault cannot currently handle incoming DUTCH token, but we keep it in the fee split for potential future replacement of `DutchVault` with a new implementation, that would need the DUTCH token to be send to it.
