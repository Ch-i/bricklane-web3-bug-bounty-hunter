---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-4-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Unnecessary price feed address validation in `Ignite::configurePriceFeed`
vuln_class: []
---

# Unnecessary price feed address validation in `Ignite::configurePriceFeed`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** Unlike [`Ignite::addPaymentToken`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L791), which performs no validation on the price feed address itself, and only the data it returns, [`Ignite::configurePriceFeed`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L838) first [validates](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L844) that the price feed address is not `address(0)`. This is not necessary as the [call](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L856) to `AggregatorV3Interface::latestRoundData` would revert during abi decoding of the return data.

**Proof of Concept:** The following standalone Forge test can be used to demonstrate this:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "forge-std/Test.sol";

contract TestZeroAddressCall is Test {
    function test_zeroAddressCall() external {
        vm.expectRevert(); // see: https://book.getfoundry.sh/cheatcodes/expect-revert#gotcha:~:text=%E2%9A%A0%EF%B8%8F%20Gotcha%3A%20Usage%20with%20low%2Dlevel%20calls
        (bool revertsAsExpected, bytes memory returnData) =
            address(0).call(abi.encodeWithSelector(AggregatorV3Interface.latestRoundData.selector));
        assertFalse(revertsAsExpected); // the call itself does not revert

        vm.expectRevert(); // it's the decode step that reverts
        (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound) =
            abi.decode(returnData, (uint80, int256, uint256, uint256, uint80));
    }
}

interface AggregatorV3Interface {
    function latestRoundData()
        external
        view
        returns (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound);
}

```

**Recommended Mitigation:** Consider removing the validation.

**BENQI:** Fixed in commit [7cbe588](https://github.com/Benqi-fi/ignite-contracts/pull/16/commits/7cbe58883cad6da79831b83fff96c2fefe348cdb).

**Cyfrin:** Verified. Validation has been removed and the corresponding test has been updated.

\clearpage
