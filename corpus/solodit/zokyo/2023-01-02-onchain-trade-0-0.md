---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: User’s fund can be transferred out without consent
vuln_class: []
---

# User’s fund can be transferred out without consent

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Critical

**Status**: Resolved

**Description**


In contract Swap, the function settleFutureProfit(address token, uint256 amount, address from) can transfer funds from any user to itself. Anyone can call settleFutureProfit(...) with address of any other user who has approved the spender as Swapl and the tokens can be moved without the consent of the user. A bot can also monitor the approvals on public networks/mem pools and call settleFutureProfit(...) leading to the draining of user funds.  Also, the user does not get any liquidity token in return, making the tokens immovable from the contract. 

Step 1: List token in Swap.sol
Step 2: User approves Swap.sol to spend tokens
Step 3: Anyone can call settleFutureProfit(token, amount, address_from_step_2) and transfer tokens of the address from step 2 to Swap.sol.


**Recommendation**: 

Fix the logic in the contract so that no user can transfer tokens of another address and provide liquidity tokens in case the user transfers their own tokens so that tokens can be retrieved.
