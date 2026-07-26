---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Using `pool.slot0` can be easily manipulated
vuln_class: []
---

# Using `pool.slot0` can be easily manipulated

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `StrategyPassiveManagerUniswap::sqrtPrice` gets the current tick and the current price [using](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L544) `pool.slot0`.

This price is used in a number of functions such as `_addLiquidity` [L217](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L217), `_checkAmounts` [L283](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L283), `balancesOfPool` [L452](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L452), `_setAltTick` [L601](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L601) and `price` [L535](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L535) and in `BeefyVaultConcLiq::previewDeposit` [L117](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L117) and `deposit` [L170](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L170) while the current tick is used to calculate the LP range.

`pool.slot0` can be [easily manipulated](https://solodit.xyz/issues/h-10-ichilporacle-is-extemely-easy-to-manipulate-due-to-how-ichivault-calculates-underlying-token-balances-sherlock-blueberry-blueberry-git) via flash loans to return arbitrary value price and tick values. In Beefy's case this can allow an attacker to force the protocol to deploy its liquidity into an unfavorable range.

Beefy is aware of this risk and has implemented an [`_onlyCalmPeriods`](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L96-L102) function that prevents many functions from working if the pool has been abruptly manipulated. However as our Critical finding has shown, any asymmetry in the implementation of `_onlyCalmPeriods` can lead to the protocol being drained.

Hence we note the use of `pool.slot0` as a risk for this codebase as it continues to evolve, especially around functions that set the LP range from the current tick and deploy the protocol's liquidity.

**Beefy:**
Acknowledged.
