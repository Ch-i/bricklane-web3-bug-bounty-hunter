---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-2-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Refactor `InvestorBasedRateLimiter::checkAndUpdateMintLimit` and `checkAndUpdateRedemptionLimit`
  to avoid performing unnecessary operations when creating a new investor
vuln_class: []
---

# Refactor `InvestorBasedRateLimiter::checkAndUpdateMintLimit` and `checkAndUpdateRedemptionLimit` to avoid performing unnecessary operations when creating a new investor

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** When creating a new investor inside `InvestorBasedRateLimiter::checkAndUpdateMintLimit` and `checkAndUpdateRedemptionLimit` there is no need to do a lot of the current processing that occurs after the second `if` statement. A more optimized version could look like this:

```solidity
  function checkAndUpdateMintLimitOptimized(
    address investorAddress,
    uint256 mintAmount
  ) external override onlyRole(CLIENT_ROLE) {
    if (mintAmount == 0) {
      revert InvalidAmount();
    }

    uint256 investorId = addressToInvestorId[investorAddress];

    if (investorId == 0) {
      // @audit GAS - for new investor, revert if `mintAmount > defaultMintLimit`
      // otherwise execute next code then update investorIdToMintState[investorId].currentAmount
      // and slightly change emitted event since prevAmount = 0
      uint256 defaultMintLimitCache = defaultMintLimit;

      if(mintAmount > defaultMintLimitCache) revert RateLimitExceeded();

      // If this is a new investor, initialize their state with the default values
      address[] memory addresses = new address[](1);
      addresses[0] = investorAddress;

      // @audit GAS - return new investorId from `_initializeInvestorState`
      investorId = _initializeInvestorState(
        addresses,
        defaultMintLimit,
        defaultRedemptionLimit,
        defaultMintLimitDuration,
        defaultRedemptionLimitDuration
      );

      // @audit now update current minted amount
      investorIdToMintState[investorId].currentAmount = mintAmount;

      // @audit and alter emitted event to reflect first mint for this new investor
      emit MintStateUpdated(
        investorAddress,
        investorId,
        0,
        mintAmount,
        defaultMintLimitCache - mintAmount
      );
    }
    else {
      // @audit GAS - wrap remaining code in an `else` to only
      // execute if it wasn't a new investor
      RateLimit storage mintState = investorIdToMintState[investorId];

      uint256 prevAmount = mintState.currentAmount;
      _checkAndUpdateRateLimitState(mintState, mintAmount);

      emit MintStateUpdated(
        investorAddress,
        investorId,
        prevAmount,
        mintState.currentAmount,
        mintState.limit - mintState.currentAmount
      );
    }
  }
```
The same optimization could be applied to `checkAndUpdateRedemptionLimit`.

**Ondo:**
Acknowledged.
