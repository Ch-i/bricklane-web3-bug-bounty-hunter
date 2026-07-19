---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-2-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Missing sanity value checks in `initPool()` of Core
vuln_class: []
---

# Missing sanity value checks in `initPool()` of Core

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged 

**Description**

There is missing sanity value checks for config parameter in `initPool()`. It is advised to add appropriate require checks such as zero value check for `optimalUtilizationRatio`, etc. 

Failing to do so can lead to division by zero ppanic such as on line: 178. Also the `optimalUtilizationRatio` should never be 1 and it is advised to add a require check for this in `initPool` as well, 
otherwise it can lead to division by zero error again on line: 188. 
The `updateInterestRate` function in the Core contract, along with the `ConfigData` structure, lacks essential validations for various parameters. This absence of validation checks can lead to scenarios where critical financial parameters are set to values that could destabilise the pool's economic model or render it susceptible to manipulation or dysfunctional behaviour.
**Optimal Utilization Ratio**:
- Missing validation for optimalUtilizationRatio in ConfigData could allow it to be set to impractical values, affecting the interest rate calculation.
**Base Interest Rate**:
- Absence of checks on baseRate allows setting unrealistic base rates, potentially leading to either extremely high or low interest rates.
**Loan to Value Ratio**:
- If the Loan to Value (LTV) ratio is set to 0, it could prohibit any borrowing, negating the purpose of the lending pool.
**Liquidation Threshold**:
- Setting the liquidation threshold to 100% could lead to immediate liquidations, posing a risk to borrowers.
**Treasury Percent**:
- Manipulation of treasuryPercent could lead to unfair distribution of liquidation proceeds or fees.
**Liquidity Closing Factor**:
- Without validation, liqClosingFac could be set to values that either make liquidations overly punitive or ineffective.

**Exploit Scenario**:
- An administrator or entity with the INIT_POOL role could set these parameters to extreme values during pool initialization or configuration updates.
- This could lead to a pool that is either too risky or unattractive for lenders and borrowers, disrupt the pool's economic balance, or make the pool vulnerable to economic attacks.

**Recommendation**: 

It is advised to add appropriate sanity value checks for the same.
Note#1: We were already aware of it and  will be checking all the values properly while deploying
