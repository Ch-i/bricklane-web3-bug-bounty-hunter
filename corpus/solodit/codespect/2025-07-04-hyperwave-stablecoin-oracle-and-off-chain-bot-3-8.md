---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-8
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
title: '[I-09] Some calls within the WithdrawalSolver task lack a retry mechanism'
vuln_class: []
---

# [I-09] Some calls within the WithdrawalSolver task lack a retry mechanism

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`boring_vault.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/cea4d156cafd2d9a5757d21d85aaea1db81479d6/app/domain/boring_vault/service/boring_vault.py#L576)

**Description:**

The WithdrawalSolver task involves many operations that rely on on-chain data retrieval and calls via underlying RPC, as well as database connections. If these operations temporarily fail due to transient network instability or other issues, the program often throws exceptions directly without an appropriate retry mechanism with backoff delay. This will cause the WithdrawalSolver task to terminate immediately.

For example, in the `approve_if_needed` function, it attempts to send the transaction only once, and if it fails, it directly raises an exception without retrying.

```python
def approve_if_needed(self, owner: LocalAccount, spender: str, amount: int) -> Optional[str]:
    // ...
    signed_tx = self.w3.eth.account.sign_transaction(tx, owner.key)
    tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    tx_hash_str = add_0x_prefix(tx_hash.hex())
    logger.info(f"Transaction sent: {tx_hash_str}")

    # Wait for transaction receipt (success)
    receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
    logger.debug(f"Transaction mined: {receipt}")
    ...
```

**Impact:** The WithdrawalSolver task has a relatively long scheduling interval—approximately one hour. As a result, if the task execution fails due to transient instability, it may lead to withdrawal delays and increase the processing load during the next execution.

**Recommendation:** It is recommended to implement an appropriate delayed retry mechanism for failures in database and on-chain RPC calls.

**Status:** Fixed

**Client response:** Fixed in [PR-22](https://github.com/SwellNetwork/hlp-internal-be/pull/22) by adding auto retry to Celery tasks.
