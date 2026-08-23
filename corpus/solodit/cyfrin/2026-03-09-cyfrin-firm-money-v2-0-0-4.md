---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-09-cyfrin-firm-money-v2-0-0-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-09-cyfrin-firm-money-v2-0
title: Insufficient liquidator incentive on non-ETH branches
vuln_class: []
---

# Insufficient liquidator incentive on non-ETH branches

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-09-cyfrin-firm-money-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md)_

---

**Description:** The collateral gas compensation cap is set to a universal 0.1 ether (0.1e18 token units) for all collateral branches at [Constants.sol:71](https://github.com/firm-money/firm/blob/main/contracts/src/Dependencies/Constants.sol#L71):

```solidity
uint256 constant COLL_GAS_COMPENSATION_CAP = 0.1 ether;
```

This value is applied in [TroveManager.sol:344](https://github.com/firm-money/firm/blob/main/contracts/src/TroveManager.sol#L344):

```solidity
return LiquityMath._min(_coll / COLL_GAS_COMPENSATION_DIVISOR, COLL_GAS_COMPENSATION_CAP);
```

Since each collateral has a vastly different dollar value, 0.1 token units translates to vastly different compensation:

| Collateral | 0.1 tokens | USD value |
|------------|------------|-----------|
| WETH | 0.1 ETH | ~$200 |
| wstETH | 0.1 wstETH | ~$250 |
| rETH | 0.1 rETH | ~$220 |
| sGUSD | 0.1 sGUSD | $0.09997 |
| SNT | 0.1 SNT | $0.001102 |
| LINEA | 0.1 LINEA | $0.0003209 |

The cap is meaningless for non-ETH branches.

**Impact:** Liquidators of `sGUSD`, `SNT`, and `LINEA` troves receive effectively zero compensation even when the SP offset path is used, reducing liquidation incentives on these branches regardless of SP state.

**Recommended Mitigation:** Define a per-branch `COLL_GAS_COMPENSATION_CAP` that reflects each collateral's dollar value, similar to how CCR/MCR/SCR and liquidation penalties are already configured per branch.

**Firm Money:**
Fixed in commit [656ef21](https://github.com/firm-money/firm/tree/656ef21f7f59dc2009f062d5a129432333c2ce38).

**Cyfrin:** Verified. Team has extended the TroveManager to support immutable collateral gas compensation, adjustable per the collateral token.

\clearpage
