---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-7
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Seller `minBuyAmount` order parameter is not respected due to post application
  of trade fees
vuln_class: []
---

# Seller `minBuyAmount` order parameter is not respected due to post application of trade fees

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** The `SablierEscrow::fillOrder` function ensures that the `buyAmount` provided by the buyer is not lower than the `minBuyAmount` asked by the seller. However, the seller can receive an amount lower than `minBuyAmount` as trading fees are applied after the check.

```solidity
// Check: the buy amount meets the minimum asked.
if (buyAmount < order.minBuyAmount) {
            revert Errors.SablierEscrow_InsufficientBuyAmount(buyAmount, order.minBuyAmount);
}

... ...

// Calculate the fee on the buy amount.
feeDeductedFromSellerAmount = ud(buyAmount).mul(currentTradeFee).intoUint128();
amountToTransferToSeller -= feeDeductedFromSellerAmount;
```

**Impact:** User receives amount lower than the `minBuyAmount` asked.

**Proof of Concept:** Let's assume the following scenario:
 - Alice requested 10 WETH from buyer as `minBuyAmount`.
 - Bob fills the order by providing the 10 WETH exactly.
 - Assuming a trading fee of 1%, Alice will receive 9 WETH in total as a result instead of the 10 WETH asked.

**Recommended Mitigation:** Consider modifying and moving the if condition check after application of trade fees as shown below:

```solidity
// If the fee is non-zero, deduct the fee from both sides.
        if (currentTradeFee.unwrap() > 0) {
            ... ... ...
        }

if (amountToTransferToSeller < order.minBuyAmount) {
            revert Errors.SablierEscrow_InsufficientBuyAmount(amountToTransferToSeller, order.minBuyAmount);
        }
```

**Sablier:** In commit [edc617b](https://github.com/sablier-labs/lockup/commit/edc617bc708cd23ceac7fb65bf51076d5ae85c5d) we updated the natspec to make more explicit the purpose of this variable as being the _"minimum amount of buy token required to fill the order"_.

**Cyfrin:** Verified.
