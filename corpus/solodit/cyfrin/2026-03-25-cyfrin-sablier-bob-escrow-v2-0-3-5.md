---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Fee calculations round in favor of the user instead of the protocol
vuln_class: []
---

# Fee calculations round in favor of the user instead of the protocol

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Fee calculations in both `SablierLidoAdapter` and `SablierEscrow` use `UD60x18::mul` which internally computes `(a * b) / 1e18` — this division truncates (rounds down). Since fees are amounts the protocol collects, rounding down means the protocol receives less than the exact amount and the user retains more. The standard practice is to round fees up (in favor of the protocol).

In `SablierLidoAdapter::calculateAmountToTransferWithYield` (`SablierLidoAdapter.sol:186-187`):
```solidity
feeAmount = ud(yieldAmount).mul(_vaultYieldFee[vaultId]).intoUint128();
amountToTransfer = userWethShare - feeAmount;
```

In `SablierEscrow::fillOrder` (`SablierEscrow.sol:212-217`):
```solidity
feeDeductedFromBuyerAmount = ud(order.sellAmount).mul(currentTradeFee).intoUint128();
amountToTransferToBuyer -= feeDeductedFromBuyerAmount;

feeDeductedFromSellerAmount = ud(buyAmount).mul(currentTradeFee).intoUint128();
amountToTransferToSeller -= feeDeductedFromSellerAmount;
```

In all three cases, `mul` truncates, so the fee rounds down — against the protocol.

For comparison, the non-fee calculation `userWstETH * totalWeth / totalWstETH` correctly rounds down (user receives less, protocol retains dust).

**Impact:** The protocol collects slightly less fees than the exact amount on every redemption and trade. The per-transaction loss is at most 1 wei due to UD60x18's 18-decimal precision, but it accumulates over time and violates the principle that rounding should always favor the protocol.

Incorrect rounding directions have historically been used as part of blackhat exploit chains so using correct rounding directions is a good defensive practice.

**Recommended Mitigation:** Use ceiling division for fee calculations. PRBMath does not provide a `mulDiv18Up`, so add 1 wei when there is a remainder:
```solidity
uint256 raw = ud(yieldAmount).mul(_vaultYieldFee[vaultId]).unwrap();
feeAmount = raw + 1; // round up by 1 wei to favor the protocol
```

Or implement a `mulDivUp` helper: `(a * b + denominator - 1) / denominator`.

**Sablier:** Acknowledged; we decided not to implement the change, we are ok with the dust.
