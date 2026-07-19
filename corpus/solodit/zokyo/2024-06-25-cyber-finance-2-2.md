---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-06-25-cyber-finance-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-06-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md
tags:
- firm:zokyo
- report:2024-06-25-cyber-finance
title: Contract Balance Insufficiency Prevents User Withdrawals
vuln_class: []
---

# Contract Balance Insufficiency Prevents User Withdrawals

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-06-25-Cyber Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

The claim function currently restricts withdrawals if the contract's balance of the reward token is less than the user's claimable balance. This may lead to user frustration, as they are unable to withdraw any portion of their claimable assets under these conditions. A scenario where users are unable to claim their rewards due to contract balance constraints undermines user trust and satisfaction.

**Recommendation**: 

To address this issue, modify the claim function to allow users to withdraw whatever portion of their claimable balance is available in the contract. If the contract's balance is less than the user's claimable balance, the function should allow the user to withdraw the available balance and subsequently deduct the withdrawn amount from the user's claimable balance. This ensures that users can at least partially receive their assets and improves user experience by mitigating frustrations related to withdrawal failures.
