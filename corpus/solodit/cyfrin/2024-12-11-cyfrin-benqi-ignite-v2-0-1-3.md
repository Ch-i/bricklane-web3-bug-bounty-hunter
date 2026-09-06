---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-1-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Redemption of failed registration fees and pre-validated QI is not guaranteed
  to be possible
vuln_class: []
---

# Redemption of failed registration fees and pre-validated QI is not guaranteed to be possible

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** [`Ignite::registerWithStake`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L202) performs a [low-level call](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L215-L216) as part of its validation to ensure the beneficiary,in this case `msg.sender`, can receive `AVAX`:

```solidity
// Verify that the sender can receive AVAX
(bool success, ) = msg.sender.call("");
require(success);
```

However, this is missing from [`Ignite::registerWithAvaxFee`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L251), meaning that failed registration fees are not guaranteed to be redeemable if the sender is a contract that cannot receive `AVAX`.

Similarly, [`Ignite::registerWithPrevalidatedQiStake`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L361) performs no such validation on the beneficiary. While this may not seem to be problematic, since the stake requirement is provided in `QI`, there is a [low-level call](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L477-L478) in [`Ignite::redeemAfterExpiry`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L407) that will attempt a zero-value transfer for pre-validated `QI` stakes:

```solidity
(bool success, ) = msg.sender.call{ value: avaxRedemptionAmount}("");
require(success);
```

If the specified beneficiary is a contract without a payable fallback/receive function then this call will fail. Furthermore, if this beneficiary contract is immutable, the `QI` stake will be locked in the `Ignite` contract unless it is upgraded.

**Impact:** Failed `AVAX` registration fees and prevalidated `QI` stakes will remain locked in the `Ignite` contract.

**Proof of Concept:** The following standalone Forge test demonstrates the behavior described above:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "forge-std/Test.sol";

contract A {}

contract TestPayable is Test {
    address eoa;
    A a;

    function setUp() public {
        eoa = makeAddr("EOA");
        a = new A();
    }

    function test_payable() external {
        // Attempt to call an EOA with zero-value transfer
        (bool success, ) = eoa.call{value: 0 ether}("");

        // Assert that the call succeeded
        assertEq(success, true);

        // Attempt to call a contract that does not have a payable fallback/receive function with zero-value transfer
        (success, ) = address(a).call{value: 0 ether}("");

        // Assert that the call failed
        assertEq(success, false);
    }
}
```

**Recommended Mitigation:** Consider adding validation to `Ignite::registerWithAvaxFee` and `Ignite::registerWithPrevalidatedQiStake`. If performing a low-level call within `Ignite::registerWithPrevalidatedQiStake`, also consider adding the `nonReentrant` modifier.

**BENQI:** Fixed in commit [7d45908](https://github.com/Benqi-fi/ignite-contracts/pull/16/commits/7d45908fce2eefec90e5a67963311b250ae8c748). There will no longer be a native token transfer for pre-validated QI stake registrations since this non-zero check is added before the call in commit [f671224](https://github.com/Benqi-fi/ignite-contracts/blob/f67122426c5dff6023da1ec9602c1959703db28e/src/Ignite.sol#L478-L481).

**Cyfrin:** Verified. The low-level call has been added to `Ignite::registerWithAvaxFee` and pre-validated QI stake registrations no longer have a zero-value call on redemption.
