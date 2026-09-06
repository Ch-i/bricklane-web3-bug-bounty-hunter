---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::invalidateNonce` is keyed to msg.sender, so open orders cannot
  be globally cancelled and are single-use per caller'
vuln_class: []
---

# `BebopRouter::invalidateNonce` is keyed to msg.sender, so open orders cannot be globally cancelled and are single-use per caller

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** Replay protection for an order is a bitmap nonce, but the **owner** the nonce is keyed to is chosen by the entry path:

```solidity
// BebopRouter.sol:248  _validateAndPrepare
_invalidateNonce(isSettle ? order.tokensOwner : msg.sender, ctx.routerNonce); // @audit swap keys nonce to msg.sender
```

For `swap`, the key is the volatile `msg.sender`. The access check additionally allows *any* caller when the order is authored as an "open" order (`tokensOwner == address(0)`):

```solidity
// BebopRouter.sol:351
require(isSettle || order.tokensOwner == address(0) || msg.sender == order.tokensOwner, InvalidMsgSender());
// @audit tokensOwner == 0  ⇒ passes for every caller
```

Because each caller's nonce lives in its own bitmap (`_nonces[owner][slot]`, `BebopValidation.sol:84-91`), caller A consuming nonce `N` does not mark `N` consumed for caller B. So one routerSigner-signed open order is **single-use per caller**, not globally single-use.

The user-cancel path is keyed the same way and therefore cannot retire an open order:

```solidity
// BebopRouter.sol:103-106
function invalidateNonce(uint256 nonce) external {
    _invalidateNonce(msg.sender, nonce); // @audit only burns the caller's own bitmap
    emit NonceInvalidated(msg.sender, nonce);
}
```

A routerSigner (or anyone) calling `invalidateNonce(N)` only burns `N` in **their own** bitmap; it does not invalidate `N` for the open order across other potential callers. So an outstanding open order **cannot be revoked on-chain** — the only thing that retires it is `expiry` (`info`-packed).

**Impact:** Operational / order-lifecycle, not loss of funds:
- An outstanding open order (`tokensOwner == 0`) **cannot be cancelled before expiry**. If its terms need to be retired early — market move, fee/oracle/checker reconfiguration, or an order issued in error — there is no on-chain lever; the issuer can only wait out `expiry` (so the only mitigation is issuing open orders with short expiries).
- The same order is **executable once per distinct caller** rather than once globally, so any "single-use authorization" intent is not enforced on-chain for open orders.


**Recommended Mitigation:** Consider making open orders globally single-use. Key the nonce to the signed `order.tokensOwner` in both paths rather than the call-volatile `msg.sender`:

```diff
- _invalidateNonce(isSettle ? order.tokensOwner : msg.sender, ctx.routerNonce);
+ _invalidateNonce(order.tokensOwner, ctx.routerNonce);
```
If cancelability option for open orders is desirable, consider adding an owner gated function for the same:

```solidity
function invalidateOpenNonce(uint256 nonce) external onlyOwner { // or routerSigner-gated
    _invalidateNonce(address(0), nonce);
    emit NonceInvalidated(address(0), nonce);
}
```

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.
