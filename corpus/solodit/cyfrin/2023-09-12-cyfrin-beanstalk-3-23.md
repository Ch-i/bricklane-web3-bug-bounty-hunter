---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-23
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Miscellaneous informational findings regarding Curve-related contracts/libraries
vuln_class: []
---

# Miscellaneous informational findings regarding Curve-related contracts/libraries

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

It is understood that a significant portion of logic related to Curve contracts has been copied from existing implementations, written in Vyper, and ported to Solidity for the purpose of use both within Beanstalk and as an on-chain reference for wider Beanstalk ecosystem contracts. The most pressing issue identified here pertains to the use of unchecked arithmetic. Unlike the Solidity compiler version 0.7.6 utilized by the Beanstalk contracts, the Vyper compiler, utilized by Curve contracts, handles integer overflow checks by default and will revert if one is detected. In other contracts where this functionality is desired, Beanstalk uses the OpenZeppelin SafeMath library; however, this is not the case at all in [`LibCurve`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Curve/LibCurve.sol#L13), [`CurvePrice`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/ecosystem/price/CurvePrice.sol#L17) and [`BeanstalkPrice`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/ecosystem/price/BeanstalkPrice.sol#L7). While we have been unable to identify any specific vulnerabilities (due to the time-constrained nature of this engagement) that may arise as a result, it is recommended to implement these contracts as closely to the existing Vyper implementations as possible, using SafeMath functions rather than unchecked arithmetic operators. `LibBeanMetaCurve` does import the SafeMath library but still contains some [instances](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Curve/LibBeanMetaCurve.sol#L40) of [unchecked arithmetic](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Curve/LibBeanMetaCurve.sol#L58) – if this is intentional, then it should at least be commented as explaining why it is safe to do so; otherwise, the recommendation applies here also.

The following additional informational findings were identified:
* `CurvePrice::getCurveDeltaB` and `LibBeanMetaCurve::getDeltaBWithD` both contain [unsafe](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/ecosystem/price/CurvePrice.sol#L56) [casts](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Curve/LibBeanMetaCurve.sol#L59) from `uint256` to `int256`. While it is unlikely that these will ever cause an issue since the number of beans at peg and the corresponding equilibrium pool BEAN balance are both highly unlikely to exceed the max `int256` value, it is recommended that this be resolved along with the recommendation regarding the use of unchecked arithmetic.
* [Multiplication by one](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Curve/LibCurve.sol#L43) is unnecessary and redundant when calculating the price based on normalized reserves and rates, given that it adds no additional precision and that of the BEAN rate is already sufficient at 30 decimals.
* The [implementation referenced](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Curve/LibCurve.sol#L88) in `LibCurve::getD` uses `255` as the upper bound for the number of Newton-Raphson approximation iterations rather than `256`, as is the case [here](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Curve/LibCurve.sol#L98). In reality, the approximation should converge long before nearing either of these values, so any additional gas usage is unlikely.
* In the event `LibCurve::getD` fails to converge, this function [will revert](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Curve/LibCurve.sol#L110); therefore, the unreachable line of code which [returns zero](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Curve/LibCurve.sol#L111) does not appear to be necessary.
* The NatSpec of `LibCurve::getXP` contains a small [mistake](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Curve/LibCurve.sol#L151):
```diff
    /**
     * @dev Return the `xp` array for two tokens. Adjusts `balances[0]` by `padding`
     * and `balances[1]` by `rate / PRECISION`.
     *
-    * This is provided as a gas optimization when `rates[0] * PRECISION` has been
+    * This is provided as a gas optimization when `rates[0] / PRECISION` has been
     * pre-computed.
     */
```
* The `xp1` variable in [`LibCurveConvert::beansToPeg`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Convert/LibCurveConvert.sol#L24-L35) should be renamed `xp0` to be semantically correct.
* `CurveFacet::is3Pool` should be formatted with the same indentation as other functions – consider running a formatting tool such as `forge fmt`.
* The existing [`token`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/farm/CurveFacet.sol#L244) declaration within `CurveFacet::removeLiquidityImbalance` can be reused when entering the conditional 3Pool/Tri-Crypto block rather than also declaring [`lpToken`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/farm/CurveFacet.sol#L244) which will be assigned the same value.
