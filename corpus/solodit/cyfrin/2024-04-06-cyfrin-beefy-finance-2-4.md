---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: '`StrategyPassiveManagerUniswap::withdraw` should call `_setTicks` before calling
  `_addLiquidity`'
vuln_class: []
---

# `StrategyPassiveManagerUniswap::withdraw` should call `_setTicks` before calling `_addLiquidity`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** When a withdraw is initiated, `BeefyVaultConcLiq::withdraw` [calls](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L213) `StrategyPassiveManagerUniswap::beforeAction` which removes the liquidity.

In 4 other places when liquidity has been removed, `_setTicks` is always called immediately before calling `_addLiquidity` [[1](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L181-L182), [2](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L315-L316), [3](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L717-L718), [4](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L740-L741)].

This pattern does not occur inside `StrategyPassiveManagerUniswap::withdraw` [L204](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L204) where liquidity gets removed but then `_setTicks` is not called before adding liquidity again.

Consider the following scenario:

1. Beefy sets their LP position based on the current tick
2. Other users transact in the Uniswap pool moving the current liquidity range possibly even outside of Beefy's LP range
3. Someone interacts with Beefy protocol. On almost every interaction Beefy removes their liquidity, gets the current tick and deploys its new liquidity range calculated off the current tick.
4. But on withdrawals Beefy would remove its liquidity but then deploy its new liquidity range using the old stored current tick data since it doesn't fetch the new current tick.

In the above scenario could Beefy deploy its new LP range in an area where it wouldn't get any rewards since the actual current range moved outside it due the activity of other users.

**Impact:** Whenever withdrawals occur the newly added liquidity can be based off a stale current tick. The most likely result of this is reduced liquidity provider rewards due to a non-optimal LP position.

**Recommended Mitigation:** `StrategyPassiveManagerUniswap::withdraw` should call `_setTicks` before calling `_addLiquidity`.

**Beefy:**
We chose to remove the `_onlyCalmPeriods` check from `withdraw` in commit [be0f1ea](https://github.com/beefyfinance/experiments/commit/be0f1eac6944d6f8f73d74a8c3ec80ae3bc3d089) to allow users to withdraw at any time. Hence we don't want withdraw to be able to set ticks so that a malicious actor can't force us to deploy liquidity into an unfavorable range.
