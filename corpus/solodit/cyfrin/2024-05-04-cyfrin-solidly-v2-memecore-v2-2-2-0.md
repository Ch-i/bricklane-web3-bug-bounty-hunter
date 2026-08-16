---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-04-cyfrin-solidly-v2-memecore-v2-2-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-05-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md
tags:
- firm:cyfrin
- report:2024-05-04-cyfrin-solidly-v2-memecore-v2-2
title: Flash loans can be taken for free
vuln_class: []
---

# Flash loans can be taken for free

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md)_

---

**Description:** Unlike other AMM implementations, `SolidlyV2Pair` calculates fees independently for each underlying pool token. Showing just the `amount0Out` calculation:
```solidity
if (amount0Out > 0) {
    uint256 amount1In = balance1 - (_reserve1 - amount1Out);
    uint256 fee1 = _updateFees(1, amount1In, _poolFee, _protocolRatio);
    _k(balance0, balance1 - fee1, uint256(_reserve0), uint256(_reserve1));
    _updateReserves(balance0, (balance1 - fee1));
    _emitSwap(0, amount1In, amount0Out, amount1Out, to);
}
```

Since it is only possible to swap a single token, say `token0`, only `token0Out` will be non-zero. Since `amount1Out` is `0` the calculation `uint256 amount1In = balance1 - (_reserve1 - amount1Out);` will yield `amount1In = 0`. Hence, no fee will be charged.

**Impact:** This has a high likelihood, but it is up to the project to determine the impact of being able to take flash swaps for free.

**Proof of Concept:** Add this test to `MultiTest.js`:
```javascript
it("charges no fee for flashloans", async function () {
const { user1, test0, test1, router, pair } = await loadFixture(deploySolidlyV2Fixture);

let token0 = test0;
let token1 = test1;


// Approve tokens for liquidity provision
await token0.connect(user1).approve(router.address, ethers.constants.MaxUint256);
await token1.connect(user1).approve(router.address, ethers.constants.MaxUint256);

// Provide liquidity
await router.connect(user1).addLiquidity(
  token0.address,
  token1.address,
  ethers.utils.parseUnits("100", 18),
  ethers.utils.parseUnits("100", 18),
  0,
  0,
  user1.address,
  ethers.constants.MaxUint256
);

const FlashRecipient = await ethers.getContractFactory("FlashRecipient");
const flashRecipient = await FlashRecipient.deploy(token0.address, pair.address);

// doesn't revert
await flashRecipient.takeFlashloan();
});
```

with this file in `contracts/test/FlashRecipient.sol`:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {SolidlyV2Pair} from "../SolidlyV2Pair.sol";
import {IERC20} from "./IERC20.sol";

contract FlashRecipient {

    IERC20 public token0;
    SolidlyV2Pair public pair;

    constructor(address _token0, address _pair) {
        token0 = IERC20(_token0);
        pair = SolidlyV2Pair(_pair);
    }

    function takeFlashloan() external {
        pair.swap(1e18, 0, address(this), "data");
    }

    function solidlyV2Call(address , uint256 amount0Out, uint256, bytes memory) external returns (bool) {
        // no fee being paid
        token0.transfer(msg.sender, amount0Out);
        return true;
    }
}
```


**Recommended Mitigation:** Calculate the fee for both sides, but only call `_updateFees()` if they have changed.

**Solidly Labs:** Acknowledged. Flashloans are not a big market, especially with memecoins, we see more potential benefits in leaving them free of charge.

**Cyfrin:** Acknowledged.
