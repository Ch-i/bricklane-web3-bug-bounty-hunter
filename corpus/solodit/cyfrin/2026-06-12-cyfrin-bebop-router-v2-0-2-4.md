---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::settle` relayer can dust-fill an order with a tiny exactAmount,
  consuming the user''s nonce and griefing the intended fill'
vuln_class: []
---

# `BebopRouter::settle` relayer can dust-fill an order with a tiny exactAmount, consuming the user's nonce and griefing the intended fill

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `exactAmount` is a function argument of `settle`, not a field of the signed `BebopRouterOrder`, so it is not covered by either the router-signer or user signature. The user's nonce is consumed inside `_validateAndPrepare`, *before* the swap executes:

```solidity
// BebopRouter.sol:248
_invalidateNonce(isSettle ? order.tokensOwner : msg.sender, ctx.routerNonce); // @audit consumed before the fill, on any successful exactAmount
```
A relayer can therefore submit a user's gasless order with a very small positive `exactAmount` (a partial fill). The PMM partial-fills it successfully, the transaction succeeds, and the user's `routerNonce` is permanently invalidated — so the user's intended full-size fill can no longer be executed against that signed order.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::settle` (lines 205, 248)

**Impact:** Griefing of a user's intended swap. A malicious or competing relayer can burn a user's signed `settle` order for a negligible fill, wasting the user's quote and round-trip. No direct fund loss beyond the dust fill. Note this is partly inherent to partial-fill RFQ designs, but the relayer-chosen (unsigned) `exactAmount` makes it freely griefable rather than user-controlled.

**Recommended Mitigation:** Include `exactAmount` (or a minimum fill size) in the signed order.

**Bebop:** Acknowledged.

**Cyfrin:**
Bebop accepts the dust-fill risk because settle is submitted only by a trusted Bebop-controlled relayer.
