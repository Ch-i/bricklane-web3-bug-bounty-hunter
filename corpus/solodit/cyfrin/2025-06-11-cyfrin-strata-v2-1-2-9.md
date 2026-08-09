---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: '`pUSDeVault::maxWithdraw` doesn''t account for withdrawal pausing, in violation
  of EIP-4626 which can break protocols integrating with `pUSDeVault`'
vuln_class: []
---

# `pUSDeVault::maxWithdraw` doesn't account for withdrawal pausing, in violation of EIP-4626 which can break protocols integrating with `pUSDeVault`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** [EIP-4626](https://eips.ethereum.org/EIPS/eip-4626) states on `maxWithdraw`:
> MUST factor in both global and user-specific limits, like if withdrawals are entirely disabled (even temporarily) it MUST return 0.

`pUSDeVault::maxWithdraw` doesn't account for withdrawal pausing, in violation of EIP-4626 which can break protocols integrating with `pUSDeVault`.

**Proof of Concept:**
```solidity
function test_maxWithdraw_WhenWithdrawalsPaused() external {
    // user1 deposits $1000 USDe into the main vault
    uint256 user1AmountInMainVault = 1000e18;
    USDe.mint(user1, user1AmountInMainVault);

    vm.startPrank(user1);
    USDe.approve(address(pUSDe), user1AmountInMainVault);
    uint256 user1MainVaultShares = pUSDe.deposit(user1AmountInMainVault, user1);
    vm.stopPrank();

    // admin pauses withdrawals
    pUSDe.setWithdrawalsEnabled(false);

    // reverts as maxWithdraw returns user1AmountInMainVault even though
    // attempting to withdraw would revert
    assertEq(pUSDe.maxWithdraw(user1), 0);

    // https://eips.ethereum.org/EIPS/eip-4626 maxWithdraw says:
    // MUST factor in both global and user-specific limits,
    // like if withdrawals are entirely disabled (even temporarily) it MUST return 0
}
```

**Recommended Mitigation:** When withdrawals are paused, `maxWithdraw` should return 0. The override of `maxWithdraw` should likely be done in `PreDepositVault` because there is where the pausing is implemented.

**Strata:** Fixed in commit [8021069](https://github.com/Strata-Money/contracts/commit/80210696f5ebe73ad7fca071c1c1b7d82e2b02ae).

**Cyfrin:** Verified.
