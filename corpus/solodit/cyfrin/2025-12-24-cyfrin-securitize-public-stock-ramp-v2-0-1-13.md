---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-13
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: '`SecuritizeAmmNavProvider` trades when pool price and anchor price differ
  can leak value'
vuln_class: []
---

# `SecuritizeAmmNavProvider` trades when pool price and anchor price differ can leak value

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** Due to the asymmetric smoothing formula and integer truncation, a BUY followed by an immediate SELL at the same `anchorPriceWad` and `marketStatus = CLOSED_MARKET` can return more quote than initially spent (profitable round-trip), leaking value from the virtual pool.

**Impact:** This can slowly leak value out of the pool if not monitored.

**Proof of Concept:** First [add Foundry to the existing Hardhat](https://getfoundry.sh/config/hardhat/#adding-foundry-to-a-hardhat-project) repo, then create a new file `RoundTripTest.t.sol` inside the `test` folder containing:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Test.sol";
import {SecuritizeAmmNavProvider} from "../contracts/nav/SecuritizeAmmNavProvider.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

contract AssetMock {
    uint8 public decimals = 6;
}

contract RoundTripTest is Test {
    SecuritizeAmmNavProvider public navProvider;
    uint256 constant WAD = 1e18;

    function setUp() public {
        AssetMock asset = new AssetMock();
        SecuritizeAmmNavProvider impl = new SecuritizeAmmNavProvider();

        ERC1967Proxy proxy = new ERC1967Proxy(
            address(impl),
            abi.encodeWithSelector(
                SecuritizeAmmNavProvider.initialize.selector,
                100_000e6,  // baseReserves
                100_000e6,  // quoteReserves
                address(asset)
            )
        );

        navProvider = SecuritizeAmmNavProvider(address(proxy));
        navProvider.grantRole(navProvider.EXECUTOR_ROLE(), address(this));
    }

    function test_roundTrip() public {
        uint256 quoteIn = 10e6;
        uint256 anchorPrice = 1.01e18;
        uint8 closedMarket = navProvider.CLOSED_MARKET();

        (uint256 baseOut,) = navProvider.executeBuyBase(quoteIn, anchorPrice, closedMarket);
        (uint256 quoteBack,) = navProvider.executeSellBase(baseOut, anchorPrice, closedMarket);

        assertLt(quoteBack, quoteIn, "Round-trip should result in loss");
    }
}
```

Then run using: `forge test --match-contract RoundTripTest`.

**Recommended Mitigation:** Consider redesigning the smoothing formula to be symmetric to prevent a slight leak of value.

**Securitize:** Formulas changed in commits [`0b268e8`](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/0b268e8282cfcacf4cbcd32e4b908a87af04b0e8) and [`7d7a4cf`](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/7d7a4cf2de1eaff5633ea9ea2a6c12b9a2f8be3f) which minimizes the round trip issue.

**Cyfrin:** Partly verified. The round trip can still make a profit, however the cost of the round trip (gas and protocol fees) is higher than any profit hence not a viable attack.

\clearpage
