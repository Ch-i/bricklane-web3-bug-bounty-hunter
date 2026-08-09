---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-0-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Prevent creating an investor record associated with no address
vuln_class: []
---

# Prevent creating an investor record associated with no address

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** `InvestorBasedRateLimiter::initializeInvestorStateDefault` is supposed to associate a newly created investor with one or more addresses but the `for` [loop](https://github.com/ondoprotocol/rwa-internal/blob/6747ebada1c867a668a8da917aaaa7a0639a5b7a/contracts/ousg/InvestorBasedRateLimiter.sol#L253-L260) which does this can be bypassed by calling the function with an empty array:
```solidity
function initializeInvestorStateDefault(
    address[] memory addresses
    ) external onlyRole(CONFIGURER_ROLE) {
    _initializeInvestorState(
      addresses,
      defaultMintLimit,
      defaultRedemptionLimit,
      defaultMintLimitDuration,
      defaultRedemptionLimitDuration
    );
}

function _initializeInvestorState(
    address[] memory addresses,
    uint256 mintLimit,
    uint256 redemptionLimit,
    uint256 mintLimitDuration,
    uint256 redemptionLimitDuration
    ) internal {
    uint256 investorId = ++investorIdCounter;

    // @audit this `for` loop can by bypassed by calling
    // `initializeInvestorStateDefault` with an empty array
    for (uint256 i = 0; i < addresses.length; ++i) {
      // Safety check to ensure the address is not already associated with an investor
      // before associating it with a new investor
      if (addressToInvestorId[addresses[i]] != 0) {
        revert AddressAlreadyAssociated();
      }
      _setAddressToInvestorId(addresses[i], investorId);
    }

    investorIdToMintState[investorId] = RateLimit({
      currentAmount: 0,
      limit: mintLimit,
      lastResetTime: block.timestamp,
      limitDuration: mintLimitDuration
    });
    investorIdToRedemptionState[investorId] = RateLimit({
      currentAmount: 0,
      limit: redemptionLimit,
      lastResetTime: block.timestamp,
      limitDuration: redemptionLimitDuration
    });
}
```

**Impact:** An investor record can be created without any associated address. This breaks the following invariant of the `InvestorBasedRateLimiter` contract:

> when a new `investorId` is created, it should be associated with one or more valid addresses

**Proof of Concept:** Add this drop-in PoC to `forge-tests/ousg/InvestorBasedRateLimiter/setters.t.sol`:
```solidity
function test_initializeInvestor_NoAddress() public {
    // no investor created
    assertEq(0, rateLimiter.investorIdCounter());

    // empty input array will bypass the `for` loop that is supposed
    // to associate addresses to the newly created investor
    address[] memory addresses;

    vm.prank(guardian);
    rateLimiter.initializeInvestorStateDefault(addresses);

    // one investor created
    assertEq(1, rateLimiter.investorIdCounter());

    // not associated with any addresses
    assertEq(0, rateLimiter.investorAddressCount(1));
}
```

Run with: `forge test --match-test test_initializeInvestor_NoAddress`

**Recommended Mitigation:** In `_initializeInvestorState` revert if the input address array is empty:
```solidity
uint256 addressesLength = addresses.length;

if(addressesLength == 0) revert EmptyAddressArray();
```

**Ondo:**
Fixed in commit [bac99d0](https://github.com/ondoprotocol/rwa-internal/commit/bac99d03d75e84ea5541297b3aa0751283c1272e).

**Cyfrin:** Verified.
