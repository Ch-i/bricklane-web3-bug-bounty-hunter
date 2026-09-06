---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-19-cyfrin-bunni-fee-override-hooklet-v2-0-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-19-cyfrin-bunni-fee-override-hooklet-v2-0
title: No need to bound the fee override in `FeeOverrideHooklet::setFeeOverride` as
  it is clamped in `HookletLib::beforeSwap`
vuln_class: []
---

# No need to bound the fee override in `FeeOverrideHooklet::setFeeOverride` as it is clamped in `HookletLib::beforeSwap`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md)_

---

**Description:** `FeeOverrideHooklet::setFeeOverride` bounds the overridden fees to prevent them from exceeding `SWAP_FEE_BASE`:

```solidity
function setFeeOverride(
    PoolId id,
    bool overrideZeroToOne,
    uint24 feeZeroToOne,
    bool overrideOneToZero,
    uint24 feeOneToZero
) public {
    if (feeZeroToOne >= SWAP_FEE_BASE || feeOneToZero >= SWAP_FEE_BASE) {
        revert FeeOverrideHooklet__InvalidSwapFee();
    }

    ...
}
```

Assuming L-01 is correctly mitigated as suggested, it is not strictly necessary to perform this validation in the hooklet as fees will be clamped by the `HookletLib::beforeSwap` logic.

**Recommended Mitigation:** Avoid performing the same validation in multiple instances and instead rely on the behavior of core Bunni contracts.

```diff
    function setFeeOverride(
        PoolId id,
        bool overrideZeroToOne,
        uint24 feeZeroToOne,
        bool overrideOneToZero,
        uint24 feeOneToZero
    ) public {
-       if (feeZeroToOne >= SWAP_FEE_BASE || feeOneToZero >= SWAP_FEE_BASE) {
-           revert FeeOverrideHooklet__InvalidSwapFee();
-       }

        ...
    }
```

**Bacon Labs:** Acknowledged. We're going to keep this validation vs relying solely on the clamping behavior in the core contracts. Without this validation there is a scenario where a pool curator can set a fee higher than the maximum allowable value, which is then clamped to the maximum value in the core contracts, leading to a swap fee value that differs from the one set by the curator. Keeping this validation removes the potential for confusion and does not otherwise hurt to have it beyond the minor increase in gas costs.

**Cyfrin:** Acknowledged.

\clearpage
