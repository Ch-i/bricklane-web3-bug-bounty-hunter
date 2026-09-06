---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Zero-for-one swaps will revert for small input amounts relative to the specified
  priority fee
vuln_class: []
---

# Zero-for-one swaps will revert for small input amounts relative to the specified priority fee

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** For zero-for-one native token swaps, a sufficiently large priority fee relative to the swap amount will cause a revert with `HookDeltaExceedsSwapAmount()`. This is because the calculated swap tax is greater than the native token provided for the swap; however, the `Hooks::beforeSwap` logic explicitly prevents this scenario in which the returned hook delta would cause the swap semantics to change:

```solidity
// Update the swap amount according to the hook's return, and check that the swap type doesn't change (exact input/output)
if (hookDeltaSpecified != 0) {
    bool exactInput = amountToSwap < 0;
    amountToSwap += hookDeltaSpecified;
    if (exactInput ? amountToSwap > 0 : amountToSwap < 0) {
        HookDeltaExceedsSwapAmount.selector.revertWith();
    }
}
```

**Proof of Concept:** The following test should be added to `AngstromL2.t.sol`

```solidity
/*
 * Reverts with HookDeltaExceedsSwapAmount because calculated tax amount is 0.00343e18 which is
 * more ETH than it provided
 */
function test_cyfrin_verySmallZeroForOneSwap() public {
    uint256 PRIORITY_FEE = 0.7 gwei;
    PoolKey memory key = initializePool(address(token), 10, 3);

    setupSimpleZeroForOnePositions(key);
    setPriorityFee(PRIORITY_FEE);

    bytes4 selector = bytes4(keccak256("HookDeltaExceedsSwapAmount()"));
    vm.expectRevert(selector);
    router.swap(key, true, -0.00342e18, int24(-35).getSqrtPriceAtTick());
}

```

**Sorella Labs:** If they're expecting to pay more in tax than to swap then it doesn't make sense to complete the tx in the first place. Believe this to be a non-issue.

**Cyfrin:** Acknowledged.
