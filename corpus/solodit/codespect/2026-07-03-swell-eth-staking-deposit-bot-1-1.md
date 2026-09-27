---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-1-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-07-03T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md
tags:
- firm:codespect
- report:2026-07-03-swell-eth-staking-deposit-bot
title: '[M-02] Nonce read at latest not pending causes nonce collision on an in-flight
  transaction'
vuln_class: []
---

# [M-02] Nonce read at latest not pending causes nonce collision on an in-flight transaction

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`web3_broadcast.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_broadcast.py#L55-L66)

**Description:**

`Web3Broadcaster.prepare` builds the deposit transaction by hand and reads the signing account’s transaction count to set the nonce, with no `block_identifier`: [`web3_broadcast.py:64`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_broadcast.py#L64)

```python
# @audit no block_identifier defaults to "latest", ignores in-flight mempool tx, causing nonce collision
"nonce": self.w3.eth.get_transaction_count(self.account.address),
```

With no `block_identifier`, the call falls back to web3’s default block `"latest"`, which returns the count of mined transactions only and ignores transactions already signed and sitting in the mempool. If a previous deposit transaction was submitted but not yet mined, the count at `"latest"` is unchanged, so `get_transaction_count` returns the same nonce the in-flight transaction already occupies. The newly signed transaction takes the colliding nonce, and the node either rejects it (`replacement transaction underpriced`) or silently drops it, leaving the operator to manually cancel the original before a re-run can succeed. web3’s own `fill_nonce` reads `"pending"` precisely to include unmined transactions, but the bot hand-builds the transaction dict and never goes through it. The most realistic way to reach the stuck-transaction precondition is the bot’s static EIP-1559 fee cap: a base-fee spike above the fixed `maxFeePerGas` strands the first deposit transaction in the mempool, and the operator’s manual re-run then signs against the stale `"latest"` count and collides. The same condition arises if the signing key is used concurrently from a second process.

**Impact:** Denial of service and operational disruption, no fund loss. Dormant under single-run usage where `latest == pending`; it activates when a prior deposit transaction is stuck in the mempool (the condition the static fee cap creates) or when the signing key is used concurrently. In that state the freshly signed transaction collides on nonce with the in-flight one, and the operator must manually cancel the stuck transaction before re-running. No 32 ETH deposit is misdirected and no funds leave the `DepositManager`; the consequence is a blocked run requiring manual intervention.

**Recommendation:** Read the nonce at `"pending"` so the count includes unmined transactions:

```python
"nonce": self.w3.eth.get_transaction_count(self.account.address, block_identifier="pending"),
```

Pair this with a fee-bump / replacement path for the deposit transaction; the two deficiencies interact (a stuck transaction plus a stale-nonce re-run produces a collision with no automated recovery), and reading the pending nonce is a prerequisite for any EIP-1559 same-nonce replacement. Add a persistent single-run signer lock keyed by (`chain id`, `signer address`, `mode`) so two runs cannot sign concurrently, and refuse to execute if the witness log holds an unresolved `tx.signed` or `tx.in_flight_uncertain` hash not yet confirmed or reverted on chain.

**Status:** Fixed

**Client response:** Addressed in [ede12615](https://github.com/SwellNetwork/eth-staking-deposit-bot/commit/ede12615c831e707413e020ec4dfb340f8637aab). The nonce is read at `pending`, and the send path refuses to run while the signer has an in-flight transaction (`pending > latest`) — the stuck-tx re-run path that produced the collision. That check also covers the suggested refusal over the bot’s own record of signed transactions: reading the chain catches in-flight transactions signed outside this bot too. We did not add the signer lock: the bot is an interactively-confirmed, human-run CLI, so simultaneous runs from one signer are an operational error, and their collision fails clean on the node. We did not add fee-bump/replacement either: the bot sends one transaction and does not manage the mempool, so a stalled tx is an out-of-band operator step (see CODESPECT-10).

**CODESPECT fix review:** Fixed. The send path now aborts when `pending > latest`, so a stuck-tx re-run stops instead of colliding on nonce.
