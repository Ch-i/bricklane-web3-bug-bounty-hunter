---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-protectorate-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-protectorate
title: '[C-01] If strategy is losing money the last person left to claim from vault
  will handle all losses'
vuln_class: []
---

# [C-01] If strategy is losing money the last person left to claim from vault will handle all losses

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-Protectorate.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md)_

---

**Impact:**
High, as some users will bear substantial value losses

**Likelihood:**
High, as it is possible that strategy is losing money at a given time

**Description**

Currently, the way that `LendingVault` is designed, is that the funds in the vault are transferred out to chosen strategies. Due to the fact that users can still withdraw funds from the vault's balance while some of the funds are lent out to a strategy, the following scenario can happen:

1. Alice deposits 100 ETH to the Vault
2. Bob deposits 100 ETH to the Vault
3. Strategy requests 200 ETH from the Vault - now Vault balance is 0, Strategy balance is 200
4. Chris deposits 100 ETH to the Vault
5. Strategy is not doing good and is left with 100 ETH balance
6. Bob sees this, and withdraws his share, which is 100 ETH
7. Now the strategy is losing but funds are returned back, leaving the Vault with 100 ETH balance and Strategy with 0 balance
8. Now Alice and Chris will bear all of the loss of the strategy, while Bob managed to get 100% of his initial deposit despite of the loss.

**Recommendations**

Possibly forbid withdraws while funds are lent out to a strategy or think of another design for Vault-Strategy lending.
