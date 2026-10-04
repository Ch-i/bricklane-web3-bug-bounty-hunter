---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-2-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[L-02] Mix of sync/async causes latency in withdrawal processing'
vuln_class: []
---

# [L-02] Mix of sync/async causes latency in withdrawal processing

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`boring_vault.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/domain/boring_vault/service/boring_vault.py#L277)

**Description:**

In the `solve_atomic_requests()` function, the following line is used to send a Telegram alert:

```python
asyncio.run(
    self.telegram_bot.send_msg(
        base_config.telegram.group_chat_id,
        f"Boring Vault {self.boring_vault_address} has not enough balance to solve withdrawal requests for {want_contract.symbol()}: "
        f"Required: {want_contract.from_wei(minimum_assets_out)} {want_contract.symbol()} "
        f"Vault balance: {want_contract.from_wei(boring_vault_balance)} {want_contract.symbol()}",
    )
)
```

This implementation mixes asynchronous and synchronous programming, which introduces several concerns:

- `asyncio.run()` creates a new event loop and blocks the current thread until completion.
- It adds unnecessary overhead just for a single async call.
- If the Telegram API call is slow or fails, it can block or slow down the entire withdrawal request handling.

**Impact:** Potential performance degradation or blocking of the withdrawal processing flow due to external API delays.

**Recommendation:**

- Offload the Telegram call using a background thread or queue-based notification mechanism.
- Alternatively, refactor the logic to be fully synchronous with proper try/except handling to isolate potential Telegram errors from the main logic.

**Status:** Fixed

**Client response:** Fixed in [41378fa9b9fbee9b334ee0e27163e060dfa8f0cb](https://github.com/SwellNetwork/hlp-internal-be/pull/13/commits/41378fa9b9fbee9b334ee0e27163e060dfa8f0cb) by creating new function for sending Telegram message synchronously.
