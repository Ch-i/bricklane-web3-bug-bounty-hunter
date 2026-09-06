---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-M-1 small LP providers may be unable to withdraw their deposits
vuln_class: []
---

# TRST-M-1 small LP providers may be unable to withdraw their deposits

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
In LiquidityPool’s initiateWithdraw(), it’s required that withdrawn value is above a minimum 
parameter, or that withdrawn tokens is above the minimum parameter.
```solidity 
      if (withdrawalValue < lpParams.minDepositWithdraw && 
          amountLiquidityToken < lpParams.minDepositWithdraw) {
      revert MinimumWithdrawNotMet(address(this), withdrawalValue, lpParams.minDepositWithdraw);
      }
```
The issue is that **minDepositWithdraw** is measured in dollars while **amountLiquidityToken** is 
LP tokens. The intention was that if LP tokens lost value and a previous deposit is now worth 
less than **minDepositWithdraw**, it would still be withdrawable. However, the current 
implementation doesn’t check for that correctly, since the LP to dollar exchange rate at 
deposit time is not known, and is practically being hardcoded as 1:1 here. The impact is that 
users may not be able to withdraw LP with the token amount that was above the minimum at 
deposit time, or vice versa

**Recommended Mitigation:**
Consider calculating an average exchange rate at which users have minted and use it to verify 
withdrawal amount is satisfactory.

**Team Response:**
While valid, the proposed solution adds far more complexity to the system than the benefit it 
would provide. Small (<$1) LPs will need to find an alternative place to liquidate their holdings 
like a uniswap pool. This will not be resolved at the protocol level.
As keepers process deposits and withdrawals, the minimums are necessary to prevent 
unwanted spam.
