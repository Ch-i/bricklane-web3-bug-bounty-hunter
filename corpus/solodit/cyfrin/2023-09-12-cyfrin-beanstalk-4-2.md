---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-4-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Avoid using `SafeMath::div` when it is not possible for the divisor to be zero
vuln_class: []
---

# Avoid using `SafeMath::div` when it is not possible for the divisor to be zero

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Use of `SafeMath::div` is only necessary if the divisor can be zero. Therefore, if the divisor cannot be zero then use of this function can be avoided. The following instances have been identified where this is the case:

```solidity
File: /beanstalk/barn/FertilizerFacet.sol

45:        uint128 remaining = uint128(LibFertilizer.remainingRecapitalization().div(1e6)); // remaining <= 77_000_000 so downcasting is safe.

52:        ).div(1e6)); // return value <= amount, so downcasting is safe.
```

```solidity
File: /beanstalk/diamond/PauseFacet.sol

42:        timePassed = (timePassed.div(3600).add(1)).mul(3600);
```

```solidity
File: /beanstalk/field/FieldFacet.sol

344:            LibDibbler.morningTemperature().div(LibDibbler.TEMPERATURE_PRECISION)
```

```solidity
File: /beanstalk/market/MarketFacet/Order.sol

105:        uint256 costInBeans = amount.mul(o.pricePerPod).div(1000000);

197:        beanAmount = beanAmount.div(1000000);
```

```solidity
File: /beanstalk/metadata/MetadataImage.sol

167:        uint256 totalSprouts = uint256(stalkPerBDV).div(STALK_GROWTH).add(16);
168:        uint256 numRows = uint256(totalSprouts).div(4).mod(4);

596:        numStems = uint256(grownStalkPerBDV).div(STALK_GROWTH);
597:        plots = numStems.div(16).add(1);
```

```solidity
File: /beanstalk/silo/SiloFacet/SiloExit.sol

205:        beans = (stalk - accountStalk).div(C.STALK_PER_BEAN); // Note: SafeMath is redundant here.
```

```solidity
File: /beanstalk/sun/SeasonFacet/SeasonFacet.sol

139:        .div(C.BLOCK_LENGTH_SECONDS);
```

```solidity
File: /beanstalk/sun/SeasonFacet/Sun.sol

121:        uint256 maxNewFertilized = amount.div(FERTILIZER_DENOMINATOR);

167:        newHarvestable = amount.div(HARVEST_DENOMINATOR);

227:        uint256 newSoil = newHarvestable.mul(100).div(100 + s.w.t);

229:            newSoil = newSoil.mul(SOIL_COEFFICIENT_HIGH).div(C.PRECISION); // high podrate

231:            newSoil = newSoil.mul(SOIL_COEFFICIENT_LOW).div(C.PRECISION); // low podrate
```

```solidity
File: /ecosystem/price/CurvePrice.sol

47:        rates[0] = rates[0].mul(pool.price).div(1e6);
```

```solidity
File: /libraries/Convert/LibMetaCurveConvert.sol

36:        return balances[1].mul(C.curve3Pool().get_virtual_price()).div(1e30);

86:            dy_0.sub(dy).mul(ADMIN_FEE).div(FEE_DENOMINATOR)
```

```solidity
File: /libraries/Curve/LibBeanMetaCurve.sol

114:        balance0 = xp0.div(RATE_MULTIPLIER);
```

```solidity
File: /libraries/Curve/LibCurve.sol

160:        xp[1] = balances[1].mul(rate).div(PRECISION);

171:        xp[0] = balances[0].mul(rates[0]).div(PRECISION);
172:        xp[1] = balances[1].mul(rates[1]).div(PRECISION);
```

```solidity
File: /libraries/Minting/LibMinting.sol

22:        int256 maxDeltaB = int256(C.bean().totalSupply().div(MAX_DELTA_B_DENOMINATOR));
```

```solidity
File: /libraries/Oracle/LibChainlinkOracle.sol

63:            return uint256(answer).mul(PRECISION).div(10**decimals);
```

```solidity
File: /libraries/Oracle/LibEthUsdOracle.sol

58:            return chainlinkPrice.add(usdcPrice).div(2);

68:                return chainlinkPrice.add(usdtPrice).div(2);

74:                return chainlinkPrice.add(usdcPrice).div(2);
```

```solidity
File: /libraries/Silo/LibLegacyTokenSilo.sol

143:             uint256 removedBDV = amount.mul(crateBDV).div(crateAmount);
```

```solidity
File: /libraries/Silo/LibSilo.sol

493:                   plentyPerRoot.mul(s.a[account].sop.roots).div(
494:                       C.SOP_PRECISION
495:                   )


507:               plentyPerRoot.mul(s.a[account].roots).div(
508:                   C.SOP_PRECISION
509:                )
```

```solidity
File: /libraries/Silo/LibTokenSilo.sol

390:        ).div(1e6); //round here

460:        int96 grownStalkPerBdv = bdv > 0 ? toInt96(grownStalk.div(bdv)) : 0;
```

```solidity
File: /libraries/Silo/LibUnripeSilo.sol

131:            .add(legacyAmount.mul(C.initialRecap()).div(1e18));

201:            .div(C.precision());

246:            .div(1e18);

267:        ).mul(AMOUNT_TO_BDV_BEAN_LUSD).div(C.precision());

288:        ).mul(AMOUNT_TO_BDV_BEAN_3CRV).div(C.precision());
```

```solidity
File: /libraries/Decimal.sol

228:        return self.value.div(BASE);
```

```solidity
File: /libraries/LibFertilizer.sol

80:            newDepositedBeans = newDepositedBeans.mul(percentToFill).div(
81:                C.precision()
82:            );

86:        uint256 newDepositedLPBeans = amount.mul(C.exploitAddLPRatio()).div(
87:            DECIMALS
88:        );

145:            .div(DECIMALS);
```

```solidity
File: /libraries/LibFertilizer.sol

99:            BASE_REWARD + gasCostWei.mul(beanEthPrice).div(1e18), // divide by 1e18 to convert wei to eth

230:        return beans.mul(scaler).div(FRAC_EXP_PRECISION);
```

```solidity
File: /libraries/LibPolynomial.sol

77:                positiveSum = positiveSum.add(pow(x, degree).mul(significands[degree]).div(pow(10, exponents[degree])));

79:                negativeSum = negativeSum.add(pow(x, degree).mul(significands[degree]).div(pow(10, exponents[degree])));

124:                positiveSum = positiveSum.add(pow(end, 1 + degree).mul(significands[degree]).div(pow(10, exponents[degree]).mul(1 + degree)));

126:                positiveSum = positiveSum.sub(pow(start, 1 + degree).mul(significands[degree]).div(pow(10, exponents[degree]).mul(1 + degree)));

128:                negativeSum = negativeSum.add(pow(end, 1 + degree).mul(significands[degree]).div(pow(10, exponents[degree]).mul(1 + degree)));

130:                negativeSum = negativeSum.sub(pow(start, 1 + degree).mul(significands[degree]).div(pow(10, exponents[degree]).mul(1 + degree)));
```
