---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Wrong `avgDepositPrice` calculated
vuln_class: []
---

# Wrong `avgDepositPrice` calculated

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In Contract VaultETH_V2, the method Request_BuyETH(...) allows users to buy ETH using ZeUSD tokens.

In the method, the epoch’s average deposit price is calculated as follows:
```solidity
tempEpochInfo.avgDepositPrice =
           (tempEpochInfo.rmDeposit *
               tempEpochInfo.avgDepositPrice +
               sendAmt *
               ethPrice) /
           (tempEpochInfo.rmDeposit + sendAmt);

       *// Update the total deposit Ether amount for the epoch*
       tempEpochInfo.rmDeposit += ethAmt;
```
`tempEpochInfo.avgDepositPrice` is the weighted average ETH price when the user calls the "Request_BuyETH" function, but this formula is using ZeUSD tokens amount for calculating the same which is incorrect.

**Recommendation**:  

Update the above formula as follows:
```solidity
tempEpochInfo.avgDepositPrice = (tempEpochInfo.rmDeposit * tempEpochInfo.avgDepositPrice + ethAmt * ethPrice) / (tempEpochInfo.rmDeposit + ethAmt);
```
