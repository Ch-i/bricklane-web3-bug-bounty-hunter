---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-24-cyfrin-avant-requestmanagerv2-v2-0-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-24-cyfrin-avant-requestmanagerv2-v2-0
title: '`RequestsManagerV2` cache storage slots to prevent identical storage reads'
vuln_class: []
---

# `RequestsManagerV2` cache storage slots to prevent identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md)_

---

**Description:** Several functions in `RequestsManagerV2` read the same storage slot more than once within a single call even though the value does not change between reads. With the optimizer enabled but `via_ir` off, it does not dedupe same-slot reads across statement boundaries or around an intervening external call (a `safeTransfer`, `mint`, or `burn` forces a re-read because storage could have changed during the call), so each becomes a separate warm SLOAD (~100 gas). Caching each value into a local once and reusing it removes the redundant read:

1. **`RequestsManagerV2::completeMint`** - reads `mintFee` twice, in the fee calculation at src/RequestsManagerV2.sol:291 and the `MintRequestCompleted` emit at src/RequestsManagerV2.sol:304, with two external calls in between. Cache `uint64 fee = mintFee;`, mirroring `completeBurn` which already caches its per-request `fee`.

2. **`RequestsManagerV2::adminCancelMint`** - reads `request.provider` twice, at the `safeTransfer` (src/RequestsManagerV2.sol:267) and the emit (src/RequestsManagerV2.sol:269); the external transfer between them forces the second SLOAD. Cache `address provider = request.provider;` before the transfer.

3. **`RequestsManagerV2::adminCancelBurn`** - reads `request.provider` twice, at the `safeTransfer` (src/RequestsManagerV2.sol:384) and the emit (src/RequestsManagerV2.sol:386). Cache before the transfer.

4. **`RequestsManagerV2::requestMint`** - reads `mintRequestsCounter` at src/RequestsManagerV2.sol:216 then re-reads it via `mintRequestsCounter++` at src/RequestsManagerV2.sol:226. The pre-increment value is already held in the local `id`.

5. **`RequestsManagerV2::requestBurn`** - reads `burnRequestsCounter` at src/RequestsManagerV2.sol:325 then re-reads it via `burnRequestsCounter++` at src/RequestsManagerV2.sol:337. Same as above.

**Recommended Mitigation:** Cache each repeated read into a local before its first use and reuse the local. For the request counters, assign the incremented value directly instead of re-reading the slot:

```solidity
unchecked {
    mintRequestsCounter = id + 1;
}
```

For the provider re-reads, load the value before the external transfer so the post-call SLOAD is avoided:

```solidity
address provider = request.provider;
request.state = State.CANCELLED;
IERC20(request.token).safeTransfer(provider, request.amount);
emit MintRequestAdminCancelled(_id, provider, msg.sender);
```

**Avant:** Fixed in commit [96e36b5](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/96e36b548c88ed68594d0cf7f1b99cd4528dffc7).

**Cyfrin:** Verified.

\clearpage
