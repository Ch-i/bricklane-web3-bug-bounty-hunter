---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-topiastaking-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-TopiaStaking.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-topiastaking
title: '[M-03] Staking won''t work correctly with non-standard ERC20 tokens'
vuln_class: []
---

# [M-03] Staking won't work correctly with non-standard ERC20 tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-TopiaStaking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-TopiaStaking.md)_

---

**Description**

Some tokens do not revert on failure in `transfer` or `transferFrom` but instead return `false` (example is [ZRX](https://etherscan.io/address/0xe41d2489571d322189246dafa5ebde1f4699f498#code)). While such tokens are technically compliant with the standard it is a common issue to forget to check the return value of the `transfer`/`transferFrom` calls. With the current code, if such a call fails but does not revert it can result in users unstaking without claiming their rewards, even though they wanted to. Those rewards will be forever stuck in the contract.

Some tokens also implement a fee-on-transfer mechanism, meaning on `stake`, the actual value transferred to the contract's balance won't be `_lpAmount` but `_lpAmount - fee`. This will be problematic on `unstake` as the last users to call it will get their transactions reverted because of insufficient balance in the contract.

Low decimals tokens won't work with `setRewards`, as the method requires at least 10e18 worth of the reward token as a reward per second, which in the case of just a stable coin would be a crazy daily reward rate, which is close to impossible to fulfill for a prolonged period of time. Using highly valued tokens as ETH or BTC would make it even worse.

While those are expected to not be a problem since the README suggests the staking token will be `TOPIA/ETH` Uniswap V2 LP tokens and the reward token will be `TOPIA`, currently the contract has a mechanism to update both tokens and it opens up the attack vector to use ones that are not compatible with the staking contract.

**Recommendations**

Use OpenZeppelin's `SafeERC20` library and its `safe` methods for ERC20 transfers. For fee-on-transfer tokens, check the balance before and after the deposit (`stake`) and use the difference between the two as the actual transferred value. Consider allowing a lower rewards rate in `setRewards`.

Or you can just remove the `setRewardsToken` and `setUniswapPair` methods.

**Discussion**

**pashov:** Fixed.
