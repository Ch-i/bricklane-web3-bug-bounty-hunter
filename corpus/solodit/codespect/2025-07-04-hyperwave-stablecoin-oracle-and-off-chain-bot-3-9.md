---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-9
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
title: '[I-10] update_exchange_rate_all_chains may result in partial exchange rate
  updates'
vuln_class: []
---

# [I-10] update_exchange_rate_all_chains may result in partial exchange rate updates

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`boring_vault.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/cea4d156cafd2d9a5757d21d85aaea1db81479d6/app/domain/boring_vault/service/boring_vault.py#L559)

**Description:**

The `ExchangeRateTask`, which is responsible for updating the on-chain `exchange_rate`, calls the `update_exchange_rate_all_chains` function. This function attempts to update the exchange rate for each chain.

However, if any one of the chains encounters an issue during the process, it will cause the program to throw an exception and stop execution, resulting in only partial exchange rate updates.

For example, if the exchange rates for two chains have already been updated but the third chain’s contract is paused and throws an exception, the task will immediately stop. The exchange rates for the first two chains have been updated, but the remaining chains will not be updated.

```python
def update_exchange_rate_all_chains(self):
    """Update the exchange rate of the vault across all chains."""
    for chain_id, new_rate in self.get_exchange_rate_upper_bound_by_chain().items():
        self.accountant.update_exchange_rate(chain_id, new_rate)

def update_exchange_rate(self, chain_id: str, new_rate: int) -> str:
    # Check current state
    current_state = self.get_accountant_state(chain_id)
    if current_state.is_paused:
        self.telegram_bot.try_send_msg(
            chat_id=base_config.telegram.group_chat_id,
            text=f"Exchange rate update failed on {chain_id}: Accountant is paused.",
        )
        raise ExchangeRateError(f"Accountant is paused on {chain_id}")
    if current_state.last_update_timestamp + current_state.minimum_update_delay_in_seconds > now_seconds():
        logger.info(f"Accountant last update timestamp is too recent on {chain_id}, skipping exchange rate update.")
        self.telegram_bot.try_send_msg(
            chat_id=base_config.telegram.group_chat_id,
            text=f"Exchange rate update skipped on {chain_id}: Last update too recent.",
        )
        raise ExchangeRateError(
            f"Last update timestamp is too recent on {chain_id}, skipping exchange rate update."
        )
    //...
```

**Impact:** This issue has a low impact because `solve_withdrawal_queue_all_chains` currently calls `try_update_exchange_rate_all_chains` to update the exchange rates again. However, if, according to the comments, `solve_withdrawal_queue_all_chains` is designed to terminate upon failure to update the exchange rate, then this issue needs to be taken into consideration.

**Recommendation:** It is recommended not to let the exchange rate update failure of a single chain affect the updates of subsequent chains.

**Status:** Fixed

**Client response:** Fixed in [PR-22](https://github.com/SwellNetwork/hlp-internal-be/pull/22).
