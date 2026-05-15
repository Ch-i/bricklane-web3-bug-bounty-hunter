---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-0-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Repay paused but Liquidation enabled
vuln_class: []
---

# Repay paused but Liquidation enabled

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: High

**Status**: Acknowledged

**Description**

The protocol can enter a state where repay is paused for borrowers but liquidation is open. 
```solidity
 function repayRequest(
       bytes32 id,
       uint256 amount,
       bytes32 route,
       uint256 airdropAmount
   ) external payable nonReentrant {
       if (protocolPause) revert ProtocolPaused(TAG);
       if (repayPause[id]) revert DepositPaused(TAG, id); 
… }
```
Given the volatility of the market, this state will prevent borrowers from repaying their loans leading to the risk of being liquidated. 

If repayment can be paused, liquidation should be paused at the same time as well.

**Recommendation**: 

Please ensure that the protocol does not enter this state. If repayment is paused then liquidation should be paused as well.

**Client commented**: We consider this scenario.
