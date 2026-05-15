---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-dolomite-polvaults-v2-0-4-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-dolomite-polvaults-v2-0
title: '`_handleRewards` gas optimisation'
vuln_class: []
---

# `_handleRewards` gas optimisation

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md)_

---

**Description:** `InfraredBGTMetaVault._performDepositRewardByRewardType` is a function that will be called every time rewards are fetched from Infrared vault. The function can be optimized as follows:

- Remove the reward amount > 0 check (as listed in [*Redundant check for non-zero reward amount in `_handleRewards` function*](#redundant-check-for-nonzero-reward-amount-in-handlerewards-function) )
- Cache frequently used functions `DOLOMITE_MARGIN()`, `OWNER()`
- Cache reward token and reward amount at the start of the loop
- Use unchecked integer for incrementing reward counter


**Recommended Mitigation:** Consider using the below optimized version:

```solidity
function _handleRewards(IInfraredVault.UserReward[] memory _rewards) internal {
    IIsolationModeVaultFactory factory = IIsolationModeVaultFactory(VAULT_FACTORY());
    address owner = OWNER();
    IDolomiteMargin dolomiteMargin = DOLOMITE_MARGIN();

    for (uint256 i = 0; i < _rewards.length;) {
        //@audit Removed redundant check since InfraredVault only sends non-zero rewards
        address rewardToken = _rewards[i].token;
        uint256 rewardAmount = _rewards[i].amount;

        if (rewardToken == UNDERLYING_TOKEN()) {
            _setIsDepositSourceThisVault(true);
            factory.depositIntoDolomiteMargin(
                DEFAULT_ACCOUNT_NUMBER,
                rewardAmount
            );
            assert(!isDepositSourceThisVault());
        } else {
        try dolomiteMargin.getMarketIdByTokenAddress(rewardToken) returns (uint256 marketId) {
                        IERC20(rewardToken).safeApprove(address(dolomiteMargin), rewardAmount);
                        try factory.depositOtherTokenIntoDolomiteMarginForVaultOwner(
                            DEFAULT_ACCOUNT_NUMBER,
                            marketId,
                           rewardAmount
                        ) {} catch {
                            IERC20(rewardToken).safeApprove(address(dolomiteMargin), 0);
                            IERC20(rewardToken).safeTransfer(owner, rewardAmount);
                        }
                    } catch {
                        IERC20(rewardToken).safeTransfer(owner,  rewardAmount);
                    }
        }
        unchecked { ++i; }
    }
}
```


**Dolomite:**
No longer applicable. Code changed a good bit because of bricked rewards fix.

**Cyfrin:** Acknowledged.

\clearpage
