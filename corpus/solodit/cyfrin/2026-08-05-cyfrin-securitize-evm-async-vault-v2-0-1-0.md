---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: Double rounding in partial redemption allows reserve extraction without equivalent
  DS Token burn
vuln_class: []
---

# Double rounding in partial redemption allows reserve extraction without equivalent DS Token burn

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** `AsyncFundVault::fulfillRedemptions` can commit more liquidity than the economic value of the DS Tokens it actually burns. A redeemer can consequently receive reserve assets while retaining part or all of the DS Tokens that should have funded that payment.

For a partially funded generation, the function first rounds the generation-wide fulfillment rate down, assigns all available liquidity to the generation, and then rounds the DS Token burn down a second time. The committed liquidity is not recomputed from the resulting integer burn amount.

```solidity
// contracts/AsyncFundVault.sol
if (availableLiquidity >= totalRedemptionValue) {
    fulfillmentRate = WAD;
    totalLiquidityCommitted = totalRedemptionValue;
} else {
    fulfillmentRate = (availableLiquidity * WAD) / totalRedemptionValue;
    totalLiquidityCommitted = availableLiquidity;
}

uint256 burnAmount = (totalShares * fulfillmentRate) / WAD;
if (burnAmount > 0) {
    $.dsToken.burn(address(this), burnAmount, "AsyncFundVault: redemption");
}
```

This composes two floor operations as follows.

```text
fulfillmentRate = floor(availableLiquidity * WAD / totalRedemptionValue)
burnAmount = floor(totalShares * fulfillmentRate / WAD)
totalLiquidityCommitted = availableLiquidity
```

The required solvency relationship is that `totalLiquidityCommitted` must not exceed the NAV value of `burnAmount`. The current formulas do not preserve that relationship. For example, consider a two-decimal DS Token with a NAV of 1,000,000 liquidity tokens. Each DS Token base unit is worth 10,000 liquidity tokens. If a redeemer requests three base units and the vault has 20,000 liquidity tokens available, `totalRedemptionValue` is 30,000 and the rounded fulfillment rate is `666666666666666666`. Multiplying three by this rate and rounding down burns only one base unit, worth 10,000, even though the generation commits 20,000. On claim, the redeemer receives the full 20,000 and gets the other two base units back.

The more extreme boundary occurs when available liquidity is worth less than one DS Token base unit. The calculated `burnAmount` is then zero while `totalLiquidityCommitted` remains all available liquidity. The redeemer receives that liquidity and recovers the complete DS Token request, allowing the same tokens to be submitted again in a later generation. This does not permit an unbounded zero-burn withdrawal in a single generation. For an exactly linear NAV conversion and `totalShares < WAD`, the overcommit is strictly less than one DS Token base-unit value plus `totalRedemptionValue / WAD`; the ordinary asset-conversion floor adds only its base-unit residue. Repetition also requires the settler to progress through additional generations.

**Impact:** Partial fulfillment can release more liquidity than the NAV value of the DS Tokens burned while returning the unburned portion with its economic rights intact. The client confirmed that supported DS Token precision ranges from 0 to 18 decimals, normally six. At low precision, one base unit can represent a full economically valuable DS Token, and the zero-burn boundary returns that token for reuse in later generations after liquidity has been paid. Because the code imposes no NAV cap, repeated partial settlements can produce material reserve loss in a supported configuration, which supports Medium. Ordinary six-decimal configurations reduce the per-generation discrepancy to dust.

**Recommended Mitigation:** Finalize the integer burn amount first, then derive committed liquidity from that exact burn and leave any residual uncommitted. Enforce that committed liquidity never exceeds the NAV value removed from circulation, including zero-burn boundaries.

**Securitize:** Fixed in commit [cec2082](https://github.com/securitize-io/bc-async-ramp-sc/commit/cec2082e3b6808c35a050dd950756f5a8e66596b).

**Cyfrin:** Verified.


\clearpage
