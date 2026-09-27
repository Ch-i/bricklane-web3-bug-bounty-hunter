---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-2-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[L-03] The multi-chain solve_withdrawal logic is too tightly coupled'
vuln_class: []
---

# [L-03] The multi-chain solve_withdrawal logic is too tightly coupled

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`boring_vault.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/domain/boring_vault/service/boring_vault.py#L541)

**Description:**

Currently, the multi-chain `solve_withdrawal` logic is too tightly coupled. A single-node failure on any one chain can easily cause the entire task to fail, preventing order fulfillment across all chains.

For example:

- `solve_withdrawal` relies on all oracles and rate providers across all chains functioning correctly, and on prices not being outdated. If the oracle for any asset on any chain fails to meet the required conditions, the task will terminate, preventing order execution on all chains. This is because calculating and update the exchange rate involves calling the oracles and rate providers for all assets across all chains. A single oracle failure can prevent order fulfillment across all chains. For instance, if a `rateProvider` on one chain is unable to provide a valid price due to stale price data from its source, orders on other chains will also fail to be fulfilled.
- During the `solve_atomic_requests` process, when fulfilling orders on each chain, if an RPC exception, network instability, or transaction failure occurs while calling a contract on any chain, the process will immediately terminate instead of skipping and continuing to fulfill orders on the remaining chains. This causes partial execution.

```python
def solve_atomic_requests(
    self, chain_id: str, offer: str, want: str, requests: List[AtomicRequest], rate_by_token: Dict[str, int]
):
    // ...
    want_contract.approve_if_needed(solver_account, vault_config.atomic_solver_v3_address, minimum_assets_out)
    self.atomic_solver_v3.redeem_solve(
        chain_id=chain_id,
        atomic_queue_address=vault_config.atomic_queue_address,
        teller_address=vault_config.teller_address,
        offer=offer,
        want=want,
        users=users,
        minimum_assets_out=minimum_assets_out,
        max_assets=max_assets,
    )
    self.transfer_dust_from_solver_to_vault(chain_id)
```

**Impact:** The strong coupling makes the entire system vulnerable to single points of failure.

**Recommendation:** It is recommended to decouple order fulfillment across different chains, allowing partial fulfillment in some cases. Additionally, providing fallback oracles or alternative pricing methods can help reduce the impact when the primary oracle is down.

**Status:** Fixed

**Client response:** Fixed in [PR-22](https://github.com/SwellNetwork/hlp-internal-be/pull/22).
