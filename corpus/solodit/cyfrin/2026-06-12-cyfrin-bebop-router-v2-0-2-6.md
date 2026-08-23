---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`HookLib::hookHash` omits order context and relies on PMM maker-nonce consumption,
  leaving maker-hook replay protection dependent on routerSigner nonce discipline'
vuln_class: []
---

# `HookLib::hookHash` omits order context and relies on PMM maker-nonce consumption, leaving maker-hook replay protection dependent on routerSigner nonce discipline

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** A maker authorizes a hook by signing `_toEIP712Digest(hookHash(hook, makerNonce))`, where `hookHash` commits to only `HOOK_SIGN_TYPE_HASH`, `hook.targetContract`, `keccak256(hook.data)`, `makerNonce`, and `hook.flags`:

```solidity
// contracts/libraries/HookLib.sol:65-73
function hookHash(Hook calldata hook, uint256 makerNonce) internal pure returns (bytes32) {
    return keccak256(abi.encode(
        HOOK_SIGN_TYPE_HASH,
        hook.targetContract,
        keccak256(hook.data),
        makerNonce,
        hook.flags
    ));
}
```

The maker's signature binds the hook body and maker nonce, but it does not bind the surrounding router order identity, receiver, fill amounts, taker amounts, or `msg.sender`.

The intended one-shot protection is the PMM maker nonce: the hook nonce is taken from the matching PMM order, so settling or canceling the PMM order should also retire the hook authorization. However, the router itself never consumes or invalidates the maker nonce. `_invalidateNonce` is called only for `ctx.routerNonce`, while maker-nonce consumption happens inside `BebopSettlement` when that maker's PMM leg settles.

This does not create a permissionless replay path across arbitrary router contexts. `HookLib.hooksHash(hooks, makerAddresses, makerNonces)` is included in `order.hash(extraInfo, hooksHashVal)`, and the router validates the `routerSigner` signature over that hash before validating maker hook signatures. Reusing the same maker hook signature in a different receiver/order context with the old router signature fails `InvalidSigner`. After a successful PMM fill, reusing the consumed maker nonce in a fresh routerSigner-signed order also reverts in the PMM settlement path.

The remaining risk is narrower: if the routerSigner/backend authorizes another order that reuses the same unconsumed PMM maker nonce, the same maker hook authorization can validate for that new signed order. The maker hook may then execute in a context the maker did not explicitly bind into the hook signature, with harm depending on the hook target's behavior.

**Files:**

- `contracts/libraries/HookLib.sol` - `HookLib::hookHash`, `HookLib::hooksHash`
- `contracts/BebopRouter.sol` - `BebopRouter::_validateSignaturesAndAccess`, `BebopRouter::_validateHookSignatures`

**Impact:** Maker hook authorization is not self-contained at the router layer and depends on the routerSigner/backend never reusing an unconsumed maker nonce in a different signed order. If that assumption fails, a maker-signed hook can execute in a different routerSigner-authorized context than the maker intended.

The concrete harm depends on the hook target, for example a `bebopHook` target that acts on `scaledSwaps` or a hook that moves maker-owned assets. Once the maker nonce has been consumed in PMM settlement, reuse of the same nonce reverts in the PMM path.

**Recommended Mitigation:** Bind the maker hook signature to the specific router order context by including the order hash, or at minimum the `routerNonce`, receiver, and relevant token/amount fields, in `HOOK_SIGN_TYPE_HASH` / `hookHash`. Additionally, consider having the router consume a hook-specific maker nonce when it validates a maker hook signature, or document and enforce backend-side uniqueness of maker nonces across all outstanding hook-authorized orders.

**Bebop:** Acknowledged.

**Cyfrin:**
Bebop accepts reliance on unique PMM maker nonces and trusted router-signer nonce discipline to prevent hook replay.
