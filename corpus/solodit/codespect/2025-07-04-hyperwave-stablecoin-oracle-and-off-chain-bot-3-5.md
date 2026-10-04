---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-5
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[I-06] Non-unique addresses may cause balance miscalculation'
vuln_class: []
---

# [I-06] Non-unique addresses may cause balance miscalculation

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`boring_vault.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/domain/boring_vault/service/boring_vault.py)

**Description:**

During the calculation of token balances, the following loops are executed:

```python
# ...
for token_address in base_config.boring_vault.all_token_addresses:
    token_contract = self.token_contract_by_address[token_address]
    balance = token_contract.balance_of(self.boring_vault_address)
    token_balances[token_address] = token_balances.get(token_address, 0) + balance

# Multisig balances on HyperCore
for ms in base_config.boring_vault.multisig_addresses:
    base_token_decimals = self.base_token_contract.decimals()
    # ...
```

The token and multisig addresses are defined in `all_token_addresses` and `multisig_addresses`, respectively—both populated via a configuration file maintained by the protocol team.

Currently, these structures are lists (array type), which may allow accidental duplication of entries. Since each token or multisig address should be processed only once, it would be a best practice to use a set instead. This ensures uniqueness and prevents redundant computation.

**Impact:** If any address is duplicated in the configuration, it may lead to incorrect accounting due to repeated balance aggregation.

**Recommendation:** Change the data structures `all_token_addresses` and `multisig_addresses` from lists to sets to enforce uniqueness automatically.

**Status:** Fixed

**Client response:** Fixed in [d8da0f599a898a4484e22dbb3652f496f671580b](https://github.com/SwellNetwork/hlp-internal-be/pull/13/commits/d8da0f599a898a4484e22dbb3652f496f671580b).
