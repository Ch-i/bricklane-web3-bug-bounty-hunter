---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-3-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-07-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md
tags:
- firm:codespect
- report:2026-07-03-swell-eth-staking-deposit-bot
title: '[I-01] Beacon validator query is an un-chunked GET with no error handling
  and can exceed strict URI limits (HTTP 414)'
vuln_class: []
---

# [I-01] Beacon validator query is an un-chunked GET with no error handling and can exceed strict URI limits (HTTP 414)

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`web3_chain.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_chain.py#L150-L162)

**Description:**

`beacon_known` asks the beacon node which selected pubkeys are already known on the beacon chain (feeding the `not_on_beacon` gate). It concatenates every selected pubkey into one GET query string and issues a single un-chunked request with no error handling: [`web3_chain.py:154-161`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_chain.py#L154-L161)

```python
# @audit all pubkeys in one un-chunked GET, no try/except around the call; a transport error aborts the whole run
q = "&".join(f"id={urllib.parse.quote(pk)}" for pk in pubkeys)
url = f"{self.beacon_url.rstrip('/')}/eth/v1/beacon/states/head/validators?{q}"
```

Two issues. First, there is no `try/except` around the request, so any transport failure (a 414, a 5xx, a dropped connection) propagates out of `build_plan` and aborts the whole run, taking the `not_on_beacon` gate down with it. Second, the query length scales with the batch: each pubkey is 98 characters and contributes `id=` plus the key, so at the default `--cap 64` the request URL is about 6.6 KB. Common beacon-fronting proxies accept that at their defaults (nginx caps the request line at 8 KB; Apache’s `LimitRequestLine` is 8190 B), so it does not fail on a typical deployment. It returns HTTP 414 only on a stricter endpoint (for example an IIS-style front with `maxUrl 4096` / `maxQueryString 2048`) or once the cap is raised past roughly 78 keys, where the URL crosses 8 KB.

**Impact:** Availability and robustness only; no fund loss and no wrong deposit. On the common proxy defaults the default-cap batch is accepted, so this is a hardening item rather than a guaranteed failure. Where it does fire, the cause (URL length, not a beacon-data problem) is not obvious from the raised transport error, and the `not_on_beacon` gate cannot run for that batch. It is not attacker-triggerable and applies to both products, since the beacon read is shared.

**Recommendation:** Use the beacon API’s `POST /eth/v1/beacon/states/state_id/validators` form, which carries the validator IDs in the request body and is the spec’s intended mechanism for large ID lists, avoiding URI limits entirely. Alternatively, chunk the GET into batches of about 20 keys and union the responses. In either case, wrap the call so a transport failure fails the gate closed rather than aborting the whole run.

**Status:** Fixed

**Client response:** Addressed in [ede12615](https://github.com/SwellNetwork/eth-staking-deposit-bot/commit/ede12615c831e707413e020ec4dfb340f8637aab). The validator query now uses the beacon API’s POST form (ids in the body). The error-handling half of this finding is covered by the CODESPECT-03 fix, which fails the beacon read closed on any transport error.

**CODESPECT fix review:** Fixed. Beacon query is now a POST with ids in the body and wrapped to fail closed, so no HTTP 414 and no run-aborting transport error.
