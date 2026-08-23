---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-3-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Missing cancellation of withdrawal and redeem requests
vuln_class: []
---

# Missing cancellation of withdrawal and redeem requests

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** The withdrawal process in `BasisTradeVault` is a two-step mechanism. A user first calls `requestWithdraw` or `requestRedeem`, which places their request into a queue and escrows their vault shares within the contract. The second step, `processWithdrawal`, which actually sends the underlying assets to the user, can only be executed by a privileged address with the `AGENT_ROLE`.

This design introduces a significant centralization risk. If the agent(s) become malicious, are compromised, or simply stop performing their duties, they can refuse to call `processWithdrawal`. As a result, all pending withdrawal requests will be stuck in the queue indefinitely.

Users who have requested a withdrawal have their shares locked in the contract and have no way to unilaterally cancel their request to reclaim their shares. This means their funds are effectively frozen, entirely dependent on the liveness and cooperation of the agent.

**Recommended Mitigation:** To mitigate this, a function should be introduced that allows users to cancel their own pending withdrawal requests. This function would return the escrowed shares to the user, effectively un-staking them from the withdrawal queue.

A time-lock could be added to this cancellation function, such that a user can only cancel their request after a certain amount of time has passed since the request was made. This prevents users from spamming the queue while still providing an escape hatch if the agent is unresponsive.

**Button:** Acknowledged, will leave as is. Cancellation is tricky because the vault may have already incurred a cost in an attempt to wind down the basis trade and process the withdrawal. Did not add the ability to modify withdrawals to see real patterns in production for failed requests. In particular, do not think it makes sense to assist a user that is otherwise blacklisted from an ERC20 contract in recovering said assets
