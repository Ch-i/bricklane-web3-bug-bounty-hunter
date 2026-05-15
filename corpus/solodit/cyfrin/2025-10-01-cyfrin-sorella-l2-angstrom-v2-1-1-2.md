---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: All swaps will revert if the dynamic protocol fee is enabled since `hook-config.sol`
  does not encode the `afterSwapReturnDelta` permission
vuln_class: []
---

# All swaps will revert if the dynamic protocol fee is enabled since `hook-config.sol` does not encode the `afterSwapReturnDelta` permission

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** If `AngstromL2::setPoolHookSwapFee` is called by the owner to configure the dynamic hook protocol fee to a non-zero value then the Uniswap V4 delta accounting will result in a revert with `CurrencyNotSettled()`.

This happens because the non-zero fee delta will be accounted to the hook:

```solidity
    if (feeCurrencyId == NATIVE_CURRENCY_ID) {
        unclaimedProtocolRevenueInEther += fee.toUint128();
@>      UNI_V4.mint(address(this), feeCurrencyId, fee + taxInEther);
    } else {
@>      UNI_V4.mint(address(this), feeCurrencyId, fee);
        UNI_V4.mint(address(this), NATIVE_CURRENCY_ID, taxInEther);
    }
```

However, `hook-config.sol` does not specify that the `afterSwapReturnDelta` permission should be encoded within the hook address, so it is possible to construct the contract without it:

```solidity
Hooks.validateHookPermissions(IHooks(address(this)), getRequiredHookPermissions());
```

With this omission, the permission is false and so the unspecified hook delta is not parsed, meaning the intended `afterSwap()` return delta is not added to the caller delta and the additional protocol fee is not paid:

```solidity
    if (self.hasPermission(AFTER_SWAP_FLAG)) {
        hookDeltaUnspecified += self.callHookWithReturnDelta(
            abi.encodeCall(IHooks.afterSwap, (msg.sender, key, params, swapDelta, hookData)),
@>          self.hasPermission(AFTER_SWAP_RETURNS_DELTA_FLAG)
        ).toInt128();
    }

    function callHookWithReturnDelta(IHooks self, bytes memory data, bool parseReturn) internal returns (int256) {
        bytes memory result = callHook(self, data);

        // If this hook wasn't meant to return something, default to 0 delta
@>      if (!parseReturn) return 0;

        // A length of 64 bytes is required to return a bytes4, and a 32 byte delta
        if (result.length != 64) InvalidHookResponse.selector.revertWith();
        return result.parseReturnDelta();
    }
```

**Impact:** All swaps will revert if the dynamic protocol fee is enabled.

**Proof of Concept:** The following test should be added to `AngstromL2.t.sol`

```solidity
function test_cyfrin_SwapFeeNotSettledBecauseHookConfigMissing() public  {
    PoolKey memory key = initializePool(address(token), 10, 3);

    angstrom.setPoolHookSwapFee(key, 0.005e6); // 0.5%

    addLiquidity(key, 0, 10, 1e22);

    vm.expectRevert(bytes4(keccak256("CurrencyNotSettled()")));
    router.swap(key, true, -10e18, int24(0).getSqrtPriceAtTick());
}
```

**Recommended Mitigation:** The following permission should be added to `hooks-config.sol`:

```solidity
permissions.afterSwapReturnDelta = true;
```

**Sorella Labs:** Fixed in commit [d79a87b](https://github.com/SorellaLabs/l2-angstrom/commit/d79a87bc0153e9d75079f0a5de98f444fb9a8cd6).

**Cyfrin:** Verified. The permission has been added.
