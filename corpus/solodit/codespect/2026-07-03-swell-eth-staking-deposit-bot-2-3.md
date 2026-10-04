---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-2-3
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-07-03T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md
tags:
- firm:codespect
- report:2026-07-03-swell-eth-staking-deposit-bot
title: '[L-04] The not_on_beacon gate fails open on an empty, lagging, or hostile
  beacon feed'
vuln_class: []
---

# [L-04] The not_on_beacon gate fails open on an empty, lagging, or hostile beacon feed

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`web3_chain.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_chain.py#L150-L162), [`gates.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/gates.py#L97-L102)

**Description:**

Gate 5 (`not_on_beacon`) is the bot’s primary check that a selected key has not already received a beacon-chain deposit. It is a plain set intersection of the selected pubkeys against a set built from the beacon REST response, where `data.get("data", [])` treats a missing array as empty: [`web3_chain.py:160-162`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_chain.py#L160-L162)

```python
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.load(resp)
# @audit missing/empty data array silently yields empty set; gate fails open
return {v["validator"]["pubkey"].lower() for v in data.get("data", [])}
```

A key absent from that set is treated as not-on-beacon, with no confirmation that the node is synced, canonical, serving a complete response, or even reachable, and the bot uses a single `--beacon` URL with no fallback or health check. So an empty body (`"data":[]`), a partial or MITM-injected response, or an HTTP 200 from a minority fork makes `beacon_known` empty or incomplete, and any selected key absent from it passes regardless of true on-chain state: absence of evidence is treated as evidence of absence. An empty `--beacon ""` value also passes argparse’s `required=True` while being falsy, silently disabling the gate, since `beacon_known` returns an empty set whenever `beacon_url` is falsy.

**Impact:** Standalone, a defense-in-depth weakening (liveness; the degraded-feed case needs no attacker). Its material risk is as an amplifier for the deposit front-run of an aged key: that attack relies on a window during which the attacker’s pre-deposit is not yet visible on the beacon validator set, and an unreliable or operator-controlled feed can extend that window across multiple runs. Low standalone.

**Recommendation:** Absence cannot be the integrity signal, because on a normal batch every selected key is legitimately not yet on beacon (`data == []`), so a naive `"refuse if data == []"` would block every deposit and still fail open on a partial response. Use out-of-band positive confirmation instead:

- Include a sentinel `id=<known-active-validator>` in the same query (the URL builder already joins arbitrary `id=` params) and fail closed if it is absent from `data[]`;

- Query `/eth/v1/node/syncing` and refuse unless `is_syncing == false`;

- Cross-check the beacon head slot against the execution-layer finalized block;

- Consider two independent beacon endpoints and block the run if they disagree;

Also reject an empty or whitespace-only `--beacon` value at startup.

**Status:** Fixed

**Client response:** Update from the client: Addressed in [ede12615](https://github.com/SwellNetwork/eth-staking-deposit-bot/commit/ede12615c831e707413e020ec4dfb340f8637aab). Implemented as recommended: an empty result is trusted only when the node reports synced, its head slot (converted to wall-clock time) is ahead of the EL finalized block, and a configured sentinel validator appears in the response; a transport error, a syncing node, a stale head, or a missing sentinel refuses. A beacon endpoint is now mandatory and an empty `--beacon` is rejected. We did not adopt the remaining "consider" item (two independent beacon endpoints) — a second trusted endpoint adds operational surface for little marginal benefit once freshness is cross-checked.

**CODESPECT fix review:** Fixed. `not_on_beacon` now fails closed unless the feed proves itself (synced, sentinel present, head ahead of EL finality); empty `--beacon` rejected.
