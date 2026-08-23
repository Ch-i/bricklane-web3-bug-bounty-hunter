---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-7
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
title: BebopRouter ignores PMM partnerId referral fees, allowing maker output to arrive
  below the router's expected delivery
vuln_class: []
---

# BebopRouter ignores PMM partnerId referral fees, allowing maker output to arrive below the router's expected delivery

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `BebopSettlement` supports a maker-signed `partnerId` embedded in the PMM order flags. The partner ID is included in the maker's PMM signature, but the router decodes only the PMM event ID from the flags and does not account for partner fees.

For single orders, settlement extracts the partner ID from `order.flags` and passes it into `_transferToken` for the maker-to-receiver transfer:

```solidity
// external/bebop-settlement/src/BebopSettlement.sol:274-295
(uint128 eventId, uint64 partnerId) = Order.extractFlags(order.flags);
...
_transferToken(
    order.maker_address, order.receiver, order.maker_token, newMakerAmount,
    makerUsingPermit2 ? Commands.PERMIT2_TRANSFER : Commands.SIMPLE_TRANSFER,
    makerHasNative ? Transfer.Action.Unwrap : Transfer.Action.None, partnerId
);
```

`BebopTransfer::_transferToken` then deducts the registered partner fee from the maker transfer before sending the remainder to the router:

```solidity
// external/bebop-settlement/src/base/BebopTransfer.sol:93-107
if (partnerInfo.registered && partnerInfo.fee > 0) {
    fee = amount * partnerInfo.fee / HUNDRED_PERCENT;
}
...
IERC20(token).safeTransferFrom(from, partnerInfo.beneficiary, fee);
amount -= fee;
IERC20(token).safeTransferFrom(from, receiver, amount);
```

The aggregate path applies the same deduction in `_transferMakerTokens`.

The router's decoded `pmm.pmmMakerAmount` remains the pre-fee PMM maker amount. `_calculateAmounts` and `_distributeFees` therefore reason about the gross maker delivery, while the actual `pmmToToken` balance received by the router is net of the partner fee:

```solidity
// contracts/BebopRouter.sol:450-455
feePool = pmmToBalance > calc.toAmountAfterFeeSlippage
    ? pmmToBalance - calc.toAmountAfterFeeSlippage
    : 0;
```

If the partner-fee-reduced delivery is below the router's required receiver floor, exactOut fills and exactIn fills with a positive `limitAmount` revert with `LimitAmountViolation` even though the decoded PMM `maker_amount` appeared sufficient before settlement applied the partner fee.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::_distributeFees`, `BebopRouter::_executeSwapCore`
- `contracts/base/BebopPmmHelper.sol` - `BebopPmmHelper::_decodeSinglePmm`, `BebopPmmHelper::_decodeAggregatePmm`
- `external/bebop-settlement/src/BebopSettlement.sol` - `BebopSettlement::_executeSingleOrder`, aggregate/multi settlement paths
- `external/bebop-settlement/src/base/BebopTransfer.sol` - `BebopTransfer::_transferToken`, `BebopTransfer::_transferMakerTokens`
- `external/bebop-settlement/src/base/BebopPartner.sol` - partner fee registration and `HUNDRED_PERCENT`

**Impact:** When a maker signs a PMM order with a nonzero registered `partnerId`, the router may receive less `pmmToToken` than the PMM `maker_amount` it decoded and used for quote/accounting decisions.

For exactOut, or exactIn orders with a positive `limitAmount` above the net delivery, the fill reverts and must be reissued without the partner fee or with amounts adjusted for it.

**Recommended Mitigation:** Either reject PMM orders with nonzero `partnerId` in the router path, or explicitly account for the net maker delivery after the partner fee. If partner-fee PMM orders must be supported, decode `partnerId`, obtain the registered fee rate from the PMM settlement contract, and compute/check the expected net `pmmToToken` delivery before applying fee distribution and receiver floors.

**Bebop:** Acknowledged.
