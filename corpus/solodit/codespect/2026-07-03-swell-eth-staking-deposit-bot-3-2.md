---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-3-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-07-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md
tags:
- firm:codespect
- report:2026-07-03-swell-eth-staking-deposit-bot
title: '[I-03] Hardcoded fee policy can strand the deposit tx'
vuln_class: []
---

# [I-03] Hardcoded fee policy can strand the deposit tx

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`web3_broadcast.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_broadcast.py#L71)

**Description:**

`prepare(...)` builds and signs the run’s single deposit transaction and sets its EIP-1559 fees with a fixed policy and no bump/replace path:

```python
base = self.w3.eth.gas_price
txn["maxFeePerGas"] = base * 2
txn["maxPriorityFeePerGas"] = min(base, Web3.to_wei(2, "gwei"))
```

Despite the name, `base` is `eth.gas_price` (a suggested all-in gas price, not the EIP-1559 base fee), so `maxFeePerGas` is only 2x the current suggestion and the tip is capped at 2 gwei. These are read at `prepare(...)` time, after the human confirm, so the exposure is the prepare-to-inclusion window: if the base fee climbs past the 2x headroom (it can roughly double in 6 blocks under sustained congestion) or a flat 2 gwei tip is uncompetitive, the tx is underpriced and stalls unmined with no automatic bump. A stalled tx then feeds the in-flight re-run path above.

**Impact:** Liveness only; no fund loss, but the deposit transaction can stall in the mempool with no way to bump or replace it.

**Recommendation:** Make the fee policy configurable (or use a larger/dynamic headroom and a competitive tip), and add a bump-and-replace path for a stuck tx.

**Status:** Fixed

**Client response:** Addressed in [ede12615](https://github.com/SwellNetwork/eth-staking-deposit-bot/commit/ede12615c831e707413e020ec4dfb340f8637aab). Fees are now dynamic EIP-1559 read at send time — `maxFeePerGas = baseFee × headroom + node-suggested tip`, both configurable via CLI/env, with intentionally no hard ceiling (a ceiling would re-introduce exactly the stranding this finding describes). We did not add bump-and-replace: the bot sends one transaction and does not manage the mempool (consistent with CODESPECT-01), so a stalled tx is an out-of-band operator action.

**CODESPECT fix review:** Fixed. Dynamic EIP-1559 (real `baseFee`, configurable headroom and tip, no hard cap) replaces the old `base*2` / 2 gwei-cap that stranded the tx.
