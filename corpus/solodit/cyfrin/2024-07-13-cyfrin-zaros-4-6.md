---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-4-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Cache result of `indexPriceX18.intoSD59x18` in `PerpMarket::getMarkPrice`
vuln_class: []
---

# Cache result of `indexPriceX18.intoSD59x18` in `PerpMarket::getMarkPrice`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Cache result of `indexPriceX18.intoSD59x18` in `PerpMarket::getMarkPrice` instead of re-calculating the same value 4 times.

**Impact:** This stand-alone test shows caching saves 227 gas per execution:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.21;

import {UD60x18} from "@prb/math/src/UD60x18.sol";
import {SD59x18} from "@prb/math/src/SD59x18.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";
import {Test, console} from "forge-std/Test.sol";

interface IMath {
    function calc(UD60x18 indexPriceX18,
                  SD59x18 priceImpactBeforeDelta,
                  SD59x18 priceImpactAfterDelta) external pure
             returns (UD60x18 priceBeforeDelta, UD60x18 priceAfterDelta) ;
}

// each function gets its own contract to avoid gas cost due to
// function selector preferring one over another
contract CacheMath is IMath {
    function calc(UD60x18 indexPriceX18,
                  SD59x18 priceImpactBeforeDelta,
                  SD59x18 priceImpactAfterDelta) external pure
             returns (UD60x18 priceBeforeDelta, UD60x18 priceAfterDelta)  {

        SD59x18 cachedVal = indexPriceX18.intoSD59x18();

        priceBeforeDelta = cachedVal.add(cachedVal.mul(priceImpactBeforeDelta)).intoUD60x18();
        priceAfterDelta  = cachedVal.add(cachedVal.mul(priceImpactAfterDelta)).intoUD60x18();
    }
}

contract NoCacheMath is IMath {
    function calc(UD60x18 indexPriceX18,
                  SD59x18 priceImpactBeforeDelta,
                  SD59x18 priceImpactAfterDelta) external pure
             returns (UD60x18 priceBeforeDelta, UD60x18 priceAfterDelta)  {

        priceBeforeDelta =
            indexPriceX18.intoSD59x18().add(indexPriceX18.intoSD59x18().mul(priceImpactBeforeDelta)).intoUD60x18();
        priceAfterDelta =
            indexPriceX18.intoSD59x18().add(indexPriceX18.intoSD59x18().mul(priceImpactAfterDelta)).intoUD60x18();
    }
}

// run from base directory with:
// forge test --match-contract CacheMathGasTest -vvv
contract CacheMathGasTest is Test {
    GasMeter gasMeter    = new GasMeter();
    IMath    cacheMath   = new CacheMath();
    IMath    noCacheMath = new NoCacheMath();

    uint256 a = 12345667345345564334;
    int256 b  = 3645645897645689746;
    int256 c  = 546546458764565646;

    function test_CacheMathVsNoCacheMath() external {
        UD60x18 a1 = UD60x18.wrap(a);
        SD59x18 b1 = SD59x18.wrap(b);
        SD59x18 c1 = SD59x18.wrap(c);

        // call every function to have gas calculated
        (uint256 cacheMathGas,) = gasMeter.meterCall(
            address(cacheMath),
            abi.encodeWithSelector(IMath.calc.selector, a1, b1, c1)
        );

        (uint256 noCacheMathGas,) = gasMeter.meterCall(
            address(noCacheMath),
            abi.encodeWithSelector(IMath.calc.selector, a1, b1, c1)
        );

        string memory outputStr = string.concat(Strings.toString(cacheMathGas), " ",
                                                Strings.toString(noCacheMathGas));

        // easy spreadsheet input
        console.log(outputStr);
        // cached     = 1886
        // not cached = 2113
        // result: cached version saves 227 gas
    }
}

// taken from https://github.com/orenyomtov/gas-meter/blob/main/test/GasMeter.t.sol
contract GasMeter {
    // output of: huffc --evm-version paris -r src/GasMeter.huff
    bytes internal constant _HUFF_GAS_METER_COMPILED_BYTECODE = (
        hex"5b60003560e01c8063abe770f2146100296101d8015780632b73eefa146100716101d80157600080fd5b36600460003760005131505a6000600060405160606000515afa905a60800190036000523d600060603e6100606101d801573d6060fd5b60406020523d6040523d6060016000f35b36600460003760005131505a600060006040516060346000515af1905a60820190036000523d600060603e6100a96101d801573d6060fd5b60406020523d6040523d6060016000f3"
    );
    uint256 internal constant _HUFF_GAS_METER_COMPILED_BYTECODE_OFFSET = 472;

    function meterStaticCall(
        address /*addr*/,
        bytes memory /*data*/
    ) external view returns (uint256 gasUsed, bytes memory returnData) {
        function() internal pure huffGasMeter;
        assembly {
            huffGasMeter := _HUFF_GAS_METER_COMPILED_BYTECODE_OFFSET
        }
        huffGasMeter();

        // Just to trick the compiler into including the bytecode
        // This code will never be executed, because huffGasMeter() will return or revert
        bytes memory r = _HUFF_GAS_METER_COMPILED_BYTECODE;
        return (r.length, r);
    }

    function meterCall(
        address /*addr*/,
        bytes memory /*data*/
    ) external returns (uint256 gasUsed, bytes memory returnData) {
        function() internal pure huffGasMeter;
        assembly {
            huffGasMeter := _HUFF_GAS_METER_COMPILED_BYTECODE_OFFSET
        }
        huffGasMeter();

        // Just to trick the compiler into including the bytecode
        // This code will never be executed, because huffGasMeter() will return or revert
        bytes memory r = _HUFF_GAS_METER_COMPILED_BYTECODE;
        return (r.length, r);
    }
}
```

**Recommended Mitigation:**
```solidity
SD59x18 cachedVal = indexPriceX18.intoSD59x18();

UD60x18 priceBeforeDelta = cachedVal.add(cachedVal.mul(priceImpactBeforeDelta)).intoUD60x18();
UD60x18 priceAfterDelta  = cachedVal.add(cachedVal.mul(priceImpactAfterDelta)).intoUD60x18();
```

**Zaros:** Fixed in commit [e0396d3](https://github.com/zaros-labs/zaros-core/commit/e0396d35386d00be97b20bb81c7f70c17851e636).

**Cyfrin:** Verified.
