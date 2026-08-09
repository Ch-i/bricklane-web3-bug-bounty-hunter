---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-4-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Fail fast in `BeefyVaultConcLiq:withdraw`
vuln_class: []
---

# Fail fast in `BeefyVaultConcLiq:withdraw`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** In `BeefyVaultConcLiq:withdraw` the `minAmount0` and `minAmount1` [slippage check](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L225) should be before the call to `strategy.withdraw`, because there's no point in doing the additional processing if the function is going to revert. Make it like this:
```solidity
uint256 _amount0 = (_bal0 * _shares) / _totalSupply;
uint256 _amount1 = (_bal1 * _shares) / _totalSupply;

// @audit fail fast
if (_amount0 < _minAmount0 || _amount1 < _minAmount1) revert TooMuchSlippage();

strategy.withdraw(_amount0, _amount1);
```

**Beefy:**
Acknowledged.
