---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-10
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
title: '[I-11] The on-chain exchange rate update failure will not terminate the WithdrawalSolver
  task'
vuln_class: []
---

# [I-11] The on-chain exchange rate update failure will not terminate the WithdrawalSolver task

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`boring_vault.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/cea4d156cafd2d9a5757d21d85aaea1db81479d6/app/domain/boring_vault/service/boring_vault.py#L568)

**Description:**

When executing the WithdrawalSolver task, it will first attempt to update the on-chain exchange rate. According to the comments, if the on-chain exchange rate update fails, it is expected to throw an error and stop the task.

```python
def solve_withdrawal_queue_all_chains(self):
    """Solve a withdrawal requests."""
    # 1. Update exchange rates for all chains
    # If updaing exchange rate fails, it will raise an exception and stop the process.
    self.try_update_exchange_rate_all_chains()
    // ...
```

However, upon inspecting the `try_update_exchange_rate` function, it can be seen that when an error occurs during the on-chain update, the function simply returns instead of propagating the exception.

```python
def try_update_exchange_rate(self, chain_id: str, new_rate: int) -> str:
    """Try to update the exchange rate, catching any errors."""
    try:
        return self.update_exchange_rate(chain_id, new_rate)
    except Exception:
        return ""
```

**Impact:** The task continues to execute silently even after the on-chain exchange rate update fails, rather than stopping. This does not match the expected behavior.

**Recommendation:** It is recommended that call `update_exchange_rate` function raises an exception instead of `try_update_exchange_rate`. Or modify the comments to match the intended behavior.

**Status:** Fixed

**Client response:** Fixed in [PR-22](https://github.com/SwellNetwork/hlp-internal-be/pull/22).
