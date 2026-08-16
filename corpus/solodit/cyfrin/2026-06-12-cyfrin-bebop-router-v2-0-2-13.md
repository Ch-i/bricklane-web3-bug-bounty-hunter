---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-13
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouterOrderLib::getProtocolShareFee`, `getProtocolShareSlippage` are
  not capped at `UNIT_BASE`, allowing over-range protocol shares to revert fills'
vuln_class: []
---

# `BebopRouterOrderLib::getProtocolShareFee`, `getProtocolShareSlippage` are not capped at `UNIT_BASE`, allowing over-range protocol shares to revert fills

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `getProtocolShareFee` and `getProtocolShareSlippage` unpack `uint32` bit-fields from `order.info`, returning values that range from `0` to `2^32 - 1`:

```solidity
// contracts/libraries/BebopRouterOrderLib.sol:92-98
function getProtocolShareSlippage(BebopRouterOrder calldata order) internal pure returns (uint32) {
    return uint32(order.info >> 32);
}

function getProtocolShareFee(BebopRouterOrder calldata order) internal pure returns (uint32) {
    return uint32(order.info);
}
```

These shares are treated as fractions of `UNIT_BASE` (1,000,000 = 100%) in `_distributeFees`:

```solidity
// contracts/BebopRouter.sol:474-486
uint32 protocolShareFee = order.getProtocolShareFee();
uint32 protocolShareSlippage = order.getProtocolShareSlippage();
uint256 protocolFeeShare = (feeAmount * protocolShareFee) / UNIT_BASE;
uint256 protocolSlippageShare = (slippageAmount * protocolShareSlippage) / UNIT_BASE;
...
uint256 totalMakerRefund = (feeAmount + slippageAmount) - protocolFeeShare - protocolSlippageShare;
```

If `protocolShareFee > UNIT_BASE` while `feeAmount > 0`, or `protocolShareSlippage > UNIT_BASE` while `slippageAmount > 0`, the computed protocol share can exceed its source amount. The final subtraction then underflows under Solidity 0.8 checked arithmetic and reverts the swap.

No in-scope code validates that the packed `uint32` share fields satisfy `<= UNIT_BASE`; the protection is entirely reliance on the `routerSigner` not encoding an over-range value.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::_distributeFees`
- `contracts/libraries/BebopRouterOrderLib.sol` - `getProtocolShareFee`, `getProtocolShareSlippage`

**Impact:** A routerSigner-signed order with an over-range protocol share can cause every `swap` or `settle` call using that order to revert in `_distributeFees`. The transaction revert unwinds earlier token transfers and nonce invalidation, so user funds are not lost, but the affected order remains unfillable until a corrected order is signed.

**Recommended Mitigation:** Add a defensive cap after fetching the protocol shares:

```solidity
uint32 protocolShareFee = order.getProtocolShareFee();
uint32 protocolShareSlippage = order.getProtocolShareSlippage();
require(protocolShareFee <= UNIT_BASE && protocolShareSlippage <= UNIT_BASE, InvalidProtocolShares());
```

Alternatively, clamp at read time in `getProtocolShareFee`/`getProtocolShareSlippage` or validate shares at order-hash time. Either prevents an encoding error from producing an opaque underflow revert.

**Bebop:** Fixed in commit [3c31680](https://github.com/bebop-dex/bebop-rfqa/commit/3c316807291b79c1c658ea25dd2b603c90c22b8c).

**Cyfrin:**
Verified.
