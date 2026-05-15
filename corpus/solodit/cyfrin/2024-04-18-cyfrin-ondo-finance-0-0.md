---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: '`InvestorBasedRateLimiter::setInvestorMintLimit` and `setInvestorRedemptionLimit`
  can make subsequent calls to `checkAndUpdateMintLimit` and `checkAndUpdateRedemptionLimit`
  revert due to underflow'
vuln_class: []
---

# `InvestorBasedRateLimiter::setInvestorMintLimit` and `setInvestorRedemptionLimit` can make subsequent calls to `checkAndUpdateMintLimit` and `checkAndUpdateRedemptionLimit` revert due to underflow

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** `InvestorBasedRateLimiter::_checkAndUpdateRateLimitState` [L211-213](https://github.com/ondoprotocol/rwa-internal/blob/6747ebada1c867a668a8da917aaaa7a0639a5b7a/contracts/ousg/InvestorBasedRateLimiter.sol#L211-L213) subtracts the current mint/redemption amount from the corresponding limit:
```solidity
if (amount > rateLimit.limit - rateLimit.currentAmount) {
  revert RateLimitExceeded();
}
```

If `setInvestorMintLimit` or `setInvestorRedemptionLimit` are used to set the limit amount for minting or redemptions smaller than the current mint/redemption amount, calls to this function will revert due to underflow.

**Impact:** `InvestorBasedRateLimiter::setInvestorMintLimit` and `setInvestorRedemptionLimit` can make subsequent calls to `checkAndUpdateMintLimit` and `checkAndUpdateRedemptionLimit` revert due to underflow.

**Proof of Concept:** Add this drop-in PoC to `forge-tests/ousg/InvestorBasedRateLimiter/setters.t.sol`:
```solidity
function test_setInvestorMintLimit_underflow_DoS() public initDefault(alice) {
    // first perform a mint
    uint256 mintAmount = rateLimiter.defaultMintLimit();
    vm.prank(client);
    rateLimiter.checkAndUpdateMintLimit(alice, mintAmount);

    // admin now reduces the mint limit to be under the current
    // minted amount
    uint256 aliceInvestorId = 1;
    uint256 newMintLimit = mintAmount - 1;
    vm.prank(guardian);
    rateLimiter.setInvestorMintLimit(aliceInvestorId, newMintLimit);

    // subsequent calls to `checkAndUpdateMintLimit` revert due to underflow
    vm.prank(client);
    rateLimiter.checkAndUpdateMintLimit(alice, 1);

    // same issue affects `setInvestorRedemptionLimit`
}
```

Run with: `forge test --match-test test_setInvestorMintLimit_underflow_DoS`

Produces output:
```
Ran 1 test for forge-tests/ousg/InvestorBasedRateLimiter/setters.t.sol:Test_InvestorBasedRateLimiter_setters_ETH
[FAIL. Reason: panic: arithmetic underflow or overflow (0x11)] test_setInvestorMintLimit_underflow_DoS() (gas: 264384)
Suite result: FAILED. 0 passed; 1 failed; 0 skipped; finished in 1.09ms (116.74µs CPU time)
```

**Recommended Mitigation:** Explicitly handle the case where the limit is smaller than the current mint/redemption amount:
```solidity
if (rateLimit.limit <= rateLimit.currentAmount || amount > rateLimit.limit - rateLimit.currentAmount) {
  revert RateLimitExceeded();
}
```

**Ondo:**
Fixed in commit [fb8ecff](https://github.com/ondoprotocol/rwa-internal/commit/fb8ecff80960c8c891ddc206c6f6f27a620e42d6).

**Cyfrin:** Verified.
