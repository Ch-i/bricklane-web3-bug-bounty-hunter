---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Prevent creating an investor record associated with the zero address
vuln_class: []
---

# Prevent creating an investor record associated with the zero address

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** `InvestorBasedRateLimiter::checkAndUpdateMintLimit` and `checkAndUpdateRedemptionLimit` can create a new investor record and associate it with the zero address.

**Impact:** Investor records can be created which are associated with the zero address. This breaks the following invariant of the `InvestorBasedRateLimiter` contract:

> when a new `investorId` is created, it should be associated with one or more valid addresses

**Proof of Concept:** Add this drop-in PoC to `forge-tests/ousg/InvestorBasedRateLimiter/client.t.sol`:
```solidity
function test_mint_zero_address() public {
    uint256 mintAmount = rateLimiter.defaultMintLimit();
    vm.prank(client);
    rateLimiter.checkAndUpdateMintLimit(address(0), mintAmount);

    // an investor has been created with a 0 address
    assertEq(1, rateLimiter.addressToInvestorId(address(0)));

    // same issue affects checkAndUpdateRedemptionLimit
}
```

Run with: `forge test --match-test test_mint_zero_address`

**Recommended Mitigation:** In `_setAddressToInvestorId` revert for the zero address:
```solidity
function _setAddressToInvestorId(
    address investorAddress,
    uint256 newInvestorId
) internal {
    if(investorAddress == address(0)) revert NoZeroAddress();
```

**Ondo:**
Fixed in commit [bac99d0](https://github.com/ondoprotocol/rwa-internal/commit/bac99d03d75e84ea5541297b3aa0751283c1272e).

**Cyfrin:** Verified.
