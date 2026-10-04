---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-2-4
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
title: '[L-05] verify_deposit(...) crashes instead of returning False on malformed-hex
  input'
vuln_class: []
---

# [L-05] verify_deposit(...) crashes instead of returning False on malformed-hex input

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`bls.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/bls.py#L81)

**Description:**

`verify_deposit(...)` is the bot’s signature check on data from an untrusted RPC, and its docstring promises a fail-closed contract: malformed input returns `False`, never raises. It honours that for a wrong byte length (the `if len(...)` guard) and a malformed curve point (caught by `try/except ValueError`), but not for malformed hex, because the hex decode runs before the try:

```python
pk, wc, sig = _b(pubkey), _b(withdrawal_credentials), _b(signature) # outside the try
if len(pk) != 48 or len(wc) != 32 or len(sig) != 96:
    return False
# ...
try:
    return bool(PopSchemeMPL.verify(...))
except ValueError:
    return False
```

`_b(...)` calls `bytes.fromhex(...)`, which raises `ValueError` on an odd-length or non-hex string, so such input escapes `verify_deposit(...)` and crashes the run instead of returning `False`. This is fail-safe (a crash never returns a wrong `True`) and is not reachable through the normal pipeline (web3’s `_hex(...)` always emits even-length `0x...`); the issue is the violation of the documented "never raises" contract.

**Impact:** Fail-closed-by-crash: no wrong verification and no fund risk, but malformed input aborts the run with an uncaught exception instead of the documented `False`.

**Recommendation:** Move the `_b(...)` parsing inside the try (or wrap parse, length-check, and verify in one `try/except ValueError`) so every malformed input returns `False`.

**Status:** Fixed

**Client response:** Addressed in [ede12615](https://github.com/SwellNetwork/eth-staking-deposit-bot/commit/ede12615c831e707413e020ec4dfb340f8637aab). The hex parse moved inside the try, so malformed input returns `False` per the documented contract.

**CODESPECT fix review:** Fixed. The hex parse moved inside `try/except`, so malformed input returns `False` instead of crashing the run.
