---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-stakedao-onlyboost-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md
tags:
- firm:zachobront
- report:2023-11-01-stakedao-onlyboost
title: '[L-04] `_isValidToken()` check should not allow SDT'
vuln_class: []
---

# [L-04] `_isValidToken()` check should not allow SDT

_Section severity (from Solodit section header): Low_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-StakeDAO-Onlyboost.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md)_

---

When a new vault and reward distributor are created using the PoolFactory, we add the reward tokens to the new StakeDAO reard distributor as follows:
1) We manually add CRV and SDT as reward tokens.
2) We iterate through all extra reward tokens from the Curve gauge, and if they pass the `_isValidToken()` check, we add them as reward tokens.

```solidity
if (_isValidToken(_extraRewardToken)) {
    /// Then we add the extra reward token to the reward distributor through the strategy.
    strategy.addRewardToken(_gauge, _extraRewardToken);
}
```

The `_isValidToken()` check returns `false` for CRV, as well as some other situations that should not be allowed:

```solidity
function _isValidToken(address _token) internal view override returns (bool) {
    /// We can't add the reward token as extra reward.
    /// We can't add special pools like the Ve Funder.
    if (_token == rewardToken || _token == VE_FUNDER) return false;

    /// If the token is available as an inflation receiver, it's not valid.
    try GAUGE_CONTROLLER.gauge_types(_token) {
        return false;
    } catch {
        return true;
    }
}
```

However, it will return `true` for `SDT`.

This means, in the event that `SDT` is ever an extra reward token for a Curve gauge, we will attempt to call `strategy.addRewardToken()` with it.

However, since `SDT` has already been added manually to the list, this second attempt to add it will trigger the assertion on the reward distributor that the `distributor` for the given token has not yet been set:
```python
@external
def add_reward(_reward_token: address, _distributor: address):
    """
    @notice Set the active reward contract
    """
    assert msg.sender == self.admin  # dev: only owner

    reward_count: uint256 = self.reward_count
    assert reward_count < MAX_REWARDS
    assert self.reward_data[_reward_token].distributor == ZERO_ADDRESS

    self.reward_data[_reward_token].distributor = _distributor
    self.reward_tokens[reward_count] = _reward_token
    self.reward_count = reward_count + 1
```
This will cause the pool creation to revert, and there will be no way to create a vault for this gauge.

**Proof of Concept**

The following contract can be etched over an existing pool in order to maintain the correct respond to `lp_token()` but return `SDT` as a reward token:
```solidity
contract GaugeWithSDTExtraReward {
    function lp_token() external view returns (address) {
        return 0x845838DF265Dcd2c412A1Dc9e959c7d08537f8a2;
    }

    function reward_tokens(uint i) external view returns (address) {
        if (i == 0) {
            return 0x73968b9a57c6E53d41345FD57a6E6ae27d6CDB2F;
        } else {
            return address(0);
        }
    }
}
```
The trace of the following test will show that the call reverts when `add_reward()` is called for SDT the second time, due to the failure outlined above:
```solidity
function testZach__gauge_with_sdt_fails() public {
    address gauge_to_test = 0x7ca5b0a2910B33e9759DC7dDB0413949071D7575;
    address gauge_with_max = address(new GaugeWithSDTExtraReward());
    vm.etch(gauge_to_test, gauge_with_max.code);
    poolFactory.create(gauge_to_test);
}
```

**Recommendation**

[Note: This recommendation is not finalized. The recommendation below would cause a problem because the distributor would still be set for SDT_DISTRIBUTOR instead of strategy, so the deposits to the reward distributor would fail. Let's discuss if there's a better solution or if we're certain the situation will never happen, and this issue can be removed.]

Ensure that `_isValidToken()` returns false when `SDT` is passed.

```diff
+   address constant SDT = 0x73968b9a57c6E53d41345FD57a6E6ae27d6CDB2F;

    /// @inheritdoc PoolFactory
    function _isValidToken(address _token) internal view override returns (bool) {
        /// We can't add the reward token as extra reward.
+       /// We can't add SDT as extra reward because it's already added
        /// We can't add special pools like the Ve Funder.
-       if (_token == rewardToken || _token == VE_FUNDER) return false;
+       if (_token == rewardToken || _token == SDT || _token == VE_FUNDER) return false;
        ...
```

**Review**

Fixed as recommended in commit [13a244aba97300ef4e707b6401bc4e8124c59048](https://github.com/stake-dao/only-boost/commit/13a244aba97300ef4e707b6401bc4e8124c59048).

Note that, in this fix, gauges that have SDT as a reward token will have the reward distributed by the `SDT_DISTRIBUTOR` instead of the strategy. The StakeDAO team has acknowledged this, and will ensure that if users want to incentivize with SDT, they should do it through StakeDAO.
