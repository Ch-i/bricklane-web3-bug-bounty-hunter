---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Incorrect usage of minOutputAmount in executeTwoStepRedemption can cause unnecessary
  reverts
vuln_class: []
---

# Incorrect usage of minOutputAmount in executeTwoStepRedemption can cause unnecessary reverts

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** In the `RedemptionManager::executeTwoStepRedemption` function, the following call is made:

```solidity
params.liquidityProvider.supplyTo(contractAddress, params.liquidityTokenAmount, params.minOutputAmount);
```

Here, `params.minOutputAmount` is used as the minimum expected return from the liquidity provider. However, this value does not account for any fee deductions that are applied later in the function.

Immediately after the `supplyTo` call, the contract performs a slippage protection check:

```solidity
uint256 offRampBalance = params.liquidityProvider.liquidityToken().balanceOf(contractAddress);
uint256 fee = _getFee(params.feeManager, offRampBalance);

if (offRampBalance - fee < params.minOutputAmount) {
    revert Errors.SlippageControlError();
}
```

If the liquidity provider returns exactly `minOutputAmount`, then the deduction of the fee from that amount will cause `offRampBalance - fee` to fall below `minOutputAmount`, resulting in a slippage error—even though the liquidity provider met the minimum requirement.

The issue is not with the slippage check itself, which is correctly accounting for the fee. The problem is that the `minOutputAmount` passed to `supplyTo` should also include the fee, to ensure consistency with the later slippage check.

**Impact:** Unexpected transaction reverts may occur due to slippage errors, even when the liquidity provider meets the `minOutputAmount` requirement.

**Recommended Mitigation:** Update the call to `supplyTo` to include the expected fee in the `minOutputAmount` parameter. For example:

```solidity
uint256 expectedFee = _getFee(params.feeManager, params.minOutputAmount);
params.liquidityProvider.supplyTo(contractAddress, params.liquidityTokenAmount, params.minOutputAmount + expectedFee);
```

This ensures that the post-fee amount meets the expected minimum and aligns with the logic in the slippage protection check.

**Securitize:** Fixed in commit [54243f](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/54243f7e6716826c30c9561c6390fa0e05440252).

**Cyfrin:** Verified.
