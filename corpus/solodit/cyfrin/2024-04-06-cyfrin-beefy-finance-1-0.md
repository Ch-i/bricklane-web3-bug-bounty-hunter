---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: '`block.timestamp` used as swap deadline offers no protection'
vuln_class: []
---

# `block.timestamp` used as swap deadline offers no protection

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `UniV3Utils::swap` performs a [swap](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/interfaces/exchanges/UniV3Utils.sol#L20) with `deadline: block.timestamp`. This function is called by `StrategyPassiveManagerUniswap::_chargeFees` [L375](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L375), [L389](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L389) and `BeefyQIVault::_swapRewardsToNative` [L223](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/qidao/BeefyQIVault.sol#L223).

**Impact:** The block the transaction is eventually put into will be `block.timestamp` so this [offers no protection](https://dacian.me/defi-slippage-attacks#heading-no-expiration-deadline).

**Recommended Mitigation:** Caller should pass in a desired deadline which should be passed to the swap as the deadline parameter.

**Beefy:**
Acknowledged - known issue.
