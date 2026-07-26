---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: '`StrategyPassiveManagerUniswap::price` will revert due to overflow for large
  but valid `sqrtPriceX96`'
vuln_class: []
---

# `StrategyPassiveManagerUniswap::price` will revert due to overflow for large but valid `sqrtPriceX96`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** The maximum value of `sqrtPriceX96` is [1461446703485210103287273052203988822378723970342](https://github.com/Uniswap/v3-core/blob/d8b1c635c275d2a9450bd6a78f3fa2484fef73eb/contracts/libraries/TickMath.sol#L16) but `StrategyPassiveManagerUniswap::price` will revert due to overflow for values much lower than this.

**Impact:** Functionality such as deposits which depend on `StrategyPassiveManagerUniswap::price` will revert resulting in denial of service.

**Proof of Concept:** A stand-alone Foundry fuzz test:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.23;

import "../src/FullMath.sol";
import "forge-std/Test.sol";

// run from base project directory with:
// forge test --match-contract PriceTest
contract PriceTest is Test {

    uint256 private constant PRECISION = 1e36;

    function price(uint160 sqrtPriceX96) internal pure returns (uint256 _price) {
        _price = FullMath.mulDiv(uint256(sqrtPriceX96) ** 2, PRECISION, (2 ** 192));
    }

    function test_price(uint160 sqrtPriceX96) external {
        price(sqrtPriceX96);
    }
}
```

Running it shows the overflow:
```solidity
encountered 1 failing test in test/PriceTest.t.sol:PriceTest
[FAIL. Reason: panic: arithmetic underflow or overflow (0x11); counterexample:
calldata=0x4f3b91450000000000000000000000000000000100000000000000000000000000000000
args=[340282366920938463463374607431768211456 [3.402e38]]] test_price(uint160)
(runs: 3, μ: 1319, ~: 1421)
```

**Recommended Mitigation:** Rethink the implementation of `StrategyPassiveManagerUniswap::price`.

**Beefy:**
Fixed in commits [4f061b1](https://github.com/beefyfinance/experiments/commit/4f061b18c0a99392770f68f8c6762fba3c096e97), [1ae1649](https://github.com/beefyfinance/experiments/commit/1ae16493d03417d63010fe034672876b2364c284).

**Cyfrin:** Verified that the function no longer reverts. The fix does introduce a slight precision loss as illustrated by this stand-alone stateless fuzz test:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.23;

import "../src/FullMath.sol";
import {Math} from "openzeppelin-contracts/utils/math/Math.sol";
import "forge-std/Test.sol";

// run from base project directory with:
// forge test --match-contract PriceTest

contract PriceTest is Test {

    uint256 private constant PRECISION = 1e36;

    function price(uint160 sqrtPriceX96) internal pure returns (uint256 _price) {
        _price = FullMath.mulDiv(uint256(sqrtPriceX96) ** 2, PRECISION, (2 ** 192));
    }

    function newPrice(uint160 sqrtPriceX96) internal pure returns (uint256 _price) {
        _price = FullMath.mulDiv(uint256(sqrtPriceX96), Math.sqrt(PRECISION), (2 ** 96)) ** 2;
    }

    function test_price(uint160 sqrtPriceX96) external {
        assertEq(price(sqrtPriceX96), newPrice(sqrtPriceX96));
    }
}
```

which produces the following output:
```
Ran 1 test for test/PriceTest.t.sol:PriceTest
[FAIL. Reason: assertion failed; counterexample: calldata=0x4f3b9145000000000000000000000000000000000000000000000000000000293f884ffb args=[177159557115 [1.771e11]]] test_price(uint160) (runs: 19, μ: 2553, ~: 2553)
Logs:
  Error: a == b not satisfied [uint]
        Left: 5
       Right: 4
```
