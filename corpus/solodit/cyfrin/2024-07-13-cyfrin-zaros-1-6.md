---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-1-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Liquidation leaves traders with unhealthier and riskier collateral basket,
  making them more likely to be liquidated in future trades
vuln_class: []
---

# Liquidation leaves traders with unhealthier and riskier collateral basket, making them more likely to be liquidated in future trades

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** The protocol's proposed collateral priority queue with associated Loan-To-Value (LTV) is:
```
1 - USDz   - 1e18 LTV
2 - USDC   - 1e18 LTV
3 - WETH   - 0.8e18 LTV
4 - WBTC   - 0.8e18 LTV
5 - wstETH - 0.7e18 LTV
6 - weETH  - 0.7e18 LTV
```

This means that the protocol will:
* first liquidate the more stable collateral with higher LTV
* only after these have been exhausted will it liquidate the less stable, riskier collaterals with lower LTV

**Impact:** When a trader is liquidated, their resulting collateral basket will contain less stable, more riskier collateral. This makes it more likely they will be liquidated in future trades.

**Recommended Mitigation:** The collateral priority queue should first liquidate riskier, more volatile collateral with lower LTV.

**Zaros:** Fixed in commit [5baa628](https://github.com/zaros-labs/zaros-core/commit/5baa628979d6d33ca042dfca2444c4403393b427).

**Cyfrin:** Verified.
