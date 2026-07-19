---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: No slippage parameter on UniswapV3 swaps can be exploited by MEV to return
  fewer output tokens
vuln_class: []
---

# No slippage parameter on UniswapV3 swaps can be exploited by MEV to return fewer output tokens

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `UniV3Utils::swap` performs a [swap](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/interfaces/exchanges/UniV3Utils.sol#L22) with `amountOutMinimum: 0`. This function is called by `StrategyPassiveManagerUniswap::_chargeFees` [L375](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L375), [L389](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L389) and `BeefyQIVault::_swapRewardsToNative` [L223](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/qidao/BeefyQIVault.sol#L223).

**Impact:** Due to the [lack of slippage parameter](https://dacian.me/defi-slippage-attacks#heading-no-slippage-parameter) an MEV attacker could sandwich attack the swap to return fewer output tokens to the protocol than would otherwise be returned. For `StrategyPassiveManagerUniswap` the reduced output tokens applies to the protocol's fees.

Whether the attack will be profitable or not will depend on the gas cost the attacker has to pay; it may well be that on L2s and Alt-L1s where Beefy intends to deploy, it will be profitable to exploit these swaps with the small pool manipulation `onlyCalmPeriods` may allow because the gas costs are so low.

Combined with a lack of effective deadline timestamp, malicious validators could also hold the swap transaction and execute it at a later time when it would return a reduced token amount than if it had been executed immediately. The `onlyCalmPeriods` check wouldn't appear to provide any protection against this since the swap would still be executed in a calm period, just at a later time when it would return less tokens than the caller expected when they called it.

The previous state could also arise organically due to a sudden and sustained spike in gas costs for example from a popular and prolonged NFT mint; the transaction could be organically delayed and executed at a later time resulting in a worse swap than would have occurred had it been executed when it was supposed to.

**Recommended Mitigation:** A valid slippage parameter [ideally calculated off-chain](https://dacian.me/defi-slippage-attacks#heading-on-chain-slippage-calculation-can-be-manipulated) should be passed to the swap.

**Beefy:**
Acknowledged - known issue. Problem lies in the price being manipulated and then harvest being called would still result in a bad trade even with slippage protections. We harvest frequently to make sure the viability of this attack is mitigated. Also this is only resulting in less fees for the protocol, not the users.

\clearpage
