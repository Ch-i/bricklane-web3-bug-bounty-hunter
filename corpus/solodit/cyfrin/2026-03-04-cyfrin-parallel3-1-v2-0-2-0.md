---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: Outdated accounting after burning the surplus `USDP` in `Surplus::release`
vuln_class: []
---

# Outdated accounting after burning the surplus `USDP` in `Surplus::release`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** When surplus USDP (TokenP) is burned and sent to the zero address (`address(0)`) during the `release()` function, the burn is executed via `tokenP.burnSelf(income, address(this))`, but **no update is made to the protocol's internal accounting** (`normalizedStables`, `normalizer`, or per-collateral `normalizedStables`).
```solidity
  function _release(
    uint256 _totalIncomeReceived,
    address _payee,
    ParallelizerStorage storage _ts
  )
    internal
    returns (uint256 income)
  {
    income = _totalIncomeReceived.mulDiv(_ts.shares[_payee], _ts.totalShares);
    if (_payee == address(0)) {
@>    _ts.tokenP.burnSelf(income, address(this));
    } else {
      IERC20(address(_ts.tokenP)).safeTransfer(_payee, income);
    }
    emit IncomeReleasedToPayee(income, _payee, _ts.lastReleasedAt);
  }
```

This is inconsistent with how burns are handled elsewhere:
- In normal mint/burn operations via `swapExactInput`/`swapExactOutput` (`Swapper` facet), burns correctly decrease both total and per-collateral `normalizedStables` and call `_updateNormalizer(…, false)`.
- In redemptions (`_redeem()`), burns decrease total `normalizedStables` and call `_updateNormalizer(…, false)` (without touching per-collateral values).

Because accounting is not adjusted after burning surplus USDP to `address(0)`, the protocol's tracked total issued stablecoins (`getTotalIssued()`) becomes **permanently higher than the actual circulating supply** of TokenP. This creates a persistent divergence between:

- The tracked issued amount used for collateral ratio, hard caps, redemption proportions, etc.
- The real economic supply of TokenP after the burn.

**Impact:**
- The protocol **underestimates** its true collateralization ratio (`collatRatio`) after any surplus burn to `address(0)`. The system appears less over-collateralized (or even under-collateralized in edge cases) than it actually is.
- Redemption amounts become **slightly inflated** for users (they receive more collateral than deserved because `stablecoinsIssued` in the denominator is artificially high).
- Surplus processing becomes progressively less effective: the protocol keeps minting new surplus USDP to absorb excess backing, but when that surplus is later burned to `address(0)`, the backing benefit is not removed from accounting → the system becomes increasingly over-collateralized in reality while reported metrics drift lower.
- Breaks core accounting invariant: sum of per-collateral `normalizedStables` should approximate total `normalizedStables`. Repeated surplus burns widen this gap.


**Proof of Concept:**
1. Protocol has over-collateralization → surplus exists on some collateral.
2. Governance calls `processSurplus(collateral, maxAmount)` → mints extra USDP to the contract (accounting increases `normalizedStables`).
3. Governance later calls `release()` with one payee = `address(0)` → surplus USDP is burned via `burnSelf()`.
4. Actual `TokenP.totalSupply()` decreases, but:
   - `transmuterStorage().normalizedStables` **remains unchanged**
   - `_updateNormalizer(…, false)` is **not called**
   - Reported collateral ratio is now **lower than reality**
5. The divergence grows with every subsequent surplus burn to `address(0)`.

**Recommended Mitigation:** Since the burning of USDP during surplus release to address(0) is not tied to any specific collateral (unlike a swap burn which is collateral-specific), it is only needed to call `_updateNormalizer()` to proportionally reduce the tracked issued amount across all collaterals.

In `LibSurplus::_release`:
```solidity
if (_payee == address(0)) {
    _updateNormalizer(income, false);
    _ts.tokenP.burnSelf(income, address(this));
}
```
This:
- Matches the redemption burn pattern (where no specific collateral is burned against)
- Lets _updateNormalizer() handle the scaling of normalizedStables and renormalization (if the normalizer falls below BASE_18 or exceeds BASE_36)
- Avoids incorrectly attributing the burn to any single collateral's normalizedStables

**Parallel:** Acknowledged. The current design is that the `USDp` burned during the release process is the amount that's going to be minted by the Savings contract, as a result, no net changes to the backing.
