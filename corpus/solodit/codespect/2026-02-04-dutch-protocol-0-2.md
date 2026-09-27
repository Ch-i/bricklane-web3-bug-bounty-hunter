---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-0-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[H-03] DOS in _createVestingStreams(...) due to unbounded loop'
vuln_class: []
---

# [H-03] DOS in _createVestingStreams(...) due to unbounded loop

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`Presale.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/Presale.sol#L585)

**Description:**

The `_createVestingStreams(...)` function iterates over all contributors in a single transaction to create Sablier vesting streams. Each stream creation costs approximately 175,000–250,000 gas.

```solidity
function _createVestingStreams(uint256 totalTokens) internal {
    uint256 contributorCount = contributors.length;

    // @audit unbounded loop over all contributors
    for (uint256 i = 0; i < contributorCount; i++) {
        address contributor = contributors[i];
        // ...
        // @audit each call costs ~175,000-250,000 gas
        try sablierV2.createWithDurationsLL(params, unlockAmounts, durations)
            returns (uint256 streamId) {
            // ...
        } catch {
            // ...
        }
    }
}
```

With a block gas limit of 30 million, the function can only handle approximately 120–170 contributors before reverting. An attacker can exploit this by creating 200+ small contributions from different addresses during the presale. When the presale ends and `_createVestingStreams(...)` is called, the transaction reverts due to exceeding the block gas limit. This permanently locks all presale funds (both ETH and DUTCH tokens) with no recovery mechanism.

**Impact:** Lock of funds of all contributors.

**Recommendation:** Implement a batched claiming pattern where each contributor claims their own vesting stream.

**Status:** Fixed

**Client response:** Fixed in [5f12a82ae4dc706ae4a0891b272b22f69b0cea7f](https://github.com/dutch-protocol/Protocol-Contracts/commit/5f12a82ae4dc706ae4a0891b272b22f69b0cea7f)
