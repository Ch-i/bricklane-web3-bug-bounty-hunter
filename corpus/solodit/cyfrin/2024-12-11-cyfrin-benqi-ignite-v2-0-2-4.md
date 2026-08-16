---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Lack of user-defined slippage and deadline parameters in `StakingContract::swapForQI`
  may result in unfavorable `QI` token swaps
vuln_class: []
---

# Lack of user-defined slippage and deadline parameters in `StakingContract::swapForQI` may result in unfavorable `QI` token swaps

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** When a user interacts with `StakingContract` to provision a hosted node, they can choose between two methods:[`StakingContract::stakeWithAVAX`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L457-L511) or [`StakingContract::stakeWithERC20`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L513-L577). If the staked token is not `QI`, `StakingContract::swapForQI` is invoked to swap the staked token for `QI` via Trader Joe. Once created, the validator node is then [registered](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L441-448) with [`Ignite`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L353-L400), using `QI`, via `StakingContract::registerNode`.

Within the swap to `QI`, `amountOutMin` is [calculated](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L844) using Chainlink price data and a slippage parameter defined by the protocol:

```solidity
// Get the best price quote
uint256 slippageFactor = 100 - slippage; // Convert slippage percentage to factor
uint256 amountOutMin = (expectedQiAmount * slippageFactor) / 100; // Apply slippage
```

If the actual amount of `QI` received is below this `amountOutMin`, the transaction will [revert](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L897-L900); however, users are restricted by the protocol-defined slippage, which may not reflect their preferences if they desire a smaller slippage tolerance to ensure they receive a more favorable swap execution.

Additionally, the swap [deadline](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L863) specified as `block.timestamp` in `StakingContract::swapForQI` provides no protection as deadline validation will pass whenever the transaction is included in a block:

```solidity
uint256 deadline = block.timestamp;
```

This could expose users to unfavorable price fluctuations and again offers no option for users to provide their own deadline parameter.

**Impact:** Users may receive fewer `QI` tokens than expected due to the fixed slippage tolerance set by the protocol, potentially resulting in unfavorable swap outcomes.

**Recommended Mitigation:** Consider allowing users to provide a `minAmountOut` slippage parameter and a `deadline` parameter for the swap operation. The user-specified `minAmountOut` should override the protocol's slippage-adjusted amount if larger.

**BENQI:** Acknowledged, there is already a slippage check inside `StakingContract::swapForQI` based on the Chainlink pricing.

**Cyfrin:** Acknowledged.

\clearpage
