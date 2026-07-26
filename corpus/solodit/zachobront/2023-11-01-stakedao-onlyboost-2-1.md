---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-stakedao-onlyboost-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md
tags:
- firm:zachobront
- report:2023-11-01-stakedao-onlyboost
title: '[L-02] Fallback & vault fees must remain at zero for Optimizer to work as
  intended'
vuln_class: []
---

# [L-02] Fallback & vault fees must remain at zero for Optimizer to work as intended

_Section severity (from Solodit section header): Low_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-StakeDAO-Onlyboost.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md)_

---

In the OnlyBoost whitepaper, it's explained that fees on Convex rewards must be set to zero in order to justify the optimizations provided by the protocol.

> As we said earlier, it is a very nice increase but doesn't justify an additional performance fee on top of Convex, that's why it's important that this strategy doesn't charge fees for the share of deposits that go through Convex.

However, the protocol does implement a fee layer on the funds returned by Convex. As we can see in the ConvexImplementation.sol#claim() function:
```solidity
protocolFees = _chargeProtocolFees(rewardTokenAmount);
```
```solidity
/// @notice Internal function to charge protocol fees from `rewardToken` claimed by the locker.
function _chargeProtocolFees(uint256 _amount) internal view returns (uint256 _feeAccrued) {
    if (_amount == 0) return 0;

    uint256 protocolFeesPercent = factory().protocolFeesPercent();
    if (protocolFeesPercent == 0) return 0;

    _feeAccrued = _amount.mulDiv(protocolFeesPercent, DENOMINATOR);
}
```
While these fees are kept separate from the StakeDAO fees (which allows settings to be set in accordance with the whitepaper), it is important that these fees be set to exactly `0` in order for the optimizations performed by the protocol to work as expected.

Note that a similar issue exists with the `withdrawalFee` set on all vaults that use the old implementation. Taking any fees at this layer will take from both Convex and StakeDAO rewards, and will therefore break the intended optimization.

**Recommendation**

Be sure to keep the fees on all Convex fallbacks, as well as all old vaults, set to `0` for the protocol to work as expected.

**Review**

Acknowledged.
