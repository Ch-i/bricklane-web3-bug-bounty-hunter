---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-10
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Precision loss in `swETH::_deposit` from unnecessary hidden division before
  multiplication
vuln_class: []
---

# Precision loss in `swETH::_deposit` from unnecessary hidden division before multiplication

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** `swETH::_deposit` [L170](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L170) contains a hidden unnecessary [division before multiplication](https://dacian.me/precision-loss-errors#heading-division-before-multiplication) as the call to `_ethToSwETHRate` performs a division which then gets multiplied by `msg.value`:
```solidity
uint256 swETHAmount = wrap(msg.value).mul(_ethToSwETHRate()).unwrap();
// @audit expanding this out
// wrap(msg.value).mul(_ethToSwETHRate()).unwrap();
// wrap(msg.value).mul(wrap(1 ether).div(_swETHToETHRate())).unwrap();
```

This issue has not been introduced in the new changes but is in the mainnet [code](https://github.com/SwellNetwork/v3-core-public/blob/master/contracts/lst/contracts/implementations/swETH.sol#L170).

**Impact:** Slightly less `swETH` will be minted to depositors. While the amount by which individual depositors are short-changed is individually small, the effect is cumulative and increases as depositors and deposit size increase.

**Proof of Concept:** This stand-alone stateless fuzz test can be run inside Foundry to prove this as well as provided hard-coded test cases:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {UD60x18, wrap} from "@prb/math/src/UD60x18.sol";

import "forge-std/Test.sol";

// run from base project directory with:
// (fuzz test) forge test --match-test FuzzMint -vvv
// (hardcoded) forge test --match-test HardcodedMint -vvv
contract MintTest is Test {

    uint256 private constant SWETH_ETH_RATE = 1050754209601187151; //as of 2024-02-15

    function _mintOriginal(uint256 inputAmount) private pure returns(uint256) {
        // hidden division before multiplication
        // wrap(inputAmount).mul(_ethToSwETHRate()).unwrap();
        // wrap(inputAmount).mul(wrap(1 ether).div(_swETHToETHRate())).unwrap()

        return wrap(inputAmount).mul(wrap(1 ether).div(wrap(SWETH_ETH_RATE))).unwrap();
    }

    function _mintFixed(uint256 inputAmount) private pure returns(uint256) {
        // refactor to perform multiplication before division
        // wrap(inputAmount).mul(wrap(1 ether)).div(_swETHToETHRate()).unwrap();

        return wrap(inputAmount).mul(wrap(1 ether)).div(wrap(SWETH_ETH_RATE)).unwrap();
    }

    function test_FuzzMint(uint256 inputAmount) public pure {
        uint256 resultOriginal = _mintOriginal(inputAmount);
        uint256 resultFixed    = _mintFixed(inputAmount);

        assert(resultOriginal == resultFixed);
    }

    function test_HardcodedMint() public {
        // found by fuzzer
        console.log(_mintFixed(3656923177187149889) - _mintOriginal(3656923177187149889)); // 1

        // 100 eth
        console.log(_mintFixed(100 ether) - _mintOriginal(100 ether)); // 21

        // 1000 eth
        console.log(_mintFixed(1000 ether) - _mintOriginal(1000 ether)); // 215

        // 10000 eth
        console.log(_mintFixed(10000 ether) - _mintOriginal(10000 ether)); // 2159
    }
}
```

**Recommended Mitigation:** Refactor to perform multiplication before division:
```solidity
uint256 swETHAmount = wrap(msg.value).mul(wrap(1 ether)).div(_swETHToETHRate()).unwrap();
```

**Swell:** Fixed in commit [cb093ea](https://github.com/SwellNetwork/v3-contracts-lst/commit/cb093eac675e5248a3f736a01a3725d794dd177e).

**Cyfrin:**
Verified.

\clearpage
