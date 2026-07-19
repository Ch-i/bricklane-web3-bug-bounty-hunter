---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Owner of `StrategyPassiveManagerUniswap` can rug-pull users' deposited tokens
  by manipulating `onlyCalmPeriods` parameters
vuln_class: []
---

# Owner of `StrategyPassiveManagerUniswap` can rug-pull users' deposited tokens by manipulating `onlyCalmPeriods` parameters

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** While `StrategyPassiveManagerUniswap` does have some permissioned roles, one of the attack paths we were asked to check was that the permissioned roles could not rug-pull the users' deposited tokens. There is a way that the owner of the `StrategyPassiveManagerUniswap` contract could accomplish this by modifying key parameters to reduce the effectiveness of the `_onlyCalmPeriods` check. This appears to be how a similar protocol Gamma was [exploited](https://rekt.news/gamma-strategies-rekt/).

**Proof of Concept:**
1. Owner calls `StrategyPassiveManagerUniswap::setDeviation` to increase the maximum allowed deviations to large numbers or alternatively `setTwapInterval` to decrease the twap interval rendering it ineffective
2. Owner takes a flash loan and uses it to manipulate `pool.slot0` to a high value
3. Owner calls `BeefyVaultConcLiq::deposit` to perform a deposit; the shares are calculated thus:
```solidity
// @audit `price` is derived from `pool.slot0`
shares = _amount1 + (_amount0 * price / PRECISION);
```
4. As `price` is derived from `pool.slot0` which has been inflated, the owner will receive many more shares than they normally would
5. Owner unwinds the flash loan returning `pool.slot0` back to its normal value
6. Owner calls `BeefyVaultConcLiq::withdraw` to receive many more tokens than they should be able to due to the inflated share count they received from the deposit

**Impact:** Owner of `StrategyPassiveManagerUniswap` can rug-pull users' deposited tokens.

**Recommended Mitigation:** Beefy already intends to have all owner functions behind a timelocked multi-sig and if these transactions are attempted the suspicious parameters would be an obvious signal that a future attack is coming. Because of this the probability of this attack being effectively executed is low though it is still possible.

One way to further mitigate this attack would be to have a minimum required twap interval and maximum required deviation amounts such that the owner couldn't change these parameters to values which would enable this attack.

**Beefy:**
Fixed in commit [b5769c4](https://github.com/beefyfinance/experiments/commit/b5769c4ccad6357ac9d3de2c682749bbaeeae6d1).

**Cyfrin:** Verified.
