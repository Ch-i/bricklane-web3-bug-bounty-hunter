---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Liquidation fails if the chainId is not configured for `collateralId` or `debtId`
vuln_class: []
---

# Liquidation fails if the chainId is not configured for `collateralId` or `debtId`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Medium

**Status**: Acknowledged

**Description**

In Contract `LiquidationManager.sol`, the method `liquidate(...)` allows a liquidator to liquidate a borrowers’ default loan.

This method has the following check:
```solidity
if (chainId[collateralId] == "" || chainId[debtId] == "")
           revert ChainIdNotConfigured(TAG);
```
This check can prevent liquidations if the `chainId` not set for either `collateralId` or `debtId`. 

For ex. Initially MATIC, FTM, BNB price is 1$ and MATIC’s chainID is set.
User A deposited 10 MATIC 
User A deposited 10 BNB
User B deposited 10 FTM
User A borrowed 5 FTM 

FTM price surges to 3.5$ 

Now User B can liquidate User B for a max amount of ~12$ (as per liquidation percent)
But User B can at max liquidate User A’s MATIC collateral as it’s chainID is set but BNB will be untouched until chainID is set.

**Recommendation**: 

It is to be ensured that chainID is set for borrowers with all collateral IDs.
