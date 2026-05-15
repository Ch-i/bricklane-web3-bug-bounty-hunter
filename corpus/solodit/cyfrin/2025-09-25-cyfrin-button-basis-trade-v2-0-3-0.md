---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Redundant variable statements
vuln_class: []
---

# Redundant variable statements

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** In `BasisTradeVault` the functions `maxMint`, `mint`, `withdraw`, and `redeem` are overrides of the standard ERC4626 interface. In this contract, these functions are intentionally disabled to enforce a custom deposit and withdrawal flow (e.g., using `requestWithdraw` and `requestRedeem` instead of the standard `withdraw` and `redeem`).

Because these functions are disabled and immediately revert or return a fixed value, their parameters (`receiver`, `shares`, `assets`, `owner`) are not used within the function bodies. The code explicitly acknowledges this by placing the parameter names on their own lines (e.g., `receiver;`), which silences compiler warnings about unused variables but is redundant.

**Recommended Mitigation:** An alternative way to denote unused parameters, which can improve clarity, is to write the function declarations without the parameters (e.g., `foo(uint256, address)`). This is a common convention in Solidity to signal that a parameter is intentionally unused.

```solidity
// ...existing code...
    /**
     * @notice Mint function is disabled
     * @dev This vault only supports asset-based deposits
     */
    function mint(uint256 /*shares*/, address /*receiver*/) public virtual override returns (uint256) {
        revert("Mint disabled: use deposit");
    }

    // ============================================
// ...existing code...
    /**
     * @notice Standard withdraw function is disabled
     * @dev Users must use requestWithdraw instead
     */
    function withdraw(
        uint256 /*assets*/,
        address /*receiver*/,
        address /*owner*/
    ) public virtual override returns (uint256) {
        revert("Withdraw disabled: use requestWithdraw");
    }

    /**
     * @notice Standard redeem function is disabled
     * @dev Users must use requestRedeem instead
     */
    function redeem(
        uint256 /*shares*/,
        address /*receiver*/,
        address /*owner*/
    ) public virtual override returns (uint256) {
        revert("Redeem disabled: use requestRedeem");
    }

// ...existing code...
    /**
     * @notice Returns the maximum shares that can be minted
     * @dev Always returns 0 as mint is disabled
     * @param receiver Address that would receive the shares
     * @return Always 0 (mint disabled)
     */
    function maxMint(address /*receiver*/) public view virtual override returns (uint256) {
        return 0; // Mint is disabled
    }
}
```

**Button:** FIxed in commit [`9d8ed75`](https://github.com/buttonxyz/button-protocol/commit/9d8ed75bd5ed4957c7b23f9b06ff362b7bb218a4)

**Cyfrin:** Verified.
