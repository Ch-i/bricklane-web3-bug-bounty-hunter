---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[M-01] Bonding-curve taxes and burn revenue cannot be distributed within the
  collection'
vuln_class: []
---

# [M-01] Bonding-curve taxes and burn revenue cannot be distributed within the collection

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DUTCHBondingHook.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DUTCHBondingHook.sol)

**Description:**

Bonding-curve taxes and burn revenue are sent to the `DutchVault`. These revenues are distributed according to the basis-point weights configured by the owner, increasing the available funds for NFT purchases in each collection. This process is carried out in the `receive()` function.

```solidity
function withdrawExcessReserve(uint256 amount_) external onlyOwner {
    //...
    IERC20(Currency.unwrap(_wethCurrency)).safeTransfer(
        _dutchVault,
        amount_
    );
    emit ExcessReserveWithdrawn(amount_, _dutchVault);
}

function _executeBuy(...) internal returns (...) {
    //...
    // Distribute tax.
    (uint256 vaultAmount_, uint256 opsAmount_) =
        _calculateBuyTax(taxAmount_);
    IERC20(Currency.unwrap(_wethCurrency)).safeTransfer(
        _dutchVault,
        vaultAmount_
    );
    //...
}

function _executeSell(...) internal returns (...) {
    //...
    // Distribute tax.
    (uint256 vaultAmount_, uint256 opsAmount_) =
        _calculateBuyTax(taxAmount_);
    IERC20(Currency.unwrap(_wethCurrency)).safeTransfer(
        _dutchVault,
        vaultAmount_
    );
    //...
}
```

However, when sending bonding-curve taxes and burn revenue, WETH is transferred directly instead of being unwrapped into ETH.

**Impact:** Bonding-curve taxes and burn revenue are sent as WETH to the `DutchVault`, and there is no function in `DutchVault` to unwrap WETH. This causes the revenue distribution to not actually occur, leaving the WETH stuck.

**Recommendation:** It is recommended to unwrap the revenue into ETH before sending it to the `DutchVault`.

**Status:** Fixed

**Client response:** Fixed in commit [734d928fa3344927a8ac14a402778486cdc8e6cf](https://github.com/dutch-protocol/Protocol-Contracts/commit/734d928fa3344927a8ac14a402778486cdc8e6cf)
