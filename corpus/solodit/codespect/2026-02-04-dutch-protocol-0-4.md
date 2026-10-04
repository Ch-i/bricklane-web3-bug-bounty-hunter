---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-0-4
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
title: '[H-05] Inverted sign convention for amountSpecified breaks swap logic'
vuln_class: []
---

# [H-05] Inverted sign convention for amountSpecified breaks swap logic

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DUTCHBondingHook.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DUTCHBondingHook.sol#L905)

**Description:**

The `_executeBuy(...)` and `_executeSell(...)` functions interpret the sign of `params.amountSpecified` to determine swap type. In Uniswap V4, the sign convention is:

- Negative: Exact Input → User specifies exact amount to pay;
- Positive: Exact Output → User specifies exact amount to receive.

The hook inverts this convention:

```solidity
function _executeBuy(...) internal returns (...) {
    // ...
    // @audit inverted - positive should be exact output, not exact input
    if (params_.amountSpecified > 0) {
        // Hook treats this as "Exact Input"
        inputAmount_ = uint256(params_.amountSpecified);
        // ...
    } else {
        // Hook treats this as "Exact Output"
        outputAmount_ = uint256(-params_.amountSpecified);
        // ...
    }
}
```

The V4 source code confirms the correct convention in `lib/v4-core/src/libraries/Hooks.sol`.

**Impact:** This causes the specified and unspecified amounts to be swapped together in the `afterSwap` hook in V4, eventually causing the transaction to revert.

**Recommendation:** Invert the condition to match V4's sign convention:

```solidity
if (params_.amountSpecified < 0) {
    // Exact Input - user specifies input amount (negative in V4)
    inputAmount_ = uint256(-params_.amountSpecified);
    // ... exact input logic
} else {
    // Exact Output - user specifies output amount (positive in V4)
    outputAmount_ = uint256(params_.amountSpecified);
    // ... exact output logic
}
```

Same fix can be applied ot `_executeSell(...)`.

**Status:** Fixed

**Client response:** Fixed in commit [c79da4114ffd2b47c5fd313bfd38ec1ca8540044](https://github.com/dutch-protocol/Protocol-Contracts/commit/c79da4114ffd2b47c5fd313bfd38ec1ca8540044)

**CODESPECT fix review:** Fixed due to the removal of the hook design.
